import requests
from typing import Any
from pprint import pprint
from flask import current_app
from typing import Dict


# Any - это запись о том, что значением словаря может быть любой тип данных
def weather_by_city(city_name: str) -> Dict[str, Any] | bool:
    url = 'http://api.weatherapi.com/v1/current.json'
    params = {
        'key': current_app.config['WEATHER_API_KEY'],
        'q': city_name,
        'is_day': 1,
        'format': 'json',
        'lang': 'ru'
    }
    try:
        responce = requests.get(url, params=params)
        responce.raise_for_status()
        responce = responce.json()
        # responce = responce.json()
    except (requests.RequestException, ValueError):
        return False
    try:
        responce = responce['current']
    except (IndexError, KeyError, TypeError):
        return False
    return responce


if __name__ == '__main__':
    pprint(weather_by_city('Moscow'))
