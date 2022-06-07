import json, uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.views.decorators.http import require_POST
from ..cart import Cart
from ..models import OrderItem, Order
from .. import GRAND_TOTAL_ID
from pprint import pprint
# from ..tasks import order_created
from yookassa import Configuration, Payment

# Configuration.account_id = <Идентификатор магазина>
# Configuration.secret_key = <Секретный ключ>

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_type', 'grand_total', 'first_name', 'last_name', 'country', 'region',
        'address', 'postal_code', 'phone', 'email', 'notes']

def clear_grand_total(request):
    if request.session.get(GRAND_TOTAL_ID):
        del request.session[GRAND_TOTAL_ID]
        request.session.modified = True

@require_POST
def del_grand_total_session(request):
    clear_grand_total(request)
    return HttpResponse(json.dumps({'info': 'del GRAND_TOTAL_ID'}))

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:product_list')

    errorMessage = None
    if request.method == 'POST':
        request_post = request.POST.copy()
        idempotence_key = uuid.uuid4()

        if request.session.get(GRAND_TOTAL_ID):
            request_post['grand_total'] = str(request.session[GRAND_TOTAL_ID]['price'])
            # request_post['grand_total'] = str(cart.get_total_price())
        # pprint(request_post)
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
                        'return_url': 'http://127.0.0.1:8000/order/created/'
                    },
                    'capture': True,
                    'description': 'Заказ №' + str(order.id)
                }, idempotence_key)

                request.session['order_id'] = str(order.id)
                request.session['payment_id'] = str(payment.id)
                request.session.modified = True

                return redirect(payment.confirmation.confirmation_url)
            
            request.session['order_id'] = str(order.id)    
            request.session.modified = True

            return redirect('shop:order_created', order.id)
        else:
            errorMessage = 'Проверте введенные данные!'

    return render(request, 'shop/order/create.html', {
        'cart': cart,
        'errorMessage': errorMessage,
        'deactivate_mini_cart': True,
    })


def order_created(request, order_id=None):
    # "status": "succeeded", "paid": true,
    data = {}
    payment_id = request.session.get('payment_id')
    order_id   = request.session.get('order_id')

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
    pprint(data)
    return render(request, 'shop/order/created.html', data)
