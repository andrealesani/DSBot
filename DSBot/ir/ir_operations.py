from abc import ABC, abstractmethod
from typing import Iterable, Dict

from DSBot.ir.ir_exceptions import UnknownParameter
from DSBot.ir.ir_parameters import IRPar
from DSBot.tuning import TuningOpMixin, TuningOpOptionsMixin


class IROp(TuningOpMixin, ABC):
    """An operation that can be performed on the dataset.

    WARNING: Subclasses must explicitly call the constructor of this.

    :ivar name: the name of this operation
    :ivar parameters: dictionary where the keys are the parameter names and the values are `IRPar` objects
    """

    def __init__(self, name: str, parameters: Iterable[IRPar]):
        self.name = name
        self.parameters = par_helper(parameters, name)

    def get_parameters_list(self):
        return self.parameters.keys()

    def get_param(self, name):
        try:
            return self.parameters[name]
        except KeyError:
            raise UnknownParameter()

    @abstractmethod
    def run(self, result):
        pass


class IROpOptions(TuningOpOptionsMixin, object):
    """A group of `IROp` objects, calls to this are forwarded to the default IROp.

    WARNING: Subclasses must explicitly call the constructor of this.

    :ivar models: dictionary where the keys are the module names and the values are `IROp` objects
    :ivar default: the name of the default model
    :ivar actual_model: the default `IROp` model
    """

    def __init__(self, models: Iterable[IROp], default: str):
        self.models = {m.name: m for m in models}
        self.default = default
        self.actual_model = self.models[default]

    def get_models(self):
        return self.models.keys()

    def set_model(self, name):
        self.actual_model = self.models[name]

    def __getattribute__(self, item):
        if item in ["__init__", "get_models", "set_model", "actual_model", "default", "models", "to_json", "__repr__"]:
            return object.__getattribute__(self, item)
        else:
            return self.actual_model.model.__getattribute__(item)


def par_helper(parameters: Iterable[IRPar], module_name: str) -> Dict[str, IRPar]:
    """Given an iterable of IRPar and their module name, returns a dictionary containing the parameters.

    This helps to reduce chances of errors with mismatching dictionary key and parameter name,
    and sets the module attribute for all the parameters.

    The dictionary will have as keys each parameter name.
    The parameters will have the module attribute set to the module name.
    """
    result = {}
    for e in parameters:
        e.module = module_name
        result[e.name] = e
    return result
