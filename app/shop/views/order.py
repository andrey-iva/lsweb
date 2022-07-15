# import json
import retailcrm
import uuid
import time
import pickle
import logging
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django import forms
# from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from yookassa import Payment

from threading import Thread
from decimal import Decimal, getcontext

from ..cart import Cart
from ..models import OrderItem, Order
from .. import PAYMENT_REDIRECT_PAGE, PAYMENT_WAITING_TIME, ADMIN_EMAIL
from .. import ADMIN_EMAIL_ORDER_INFO, CART_SESSION_ID
from .. import RETAIL_HOST, RETAIL_CRM_ID, RETAIL_SITE
from .. import WEIGHT
from pprint import pprint


def get_subject(order_id):
    return f'iSOFIX-MSK Заказ №{order_id}'


def shopper_message(order_id, order_name):
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


def create_retail_order(order_id, copy_cart, percent, delivery_sum, params=None):
    logging.debug('Tread create_retail_order start: %s', order_id)
    client = retailcrm.v5(RETAIL_HOST, RETAIL_CRM_ID)
    order = Order.objects.get(pk=order_id)
    # address = f'{order.country} {order.region} {order.address}'.strip()
    order_c = {
        'firstName': order.first_name,
        'lastName': order.last_name,
        'phone': order.phone,
        'email': order.email,
    }
    items = []
    for item in copy_cart.values():
        product = item['product']

        items.append({
            'productName': product.name,
            'initialPrice': float(product.price),
            'purchasePrice': float(product.price),
            'quantity': item['quantity'],
        })
        if int(item['price_install']) > 0:
            items.append({
                'productName': 'Установка -> ' + product.name,
                'initialPrice': float(item['total_price_install']),
                'purchasePrice': float(item['total_price_install']),
                'quantity': item['quantity'],
            })

    order_c['items'] = items

    delivery = {}
    if params['city'] and params['country_iso'] and params['pvz_code'] and params['tariff']:
        if params['payment_method']:

            paym = ''
            if params['payment_method'] == '5':
                paym = 'cash-on-delivery'
                # paym = 'cash'
                delivery_sum = delivery_sum + percent
            if params['payment_method'] == 'paynow':
                paym = 'bank-card'

            delivery = {
                'code': 'sdek',
                'integrationCode': 'sdek',
                'address': {
                    'countryIso': params['country_iso'],
                    'city': params['city'],
                },
                'data': {
                    'pickuppointId': params['pvz_code'],
                    'tariff': params['tariff'],
                },
            }
            order_c['payments'] = [{'type': paym}]
    else:
        if params['payment_method'] == '0':
            delivery = {
                'code': 'self-delivery',
            }
            order_c['payments'] = [{'type': 'cash'}]

        if params['payment_method'] == 'paynow':
            delivery = {
                'code': 'self-delivery',
            }
            order_c['payments'] = [{'type': 'bank-card'}]

    order_c['delivery'] = delivery
    pprint(order_c)
    result = client.order_create(order_c, RETAIL_SITE)
    # 'get_error_msg', 'get_errors', 'get_response', 'get_status_code', 'is_successful'
    logging.debug('Retail response status: %s', result.get_response())
    logging.debug('Tread create_retail_order finish status: %s', result.get_status_code())


def order_info(order_id, copy_cart):
    order = Order.objects.get(pk=order_id)

    html = ''
    for item in copy_cart.values():
        product = item['product']
        price = str(item['price_install'])
        install = 'Да ' + price if int(item['price_install']) > 0 else '-'
        quantity = item['quantity']
        html += '\n<ul>\n'
        html += f'\t<li>{product.name}</li>\n'
        html += f'\t<li>{product.item_number}</li>\n'
        html += f'\t<li>{product.price}</li>\n'
        html += f'\t<li>Кол-во: {quantity} шт</li>\n'
        html += f'\t<li>Установка: {install} </li>\n'
        html += '\n</ul>\n'

    return f'''
<h3>Информация о заказе №{order_id}</h3>
<hr>
<ul>
    <li><b>Покупатель</b></li>
    <li>Имя: {order.first_name}</li>
    <li>Фамилия: {order.last_name}</li>
    <li>Телефон: {order.phone}</li>
    <li>Адрес: {order.address}</li>
    <li>Доставка: {order.delivery_type}</li>
    <li>Сумма заказа: {order.grand_total}</li>
</ul>
<h3>Продукты</h3>
<hr>
<ul>
    {html}
</ul>
'''


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'policy', 'delivery_type', 'address_full_info',
            'grand_total', 'first_name', 'last_name',
            'country', 'region', 'address', 'postal_code',
            'phone', 'email', 'notes'
        ]


def payment_status(payment_id, order_id, wait_time):
    '''Отслеживание состояния платежа'''
    order = Order.objects.get(pk=order_id)
    logging.debug("Thread %s: starting", payment_id)

    payment = Payment.find_one(payment_id)
    status = payment.status
    paid = payment.paid
    count = 0

    # print(pickle.loads(r))
    while status == 'pending':
        if count == wait_time:
            order.yookassa_status = 'unknown'
            order.save()
            logging.debug("Thread %s: finishing", payment_id)
            return
        payment = Payment.find_one(payment_id)
        status = payment.status
        paid = payment.paid
        if status == 'succeeded':
            break
        if status == 'canceled':
            break
        count += 1
        time.sleep(1)

    order.yookassa_status = payment.status
    if status == 'succeeded':
        order.paid = paid
        order.yookassa_id = payment_id
        order.yookassa_amount = payment.amount.value
        order.yookassa_full_info = pickle.dumps(payment)
    order.save()

    logging.debug("Thread %s: finishing", payment_id)


def get_percent(total_price, percent):
    # return (total_price / Decimal(100)) * Decimal(percent)
    return total_price * Decimal((1 + percent / 100))


def send_MAIL(subject, message, from_email, to_email):
    logging.debug('Thread start send_EMAIL: %s', subject)
    try:
        send_mail(subject, message, from_email, to_email)
    except Exception as e:
        logging.exception('Thread finish send_EMAIL: %s', e)
    logging.debug('Thread finish send_EMAIL: %s', subject)


def order_create(request):
    cart = Cart(request)
    copy_cart = request.session.get(CART_SESSION_ID).copy()
    percent = 0
    if len(cart) == 0:
        return redirect('shop:product_list')

    errorMessage = None
    if request.method == 'POST':
        request_post = request.POST.copy()
        idempotence_key = uuid.uuid4()

        getcontext().prec = 6
        if request_post['payment_method'] == '5':
            gt = (cart.get_total_price() + Decimal(request_post['delivery_sum'])) * Decimal(1 + 5.2631 / 100)
        else:
            gt = cart.get_total_price() + Decimal(request_post['delivery_sum'])

        # gtl = Decimal(cart.get_total_price()) + percent
        # gtr = Decimal(request_post['delivery_sum'])
        # gt = gtl + gtr
        request_post['grand_total'] = str(gt)

        pprint(request_post)
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
            # clear_grand_total(request)
            # send mail
            # request.session.flush()
            
            # Thread(target=create_retail_order,
            #        args=(order.id, copy_cart, percent, Decimal(request_post['delivery_sum']), {
            #            'city': request.POST.get('cdek_city'),
            #            'country_iso': request.POST.get('cdek_country_iso'),
            #            'pvz_code': request.POST.get('pvz_code'),
            #            'tariff': request.POST.get('tariff_code'),
            #            'payment_method': request.POST.get('payment_method')
            #        }.copy())
            #        ).start()

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
                # payment status, set wait time shop/__init__
                Thread(target=payment_status, args=(
                    payment.id, order.id, PAYMENT_WAITING_TIME)).start()
                # client
                Thread(target=send_MAIL, args=(
                    get_subject(order.id),
                    shopper_message(order.id, order.first_name),
                    ADMIN_EMAIL, [order.email]
                )).start()
                # admin
                Thread(target=send_MAIL, args=(
                    get_subject(order.id),
                    order_info(order.id, copy_cart),
                    ADMIN_EMAIL, [ADMIN_EMAIL_ORDER_INFO]
                )).start()
                # retail
                # Thread(target=create_retail_order, args=(
                #     order.id, copy_cart, percent, gtr, payment.id)).start()

                return redirect(payment.confirmation.confirmation_url)

            Thread(target=send_MAIL, args=(
                get_subject(order.id),
                shopper_message(order.id, order.first_name),
                ADMIN_EMAIL, [order.email]
            )).start()
            # admin
            Thread(target=send_MAIL, args=(
                get_subject(order.id),
                order_info(order.id, copy_cart),
                ADMIN_EMAIL, [ADMIN_EMAIL_ORDER_INFO]
            )).start()
            request.session['order_id'] = str(order.id)
            request.session.modified = True

            # Thread(target=create_retail_order,
            #        args=(order.id, copy_cart, percent, gtr)).start()

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
    order_id = request.session.get('order_id')

    if payment_id is None and order_id is None:
        return redirect('shop:shop_page')

    if payment_id and order_id:
        payment = Payment.find_one(payment_id)
        logging.debug('Order crested PAYMENT status {%s}', payment.status)
        # если клиет вернулся status penging
        data['status'] = payment.status
        data['paid'] = payment.paid

    data['order_id'] = order_id

    if payment_id:
        del request.session['payment_id']
    if order_id:
        del request.session['order_id']
    request.session.modified = True

    return render(request, 'shop/order/created.html', data)
