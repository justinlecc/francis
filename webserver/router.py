class Router():

	def __init__(app):
		pass

	def applyRoutes(self, app):
		# Test the availability of Francis
		@app.route("/status", methods=['GET', 'POST'])
		def status ():
			return "Francis is available"
		# Endpoint for Twilio sms messages
		@app.route("/twilio/sms", methods=['POST']) # endpoint for Twilio sms messages
		def twilio_sms():
			message_receiver = MessageReceiver(db)
			from_phone_number = request.values.get("From")
			text = request.values.get("Body")
			message_receiver.sms(from_phone_number, text)
			return '/twilio/sms returned'
		# Endopoint for sms test messages
		@app.route("/simulator/sms", methods=['POST'])
		def simulator_sms():
			message_receiver = MessageReceiver(db)
			from_phone_number = request.values.get("From")
			text = request.values.get("Body")
			message_receiver.sms(from_phone_number, text)
			return '/simulator/sms returned'