import os, sys, logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from modules.router import Router
from modules.assessment_worker import AssessmentWorker

# Config log files
# Logging levels
# 	1. debug    - detailed info
#   2. info     - confirmation that things are working
#   3. warning  - something unexpected happened
# 	4. error    - a function failed
#   5. critical - the application failed
if os.environ['FRANCIS_ENV'] == 'LOCAL':
	logging.basicConfig(filename=os.environ['FRANCIS_LOGFILE'], level=logging.DEBUG)
	print("APP LOGGING TO " + os.environ['FRANCIS_LOGFILE'])
else:
	# logging.basicConfig(filename=os.environ['FRANCIS_LOGFILE'], level=logging.DEBUG)
	# print("APP LOGGING TO " + os.environ['FRANCIS_LOGFILE'])
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
	print("APP LOGGING TO stdout")

# Initialize app
application = Flask(__name__)
app = application
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FRANCIS_DB_URI']
db = SQLAlchemy(app)

# Apply routes
router = Router()
router.apply_routes(app)

if __name__ == "__main__":

	# Run a worker
	if len(sys.argv) >= 2:

		if "assessment" == sys.argv[1]:
			if len(sys.argv) == 3:
				assessment_worker = AssessmentWorker('/tmp/assessment-worker.pid')
				# assessment_worker.set_db(db)
				if "start" == sys.argv[2]:
					assessment_worker.start()
				elif "restart" == sys.argv[2]:
					assessment_worker.restart()
				elif "stop" == sys.argv[2]:
					assessment_worker.stop()
				elif "foreground" == sys.argv[2]:
					assessment_worker.run()
				else:
					print("ERROR: Unknown argument for the assessment worker")
			else:
				print("ERROR: Incorrect number of parameters for the assessment worker")
		else:
			print("ERROR: Unknown process type in application.py")
	
	# Run the webserver
	# Note: Application will not be started here on Elastic Beanstalk.
	#		Instead, EB will import the 'application' object and call
	#       the 'run' method on it. Having app.run() here is for running
	#       the application locally (or other non-EB environments).
	else:
		app.run()
