from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd2225fa7c11f66924eabf4264bfc9cae611c33081e'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Hiren@123@localhost/cms"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app import routs
