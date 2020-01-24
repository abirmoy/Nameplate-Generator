# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 09:49:41 2019

@author: qxz0ga0
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_bootstrap import Bootstrap

from flask_debug import Debug

app = Flask(__name__)
Debug(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)

from app import routes, models

if __name__ == "__main__":
    app.run(host= '0.0.0.0')