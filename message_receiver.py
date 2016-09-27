from db import Human, Message

class MessageReceiver():

	def __init__(self, db):
		self.db = db

	def sms(self, from_phone_number, text):

		# Get the human from the DB
		from_human = self.db.session.query(Human).filter_by(phone_number=from_phone_number).first()
		
		# Create the human if it does not exist
		if from_human is None:
			from_human = Human(from_phone_number)
			self.db.session.add(from_human)
			self.db.session.commit()

		# Insert the sms into the db
		message = Message(text, from_human.id) # TODO: make 'text' db safe?
		self.db.session.add(message)
		self.db.session.commit()
		return 