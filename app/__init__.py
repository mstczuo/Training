#-*-coding:utf-8-*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from config import basedir
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

env = app.jinja_env
env.filters['eval'] = eval
env.filters['chr2'] = lambda x: chr(x + 64)

login_manager = LoginManager(app)
from models import AnonymousUser 
login_manager.anonymous_user = AnonymousUser
login_manager.login_view = 'login'
login_manager.login_message = u'你需要登录才能查看本页面'
login_manager.login_message_category = 'error'

Bootstrap(app)

from app import views, models

