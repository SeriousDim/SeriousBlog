# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, url_for, request
from app import my_app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

user = {"name": None}
posts = [
    {
        "author": "Вадим Горький",
        "body": "Спешу вас всех обрадовать с тем, что мой новый музыкальный альбом наконец-то вышел! Вы можете скачать его прмяо сейчас и слушать на здоровье. Напоминаю, что альбом - бесплатный!"
    },
    {
        "author": "Андрей Куйбышев",
        "body": "Я считаю, что моего политеческого опыта уже достачно для того, чтобы приступить к достижению моей главной цели жизни. Я собираюсь болатироваться в президенты!"
    },
    {
        "author": "Захар Сахаров",
        "body": "Flask или Django? Вот в чем вопрос! Что же мне выбрать?"
    },
    {
        "author": "Serious Test System",
        "body": "<h2>Это тестовая запись, просто проигнорируйте ее.</h2><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
    },
    {
        "author": "Википедия",
        "body": "Python - высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Синтаксис ядра Python минималистичен. В то же время стандартная библиотека включает большой объём полезных функций. Python поддерживает структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное программирование. Основные архитектурные черты — динамическая типизация, автоматическое управление памятью, полная интроспекция, механизм обработки исключений, поддержка многопоточных вычислений, высокоуровневые структуры данных. Поддерживается разбиение программ на модули, которые, в свою очередь, могут объединяться в пакеты."
    },
    {
        "author": "Модуль праздников",
        "body": "1 мая во многих странах мира отмечается международный праздник — День труда (Праздник Весны и Труда), который изначально носил название День международной солидарности трудящихся. 1 мая 1886 года американские рабочие организовали забастовку в Чикаго, выдвинув требование 8-часового рабочего дня. Забастовка и сопутствующая демонстрация закончились кровопролитным столкновением с полицией."
    },
    {
        "author": "Википедия",
        "body": "<h2>О пожаре в Нотр-Дам-де-Пари</h2><p>15 апреля 2019 года в 18:20 по центральноевропейскому времени в соборе сработала пожарная сигнализация. Администрация храма начала эвакуацию посетителей, собравшихся на запланированную мессу, после чего принялась самостоятельно искать источник пожара. Сотрудники предполагали, что тревога могла оказаться ложной, поскольку не видели источник огня. Пожарных вызвали в 18:43, когда сработала вторая пожарная тревога и стало очевидно, что горит крыша собора[7]. Источник возгорания располагался в верхней части здания, на мансарде в основании шпиля, спроектированного архитектором Виолле-ле-Дюком. Большая часть загоревшейся деревянной конструкции представляла собой каркас, сооружённый в XII—XIII веках из 1300 дубов. Сверху находились свинцовые листы, расплавившиеся в огне. В течение часа пламя объяло свинцово-деревянную крышу собора и центральный деревянный шпиль, что привело к его обрушению на свод потолка каменной кладки собора[8][9]."
    },
    {
        "author": "Википедия",
        "body": "Дисциплини́рованность (также самодисципли́на, организо́ванность) — черта характера, или выработанная, ставшая привычкой склонность человека к соблюдению правил работы и норм поведения[1]. Входит в число так называемых «прусских добродетелей». Тесно связана с психологическим понятием самоконтроля. Педагог А. С. Макаренко следующим образом высказывался о дисциплинированности: «Всегда соблюдать дисциплину, выполнять то, что неприятно, но нужно делать, — это и есть высокая дисциплинированность»."
    },
    {
        "author": "Google",
        "body": "Material Design (рус. Материальный дизайн) — стиль дизайна программного обеспечения и приложений, разработанный компанией Google. Впервые представлен на конференции Google I/O 25 июня 2014 года. Стиль расширяет идею \"карточек\", появившуюся в Google Now, более широким применением строгих макетов, анимаций и переходов, отступов и эффектов глубины (света и тени). По идее дизайнеров Google, у приложений не должно быть острых углов, карточки должны переключаться между собой плавно и практически незаметно[1]."
    },
    {
        "author": "Jinja",
        "body": "Jinja (произносится как дзиндзя) — это шаблонизатор для языка программирования Python. Он подобен шаблонизатору Django, но предоставляет Python-подобные выражения, обеспечивая исполнение шаблонов в песочнице. Это текстовый шаблонизатор, поэтому он может быть использован для создания любого вида разметки, а также исходного кода. Лицензирован под BSD лицензией. Шаблонизатор Jinja позволяет настраивать теги[1], фильтры, тесты и глобальные переменные[2]. Также, в отличие от шаблонизатора Django, Jinja позволяет конструктору шаблонов вызывать функции с аргументами на объектах."
    }
]



@my_app.route("/")
def main():
    return redirect(url_for("notes"))



@my_app.route("/notes")
@login_required
def notes():
    if user["name"]==None:
        return render_template("notes.html", notes=posts)
    else:
        return render_template("notes.html", user=user, notes=posts)



@my_app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:                       # если пользователь уже вошел
        return redirect(url_for("notes"))
    form = LoginForm()                                      # создание формы
    if form.validate_on_submit():                           # вызывается при запросе POST, при нажатии на кнопку Submit
        user = User.query.filter_by(username=form.username.data).first()
        if user == None or not user.check_password(form.password.data):     # если пользователя не существует млм пароль неверный
            flash("Неверное имя пользователя или пароль")
            return render_template("login.html", form=form)                 # возвращаем эту же самую форму

        login_user(user, remember=form.remember.data)      # иначе входим в систему
        next_page = request.args.get('next')               # и проверяем параметр next
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for("notes")
        return redirect(next_page)

    return render_template("login.html", form=form)



@my_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))



@my_app.route("/me")
def me():
    return "Account page"



@my_app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("notes"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)