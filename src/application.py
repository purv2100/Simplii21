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
import plotly.graph_objs as go

from plotly.subplots import make_subplots

import pandas as pd
import dash

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
    """
    friends() function displays the list of friends corresponding to the given email.
    The route "/friends" will redirect to the friends() function, which further redirects to the friends.html page.
    The friends() function presents a list of "My friends," "Add Friends" functionality, "Send Request," and "Pending Approvals."
    Details corresponding to the given email address are fetched from the database entries.

    Input:
        Email (retrieved from the session)

    Output:
        Rendered template 'friends.html' with the following variables:
        - allUsers: A list of all users with their names and emails
        - pendingRequests: A list of friend requests sent by the user that are pending approval
        - active: The email address of the current user
        - pendingReceivers: A list of users who have sent friend requests to the current user (pending approval)
        - pendingApproves: A list of users whose friend requests to the current user are pending approval
        - myFriends: A list of accepted friend relationships (sender, receiver, accept=True)
        - myFriendsList: A list of email addresses corresponding to the user's accepted friends

    """
    email = session.get('email')

    if email is not None:
        myFriends = list(mongo.db.friends.find(
            {'sender': email, 'accept': True}, {'sender', 'receiver', 'accept'}))
        myFriendsList = list()

        for f in myFriends:
            myFriendsList.append(f['receiver'])

        print(myFriends)
        allUsers = list(mongo.db.users.find({}, {'name', 'email'}))
        print(allUsers)
        
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
    """
    ajaxsendrequest() is a function that updates friend request information in the database.
    The route "/ajaxsendrequest" redirects to ajaxsendrequest() function.
    Details corresponding to the given email address are fetched from the database entries, and send request details are updated.

    Input:
        - Email (retrieved from the session)
        - Receiver (retrieved from the form data in the request)

    Output:
        - Database entry of receiver information in the database.
        - Returns JSON response with status True if the operation is successful, and False otherwise.
    """
    
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
    """
    ajaxsendrequest() is a function that updates friend request information into the database.
    The route "/ajaxsendrequest" will redirect to the ajaxsendrequest() function.
    Details corresponding to the given email address are fetched from the database entries, and send request details are updated.

    Input:
        Email (retrieved from the session)
        Receiver (retrieved from the form data in the request)

    Output:
        - Database entry of receiver information into the database.
        - Returns JSON response with status True if the operation is successful, and False otherwise.
    """
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
    """
    ajaxapproverequest() is a function that updates friend request information into the database.
    The route "/ajaxapproverequest" will redirect to the ajaxapproverequest() function.
    Details corresponding to the given email address are fetched from the database entries, and approve request details are updated.

    Input:
        Email (retrieved from the session)
        Receiver (retrieved from the form data in the request)

    Output:
        - Database update of accept as TRUE information into the database.
        - Returns JSON response with status True if the operation is successful, and False otherwise.
    """
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

def get_first_day_of_week(date):
    # Calculate the difference between the current day and Monday (0)
    days_to_monday = date.weekday()

    # Subtract the difference to get the first day of the week
    first_day_of_week = date - timedelta(days=days_to_monday)

    return first_day_of_week

@app.route("/analytics")
def analytics():
    # ############################
    # analytics() function displays visualizations related to tasks of the user.
    # route "/analytics" will redirect to analytics() function.
    # ##########################
    email = session.get('email')
    # Check if there are any tasks in the database.
    data = mongo.db.tasks.find({'email': email})
    if data is not None:
        # ----------------------------------------------------------------------------------------
        # Histogram of tasks based on 'Category': Easy, Medium, Hard 
        data_hist = mongo.db.tasks.find({'email': email}, {'category'})
        data_hist_list = list(data_hist)
        data_hist = pd.DataFrame(data_hist_list)

        # Create a histogram using Plotly Express
        fig = px.histogram(data_hist, x='category', nbins=3, title="Histogram Example")

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
        hist_html = fig.to_html(full_html=False)

        # ----------------------------------------------------------------------------------------
        # Side-by-side bar chart of expected hours and actual hours required to complete the task
        # Only consider the tasks which are complete. i.e. progress = 1
        data_exp_act = mongo.db.tasks.find({'email':email, 'completed':True}, {'taskname', 'starttime', 'endtime', 'actualhours'})

        data_exp_act_df = pd.DataFrame(columns = ['Name', 'Expected Hours', 'Actual Hours'])
        time_format = "%H:%M"
        i=0
        for task in data_exp_act:
            start_time = datetime.strptime(task['starttime'], time_format)
            end_time = datetime.strptime(task['endtime'], time_format)
            expected_hours = (end_time - start_time).total_seconds()/3600
            data_exp_act_df.loc[i] = [task['taskname'], expected_hours, task['actualhours']]
            i+=1

        print(data_exp_act_df)
        # Set a fixed bar width
        bar_width = 0.4

        # Calculate the total width occupied by bars and gaps
        total_width = len(data_exp_act_df) * ((2 * bar_width)+0.1)   # 0.1 is the sum of bargap and bargroupgap

        # Calculate the figure size based on the total width
        fig_width = max(4, total_width)  # Ensure a minimum width

        # Create trace for Value1 with custom bar color
        trace1 = go.Bar(x=data_exp_act_df['Name'], y=data_exp_act_df['Expected Hours'], name='Expected Hours', marker=dict(color='green'), width=bar_width)

        # Create trace for Value2 with a different bar color
        trace2 = go.Bar(x=data_exp_act_df['Name'], y=data_exp_act_df['Actual Hours'], name='Actual Hours', marker=dict(color='cyan'), width=bar_width)

        # Create layout
        layout = go.Layout(barmode='group', title='Side-by-Side Bar Chart', xaxis=dict(title='Task Name'), yaxis=dict(title='Hours to Complete'), width=fig_width*80, height=400)

        # Create figure
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        exp_act_html = fig.to_html(full_html=False)

        # ----------------------------------------------------------------------------------------
        # Time chart to show distribution of completed tasks across different years,
        # different months and different weeks.

        timeline_data = mongo.db.tasks.find({'email':email, 'completed':True}, {'startdate'})
        timeline_list = list(timeline_data)
        timeline_df = pd.DataFrame(timeline_list)

        timeline_df['startdate'] = [datetime.strptime(date, "%Y-%m-%d") for date in timeline_df['startdate']]

        year = [start_date.year for start_date in timeline_df['startdate']]
        timeline_df['year'] = year

        timeline_df['week'] = timeline_df['startdate'].dt.strftime('Week %U, %Y')

        timeline_df['month_year'] = timeline_df['startdate'].dt.strftime('%b \'%y')

        # Year-wise distribution of tasks
        layout = go.Layout(title='Yearwise distribution of tasks', xaxis=dict(title='Year'), yaxis=dict(title='Frequency'))

        year_hist = go.Histogram(x=timeline_df['year'], name='Completed tasks by year')
        fig = go.Figure(data=[year_hist], layout=layout)
        fig.update_xaxes(dtick = 1)

        # Convert the Plotly figure to HTML
        by_year_html = fig.to_html(full_html=False)

        # Monthly distribution of tasks
        layout = go.Layout(title='Monthly distribution of tasks', xaxis=dict(title='Month'), yaxis=dict(title='Frequency'))

        month_hist = go.Histogram(x=timeline_df['month_year'], name='Completed tasks by month')
        fig = go.Figure(data=[month_hist], layout=layout)
        fig.update_xaxes(dtick = 1)

        # Convert the Plotly figure to HTML
        by_month_html = fig.to_html(full_html=False)

        # Weekly distribution of tasks
        layout = go.Layout(title='Weekly distribution of tasks', xaxis=dict(title='Week'), yaxis=dict(title='Frequency'))

        week_hist = go.Histogram(x=timeline_df['week'], name='Completed tasks by week')
        fig = go.Figure(data=[week_hist], layout=layout)
        fig.update_xaxes(dtick = 1)

        # Convert the Plotly figure to HTML
        by_week_html = fig.to_html(full_html=False)

        #----------------------------------------------------------------------------------------------
        # Pie chart to show complete and incomplete tasks.

        pie_data = mongo.db.tasks.find({'email': email}, {'completed'})
        pie_data_list = list(pie_data)
        pie_df = pd.DataFrame(pie_data_list)

        map_category = {True: "Complete", False: "Incomplete"}

        count_completed = pie_df['completed'].value_counts().reset_index()
        count_completed.columns = ['Category', 'count']
        count_completed['Category_New'] =  [map_category[category] for category in count_completed['Category']]
        print(count_completed['Category_New'])

        

        fig = px.pie(count_completed, names='Category_New', values='count', title='Pie Chart Example')

        # Convert the Plotly figure to HTML
        pie_html = fig.to_html(full_html=False)

        return render_template('analytics.html', hist_html=hist_html, exp_act_html=exp_act_html, by_year_html=by_year_html, by_month_html=by_month_html, by_week_html = by_week_html, pie_html = pie_html, title='Analytics')
    return render_template('dashboard.html')


@app.route("/about_us")
def about_us():
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
        task = request.form.get('task')
        mongo.db.tasks.delete_many({'taskname':task})
        print("Task", task, "deleted!!")
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
        form = TaskForm(session.get('email'))
        if form.validate_on_submit():
            print("inside form")
            if request.method == 'POST':
                email = session.get('email')
                taskname = request.form.get('taskname')
                friendsemail = request.form.getlist('invitees')+["Please Select"]
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                start_time = request.form.get('start_time')
                end_time = request.form.get('end_time')
                description = request.form.get('description')
                print(friendsemail)
                check = mongo.db.tasks.find_one({'taskname': taskname})
                if not check:
                    mongo.db.tasks.insert_one({'email': email,
                                            'taskname': taskname,
                                            'category': category,
                                            'startdate': startdate,
                                            'starttime': start_time,
                                            'endtime': end_time,
                                            'description': description,
                                            'progress': 0,
                                            'actualhours': 0,
                                            'completed':False})
                    
                    for friendemail in friendsemail:
                        if friendemail!="Please Select":
                            mongo.db.tasks.insert_one({'email': friendemail,
                                                    'taskname': taskname,
                                                    'category': category,
                                                    'startdate': startdate,
                                                    'starttime': start_time,
                                                    'endtime': end_time,
                                                    'description': description,
                                                    'progress': 0,
                                                    'acutalhours': 0,
                                                    'completed':False})
                    flash(f' {form.taskname.data} Task Added!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash(
                        'Task name already taken. Please find another task name. Thank you!',
                        'danger')
                    return redirect(url_for('task'))
    else:
        return redirect(url_for('home'))
    return render_template('task.html', title='Task', form=form)

@app.route("/completeTask", methods = ['POST'])
def completeTask():
    if session.get('email'):
        email = session.get('email')
        task = request.form.get('task')
        is_completed = mongo.db.tasks.find_one({'taskname': task, 'email': email},{'completed'})
        print(is_completed)
        if is_completed['completed']:
            flash('Task already completed!', 'danger')
        else:
            actualhours = request.form.get('actualhours')
            print(actualhours)
            print("Actual hours taken", int(actualhours))
            mongo.db.tasks.update_one({'email':email, 'taskname':task}, {'$set': {'completed':True, 'actualhours':int(actualhours)}})
            tasks = mongo.db.tasks.find({'taskname': task}, {'completed'})
            total_tasks=0
            total_completed_tasks=0
            for tsk in tasks:
                if tsk['completed']:
                    total_completed_tasks+=1
                total_tasks+=1

            mongo.db.tasks.update_many({'taskname':task}, {'$set': {'progress':round(total_completed_tasks/total_tasks,2)*100}})

            flash(f' {task} Task Completed!', 'success')
    return redirect(url_for('home'))


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
