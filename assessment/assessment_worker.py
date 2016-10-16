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

	# def __init__(self, db):
	# 	self.db = db

	# def run(self):
 #        while True:
 #            time.sleep(1)


 
# if __name__ == "__main__":
#     daemon = MyDaemon('/tmp/daemon-example.pid')
#     if len(sys.argv) == 2:
#         if 'start' == sys.argv[1]:
#             daemon.start()
#         elif 'stop' == sys.argv[1]:
#             daemon.stop()
#         elif 'restart' == sys.argv[1]:
#             daemon.restart()
#         else:
#             print("Unknown command")
#             sys.exit(2)
#         sys.exit(0)
#     else:
#         print("usage: %s start|stop|restart" % sys.argv[0])
#         sys.exit(2)

