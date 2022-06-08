from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django import forms
from pprint import pprint

from ..models import Message
from ..models import Post

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'subject', 'email', 'notes']

def home(request):
	posts = Post.objects.all()[0:9]
	
	return render(request, 'shop/index.html', {
			'posts': posts,
		})

def about(request):
	return render(request, 'shop/adout.html')

def shipping_payment(request):
	return render(request, 'shop/shipping_payment.html')

def pdd(request):
	return render(request, 'shop/pdd.html')

def contact(request, message=None):
	return render(request, 'shop/contact.html', {'message': message})

@require_POST
def contact_send_message(request):
	successMessage = 'Ваше сообщение отправлено!'
	errorMessage = 'Произошла ошибка при отправке сообщения!'

	form = MessageCreateForm(request.POST)
	if form.is_valid():
		form.save()
		return redirect('shop:contact', successMessage)
	
	return redirect('shop:contact', errorMessage)
