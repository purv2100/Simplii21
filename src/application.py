from datetime import datetime, timedelta
from bson.objectid import ObjectId

from flask_wtf import form
from flask import app, render_template, session, url_for, flash, redirect, request, Response, Flask
from flask_pymongo import PyMongo
from flask import json
from flask.helpers import make_response
from flask.json import jsonify
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, PostingForm, ApplyForm, TaskForm, UpdateForm
import bcrypt
import os
import csv
import sys
from dotenv import load_dotenv
from flask_login import LoginManager, login_required
import uuid
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

scheduler = BackgroundScheduler()

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
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


def generate_reset_token(email):
    token=str(uuid.uuid1())
    mongo.db.users.update_one({'email': email, },
                                      {'$set': {'token':token}})
    return token

def send_reset_email(email, token):
    msg = Message('Password Reset Request', sender='simplii043@gmail.com', recipients=[email])
    msg.body = f'''To reset your password, visit the following link: {url_for('reset_password', token=token, _external=True)}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        # Validate the token (you may want to add more security checks)
        user = mongo.db.users.find_one({'token': token})
        password=request.form.get('password')
        print(password)
        if user:
            # Update the password
            
            mongo.db.users.update_one({'token':token}, {'$set': {'pwd': bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt())}})

            # Remove the reset token
            mongo.db.users.update_one({'token':token}, {'$unset': {'token': 1}})

            flash('Password reset successfully. You can now log in with your new password.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid or expired token. Please try again.', 'danger')

    return render_template('resetPass.html', token=token)

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    ############################
    # forgotPassword() redirects the user to dummy template.
    # route "/forgotPassword" will redirect to forgotPassword() function.
    # input: The function takes session as the input
    # Output: Out function will redirect to the dummy page
    # ##########################
    if not session.get('email'):
        form = ResetPasswordForm()
        if request.method == 'POST':
            email = request.form.get('email')
            user = mongo.db.users.find_one({'email': email})
            if user:
                token = generate_reset_token(email)
                send_reset_email(user['email'], token)
                flash('Password reset email sent. Check your inbox.', 'info')
            else:
                flash('Email not found. Please register.', 'danger')

            print(email)
    return render_template('forgotPass.html', title='Forget', form=form)


@app.route("/recommend")
def recommend():
    ############################
    # recommend() function opens the task_recommendation.csv file and displays the data of the file
    # route "/recommend" will redirect to recommend() function.
    # input: The function opens the task_recommendation.csv
    # Output: Our function will redirect to the recommend page for showing the data
    # ##########################
    data = []
    with open(os.path.join(sys.path[0], "../models/task_recommendation.csv")) as f:
        reader = csv.DictReader(f)

        for row in reader:
            data.append(dict(row))

    return render_template('recommend.html', data=data, list=list)


@app.route("/dashboard")
def dashboard():
    ############################
    # dashboard() function displays the tasks of the user
    # route "/dashboard" will redirect to dashboard() function.
    # input: The function takes session as the input and fetches user tasks from Database
    # Output: Our function will redirect to the dashboard page with user tasks being displayed
    # ##########################
    tasks = ''
    if session.get('email'):
        tasks = mongo.db.tasks.find({'email': session.get('email')})
    return render_template('dashboard.html', tasks=tasks)


@app.route("/about")
def about():
    # ############################
    # about() function displays About Us page (about.html) template
    # route "/about" will redirect to about() function.
    # ##########################
    return render_template('about.html', title='About')


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


@app.route("/deleteTask", methods=['GET', 'POST'])
def deleteTask():
    ############################
    # deleteTask() function will delete the particular user task from database.
    # route "/deleteTask" will redirect to deleteTask() function.
    # input: The function takes email, task, status, category as the input and fetches from the database
    # Output: Out function will delete the particular user task from database
    # ##########################
    if request.method == 'POST':
        email = session.get('email')
        task = request.form.get('task')
        status = request.form.get('status')
        category = request.form.get('category')
        id = mongo.db.tasks.find_one(
            {'email': email, 'taskname': task, 'status': status, 'category': category}, {'_id'})
        print("Hereeeeeeeeeeeeeee", id['_id'])
        mongo.db.tasks.delete_one({'_id': id['_id']})
        return "Success"
    else:
        return "Failed"


@app.route("/task", methods=['GET', 'POST'])
def task():
    # ############################
    # task() function displays the Add Task portal (task.html) template
    # route "/task" will redirect to task() function.
    # TaskForm() called and if the form is submitted then new task values are fetched and updated into database
    # Input: Task, Category, start date, end date, number of hours
    # Output: Value update in database and redirected to home login page
    # ##########################
    if session.get('email'):
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
                status = request.form.get('status')
                mongo.db.tasks.insert({'email': email,
                                       'taskname': taskname,
                                       'category': category,
                                       'startdate': startdate,
                                       'duedate': duedate,
                                       'status': status,
                                       'hours': hours})
            flash(f' {form.taskname.data} Task Added!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('task.html', title='Task', form=form)


@app.route("/editTask", methods=['GET', 'POST'])
def editTask():
    ############################
    # editTask() function helps the user to edit a particular task and update in database.
    # route "/editTask" will redirect to editTask() function.
    # input: The function takes email, task, status, category as the input
    # Output: Out function will update new values in the database
    # ##########################
    if request.method == 'POST':
        email = session.get('email')
        task = request.form.get('task')
        status = request.form.get('status')
        category = request.form.get('category')
        id = mongo.db.tasks.find_one(
            {'email': email, 'taskname': task, 'status': status, 'category': category})
        return json.dumps({'taskname': id['taskname'], 'catgeory': id['category'], 'startdate': id['startdate'], 'duedate': id['duedate'], 'status': id['status'], 'hours': id['hours']}), 200, {
            'ContentType': 'application/json'}
    else:
        return "Failed"


@app.route("/updateTask", methods=['GET', 'POST'])
def updateTask():
    ############################
    # updateTask() function displays the updateTask.html page for updations
    # route "/updateTask" will redirect to updateTask() function.
    # input: The function takes variious task values as Input
    # Output: Out function will redirect to the updateTask page
    # ##########################
    if session.get('email'):
        params = request.url.split('?')[1].split('&')
        for i in range(len(params)):
            params[i] = params[i].split('=')
        for i in range(len(params)):
            if "%" in params[i][1]:
                index = params[i][1].index('%')
                params[i][1] = params[i][1][:index] + \
                    " " + params[i][1][index + 3:]
        d = {}
        for i in params:
            d[i[0]] = i[1]

        form = UpdateForm()

        form.taskname.data = d['taskname']
        form.category.data = d['category']
        form.status.data = d['status']
        form.hours.data = d['hours']

        if form.validate_on_submit():
            if request.method == 'POST':
                email = session.get('email')
                taskname = request.form.get('taskname')
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                duedate = request.form.get('duedate')
                hours = request.form.get('hours')
                status = request.form.get('status')
                mongo.db.tasks.update({'email': email, 'taskname': d['taskname'], 'startdate': d['startdate'], 'duedate': d['duedate']},
                                      {'$set': {'taskname': taskname, 'startdate': startdate, 'duedate': duedate, 'category': category, 'status': status, 'hours': hours}})
            flash(f' {form.taskname.data} Task Updated!', 'success')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('home'))
    return render_template('updateTask.html', title='Task', form=form)


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

def emailReminder():
    # ############################
    # emailReminder() function is called by cron job that runs at 8 am every day
    # This function will check if there is any uncompleted task that is due the next day
    # If yes, then it remind user to complete that task
    # Output: send mails to users about uncompleted tasks
    # ##########################
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    tasks = mongo.db.tasks.find({"duedate": tomorrow, "status": "In Progress"})

    for task in tasks:
        with app.app_context():
            msg = Message('Task due tomorrow', sender = os.getenv('MAIL_USERNAME'), recipients = [ task['email'] ])
            msg.body = "Hey, your task " + task['taskname'] + " is due tomorrow"
            mail.send(msg)

    return "Message sent"

scheduler.add_job(emailReminder, 'cron', hour=8, minute=0)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
