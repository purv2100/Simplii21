from datetime import datetime, timedelta
from bson.objectid import ObjectId

from flask_wtf import form
from flask import app, render_template, session, url_for, flash, redirect, request, Response, Flask
from flask_pymongo import PyMongo
from flask import json
from flask.helpers import make_response
from flask.json import jsonify
from flask_mail import Mail, Message
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, PostingForm, ApplyForm, TaskForm
import bcrypt

from flask_login import LoginManager, login_required
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/simplii'
mongo = PyMongo(app)

"""app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "bogusdummy123@gmail.com"
app.config['MAIL_PASSWORD'] = "helloworld123!"
mail = Mail(app)
"""

@app.route("/")
@app.route("/home")
def home():
############################ 
# home() function displays the homepage of our website.
# route "/home" will redirect to home() function. 
# input: The function takes session as the input 
# Output: Out function will redirect to the login page
# ########################## 
    if session.get('email'):
        return redirect(url_for('dummy'))
    else:
        return redirect(url_for('login'))

@app.route("/forgotPassword")
def forgotPassword():
    return redirect(url_for('dummy'))

@app.route("/dashboard")
def dashboard():
    return redirect(url_for('dummy'))

@app.route("/about")
def about():
# ############################ 
# about() function displays About Us page (about.html) template
# route "/about" will redirect to home() function. 
# ########################## 
    return redirect(url_for('dummy'))

@app.route("/register", methods=['GET', 'POST'])
def register():
# ############################ 
# register() function displays the Registration portal (register.html) template
# route "/register" will redirect to register() function.
# RegistrationForm() called and if the form is submitted then various values are fetched and updated into database
# Input: Username, Email, Password, Confirm Password
# Output: Value update in database and redirected to home login page
# ########################## 
    if not session.get('email'):
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                mongo.db.users.insert({'name': username, 'email': email, 'pwd': bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()), 'temp': None})
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/task", methods=['GET', 'POST'])
def task():
# ############################ 
# task() function displays the Add Task portal (task.html) template
# route "/task" will redirect to task() function.
# TaskForm() called and if the form is submitted then new task values are fetched and updated into database
# Input: Task, Category, start date, end date, number of hours
# Output: Value update in database and redirected to home login page
# ########################## 
    if not session.get('email'):
        form = TaskForm()
        if form.validate_on_submit():
            print("inside form")
            if request.method == 'POST':
                email = session.get('email')
                taskname = request.form.get('taskname')
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                duedate = request.form.get('duedate')
                hours = request.form.get('hours')
                mongo.db.tasks.insert({'email':email, 'taskname': taskname, 'category': category, 'startdate': startdate,'duedate': duedate, 'hours': hours})
            flash(f' {form.taskname.data} Task Added!', 'success')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('home'))
    return render_template('task.html', title='Task', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
# ############################ 
# login() function displays the Login form (login.html) template
# route "/login" will redirect to login() function.
# LoginForm() called and if the form is submitted then various values are fetched and verified from the database entries
# Input: Email, Password, Login Type 
# Output: Account Authentication and redirecting to Dashboard
# ########################## 
    if not session.get('email'):
        form = LoginForm()
        if form.validate_on_submit():
            temp = mongo.db.users.find_one({'email': form.email.data}, {
                                         'email', 'pwd'})
            if temp is not None and temp['email'] == form.email.data and (
                bcrypt.checkpw(
                    form.password.data.encode("utf-8"),
                    temp['pwd']) or temp['temp'] == form.password.data):
                flash('You have been logged in!', 'success')
                session['email'] = temp['email']
                return redirect(url_for('dashboard'))
            else:
                flash(
                    'Login Unsuccessful. Please check username and password',
                    'danger')
    else:
        return redirect(url_for('home'))
    return render_template(
        'login.html',
        title='Login',
        form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
# ############################ 
# logout() function just clears out the session and returns success
# route "/logout" will redirect to logout() function.
# Output: session clear 
# ########################## 
    session.clear()
    return "success"


@app.route("/dummy", methods=['GET'])
def dummy():
# ############################ 
# dummy() function performs the functionality displaying the message "feature will be added soon"
# route "/dummy" will redirect to dummy() function.
# Output: redirects to dummy.html
# ########################## 
    """response = make_response(
                redirect(url_for('home'),200),
            )
    response.headers["Content-Type"] = "application/json",
    response.headers["token"] = "123456"
    return response"""
    return "Page Under Maintenance"


if __name__ == '__main__':
    app.run(debug=True)
