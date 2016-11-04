import logging
from db.db import Human, IncomingSms, OutgoingSms, db

class SmsReceiver():

    def __init__(self):
        pass

    def sms(self, from_phone_number, text):
        
        try:

            # Get the human from the DB
            from_human = db.session.query(Human).filter_by(phone_number=from_phone_number).first()

            # Create the human if it does not exist
            if from_human is None:
                from_human = Human(phone_number=from_phone_number)
                db.session.add(from_human)
                # db.session.commit()

            # Insert the sms into the db
            incoming_sms = IncomingSms(text=text, human=from_human) # TODO: make 'text' db safe?
            db.session.add(incoming_sms)
            db.session.commit()

        except Exception as e:
            logging.error("Failed to receive sms - " + str(e))
            db.session.rollback()

        return

class SmsSender():

    def __init__(self):
        pass

    # Schedule a message to be sent
    def sms(self, human, text, senddatetime):
        if senddatetime.tzinfo != None:
            logging.error("senddatetime parameter in SmsSender::sms had timezone information (which it cannot)")
            return

        try:
            outgoing_sms = OutgoingSms(text=text, human=human, send_at=senddatetime)
            db.session.add(outgoing_sms)
            db.session.commit()
            logging.debug("Added outgoing_sms - " + text)

        except Exception as e:
            logging.error("Failed to send sms - " + str(e))
            db.session.rollback()

        return
