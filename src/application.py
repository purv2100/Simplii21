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
import bcrypt
import os
import csv
import sys
from dotenv import load_dotenv
from flask_login import LoginManager, login_required
import uuid
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, PostingForm, ApplyForm, TaskForm, UpdateForm
import plotly.express as px
import pandas as pd

load_dotenv()

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/simplii'
mongo = PyMongo(app)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'simpli7423@gmail.com'
app.config['MAIL_PASSWORD'] = 'qjdc klot ntgx kdci'
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
    token = str(uuid.uuid1())
    mongo.db.users.update_one({'email': email, },
                              {'$set': {'token': token}})
    return token


def send_reset_email(email, token):
    msg = Message('Password Reset Request',
                  sender='simplii043@gmail.com', recipients=[email])
    msg.body = f'''To reset your password, visit the following link: {url_for('reset_password', token=token, _external=True)}

If you did not make this request, simply ignore this email.
'''
    mail.send(msg)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        # Validate the token (you may want to add more security checks)
        user = mongo.db.users.find_one({'token': token})
        password = request.form.get('password')
        print(password)
        if user:
            # Update the password

            mongo.db.users.update_one({'token': token}, {'$set': {'pwd': bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt())}})

            # Remove the reset token
            mongo.db.users.update_one(
                {'token': token}, {'$unset': {'token': 1}})

            flash(
                'Password reset successfully. You can now log in with your new password.', 'success')
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


@app.route("/friends")
def friends():
    # ############################
    # friends() function displays the list of friends corrsponding to given email
    # route "/friends" will redirect to friends() function which redirects to friends.html page.
    # friends() function will show a list of "My friends", "Add Friends" functionality, "send Request" and Pending Approvals" functionality
    # Details corresponding to given email address are fetched from the database entries
    # Input: Email
    # Output: My friends, Pending Approvals, Sent Requests and Add new friends
    # ##########################
    email = session.get('email')

    if email is not None:
        myFriends = list(mongo.db.friends.find(
            {'sender': email, 'accept': True}, {'sender', 'receiver', 'accept'}))
        myFriendsList = list()

        for f in myFriends:
            myFriendsList.append(f['receiver'])

        # print(myFriends)
        allUsers = list(mongo.db.users.find({}, {'name', 'email'}))
        # print(allUsers)

        pendingRequests = list(mongo.db.friends.find(
            {'sender': email, 'accept': False}, {'sender', 'receiver', 'accept'}))
        pendingReceivers = list()
        for p in pendingRequests:
            pendingReceivers.append(p['receiver'])

        pendingApproves = list()
        pendingApprovals = list(mongo.db.friends.find(
            {'receiver': email, 'accept': False}, {'sender', 'receiver', 'accept'}))
        for p in pendingApprovals:
            pendingApproves.append(p['sender'])

        # print(pendingApproves)
    else:
        return redirect(url_for('login'))

    # print(pendingRequests)
    return render_template('friends.html', allUsers=allUsers, pendingRequests=pendingRequests, active=email,
                           pendingReceivers=pendingReceivers, pendingApproves=pendingApproves, myFriends=myFriends, myFriendsList=myFriendsList)


@app.route("/ajaxsendrequest", methods=['POST'])
def ajaxsendrequest():
    # ############################
    # ajaxsendrequest() is a function that updates friend request information into database
    # route "/ajaxsendrequest" will redirect to ajaxsendrequest() function.
    # Details corresponding to given email address are fetched from the database entries and send request details updated
    # Input: Email, receiver
    # Output: DB entry of receiver info into database and return TRUE if success and FALSE otherwise
    # ##########################
    email = session.get('email')
    if email is not None:
        receiver = request.form.get('receiver')
        res = mongo.db.friends.insert_one(
            {'sender': email, 'receiver': receiver, 'accept': False})
        if res:
            return json.dumps({'status': True}), 200, {
                'ContentType': 'application/json'}
    return json.dumps({'status': False}), 500, {
        'ContentType:': 'application/json'}


@app.route("/ajaxcancelrequest", methods=['POST'])
def ajaxcancelrequest():
    # ############################
    # ajaxcancelrequest() is a function that updates friend request information into database
    # route "/ajaxcancelrequest" will redirect to ajaxcancelrequest() function.
    # Details corresponding to given email address are fetched from the database entries and cancel request details updated
    # Input: Email, receiver
    # Output: DB deletion of receiver info into database and return TRUE if success and FALSE otherwise
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        receiver = request.form.get('receiver')
        res = mongo.db.friends.delete_one(
            {'sender': email, 'receiver': receiver})
        if res:
            return json.dumps({'status': True}), 200, {
                'ContentType': 'application/json'}
    return json.dumps({'status': False}), 500, {
        'ContentType:': 'application/json'}


@app.route("/ajaxapproverequest", methods=['POST'])
def ajaxapproverequest():
    # ############################
    # ajaxapproverequest() is a function that updates friend request information into database
    # route "/ajaxapproverequest" will redirect to ajaxapproverequest() function.
    # Details corresponding to given email address are fetched from the database entries and approve request details updated
    # Input: Email, receiver
    # Output: DB updation of accept as TRUE info into database and return TRUE if success and FALSE otherwise
    # ##########################
    email = get_session = session.get('email')
    if get_session is not None:
        receiver = request.form.get('receiver')
        print(email, receiver)
        res = mongo.db.friends.update_one({'sender': receiver, 'receiver': email}, {
                                          "$set": {'sender': receiver, 'receiver': email, 'accept': True}})
        mongo.db.friends.insert_one(
            {'sender': email, 'receiver': receiver, 'accept': True})
        if res:
            return json.dumps({'status': True}), 200, {
                'ContentType': 'application/json'}
    return json.dumps({'status': False}), 500, {
        'ContentType:': 'application/json'}


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


@app.route("/analytics")
def analytics():
    # ############################
    # analytics() function displays visualizations related to tasks of the user.
    # route "/analytics" will redirect to analytics() function.
    # ##########################
    email = session.get('email')
    data = mongo.db.tasks.find({'email': email}, {'category'})
    data_list = list(data)
    data = pd.DataFrame(data_list)

    # Create a histogram using Plotly Express
    fig = px.histogram(data, x='category', nbins=3, title="Histogram Example")

    # You can customize the layout and appearance of the histogram, e.g., titles, labels, colors, etc.
    fig.update_layout(
        xaxis_title="Categories",
        yaxis_title="Frequency",
        font=dict(family="Arial", size=18, color="black"),
        paper_bgcolor="white",
        plot_bgcolor="lightgray",
        width=550,
        height=550,
    )

    # Customize the y-axis ticks to show integer values
    fig.update_yaxes(dtick=1)

    # Convert the Plotly figure to HTML
    chart_html = fig.to_html(full_html=False)
    return render_template('analytics.html', chart_html=chart_html, title='Analytics')


@app.route("/view_tasks")
def view_tasks():
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
                mongo.db.users.insert_one({'name': username, 'email': email, 'pwd': bcrypt.hashpw(
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
                description = request.form.get('description')

                date_format = "%Y-%m-%d"
                datediff = datetime.strptime(
                    duedate, date_format) - datetime.strptime(startdate, date_format)
                print(datediff, "difffffff")
                print("start date", startdate)
                if (not is_integer(hours)):
                    flash(f' Error hours should be numeric!', 'danger')
                elif (datediff.days < 0):
                    flash(f' DueDate should be a future date!', 'danger')
                else:
                    mongo.db.tasks.insert_one({'email': email,
                                               'taskname': taskname,
                                               'category': category,
                                               'startdate': startdate,
                                               'duedate': duedate,
                                               'status': status,
                                               'hours': hours,
                                               'description': description})
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
        # print(id, '_______-----______---- ID ------_____-----____')
        return json.dumps({'taskname': id['taskname'], 'catgeory': id['category'], 'startdate': id['startdate'], 'duedate': id['duedate'], 'status': id['status'], 'hours': id['hours'], 'description': id['description']}), 200, {
            'ContentType': 'application/json'}
    else:
        return "Failed"


def is_integer(s):
    try:
        # Try to convert the string to an integer
        int_value = int(s)
        return True
    except ValueError:
        # ValueError is raised if the conversion fails
        return False


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
        # print(params, "______------_____------______--- PARAMMMMSSSSSSSSS")
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

        # print(d)

        form = UpdateForm()

        form.taskname.data = d['taskname']
        form.category.data = d['category']
        form.status.data = d['status']
        form.hours.data = d['hours']
        form.description.data = d['des']
        date_format = "%Y-%m-%d"
        form.startdate.data = datetime.strptime(d['startdate'], date_format)
        form.duedate.data = datetime.strptime(d['duedate'], date_format)

        # print(d['startdate'], "start")

        if form.validate_on_submit():
            if request.method == 'POST':
                email = session.get('email')
                taskname = request.form.get('taskname')
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                duedate = request.form.get('duedate')
                hours = request.form.get('hours')
                status = request.form.get('status')
                datediff = datetime.strptime(
                    duedate, "%Y-%m-%d") - datetime.strptime(startdate, "%Y-%m-%d")
                description = request.form.get('description')
                print(datediff, "difffffff")
                print("start date", startdate)
                if (not is_integer(hours)):
                    flash(f' Error hours should be numeric!', 'danger')
                elif (datediff.days < 0):
                    flash(f' DueDate should be a future date!', 'danger')
                else:
                    mongo.db.tasks.update_one({'email': email, 'taskname': d['taskname'], 'startdate': d['startdate'],
                                               'duedate': d['duedate']},
                                              {'$set': {'taskname': taskname, 'startdate': startdate,
                                                        'duedate': duedate, 'category': category, 'status': status,
                                                        'hours': hours, 'description': description}})
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
                'email', 'pwd', 'temp'})
            if temp is not None and temp['email'] == form.email.data and (
                bcrypt.checkpw(
                    form.password.data.encode("utf-8"),
                    temp['pwd']) or temp == form.password.data):
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
            msg = Message('Task due tomorrow', sender=os.getenv(
                'MAIL_USERNAME'), recipients=[task['email']])
            msg.body = "Hey, your task " + \
                task['taskname'] + " is due tomorrow"
            mail.send(msg)

    return "Message sent"


scheduler.add_job(emailReminder, 'cron', hour=8, minute=0)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
