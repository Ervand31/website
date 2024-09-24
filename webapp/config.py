import os
from datetime import timedelta

basedir = os.getcwd()
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'webapp.db')
REMEMBER_COOKIE_DURATION = timedelta(weeks=4)
WEATHER_API_KEY = '941a982031ef4f7187693807241208'
CURRENCY_API_KEY = "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=EUR"
SECRET_KEY = 'werhohoiho22388958!!ldg&'
API_STOCKS = 'PP9YW68T5M1FR39U'

# pq6Q6gjTQZ
