from abc import ABC

from ir.ir_exceptions import UnknownParameter
from tuning.tuning_mixins import TuningOpMixin, TuningOpOptionsMixin


class IROp(TuningOpMixin, ABC):
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def get_parameters_list(self):
        return self.parameters.keys()

    def get_param(self, name):
        try:
            return self.parameters[name]
        except:
            raise UnknownParameter()

    def run(self):
        pass


class IROpOptions(TuningOpOptionsMixin):
    def __init__(self, models, default):
        self.models = models
        self.default = default
        self.actual_model = models[default]

    def get_models(self):
        return self.models.keys()

    def set_model(self, name):
        self.actual_model = self.models[name]

    def __getattribute__(self, item):
        if item in ["__init__", "get_models", "set_model", "actual_model", "default", "models"]:
            return object.__getattribute__(self, item)
        else:
            return self.actual_model.model.__getattribute__(item)
