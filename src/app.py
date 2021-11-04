"""Importing all the standard Python modules."""
import csv
import json
import os
import random
import string

import pymongo
import datetime
import bcrypt

from pymongo import MongoClient

from flask import Flask
from flask import render_template, url_for
from flask import request, redirect
from flask import flash, session

#MongoDB connection using cluster's connection string
client = pymongo.MongoClient("mongodb+srv://radhika:Radhika1997@simplii.tvhh1.mongodb.net/simplii?retryWrites=true&w=majority")

#database to which connections are to be made
db = client.simplii
testUserInfo = db.testUserInfo


app = Flask(__name__, static_folder='static')
app.secret_key = "simpliitesting"
package_dir = os.path.dirname(os.path.abspath(__file__))
"""Global constant to store directory path""" 
TODO_TASKS_PATH = os.path.join(package_dir, "../static", "tasks", "todo")
COMPLETED_TASKS_PATH = os.path.join(package_dir, "../static", "tasks", "completed")

"""List declaration for storing the quotes and authors """
ALL_QUOTES = []
ALL_AUTHORS = []

"""Loading our code dataset in memory"""

with open(os.path.join(package_dir, "../static", "quotes.csv"), "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        ALL_QUOTES.append(row["Quote"])
        ALL_AUTHORS.append(row["Author"])


def refresh_data():
    """This function loads all the data required to display the home page from file-system."""

    ##### Load user information from file
    with open(os.path.join(package_dir,"../static","user_information.json"), "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    initialized = json_data["initialized"]
    name = json_data["name"]
    email_id = json_data["email_id"]
    email_notifications = json_data["email_notifications"]

    ##### Load a random quote
    index = random.randint(0, len(ALL_AUTHORS)-1)

    ##### Load the todo task list
    tasks = {}
    for file in os.listdir(TODO_TASKS_PATH):
        if ".json" in file:
            with open(os.path.join(TODO_TASKS_PATH, file), "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)

            tasks[json_data["id"]] = json_data

    ##### Sorting the tasks
    tasks = {key:value for (key,value) in sorted(tasks.items(), key = lambda item: item[1]["deadline"])}
    #####

  ##### Compile the data and send as json!
    data = {
      "name_block" : {"initialized":initialized, "name": name, "email_id": email_id,
      "email_notifications": email_notifications},
      "quote_block" : {"quote": ALL_QUOTES[index], "author": ALL_AUTHORS[index]},
      "task-list-block" : {"task-list": tasks}
    }
  #####
    return data

def getnewTaskID():
    """Gets a task to be shown to the user."""
    todo_ids = [f[0:6] for f in os.listdir(TODO_TASKS_PATH)]
    completed_ids = [f[0:6] for f in os.listdir(COMPLETED_TASKS_PATH)]
    while True:
        possible_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))

        if possible_id not in todo_ids and possible_id not in completed_ids:
            return possible_id



@app.route("/", methods=['GET'])
def homePage():
    """This function renders the landing page."""
    return render_template("base.html")

@app.route("/login", methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login_post():
    error = None
    if request.method == 'POST':
        user_id = request.form.get("userid")
        #print(user_id)
        email = request.form.get("email")
        user_password = request.form.get("password")
        #print(user_password)

        db_user = testUserInfo.find_one({"user_id": user_id})
        #print(db_user)

        if(db_user==None):
            flash('The entered user ID does not exist, please login with valid credentials or sign up.')
            return redirect(url_for('login_post'))
        else:
            db_userid = db_user['user_id']
            #print(db_userid)
            db_password = db_user['password']
            valid_password = bcrypt.checkpw(user_password.encode(), db_password)
            #print(valid_password)

            if user_id == db_userid and valid_password != True:
                flash('The entered password is invalid, please login with valid credentials.')
                return redirect(url_for('login_post'))

            else:
                session['user_id'] = user_id
                session['email'] = email
            
                return redirect(url_for('mainPage'))
        return render_template('index.html')


'''


@app.route("/signup", methods=['GET','POST'])
def signup():
    error = None
    if request.method == 'POST':
        name = request.form["name"]
        username = request.form["email"]
        password = request.form["password"]
        # Check if username exists in database
        #query = "SELECT username FROM users WHERE username = :username"
        #if db.execute(query, {'username': reg_username}).first():
        #    flash('Username already exists')
        #    return render_template('register.html')
        #else:
        #new_user = User(name, username, password)
        #db.session.add(new_user)
        #db.session.commit()
        #session['username'] = reg_username
        return redirect(url_for('login'))
    return render_template('signup.html')
'''

@app.route("/signup", methods=['GET'])
def signup_get():
    return render_template('signup.html')

@app.route("/signup", methods=['POST'])
def signup_post():
    message = ''

    '''
    if "email" in session:
        return redirect(url_for("logged_in"))
        
    '''

    if request.method == 'POST':
        user_id = request.form.get("userid")
        user_first_name = request.form.get("firstname")
        user_last_name = request.form.get("lastname")
        email = request.form.get("email")
        user_password = request.form.get("password")

        user_found = testUserInfo.find_one({"user_id": user_id})
        email_found = testUserInfo.find_one({"email_id": email})


        if user_found:
            flash('User ID already taken, please enter a different user ID')
            #message = 'User ID already taken, please enter a different user ID'

            return redirect(url_for('signup_post'))

            #return render_template('signup.html', message=message)


        if email_found:
            message = 'This email already exists in database'
            return render_template('signup.html', message=message)

        else:
            pw_hashAndSalt = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())

            user_input_data = {'user_id': user_id, 'first_name': user_first_name, 'last_name': user_last_name, 'email_id': email, 'password': pw_hashAndSalt}
            #user_input_data = {'first_name': user_name, 'email_id': email, 'password': pw_hashAndSalt}

            testUserInfo.insert_one(user_input_data)

            user_data = testUserInfo.find_one({"email_id": email})
            new_email = user_data['email_id']

            return redirect(url_for('mainPage'))
    return render_template('index.html')

@app.route("/index")
def mainPage():
    """This function renders the home page."""
    #email = session["email"]
    return render_template("index.html", name = session["name"], e = session["email"], data=refresh_data())

@app.route('/logout')
def logout():
    """This function ends the session and logs the user out."""
    #session.pop('user', None)
    return redirect('/')

@app.route("/update_user_info", methods = ["POST"])
def update_user_information():
    """Updates user information into JSON."""
    user_information = request.form
    new_info = {}

    new_info["name"] = user_information["name"]
    new_info["email_id"] = user_information["email"]
    new_info["initialized"] = "yes"
    new_info["email_notifications"] = user_information["emailChoose"]

    with open(os.path.join(package_dir,"../static", "user_information.json"), "w", encoding="utf-8") as json_file:
        json.dump(new_info, json_file)

    return redirect("/index")



@app.route("/add_task", methods = ["POST"])
def add_new_task():
    """Add a new task to the JSON."""
    form_data = request.values

    new_id = getnewTaskID()

    new_task_information = {}

    new_task_information["id"] = new_id
    new_task_information["task_name"] = form_data["taskName"]
    new_task_information["deadline"] = form_data["deadline"].replace("T"," ")
    new_task_information["estimate"] = form_data["estimateInput"]

    new_task_information["task_type"] = form_data["taskType"]

    if new_task_information["task_type"] == "intellectual":
        new_task_information["quant_verbal"] = form_data["quant/verbal"]
        new_task_information["creat_consum"] = form_data["contentconsump"]

    elif new_task_information["task_type"] == "physical":
        new_task_information["quant_verbal"] = "NA"
        new_task_information["creat_consum"] = "NA"

    else:
        print("Error! task_type is neither intellectual nor physical")


    new_task_information["difficulty"] = form_data["difficulty"]

    print(new_task_information)
    with open(os.path.join(TODO_TASKS_PATH, new_id+".json"), "w", encoding="utf-8") as json_file:
        json.dump(new_task_information, json_file)

    return redirect("/index")

@app.route("/delete_task", methods = ["POST"])
def delete_task_byID():
    """Deleting a task by its ID."""
  # task_id = request.data.decode("utf-8")

    print(request.values)
    task_id = request.values["id"]

    if os.path.exists(os.path.join(TODO_TASKS_PATH, str(task_id)+".json")):
        with open(os.path.join(TODO_TASKS_PATH, str(task_id)+".json"),
        "r", encoding="utf-8") as json_file:
            task_information = json.load(json_file)


        os.remove(os.path.join(TODO_TASKS_PATH, str(task_id)+".json"))

        with open(os.path.join(COMPLETED_TASKS_PATH, str(task_id)+".json"),
        "w", encoding="utf-8") as json_file:
            json.dump(task_information, json_file)

    return redirect("/index")

if __name__ == "__main__":
    app.run(debug=True)
