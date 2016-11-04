import os, datetime
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
# Represents a human user of Francis. Currently assumes
# each human only has one phone number.
#     id: primary key
#     phone_number: human's phone number
class Human(db.Model):

    __tablename__ = 'humans'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, index=True)
    nickname = db.Column(db.String(20))

    def __repr__(self):
        return '<Human %r>' % self.phone_number

class IncomingSms(db.Model):

    __tablename__ = 'incoming_sms'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    human_id = db.Column(db.Integer, db.ForeignKey(Human.id))
    human = db.relationship(Human, backref="incoming_sms")
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

class OutgoingSms(db.Model):

    __tablename__ = 'outgoing_sms'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    human_id = db.Column(db.Integer, db.ForeignKey(Human.id))
    human = db.relationship(Human, backref="outgoing_sms")
    sent = db.Column(db.Boolean, default=False)
    send_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# RUN MANAGER (MIGRATIONS)
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
if __name__ == "__main__":
    manager.run()
