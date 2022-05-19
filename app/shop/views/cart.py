from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from decimal import Decimal

from .. import CART_SESSION_ID, GRAND_TOTAL_SESSION_ID, NO_IMAGE_PATH
from ..models import Product
from ..cart import Cart
from ..ctx_proc import currency

import json


@require_POST
def cart_add(request, product_id):
    try:
        quantity = int(request.POST.get('quantity'))
        override = int(request.POST.get('override'))
    except Exception as e:
        print(e)
    else:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        if quantity > 0:
            if request.session.get(GRAND_TOTAL_SESSION_ID):
                del request.session[GRAND_TOTAL_SESSION_ID]
            cart.add(product=product, quantity=quantity,
                     override_quantity=override)

            if request.headers.get('X-Requested-With'):
                price = Decimal(cart.cart[str(product_id)]['price']) * quantity
                total_price = currency(request)['currency'] + str(price)
                sub_total = currency(
                    request)['currency'] + str(cart.get_total_price())

                return HttpResponse(json.dumps({
                    'product_id': product_id,
                    'result': 'update',
                    'total_price': total_price,
                    'sub_total': sub_total,
                    'cart_length': len(cart)
                }))

    return redirect('shop:cart_detail')


@require_POST
def add_delivery_tax(request):
    request.session[GRAND_TOTAL_SESSION_ID] = {}

    delivery_tax = request.POST.get('delivery_tax')
    tariff_code = request.POST.get('tariff_code')
    grand_total = 0
    cart = Cart(request)

    if delivery_tax and tariff_code:
        grand_total = cart.get_total_price() + Decimal(delivery_tax)
        request.session[GRAND_TOTAL_SESSION_ID]['total_price'] = str(grand_total)
        request.session[GRAND_TOTAL_SESSION_ID]['tariff_code'] = str(tariff_code)
        request.session.modified = True

        return HttpResponse(json.dumps({
                'ok': True,
                'grand_total': currency(request)['currency'] + str(grand_total)
            }))
    
    return HttpResponse(json.dumps({'error': 'add delivery tax!'}))


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.session.get(GRAND_TOTAL_SESSION_ID):
        del request.session[GRAND_TOTAL_SESSION_ID]

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
            }
        response_data['sub_total'] = currency(
            request)['currency'] + str(cart.get_total_price())
        response_data['cart_length'] = str(len(cart))
        return HttpResponse(json.dumps(response_data))
    else:
        return HttpResponse(json.dumps({'cart': 'empty'}))
    return redirect('shop:product_list')


def cart_clear(request):
    if request.session.get(GRAND_TOTAL_SESSION_ID):
        del request.session[GRAND_TOTAL_SESSION_ID]
    cart = Cart(request)
    cart.clear()
    return redirect('shop:product_list')
