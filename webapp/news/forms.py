from flask_wtf import FlaskForm
from webapp.news.models import Comment
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment_text = StringField('Текст комментария: ',
                               validators=[DataRequired()])
    submit = SubmitField('Отправить',
                         render_kw={'class': 'btn btn-primary'})
