
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


    #TODO per implementare il back di uno stato fai update pred state a ogni chiamata
    """returns a dictionary with 1 "response" field"""
    def get_response(self, intent: str, session_id, state="greeting"):
        """fsm manager"""
        #debug
        response = {"response": ["Sorry, I couldn't understand. Can you try to use synonyms or rephrase your message?"]}

        if state != "help" and intent == "help":
            self.jh.updatePredState(session_id, state)
            response = self.send_help(state, 1)
            state = "help"
            response["response"].extend(["Got it?"])
        elif state == "help" and (intent == "affirm" or intent == "help" or intent == "deny" or intent == "example"):
            if intent == "affirm":
                state = self.jh.getPredState(session_id)
                response = {"response": ["So you're a data scientist and kept it from me 🤷‍♂️"]}
                for s in self.jh.getQuestion(state):
                    response["response"].append(s)
            elif intent == "help" or intent == "deny" or intent == "example":
                state = self.jh.getPredState(session_id)
                response = self.send_help(state, 2)
                response["response"].append("So after these nice examples you've got to choose 👀")
                for s in self.jh.getQuestion(state):
                    response["response"].append(s)
            #TODO STATO CONFERMA RESET
        elif state != "reset" and intent == "reset":
            self.jh.updatePredState(session_id, state)
            response = {"response": ["Would you like to start all over again?"]}
            state = "reset"
        elif state == "reset":
            if (intent == "affirm" or intent == "reset"):
                response = {"response": ["I understand this may be frustrating but lets just restart from the beginning",
                                     "Don't forget to ask me for help whenever you need",
                                     "Would you like to perform supervised or unsupervised learning?"]}
                state = "greeting"
                self.jh.updatePredState(session_id, state)
            else:
                state = self.jh.getPredState(session_id)
                response = {"response": ["All right then, lets go on"]}
                response["response"].extend(self.jh.getQuestion(self.jh.getPredState(session_id)))
        elif state == "greeting":
            if intent == "greet":
                # state = "sup_unsup"
                response = {"response": ["Hello!", "Would you like to do supervised or unsupervised learning?"]}
            elif intent == "supervised":
                state = "supervised"
                response = {"response": self.jh.getQuestion(state)}
            elif intent == "unsupervised":
                state = "unsupervised"
                response = {"response":self.jh.getQuestion(state)}
            elif intent == "clustering":
                state = "start_pipeline"
                response = {"response": ["Ok, you want to do " + intent + ". Let's set some parameters."]}
            elif intent == "association" or intent == "classification" or intent == "regression":
                state = "greeting"
                response = {"response": ["Ok, you want to do " + intent + "."]}

        #elif state == "sup_unsup":
        #    if intent == "supervised":
        #        state = "supervised"
        #        response = {"response": self.jh.getQuestion(state)}
        #        #response = {"response": ["Are you trying to predict a label or a categorical attribute?"]}
        #    elif intent == "unsupervised":
        #        state = "unsupervised"
        #        response = {"response":self.jh.getQuestion(state)}
        #        #response = {"response": ["Do you want to gather together in groups similar data or find some pattern in their features?"]}
        #    elif intent == "clustering" or intent == "association" or intent == "classification" or intent == "regression":
        #        state = "start_pipeline"
        #        response = {"response": ["Ok, " + intent + ". Let's set some parameters."]}
#
        elif state == "unsupervised":
            if intent == "greet":
                response = {"response": ["Hi!",
                                         "Do you want to gather together in groups similar data or find some pattern in their features?"]}
            elif intent == "clustering":
                state = "start_pipeline"
                response = {"response": ["Ok, you want to do " + intent + ". Let's set some parameters."]}
            elif intent == "association":
                state = "unsupervised"
                response = {"response": ["Ok, you want to do " + intent + "."]}

        elif state == "supervised":
            if intent == "greet":
                response = {"response": ["Hi!", "Are you trying to predict a label or a categorical attribute?"]}
            elif intent == "classification" or intent == "regression":
                state = "supervised"
                response = {"response": ["Ok, you want to do " + intent + "."]}

        self.jh.updatestate(session_id, state)
        return response

    def send_help(self, state: str, helpN: int):
        """returns a hint for each state the user can be in"""
        help = self.jh.getHelp(state)
        if helpN == 1:
            del help["response2"]
        else:
            del help["response"]
            help["response"] = help["response2"]
            del help["response2"]
            #TODO sposta il codice per trascrivere l'immagine in json_helper.getHelp()
        with open(help["image"], "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
            # trasformo il bytecode in stringa
            base64_string = my_string.decode('utf-8')
            help["image"] = str(base64_string)
        return help
        #if (state == "greeting"):
        #    return {"response":"I'm sorry, I don't know how to help you right now"}
        #if (state == "sup_unsup"):
        #    return {"response":"help1"}
        #elif (state == "unsupervised"):
        #    return {"response":"help1"}
        #elif (state == "supervised"):
        #    return {"response":"help1"}
        #elif (state == "clustering"):
        #    return {"response":"help1"}
        #elif (state == "association"):
        #    return {"response":"help1"}
        #elif (state == "classification"):
        #    return {"response":"help1"}
        #elif (state == "regression"):
        #    return {"response":"help1"}
#

#"I understand this may be frustrating but lets just restart from the beginning",
#                                     "Don't forget to ask me for help whenever you need",
#                                     "Would you like to perform supervised or unsupervised learning?"