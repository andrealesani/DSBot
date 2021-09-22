from abc import abstractmethod

import pandas as pd
from sklearn.impute._iterative import IterativeImputer

from ir.ir_operations import IROp, IROpOptions


class IRPreprocessing(IROp):
    def __init__(self, name, parameters=None, model = None):
        super(IRPreprocessing, self).__init__(name, parameters if parameters is not None else [])
        #self.parameter = parameters['value']  # FIXME: use self.get_param('value'), but it will raise UnknownParameter
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        if self.parameter == None:
            self.parameter_tune(dataset)
        #for p,v in self.parameters.items():
        #    self._model.__setattr__(p,v.value)
        self._param_setted = True

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        pass

class IRMissingValuesRemove(IRPreprocessing):
    def __init__(self):
        super(IRMissingValuesRemove, self).__init__("missingValuesRemove")


    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        dataset = dataset.dropna()
        result['new_dataset'] = dataset
        print('missingvalremove')
        return result

class IRMissingValuesFill(IRPreprocessing):
    def __init__(self, parameter):
        super(IRMissingValuesFill, self).__init__("missingValuesFill", parameter)

    def parameter_tune(self, dataset):
        imp = IterativeImputer(max_iter=10, random_state=0)
        if len(dataset.col) > 0:
            values_col = dataset.columns.difference(dataset.col)
            values_dataset = pd.DataFrame(imp.fit_transform(dataset[values_col]))
            values_dataset.columns = values_col
            dataset = dataset.apply(lambda col: col.fillna(col.value_counts().index[0]))
            values_dataset = pd.concat([dataset, values_dataset])
        else:
            values_dataset = pd.DataFrame(imp.fit_transform(dataset))
        return values_dataset

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        if not self._param_setted:
            self.parameter_tune(dataset)
        else:
            dataset = dataset.apply(lambda col: col.fillna(self.parameter))
        result['new_dataset'] = dataset
        print('missingvalfill')

        return result

class IROneHotEncode(IRPreprocessing):
    def __init__(self):
        super(IROneHotEncode, self).__init__("oneHotEncode")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        cols = dataset.columns
        num_cols = dataset._get_numeric_data().columns
        dataset = pd.get_dummies(dataset, columns=list(set(cols) - set(num_cols)))
        result['new_dataset'] = dataset
        print('onehotencode')
        return result


class IRLabelRemove(IRPreprocessing):

    def __init__(self):
        super(IRLabelRemove, self).__init__("labelRemove")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        label = result['labels']
        columns=list(set(dataset.columns) - set(label))
        result['new_dataset'] = dataset[columns]
        return result

class IRGenericPreprocessing(IROpOptions):
    def __init__(self):
        super(IRGenericPreprocessing, self).__init__([IRMissingValuesRemove(), IRMissingValuesFill([]), IRLabelRemove(), IROneHotEncode()],
                                                     "missingValuesRemove")
