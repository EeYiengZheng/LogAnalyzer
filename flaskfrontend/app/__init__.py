from flask import Flask
'''from flask_oauthlib.provider import OAuth2Provider'''
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_folder='static')
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = '/uploads'
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
'''oauth = OAuth2Provider(app)'''

from app import views, models