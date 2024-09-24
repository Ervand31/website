from flask_wtf import FlaskForm
from flask_login import current_user
from webapp.user.models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField(
        'Логин',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )

    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={'class': 'form-check-input'})
    submit = SubmitField(
        'Войти',
        validators=[DataRequired()],
        render_kw={'class': 'btn btn-primary'}
    )


class Regform(FlaskForm):
    name = StringField(
        'Имя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    surname = StringField(
        'Фамилия',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    mail = StringField(
        'Почта',
        validators=[DataRequired(), Email()],
        render_kw={'class': 'form-control'}
    )
    username = StringField(
        'Логин',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    confirm_password = PasswordField(
        'Подтвердите пароль',
        validators=[DataRequired(), EqualTo(
            'password', 'Пароли не совпадают')],
        render_kw={'class': 'form-control'}
    )
    submit = SubmitField(
        'Зарегистрироваться',
        render_kw={'class': 'btn btn-primary'}
    )

    def validate_mail(self, mail):
        mail_counter = User.query.filter(User.mail == mail.data).count()
        if mail_counter:
            raise ValidationError('Данный email уже занят')

    def validate_username(self, username):
        username_counter = User.query.filter(
            User.username == username.data).count()
        if username_counter:
            raise ValidationError('Данный ник уже занят')


class Personalform(FlaskForm):
    name = StringField(
        'Имя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    surname = StringField(
        'Фамилия',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    mail = StringField(
        'Почта',
        validators=[DataRequired(), Email()],
        render_kw={'class': 'form-control'}
    )
    username = StringField(
        'Логин',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'}
    )
    confirm_password = PasswordField(
        'Подтвердите пароль',
        validators=[DataRequired(), EqualTo(
            'password', 'Пароли не совпадают')],
        render_kw={'class': 'form-control'}
    )
    submit = SubmitField(
        'Сохранить изменения',
        render_kw={'class': 'btn btn-primary'}
    )

    def validate_mail(self, mail):
        if mail.data != current_user.mail:
            mail_counter = User.query.filter(User.mail == mail.data).count()
            if mail_counter:
                raise ValidationError('Данный email уже занят')

    def validate_username(self, username):
        if username.data != current_user.username:
            username_counter = User.query.filter(
                User.username == username.data).count()
            if username_counter:
                raise ValidationError('Данный ник уже занят')
