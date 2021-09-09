import logging

from DSBot.ir.ir_exceptions import IncorrectValue
from DSBot.tuning import TuningParMixin


class IRPar(TuningParMixin, object):
    """Represents a parameter of an operation.

    :ivar name: the name of this
    :ivar value: the initial value of this
    :ivar v_type: the type of this, supported values are `int` and `float`
    :ivar min_v: the minimum value that can be set
    :ivar max_v: the maximum value that can be set
    """

    def __init__(self, name: str, value: float, v_type: str, min_v: float, max_v: float):
        self.name = name
        self.default_value = value
        self.v_type = v_type
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
        """Do not use this method during tuning by the user (use tune_value)."""
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
        """Whether the user has set a custom value during tuning."""
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
