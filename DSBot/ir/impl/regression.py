from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, KFold
import numpy as np


class IRRegression(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRRegression, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels']
        self.parameter_tune(dataset, labels)
        for p,v in self.parameters.items():
            print(p,v)
            self._model.__setattr__(p,self.parameters[p].value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        print(self._param_setted)
        if not self._param_setted:
            self.set_model(result)

        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels']
        print('PARAMETERSSSS', self.parameters)
        predicted = []
        kf = KFold(n_splits=4)
        result['predicted_labels'] = []
        result['y_test'] = []
        result['y_score'] = []
        for train_index, test_index in kf.split(dataset):
            train_features, test_features = dataset.values[train_index], dataset.values[test_index]
            train_labels, test_labels = labels.values[train_index], labels.values[test_index]
            try:
                #print((self._model.fit(train_features, train_labels).predict(test_features)))
                #self._model.fit(train_features, train_labels)
                predicted += list(self._model.fit(train_features, train_labels).predict(test_features))
            except:
                predicted += list(self._model.fit(train_features, train_labels).predict(test_features))
        #y_score = self._model.predict_proba(test_features)

        result['predicted_labels'].append(predicted)
        result['y_test']= test_labels
        result['original_dataset'].measures.update({p:self.parameters[p].value for p,v in self.parameters.items()})
        return result



class IRLinearRegression(IRRegression):
    def __init__(self):
        super(IRLinearRegression, self).__init__("linearRegression",
                                             [],  # TODO: if I want to pass a list of values?
                                             LinearRegression)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        pass



class IRGenericRegression(IROpOptions):
    def __init__(self):
        super(IRGenericRegression, self).__init__([IRLinearRegression()], "linearRegression")