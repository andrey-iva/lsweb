import json, uuid, time, pickle, logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from yookassa import Configuration, Payment

from threading import Thread
from decimal import Decimal

from ..cart import Cart
from ..models import OrderItem, Order
from .. import GRAND_TOTAL_ID, PAYMENT_REDIRECT_PAGE, ADMIN_EMAIL
from pprint import pprint

format = '%(asctime)s: %(message)s'
logging.basicConfig(format=format, level=logging.INFO, datefmt='%H:%M:%S')


# Configuration.account_id = <Идентификатор магазина>
# Configuration.secret_key = <Секретный ключ>

def get_subject(order_id):
    return f'iSOFIX-MSK Заказ №{order_id}'

def get_message(order_id, order_name):
    return f'''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>ifsofix-msk</title>
</head>
<body>
    <div style="text-align: center;">
        <h2>iSOFIX-MSK</h2>
        <p>Заказ №{order_id}</p>
        <p>Уважаемый {order_name}, благодарим вас за заказ!</p>
    </div>
</body>
</html>'''

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'delivery_type', 'address_full_info',
            'grand_total', 'first_name', 'last_name',
            'country', 'region', 'address', 'postal_code',
            'phone', 'email', 'notes'
        ]

def payment_status(payment_id, order):
    # logging.info("Thread %s: starting", payment_id)
    payment = Payment.find_one(payment_id)
    status = payment.status
    paid = payment.paid
    count = 0
    
    # print(pickle.loads(r))
    while status == 'pending':
        if count == 600:
            order.yookassa_status = 'unknown'
            order.save()
            # logging.info("Thread %s: finishing", payment_id)
            return
        payment = Payment.find_one(payment_id)
        status = payment.status
        paid = payment.paid
        # print('status>>', status)
        count += 1
        time.sleep(1)
    # print('status>>', status)
    order.yookassa_status = payment.status
    if status == 'succeeded':
        order.paid = paid
        order.yookassa_id = payment_id
        order.yookassa_amount = payment.amount.value
        order.yookassa_full_info = pickle.dumps(payment)
    order.save()
    # logging.info("Thread %s: finishing", payment_id)

def get_percent(total_price, percent):
    return (total_price / Decimal(100)) * Decimal(percent)

def clear_grand_total(request):
    ''' js калькулятор '''
    if request.session.get(GRAND_TOTAL_ID):
        request.session[GRAND_TOTAL_ID]['price'] = '0.0'
        request.session.modified = True

@require_POST
def del_grand_total_session(request):
    ''' js калькулятор '''
    clear_grand_total(request)
    return HttpResponse(json.dumps({'info': 'set GRAND_TOTAL_ID[price] = 0.0'}))

def order_create(request):
    cart = Cart(request)
    percent = 0
    if len(cart) == 0:
        return redirect('shop:product_list')

    errorMessage = None
    if request.method == 'POST':
        request_post = request.POST.copy()
        idempotence_key = uuid.uuid4()
        
        if request_post['payment_method'] == '5':
            percent = get_percent(cart.get_total_price(), 5)
        
        request_post['grand_total'] = str( 
            (Decimal(cart.get_total_price()) + percent) + Decimal(request_post['delivery_sum']) )

        form = OrderCreateForm(request_post)
        if form.is_valid():
            order = form.save()

            for item in cart:
                install_product = int(item['price_install']) > 0
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         install=install_product,
                                         price=item['price'],
                                         price_install=item['price_install'],
                                         quantity=item['quantity'])
            cart.clear()
            clear_grand_total(request)
            # send mail
            # request.session.flush()

            if request_post['payment_method'] == 'paynow':
                payment = Payment.create({
                    'amount': {
                        'value': order.grand_total,
                        'currency': 'RUB'
                    },
                    'confirmation': {
                        'type': 'redirect',
                        'return_url': PAYMENT_REDIRECT_PAGE
                    },
                    'capture': True,
                    'description': 'Заказ №' + str(order.id)
                }, idempotence_key)

                request.session['order_id'] = str(order.id)
                request.session['payment_id'] = str(payment.id)
                request.session.modified = True

                Thread(target=payment_status, args=(payment.id, order)).start()
                Thread(target=send_mail, args=(
                        get_subject(order.id),
                        get_message(order.id, order.first_name),
                        ADMIN_EMAIL, [order.email]
                    )).start()

                return redirect(payment.confirmation.confirmation_url)
            
            Thread(target=send_mail, args=(
                    get_subject(order.id),
                    get_message(order.id, order.first_name),
                    ADMIN_EMAIL, [order.email]
                 )).start()
            request.session['order_id'] = str(order.id)    
            request.session.modified = True

            return redirect('shop:order_created')
        else:
            errorMessage = 'Проверте введенные данные!'

    return render(request, 'shop/order/create.html', {
        'cart': cart,
        'errorMessage': errorMessage,
        'deactivate_mini_cart': True,
    })


def order_created(request):
    data = {}
    payment_id = request.session.get('payment_id')
    order_id   = request.session.get('order_id')

    if payment_id is None and order_id is None:
        return redirect('shop:shop_page')

    if payment_id and order_id:
        payment = Payment.find_one(payment_id)
        data['status'] = payment.status
        data['paid']   = payment.paid
    
    data['order_id'] = order_id

    if payment_id:
        del request.session['payment_id']
    if order_id:
        del request.session['order_id']
    request.session.modified = True

    return render(request, 'shop/order/created.html', data)
