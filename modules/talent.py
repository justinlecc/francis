import logging, datetime, pytz, parsedatetime, random
from modules.sms_io import SmsIo
from modules.helpers import naivelocal_to_naiveutc

# Represents a collection of actions that serve a general facility.
class Talent():

    # Returns the contained action that has the highest probablility of
    # intended execution.
    #    Returns {p: <probability of intention>, action: <action instance>}.
    def get_likely_action(self, state):
        pass

    # Returns a message that can help the human to understand and use 
    # this talent.
    def get_help_message(self):
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

class DisplayHelp(Action):

    name = "DisplayHelp"

    def get_likelihood(self, state):

        # Log is not empty
        if len(state.log) > 0:
            # The last item in the log is an incoming sms
            if state.log[len(state.log)-1]['type'] == 'incoming_sms':

                # Split the message into words
                split_message = state.log[len(state.log)-1]['text'].split()

                # If the first word is help, then this is the action the human wants
                if ('help' == split_message[0].lower()):

                    return 800 # Strong probability

        return 0
                
    # DisplayHelp shows the human two types of help manuals:
    #   1. The help manual of the 'HelpMenu' talent.
    #   2. The help manual of the specified talent.
    def perform(self, state):

        # Get the system's talents
        talents = TalentNetwork().get_talents()

        split_message = state.log[len(state.log)-1]['text'].split()

        # Check if the human wants help with a specific talent
        if len(split_message) == 1:

            # Display the main help manual
            message = "The following are my talents:\n"

            for talent in talents:
                message += "-" + talent.name + "\n"

            message += '\nSend the message "help <talent name>" for help with that talent.'

        elif len(split_message) > 1:

            message = ""
            for talent in talents:

                if talent.name.lower() ==  split_message[1].lower():
                    message = talent.get_help_message()

            if message == "":
                message = "I don't have any talent's named " + split_message[1] + "."

        else:

            logging.error("DisplayHelp::perform called with an empty (all whitespace) last message")

        # Send the help message to the human
        SmsIo().send_sms(state.human, message, datetime.datetime.utcnow())

# Help menu
# Talent acts as a manual for humans
class HelpMenu(Talent):

    name = "HelpMenu"

    __actions = [DisplayHelp()]

    def get_likely_action(self, state):
        max_p = -1
        for action in HelpMenu.__actions:
            p = action.get_likelihood(state)
            if p > max_p:
                max_p = p
                max_p_action = action
        return max_p, max_p_action

    # Returns a message that can help the human to understand and use 
    # this talent.
    def get_help_message(self):
        return 'Send me "help" for a list of all talents or "help <talent name>" for help with that talent.'



# SetReminderNotification
# An action that sends an sms notification at the desired time.
# A specific action.
class SetReminderNotification(Action):

    name = "SetReminderNotification"

    # If I said it, I can't take my word back.
    def _parse_command(self, command):

        split_command = command.split()

        # I got two phones, one for the bitches and one for the dough
        version = 2
        if (version == 1) :

            # Reminder command
            if split_command[0].lower() != 'reminder':
                return None

            # Get the date of reminder
            split_date = split_command[1].split('-')
            if len(split_date) != 3:
                return None

            # Get time of the reminder
            time_str = split_command[2]
            try:
                time_dt = datetime.datetime.strptime(time_str, "%I:%M%p")
            except Exception as e:
                logging.error("parsing time failed in SetReminderNotification::_parse_command")
                return None

            # Get the text of the reminder
            text = ' '.join(split_command[3:])

            return_dict = {
                'year': int(split_date[0]),
                'month': int(split_date[1]),
                'day': int(split_date[2]),
                'hour': int(time_dt.hour),
                'minute': int(time_dt.minute),
                'text': text
            }

        else:

            if 'remind' not in command.lower():
                return None

            # parse statuses (https://bear.im/code/parsedatetime/docs/index.html):
            #   0 = not parsed at all 
            #   1 = parsed as a C{date} 
            #   2 = parsed as a C{time} 
            #   3 = parsed as a C{datetime}
            local_dt = datetime.datetime.now(pytz.timezone("Canada/Eastern"))
            pdt_tuples = parsedatetime.Calendar().nlp(command, local_dt)

            # Check if no dates were found
            if pdt_tuples is None:
                return None

            pdt_tuple = parsedatetime.Calendar().nlp(command, local_dt)[0] # Only takes the first tuple (for now)

            # Pick up the phone babe-eh
            # Check if the parse status was 0 (ie. the command was not parsed)
            if pdt_tuple[1] == 0:
                return None

            pdt_dt = pdt_tuple[0]

            reminder_intros = [
                "Don't forget",
                "Remember when you told me to remind you",
                "If I remember correctly, I should be reminding you"
            ]

            text = reminder_intros[random.randint(0, 100) % (len(reminder_intros) - 1)] + ": " + command

            return_dict = {
                'year': pdt_dt.year,
                'month': pdt_dt.month,
                'day': pdt_dt.day,
                'hour': pdt_dt.hour,
                'minute': pdt_dt.minute,
                'text': text
            }            

        return return_dict

    # I swear she do the most.
    def get_likelihood(self, state):
        # Naive first model
        #
        # Looks if last log item is the command:
        # 'reminder yyyy-mm-dd hh:mm{am|pm} <some message to send>'
        if len(state.log) > 0:
            if state.log[len(state.log)-1]['type'] == 'incoming_sms':
                command_components = self._parse_command(state.log[len(state.log)-1]['text'])
                if command_components is not None:
                    return 501 # Cheeky return value

        return 499 # Probability * 1000

    # Fuckwithmeyouknowigotit
    def perform(self, state):

        command = self._parse_command(state.log[len(state.log)-1]['text'])
        date_str = str(command['year']) + '-' + str(command['month']) + '-' + str(command['day'])
        time_str = str(command['hour']) + ':' + str(command['minute'])

        naive = datetime.datetime.strptime (date_str + ' ' + time_str, "%Y-%m-%d %H:%M")
        # TODO: store local timezone somewhere
        utc_naive = naivelocal_to_naiveutc(naive, "Canada/Eastern")

        sms_io = SmsIo()

        # Let the human know what was accomplished
        message = "I set a reminder for " + naive.strftime("%c") + "."
        sms_io.send_sms(state.human, message, datetime.datetime.utcnow())

        # Set the reminder
        sms_io.send_sms(state.human, command['text'], utc_naive)


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

    # Returns a message that can help the human to understand and use 
    # this talent.
    def get_help_message(self):
        return """Send me a message, starting with the word "Remind", that contains the date and/or time you'd to be reminded."""



# Collection of available talents
class TalentNetwork():

    # List of talents available in the talent network.
    # TODO: put the talents somewhere appropriate.
    __talents = [ReminderNotifications(), HelpMenu()]

    # Singleton instance.
    __instance = None

    # Instantiation creates/returns the singleton instance.
    def __new__(cls):

        if TalentNetwork.__instance is None:
            TalentNetwork.__instance = object.__new__(cls)
            TalentNetwork.__instance.talents = TalentNetwork.__talents

        return TalentNetwork.__instance

    def get_talents(self):
        return TalentNetwork.__talents

    def fetch_talent_probabilities(self, state):
        talent_probabilities = []
        for talent in self.talents:
            p, action = talent.get_likely_action(state)
            talent_probabilities.append({
                'p': p, 
                'action': action
            })
        return talent_probabilities