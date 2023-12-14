from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app=Flask(__name__)

app.config['SECRET_KEY']='0123456789ABCDEF'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app) #database instance
app.app_context().push()
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login' # 'login' function name 
login_manager.login_message_category='info' #it is the flask category means class applied

from flaskblog import routes