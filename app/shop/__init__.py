from yookassa import Configuration

# python manage.py runserver_plus --cert-file cert.pem --key-file key.pem localhost:8000
# --keep-meta-shutdown localhost:9000
# python manage.py createcachetable
# python -m smtpd -n -c DebuggingServer localhost:1025

POSTS_DETAIL_CACHE_TIME = 60 * 60 * 24 * 7
PRODUCT_DETAIL_CACHE_TIME = 600

# PERCENT = 5.2631
PERCENT = 5

# retailcrm
RETAIL_SITE = 'isofix-msk-ru'
RETAIL_HOST = 'https://isofix-msk.retailcrm.ru'
RETAIL_CRM_ID = ''

# yookassa
Configuration.account_id = '916494'
Configuration.secret_key = 'test_ptA6-o_oaTCYnc9R0Fvh-WIXe50UNgXKIUob2qZT86I'
PAYMENT_REDIRECT_PAGE = 'http://127.0.0.1:8000/order/created/'
PAYMENT_WAITING_TIME = 900

# cdek
# PROD = False
# CLIENT_ID = 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI'
# CLIENT_SECRET = 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG'

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
    # '138': 'Посылка дверь-склад',
    # '139': 'Посылка дверь-дверь',
    # '483': 'Экспресс склад-склад',
}

# app
CART_SESSION_ID = 'cart'
GRAND_TOTAL_ID = 'gt'
NO_IMAGE_PATH = '/static/shop/images/no_image/placeholder.jpg'
# ADMIN_EMAIL_ORDER_INFO = 'info@isofix-msk.ru'
ADMIN_EMAIL_ORDER_INFO = 'andrey.cherkessk@yandex.ru'
ADMIN_EMAIL = 'site-admin@email.ru'
