import requests as request
import json

from pprint import pprint

FROM_LOCATION = {
    'code': 44,
    'country_code': 'RU',
    'city': 'Москва',
    'address': 'г. Москва, Солнцево, ул.Щорса, д.8 стр.1'
}

data = {
    "type": 1,
    "currency": 1,
    "lang": "rus",
    "from_location": FROM_LOCATION,
    "to_location": {
        "code": 1085
    },
    "packages": [
        {
            "height": 10,
            "length": 10,
            "weight": 4000,
            "width": 10
        }
    ]
}



res = request.post('https://api.edu.cdek.ru/v2/oauth/token?parameters', {
    'grant_type': 'client_credentials',
    'client_id': 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI',
    'client_secret': 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG',
    })

if res.status_code == 200:
    response = res.json()
    access_token = response['access_token']
    token_type = response['token_type']
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-type': 'application/json',
    }
    
    req = request.post('https://api.edu.cdek.ru/v2/calculator/tarifflist', json.dumps(data), headers=headers)
    pprint(req.json())

# {'tariff_codes': [{'calendar_max': 12,
#                    'calendar_min': 8,
#                    'delivery_mode': 4,
#                    'delivery_sum': 1470.0,
#                    'period_max': 12,
#                    'period_min': 8,
#                    'tariff_code': 62,
#                    'tariff_name': 'Магистральный экспресс склад-склад'},
#                   {'calendar_max': 12,
#                    'calendar_min': 8,
#                    'delivery_mode': 1,
#                    'delivery_sum': 950.0,
#                    'period_max': 12,
#                    'period_min': 8,
#                    'tariff_code': 139,
#                    'tariff_name': 'Посылка дверь-дверь'},
#                   {'calendar_max': 12,
#                    'calendar_min': 8,
#                    'delivery_mode': 2,
#                    'delivery_sum': 795.0,
#                    'period_max': 12,
#                    'period_min': 8,
#                    'tariff_code': 138,
#                    'tariff_name': 'Посылка дверь-склад'},
#                   {'calendar_max': 12,
#                    'calendar_min': 8,
#                    'delivery_mode': 6,
#                    'delivery_sum': 795.0,
#                    'period_max': 12,
#                    'period_min': 8,
#                    'tariff_code': 366,
#                    'tariff_name': 'Посылка дверь-постамат'},
#                   {'calendar_max': 12,
#                    'calendar_min': 8,
#                    'delivery_mode': 3,
#                    'delivery_sum': 795.0,
#                    'period_max': 12,
#                    'period_min': 8,
#                    'tariff_code': 137,
#                    'tariff_name': 'Посылка склад-дверь'},
#                   {'calendar_max': 12,
#                    'calendar_min': 8,
#                    'delivery_mode': 4,
#                    'delivery_sum': 640.0,
#                    'period_max': 12,
#                    'period_min': 8,
#                    'tariff_code': 136,
#                    'tariff_name': 'Посылка склад-склад'},
#                   {'calendar_max': 12,
#                    'calendar_min': 8,
#                    'delivery_mode': 7,
#                    'delivery_sum': 640.0,
#                    'period_max': 12,
#                    'period_min': 8,
#                    'tariff_code': 368,
#                    'tariff_name': 'Посылка склад-постамат'},
#                   {'calendar_max': 4,
#                    'calendar_min': 2,
#                    'delivery_mode': 1,
#                    'delivery_sum': 1225.0,
#                    'period_max': 4,
#                    'period_min': 2,
#                    'tariff_code': 480,
#                    'tariff_description': 'Экспресс-доставка',
#                    'tariff_name': 'Экспресс дверь-дверь'},
#                   {'calendar_max': 4,
#                    'calendar_min': 2,
#                    'delivery_mode': 2,
#                    'delivery_sum': 1130.0,
#                    'period_max': 4,
#                    'period_min': 2,
#                    'tariff_code': 481,
#                    'tariff_description': 'Экспресс-доставка',
#                    'tariff_name': 'Экспресс дверь-склад'},
#                   {'calendar_max': 4,
#                    'calendar_min': 2,
#                    'delivery_mode': 6,
#                    'delivery_sum': 1130.0,
#                    'period_max': 4,
#                    'period_min': 2,
#                    'tariff_code': 485,
#                    'tariff_description': 'Экспресс-доставка',
#                    'tariff_name': 'Экспресс дверь-постамат'},
#                   {'calendar_max': 4,
#                    'calendar_min': 2,
#                    'delivery_mode': 3,
#                    'delivery_sum': 1130.0,
#                    'period_max': 4,
#                    'period_min': 2,
#                    'tariff_code': 482,
#                    'tariff_description': 'Экспресс-доставка',
#                    'tariff_name': 'Экспресс склад-дверь'},
#                   {'calendar_max': 4,
#                    'calendar_min': 2,
#                    'delivery_mode': 4,
#                    'delivery_sum': 1050.0,
#                    'period_max': 4,
#                    'period_min': 2,
#                    'tariff_code': 483,
#                    'tariff_description': 'Экспресс-доставка',
#                    'tariff_name': 'Экспресс склад-склад'},
#                   {'calendar_max': 4,
#                    'calendar_min': 2,
#                    'delivery_mode': 7,
#                    'delivery_sum': 1050.0,
#                    'period_max': 4,
#                    'period_min': 2,
#                    'tariff_code': 486,
#                    'tariff_description': 'Экспресс-доставка',
#                    'tariff_name': 'Экспресс склад-постамат'}]}
