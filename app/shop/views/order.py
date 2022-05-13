import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from ..cart import Cart
from ..models import OrderItem, Order
# from ..tasks import order_created


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'country', 'region',
        'address', 'postal_code', 'phone', 'email', 'notes']


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:product_list')

    errorMessage = None
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # send mail
            return redirect('shop:order_created', order.id)
        else:
            errorMessage = 'Проверте введенные данные!'

    return render(request, 'shop/order/create.html', {
        'cart': cart,
        'errorMessage': errorMessage,
        'deactivate_mini_cart': True,
    })


def order_created(request, order_id):
    return render(request, 'shop/order/created.html', {'order_id': order_id})
