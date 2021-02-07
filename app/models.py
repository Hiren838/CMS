from app import db,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))



class Admin(db.Model,UserMixin):
    a_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(100), nullable=False)


    def __init__(self, fname, lname, email, mobile, address, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.mobile = mobile
        self.address = address
        self.password = password


    def get_id(self):
        return (self.a_id)

    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.email}', '{self.image_file}', '{self.mobile}', '{self.address})"


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Student(db.Model,UserMixin):
    s_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    enroll = db.Column(db.String(255),nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, fname, lname,  enroll, dob, email, mobile, address, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.enroll = enroll
        self.dob = dob
        self.mobile = mobile
        self.address = address
        self.password = password

    def get_id(self):
        return (self.s_id)

    def get_reset_token(self,expire_sec=400):
        s = Serializer(app.config['SECRET_KEY'],expire_sec)
        return s.dump({'user_id':self.s_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s= Serializer(app.config['secret_key'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Student.query.get(user_id)

    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.email}', '{self.enroll}', '{self.dob}','{self.image_file}', '{self.mobile}', '{self.address})"
