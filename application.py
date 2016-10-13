import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from message_receiver import MessageReceiver
from webserver.router import Router
from assessment.assessment_worker import AssessmentWorker
import twilio.twiml	
import pprint
import time

application = Flask(__name__)
app = application
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']
db = SQLAlchemy(app)

# Test to see if AWS will run the AssessmentWorker
# assessment_worker = AssessmentWorker(db)
# application = assessment_worker

if __name__ == "__main__":
	router = Router()
	router.applyRoutes(app)
	app.run()

# if __name__ == "__main__" and os.environ['FRANCIS_PROCESS_TYPE'] == 'WEBSERVER':
# 	router = Router()
# 	router.applyRoutes(app)
# 	app.run()
# elif __name__ == "__main__" and os.environ['FRANCIS_PROCESS_TYPE'] == 'ASSESSMENT_WORKER':
# 	print ("Here I would run the Assessment Worker")
# elif __name__ == "__main__":
# 	print ("ERROR: unrecognized PROCESS_TYPE with __name == '__main__'")
