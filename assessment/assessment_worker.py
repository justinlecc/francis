from db import Human, Message

class AssessmentWorker():

	def __init__(self, db):
		self.db = db

	def run(self):

		print("-------!!!!!!!! AssessmentWorker ran and finished !!!!!!!!!---------")
		return 