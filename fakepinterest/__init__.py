from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pinterest.db'
app.config['SECRET_KEY'] = '5f4152dba8d9c3f0d089ac4aa2ce1372'
app.config['UPLOAD_FOLDER'] = 'static/fotos_posts'
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

from fakepinterest.routes import *