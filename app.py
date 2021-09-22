from flask import Flask
from flask import render_template

import os, sys
import random
import csv

app = Flask(__name__)


@app.route("/")
def homePage():

  all_quotes = []
  all_authors = []


  with open(os.path.join("static", "quotes.csv")) as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
      all_quotes.append(row["quote"])
      all_authors.append(row["author"])


  index = random.randint(0, len(all_authors)-1)


  return render_template("index.html", quote= all_quotes[index], author = all_authors[index])
  
  
app.run(debug = True)
