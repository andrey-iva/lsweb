from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from decimal import Decimal

from .. import CART_SESSION_ID, NO_IMAGE_PATH, GRAND_TOTAL_ID
from ..models import Product
from ..cart import Cart
from ..ctx_proc import currency

import json

@require_POST
def cart_add(request, product_id):
    print(product_id)
    try:
        quantity = int(request.POST.get('quantity'))
        override = int(request.POST.get('override'))
        install = int(request.POST.get('price_install') or 0)
    except Exception as e:
        print(e)
    else:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        if quantity > 0:
            cart.add(product=product, 
                    quantity=quantity,
                    override_quantity=override,
                    install=install)

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

    if delivery_tax and request.session.get(GRAND_TOTAL_ID):
        if int(delivery_tax) >= 0:
            grand_total = Decimal(request.session[GRAND_TOTAL_ID]['price']) + Decimal(delivery_tax)
            request.session[GRAND_TOTAL_ID]['price'] = str(grand_total)
            request.session.modified = True

            return HttpResponse(json.dumps({
                    'grand_total': currency(request)['currency'] + str(grand_total)
                }))

    return HttpResponse(json.dumps({'error': 'fail add delivery tax!'}))

@require_POST
def add_percent(request):
    request.session[GRAND_TOTAL_ID] = {}
    percent = request.POST.get('percent')
    grand_total = 0

    cart = Cart(request)

    if percent is not None:
        if int(percent) >= 0:
            percent = (cart.get_total_price() / Decimal(100)) * Decimal(percent)
            grand_total = cart.get_total_price() + percent
            
            request.session[GRAND_TOTAL_ID]['price'] = str(grand_total)
            request.session.modified = True

            return HttpResponse(json.dumps({
                    'grand_total': currency(request)['currency'] + str(grand_total)
                }))


    return HttpResponse(json.dumps({'error': 'no add percent!'}))

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)


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
                'price_install': currency(request)['currency'] + str(item['price_install'])
            }
        response_data['sub_total'] = currency(
            request)['currency'] + str(cart.get_total_price())
        response_data['cart_length'] = str(len(cart))
        return HttpResponse(json.dumps(response_data))
    else:
        return HttpResponse(json.dumps({'cart': 'empty'}))
    return redirect('shop:product_list')

@require_POST
def get_grand_total(request):
    if request.session.get(GRAND_TOTAL_ID):
        return HttpResponse(json.dumps({'grand_total': request.session.get(GRAND_TOTAL_ID)}))
    return HttpResponse(json.dumps({'error': 'error get_grand_total'}))

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('shop:product_list')
