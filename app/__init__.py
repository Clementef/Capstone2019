from flask import Flask
from mongoengine import connect
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(20)
connect("capstone2019", host='mongodb://admin:1superadmin@ds012889.mlab.com:12889/capstone2019')

from .routes import *
