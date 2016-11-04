import logging, datetime, pytz
from modules.sms_messages import SmsSender
from modules.helpers import naivelocal_to_naiveutc

# Represents a collection of actions that serve a general facility.
class Talent():

    # Returns the contained action that has the highest probablility of
    # intended execution.
    #    Returns {p: <probability of intention>, action: <action instance>}.
    def get_likely_action(self, state):
        pass

# Represents a specific routine which can be executed in the 'perform' method.
class Action():

    # Returns the probability that this action is desired given the passed
    # state.
    #    Defined by the subclass.
    def get_likelihood(self, state):
        pass

    # Executes the action.
    #    Defined by the subclass.
    def perform(self, state):
        pass

# SetReminderNotification
# An action that sends an sms notification at the desired time.
# A specific action.
class SetReminderNotification(Action):

    name = "SetReminderNotification"

    def _parse_command(self, command):
        
        split_command = command.split()

        if split_command[0].lower() != 'reminder':
            return None

        split_date = split_command[1].split('-')
        if len(split_date) != 3:
            return None

        split_time = split_command[2][:-2].split(':')
        ampm = split_command[2][-2:]
        if len(split_time) != 2 or (ampm != 'am' and ampm != 'pm'):
            return None

        return {
            'year': int(split_date[0]),
            'month': int(split_date[1]),
            'day': int(split_date[2]),
            'hour': int(split_time[0]),
            'minute': int(split_time[1]),
            'ampm': ampm,
            'text': 'This is the reminder text that still needs to be parsed.'
        }


    def get_likelihood(self, state):

        # Naive first model
        #
        # Looks if last log item is the command:
        # 'reminder yyyy-mm-dd hh:mm{am|pm} <some message to send>'

        if len(state.log) > 0:
            logging.debug("In here 1" + str(state.log[len(state.log)-1]['type']))
            if state.log[len(state.log)-1]['type'] == 'incoming_sms':
                logging.debug("In here 2")
                command_components = self._parse_command(state.log[len(state.log)-1]['text'])
                if command_components is not None:
                    logging.debug("In here 3")
                    return 501



        return 499 # Probability * 1000

    def perform(self, state):

        command = self._parse_command(state.log[len(state.log)-1]['text'])
        date_str = str(command['year']) + '-' + str(command['month']) + '-' + str(command['day'])
        time_str = str(command['hour']) + ':' + str(command['minute']) + command['ampm']

        naive = datetime.datetime.strptime (date_str + ' ' + time_str, "%Y-%m-%d %I:%M%p")
        # TODO: store local timezone somewhere
        utc_naive = naivelocal_to_naiveutc(naive, "Canada/Eastern")

        sms_sender = SmsSender()
        sms_sender.sms(state.human, "text of an outgoing sms!", utc_naive)


# ReminderNotifications
# A talent that sends sms requested reminders to the human.
# A specific talent.
class ReminderNotifications(Talent):

    name = "ReminderNotifications"

    __actions = [SetReminderNotification()]

    def get_likely_action(self, state):
        max_p = -1
        for action in ReminderNotifications.__actions:
            p = action.get_likelihood(state)
            if p > max_p:
                max_p = p
                max_p_action = action
        return max_p, max_p_action


# Collection of available talents
class TalentNetwork():

    # List of talents available in the talent network.
    # TODO: put the talents somewhere appropriate.
    __talents = [ReminderNotifications()]

    # Singleton instance.
    __instance = None

    # Instantiation creates/returns the singleton instance.
    def __new__(cls):

        if TalentNetwork.__instance is None:
            TalentNetwork.__instance = object.__new__(cls)
            TalentNetwork.__instance.talents = TalentNetwork.__talents

        return TalentNetwork.__instance

    def fetch_talent_probabilities(self, state):
        talent_probabilities = []

        for talent in self.talents:
            p, action = talent.get_likely_action(state)
            talent_probabilities.append({
                'p': p, 
                'action': action
            })
        return talent_probabilities