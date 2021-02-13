import os
import secrets
from sqlalchemy import or_
from PIL import Image
from flask import render_template, flash, url_for, redirect, request, session, logging, abort
from app.form import (ARegisterForm, ALogin, SLogin,
                      SRegisterForm, UpdateAccountForm,
                      UpdateStudent, UpdateAdmin,ContactUsForm,
                      RequestResetForm,ResetPasswordForm)
from app import app, db, bcrypt
from app.models import Student, Admin
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps


# Home Page
@app.route("/")
@app.route("/home")
def home():
    return render_template("student/index.html")


# About Page
@app.route("/about")
def about():
    return render_template("student/about.html", title = "About")


# not found
@app.route("/notfound")
def not_found():
    return render_template('layout/notfound.html')


# admin blocker
def is__logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("not_found"))

    return wrap


# Admin Register page
@app.route("/aregister/new", methods = ["GET", "POST"])
@is__logged_in
def aregister():
    form = ARegisterForm(request.form)
    if request.method == "POST" and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(
            fname = form.fname.data,
            lname = form.lname.data,
            email = form.email.data,
            mobile = form.mobile.data,
            address = form.address.data,
            password = hashed_password
        )
        db.session.add(admin)
        db.session.commit()
        flash('You Have Registred Successfully Now Logged in!', "success")
        return redirect(url_for("admin_details"))
    return render_template('admin/aregister.html', form = form, title = "ARegister")


# Admin Login Page
@app.route("/admin", methods = ["GET", "POST"])
def alogin():
    form = ALogin(request.form)
    if request.method == "POST":
        admin = Admin.query.filter_by(email = form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            session['logged_in'] = True
            session['email'] = form.email.data

            # login_user(admin, remember = form.remember.data)
            # next_page = request.args.get('next')
            # return redirect(next_page) if next_page else
            return redirect(url_for("admin_panel"))
        else:
            flash("User is not found please enter valid email or password", 'danger')
    return render_template("admin/alogin.html", form = form, title = "ALogin")


# admin account details
# @app.route("/aaccount")
# @is__logged_in
# def aaccount():
#     return render_template('admin/aacount.html')

# admin logout
@app.route("/alogout")
@is__logged_in
def alogout():
    # logout_user()
    session.clear()
    return redirect(url_for('alogin'))


# Student Register Page
@app.route("/sregister/new", methods = ["GET", "POST"])
@is__logged_in
def sregister():
    form = SRegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(fname = form.fname.data, lname = form.lname.data,
                          enroll = form.enroll.data,
                          email = form.email.data,
                          mobile = form.mobile.data,
                          address = form.address.data,
                          dob = form.dob.data,
                          password = hashed_password)
        db.session.add(student)
        db.session.commit()

        # flash(f"Account Created for {form.fname.data}!", 'success')
        return redirect(url_for("student_details"))
    return render_template("student/sregister.html", form = form, title = "SRegister")


# Student Login Page
@app.route("/slogin", methods = ["GET", "POST"])
def slogin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SLogin(request.form)
    if request.method == "POST":
        student = Student.query.filter_by(enroll = form.enroll.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("User is not found. Please check your enroll-number and password", "danger")
    return render_template("student/slogin.html", form = form, title = "SLogin")


# save picture ever time using os and file type
def save_picture(form_picture):
    random_hax = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hax + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# Student Account Details of student
@app.route("/saccount", methods = ["GET", "POST"])
@login_required
def saccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.address = form.address.data
        current_user.email = form.email.data
        db.session.commit()
        flash("You account has been updated", "success")
        return redirect(url_for('saccount'))
    elif request.method == "GET":
        form.address.data = current_user.address
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'img/' + current_user.image_file)
    return render_template('student/saccount.html', title = 'Account', image_file = image_file, form = form)


# student logout
@app.route("/slogout")
@login_required
def slogout():
    logout_user()
    flash("You are logged out!", 'success')
    return redirect(url_for('home'))


# Student Corner Page
@app.route("/scorner")
def scorner():
    return render_template("student/student_corner.html", title = "SCorner")


# Contact Us Page
@app.route("/contact")
def contact():
    form = ContactUsForm(request.form)
    return render_template("student/Contact_us.html", title = "Contact-us",form=form)


# student Admin Panel
@app.route("/admin_panel")
@is__logged_in
def admin_panel():
    return render_template("admin/dashbord.html", title = "Admin")


#Reset Request
@app.route("/reset_request")
def reset_request():
    form = RequestResetForm(request.form)
    return render_template("student/reset_request.html", form=form, title="Reset-Request")


# Student full Details in admin panel
@app.route("/sview/<int:s_id>")
def sview(s_id):
    student = Student.query.get_or_404(s_id)
    return render_template("student/s_view.html", title = 'S_view', student = student)


# Update student details
@app.route("/supdate/<int:s_id>", methods = ["GET", "POST"])
def supdate(s_id):
    student = Student.query.get_or_404(s_id)
    if student.email != session:
        form = UpdateStudent(request.form)
        if form.validate_on_submit():
            student.fname = form.fname.data
            student.lname = form.lname.data
            student.email = form.email.data
            student.mobile = form.mobile.data
            student.address = form.address.data
            student.dob = form.dob.data
            db.session.commit()
            return redirect(url_for('sview', s_id=student.s_id))
        elif request.method == "GET":
            form.fname.data = student.fname
            form.lname.data = student.lname
            form.email.data = student.email
            form.mobile.data = student.mobile
            form.address.data = student.address
            form.dob.data = student.dob
        return render_template("student/update_student.html", title = 'Student Update', student = student, form = form)
#Delete Student
@app.route("/sview/<int:s_id>/delete", methods=['POST'])
def delete_student(s_id):
    student = Student.query.get_or_404(s_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('student_details'))


# Student Details
@app.route("/sdetails",methods=["POST","GET"])
@is__logged_in
def student_details():
    page = request.args.get('page', 1, type=int)
    students = Student.query.order_by(Student.s_id.desc()).paginate(page=page, per_page=5)
    if request.method == "POST" and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        students = Student.query.filter(or_(Student.fname.like(search),
                                            Student.lname.like(search),
                                            Student.email.like(search))).paginate(error_out = False)
        return render_template('student/student_details.html',students=students,tag=tag)
    else:
        "Not Found"
    return render_template("student/student_details.html", title = "Stuent-Details", students = students)

#admin view
@app.route("/aview/<int:a_id>")
@is__logged_in
def aview(a_id):
    admin = Admin.query.get_or_404(a_id)
    return render_template("admin/a_view.html", title = 'A_view', admin = admin)

#admin update
@app.route("/aupdate/<int:a_id>", methods = ["GET", "POST"])
def aupdate(a_id):
    admin = Admin.query.get_or_404(a_id)
    if admin.email != session:
        form = UpdateAdmin(request.form)
        if form.validate_on_submit():
            admin.fname = form.fname.data
            admin.lname = form.lname.data
            admin.email = form.email.data
            admin.mobile = form.mobile.data
            admin.address = form.address.data
            db.session.commit()
            return redirect(url_for('aview', a_id=admin.a_id))
        elif request.method == "GET":
            form.fname.data = admin.fname
            form.lname.data = admin.lname
            form.email.data = admin.email
            form.mobile.data = admin.mobile
            form.address.data = admin.address
        return render_template("admin/update_admin.html", title = 'Admin Update', admin = admin, form = form)

#admin delete@
@app.route("/aview/<int:a_id>/delete",methods=["POST"])
@is__logged_in
def delete_admin(a_id):
    admin = Admin.query.get_or_404(a_id)
    db.session.delete(admin)
    db.session.commit()
    return redirect(url_for("admin_details"))

# admin details routing
@app.route("/adetails",methods=["POST","GET"])
@is__logged_in
def admin_details():
    page = request.args.get('page', 1 ,type=int)
    admins = Admin.query.order_by(Admin.a_id.desc()).paginate(per_page=5, page=page )
    if request.method == "POST" and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        admins = Admin.query.filter(or_(Admin.fname.like(search),
                                        Admin.lname.like(search),
                                        Admin.email.like(search))).paginate(error_out = False)
    return render_template("admin/admin_details.html", title = "Admin-Details", admins = admins)
