import retailcrm
import uuid
import time
import pickle
import logging
import json
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django import forms
# from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from yookassa import Payment

from threading import Thread, Lock
from decimal import Decimal

from ..cart import Cart
from ..models import OrderItem, Order
from .. import PAYMENT_REDIRECT_PAGE, PAYMENT_WAITING_TIME, ADMIN_EMAIL
from .. import ADMIN_EMAIL_ORDER_INFO, CART_SESSION_ID
from .. import RETAIL_HOST, RETAIL_CRM_ID, RETAIL_SITE, RETAIL_BRAND_CODE
from .. import WEIGHT, PERCENT
from pprint import pprint

lock = Lock()

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


def create_retail_order(order_id, copy_cart, params=None):
    logging.debug('Tread create_retail_order start: %s', order_id)
    delivery = {}
    dadata = {}
    items = []

    # client = retailcrm.v5(RETAIL_HOST, RETAIL_CRM_ID)

    if params['payment_method'] == 'paynow':
        time.sleep(PAYMENT_WAITING_TIME * 2)

    order = Order.objects.get(pk=order_id)

    logging.debug('yookassa_status: %s', order.yookassa_status)
    logging.debug('paid status: %s', order.paid)

    try:
        dadata = json.loads(order.address_full_info)
    except Exception as e:
        logging.debug('address_full_info not found: %s', e)

    order_c = {
        'firstName': order.first_name,
        'lastName': order.last_name,
        'phone': order.phone,
        'email': order.email,
        'customerComment': params.get('notes', '')
    }

    first_product = False
    install = False
    for item in copy_cart.values():
        product = item['product']
        if int(item['price_install']) > 0:
            install = True
    for item in copy_cart.values():
        product = item['product']
        if first_product is False:
            first_product = product

        items.append({
            'productName': product.name,
            'initialPrice': float(product.price),
            'purchasePrice': float(product.price),
            'quantity': item['quantity'],
        })
        if int(item['price_install']) > 0:
            items.append({
                'productName': 'Установка [' + product.name + ']',
                'initialPrice': float(item['total_price_install']),
                'purchasePrice': float(item['total_price_install']),
                'quantity': item['quantity'],
            })

    order_c['items'] = items
    if first_product:
        if first_product.product_type == 'кронштейн':
            order_c['orderType'] = 'kronshtejn'
            if install:
                order_c['orderType'] = 'kronshtejn-ustanovka'
            for item in copy_cart.values():
                product = item['product']
                if product.brand_car and product.model_car:
                    brand = product.brand_car.lower().capitalize()
                    model = product.model_car.lower().capitalize()
                    order_c['customFields'] = {
                        'machine_model': brand + ' ' + model,
                        'brand_of_the_machine': RETAIL_BRAND_CODE.get(brand.upper(),
                                                                      'no_information'),
                    }
                break

        if first_product.order_type == 'zamery':
            order_c['orderType'] = first_product.order_type
        if first_product.order_type == 'tretiy-ryad':
            order_c['orderType'] = first_product.order_type
        if first_product.order_type == 'kronshtejn-ustanovka':
            order_c['orderType'] = first_product.order_type
        if first_product.order_type == 'reyka-ind':
            order_c['orderType'] = first_product.order_type
        if first_product.order_type == 'reyka':
            order_c['orderType'] = first_product.order_type

    # самовывоз
    if params['payment_method'] == '0':
        order_c['payments'] = [
            {
                'type': 'cash',
                'status': 'payment-at-pickup'
            },
        ]
    # при получении сдек
    if params['payment_method'] == '5':
        order_c['payments'] = [{'type': 'cash-on-delivery'}]
    # картой сдек
    if params['payment_method'] == 'paynow':
        order_c['payments'] = [{'type': 'bank-card'}]

        if order.paid:
            order_c['payments'] = [
                {
                    'type': 'bank-card',
                    'externalId': params.get('payment_id', ''),
                    'amount': str(order.grand_total),
                    'status': 'paid',
                },
            ]

    if params.get('tariff_code'):
        p = 0
        # сумма наложенного платежа
        if params['payment_method'] == '5':
            p = (params['cart_total_price'] + Decimal(params['delivery_sum'])) * \
                Decimal(PERCENT) / Decimal(100)
        delivery = {
            'code': 'sdek',
            'integrationCode': 'sdek',
            'cost': str(Decimal(params['delivery_sum']) + p),
            'address': {
                'countryIso': dadata['data'].get('country_iso_code', ''),
                'city': dadata['data'].get('city_with_type', ''),
                'region': dadata['data'].get('region_with_type', ''),
                'city': dadata['data'].get('city_with_type', ''),
                'street': params.get('street', '').capitalize(),
                'building': params.get('building', ''),
                'flat': params.get('flat', ''),
                'text': order.address,
            },
            'data': {
                'pickuppointId': params.get('pvz_code', ''),
                'tariff': params['tariff_code'],
            },
        }
    else:
        delivery = {
            'code': 'self-delivery',
        }

    order_c['delivery'] = delivery

    pprint(order_c)
    # 'get_error_msg', 'get_errors', 'get_response', 'get_status_code', 'is_successful'
    # result = client.order_create(order_c, RETAIL_SITE)
    # res = result.get_response()
    # pprint(res)
    # lock.acquire()
    # if res['success'] is True:
    #     order.retail_crm_status = str(res['id'])
    # if res['success'] is False:
    #     order.retail_crm_status = 'FAIL'
    # order.save()
    # lock.release()
    # if result.get_errors():
    #     logging.error('Retail error: %s', result.get_errors())
    # logging.debug('Tread create order finish status: %s', result.get_status_code())
    logging.debug('Tread create_retail_order finish status: %s', 'end')


def order_info(order_id, copy_cart):
    order = Order.objects.get(pk=order_id)

    html = ''
    for item in copy_cart.values():
        product = item['product']
        price = str(item['price_install'])
        install = 'Да ' + price if int(item['price_install']) > 0 else 'Нет '
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
            lock.acquire()
            order.yookassa_status = 'unknown'
            order.save()
            lock.release()
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
    lock.acquire()
    order.yookassa_status = payment.status
    if status == 'succeeded':
        order.paid = paid
        order.yookassa_id = payment_id
        order.yookassa_amount = payment.amount.value
        order.yookassa_full_info = pickle.dumps(payment)
    order.save()
    lock.release()

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
    # percent = 0
    if len(cart) == 0:
        return redirect('shop:product_list')

    errorMessage = None
    if request.method == 'POST':
        request_post = request.POST.copy()
        request_post['cart_total_price'] = cart.get_total_price()
        idempotence_key = uuid.uuid4()

        if request_post['payment_method'] == '5':
            delivery_sum = request_post['delivery_sum']
            logging.debug('cart total: %s', cart.get_total_price())
            logging.debug('delivery sum: %s', Decimal(delivery_sum))
            logging.debug('percent: %s', Decimal(PERCENT))
            p = (cart.get_total_price() +
                 Decimal(delivery_sum)) * Decimal(PERCENT) / Decimal(100)
            gt = (cart.get_total_price() + Decimal(delivery_sum)) + p
            logging.debug('grand total: %s', gt)
        else:
            gt = cart.get_total_price() + Decimal(request_post['delivery_sum'])

        # gtl = Decimal(cart.get_total_price()) + percent
        # gtr = Decimal(request_post['delivery_sum'])
        # gt = gtl + gtr
        request_post['grand_total'] = Decimal('%.2f' % gt)

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

            # Thread(target=create_retail_order, args=(order.id, copy_cart, request_post)).start()

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
                request_post['payment_id'] = payment.id
                Thread(target=create_retail_order, args=(order.id, copy_cart, request_post)).start()

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

            Thread(target=create_retail_order, args=(order.id, copy_cart, request_post)).start()

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
