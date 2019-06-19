# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, url_for, request
from app import db
from flask_login import current_user, logout_user, login_required
from app.models import User, Post
from datetime import datetime

from app.main.forms import EditProfileForm, PostForm
from app.main import bp



"""
posts = [
    {
        "author": u1,
        "body": "Спешу вас всех обрадовать с тем, что мой новый музыкальный альбом наконец-то вышел! Вы можете скачать его прмяо сейчас и слушать на здоровье. Напоминаю, что альбом - бесплатный!"
    },
    {
        "author": u1,
        "body": "Я считаю, что моего политеческого опыта уже достачно для того, чтобы приступить к достижению моей главной цели жизни. Я собираюсь болатироваться в президенты!"
    },
    {
        "author": u1,
        "body": "Flask или Django? Вот в чем вопрос! Что же мне выбрать?"
    },
    {
        "author": u1,
        "body": "<h2>Это тестовая запись, просто проигнорируйте ее.</h2><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
    },
    {
        "author": u1,
        "body": "Python - высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Синтаксис ядра Python минималистичен. В то же время стандартная библиотека включает большой объём полезных функций. Python поддерживает структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное программирование. Основные архитектурные черты — динамическая типизация, автоматическое управление памятью, полная интроспекция, механизм обработки исключений, поддержка многопоточных вычислений, высокоуровневые структуры данных. Поддерживается разбиение программ на модули, которые, в свою очередь, могут объединяться в пакеты."
    },
    {
        "author": u1,
        "body": "1 мая во многих странах мира отмечается международный праздник — День труда (Праздник Весны и Труда), который изначально носил название День международной солидарности трудящихся. 1 мая 1886 года американские рабочие организовали забастовку в Чикаго, выдвинув требование 8-часового рабочего дня. Забастовка и сопутствующая демонстрация закончились кровопролитным столкновением с полицией."
    },
    {
        "author": u1,
        "body": "<h2>О пожаре в Нотр-Дам-де-Пари</h2><p>15 апреля 2019 года в 18:20 по центральноевропейскому времени в соборе сработала пожарная сигнализация. Администрация храма начала эвакуацию посетителей, собравшихся на запланированную мессу, после чего принялась самостоятельно искать источник пожара. Сотрудники предполагали, что тревога могла оказаться ложной, поскольку не видели источник огня. Пожарных вызвали в 18:43, когда сработала вторая пожарная тревога и стало очевидно, что горит крыша собора[7]. Источник возгорания располагался в верхней части здания, на мансарде в основании шпиля, спроектированного архитектором Виолле-ле-Дюком. Большая часть загоревшейся деревянной конструкции представляла собой каркас, сооружённый в XII—XIII веках из 1300 дубов. Сверху находились свинцовые листы, расплавившиеся в огне. В течение часа пламя объяло свинцово-деревянную крышу собора и центральный деревянный шпиль, что привело к его обрушению на свод потолка каменной кладки собора[8][9]."
    },
    {
        "author": u1,
        "body": "Дисциплини́рованность (также самодисципли́на, организо́ванность) — черта характера, или выработанная, ставшая привычкой склонность человека к соблюдению правил работы и норм поведения[1]. Входит в число так называемых «прусских добродетелей». Тесно связана с психологическим понятием самоконтроля. Педагог А. С. Макаренко следующим образом высказывался о дисциплинированности: «Всегда соблюдать дисциплину, выполнять то, что неприятно, но нужно делать, — это и есть высокая дисциплинированность»."
    },
    {
        "author": u1,
        "body": "Material Design (рус. Материальный дизайн) — стиль дизайна программного обеспечения и приложений, разработанный компанией Google. Впервые представлен на конференции Google I/O 25 июня 2014 года. Стиль расширяет идею \"карточек\", появившуюся в Google Now, более широким применением строгих макетов, анимаций и переходов, отступов и эффектов глубины (света и тени). По идее дизайнеров Google, у приложений не должно быть острых углов, карточки должны переключаться между собой плавно и практически незаметно[1]."
    },
    {
        "author": u1,
        "body": "Jinja (произносится как дзиндзя) — это шаблонизатор для языка программирования Python. Он подобен шаблонизатору Django, но предоставляет Python-подобные выражения, обеспечивая исполнение шаблонов в песочнице. Это текстовый шаблонизатор, поэтому он может быть использован для создания любого вида разметки, а также исходного кода. Лицензирован под BSD лицензией. Шаблонизатор Jinja позволяет настраивать теги[1], фильтры, тесты и глобальные переменные[2]. Также, в отличие от шаблонизатора Django, Jinja позволяет конструктору шаблонов вызывать функции с аргументами на объектах."
    }
]
"""



@bp.before_request
def before():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route("/")
def main():
    return redirect(url_for("main.notes"))



@bp.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Ваш пост опубликован!")
        return redirect(url_for("main.notes"))
    posts = current_user.followed_posts().all()
    return render_template("main/notes.html", notes=posts, form=form)



@bp.route("/me/<username>")
@login_required
def me(username):
    user = User.query.filter_by(username=username).first_or_404()
    my_posts = user.posts.order_by(Post.timestamp.desc())
    return render_template("main/user.html", notes=my_posts, user=user)



@bp.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Изменения успешно сохранены")
        return redirect(url_for("main.edit"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("main/edit_profile.html", form=form)



@bp.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        # flash("Пользователь {} не найден".format(username))
        return render_template("errors/error.html", number="Ошибка", description="Пользователь {} не найден".format(username))
    if user == current_user:
        # flash('Вы не можете подписаться на себя!')
        return render_template("errors/error.html", number="Ошибка", description="Вы не можете подписаться на себя!")
    current_user.follow(user)
    db.session.commit()
    # flash('Вы подписаны!')
    return redirect(url_for('main.me', username=username))



@bp.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template("errors/error.html", number="Ошибка", description="Пользователь {} не найден".format(username))
    if user == current_user:
        return render_template("errors/error.html", number="Ошибка", description="Вы не можете отписаться от себя!")
    current_user.unfollow(user)
    db.session.commit()
    # flash('Вы отписались')
    return redirect(url_for('main.me', username=username))



@bp.route("/globe")
def globe():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("main/notes.html", notes=posts)