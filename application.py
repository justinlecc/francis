import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from message_receiver import MessageReceiver
import twilio.twiml	
import pprint
import time

application = Flask(__name__)
app = application
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']
db = SQLAlchemy(app)

# Test the availability of Francis
@app.route("/status", methods=['GET', 'POST'])
def status ():
	return "Francis is available"

@app.route("/assessment", methods=['POST'])
def assessment ():
	message_receiver = MessageReceiver(db)
	from_phone_number = '666'
	text = "This is a test to see if the assessment daemon is running. I'm inside the /assessment route"
	message_receiver.sms(from_phone_number, text)
	return "/tasks/assessment returned"

# Endpoint for Twilio sms messages
@app.route("/twilio/sms", methods=['POST']) # endpoint for Twilio sms messages
def twilio_sms():

	message_receiver = MessageReceiver(db)
	from_phone_number = request.values.get("From")
	text = request.values.get("Body")
	message_receiver.sms(from_phone_number, text)

	return '/twilio/sms returned'

@app.route("/simulator/sms", methods=['POST'])
def simulator_sms():
	message_receiver = MessageReceiver(db)
	from_phone_number = request.values.get("From")
	text = request.values.get("Body")
	message_receiver.sms(from_phone_number, text)

	return '/simulator/sms returned'

	# TODO: find/create a logging system
	# Log incoming message
	# with open('sms_posts.log', 'a') as f:
	# 	f.write("\n\n===================================\n\n")
	# 	f.write(time.strftime("%c\n"))
	# 	pprint.pprint(vars(request.values), stream=f)
	# 	f.write("\n\n===================================\n\n")

	# # Get the human from the DB
	# from_human = db.session.query(Human).filter_by(phone_number=sms_from_phone_number).first()
	
	# # Create the human if it does not exist
	# if from_human is None:
	# 	from_human = Human(sms_from_phone_number)
	# 	db.session.add(from_human)
	# 	db.session.commit()

	# # Insert the sms into the db
	# message = Message(sms_text, from_human.id)
	# db.session.add(message)
	# db.session.commit()

	# return output_html

if __name__ == "__main__":
    app.run()