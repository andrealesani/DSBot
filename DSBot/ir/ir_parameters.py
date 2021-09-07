import logging

from DSBot.tuning import TuningParMixin
from ir.ir_exceptions import IncorrectValue


def par_helper(par_list: list, module_name: str) -> dict:
    """Given a list of IRPar and their module name, returns a dictionary containing the parameters.

    This helps to reduce chances of errors with mismatching dictionary key and parameter name,
    and sets the module attribute for all the parameters.

    The dictionary will have as keys each parameter name.
    The parameters will have the module attribute set to the module name.
    """
    result = {}
    for e in par_list:
        e.module = module_name
        result[e.name] = e
    return result


class IRPar(TuningParMixin):
    def __init__(self, name, value, min_v=0, max_v=1000):
        # TODO(giubots): make range mandatory, add type: int/float
        self.name = name
        self.default_value = value
        self.min_v = min_v
        self.max_v = max_v
        self._actual_value = None

    @property
    def value(self):
        if self._actual_value is None:
            return self.default_value
        return self._actual_value

    @value.setter
    def value(self, new_value):
        """Do not use this method during tuning (use tune_value)."""
        if self._actual_value is not None:
            logging.getLogger(__name__).debug('Parameter set was ignored because a custom value was defined')
            return

        if not self.is_range_valid(new_value):
            logging.getLogger(__name__).error('Out of range parameter: %s; module: %s', self.name, self.module)
            return

        self.default_value = new_value

    @value.deleter
    def value(self):
        self._actual_value = None

    @property
    def is_custom(self):
        return self._actual_value is not None

    def tune_value(self, new_value):
        """Do not use this method from within the pipeline, use the value setter."""
        if not self.is_range_valid(new_value):
            raise IncorrectValue()

        self._actual_value = new_value

    def is_range_valid(self, new_value):
        return self.max_v >= new_value >= self.min_v

    def __str__(self):
        return f'{self.name} = {self.value}'
