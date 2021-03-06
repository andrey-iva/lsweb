from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from decimal import Decimal

from .. import CART_SESSION_ID, NO_IMAGE_PATH, PERCENT
from ..models import Product
from ..cart import Cart
from ..ctx_proc import currency

import json
import logging


@require_POST
def cart_add(request, product_id):
    try:
        quantity = int(request.POST.get('quantity'))
        override = int(request.POST.get('override'))
        install = int(request.POST.get('price_install') or 0)
        loop = request.POST.get('loop')
    except Exception as e:
        print(e)
    else:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        if quantity > 0:
            cart.add(product=product,
                     quantity=quantity,
                     override_quantity=override,
                     install=install,
                     loop=loop)

            if request.headers.get('X-Requested-With'):
                price = Decimal(cart.cart[str(product_id)]['price']) * quantity
                price_install = Decimal(cart.cart[str(product_id)]['price_install']) * quantity

                total_price = currency(request)['currency'] + str(price)
                total_price_install = currency(request)['currency'] + str(price_install)

                sub_total = currency(
                    request)['currency'] + str(cart.get_total_price())

                return HttpResponse(json.dumps({
                    'product_id': product_id,
                    'result': 'update',
                    'total_price': total_price,
                    'total_price_install': total_price_install,
                    'sub_total': sub_total,
                    'cart_length': len(cart),
                }))

    return redirect('shop:cart_detail')


@require_POST
def add_delivery_tax(request):
    delivery_tax = request.POST.get('delivery_tax')
    grand_total = 0
    cart = Cart(request)

    if delivery_tax:
        if int(delivery_tax) >= 0:
            grand_total = Decimal(cart.get_total_price()) + Decimal(delivery_tax)

            return HttpResponse(json.dumps({
                'grand_total': str(grand_total)
            }))

    return HttpResponse(json.dumps({'error': 'fail add delivery tax!'}))


@require_POST
def add_percent(request):
    percent = request.POST.get('percent')
    delivery_sum = request.POST.get('delivery_sum')
    grand_total = 0

    cart = Cart(request)

    if percent is not None:
        if int(percent) >= 0:
            percent = str(PERCENT) if int(percent) > 0 else '0'
            logging.debug('percent %s', percent)
            logging.debug('delivery_sum %s', delivery_sum)
            # percent = ((cart.get_total_price() + Decimal(delivery_sum)) /
            #            Decimal(100)) * Decimal(percent)
            # grand_total = (cart.get_total_price() + Decimal(delivery_sum)) + percent
            p = (cart.get_total_price() + Decimal(delivery_sum)) * Decimal(percent) / Decimal(100)
            grand_total = (cart.get_total_price() + Decimal(delivery_sum)) + p

            return HttpResponse(json.dumps({
                'grand_total': str(grand_total)
            }))

    return HttpResponse(json.dumps({'error': 'no add percent!'}))


@require_POST
def set_loop_marker_on(request, product_id):
    if request.session[CART_SESSION_ID].get(str(product_id)):
        request.session[CART_SESSION_ID][str(product_id)]['loop'] = 'on'
        request.session.modified = True
        return HttpResponse(f'set marker for product {product_id} OK')
    return HttpResponse(f'set marker for product {product_id} FAIL')


@require_POST
def remove_loop_marker(request):
    for item in request.session[CART_SESSION_ID].values():
        if 'loop' in item:
            item['loop'] = 'off'
    request.session.modified = True
    return HttpResponse('remove markers')


@require_POST
def cart_count_quantity(request):
    cart = Cart(request)
    quantity_on = 0
    for item in cart:
        if item.get('loop_quantity'):
            quantity_on += int(item['quantity'])

    return HttpResponse(json.dumps({'quantity_on': str(quantity_on)}))


@require_POST
def cart_loop_off(request, product_id):
    ''' ?????????????? ?????????????? loop: on '''
    if request.session.get(CART_SESSION_ID):
        if request.session[CART_SESSION_ID][str(product_id)].get('loop'):
            del request.session[CART_SESSION_ID][str(product_id)]['loop']
            request.session.modified = True
            return HttpResponse(json.dumps({'loop_del': 'ok'}))

    return HttpResponse(json.dumps({'loop_del': 'no'}))


@require_POST
def cart_remove_loop(request, product_id):
    ''' ?????????????????????? ?????? ?????????????????? ???????????? ???????????????? ?????????????????? '''
    logging.debug('cart_remove_loop %s', product_id)
    if request.session[CART_SESSION_ID].get(str(product_id)):
        qty = int(request.POST.get('quantity'))

        cart = Cart(request)
        # product only loop
        cart.session[CART_SESSION_ID][str(product_id)]['loop_quantity'] = 0
        cart.save()

        product = get_object_or_404(Product, attribute='loop')
        quantity = 0

        for item in cart.cart.values():
            if item.get('loop_quantity'):
                quantity += int(item['loop_quantity'])

        if quantity <= 0 and cart.session[CART_SESSION_ID].get(str(product.id)):
            del cart.session[CART_SESSION_ID][str(product.id)]
        else:
            if cart.session[CART_SESSION_ID].get(str(product.id)):
                cart.session[CART_SESSION_ID][str(product.id)]['quantity'] = quantity
        cart.save()

        return HttpResponse(json.dumps({"loop_quantity": quantity}))
    return HttpResponse(json.dumps({"loop_quantity": 'fail'}))


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if (product.attribute == 'loop'):
        for item in cart.cart.values():
            if item.get('loop_quantity'):
                del item['loop_quantity']
        cart.save()

    if request.headers.get('X-Requested-With'):
        sub_total = currency(
            request)['currency'] + str(cart.get_total_price())
        return HttpResponse(json.dumps({
            'product_id': product_id,
            'result': 'remove',
            'sub_total': sub_total,
            'cart_length': len(cart),
        }))
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart/detail.html', {
        'cart': cart,
        'deactivate_mini_cart': True,
    })


def cart_json(request):
    cart = Cart(request)
    response_data = {}

    if len(cart) and request.headers.get('X-Requested-With'):
        for item in cart:
            product = item['product']
            image = NO_IMAGE_PATH
            if product.image_base:
                image = product.image_base.url
            response_data[str(product.id)] = {
                'name': product.name,
                'image': image,
                'price': currency(request)['currency'] + str(product.price),
                'total_price': currency(request)['currency'] + str(item['total_price']),
                'quantity': item['quantity'],
                'product_url': product.get_absolute_url(),
                'price_install': currency(request)['currency'] + str(item['price_install']),
                'attribute': product.attribute
            }
        response_data['sub_total'] = currency(
            request)['currency'] + str(cart.get_total_price())
        response_data['cart_length'] = str(len(cart))
        return HttpResponse(json.dumps(response_data))
    # else:
    #     return HttpResponse(json.dumps({'cart': 'empty'}))
    return redirect('shop:product_list')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('shop:product_list')
