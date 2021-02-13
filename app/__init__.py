from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd2225fa7c11f66924eabf4264bfc9cae611c33081e'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Hiren@123@localhost/clg"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cms.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'not_found'
login_manager.login_message_category ='info'


from app import routs

