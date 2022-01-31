import json
import logging
import os
from http.client import HTTPConnection


class Rasa:

    def __init__(self):
        self.host = os.getenv("RASA_IP", "localhost")
        self.port = int(os.getenv("RASA_PORT", "5006"))

    def parse(self, utterance: str):
        """to avoid inferring wrong entities if the user inserts only a number"""
        if utterance.isnumeric():
            entity = float(utterance)
            intent = "NotAnIntent"
        else:
            intent = self.parseIntent(utterance)
            entity = self.parseEntities(utterance)
        return intent, entity

    def parseIntent(self, utterance: str):
        """returns a string"""
        connection = HTTPConnection(host=self.host, port=self.port)
        connection.request("POST", "/model/parse", json.dumps({"text": utterance}))
        response = json.loads(connection.getresponse().read())
        logging.getLogger(__name__).debug('Detected intent: %s', response)
        return response["intent"]["name"]

    def parseEntities(self, utterance: str):
        """"returns a string"""
        connection = HTTPConnection(host=self.host, port=self.port)
        connection.request("POST", "/model/parse", json.dumps({"text": utterance}))
        response = json.loads(connection.getresponse().read())
        logging.getLogger(__name__).debug('Detected intent: %s', response)
        if len(response["entities"]) != 0:
            return response["entities"][0]["value"]
        else:
            return "NotAnEntity"