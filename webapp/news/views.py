from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from webapp.news.forms import CommentForm
from webapp.news.utils.currency import currency_rate
from webapp.news.utils.parse import parse_news
from webapp.news.models import News, Comment
from webapp import db
from webapp.news.utils.weather import weather_by_city
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import atexit
import re

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
def index() -> str:
    print(type(render_template('index.html')))
    weather = weather_by_city('Moscow')
    currency = currency_rate()
    title = 'Наш сайт'
    # parse_news('https://espanarusa.com/ru/news/index')
    data = News.query.order_by(News.date.desc()).all()
    return render_template(
        'index.html',
        weather=weather,
        currency=currency,
        data=data, title=title
    )


@blueprint.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form['search'].lower()
    data = News.query.all()
    weather = weather_by_city('Moscow')
    currency = currency_rate()
    title = 'Результаты поиска'
    all_news = []
    for news in data:
        if query in news.title.lower():
            all_news.append(news)
    return render_template(
        'index.html',
        weather=weather,
        currency=currency,
        data=all_news, title=title
    )


@blueprint.route('/news/<int:news_id>')
# @login_required
def single_news(news_id):
    form = CommentForm()
    news = News.query.get(news_id)
    comment_id = request.args.get('comment_id')
    comment = Comment.query.get(comment_id)
    if not news:
        return render_template('404.html'), 404
    currency = currency_rate()
    title = 'Новости'
    weather = weather_by_city('Moscow')
    return render_template(
        'single_news.html',
        weather=weather,
        currency=currency,
        title=title,
        news=news,
        form=form,
        comment=comment
    )


@blueprint.route('/news/<int:news_id>/comment', methods=['POST'])
@login_required
def add_comment(news_id):
    form = CommentForm()
    bad_words = ["Жопа", "Тест", "Путин"]
    if form.validate_on_submit():
        comment_text = form.comment_text.data
        news = News.query.get(news_id)
        if news:
            for word in bad_words:
                comment_text = re.sub(
                    fr'\b{word}\b', '*' * len(word), comment_text, flags=re.IGNORECASE)
            user_id = current_user.id
            new_comment = Comment(
                text=comment_text,
                news_id=news_id,
                user_id=user_id,
                news=news)
            db.session.add(new_comment)
            db.session.commit()
            flash('Комментарий добавлен', 'success')
        else:
            flash('новость не найдена', 'danger')
    return redirect(url_for('news.single_news', news_id=news_id))


@blueprint.route('/del-comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    news_id = comment.news_id
    if current_user.status == 'admin' or comment.user.id == current_user.id:
        db.session.delete(comment)
        db.session.commit()
        flash('Комментарий удален', 'success')
        return redirect(url_for('news.single_news', news_id=news_id))
    else:
        flash('У вас нет прав для удаления этого комментария', 'danger')
        return redirect(url_for('news.single_news', news_id=news_id))


news_url = 'https://espanarusa.com/ru/news/index'


def start_scheduler():
    # Инициализация планировщика
    scheduler = BackgroundScheduler()

    # Добавление задачи с интервалом 6 часов
    scheduler.add_job(
        func=parse_news,
        trigger=IntervalTrigger(hours=1),
        args=[news_url],  # Аргумент URL для функции
        next_run_time=datetime.now(),  # Первая задача сразу после старта
        id='news_update',  # Уникальный идентификатор задачи
        name='News update every 6 hours',
        replace_existing=True
    )

    # Запуск планировщика
    scheduler.start()

    # Обработка выхода из приложения для корректной остановки планировщика
    atexit.register(lambda: scheduler.shutdown())


# Вызываем планировщик в views.py или основном файле приложения
start_scheduler()
