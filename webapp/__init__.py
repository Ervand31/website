import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.user.models import User
from webapp.db import db
from webapp.news.views import blueprint as news_blueprint
from webapp.user.views import blueprint as user_blueprint
# from webapp.parse import parse_news

if os.name != 'nt':
    import fcntl


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    # with app.app_context():
    #     db.create_all()

    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
