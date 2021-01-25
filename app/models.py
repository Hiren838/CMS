from app import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader()
def load_user(get_id):
    return Student.query.get(int(get_id))

@login_manager.user_loader()
def load_user(get_id):
    return Admin.query.get(int(get_id))



class Admin(db.Model,UserMixin):
    a_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    # image = db.Column(db.String(20), nullable=False, default='default.jpg')
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, fname, lname, email, mobile, address, password):
        self.fname = fname
        self.lname = lname
        # self.image = image
        self.email = email
        self.mobile = mobile
        self.address = address
        self.password = password


class Student(db.Model,UserMixin):
    s_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    # image = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, fname, lname, email, mobile, dob, address, password):
        self.fname = fname
        self.lname = lname
        # self.image = image
        self.email = email
        self.mobile = mobile
        self.address = address
        self.dob = dob
        self.password = password
