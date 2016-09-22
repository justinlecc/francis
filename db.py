import os

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

# Human
# Each row represents a human user of Francis. Currently assumes
# each human only has one phone number.
# 	id: primary key
# 	phone_number: human's phone number
class Human(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	phone_number = db.Column(db.String(20), unique=True, index=True)
	nickname = db.Column(db.String(20))
	messages = db.relationship('Message', backref='Human', lazy='dynamic')

	def __init__(self, phone_number):
		self.phone_number = phone_number

	def __repr__(self):
		return '<Human %r>' % self.phone_number

# Message
# Each row represents a message sent from a Human to Francis.
# 	id: primary key
#	text: body of the message
# 	human: foreign key to human who sent the text
class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text)
	human_id = db.Column(db.Integer, db.ForeignKey('human.id'))

	def __init__(self, text, human_id):
		self.text = text
		self.human_id = human_id

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# RUN MANAGER (MIGRATIONS)
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
if __name__ == "__main__":
	manager.run()
