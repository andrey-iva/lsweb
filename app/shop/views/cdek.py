from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from pprint import pprint

import requests as r
import json, time, logging, csv, os

from .. import PROD, CLIENT_ID, CLIENT_SECRET, FROM_LOCATION, TARIFF_CODES
from ..cart import Cart

if PROD:
	GRANT_TYPE          = 'client_credentials'
	CDEK                = 'https://api.cdek.ru/v2/oauth/token?parameters'
	TARIFFS_URL         = 'https://api.cdek.ru/v2/calculator/tarifflist'
	TARIFF_URL          = 'https://api.cdek.ru/v2/calculator/tariff'
	CITIES_URL          = 'https://api.cdek.ru/v2/location/cities'
	DELIVERY_POINTS_URL = 'https://api.cdek.ru/v2/deliverypoints'
else:
	GRANT_TYPE          = 'client_credentials'
	CDEK                = 'https://api.edu.cdek.ru/v2/oauth/token?parameters'
	TARIFFS_URL         = 'https://api.edu.cdek.ru/v2/calculator/tarifflist'
	TARIFF_URL          = 'https://api.edu.cdek.ru/v2/calculator/tariff'
	CITIES_URL          = 'https://api.edu.cdek.ru/v2/location/cities'
	DELIVERY_POINTS_URL = 'https://api.edu.cdek.ru/v2/deliverypoints'

ATTEMPTS = 3

def get_token_cdek():
	for i in range(0, ATTEMPTS):
	    response = r.post(CDEK, {
			'grant_type': GRANT_TYPE,
			'client_id': CLIENT_ID,
			'client_secret': CLIENT_SECRET,})
	    logging.error('get_token_cdek STATUS: %s', 
	    	'Не авторизирован 401' if response.status_code == 401 else response.status_code)
	    if response.status_code == 200:
	        return response.json()
	    time.sleep(0.2)



def access_header():
	TOKEN_CDEK = get_token_cdek()
	logging.debug('TOKEN_CDEK: %s', TOKEN_CDEK)

	if TOKEN_CDEK:
		access_token = TOKEN_CDEK['access_token']
		token_type = TOKEN_CDEK['token_type']
		return {'Authorization': token_type + ' ' + access_token}

@require_POST
def get_cities(request):
	''' посказки в input файлы .json с разной структурой '''
	country_iso_code = request.POST.get('country_iso_code')

	if country_iso_code:
		if country_iso_code == 'RU':
			templates = ''
			c = []
			with open(os.path.join( os.path.dirname(__file__) , 'cities', 'ru.json'), encoding='utf-8-sig') as file:
				templates = json.load(file)

			for item in templates:
				c.append(item['Город'])
			c.append('Москва')
			c.append('Санкт-Петербург')
			c.append('Севастополь')
			c.append('Зеленоград')
			c.remove('Ростов')

			return HttpResponse(json.dumps(c))

	if country_iso_code:
		if country_iso_code == 'KZ':
			templates = ''
			c = []
			with open(os.path.join( os.path.dirname(__file__) , 'cities', 'kz.json'), encoding='utf-8') as file:
				templates = json.load(file)

			for item in templates.values():
				c.append(item)
			return HttpResponse(json.dumps(c))

	if country_iso_code:
		if country_iso_code == 'BY':
			templates = ''
			c = []
			with open(os.path.join( os.path.dirname(__file__) , 'cities', 'by.json'), encoding='utf-8') as file:
				templates = json.load(file)

			for item in templates:
				c.append(item['name'])
			return HttpResponse(json.dumps(c))
	
	return HttpResponse(json.dumps([]))

@require_POST
def get_city(request):
	''' возвращает cdek_id н.п '''
	cities = []
	country_iso_code = request.POST.get('country_iso_code')
	city = request.POST.get('city')

	logging.debug('City CDEK: %s', city)
	logging.debug('iso codes CDEK: %s', country_iso_code)
	
	for i in range(0, ATTEMPTS):
		if country_iso_code and city:
			response = r.get(CITIES_URL, {
				'country_codes': [country_iso_code],
				'city': [city]
			}, headers=access_header())

			if response.status_code == 200:
				return HttpResponse(response.text)
		time.sleep(0.2)

	return HttpResponse(json.dumps([]))

def get_tarifflist(DATA):
	''' калькулятор по тарифам '''
	
	headers = access_header()
	logging.debug('Headers: %s', headers)
	assert headers is not None
	headers['Content-type'] = 'application/json'

	tariffs = []
	for tariff_code in TARIFF_CODES:
		DATA['tariff_code'] = tariff_code

		for i in range(0, ATTEMPTS):
			tariff = r.post(TARIFF_URL, json.dumps(DATA), headers=headers)
			if tariff.status_code == 200 and len(tariff.json()):
				tariff = tariff.json()
				tariff['tariff_code'] = tariff_code
				tariff['tariff_name'] = TARIFF_CODES[tariff_code]
				tariffs.append( tariff )
				break

			time.sleep(0.2)
		time.sleep(0.2)
	
	if len(tariffs) == len(TARIFF_CODES):
		return tariffs
	# tariffs = r.post(TARIFFS_URL, json.dumps(DATA), headers=headers)
	# if tariffs.status_code == 200:
	# 	tariffs = tariffs.json()
	# 	return tariffs['tariff_codes']
	return tariffs

@require_POST
def tarifflist(request):
	''' калькулятор по тарифам '''
	cart = Cart(request)
	packages = [{'weight': 1500 + len(cart) }]
	services = [{'code': 'WASTE_PAPER', 'parameter': len(cart)}]

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
		tariffs = get_tarifflist({
			'type': 1,
			'currency': 1,
			'lang': 'rus',
			'from_location': FROM_LOCATION,
			'to_location': {
				'code': cdek_id,
				'country_code': country_iso_code,
				'city': city,
			},
			'packages': [{'weight': 1500} for i in range(0, len(cart))],
			'services': [
				{'code': 'CARTON_FILLER', 'parameter': len(cart)},
				{'code': 'INSURANCE', 'parameter': str(int(cart.get_total_price())) },
			],
		})
		logging.debug('Packeges: %s', [{'weight': 1500} for i in range(0, len(cart))])
		if tariffs:
			# pprint(tariffs)
			for i in range(0, ATTEMPTS):
				delivery_points = r.get(DELIVERY_POINTS_URL, {
					'city_code': cdek_id,
					'type': 'PVZ',
				}, headers=access_header())
				
				if delivery_points.status_code == 200:
					tariffs.append(delivery_points.json())
				return HttpResponse(json.dumps(tariffs))

	return HttpResponse(json.dumps([]))