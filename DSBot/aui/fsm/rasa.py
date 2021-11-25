import json
import logging
import os
from http.client import HTTPConnection


class Rasa:

    def __init__(self):
        self.host = os.getenv("RASA_IP", "localhost")
        self.port = int(os.getenv("RASA_PORT", "5006"))

    def parse(self, utterance: str):
        connection = HTTPConnection(host=self.host, port=self.port)
        connection.request("POST", "/model/parse", json.dumps({"text": utterance}))
        response = json.loads(connection.getresponse().read())
        logging.getLogger(__name__).debug('Detected intent: %s', response)
        return response["intent"]["name"]