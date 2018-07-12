from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app import routes, models

flaskapp = Flask(__name__)

flaskapp.config.from_object(Config)
db = SQLAlchemy(flaskapp)
migrate = Migrate(flaskapp,db)
loginmgr = LoginManager(flaskapp)
loginmgr.login_view = 'login'
