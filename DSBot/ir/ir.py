import importlib
import inspect
import logging
import pkgutil
from pathlib import Path

import DSBot.ir.impl
from DSBot.ir.ir_operations import IROpOptions


def run(ir, dataset):  # TODO: consider returning results to the caller
    # if len(ir) == 1:
    #     ir[0].run(results)
    # else:
    #     run(ir[1:], ir[0].run(results))
    # TODO(giubots): remove test code below
    if len(ir) == 0:
        logging.getLogger(__name__).warning('Empty pipeline')
        dataset.name_plot = Path(__file__).parent.parent / 'assets' / 'pepe.png'
    elif len(ir) == 1:
        logging.getLogger(__name__).info('Completed running %s', ir[0].name)
        dataset.name_plot = Path(__file__).parent.parent / 'assets' / 'pepe.png'
    else:
        logging.getLogger(__name__).info('Running %s', ir[0].name)
        run(ir[1:], dataset)


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
    return inspect.isclass(value) and 'DSBot.ir.impl.' in value.__module__ and issubclass(value, IROpOptions)


modules = []
for loader, module_name, is_pkg in pkgutil.walk_packages(DSBot.ir.impl.__path__, DSBot.ir.impl.__name__ + '.'):
    generic_classes = inspect.getmembers(importlib.import_module(module_name), is_generic)
    modules.extend(generic_classes)
    # _module = loader.find_module(module_name).load_module(module_name)  # TODO(giubots): remove
    # globals()[module_name] = _module
modules = {m: r[1] for r in modules for m in r[1]().get_models()}
