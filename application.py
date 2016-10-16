import os, sys
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

# apply routes
router = Router()
router.applyRoutes(app, db)

if __name__ == "__main__":

	# Initialization is a worker?
	if len(sys.argv) >= 2:

		if "assessment" == sys.argv[1]:
			if len(sys.argv) == 3:
				assessmentWorker = AssessmentWorker('/tmp/assessment-worker.pid')
				assessmentWorker.setDb(db)
				if "start" == sys.argv[2]:
					assessmentWorker.start()
				elif "restart" == sys.argv[2]:
					assessmentWorker.restart()
				elif "stop" == sys.argv[2]:
					assessmentWorker.stop()
				elif "foreground" == sys.argv[2]:
					assessmentWorker.run()
				else:
					print("ERROR: Unknown argument for the assessment worker")
			else:
				print("ERROR: Incorrect number of parameters for the assessment worker")
		else:
			print("ERROR: Unknown process type in application.py")
	
	# Initialization is a webserver
	# Note: Application will not be started here on Elastic Beanstalk.
	#		Instead, EB will import the 'application' object and call
	#       the 'run' method on it. Having app.run() here is for running
	#       the application locally (or other non-EB environments).
	else:
		app.run()
 

# if __name__ == "__main__" and os.environ['FRANCIS_PROCESS_TYPE'] == 'WEBSERVER':
# 	router = Router()
# 	router.applyRoutes(app)
# 	app.run()
# elif __name__ == "__main__" and os.environ['FRANCIS_PROCESS_TYPE'] == 'ASSESSMENT_WORKER':
# 	print ("Here I would run the Assessment Worker")
# elif __name__ == "__main__":
# 	print ("ERROR: unrecognized PROCESS_TYPE with __name == '__main__'")
