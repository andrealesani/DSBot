# TODO enum for states
"""This class manages the first and second part of conversation. It differentiates between the two parts with the
attribute "part" saved in a JSON named with the user's sessionID. In the JSON file there is also an attribute "state"
in which the state of the fsm is updated. The method get_response receives as input the intent (extracted by the RASA
nlu) and the current fsm state and returns the next state and the response to be shown to the user. The output state
is used to update the user's JSON file """
import json
import os
import base64
from conversation.fsm.json_helper import Json_helper

from DSBot.conversation.fsm.pipelineDrivenConv import pipelineDrivenConv

""" structure of the JSON file:
file name: conv_<session_id>.json
file content:
{
    "part": "<int(1,2)>",
    "state": "<str>"
}
    """


class Conv:
    def __init__(self):
        self.jh = Json_helper()

        try:
            os.makedirs('./conversation/temp')
        except:
            pass

    # TODO clean code, make it read from JSON file
    """returns a dictionary with 1 "response" field"""
    def get_response(self, intent: str, session_id, state="greeting"):
        """fsm manager"""
        response = {"response": ["Sorry, what did you just say?"]}
        if intent == "help":
            return self.send_help(session_id, state)
        elif intent == "reset":
            response = {"response": ["I understand this maybe frustrating but", "lets just restart from the beginning", "and ask me whenever you need help", "Would you like to perform supervised or unsupervised learning?"]}
            state = "greeting"
        elif state == "greeting":
            if intent == "greet":
                state = "sup_unsup"
                response = {"response": ["Hello!", "Would you like to do supervised or unsupervised learning?"]}
            elif intent == "supervised":
                state = "supervised"
                response = {"response": ["Are you trying to predict a label or a categorical attribute?"]}
                #   TODO sistema il formato della risposta
                response["response"].append("Capito Gigio?")
                print(response["response"][0], response["response"][1])
            elif intent == "unsupervised":
                state = "unsupervised"
                response = {"response": ["Do you want to gather together in groups similar data or find some pattern in their features?"]}
            elif intent == "clustering" or intent == "association" or intent == "classification" or intent == "regression":
                state = "start_pipeline"
                response = {"response": ["Ok, " + intent + ". Let's set some parameters."]}

        elif state == "sup_unsup":
            if intent == "supervised":
                state = "supervised"
                response = {"response": ["Are you trying to predict a label or a categorical attribute?"]}
            elif intent == "unsupervised":
                state = "unsupervised"
                response = {"response": ["Do you want to gather together in groups similar data or find some pattern in their features?"]}
            elif intent == "clustering" or intent == "association" or intent == "classification" or intent == "regression":
                state = "start_pipeline"
                response = {"response": ["Ok, " + intent + ". Let's set some parameters."]}

        elif state == "unsupervised":
            if intent == "clustering" or intent == "association":
                state = "start_pipeline"
                response = {"response": ["Ok, " + intent + ". Let's set some parameters."]}

        elif state == "supervised":
            if intent == "classification" or intent == "regression":
                state = "start_pipeline"
                response = {"response": ["Ok, " + intent + ". Let's set some parameters."]}

        else:
            response = {"response": ["I'm sorry, i couldn't get what you said. Would you repeat?"]}

        self.jh.updatestate(session_id, state)
        return response

    def send_help(self, session_id, state: str):
        """returns a hint for each state the user can be in"""
        self.jh.updatePredState(session_id, state)
        help = self.jh.getHelp(state)
        del help["response2"]
        with open(help["image"], "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
            # trasformo il bytecode in stringa
            base64_string = my_string.decode('utf-8')
            help["image"] = str(base64_string)
        return help
        """ if (state == "greeting"):
            return {"response":"I'm sorry, I don't know how to help you right now"}
        if (state == "sup_unsup"):
            return {"response":"help1"}
        elif (state == "unsupervised"):
            return {"response":"help1"}
        elif (state == "supervised"):
            return {"response":"help1"}
        elif (state == "clustering"):
            return {"response":"help1"}
        elif (state == "association"):
            return {"response":"help1"}
        elif (state == "classification"):
            return {"response":"help1"}
        elif (state == "regression"):
            return {"response":"help1"}"""









