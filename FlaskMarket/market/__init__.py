# import the library the simple flask application
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# creating the flask app
app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '635304b7412500e3a59214eb'
db = SQLAlchemy(app=app)

from market import route