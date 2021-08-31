import json

import logging

# Load the tuning kb data from file.
with open("tuning_kb.json", "r") as tuning_kb_file:
    print("reading tuning kb file")  # TODO(giubots): remove
    tuning_kb = json.loads(tuning_kb_file.read())


class TuningOpMixin:
    """Adds tuning functionalities to a IROp class."""

    @property
    def pretty_name(self):
        """Returns the printable name of this IROp, `self.name` if not found."""

        if self.name in tuning_kb and "name" in tuning_kb[self.name]:
            return tuning_kb[self.name]["name"]
        logging.getLogger(__name__).warning("missing pretty name for module: %s", self.name)
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
            "name": self.name,
            "pretty_name": self.pretty_name,
            "parameters": {k: v.to_json() for k, v in self.parameters},
            "is_highlighted": self.is_highlighted
        }


class TuningOpOptionsMixin:
    """Adds tuning functionalities to a IROpOptions class."""

    def to_json(self):
        actual = self.actual_model.to_json()
        actual["models"] = {k: v.to_json() for k, v in self.models}
        return actual


class TuningParMixin:
    """Adds tuning functionalities to a IRPar class."""

    @property
    def pretty_name(self):
        """Returns the printable name of this IRPar, `self.name` if not found."""

        param = self._get_param_data()

        if param is not None and "name" in param:
            return param["name"]
        logging.getLogger(__name__).warning("missing pretty name for param: %s", self.name)
        return self.name

    @property
    def description(self):
        """Returns the description of this IRPar, an empty string if not found."""

        param = self._get_param_data()

        if param is not None and "desc" in param:
            return param["desc"]
        logging.getLogger(__name__).warning("missing description for param: %s", self.name)
        return ""

    def _get_param_data(self):
        if self.module is None:
            error = f"missing module name for parameter: {self.name}." \
                    f"Check if its module is calling super.__init__(...)"
            logging.getLogger(__name__).exception(error)
            raise Exception(error)

        if self.module in tuning_kb \
                and "params" in tuning_kb[self.module] \
                and self.name in tuning_kb[self.module]["params"]:
            return tuning_kb[self.module]["params"][self.name]
        return None

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
            "name": self.name,
            "pretty_name": self.pretty_name,
            "value": self.value,
            "min": self.min_v,
            "max": self.max_v,
            "default": self.default_value,
            "description": self.description,
            "is_highlighted": self.is_highlighted,
        }
