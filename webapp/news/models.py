from webapp.db import db
from sqlalchemy.orm import relationship
from datetime import datetime


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    date = db.Column(db.DateTime)
    text = db.Column(db.Text)

    def comments_count(self):
        return Comment.query.filter(Comment.news_id == self.id).count()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE')
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE')
    )
    news = relationship('News', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return f'Comment {self.id} - {self.text} - {self.user_id}'
