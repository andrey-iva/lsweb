from django.shortcuts import render, redirect
from django.http import HttpResponse


def page_not_found(request, exception=None, template_name=''):
    return HttpResponse('404')


def bad_request(request, exception=None, template_name=''):
    return HttpResponse('400')


def permission_denied(request, exception=None, template_name=''):
    return HttpResponse('403')
