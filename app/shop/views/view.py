from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django import forms
from pprint import pprint
from yookassa import Configuration, Payment

from ..models import Message

import json

Configuration.account_id = '916494'
Configuration.secret_key = 'test_ptA6-o_oaTCYnc9R0Fvh-WIXe50UNgXKIUob2qZT86I'

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'subject', 'email', 'notes']

def home(request):
	return render(request, 'shop/index.html')

def about(request):
	return render(request, 'shop/adout.html')

def shipping_payment(request):
	return render(request, 'shop/shipping_payment.html')

def pdd(request):
	return render(request, 'shop/pdd.html')

def contact(request, message=None):
	return render(request, 'shop/contact.html', {'message': message})

def success_pay(request):
	# "status": "succeeded", "paid": true,
	payment_id = request.session['payment_id']
	payment = Payment.find_one(payment_id)
	return HttpResponse(json.dumps({
			'status': payment.status,
			'paid': payment.paid,
			'description': payment.description,
		}))
	return render(request, 'shop/success.html')

@require_POST
def contact_send_message(request):
	successMessage = 'Ваше сообщение отправлено!'
	errorMessage = 'Произошла ошибка при отправке сообщения!'

	form = MessageCreateForm(request.POST)
	if form.is_valid():
		form.save()
		return redirect('shop:contact', successMessage)
	
	return redirect('shop:contact', errorMessage)
