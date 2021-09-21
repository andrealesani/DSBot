from abc import abstractmethod

import numpy as np
from sklearn.decomposition import PCA

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRPar


class IRFeatureEngineering(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRFeatureEngineering, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        self.parameter_tune(result)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,v.value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result):
        print('pca', result['original_dataset'])
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset']
        if not self._param_setted:
            self.set_model(dataset)
        try:
            transformed_ds = self._model.fit_transform(dataset.values)
        except:
            transformed_ds = self._model.fit_transform(dataset.values)
        self.transformed_ds = transformed_ds
        if 'transformed_ds' not in result:
            result['transformed_ds'] = self.transformed_ds
        return result

class IRPCA(IRFeatureEngineering):
    def __init__(self):
        super(IRPCA, self).__init__("pca",
                                    [IRPar("n_components", 2, "float", 0, 10, 0.1)],  # TODO: what are minimum and maximum?
                                    PCA)

    def parameter_tune(self, dataset):
        pass

class IRPCA2(IRFeatureEngineering):
    def __init__(self):
        super(IRPCA2, self).__init__("pca2",
                                    [IRPar("n_components", 2, "float", 0, 10, 0.1)],  # TODO: what are minimum and maximum?
                                    PCA)

    def parameter_tune(self, dataset):
        pass

class IRGenericFeatureEngineering(IROpOptions):
    def __init__(self):
        super(IRGenericFeatureEngineering, self).__init__([IRPCA(), IRPCA2()], "pca")
