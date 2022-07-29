import traceback
import sys
import logging
from yookassa import Configuration


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    # print(text)
    logging.error(text)


sys.excepthook = log_uncaught_exceptions

# python manage.py runserver_plus --cert-file cert.pem --key-file key.pem localhost:8000
# --keep-meta-shutdown localhost:9000
# python manage.py createcachetable
# python -m smtpd -n -c DebuggingServer localhost:1025

POSTS_DETAIL_CACHE_TIME = 60 * 60 * 24 * 7

# 5.2631
PERCENT = 5

# retailcrm
RETAIL_SITE = ''
RETAIL_HOST = ''
RETAIL_CRM_ID = ''
RETAIL_BRAND_CODE = {
 'AUDI': 'audi',
 'BMW': 'bmw',
 'CADILLAC': 'cadillac',
 'CHEVROLET': 'chevrolet',
 'CITROEN': 'citroen',
 'DAEWOO': 'daewoo',
 'DATSUN': 'datsun',
 'FIAT': 'fiat',
 'FORD': 'ford',
 'GAZ': 'gaz',
 'GEELY': 'geely',
 'HONDA': 'honda',
 'HYUNDAI': 'hyundai',
 'INFINITI': 'infiniti',
 'JAGUAR': 'jaguar',
 'JEEP': 'jeep',
 'KIA': 'kia',
 'LADA': 'lada_vaz',
 'LAND-ROVER': 'land_rover',
 'LEXUS': 'lexus',
 'MAZDA': 'mazda',
 'MERCEDES-BENZ': 'mercedes-benz',
 'MINI': 'mini',
 'MITSUBISI': 'mitsubishi',
 'NISSAN': 'nissan',
 'OPEL': 'opel',
 'PEUGEOT': 'peugeot',
 'PORSCHE': 'porsche',
 'PORSHE': 'porsche',
 'RENAULT': 'renault',
 'SEAT': 'seat',
 'SKODA': 'skoda',
 'SMART': 'smart',
 'SSANG-YONG': 'ssangyong',
 'SUBARU': 'subaru',
 'SUZUKI': 'suzuki',
 'TOYOTA': 'toyota',
 'VOLKSWAGEN': 'volkswagen',
 'VOLVO': 'volvo',
 }

# yookassa
Configuration.account_id = ''
Configuration.secret_key = ''
PAYMENT_REDIRECT_PAGE = ''
PAYMENT_WAITING_TIME = 60

# cdek
PROD = False
CLIENT_ID = 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI'
CLIENT_SECRET = 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG'

WEIGHT = 1500
BOX = 'WASTE_PAPER'  # order.js
# 55.645283, 37.403216
FROM_LOCATION = {
    'code': 44,
    'country_code': 'RU',
    'city': 'Москва',
    'address': 'г. Москва, Солнцево, ул.Щорса, д.8 стр.1',
}

TARIFF_CODES = {
    '136': 'Посылка склад-склад',
    '137': 'Посылка склад-дверь',
}

# app
CART_SESSION_ID = 'cart'
GRAND_TOTAL_ID = 'gt'
NO_IMAGE_PATH = '/static/shop/images/no_image/placeholder.jpg'
ADMIN_EMAIL_ORDER_INFO = 'info@isofix-msk.ru'
ADMIN_EMAIL = 'site-admin@email.ru'
