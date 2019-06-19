# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from config import Config

db = SQLAlchemy()
migration = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config=Config()):
    my_app = Flask(__name__)
    my_app.config.from_object(config)

    # инициализация приложения
    db.init_app(my_app)
    migration.init_app(my_app, db)
    login.init_app(my_app)

    # регистрация blueprint`ов
    from app.errors import bp as errors_bp
    my_app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    my_app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp
    my_app.register_blueprint(main_bp)

    # для продакш-сервера: отправка ошибок по почте
    if not my_app.debug and not my_app.testing:
        if my_app.config["MAIL_SERVER"]:
            auth = None
            if my_app.config['MAIL_USERNAME'] or my_app.config['MAIL_PASSWORD']:
                auth = (my_app.config['MAIL_USERNAME'], my_app.config['MAIL_PASSWORD'])
            secure = None
            if my_app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost = (my_app.config["MAIL_SERVER"], my_app.config["MAIL_PORT"]),
                fromaddr='no-reply@'+my_app.config["MAIL_SERVER"],
                toaddrs=my_app.config["ADMINS"],
                subject='SeriousBlog failure info',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            my_app.logger.addHandler(mail_handler)

    # логирование в файл
    if not os.path.exists('logs'):
        os.mkdir('logs')
    fh = RotatingFileHandler('logs/blog.log', maxBytes=1024*100, backupCount=100)
    fh.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    fh.setLevel(logging.INFO)

    my_app.logger.addHandler(fh)
    my_app.logger.setLevel(logging.INFO)
    my_app.logger.info("SeriousBlog started")

    return my_app





