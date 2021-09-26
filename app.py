from flask import Flask
from flask import render_template
from flask import request


import os, sys
import random
import csv
import json

app = Flask(__name__)



ALL_QUOTES = []
ALL_AUTHORS = []
with open(os.path.join("static", "quotes_dataset.csv"), "r", encoding="utf-8") as csv_file:
  reader = csv.DictReader(csv_file)

  for row in reader:
    ALL_QUOTES.append(row["quote"])
    ALL_AUTHORS.append(row["author"])



def refresh_data():


  with open(os.path.join("static", "user_information.json"), "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)

  initialized = json_data["initialized"]
  name = json_data["name"]
  email_id = json_data["email_id"]
  email_notifications = json_data["email_notifications"]
  

  index = random.randint(0, len(ALL_AUTHORS)-1)

  data = {
    "name_block" : {"initialized":initialized, "name": name, "email_id": email_id,
     "email_notifications": email_notifications},
    "quote_block" : {"quote": ALL_QUOTES[index], "author": ALL_AUTHORS[index]}
  }

  return data


def delete_tasks():
  for file in os.path.join("static", "tasks", "completed_tasks"):
    os.remove(os.path.join("static", "tasks", "completed_tasks", file))

  for file in os.path.join("static", "tasks", "todo"):
    os.remove(os.path.join("static", "tasks", "todo", file))



def delete_user_information():
  empty_user_information = {
    "initialized" : "no",
    "name" : "",
    "email_id" : "",
    "email_notifications" : "no"
  }

  with open(os.path.join("static", "user_information.json"), "w", encoding="utf-8") as json_file:
    json.dump(empty_user_information, json_file)



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


app.run(debug = True)


