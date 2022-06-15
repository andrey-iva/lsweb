import logging
from .cart import Cart
from .models import Category
from .models import Product
from . import NO_IMAGE_PATH

from decimal import Decimal

def cart(request):
    return {'cart': Cart(request)}

def is_install(request):
    cart = Cart(request)
    total = 0
    for item in cart.cart.values():
        total += Decimal(item['price_install'])

    return {'is_install': int(total) > 0}

def currency(request):
    return {'currency': '₽'}

def categories(request):
    return {'categories': Category.objects.all()}

def no_image(request):
    return {'no_image': NO_IMAGE_PATH}

def get_services(request):
    return {'get_services': Product.objects.filter(product_type='услуга')}

def get_loop_id(request):
    try:
        product = Product.objects.get(attribute='loop')
    except Exception as e:
        logging.exception(e)
    else:
        return {'get_loop_id': product.id}

def get_loop_price(request):
    try:
        product = Product.objects.get(attribute='loop')
    except Exception as e:
        logging.exception(e)
    else:
        return {'get_loop_price': product.price}
