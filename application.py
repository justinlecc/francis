import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from db import Human, Message
import twilio.twiml	
import pprint
import time

application = Flask(__name__)
app = application
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']
db = SQLAlchemy(app)

@app.route("/sms", methods=['POST']) # endpoint for Twilio sms messages
def incoming_sms():

	# TODO: find/create a logging system
	# Log incoming message
	# with open('sms_posts.log', 'a') as f:
	# 	f.write("\n\n===================================\n\n")
	# 	f.write(time.strftime("%c\n"))
	# 	pprint.pprint(vars(request.values), stream=f)
	# 	f.write("\n\n===================================\n\n")
	output_html = 'hello world'

	# Values in the sms
	sms_from_phone_number = request.values.get("From")
	sms_text = request.values.get("Body")

	# Get the human from the DB
	from_human = db.session.query(Human).filter_by(phone_number=sms_from_phone_number).first()
	
	# Create the human if it does not exist
	if from_human is None:
		from_human = Human(sms_from_phone_number)
		db.session.add(from_human)
		db.session.commit()

	# Insert the sms into the db
	message = Message(sms_text, from_human.id)
	db.session.add(message)
	db.session.commit()

	return output_html

if __name__ == "__main__":
    app.run()