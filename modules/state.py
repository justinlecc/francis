import logging

# Represents a the state of the system at a fixed point
#    Includes information such as system inputs, outputs and state variables
#    Used only as a superclass for specific types of States (eg. SmsState)
class State():
    pass

# Represents the state of an interaction between Francis and the user.
#    Contains all the information neccessary to make decisions regarding
#    which actions to take.
class SmsState(State):

    def __init__(self, human):
        self.human = human

        # Log items include incoming_sms, outgoing_sms and 
        log = []
        
        # Push incoming_sms
        for sms in human.incoming_sms:
            log.append({
                'type': 'incoming_sms',
                'text': sms.text,
                'datetime': sms.created_at
            })

        # Push outgoing_sms
        for sms in human.outgoing_sms:
            log.append({
                'type': 'outgoing_sms',
                'text': sms.text,
                'datetime': sms.created_at,
                'sendtime': sms.send_at
            })

        # Sort log
        self.log = sorted(log, key=lambda k: k['datetime'])

        logging.debug(self.log)

