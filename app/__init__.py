# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from config import Config

my_app = Flask(__name__)            # создаем Flask-приложение
my_app.config.from_object(Config)   # применяем собственную конфигурацию

db = SQLAlchemy(my_app)             # класс фреймворка для работы с БД
migration = Migrate(my_app, db)     # миграция БД

login = LoginManager(my_app)
login.login_view = 'login'

if not my_app.debug:                # для продакш-сервера
    if my_app.config["MAIL_SERVER"]:    # отправка ошибок по почте
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
        
    if not os.path.exists('logs'):  # лог в файл
        os.mkdir('logs')
    fh = RotatingFileHandler('logs/blog.log', maxBytes=1024*100, backupCount=100)
    fh.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    fh.setLevel(logging.INFO)
        
    my_app.logger.addHandler(fh)
    my_app.logger.setLevel(logging.INFO)
    my_app.logger.info("SeriousBlog started")

from app import routes, models, errors      # импорты


