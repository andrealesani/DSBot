import importlib


def run(ir, results):  # TODO: consider returning results to the caller
    if len(ir) == 1:
        ir[0].run(results)
    else:
        run(ir[1:], ir[0].run(results))


def create_IR(pipeline):
    dict_pipeline = []
    package = importlib.import_module('ir')  # TODO: must add imports to __init__.py
    for i in pipeline:
        dict_pipeline.append(getattr(package, i))  # FIXME: this probably gets IROp instead of IROpOptions
    return dict_pipeline
