# TODO enum for states

class Conv:
    state = "greeting"

    def __init__(self):
        self.state = "greeting"

    # TODO clean code, make it read from JSON file
    def get_response(self, intent: str):
        """fsm manager"""

        if intent == "help":
            return self.send_help()

        elif self.state == "greeting":
            if intent == "greet":
                self.state = "sup_unsup"
                return "Would you like to do supervised or unsupervised learning?"
            elif intent == "clustering":
                self.state = "start_pipeline"
                return "Ok, clustering! Let's set some parameters"
            else:
                return "I'm sorry, i couldn't get what you said. Would you repeat?"

        elif self.state == "sup_unsup":
            if intent == "supervised":
                self.state = "supervised"
                return "Are you trying to predict a label or a categorical attribute?"
            elif intent == "unsupervised":
                self.state = "unsupervised"
                return "Do you want to gather together in groups similar data or find some pattern in their features"

        elif self.state == "unsupervised":
            if intent == "clustering" or intent == "association":
                self.state = intent
                return "Ok," + intent + ". Let's set some parameters."

        elif self.state == "supervised":
            if intent == "classification" or intent == "regression":
                self.state = intent
                return "Ok," + intent + ". Let's set some parameters."

    # TODO read help sentences from JSON
    def send_help(self):
        """returns a hint for each state the user can be in"""
        if (self.state == "sup_unsup"):
            return "help1"
        elif (self.state == "unsupervised"):
            return "help2"
        elif (self.state == "supervised"):
            return "help3"
        elif (self.state == "clustering"):
            return "help4"
        elif (self.state == "association"):
            return "help5"
        elif (self.state == "classification"):
            return "help6"
        elif (self.state == "regression"):
            return "help7"
