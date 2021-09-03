import json
import logging
from pathlib import Path

from mmcc_framework import DictCallback, Framework, NoNluAdapter

from DSBot.tuning.mmcc_config.callbacks import my_callbacks

# Load the process description and kb from file.
with open(Path(__file__).parent / 'mmcc_config/process_desc.json', "r") as process_file:
    proc = json.loads(process_file.read())
    logging.getLogger(__name__).debug('Reading process_desc file')
with open(Path(__file__).parent / 'mmcc_config/process_kb.json', "r") as process_file:
    kb = json.loads(process_file.read())
    logging.getLogger(__name__).debug('Reading process_kb file')


def get_framework() -> Framework:
    """Creates a new framework object, remember to call `handle_data_input({})` to get the first sentence.

    The framework will have an empty context, no NLU, and the kb will not be saved at the end of execution.
    """
    return Framework(process=proc,
                     kb=kb,
                     initial_context={},
                     callback_getter=DictCallback(callbacks=my_callbacks),
                     nlu=NoNluAdapter(expected_keys=[]),
                     on_save=lambda *args: None)
