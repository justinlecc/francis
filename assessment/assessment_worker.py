import sys, time
from db import Human, Message
from lib.daemon import Daemon
from message_receiver import MessageReceiver

class AssessmentWorker(Daemon):

    def setDb(self, db):
        self.db = db

    def run(self):
        message_receiver = MessageReceiver(self.db)
        from_phone_number = "975-3958"
        counter = 1
        while True:
            message_receiver.sms(from_phone_number, "Assessment message " + str(counter))
            counter += 1
            time.sleep(1)

