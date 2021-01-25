from flask import render_template, flash, url_for, redirect, request,session,logging
from app.form import ARegisterForm,ALogin,SLogin,SRegisterForm
from app import app,db,bcrypt
from app.models import Student,Admin
from flask_login import login_user,logout_user,current_user




students = [
    {
        'id':1,
        'fname':'Hiren',
        'lname': 'Thakkar',
        'email': 'Hiren@123',
        'mobile': 9054313421,
        'dob': "05-06-200",
        'address': 'dammy'
    },
    {
        'id':1,
        'fname': 'Hiren',
        'lname': 'Thakkar',
        'email': 'Hiren@123',
        'mobile': 9054313421,
        'dob': "05-06-200",
        'address': 'dammy'
    }
]

# @app.route("/notfound")
# def not_found():
#     return render_template('layout/notfound.html')
# #unaythrized links
# def is__logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args,**kwargs)
#         else:
#             return redirect(url_for("not_found"))
#     return wrap
#

# Home Page
@app.route("/")
@app.route("/home")
def home():
    return render_template("student/index.html")


# About Page
@app.route("/about")
def about():
    return render_template("student/about.html", title="About")


# Admin Register page
@app.route("/aregister", methods=["GET", "POST"])
def aregister():
    form = ARegisterForm(request.form)
    if request.method == "POST" and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(fname=form.fname.data,
                      lname=form.lname.data,
                      email=form.email.data,
                      mobile=form.mobile.data,
                      address=form.address.data,
                      password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash('You Have Registred Successfully Now Logged in!', "success")
        return redirect(url_for("alogin"))
    return render_template('admin/aregister.html', form=form, title="ARegister")


# Admin Login Page
@app.route("/admin", methods=["GET", "POST"])
def alogin():
    form = ALogin(request.form)
    if request.method == "POST":
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password,form.password.data):
            login_user(admin, remember=form.remember.data)
            return redirect(url_for("admin_panel"))
        else:
            flash("User is not found please enter valid email or password", 'danger')
    return render_template("admin/alogin.html", form=form, title="ALogin")


# Student Register Page
@app.route("/sregister", methods=["GET", "POST"])
def sregister():
    form = SRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(fname=form.fname.data,
                          lname=form.lname.data,
                          email=form.email.data,
                          mobile=form.mobile.data,
                          dob=form.dob.data,
                          address=form.address.data,
                          password=hashed_password
                          )
        db.session.add(student)
        db.session.commit()
        # flash(f"Account Created for {form.fname.data}!", 'success')
        return redirect(url_for("student_details"))
    return render_template("student/sregister.html", form=form, title="SRegister")



# Student Login Page
@app.route("/slogin", methods=["GET", "POST"])
def slogin():
    form = SLogin(request.form)
    if request.method == "POST":
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("User is not found. Please check your email and password", "danger")
    return render_template("student/slogin.html", form=form, title="SLogin")


# Student Corner Page
@app.route("/scorner")
def scorner():
    return render_template("student/student_corner.html", title="SCorner")


# Contact Us Page
@app.route("/contact")
def contact():
    return render_template("student/Contact_us.html", title="Contact-us")


# student Admin Panel
@app.route("/admin_panel")
def admin_panel():
    return render_template("layout/admin_layout.html",title="Admin")

#Student Details
@app.route("/sdetails")
def student_details():
    return render_template("student/student_details.html", title="Stuent-Details",students=students)

