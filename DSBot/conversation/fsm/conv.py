class Conv:
    state = "beginning"
    def __init__(self):
       self.state = "greeting"
    def get_response(self, intent:str):
        if(self.state=="greeting"):
            if(intent == "greet"):
                self.state = "ask_sup_unsup"
                return "Would you like to do supervised or unsupervised learning?"
            elif (intent == "clustering"):
                self.state = "start_pipeline"
                return "Ok, clustering! Let's set some parameters"
            else:
                return "I'm sorry i couldn't get what you said"
        elif(self.state=="ask_sup_unsup"):
            if (intent == "supervised"):
                self.state = "supervised"
                return "Do you want to gather together in groups similar data or find some pattern in their features"
            elif(intent=="unsupervised"):
                self.state = "unsupervised"
                return "Are you trying to predict a label or a categorical attribute?"

