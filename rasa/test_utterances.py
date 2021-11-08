"""This script tests rasa accuracy.
It submits a set of utterances to localhost:5005 and prints the result."""
import json
from http.client import HTTPConnection

utterances = [
    'the division is not clear',
    'clusters should be more split',
    'I wand the data to be more separated',
]

for u in utterances:
    connection = HTTPConnection(
        # Change here to host.docker.internal if running from inside docker
        host='localhost',
        port=5005,
    )
    connection.request("POST", "/model/parse", json.dumps({"text": u}))
    response = (json.loads(connection.getresponse().read()))
    print(f'"{response["text"]}" --> {response["intent"]["name"]} {round(response["intent"]["confidence"], 4)}')

