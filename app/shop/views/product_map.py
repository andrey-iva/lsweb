import os
import datetime
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from urllib.parse import unquote
from pathlib import Path
from urllib.parse import unquote
from ..models import Category, Product


@require_POST
def make_map(request):
    cats = Category.objects.all()
    products = Product.objects.all()
    # host = request.META.get('HTTP_ORIGIN', 'https://isofix-msk.ru')
    host = 'https://isofix-msk.ru'
    base_dir = Path(__file__).resolve().parent.parent.parent
    file_path = os.path.join(base_dir, 'media', 'products', 'map.xml')
    dt = datetime.datetime.now()
    yml_catalog = '<yml_catalog date="' + dt.strftime('%Y-%m-%d %H:%M:%S') + '">\n'
    shop = '\t<shop>\n\t\t<name>ISOFIX-MSK</name>\n'

    categories = '\t\t<categories>\n'
    for cat in cats:
        categories += f'\t\t\t<category id="{cat.id}">\n\t\t\t\t<name>{cat.name}</name>\n\t\t\t</category>\n'
    categories += '\t\t</categories>\n'
    shop += categories

    offers = '\t\t<offers>\n'
    count = 0
    for p in products:
        offer = f'\t\t\t<offer id="{p.id}" productId="{p.id}" quantity="1">\n'
        offer += f'\t\t\t\t<categoryId>{p.category_id}</categoryId>\n'
        if p.image_base:
            offer += f'\t\t\t\t<picture>{host}{unquote(p.image_base.url)}</picture>\n'
        offer += f'\t\t\t\t<name>{p.name}</name>\n'
        offer += f'\t\t\t\t<productName>{p.name}</productName>\n'
        offer += f'\t\t\t\t<price>{p.price}</price>\n'
        offer += f'\t\t\t\t<url>{host}/product/{p.slug}/</url>\n'
        if p.brand_car:
            offer += f'\t\t\t\t<param code="pa_brand" name="Марка машины:">{p.brand_car}</param>\n'
        if p.year:
            offer += f'\t\t\t\t<param code="pa_god-vipuska" name="Год выпуска:">{p.year}</param>\n'
        if p.model_car:
            offer += f'\t\t\t\t<param code="pa_model" name="Модель машины:">{p.model_car}</param>\n'
        if p.seat_type:
            offer += f'\t\t\t\t<param code="pa_tip-sideniya" name="Тип сидения:">{p.seat_type}</param>\n'
        offer += f'\t\t\t\t<param code="article" name="Article">{p.item_number}</param>\n'
        # offer += '\t\t\t\t<dimensions>50/20/10</dimensions>\n'
        # offer += '\t\t\t\t<weight>1.5</weight>\n'
        # offer += '\t\t\t\t<vatRate>none</vatRate>\n'
        offer += '\t\t\t</offer>\n'
        offers += offer

    offers += '\t\t</offers>\n'
    shop += offers
    # offers
    shop += '\t</shop>\n'
    yml_catalog += shop
    yml_catalog += '</yml_catalog>'
    with open(file_path, mode='w', encoding='utf-8') as file:
        file.write(yml_catalog)
    return HttpResponse(file_path)
