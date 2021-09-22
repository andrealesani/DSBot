from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRPar

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np


class IRClassification(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRClassification, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    @abstractmethod
    def train_test(self, dataset):
        pass

    def set_model(self, result):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset']
        self.parameter_tune(dataset)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,v.value)
        self._param_setted = True

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
        labels = result['labels']
        self.train_features, self.test_features, self.train_labels, self.test_labels = self.train_test(dataset, labels)
        if not self._param_setted:
            self.set_model(dataset)
        try:
            self._model.fit_predict(dataset.ds.values)
        except:
            self._model.fit_predict(dataset)
        return result



class IRRandomForest(IRClassification):
    def __init__(self):
        super(IRRandomForest, self).__init__("randomForest",
                                       [IRPar("n_estimators", 100, "int", 100, 2000, 10),  # TODO: what is the maximum? Which first value give?
                                        IRPar("max_depth", 10, "int", 10, 110, 11),  # TODO: what is the maximum?
                                        IRPar("min_samples_split", 2, "int", 2, 10, 3),
                                        IRPar("min_samples_leaf", 1, "int", 1, 4, 1)],  # TODO: if I want to pass a list of values?
                                       RandomForestClassifier)

    def train_test(self, dataset, labels):
        train_features, test_features, train_labels, test_labels = train_test_split(dataset, labels,
                                                                                    test_size=0.25, random_state=42)
        return train_features, test_features, train_labels, test_labels

    def parameter_tune(self, dataset):
        # Number of trees in random forest
        n_estimators = [int(x) for x in np.linspace(start=100, stop=2000, num=10)]
        # Number of features to consider at every split
        #max_features = ['auto', 'sqrt']
        # Maximum number of levels in tree
        max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
        max_depth.append(None)
        # Minimum number of samples required to split a node
        min_samples_split = [2, 5, 10]
        # Minimum number of samples required at each leaf node
        min_samples_leaf = [1, 2, 4]
        # Method of selecting samples for training each tree
        #bootstrap = [True, False]
        # Create the random grid
        random_grid = {'n_estimators': n_estimators,
                       'max_depth': max_depth,
                       'min_samples_split': min_samples_split,
                       'min_samples_leaf': min_samples_leaf}


        # Use the random grid to search for best hyperparameters
        # First create the base model to tune
        rf = RandomForestClassifier()
        # Random search of parameters, using 3 fold cross validation,
        # search across 100 different combinations, and use all available cores
        rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=100, cv=3, verbose=2,
                                       random_state=42, n_jobs=-1)
        # Fit the random search model
        rf_random.fit(self.train_features, self.train_labels)
        for k,v in rf_random:
            self.parameters[k] = v
        return self.parameters

class IRGenericClassification(IROpOptions):
    def __init__(self):
        super(IRGenericClassification, self).__init__([IRRandomForest()], "randomForest")