import json
import logging
from http.client import HTTPConnection
from pathlib import Path
from typing import Dict, Any

from mmcc_framework import DictCallback, Framework
from mmcc_framework.nlu_adapters import NluAdapter

from tuning.mmcc_config.callbacks import my_callbacks
from tuning.types import Pipeline, PipelineCallback

# Load the process description and kb from file.
with open(Path(__file__).parent / 'mmcc_config' / 'process_desc.json', "r") as process_file:
    proc = json.loads(process_file.read())
    logging.getLogger(__name__).debug('Reading process_desc file')
with open(Path(__file__).parent / 'mmcc_config' / 'process_kb.json', "r") as process_file:
    kb = json.loads(process_file.read())
    logging.getLogger(__name__).debug('Reading process_kb file')


def get_framework(pipeline: Pipeline, result: str, start_work: PipelineCallback) -> Framework:
    """Creates a new framework object, remember to call `handle_data_input({})` to get the first sentence.

    The framework will have no NLU and the kb will not be saved at the end of execution.
    The context will contain the dataset and the pipeline.

    :param pipeline: the pipeline used in the last analysis
    :param result: base64 string representation of the previous analysis result
    :param start_work: callback that takes the pipeline and starts the execution in another thread
    """
    return Framework(process=proc,
                     kb=kb,
                     initial_context={'pipeline': pipeline, 'result': result, 'start_work': start_work},
                     callback_getter=DictCallback(callbacks=my_callbacks),
                     nlu=MyRasaNlu(),
                     on_save=lambda *args: None)


class MyRasaNlu(NluAdapter):
    """ This adapter uses Rasa, to use this adapter it is necessary to first setup and train the interpreter.

    The instructions on how to use Rasa are available on Rasa's website, and consist basically in the following steps:

    - Install Rasa and its dependencies;
    - Run `rasa init` in your folder of choice;
    - Edit the `data/nlu` file with the utterances used for training;
    - Run `rasa train nlu` to produce a model;
    - Start rasa on port 5005 and pass the location of the model:
      for example `rasa run --enable-api -m models/nlu-20201228-183937.tar.gz`

    Example:
        Suppose that the nlu is trained with, among the others, the intent "insert_name" with a entity "name".
        Initialize the adapter: `my_adapter = RasaNlu()`

        Suppose that it is time to insert the name. If it is necessary to insert it as text use:
        `my_framework.handle_text_input("Mark")`. The callback corresponding to the current activity will receive
        (if the intent is recognized): `{"intent": "insert_name", "name": "Mark"}`.

        If it is necessary to insert the name as data use:
        `my_framework.handle_data_input(RasaNlu.dict("insert_name", {"name": "Mark"}))`, which will pass to the callback
        the same structure as above.

    :ivar interpreter: the instance of the rasa interpreter used by this adapter
    """

    def parse(self, utterance: str) -> Dict[str, Any]:
        """ Runs the interpreter to parse the given utterance and returns a dictionary containing the parsed data.

        If no intent can be extracted from the provided utterance, this returns an empty dictionary.

        :param utterance: the text input from the user
        :return: a dictionary containing the detected intent and corresponding entities if any exists.
        """
        connection = HTTPConnection("host.docker.internal:5005")  # TODO modify here to use without docker
        connection.request("POST", "/model/parse", json.dumps({"text": utterance}))
        response = json.loads(connection.getresponse().read())
        if response["intent"]["name"] is None:
            return {"intent": ""}
        res = self.dict(response["intent"]["name"], {item['entity']: item["value"] for item in response["entities"]})
        logging.getLogger(__name__).debug('Detected intent: %s', res)
        return res

    @staticmethod
    def dict(intent: str, values: Dict[str, Any] = None) -> Dict[str, Any]:
        """ Helper method that can be used to produce a dictionary equivalent to the one of the parse method.
        Use this method with framework.handle_data_input.

        :param intent: the intent corresponding to this input
        :param values: an optional dictionary containing pairs of entity-value
        :return: a dictionary equivalent to the one produced by the parse method
        """
        if values is None:
            values = {}
        return {"intent": intent, **values}
