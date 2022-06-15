from .cart import Cart
from .models import Category
from .models import Product
from . import NO_IMAGE_PATH

def cart(request):
    return {'cart': Cart(request)}

def currency(request):
    return {'currency': '₽'}

def categories(request):
    return {'categories': Category.objects.all()}

def no_image(request):
    return {'no_image': NO_IMAGE_PATH}

def get_services(request):
    return {'get_services': Product.objects.filter(product_type='услуга')}

def get_loop_id(request):
    product = Product.objects.get(attribute='loop')
    return {'get_loop_id': product.id}

def get_loop_price(request):
    product = Product.objects.get(attribute='loop')
    return {'get_loop_price': product.price}
