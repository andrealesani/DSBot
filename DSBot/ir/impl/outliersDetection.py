from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
import numpy as np
import pandas as pd


class IROutliersDetection(IROp):
    def __init__(self, name, parameters = None, model = None):
        super(IROutliersDetection, self).__init__(name,parameters if parameters is not None else [])
        if parameters!=None:
            self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        labels = result['labels']
        self.parameter_tune(dataset)
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
        if not self._param_setted:
            self.set_model(result)

        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        if self.__class__.__name__!="IROutliersDetection":
            print('PARAMETERSSSS', self.parameters)
            result['predicted_outliers'] = self._model.fit_predict(dataset)
            mask_outliers = result['predicted_outliers'] == -1
            result['outliers_dataset'] = pd.DataFrame(dataset.values[mask_outliers, :])
            mask = result['predicted_outliers'] != -1
            result['noOutliers_dataset'] = pd.DataFrame(dataset.values[mask, :])
            result['labels'] = mask
            self._param_setted = False
            return result
        else:
            # TODO: è sbagliato, va sistemato
            result = IROneClassSVM().run(result, session_id)
            return result


class IRIsolationForest(IROutliersDetection):
    def __init__(self):
        super(IRIsolationForest, self).__init__("isolationForest",
                                             [IRNumPar("contamination", "auto", "float", 0, 0.5, 0.1)],  # TODO: if I want to pass a list of values?
                                             IsolationForest)
        self._param_setted = False

    def parameter_tune(self, dataset):
        pass

class IRLocalOutlierFactor(IROutliersDetection):
    def __init__(self):
        super(IRLocalOutlierFactor, self).__init__("localOutlierFactor",
                                             [IRNumPar("contamination", "auto", "float", 0, 0.5, 0.1)],  # TODO: if I want to pass a list of values?
                                            LocalOutlierFactor)
        self._param_setted = False

    def parameter_tune(self, dataset):
        pass

class IROneClassSVM(IROutliersDetection):
    def __init__(self):
        super(IROneClassSVM, self).__init__("oneClassSVM",
                                             [IRNumPar("nu", 0.01, "float", 0, 0.5, 0.1)],  # TODO: if I want to pass a list of values?
                                            OneClassSVM)
        self._param_setted = False

    def parameter_tune(self, dataset):
        pass

class IRGenericOutliersDetection(IROpOptions):
    def __init__(self):
        super(IRGenericOutliersDetection, self).__init__([IROutliersDetection('outliersDetection'),IRIsolationForest(), IRLocalOutlierFactor(), IROneClassSVM()], "oneClassSVM")