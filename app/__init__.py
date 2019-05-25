# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

my_app = Flask(__name__)            # создаем Flask-приложение
my_app.config.from_object(Config)   # применяем собственную конфигурацию

db = SQLAlchemy(my_app)             # класс фреймворка для работы с БД
migration = Migrate(my_app, db)     # миграция БД

login = LoginManager(my_app)
login.login_view = 'login'

from app import routes, models      # импорт файла с маршрутами; моделями БД