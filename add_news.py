from webapp import create_app
from webapp.news.utils.parse import parse_news

app = create_app()

with app.app_context():
    parse_news("https://espanarusa.com/ru/news/index")
