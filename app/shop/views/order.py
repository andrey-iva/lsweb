import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from ..cart import Cart
from ..models import OrderItem, Order
from .. import GRAND_TOTAL_ID
# from ..tasks import order_created


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_type', 'grand_total', 'first_name', 'last_name', 'country', 'region',
        'address', 'postal_code', 'phone', 'email', 'notes']

def clear_grand_total(request):
    if request.session.get(GRAND_TOTAL_ID):
        del request.session[GRAND_TOTAL_ID]
        request.session.modified = True

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:product_list')

    errorMessage = None
    if request.method == 'POST':
        request_post = request.POST.copy()

        if request.session.get(GRAND_TOTAL_ID):
            request_post['grand_total'] = str(request.session[GRAND_TOTAL_ID]['price'])
        
        form = OrderCreateForm(request_post)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            clear_grand_total(request)
            # send mail
            return redirect('shop:order_created', order.id)
        else:
            errorMessage = 'Проверте введенные данные!'
    
    if request.session.get(GRAND_TOTAL_ID):
        request.session[GRAND_TOTAL_ID].clear()
        # request.session.modified = True

    return render(request, 'shop/order/create.html', {
        'cart': cart,
        'errorMessage': errorMessage,
        'deactivate_mini_cart': True,
    })


def order_created(request, order_id):
    return render(request, 'shop/order/created.html', {'order_id': order_id})
