from abc import abstractmethod

import pandas as pd
import numpy as np
from sklearn.impute._iterative import IterativeImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from pandas.api.types import is_numeric_dtype
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

class IRMissingValuesHandle(IROp):
    def __init__(self, name, parameters=None, model = None):
        super(IRMissingValuesHandle, self).__init__(name, parameters if parameters is not None else [])
        #self.parameter = parameters['value']  # FIXME: use self.get_param('value'), but it will raise UnknownParameter
        self.labels = None


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
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        if len(dataset)>100:
            if (dataset.isna().sum(axis=1)>0).sum()>0.05*len(dataset):
                result = IRMissingValuesRemove().run(result, session_id)
            else:
                result = IRMissingValuesFill().run(result, session_id)
        return result


class IRMissingValuesRemove(IRMissingValuesHandle):
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
        print('missingvalremove', dataset.shape)
        print(dataset.head())
        return result

class IRMissingValuesFill(IRMissingValuesHandle):
    def __init__(self):
        super(IRMissingValuesFill, self).__init__("missingValuesFill")

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        imp = IterativeImputer(max_iter=10, random_state=0)
        if len(result['original_dataset'].cat_cols) > 0:
            values_col = dataset.columns.difference(result['original_dataset'].cat_cols)
            if len(values_col)>0:
                values_dataset = pd.DataFrame(imp.fit_transform(dataset[values_col]))
                values_dataset.columns = values_col
                cat_dataset = dataset[result['original_dataset'].cat_cols].apply(lambda col: col.fillna(col.value_counts().index[0]))
                dataset = pd.concat([cat_dataset, values_dataset],axis=1)
            else:
                cat_dataset = dataset[result['original_dataset'].cat_cols].apply(
                    lambda col: col.fillna(col.value_counts().index[0]))
                dataset = cat_dataset
        else:
            dataset = pd.DataFrame(imp.fit_transform(dataset))

        #dataset = dataset.apply(lambda col: col.fillna(self.parameter))
        result['new_dataset'] = dataset
        print('missingvalfill', dataset.shape)

        return result

class IRGenericMissingValues(IROpOptions):
    def __init__(self):
        super(IRGenericMissingValues, self).__init__([IRMissingValuesHandle('missingValuesHandle'), IRMissingValuesRemove(), IRMissingValuesFill()],
                                                     "missingValuesHandle")


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
        print('onehotencode', dataset.shape)
        return result


class IRLabelRemove(IRPreprocessing):

    def __init__(self):
        super(IRLabelRemove, self).__init__("labelRemove")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id):
        label = result['labels']
        #print('labels', label.shape)
        if 'new_dataset' in result:
            dataset = result['new_dataset']
            dataset = dataset.drop(label, axis=1)
            print(dataset.shape)
            label = result['new_dataset'][label]
            print(len(dataset))
            print(len(label))

            if len(dataset)<len(label):
                label = label[set(dataset.index.values)]
                print('hola',len(label))

        else:

            dataset = result['original_dataset'].ds
            print(dataset.shape)
            dataset = dataset.drop(label, axis=1)
            label = result['original_dataset'].ds[label]
        #if not is_numeric_dtype(label):
        #    label = pd.get_dummies(label)
        #label = label.dropna()
        label = LabelEncoder().fit_transform(label)

        #result['new_dataset'] = dataset.T[set(label.index.values)].T
        result['labels']=label
        result['new_dataset'] = dataset


        #columns=list(set(dataset.columns) - set(label))
        #result['new_dataset'] = dataset[columns]
        return result

class IROutliersRemove(IRPreprocessing):
    def __init__(self):
        super(IROutliersRemove, self).__init__("outliersRemove")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        dataset = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        #df = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        df = dataset.T
        mean = df.mean()
        std = df.std()
        print(df.index)
        print(df.columns)
        ds = df[(np.abs(df - mean) <= (5 * std)).all(axis=1)].T
        if ds.shape[1]!=0 and ds.shape[0]!=0:
            print('len', ds.shape)
            result['new_dataset'] = ds

        return result

class IRStandardization(IRPreprocessing):
    def __init__(self):
        super(IRStandardization, self).__init__("standardization")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
            dataset = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        #df = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)

        result['new_dataset'] = pd.DataFrame(StandardScaler().fit_transform(dataset))
        return result

class IRNormalization(IRPreprocessing):
    def __init__(self):
        super(IRNormalization, self).__init__("normalization")

    def parameter_tune(self, dataset):
        # TODO: implement
        pass

    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
            dataset = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)
        #df = dataset.drop(list(result['original_dataset'].cat_cols), axis=1)

        result['new_dataset'] = pd.DataFrame(MinMaxScaler().fit_transform(dataset))
        return result

class IRGenericPreprocessing(IROpOptions):
    def __init__(self):
        super(IRGenericPreprocessing, self).__init__([IRLabelRemove(), IROneHotEncode(), IROutliersRemove(), IRStandardization(), IRNormalization()],
                                                     "labelRemove")

