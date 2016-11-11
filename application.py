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
    print("APP LOGGING TO " + os.environ['FRANCIS_LOGFILE'])
else:
    # logging.basicConfig(filename=os.environ['FRANCIS_LOGFILE'], level=logging.DEBUG)
    # print("APP LOGGING TO " + os.environ['FRANCIS_LOGFILE'])
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    print("APP LOGGING TO stdout")

# Main entrypoint of Francis
class FrancisApp():

    def __init__(self, flask_app, db):
        self.flask_app = flask_app
        self.db = db

    def run(self, **kwargs):

        # Run the whole application
        if ('process_type' not in kwargs) or \
            kwargs['process_type'] is None:

            # Start the assessment process
            err = subprocess.call(["python", "application.py", "assessment", "start"])
            if err:
                logging.error("Failed to create a subprocess to run assessment worker")

            # Run this process as a webserver
            # Apply routes
            router = Router()
            router.apply_routes(self.flask_app)

            try:
                self.flask_app.run()

            except Exception as e:
                logging.error("Failed to run the webserver process (spot1)- " + str(e))


        # Run this process as a webserver
        if kwargs['process_type'] == 'webserver':

            # Apply routes
            router = Router()
            router.apply_routes(self.flask_app)

            try:
                self.flask_app.run()

            except Exception as e:
                logging.error("Failed to run the webserver process (spot2)- " + str(e))

        # Run this process as an assessment worker
        elif 'assessment' == kwargs['process_type']:

            try:
                assessment_worker = AssessmentWorker('/tmp/assessment-worker.pid')

                if 'param1' in kwargs:

                    if "start" == kwargs['param1']:
                        assessment_worker.start()
                    elif "restart" == kwargs['param1']:
                        assessment_worker.restart()
                    elif "stop" == kwargs['param1']:
                        assessment_worker.stop()
                    elif "foreground" == kwargs['param1']:
                        assessment_worker.run()
                    else:
                        logging.error("Unknown action for the assessment worker.")
                        return
                else:
                    logging.error("'param1' for the assessment process was not specified.")
                    return

            except Exception as e:
                logging.error("Failed to run the assessment process - " + str(e))

        # Run this process as a database management process (migration and upgrades)
        elif 'db' == kwargs['process_type']:

            try:
                self._db_manager()

            except Exception as e:
                logging.error("Failed to run the DB process - " + str(e))

            return

        else:
            logging.error("Unknown process type.")
            return

    def _db_manager(self):

        # Migration command setup
        migrate = Migrate(self.flask_app, self.db)
        manager = Manager(self.flask_app)
        manager.add_command('db', MigrateCommand)

        # NOTE: This works when called as python application.py db migrate/upgrade
        #   Its innerworking are somewhat magical to me at this point. Would be good
        #   to provide the manager params in a different way than through 'argv'.
        manager.run()


# Initialize Francis
application = FrancisApp(FrancisFlask(), FrancisDb())

# Run Francis
if (__name__ == "__main__"):

    process_type = None
    param1 = None

    # Parse the command
    if len(sys.argv) >= 2:
        process_type = sys.argv[1]

    if len(sys.argv) >= 3:
        param1 = sys.argv[2]

    # Note: process_type=None will run the webserver process
    application.run(process_type=process_type, param1=param1)

