import json
import logging
from pathlib import Path

from mmcc_framework import DictCallback, Framework, NoNluAdapter

from DSBot.tuning.mmcc_config.callbacks import my_callbacks
from DSBot.tuning.types import Pipeline, PipelineCallback

# Load the process description and kb from file.
with open(Path(__file__).parent / 'mmcc_config/process_desc.json', "r") as process_file:
    proc = json.loads(process_file.read())
    logging.getLogger(__name__).debug('Reading process_desc file')
with open(Path(__file__).parent / 'mmcc_config/process_kb.json', "r") as process_file:
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
                     nlu=NoNluAdapter(expected_keys=['intent', 'module', 'parameter', 'value']),
                     on_save=lambda *args: None)
