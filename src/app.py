"""Importing all the standard Python modules."""
import os
import random
import csv
import json
import string

from flask import Flask
from flask import render_template
from flask import request, redirect


app = Flask(__name__)
print(os.path)
"""Global constant to store directory path""" 
TODO_TASKS_PATH = os.path.join("../static", "tasks", "todo")
COMPLETED_TASKS_PATH = os.path.join("../static", "tasks", "completed")

"""List declaration for storing the quotes and authors """
ALL_QUOTES = []
ALL_AUTHORS = []

"""Loading our code dataset in memory""" 
with open(os.path.join("src","quotes.csv"), "r", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        ALL_QUOTES.append(row["Quote"])
        ALL_AUTHORS.append(row["Author"])


def refresh_data():
    """This function loads all the data required to display the home page from file-system."""

    ##### Load user information from file
    with open(os.path.join("../static", "user_information.json"), "r", encoding="utf-8") as json_file:
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



@app.route("/")
def homePage():
    """This function renders the home page."""
    return render_template("index.html", data=refresh_data())


@app.route("/update_user_info", methods = ["POST"])
def update_user_information():
    """Updates user information into JSON."""
    user_information = request.form
    new_info = {}

    new_info["name"] = user_information["name"]
    new_info["email_id"] = user_information["email"]
    new_info["initialized"] = "yes"
    new_info["email_notifications"] = user_information["emailChoose"]

    with open(os.path.join("../static", "user_information.json"), "w", encoding="utf-8") as json_file:
        json.dump(new_info, json_file)

    return redirect("/")



@app.route("/add_task", methods = ["POST"])
def add_new_task():
    """Add a new task to the JSON."""
    form_data = request.values

    new_id = getnewTaskID()

    new_task_information = {}

    new_task_information["id"] = new_id
    new_task_information["task_name"] = form_data["taskName"]
    new_task_information["deadline"] = form_data["deadline"]
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

    return redirect("/")

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

    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
