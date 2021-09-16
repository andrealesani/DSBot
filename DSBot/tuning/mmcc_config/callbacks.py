"""
Assumes that the context contains the dataset and the pipeline to use and update, and the old result.
{
    'pipeline': pipeline,
    'result': base64oldResult,
    'start_work': callback to start the pipeline execution
}
"""
import logging

from mmcc_framework import Response

import ir.ir_exceptions
from tuning.problem_helper import get_data, MissingSolutionError
from tuning.tuning_mixins import update_pipeline


def start(_, kb, context, __):
    """Returns the result and a welcome utterance."""
    payload = {
        'status': 'choose_problem',
        'result': context['result'],
    }
    return Response(kb, context, True, payload=payload)


def choose_problem(data, kb, context, _):
    """In this step the user can try to explain the problem he is facing.

    If data['intent'] is 'skip' the process to continues without selecting a problem.
    Otherwise data['intent'] can be a problem keyword.
    """
    try:
        intent = data['intent']
        if intent == 'skip':
            context['solution'] = None
            payload = {
                'status': 'edit_param',
                'pipeline': [e.to_json() for e in context['pipeline']],
            }
            return Response(kb, context, True, utterance=kb['no_highlights_sentence'], payload=payload)

        solution = get_data(intent, context['pipeline'], data.get('test_p', None))
        utterance = solution.sentence + ' ' + kb['edit_param_sentence']
        context['pipeline'] = update_pipeline(context['pipeline'], solution.relevant_params)
        payload = {
            'status': 'edit_param',
            'pipeline': [e.to_json() for e in context['pipeline']],
        }
        return Response(kb, context, True, utterance=utterance, payload=payload)

    except KeyError:
        msg = f'Received data without intent: {str(data)}'
        logging.getLogger(__name__).error(msg)
    except MissingSolutionError:
        msg = kb['problem_err']
    return Response(kb, context, False, utterance=msg)


def edit_param(data, kb, context, _):
    """In this step the user can edit the pipeline.

    data['intent'] can be 'set' or 'run', the latter causes the pipeline to be run.
    data['module'] contains the module of the parameter to change.
    data['parameter'] contains the parameter name to change.
    data['value'] contains the new value.
    """
    try:
        intent = data['intent']
        if intent == 'run':
            context['start_work'](context['pipeline'])
            return Response(kb, context, True, payload={'status': 'end'})

        if intent == 'set' and 'module' in data and 'parameter' in data and 'value' in data:
            module = next(m for m in context['pipeline'] if m.name == data['module'])
            parameter = module.get_param(data['parameter'])
            parameter.tune_value(data['value'])
            payload = {'status': 'edit_param', 'pipeline': [e.to_json() for e in context['pipeline']]}
            return Response(kb, context, False, payload=payload, utterance=kb['values_updated'])

        msg = kb['values_intent_err']

    except KeyError:
        msg = f'Received data with missing intent or entities: {str(data)}'
        logging.getLogger(__name__).error(msg)
    except StopIteration:
        msg = kb['no_module_err'] + data['module']
    except DSBot.ir.ir_exceptions.UnknownParameter:
        msg = kb['no_param_err'] + data['parameter']
    except DSBot.ir.ir_exceptions.IncorrectValue:
        msg = kb['value_err']

    return Response(kb, context, False, utterance=msg)


my_callbacks = {
    "start": start,
    "choose_problem": choose_problem,
    "edit_param": edit_param,
}
