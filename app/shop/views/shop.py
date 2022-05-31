import json

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q

from .. import NO_IMAGE_PATH
from ..ctx_proc import currency
from ..models import Category, Product, ProductImage

PAGINATION_SIZE = 12
PAGINATION_SIZE_SESSION_ID = 'pagination_size'
SORT_BY_SESSION_ID = 'sort_by'
PRODUCT_VIEW_STYLE_SESSION_ID = 'product_view_style'

def shop_redirect(request):
    return redirect('shop:product_list')

def product_list_size(request, size=PAGINATION_SIZE):
    """
    Установка значения сессии, колличество выводимых товаров на странице
    Значение по умолчанию PAGINATION_SIZE = 12 вне сессии
    """
    if request.headers.get('X-Requested-With'):
        if size == PAGINATION_SIZE:
            request.session[PAGINATION_SIZE_SESSION_ID] = PAGINATION_SIZE
        elif size == 24:
            request.session[PAGINATION_SIZE_SESSION_ID] = 24
        return HttpResponse('SET: product_list_size = ' + str(size))
    return redirect('shop:product_list')


def product_sort_by(request, sort_by):
    """
    Установка значения сессии, для сортировки товаров
    Значение по умолчанию 'default' вне сессии
    """
    if request.headers.get('X-Requested-With'):
        if sort_by == 'default':
            request.session[SORT_BY_SESSION_ID] = 'default'
        elif sort_by == 'price_min':
            request.session[SORT_BY_SESSION_ID] = 'price_min'
        elif sort_by == 'price_max':
            request.session[SORT_BY_SESSION_ID] = 'price_max'
        return HttpResponse("SET: product_sort_by = " + sort_by)
    return redirect('shop:product_list')


def toggle_style(request, view_style):
    """
    Установка значения сессии, для отображения в виде таблицы или списка
    Значение по умолчанию 'grid' вне сессии
    """
    if request.headers.get('X-Requested-With'):
        if view_style == 'list':
            request.session[PRODUCT_VIEW_STYLE_SESSION_ID] = 'list'
        else:
            request.session[PRODUCT_VIEW_STYLE_SESSION_ID] = 'grid'
        return HttpResponse("SET: toggle_style = " + view_style)
    return redirect('shop:product_list')


def product_list(request, category_slug=None):
    """
    Выводит список всех продуктов либо список по категориям
    Осуществляет: Q(name__icontains=request.GET.get('search_query'))
        - сортировку
        - постраничную навигацию
        - стиль отображения товаров на странице
    """
    search_query = request.GET.get('search_query')
    show_products = request.GET.get('products') 
    show_services = request.GET.get('services')

    sort_by = request.session.get(SORT_BY_SESSION_ID, 'default')
    category = None

    categories = Category.objects.all()
    products = Product.objects.all()
    # products = Product.objects.filter(available=True)

    brands = {}
    for brand in (b for b in products.values(*['brand_car']).distinct()):
        # print(brand['brand_car'] == '')
        if brand['brand_car']:
            brands[brand['brand_car'].lower()] = brand['brand_car']

    if category_slug is None and show_products is not None:
        products = products.filter(product_type=show_products)

    if category_slug is None and show_services is not None:
        products = products.filter(service_type=show_services)

    # select
    if sort_by == 'price_min':
        products = products.filter(available=True).order_by('price')
    elif sort_by == 'price_max':
        products = products.filter(available=True).order_by('-price')

    # if category_slug:
    #     category = get_object_or_404(Category, slug=category_slug)
    #     products = products.filter(category=category)

    # выборка по брендам
    if len(categories.filter(slug=category_slug)) == 0 and category_slug:
        products = products.filter(brand_car=brands.get(category_slug, ''))

    # выборка по категориям 
    if len(categories.filter(slug=category_slug)):
        category = categories.get(slug=category_slug)
        products = products.filter(category=category)
        
        # фильтр JS
        if request.headers.get('X-Requested-With') and request.GET.get('brand'):
            filter_fields = ['brand_car', 'model_car', 'year', 'seat_type']
            retval = {
                'brand_car': {},
                'model_car': {},
                'year': {},
                'seat_type': {},
            }

            brand_name = request.GET.get('brand')
            products = products.filter(brand_car=brand_name)
            filter_fields = ['brand_car', 'model_car', 'year', 'seat_type']
            # исключить дубликаты
            for item in (d for d in products.values(*filter_fields).distinct()):
                retval['brand_car'][item['brand_car']] = item['brand_car']
                retval['model_car'][item['model_car']] = item['model_car']
                retval['seat_type'][item['seat_type']] = item['seat_type']
                retval['year'][item['year']] = item['year']

            return HttpResponse(json.dumps(retval))

    # search form
    if search_query:
        products = products.filter( Q(name__icontains=search_query) )

    paginator = Paginator(products, request.session.get(
        PAGINATION_SIZE_SESSION_ID, PAGINATION_SIZE))

    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'page': products,
        'sort_by': sort_by,
        'product_view_style': request.session.get(PRODUCT_VIEW_STYLE_SESSION_ID, 'grid'),
        'brands': sorted(brands),
    })

# "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product33 = get_object_or_404(Product, id=33)

    # как-то проверить есть ли
    product.full_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
    product.save()

    images = ProductImage.objects.filter(product_id=product.id)
    
    # url картинок, модальное окно с карточкой товара
    if request.headers.get('X-Requested-With'):
        images_urls = []
        for item in images:
            images_urls.append(item.image.url)
        return HttpResponse(json.dumps(images_urls))

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'images': images,
        'product33': product33,
    })

@require_POST
def product_filter(request):
    """Фильтер товаров JS"""
    products = Product.objects.filter(available=True)

    product_type = request.POST.get('product_type')
    brand_name = request.POST.get('brand_name')
    
    # select brands js
    if product_type and request.POST.get('all_brands'):
        fields = ['brand_car']
        brands = {}
        for item in (b for b in products.filter(product_type=product_type).values(*fields).distinct()):
            if item['brand_car'] == '':
                continue
            brands[item['brand_car']] = item['brand_car']


        return HttpResponse(json.dumps( brands ))
    # change select brand - ret selects model, year, seat-type
    if  product_type and brand_name:
        fields = ['model_car', 'year', 'seat_type']
        data_filter = {'model_car': {}, 'year': {}, 'seat_type': {}}
        for item in (b for b in products.filter(product_type=product_type).filter(brand_car=brand_name).values(*fields).distinct()):
            data_filter['model_car'][item['model_car']] = item['model_car']
            data_filter['year'][item['year']] = item['year']
            data_filter['seat_type'][item['seat_type']] = item['seat_type']

        return HttpResponse(json.dumps(data_filter))

    brand_car = request.POST.get('brand_car')
    model_car = request.POST.get('model_car')
    year = request.POST.get('year')
    seat_type = request.POST.get('seat_type')
    
    fields = {}

    if brand_car:
        fields['brand_car'] = brand_car
    if model_car:
        fields['model_car'] = model_car
    if seat_type:
        fields['seat_type'] = seat_type
    if year:
        fields['year'] = year
    # change selects
    if brand_car or model_car or seat_type or year:
        products = Product.objects.filter(**fields)[0:36]

        retval = {
            'products': [],
        }
        # print(fields)
        for product in products:
            image = NO_IMAGE_PATH
            if product.image_base:
                image = product.image_base.url
            retval['products'].append({
                'product_id': product.id,
                'product_name': product.name,
                'product_image': image,
                'product_url': product.get_absolute_url(),
                'product_price': currency(request)['currency'] + str(product.price),
            })

        return HttpResponse(json.dumps(retval))

    return HttpResponse(json.dumps({'length_zero': 0}))