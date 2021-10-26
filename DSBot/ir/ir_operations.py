from abc import ABC, abstractmethod
from typing import Iterable, Dict

from ir.ir_exceptions import UnknownParameter
from ir.ir_parameters import IRNumPar
from tuning import TuningOpMixin, TuningOpOptionsMixin


class IROp(TuningOpMixin, ABC):
    """An operation that can be performed on the dataset.

    WARNING: Subclasses must explicitly call the constructor of this.

    :ivar name: the name of this operation
    :ivar parameters: dictionary where the keys are the parameter names and the values are `IRPar` objects
    """

    def __init__(self, name: str, parameters: Iterable[IRNumPar]):
        self.name = name
        self.parameters = par_helper(parameters, name)
        self._param_setted = False

    def get_parameters_list(self):
        return self.parameters.keys()

    def get_param(self, name):
        try:
            return self.parameters[name]
        except KeyError:
            raise UnknownParameter()

    @abstractmethod
    def run(self, result, session_id):
        pass


class IROpOptions(TuningOpOptionsMixin, object):
    """A group of `IROp` objects, calls to this are forwarded to the default IROp.

    WARNING: Subclasses must explicitly call the constructor of this.

    :ivar models: dictionary where the keys are the module names and the values are `IROp` objects
    :ivar default: the name of the default model
    :ivar actual_model: the default `IROp` model
    """

    def __init__(self, models: Iterable[IROp], default: str) -> object:
        self.models = {m.name: m for m in models}
        self.default = default
        self.actual_model = self.models[default]

    def get_models(self):
        return self.models.keys()

    def set_model(self, name):
        self.actual_model = self.models[name]

    def __getattribute__(self, item):
        if item in ["__init__", "get_models", "set_model", "actual_model", "default", "models", "to_json", "__repr__",
                    "should_change"]:
            return object.__getattribute__(self, item)
        else:
            return self.actual_model.__getattribute__(item)

    def __setattr__(self, key, value):
        if key in ["models", "default", "actual_model", "should_change"]:
            return object.__setattr__(self, key, value)
        return self.actual_model.__setattr__(key, value)


def par_helper(parameters: Iterable[IRNumPar], module_name: str) -> Dict[str, IRNumPar]:
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
