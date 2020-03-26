from flask import render_template, url_for, flash, redirect
from flask_login import login_user, logout_user
from web_english.auth.forms import LoginForm, RegisterForm
from web_english.models import User
from web_english import db


def login():
    title = "Авторизация"
    form = LoginForm()
    return render_template(
        "auth/login.html",
        page_title=title,
        form=form,
        form_action=url_for("auth.process_login")
    )

def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вы вошли на сайт")
            return redirect(url_for("main.index"))
    flash("Что-то пошло не так")
    return redirect(url_for("auth.login"))

def register():
    title = "Регистрация"
    form = RegisterForm()
    return render_template(
        "auth/register.html",
        page_title=title,
        form=form,
        form_action=url_for("auth.process_register")
    )

def process_register():
    form = RegisterForm()
    if not form.validate_on_submit():
        flash("Что-то пошло не так")
        return redirect(url_for("auth.login"))
    new_user = User(
        username=form.username.data,
        password=form.password.data,
        email=form.email.data,
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        role=User.USER_ROLE_STUDENT
    )
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    flash("Вы вошли на сайт")
    return redirect(url_for("main.index"))

def logout():
    logout_user()
    return redirect(url_for("main.index"))
