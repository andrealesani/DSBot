"""Add info related with tuning to ir classes.

The tuning_kb must be as follows:
{
    "module_name": {
        "name": "Readable module name",
        "params": {
            "param_name": {
                "name": "Readable param name",
                "desc": "A description of what this param does"
            }
        }
    }
}
"""
import json
import logging
from pathlib import Path
from typing import Any, List, Tuple

from tuning.types import Pipeline

# Load the tuning kb data from file.
with open(Path(__file__).parent / 'tuning_kb.json', 'r') as tuning_kb_file:
    logging.getLogger(__name__).debug('Reading tuning_kb file')
    tuning_kb = json.loads(tuning_kb_file.read())


class MissingModuleNameError(Exception):
    """Raised when an IRPar does not have the module name set."""

    def __init__(self, param_name):
        super().__init__(f'This IRPar does not have the module name set: {param_name}')


class IncorrectKbError(Exception):
    """Raised when the structure of the tuning_kb is not correct."""
    pass


class TuningOpMixin:
    """Adds tuning functionalities to a IROp class."""
    name: str
    parameters: dict
    _highlighted: bool

    @property
    def pretty_name(self):
        """Returns the printable name of this IROp, `self.name` if not found."""

        try:
            return tuning_kb[self.name]['name']
        except KeyError:
            logging.getLogger(__name__).warning('Missing pretty name for module: %s', self.name)
        return self.name

    @property
    def is_highlighted(self):
        try:
            return self._highlighted
        except AttributeError:
            return False

    @is_highlighted.setter
    def is_highlighted(self, value):
        self._highlighted = value

    def to_json(self):
        return {
            'name': self.name,
            'pretty_name': self.pretty_name,
            'parameters': [v.to_json() for v in self.parameters.values()],
            'is_highlighted': self.is_highlighted
        }

    def __repr__(self) -> str:
        return str(self.to_json())

    @classmethod
    def reverse_pretty(cls, pretty: str, pipeline: Pipeline):
        """Returns the first IROp (IROpOptions) with `pretty` as its `name` or `pretty_name`.
        This ignores submodules. If none is found this returns None."""
        for module in pipeline:
            if module.name == pretty or module.pretty_name == pretty:
                return module
        return None


class TuningOpOptionsMixin:
    """Adds tuning functionalities to a IROpOptions class."""
    actual_model: Any
    models: dict
    _change: bool

    def to_json(self):
        actual = self.actual_model.to_json()
        actual['should_change'] = self.should_change
        actual['models'] = [v.to_json() for v in self.models.values()]
        return actual

    @property
    def should_change(self):
        try:
            return self._change
        except AttributeError:
            return False

    @should_change.setter
    def should_change(self, value):
        self._change = value

    def __repr__(self) -> str:
        return str(self.to_json())

    @classmethod
    def reverse_pretty(cls, pretty: str, pipeline: Pipeline):
        """Returns the first IROp that has `pretty` as its `name` or `pretty_name` and its IROpOptions.
        If none is found this returns None."""
        for module in pipeline:
            if module.name == pretty or module.pretty_name == pretty:
                return module, module

            for option in module.models.values():
                if option.name == pretty or option.pretty_name == pretty:
                    return option, module
        return None, None


class TuningParMixin:
    """Adds tuning functionalities to a IRPar class; attribute `module` must be set."""
    name: str
    module: str
    value: Any
    default_value: Any
    min_v: Any
    max_v: Any
    v_type: str
    _highlighted: bool

    @property
    def pretty_name(self):
        """Returns the printable name of this IRPar, `self.name` if not found."""

        try:
            return self._get_param_data()['name']
        except IncorrectKbError as e:
            logging.getLogger(__name__).warning(e)
        except KeyError:
            logging.getLogger(__name__).warning('Missing pretty name for param: %s; module: %s', self.name, self.module)
        return self.name

    @property
    def description(self):
        """Returns the description of this IRPar, an empty string if not found."""

        try:
            return self._get_param_data()['desc']
        except IncorrectKbError as e:
            logging.getLogger(__name__).warning(e)
        except KeyError:
            logging.getLogger(__name__).warning('Missing description for param: %s; module: %s', self.name, self.module)
        return ''

    def _get_param_data(self):
        """Returns the parameter data dictionary for this parameter.

        :raise MissingModuleNameError: if this IrPar does not have the module name set
        :raise IncorrectKbError: if the structure of the tuning_kb is not correct
        """
        try:
            if self.module is None:
                raise AttributeError()

            if self.module in tuning_kb:
                if 'params' in tuning_kb[self.module]:
                    if self.name in tuning_kb[self.module]['params']:
                        return tuning_kb[self.module]['params'][self.name]
                    raise IncorrectKbError(f'Missing param tuning data for param: {self.name}; module: {self.module}')
                raise IncorrectKbError(f'Missing params tuning data for module: {self.module}')
            raise IncorrectKbError(f'Missing module tuning data: {self.module}')

        except AttributeError:
            error = MissingModuleNameError(self.name)
            logging.getLogger(__name__).error(error)
            raise error

    @property
    def is_highlighted(self):
        try:
            return self._highlighted
        except AttributeError:
            return False

    @is_highlighted.setter
    def is_highlighted(self, value):
        self._highlighted = value

    def to_json(self):
        return {
            'name': self.name,
            'pretty_name': self.pretty_name,
            'value': self.value,
            'min': self.min_v,
            'max': self.max_v,
            'default': self.default_value,
            'description': self.description,
            'is_highlighted': self.is_highlighted,
            'type': self.v_type
        }

    def __repr__(self) -> str:
        return str(self.to_json())

    @classmethod
    def reverse_pretty(cls, pretty: str, pipeline: Pipeline):
        """Returns the first IRPar that has `pretty` as its `name` or `pretty_name` and its IROp (IROpOptions).
        If none is found this returns None."""
        for module in pipeline:
            for param in module.parameters.values():
                if param.name == pretty or param.pretty_name == pretty:
                    return param, module
        return None, None


def update_pipeline(pipeline: Pipeline, relevant_params: List[Tuple[str, str]]) -> Pipeline:
    """Updates the highlight property for this pipeline, relevant parameters must be as `module.parameter`."""
    data = {}
    logging.getLogger(__name__).debug("Relevant parameters: %s", relevant_params)
    for param in relevant_params:
        if param[0] in data:
            data[param[0]].append(param[1])
        else:
            data[param[0]] = [param[1]]

    for module in pipeline:
        if module.name in data:
            module.is_highlighted = True
            module.should_change = ('wrong_module' in data[module.name])
            for p_key in module.get_parameters_list():
                param = module.get_param(p_key)
                param.is_highlighted = (param.name in data[module.name])
        else:
            module.is_highlighted = False
            module.should_change = False
            for p in module.parameters.values():
                p.is_highlighted = False

    return pipeline
