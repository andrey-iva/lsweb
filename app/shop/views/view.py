import logging
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core import management
from django import forms
from ..models import Message
from ..models import Post, Product


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'subject', 'email', 'notes']


def clear_session(request):
    dt = datetime.datetime.now()
    management.call_command('clearsessions')
    with open('cs.txt', 'w+') as f:
        print(dt.strftime('%Y-%m-%d %H:%M:%S'), file=f)
    return HttpResponse(status=200)


def home(request):
    try:
        posts = Post.objects.filter(status='published')[0:10]
        products = Product.objects.filter(available=True).order_by('?')

        brackets = products.filter(product_type='кронштейн')[0:10]
        rails = products.filter(product_type='рейка')[0:10]
        services = products.filter(product_type='услуга')[0:10]

    except Exception as e:
        logging.debug(e)

    return render(request, 'shop/index.html', {
        'posts': posts,
        'brackets': brackets,
        'rails': rails,
        'services': services,
        'products': products[0:10],
        # 'bracket_rand_url': brackets[0].get_absolute_url(),
        # 'rail_rand_url': rails[0].get_absolute_url(),
        # 'service_rand_url': services[0].get_absolute_url(),
    })


def ret_index(request):
    return redirect('/')


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


def video_list(request):
    return render(request, 'shop/video.html')


@require_POST
def contact_send_message(request):
    successMessage = 'Ваше сообщение отправлено!'
    errorMessage = 'Произошла ошибка при отправке сообщения!'

    form = MessageCreateForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('shop:contact', successMessage)

    return redirect('shop:contact', errorMessage)


def get_message_form(request):
    formHTML = '''
<hr>
<form id="contact-form" class="mt-4" action="" method="post">\
    <div class="row">
        <div class="col-lg-6 col-md-6">
            <input maxlength="50" name="name" type="text" placeholder="Имя" required>
        </div>
        <div class="col-lg-6 col-md-6">
            <input name="email" type="email" placeholder="Email" required>
        </div>
        <div class="col-lg-12 col-md-12">
            <input maxlength="200" name="subject" type="text" placeholder="Тема сообщения" required>
        </div>
        <div class="col-lg-12 col-md-12">
            <textarea id="text_field" maxlength="1000" name="notes" 
            placeholder="Ваше сообщение" required></textarea>
        </div>
        <div class="col-lg-12 col-md-12">
            <button class="submit" type="submit">Отправить</button>
        </div>
    </div>
</form>'''
    return HttpResponse(formHTML)
