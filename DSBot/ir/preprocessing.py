from abc import abstractmethod

import pandas as pd
from sklearn.impute import IterativeImputer

from ir.ir_operations import IROp, IROpOptions


class IRPreprocessing(IROp):
    def __init__(self, name, parameters=None, model = None):
        super(IRPreprocessing, self).__init__(name, parameters if parameters is not None else [])
        self.parameter = parameters['value']  # FIXME: use self.get_param('value'), but it will raise UnknownParameter
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        dataset = result['original_dataset']
        if self.parameter == None:
            self.parameter_tune(dataset)
        #for p,v in self.parameters.items():
        #    self._model.__setattr__(p,v.value)
        self._param_setted = True

    #TDB cosa deve restituire questa funzione?
    def run(self, result):
        pass

class IRMissingValuesRemove(IRPreprocessing):
    def __init__(self):
        super(IRMissingValuesRemove, self).__init__("missingValuesRemove")

    def run(self, result):
        dataset = result['original_dataset']
        dataset = dataset.ds.dropna()
        result['new_dataset'] = dataset
        return result

class IRMissingValuesFill(IRPreprocessing):
    def __init__(self, parameter):
        super(IRMissingValuesFill, self).__init__("missingValuesFill", parameter)

    def parameter_tune(self, dataset):
        imp = IterativeImputer(max_iter=10, random_state=0)
        if len(dataset.col) > 0:
            values_col = dataset.ds.columns.difference(dataset.col)
            values_dataset = pd.DataFrame(imp.fit_transform(dataset.ds[values_col]))
            values_dataset.columns = values_col
            dataset.ds = dataset.ds.apply(lambda col: col.fillna(col.value_counts().index[0]))
            values_dataset = pd.concat([dataset.ds, values_dataset])
        else:
            values_dataset = pd.DataFrame(imp.fit_transform(dataset.ds))
        return values_dataset

    def run(self, result):
        dataset = result['original_dataset']
        if not self._param_setted:
            self.parameter_tune(dataset)
        else:
            dataset.ds = dataset.ds.apply(lambda col: col.fillna(self.parameter))
        result['new_dataset'] = dataset
        return result

def IROneHotEncode(IRPreprocessing):
    def __init__(self, parameter):
        super(IROneHotEncode, self).__init__("oneHotEncoder", parameter)

class IRGenericPreprocessing(IROpOptions):
    def __init__(self):
        super(IRGenericPreprocessing, self).__init__([IRMissingValuesRemove(), IRMissingValuesFill([])],
                                                     "missingValuesRemove")
