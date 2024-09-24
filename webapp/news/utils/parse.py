import requests
from bs4 import BeautifulSoup
from datetime import datetime
from webapp.db import db
from webapp.news import models
from pprint import pprint
# from sqlalchemy import text


def get_html(url: str) -> str | bool:
    try:
        response = requests.get(url)
        response.raise_for_status()
        # pprint(response.text)
        return response.text
    except requests.RequestException:
        print("Website isn't working")
        return False


def parse_news(url):
    from webapp import create_app
    app = create_app()
    with app.app_context():
        html = get_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find_all('div', class_='er-item-title')
        all_dates = soup.find_all('div', class_="er-item-category")
        news_data = []
        for news, date in zip(all_news, all_dates):
            title = news.text
            url = news.find('a')['href']
            if 'https://espanarusa.com' not in url:
                url = "https://espanarusa.com" + url
            else:
                url
            date_str = date.find('a')['href'][-10:]
            date = datetime.strptime(date_str, '%d.%m.%Y')
            text = parse_news_content(url)
            if text:
                save_news(title, url, date, text)
                news_data.append((title, url, date, text))
        return news_data


def parse_news_content(url):
    html = get_html(url)
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', class_="er-page-left")
    # for tag in content(['a', 'iframe', 'form', 'script', 'noscript']):
    #     tag.decompose()
    if content:
        return content.decode_contents()
    else:
        return None


# def reset_auto_increment():
#     db.session.execute(text('DELETE FROM news;'))
#     db.session.commit()

#     db.session.execute(text('VACUUM;'))
#     db.session.commit()


# def clear_news_and_reparse():
#     # Удаление всех новостей
#     models.News.query.delete()
#     db.session.commit()

#     # Сброс автоинкремента ID
#     reset_auto_increment()
#     save_all_news()


def save_news(title, url, date, text):
    check_news = models.News.query.filter(models.News.url == url).count()
    if not check_news:
        new_news = models.News(
            title=title,
            url=url,
            date=date,
            text=text
        )
        db.session.add(new_news)
        db.session.commit()


def save_all_news(url):
    news_data = parse_news(url)
    for title, url, date, text in news_data:
        if text:
            save_news(title, url, date, text)


if __name__ == "__main__":
    save_all_news('https://espanarusa.com/ru/news/index')
