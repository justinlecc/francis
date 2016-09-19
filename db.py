import os

# from http://flask.pocoo.org/ tutorial
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# App instance
application = Flask(__name__)
app = application

# DB setup
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://francisdb:nicebot99@francis-staging.c6yeo5k4ngoz.us-west-2.rds.amazonaws.com:6666/francisdb'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']

# Config can be done using:
# app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

# Migration command setup
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# SCHEMA
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# User
# Each row represents a user of Francis. Currently assumes
# each user only has one phone number.
# 	id: primary key
# 	phone_number: user's phone number
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	phone_number = db.Column(db.String(20), unique=True, index=True)

	# def __init__(self, id, phone_number):
	# 	self.id = id
	# 	self.phone_number = phone_number

	def __repr__(self):
		return '<User %r>' % self.phone_number



# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# RUN MANAGER (MIGRATIONS)
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
if __name__ == "__main__":
	manager.run()
