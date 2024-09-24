from flask import Blueprint
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from webapp.user.forms import LoginForm, Regform, Personalform
from webapp.db import db
from webapp.user.models import User

blueprint = Blueprint('user', __name__)


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Авторизация'
    form = LoginForm()
    return render_template(
        'login.html',
        title=title,
        form=form
    )


@blueprint.route('/process_login', methods=['POST'])
def process_login():
    form = LoginForm()
    user = User.query.filter(User.username == form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember_me.data)
        flash('Мы рады снова Вас видеть')
        return redirect(url_for('news.index'))
    flash('Проверьте корректность логина или пароля')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('news.index'))


@blueprint.route('/registration')
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Регистрация'
    form = Regform()
    return render_template(
        'registration.html',
        title=title,
        form=form
    )


@blueprint.route('/process_reg', methods=['POST'])
def process_reg():
    form = Regform()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            name=form.name.data.strip().capitalize(),
            surname=form.surname.data.strip().capitalize(),
            mail=form.mail.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Добро пожаловать!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {field}: {error}')
    return redirect(url_for('user.registration'))


@blueprint.route('/personal', methods=['GET', 'POST'])
def personal():
    title = "Личный кабинет"
    if current_user.is_authenticated:
        form = Personalform(obj=current_user)
        if request.method == 'POST' and form.validate_on_submit():
            current_user.name = form.name.data
            current_user.surname = form.surname.data
            current_user.mail = form.mail.data
            current_user.username = form.username.data
            current_user.password = form.password.data
            if form.password.data:
                current_user.set_password(form.password.data)
            db.session.commit()
            flash('Изменения сохранены')
            return redirect(url_for('user.personal'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Ошибка в поле {field}: {error}')
        return render_template(
            'personal.html',
            title=title,
            form=form
        )
    return redirect(url_for('user.login'))
