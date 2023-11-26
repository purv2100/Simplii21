#
# Copyright 2023 Simplii from Group74 NCSU CSC510
#
# Licensed under the MIT/X11 License (http://opensource.org/licenses/MIT)
#

from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail


class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'secret'
        self.app.config['MONGO_URI'] = 'mongodb://localhost:27017/simplii'
        self.mongo = PyMongo(self.app)

