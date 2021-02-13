from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, BooleanField, PasswordField, TextAreaField, DateField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from flask_login import current_user
from app.models import Student, Admin


# from wtforms.fields.html5 import DateField

class ARegisterForm(FlaskForm):
    fname = StringField("First-Name",
                        validators = [Length(min = 3, max = 20)])
    lname = StringField("Last-Name",
                        validators = [Length(min = 3, max = 20)])
    email = StringField("Email",
                        validators = [DataRequired(), Email()])
    mobile = IntegerField("Mobile",
                          validators = [DataRequired(message = "Must be number")])
    address = TextAreaField("Address",
                            validators = [DataRequired(), Length(min = 20, max = 200)])
    password = PasswordField("Password",
                             validators = [DataRequired()])
    confirm = PasswordField("Confirm",
                            validators = [DataRequired(), EqualTo('password', message = "Password do not match")])
    submit = SubmitField("Register")

    def validate_email(self, email):
        admin = Admin.query.filter_by(email = email.data).first()
        if admin:
            raise ValidationError('That email is taken.Please choose a another email')

    def validate_mobile(self, mobile):
        admin = Admin.query.filter_by(mobile = mobile.data).first()
        if admin:
            raise ValidationError("That Mobiel Number is taken. choose a another Mobile number")


class ALogin(FlaskForm):
    email = StringField("Email",
                        validators = [DataRequired("Please enter Email"), Email()])
    password = PasswordField("Password",
                             validators = [DataRequired("Please enter Password")])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class SRegisterForm(FlaskForm):
    fname = StringField("First-Name",
                        validators = [DataRequired(), Length(min = 4, max = 20)])
    lname = StringField("Last-Name",
                        validators = [DataRequired(), Length(min = 4, max = 20)])
    enroll = StringField("Enroll-Number",
                         validators = [DataRequired(), Length(min = 1, max = 20)])
    email = StringField("Email",
                        validators = [DataRequired(), Email()])
    mobile = IntegerField("Mobile",
                          validators = [DataRequired(message = "Must be in Number ")])
    address = TextAreaField("Address",
                            validators = [DataRequired(), Length(min = 20, max = 200)])
    dob = DateField("DOB", format = '%d-%m-%Y',
                    validators = [DataRequired()])
    password = PasswordField("Password",
                             validators = [DataRequired()])
    confirm = PasswordField("Confirm",
                            validators = [DataRequired(), EqualTo('password', message = "password do not match")])
    submit = SubmitField("Register")

    def validate_email(self, email):
            student = Student.query.filter_by(email = email.data).first()
            # if email.data != student.email:
            if student:
                raise ValidationError('That email is taken.Please choose a another email')

    def validate_mobile(self, mobile):
            student = Student.query.filter_by(mobile = mobile.data).first()
            # if mobile.data != student.mobile:
            if student:
                raise ValidationError("That Mobiel Number is taken. choose a another Mobile number")

    # def validate_enroll(self, enroll):
    #     student = Student.query.filter_by(enroll.enroll.data).first()
    #     if student:
    #         raise ValidationError("That Enroll Given Too Other Student")


class SLogin(FlaskForm):
    enroll = StringField("Enroll-number",
                         validators = [DataRequired("Please enter Enroll-Number")])
    password = PasswordField("Password",
                             validators = [DataRequired("Please enter Password")])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    email = StringField('Email',
                          validators = [DataRequired(),Email()])
    address = TextAreaField('Address',
                        validators = [DataRequired()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
    update = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            student = Student.query.filter_by(email = email.data).first()
            if student:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_mobile(self, mobile):
        if mobile.data != current_user.mobile:
            student = Student.query.filter_by(mobile = mobile.data).first()
            if student:
                raise ValidationError('That email is taken. Please choose a different one.')

class UpdateStudent(FlaskForm):
    fname = StringField("First-Name",
                        validators = [DataRequired(), Length(min = 4, max = 20)])
    lname = StringField("Last-Name",
                        validators = [DataRequired(), Length(min = 4, max = 20)])
    email = StringField("Email",
                        validators = [DataRequired(), Email()])
    mobile = IntegerField("Mobile",
                          validators = [DataRequired(message = "Must be in Number ")])
    address = TextAreaField("Address",
                            validators = [DataRequired(), Length(min = 20, max = 200)])
    dob = DateField("DOB", format = '%d-%m-%Y',
                    validators = [DataRequired()])
    update = SubmitField("Update")

    def validate_email(self, email):
            student = Student.query.filter_by(email = email.data).first()
            if email.data != student.email:
                if student:
                    raise ValidationError('That email is taken.Please choose a another email')

    def validate_mobile(self, mobile):
            student = Student.query.filter_by(mobile = mobile.data).first()
            if mobile.data != student.mobile:
                if student:
                    raise ValidationError("That Mobiel Number is taken. choose a another Mobile number")

class UpdateAdmin(FlaskForm):
    fname = StringField("First-Name",
                        validators = [Length(min = 3, max = 20)])
    lname = StringField("Last-Name",
                        validators = [Length(min = 3, max = 20)])
    email = StringField("Email",
                        validators = [DataRequired(), Email()])
    mobile = IntegerField("Mobile",
                          validators = [DataRequired(message = "Must be number")])
    address = TextAreaField("Address",
                            validators = [DataRequired(), Length(min = 20, max = 200)])
    update = SubmitField("Update")

    def validate_email(self, email):
        admin = Admin.query.filter_by(email = email.data).first()
        if email.data != admin.email:
            if admin:
                raise ValidationError('That email is taken.Please choose a another email')

    def validate_mobile(self, mobile):
        admin = Admin.query.filter_by(mobile = mobile.data).first()
        if mobile.data != admin.mobile:
            if admin:
                raise ValidationError("That Mobiel Number is taken. choose a another Mobile number")
class ContactUsForm(FlaskForm):
    name = StringField("Name",
                       validators =[DataRequired(), Length(min=1,max = 20)] )
    mobile = IntegerField("Mobile",
                          validators = [DataRequired("Must Be In Number")])
    email = StringField("Email",
                        validators = [DataRequired(),Email()])
    message = TextAreaField("Message",
                            validators=[DataRequired()])
    submit = SubmitField("Contact US")

class RequestResetForm(FlaskForm):
    email = StringField("Email",
                        validators = [DataRequired(),Email()])
    submit = SubmitField("Request Reset Password")
    def validate_email(self,email):
        student = Student.query.filter_by(email=email.data).first()
        if student is None:
            raise ValidationError("There is no Account with that email.Plese check email")
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",
                             validators = [DataRequired()])
    confirm = PasswordField("Confirm",
                            validators = [DataRequired(),EqualTo("confirm", message = "Password do not match")])
    submit = SubmitField("Reset Password")