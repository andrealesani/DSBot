from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, KFold
import numpy as np


class IRCrossValidation(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRCrossValidation, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels']
        for p,v in self.parameters.items():
            print(p,v)
            self._model.__setattr__(p,self.parameters[p].value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels


    def run(self, result, session_id):
        pass


class IRTrainTest(IRCrossValidation):
    def __init__(self):
        super(IRTrainTest, self).__init__("trainTest",
                                             [IRNumPar("test_size", 0.4, "float", 0.1, 0.9, 0.1)],  # TODO: if I want to pass a list of values?
                                             train_test_split)
        self._param_setted = False

    def parameter_tune(self, dataset):
        pass


    def run(self, result, session_id):
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels']
        result['x_train'] = []
        result['x_test'] = []
        result['y_train'] = []
        result['y_test'] = []

        x_train, x_test, y_train, y_test = self._model(dataset, labels, self.parameters['test_size'].value)
        result['x_train'].append(x_train)
        result['x_test'].append(x_test)
        result['y_train'].append(y_train)
        result['y_test'].append(y_test)
        return result

class IRKFold(IRCrossValidation):
    def __init__(self):
        super(IRKFold, self).__init__("kFold",[IRNumPar("n_splits", 2, "int", 2, 10, 1)],  # TODO: if I want to pass a list of values?
                                      KFold)
        self._param_setted = False

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if not self._param_setted:
            self.set_model(result)

        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        labels = result['labels']

        print('PARAMETERSSSS', self.parameters)
        cv = self._model
        result['x_train'] = []
        result['x_test'] = []
        result['y_train'] = []
        result['y_test'] = []
        for train_index, test_index in cv.split(dataset):
            result['x_train'].append(dataset.values[train_index])
            result['x_test'].append(dataset.values[test_index])
            result['y_train'].append(labels[train_index])
            result['y_test'].append(labels[test_index])
        return result

class IRGenericCrossValidation(IROpOptions):
    def __init__(self):
        super(IRGenericCrossValidation, self).__init__([IRKFold()], "kFold")