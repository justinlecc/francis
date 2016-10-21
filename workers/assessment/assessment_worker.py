import time, logging
from lib.daemon import Daemon

class AssessmentWorker(Daemon):

    def setDb(self, db):
        self.db = db

    def run(self):
        counter = 1
        while True:
            logging.debug("Assessment iteration " + str(counter))
            counter += 1
            time.sleep(1)

