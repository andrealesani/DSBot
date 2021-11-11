from abc import abstractmethod

import numpy as np
import pandas as pd
from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar
from ir.modules.laplace import Laplace
from sklearn.feature_selection import VarianceThreshold

class IRFeatureSelection(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRFeatureSelection, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, dataset):
        self.parameter_tune(dataset)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,v.value)
        #self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
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

class IRVarianceThreshold(IRFeatureSelection):
    def __init__(self):
        super(IRVarianceThreshold, self).__init__("varianceThreshold",
                                                  [IRNumPar('threshold', 0, "float", 0, 10, 0.1)],  # TODO: what are minimum and maximum?
                                                  VarianceThreshold)

    def parameter_tune(self, dataset):
        self.parameters['threshold'].max_v=dataset.std().max()


class IRLaplace(IRFeatureSelection):
    def __init__(self):
        super(IRLaplace, self).__init__("laplace",
                                        [IRNumPar('percentage', 1, "float", 0, 1, 0.05)],  # TODO: what are minimum and maximum?
                                        Laplace)

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        print('param', self.parameters)
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        #if not self._param_setted:
        self.set_model(dataset)
        try:
            transformed_ds = self._model.fit_transform(dataset.values)
        except:
            transformed_ds = self._model.fit_transform(dataset.values)
        self.transformed_ds = transformed_ds
        if 'transformed_ds' not in result:
            result['transformed_ds'] = self.transformed_ds
            print('laplace' , result['transformed_ds'].shape)

        return result



class IRGenericFeatureSelection(IROpOptions):
    def __init__(self):
        super(IRGenericFeatureSelection, self).__init__([IRVarianceThreshold(), IRLaplace()], "varianceThreshold")


class IRFeatureImportanceOp(IROp):
    def __init__(self, name, parameters, model=None):
        super(IRFeatureImportanceOp, self).__init__(name, parameters)
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

        self.parameter_tune(result, dataset, labels)
        for p, v in self.parameters.items():
            self._model.__setattr__(p, self.parameters[p].value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    def run(self, result, session_id):
        pass


class IRFeatureImportance(IRFeatureImportanceOp):
    def __init__(self):
        super(IRFeatureImportance, self).__init__("featureImportance",
                                                     [], VarianceThreshold)
        self._param_setted = False

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        try:
            fi = result['classifier'].feature_importances_
        except:
            fi = np.array(len(dataset.columns))
        d = {'Cols': dataset.columns, 'FI': fi}
        df = pd.DataFrame(d)
        df = df.sort_values(by='FI', ascending=0)
        result['feature_importance'] = df
        print('featIMp')
        return result

class IRGenericFeatureImportance(IROpOptions):
    def __init__(self):
        super(IRGenericFeatureImportance, self).__init__(
            [IRFeatureImportance()],
            "featureImportance")