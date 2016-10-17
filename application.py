import os, sys, logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from webserver.router import Router
from assessment.assessment_worker import AssessmentWorker

# Config log files
if os.environ['FRANCIS_ENV'] == 'LOCAL':
	logging.basicConfig(filename=os.environ['FRANCIS_LOGFILE'], level=logging.DEBUG)
else:
	logging.basicConfig(filename='/var/log/francisapp.log', level=logging.DEBUG)

# Initialize app
application = Flask(__name__)
app = application
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']
db = SQLAlchemy(app)

# Apply routes
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
