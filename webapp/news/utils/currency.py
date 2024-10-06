import requests
from pprint import pprint


def currency_rate() -> float | str:
    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=EUR"
    params = {
        'apikey': "wrDKnixyZDxjqDFo60SwqEB22nBX3O72",
        # 'q': cur
    }
    try:
        responce = requests.get(url, params=params)
        responce.raise_for_status()
        responce = responce.json()
    except (requests.RequestException, ValueError):
        return False
    try:
        responce = responce['rates']
    except (IndexError, KeyError, TypeError):
        return False
    # responce = requests.get(url, params=params).json()
    return responce['RUB']


if __name__ == '__main__':
    pprint(currency_rate())
