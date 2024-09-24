from flask_login import UserMixin
from webapp.db import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(), nullable=False)
    surname = db.Column(db.String(), nullable=False)
    mail = db.Column(db.String(), unique=True, nullable=False)
    status = db.Column(db.String(8), default='User')
    city = db.Column(db.String(), default='Moscow,Russia')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'User {self.id} - {self.username}'
