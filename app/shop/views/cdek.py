from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
# from pprint import pprint

import requests as r
import json, time

PROD = False

FROM_LOCATION = {
	'code': 44,
	'country_code': 'RU',
	'city': 'Москва',
	'address': 'г. Москва, Солнцево, ул.Щорса, д.8 стр.1',
}

TARIFF_CODES = {
	'482': 'Экспресс склад-дверь',
	'483': 'Экспресс склад-склад',
	'136': 'Посылка склад-склад',
}

SERVICES = [
	{'code': 'INSURANCE', 'parameter': '2'},
]

if PROD:
	TARIFFS_URL         = 'https://api.cdek.ru/v2/calculator/tarifflist'
	TARIFF_URL          = 'https://api.cdek.ru/v2/calculator/tariff'
	CITIES_URL          = 'https://api.cdek.ru/v2/location/cities'
	DELIVERY_POINTS_URL = 'https://api.cdek.ru/v2/deliverypoints'
else:
	TARIFFS_URL         = 'https://api.edu.cdek.ru/v2/calculator/tarifflist'
	TARIFF_URL          = 'https://api.edu.cdek.ru/v2/calculator/tariff'
	CITIES_URL          = 'https://api.edu.cdek.ru/v2/location/cities'
	DELIVERY_POINTS_URL = 'https://api.edu.cdek.ru/v2/deliverypoints'


def get_token_cdek():
    response = r.post('https://api.edu.cdek.ru/v2/oauth/token?parameters', {
		'grant_type': 'client_credentials',
		'client_id': 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI',
		'client_secret': 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG',})

    if response.status_code == 200:
        return response.json()


def access_header():
	response = get_token_cdek()
	if response:
		access_token = response['access_token']
		token_type = response['token_type']
		return {'Authorization': token_type + ' ' + access_token}

@require_POST
def get_city(request):
	''' возвращает cdek_id н.п '''
	cities = []
	country_iso_code = request.POST.get('country_iso_code')
	city = request.POST.get('city')

	if country_iso_code and city:
		response = r.get(CITIES_URL, {
			'country_codes': [country_iso_code], 
			'city': [city]
		}, headers=access_header())

		if response.status_code == 200:
			return HttpResponse(response.text)

	return HttpResponse(json.dumps([]))

def get_tarifflist(cdek_id, country_iso_code, city, address, packages):
	''' калькулятор по тарифам '''
	# data параметры тарифа
	data = {
		'type': 1,
		'currency': 1,
		'lang': 'rus',
		'from_location': FROM_LOCATION,
		'to_location': {
			'code': cdek_id,
			'country_code': country_iso_code,
			'city': city ,
			# 'address': address
		},
		'packages': packages,
		'services': SERVICES
	}
	
	headers = access_header()
	headers['Content-type'] = 'application/json'

	tariffs = []
	for tariff_code in TARIFF_CODES:
		data['tariff_code'] = tariff_code
		tariff = r.post(TARIFF_URL, json.dumps(data), headers=headers)
		if tariff.status_code == 200:
			tariff = tariff.json()
			tariff['tariff_code'] = tariff_code
			tariff['tariff_name'] = TARIFF_CODES[tariff_code]
			tariffs.append( tariff )
		time.sleep(0.2)
	
	if len(tariffs) == len(TARIFF_CODES):
		return tariffs
	# tariffs = r.post(TARIFFS_URL, json.dumps(data), headers=headers)
	# if tariffs.status_code == 200:
	# 	return tariffs.json()

@require_POST
def tarifflist(request):
	''' калькулятор по тарифам '''
	packages = []

	for product in request.session['cart'].values():
		for i in range(0, int(product['quantity'])):
			packages.append({'weight': 4000})

	cdek_id          = request.POST.get('cdek_id')
	country_iso_code = request.POST.get('country_iso_code')
	city             = request.POST.get('city')
	address          = request.POST.get('address')

	# pprint({
	# 	'cdek': 'def tarifflist',
	# 	'cdek_id': cdek_id, 
	# 	'country_iso_code': country_iso_code, 
	# 	'city': city, 
	# 	# 'address': address, 
	# 	'packages': packages})

	if cdek_id:
		tariffs = get_tarifflist(
			cdek_id=cdek_id,
			country_iso_code=country_iso_code,
			city=city, 
			address=address, 
			packages=packages)
		if tariffs:
			# pprint(tariffs)
			delivery_points = r.get(DELIVERY_POINTS_URL, {
				'city_code': cdek_id,
				'type': 'ALL',
			}, headers=access_header())
			if delivery_points.status_code == 200:
				tariffs.append(delivery_points.json())
			return HttpResponse(json.dumps(tariffs))
	return HttpResponse(json.dumps({'error': 'tariffs empty'}))