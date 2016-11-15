import time, logging, sys, datetime, os
from twilio.rest import TwilioRestClient
from lib.daemon import Daemon
from modules.francis_db import Human, IncomingSms, OutgoingSms, FrancisDb
from modules.talent import TalentNetwork
from modules.state import SmsState

INTERVAL_SECONDS = 3

class AssessmentWorker(Daemon):

    # Send the unsent messages in the outgoing sms_table.
    #   Sending sms docs: https://www.twilio.com/docs/api/rest/sending-messages.
    #   TODO: Add 'StatusCallback' url to messages in order to update the outgoing_sms table.
    def _send_sms(self):
        db = FrancisDb()
        outgoing_sms = db.session.query(OutgoingSms)\
            .filter(OutgoingSms.sent == False)\
            .filter(OutgoingSms.send_at <= datetime.datetime.utcnow()).all()

        logging.debug(outgoing_sms)

        client = TwilioRestClient(
            os.environ['FRANCIS_TWILIO_ACCOUNT_SID'], 
            os.environ['FRANCIS_TWILIO_AUTH_TOKEN']
        )
        
        for sms in outgoing_sms:

            # Verify the phone number is well-formed
            if (len(sms.human.phone_number) == 12 and sms.human.phone_number[0] == '+'):

                # In development, only send messages to myself
                if (sms.human.phone_number == os.environ['FRANCIS_DEVELOPER_PHONE_NUMBER']):

                    # Send the message
                    m = client.messages.create(
                        to=sms.human.phone_number,
                        from_=os.environ['FRANCIS_PHONE_NUMBER'], 
                        body=sms.text,
                        max_price="0.01"
                    )

                    logging.info("Sms send to " + sms.human.phone_number + " with the message: " + sms.text)

                    # TODO: There may be a quicker way to send messages when you don't care about a
                    #   synchronous status reply. Message statuses can also be sent asynch.
                    if m.status == "queued":

                        logging.debug("Sending sms via Twilio succeeded")

                        # Update sms in DB to sent == True
                        sms.sent = True
                        db.session.commit()
                        sms.update().values(sent=True)
                    
                    else:

                        # There was an error... Better luck next time!
                        #   Abra-kadabra, ballin' in orlando.
                        logging.error("Sending sms via Twilio failed with status - " + m.status)
                        logging.debug(m)

                else:
                    logging.error("Skipped message because I'm only sending messages to myself!")
            else:
                logging.error(
                    "Skipped message " + str(sms.id) + 
                    "because of malformed phone number " + 
                    str(sms.human.phone_number)
                )
            

    def _create_states(self):
        db = FrancisDb()
        humans = db.session.query(Human).all()
        states = []
        for human in humans:
            logging.debug("len of incoming_sms " + str(len(human.incoming_sms)))
            states.append(SmsState(human))

        # TODO: not sure where this should be. Being used to see changes being
        #   made by web requests.
        db.session.commit()

        return states

    # Triggers an assessment of current DB state every INTERVAL_SECONDS
    def run(self):
        
        # Get TalentNetwork
        talent_network = TalentNetwork()
    
        counter = 1
        while True:

            logging.debug("Assessment iteration since startup " + str(counter))
            counter += 1

            try:
                self._send_sms()

            except Exception as e:
                logging.error("Failed to send sms - " + str(e))

            try:
                states = self._create_states()            

            except Exception as e:
                logging.error("Failed to create the states - " + str(e))
                sys.exit(1)

            for state in states:

                # Determine the most likely talent to be used
                talent_ps = talent_network.fetch_talent_probabilities(state)
                max_p_talent = {'p': -1}
                for talent_p in talent_ps:
                    if talent_p['p'] > max_p_talent['p']:
                        max_p_talent = talent_p
                logging.debug("probability of max_p_talent" + str(max_p_talent['p']))
                if max_p_talent['p'] > 500:
                    logging.debug("performing action!! @@@@@")
                    # Perform the talent's action
                    max_p_talent['action'].perform(state)

            time.sleep(INTERVAL_SECONDS)

    # Registers an action with the AssessmentWorker
    #   Registered actions will be included in all action assessments
    def register_action(self):
        pass

    # Calculates the probability of each possible action given the user and state
    #    Returns a dictionary with the actions as keys and probability as values
    def calculate_action_probabilities(self):
        pass

    # Calculates the probability of an active given the user and state
    #    Returns the probability of an action
    def calculate_action_probability(self):
        pass