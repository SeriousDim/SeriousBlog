from flask import render_template, redirect, flash, url_for, request
from app import db
from flask_login import current_user, login_user
from flask_babel import _
from app.models import User
from werkzeug.urls import url_parse
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import logout_user



@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:                       # если пользователь уже вошел
        return redirect(url_for("main.notes"))
    form = LoginForm()                                      # создание формы
    if form.validate_on_submit():                           # вызывается при запросе POST, при нажатии на кнопку Submit
        user = User.query.filter_by(username=form.username.data).first()
        if user == None or not user.check_password(form.password.data):     # если пользователя не существует млм пароль неверный
            flash(_("Неверное имя пользователя или пароль"))
            return render_template("auth/login.html", form=form)                 # возвращаем эту же самую форму

        login_user(user, remember=form.remember.data)      # иначе входим в систему
        next_page = request.args.get('next')               # и проверяем параметр next
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("main.notes")
        return redirect(next_page)

    return render_template("auth/login.html", form=form)



@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.notes"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)



@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))