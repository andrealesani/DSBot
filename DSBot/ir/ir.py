import importlib
import inspect
import logging
import pkgutil

import ir.impl
from ir.ir_operations import IROpOptions


def run(ir, dataset, session_id):
    if len(ir) == 1:
        return ir[0].run(dataset, session_id)
    else:
        return run(ir[1:], ir[0].run(dataset, session_id), session_id)


def create_IR(pipeline):
    dict_pipeline = []
    for item in pipeline:
        try:
            module = modules[item]()
            module.set_model(item)
            dict_pipeline.append(module)
        except KeyError:
            logging.getLogger(__name__).error('Missing module implementation for: %s', item)
    return dict_pipeline


def is_generic(value):
    return inspect.isclass(value) and 'ir.impl.' in value.__module__ and issubclass(value, IROpOptions)


modules = []
for loader, module_name, is_pkg in pkgutil.walk_packages(ir.impl.__path__, ir.impl.__name__ + '.'):
    generic_classes = inspect.getmembers(importlib.import_module(module_name), is_generic)
    modules.extend(generic_classes)

modules = {m: r[1] for r in modules for m in r[1]().get_models()}
