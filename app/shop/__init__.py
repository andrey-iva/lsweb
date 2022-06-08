from yookassa import Configuration

Configuration.account_id = '916494'
Configuration.secret_key = 'test_ptA6-o_oaTCYnc9R0Fvh-WIXe50UNgXKIUob2qZT86I'

#cdek
CLIENT_ID      = ''
CLIENT_SECRET  = ''

# 55.645283, 37.403216
FROM_LOCATION = {
	'code': 44,
	'country_code': 'RU',
	'city': 'Москва',
	'address': 'г. Москва, Солнцево, ул.Щорса, д.8 стр.1',
}

TARIFF_CODES = {
	# '137': 'Посылка склад-дверь',
	'136': 'Посылка склад-склад',
	# '482': 'Экспресс склад-дверь',
}

# app
PROD = False
CART_SESSION_ID       = 'cart'
GRAND_TOTAL_ID        = 'gt'
NO_IMAGE_PATH         = '/static/shop/images/no_image/placeholder.jpg'
PAYMENT_REDIRECT_PAGE = 'http://127.0.0.1:8000/order/created/'
ADMIN_EMAIL           = 'admin@mail.com'
