from abc import abstractmethod

import pandas as pd
from sklearn.impute import IterativeImputer

from ir.ir_models import IRMod
from ir.ir_operations import IROp, IROpOptions


class IRPreprocessing(IROp):
    def __init__(self, name, parameters=None, model = None):
        super(IRPreprocessing, self).__init__(name, parameters)
        self.parameter = parameters['value']
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, dataset):
        if self.parameter == None:
            self.parameter_tune(dataset)
        #for p,v in self.parameters.items():
        #    self._model.__setattr__(p,v.value)
        self._param_setted = True

    #TDB cosa deve restituire questa funzione?
    def run(self, dataset):
        pass

class IRMissingValuesRemove(IROp):
    def __init__(self):
        super(IRMissingValuesRemove, self).__init__("missingValuesRemove", None)

    def run(self, dataset):
        dataset = dataset.ds.dropna()
        return dataset

class IRMissingValuesFill(IROp):
    def __init__(self, parameter):
        super(IRMissingValuesFill, self).__init__("missingValuesRemove", parameter)


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

    def run(self, dataset):
        if not self._param_setted:
            self.parameter_tune(dataset)
        else:
            dataset.ds = dataset.ds.apply(lambda col: col.fillna(self.parameter))
        return dataset

def IROneHotEncode(IROp):
    def __init__(self, parameter):
        super(IROneHotEncode, self).__init__("oneHotEncoder", parameter)


class IRGenericPreprocessing(IROpOptions):
    def __init__(self):
        super(IRGenericPreprocessing, self).__init__({"missingValuesRemove":IRMod("missingValuesRemove", IRMissingValuesRemove(), "missing values removal"),
                                                  "missingValuesFill":IRMod("missingValuesFill", IRMissingValuesFill(), "missing values fill")},
                                                 "missingValuesRemove")