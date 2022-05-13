from .cart import Cart
from .models import Category
from . import NO_IMAGE_PATH

def cart(request):
    return {'cart': Cart(request)}

def currency(request):
    return {'currency': '₽'}

def categories_menu(request):
    return {'categories_menu': Category.objects.all()}

def no_image(request):
    return {'no_image': NO_IMAGE_PATH}
