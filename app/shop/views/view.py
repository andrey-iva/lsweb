from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import logging
from django import forms
from pprint import pprint

from ..models import Message
from ..models import Post, Product

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'subject', 'email', 'notes']

def home(request):
	try:
		posts    = Post.objects.filter(status='published')[0:10]
		products = Product.objects.filter(available=True)

		brackets = products.filter(product_type='кронштейн')[0:10]
		rails    = products.filter(product_type='рейка')[0:10]
		services = products.filter(product_type='услуга')[0:10]

	except Exception as e:
		logging.debug(e)

	return render(request, 'shop/index.html', {
			'posts': posts,
			'brackets': brackets,
			'rails': rails,
			'services': services,
			'products': products[0:10],
		})

def about(request):
	return render(request, 'shop/adout.html')

def shipping_payment(request):
	return render(request, 'shop/shipping_payment.html')

def pdd(request):
	return render(request, 'shop/pdd.html')

def contact(request, message=None):
	return render(request, 'shop/contact.html', {'message': message})

def policy(request):
	return render(request, 'shop/policy.html')

@require_POST
def contact_send_message(request):
	successMessage = 'Ваше сообщение отправлено!'
	errorMessage = 'Произошла ошибка при отправке сообщения!'

	form = MessageCreateForm(request.POST)
	if form.is_valid():
		form.save()
		return redirect('shop:contact', successMessage)
	
	return redirect('shop:contact', errorMessage)
