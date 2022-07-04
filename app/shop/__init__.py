import os, logging
from dotenv import load_dotenv
from yookassa import Configuration

load_dotenv()
# python manage.py createcachetable
POSTS_DETAIL_CACHE_TIME = eval(os.getenv('POSTS_DETAIL_CACHE_TIME', '60'))
PRODUCT_DETAIL_CACHE_TIME = eval(os.getenv('PRODUCT_DETAIL_CACHE_TIME', '60'))

# logging.debug('SHOP loading env %s',  os.getenv('LENV') )
# logging.debug('POSTS_DETAIL_CACHE_TIME %i',  POSTS_DETAIL_CACHE_TIME)
# logging.debug('PRODUCT_DETAIL_CACHE_TIME %i',  PRODUCT_DETAIL_CACHE_TIME)


Configuration.account_id = os.getenv(
	'YOOKASSA_ACCOUNT_ID',
	'916494'
)
Configuration.secret_key = os.getenv(
	'YOOKASSA_SECRET_KEY',
	'test_ptA6-o_oaTCYnc9R0Fvh-WIXe50UNgXKIUob2qZT86I'
)
PAYMENT_REDIRECT_PAGE = os.getenv(
	'YOOKASSA_PAYMENT_REDIRECT_PAGE',
	'http://127.0.0.1:8000/order/created/'
)
PAYMENT_WAITING_TIME = int(os.getenv('YOOKASSA_PAYMENT_WAITING_TIME', 900))

#cdek
PROD          = int(os.getenv('CDEK_PRODUCTION', 0))
CLIENT_ID     = os.getenv('CLIENT_ID', 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG')

# order.js
BOX = 'WASTE_PAPER'

WEIGHT = 1500
# 55.645283, 37.403216
FROM_LOCATION = {
	'code': 44,
	'country_code': 'RU',
	'city': 'Москва',
	'address': 'г. Москва, Солнцево, ул.Щорса, д.8 стр.1',
}

TARIFF_CODES = {
	'136': 'Посылка склад-склад',
	# '137': 'Посылка склад-дверь',
	# '138': 'Посылка дверь-склад',
	# '139': 'Посылка дверь-дверь',
	# '483': 'Экспресс склад-склад',
}

# app

CART_SESSION_ID = 'cart'
GRAND_TOTAL_ID  = 'gt'
NO_IMAGE_PATH   = '/static/shop/images/no_image/placeholder.jpg'
ADMIN_EMAIL     = 'admin@mail.com'