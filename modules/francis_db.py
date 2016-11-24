import os, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from modules.francis_flask import FrancisFlask

# Sqalchemy singleton database
class FrancisDb():

    # Singleton instance.
    __instance = None

    # Instantiation creates/returns the singleton instance.
    def __new__(cls):

        if FrancisDb.__instance is None:

            FrancisDb.__instance = SQLAlchemy(FrancisFlask())

        return FrancisDb.__instance

# Database instance for setup
db = FrancisDb()

# Migration command setup
migrate = Migrate(FrancisFlask(), db)
manager = Manager(FrancisFlask())
manager.add_command('db', MigrateCommand)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#
# SCHEMA ORMs
#
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

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
