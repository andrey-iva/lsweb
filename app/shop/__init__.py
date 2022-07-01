from yookassa import Configuration

Configuration.account_id = '916494'
Configuration.secret_key = 'test_ptA6-o_oaTCYnc9R0Fvh-WIXe50UNgXKIUob2qZT86I'
PAYMENT_REDIRECT_PAGE    = 'http://127.0.0.1:8000/order/created/'
PAYMENT_WAITING_TIME     = 900

#cdek
PROD = False
CLIENT_ID     = 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI'
CLIENT_SECRET = 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG'

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
	# '482': 'Экспресс склад-дверь',
}

# app

CART_SESSION_ID = 'cart'
GRAND_TOTAL_ID  = 'gt'
NO_IMAGE_PATH   = '/static/shop/images/no_image/placeholder.jpg'
ADMIN_EMAIL     = 'admin@mail.com'