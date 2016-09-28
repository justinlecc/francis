import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from message_receiver import MessageReceiver

application = Flask(__name__)
app = application
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']
db = SQLAlchemy(app)

message_receiver = MessageReceiver(db)
from_phone_number = '666'
text = "This is a test to see if the assessment daemon is running"
message_receiver.sms(from_phone_number, text)