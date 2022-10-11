import logging
from abc import ABC, abstractmethod

from ir.ir_exceptions import IncorrectValue
from tuning import TuningParMixin

class IRPar(TuningParMixin, ABC):
    """Represents a parameter of an operation.

    The attribute `value` represents the current value of this parameter, it can be the one set in the constructor, it
    can be a value set during the pipeline execution (with parameter.value = new_value), or it can be a value set by
    the user (with parameter.tune_value(user_value).

    Whether the user changed the value of this parameter or not, `default_value` will contain the value set in the
    constructor or automatically by the pipeline during the execution.

    :ivar name: the name of this parameter
    :ivar value: the actual value of this parameter
    :ivar default_value: the value of this parameter set by the pipeline
    :ivar v_type: the type of this parameter
    """

    def __init__(self, name: str, value, v_type: str):
        """Represents a parameter of an operation.

        :param name: the name of this parameter
        :param value: the initial value of this parameter
        :param v_type: the type of this parameter, supported values are `int`, `float`, `categorical`
        """
        self.name = name
        self.default_value = value
        self.v_type = v_type
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

        if not self.is_valid(new_value):
            logging.getLogger(__name__).error('Wrong parameter: %s; module: %s', self.name, self.module)
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
        """Method to apply a value chosen by the user."""
        if not self.is_valid(new_value):
            raise IncorrectValue()

        self._actual_value = new_value

    @abstractmethod
    def is_valid(self, new_value) -> bool:
        """Whether `new_value` is valid according to `v_type`."""
        pass

    def __str__(self):
        return f'{self.name} = {self.value}'


class IRCatPar(IRPar):
    """Represents a categorical parameter of an operation.

    :ivar possible_val: the possible values that can have
    """

    def __init__(self, name: str, value: str, possible_val: list):
        """Represents a categorical parameter of an operation.

        :param name: the name of this parameter
        :param value: the initial value of this parameter
        :param possible_val: the possible values that can have
        """
        super().__init__(name, value, 'categorical')
        self.possible_val = possible_val

    def is_valid(self, new_value):
        return new_value in self.possible_val


    @IRPar.value.setter
    def value(self, new_value):
        IRPar.value.fset(self, new_value)


class IRNumPar(IRPar):
    """Represents a numeric parameter of an operation.

    :ivar min_v: the minimum value that can be set
    :ivar max_v: the maximum value that can be set
    :ivar step: the granularity of the value
    """

    def __init__(self, name: str, value: float, v_type: str, min_v: float = 1, max_v: float = 10, step: float = 1):
        """Represents a numeric parameter of an operation.

        :param name: the name of this parameter
        :param value: the initial value of this parameter
        :param v_type: the type of this parameter, supported values are `int` and `float`
        :param min_v: the minimum value that can be set
        :param max_v: the maximum value that can be set
        :param step: the granularity of the value
        """
        #assert min_v <= value <= max_v, 'The value must be inside the min_v max_v range'
        super().__init__(name, value, v_type)
        self.min_v = min_v
        self.max_v = max_v
        self.step = step

    @IRPar.value.setter
    def value(self, new_value):
        IRPar.value.fset(self, self.uniform_type(new_value))

    def is_valid(self, new_value):
        return self.max_v >= new_value >= self.min_v

    def uniform_type(self, new_value):
        if self.v_type == 'int':
            if type(new_value) != int:
                logging.getLogger(__name__).warning('Explicit int cast of param: %s; module: %s',
                                                    self.name, self.module)
                new_value = int(new_value)
        elif self.v_type == 'float':
            if type(new_value) != float:
                logging.getLogger(__name__).warning('Explicit float cast of param: %s; module: %s',
                                                    self.name, self.module)
                new_value = float(new_value)
        else:
            logging.getLogger(__name__).critical('Unexpected type: %s; param: %s; module: %s',
                                                 self.v_type, self.name, self.module)
        return new_value
