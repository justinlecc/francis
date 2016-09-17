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

class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.username

if __name__ == "__main__":
	manager.run()
