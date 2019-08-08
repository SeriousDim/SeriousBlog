# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, url_for, request, jsonify
from app import db
from flask_login import current_user, logout_user, login_required
from app.models import User, Post
from datetime import datetime
from guess_language import guess_language

from app.main.forms import EditProfileForm, PostForm
from app.main import bp
from app.main.email import send_message
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_babel import get_locale
from flask import g
from app.translate import translate



@bp.before_request
def before():
    g.locale = str(get_locale())
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



@bp.route("/")
def main():
    # send_message('Test subject', "lykov.dmitriy98@gmail.com", "lykov.dmitriy98@gmail.com", 'Здравствуйте, а вам письмо', "<h1>HTML body</h1>")
    return redirect(url_for("main.notes"))



@bp.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_("Ваш пост опубликован!"))
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
        flash(_("Изменения успешно сохранены"))
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
        return render_template("errors/error.html", number=_("Ошибка"), description=_("Пользователь %(username)s не найден", username=username))
    if user == current_user:
        # flash('Вы не можете подписаться на себя!')
        return render_template("errors/error.html", number=_("Ошибка"), description=_("Вы не можете подписаться на себя!"))
    current_user.follow(user)
    db.session.commit()
    # flash('Вы подписаны!')
    return redirect(url_for('main.me', username=username))



@bp.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template("errors/error.html", number=_("Ошибка"), description=_("Пользователь %(username)s не найден", username=username))
    if user == current_user:
        return render_template("errors/error.html", number=_("Ошибка"), description=_("Вы не можете подписаться на себя!"))
    current_user.unfollow(user)
    db.session.commit()
    # flash('Вы отписались')
    return redirect(url_for('main.me', username=username))



@bp.route("/globe")
def globe():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("main/notes.html", notes=posts)



@bp.route("/translate", methods=["POST"])
#@login_required
def translate_text():
    return jsonify(translate(request.form['text'], request.form['source_lang'], request.form['dest_lang']))