from flask import Flask
from flask import render_template
from flask import request


import os, sys
import random
import csv
import json

app = Flask(__name__)


TODO_TASKS_PATH = os.path.join("static", "tasks", "todo")
COMPLETED_TASKS_PATH = os.path.join("static", "tasks", "completed")

ALL_QUOTES = []
ALL_AUTHORS = []
with open(os.path.join("static", "quotes.csv"), "r", encoding="utf-8") as csv_file:
  reader = csv.DictReader(csv_file)

  for row in reader:
    ALL_QUOTES.append(row["Quote"])
    ALL_AUTHORS.append(row["Author"])



def refresh_data():

  ##### Load user information from file
  with open(os.path.join("static", "user_information.json"), "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

  initialized = json_data["initialized"]
  name = json_data["name"]
  email_id = json_data["email_id"]
  email_notifications = json_data["email_notifications"]
  #####

  ##### Load a random quote
  index = random.randint(0, len(ALL_AUTHORS)-1)
  #####

  # ##### Load the todo task list
  # tasks = {}
  # for file in os.listdir(TODO_TASKS_PATH):
  #   if ".json" in file:
  #     with open(os.path.join(TODO_TASKS_PATH, file), "r", encoding="utf-8") as json_file:
  #       json_data = json.load(json_file)

  #     tasks[json_data["task_id"]] = json_data
  #####

  ##DUMMY JSON
  tasks = {
   "task2": {"taskName": "Interactive narrative home work", "endDate": "2021-09-29", "approximateTime": 5, "difficulty": 2, "status": 0},
   "task1": {"taskName": "Algos home work", "endDate": "2021-09-30", "approximateTime": 6, "difficulty": 1, "status": 0}
  }


  ##### Compile the data and send as json!
  data = {
    "name_block" : {"initialized":initialized, "name": name, "email_id": email_id,
    "email_notifications": email_notifications},
    "quote_block" : {"quote": ALL_QUOTES[index], "author": ALL_AUTHORS[index]},
    "task-list-block" : {"task-list": tasks}
  }
  #####
  return data


def delete_tasks():
  for file in os.listdir(COMPLETED_TASKS_PATH):
    if ".json" in file:
      os.remove(os.path.join(COMPLETED_TASKS_PATH, file))

  for file in os.listdir(TODO_TASKS_PATH):
    if ".json" in file:
      os.remove(os.path.join(TODO_TASKS_PATH, file))



def delete_user_information():
  empty_user_information = {
    "initialized" : "no",
    "name" : "",
    "email_id" : "",
    "email_notifications" : "no"
  }

  with open(os.path.join("static", "user_information.json"), "w", encoding="utf-8") as json_file:
    json.dump(empty_user_information, json_file)

def getnewTaskID():
  todo_ids = [f[0:6] for f in os.listdir(TODO_TASKS_PATH)]
  completed_ids = [f[0:6] for f in os.listdir(COMPLETED_TASKS_PATH)]
  
  while True:
    possible_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))

    if possible_id not in todo_ids and possible_id not in completed_ids:
      return possible_id



@app.route("/")
def homePage():
  return render_template("index.html", data=refresh_data())
  
  
@app.route("/update_user_info", methods = ["POST"])
def update_user_information():
  
  user_information = json.loads(request.data)
  
  with open(os.path.join("static", "user_information.json"), "w", encoding="utf-8") as json_file:
    json.dump(user_information, json_file)

  return render_template("index.html", data=refresh_data())



@app.route("/reset_all", methods = ["POST"])
def delete_user():
  delete_tasks()
  delete_user_information()

  return render_template("index.html", data=refresh_data())


@app.route("/reset_tasks", methods = ["POST"])
def delete_tasks_only():
  delete_tasks()

  return render_template("index.html", data=refresh_data())





@app.route("/add_task", methods = ["POST"])
def add_new_task():
  new_task_information = json.loads(request.data)

  new_id = getnewTaskID()

  new_task_information["id"] = new_id

  with open(os.path.join(TODO_TASKS_PATH, new_id+".json"), "w", encoding="utf-8") as json_file:
    json.dump(new_task_information, json_file)

  return render_template("index.html", data=refresh_data())

@app.route("/edit_task", methods = ["POST"])
def edit_task_byID():
  pass

app.run(debug = True)


