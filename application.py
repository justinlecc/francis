import os, sys, logging, subprocess
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from modules.francis_flask import FrancisFlask
from modules.francis_db import FrancisDb
from modules.router import Router
from modules.assessment_worker import AssessmentWorker

# Config log files
# Logging levels
#   1. debug    - detailed info
#   2. info     - confirmation that things are working
#   3. warning  - something unexpected happened
#   4. error    - a function failed
#   5. critical - the application failed
if os.environ['FRANCIS_ENV'] == 'LOCAL':
    logging.basicConfig(filename=os.environ['FRANCIS_LOGFILE'], level=logging.DEBUG)
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # print("APP LOGGING TO " + os.environ['FRANCIS_LOGFILE'])
else:
    logging.basicConfig(filename='/var/log/cloud-init.log', level=logging.DEBUG)
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Initialize Flask here for AWS Elastic Beanstalk
application = FrancisFlask()

# Apply routes to Flask
router = Router()
router.apply_routes(application)

# Run Francis
if (__name__ == "__main__"):

    process_type = None
    param1 = None

    if len(sys.argv) == 1:
        application.run()

    # Parse the command
    if len(sys.argv) >= 2:
        process_type = sys.argv[1]

    if len(sys.argv) >= 3:
        param1 = sys.argv[2]

    # Run this process as an assessment worker
    if 'assessment' == process_type:

        try:
            assessment_worker = AssessmentWorker('/tmp/assessment-worker.pid')

            if 'param1' is not None:

                if "start" == param1:
                    assessment_worker.start()
                    exit()
                elif "restart" == param1:
                    assessment_worker.restart()
                    exit()
                elif "stop" == param1:
                    assessment_worker.stop()
                    exit()
                elif "foreground" == param1:
                    assessment_worker.run()
                    exit()
                else:
                    logging.error("Unknown action for the assessment worker.")
                    exit()
            else:
                logging.error("'param1' for the assessment process was not specified.")
                exit()

        except Exception as e:
            logging.error("Failed to run the assessment process - " + str(e))

    # Run this process as a database management process (migration and upgrades)
    elif 'db' == process_type:

        try:
            # Migration command setup
            migrate = Migrate(application, FrancisDb())
            manager = Manager(application)
            manager.add_command('db', MigrateCommand)

            # NOTE: This works when called as python application.py db migrate/upgrade
            #   Its innerworking are somewhat magical to me at this point. Would be good
            #   to provide the manager params in a different way than through 'argv'.
            manager.run()

        except Exception as e:
            logging.error("Failed to run the DB process - " + str(e))

        exit()



