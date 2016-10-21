from flask import Flask, request
import subprocess
from webserver.message_receiver import MessageReceiver
import twilio.twiml	
class Router():

	def __init__(app):
		pass

	def applyRoutes(self, app, db):

		# AVAILABILITY ENDPOINTS

		# Test the availability of Francis
		@app.route("/status", methods=['GET', 'POST'])
		def status ():
			return "Francis is available"

		# SMS ENDPOINTS

		# Endpoint for Twilio sms messages
		@app.route("/twilio/sms", methods=['POST'])
		def twilio_sms():
			message_receiver = MessageReceiver(db)
			from_phone_number = request.values.get("From")
			text = request.values.get("Body")
			message_receiver.sms(from_phone_number, text)
			return '/twilio/sms returned'
		# Endpoint for sms test messages
		@app.route("/simulator/sms", methods=['POST'])
		def simulator_sms():
			message_receiver = MessageReceiver(db)
			from_phone_number = request.values.get("From")
			text = request.values.get("Body")
			message_receiver.sms(from_phone_number, text)
			return '/simulator/sms returned'

		# ASSESSMENT WORKER ENDPOINTS
		# Start the assessment worker
		@app.route("/workers/assessment/start", methods=['GET', 'POST'])
		def assessment_start():
			err = subprocess.call(["python", "application.py", "assessment", "start"])
			if err:
				return "'assessment start' called and returned with error. Likely because assessment daemon is already started."
			else:
				return "'assessment start' called and succeeded."
		# Stop the assessment worker
		@app.route("/workers/assessment/stop", methods=['GET', 'POST'])
		def assessment_stop():
			err = subprocess.call(["python", "application.py", "assessment", "stop"])
			if err:
				return "'assessment stop' called and returned with error."
			else:
				return "'assessment stop' called and succeeded."

