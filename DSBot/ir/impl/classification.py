from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar, IRCatPar

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold

from collections import Counter
import numpy as np


class IRClassification(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRClassification, self).__init__(name,parameters)
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
        for p,v in self.parameters.items():
            self._model.__setattr__(p,self.parameters[p].value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    def run(self, result, session_id):

        if not self._param_setted:
            self.set_model(result)

        result['predicted_labels'] = []
        result['y_score'] = []
        result['feat_imp'] = []

        for x_train, x_test, y_train,y_test in zip(result['x_train'],result['x_test'],result['y_train'],result['y_test']):
            result['predicted_labels'] += list(self._model.fit(x_train, y_train).predict(x_test))
            result['y_score'] += list(self._model.predict_proba(x_test))
        result['classifier'] = self._model
        self._param_setted = False
        return result

class IRRandomForest(IRClassification):
    def __init__(self):
        super(IRRandomForest, self).__init__("randomForest",
                                             [IRNumPar("n_estimators", 100, "int", 100, 150, 10),  # TODO: what is the maximum? Which first value give?
                                              IRNumPar("max_depth", 10, "int", 10, 22, 11),  # TODO: what is the maximum?
                                              IRNumPar("min_samples_split", 2, "int", 2, 9, 3),
                                              IRNumPar("min_samples_leaf", 1, "int", 1, 5, 1)],  # TODO: if I want to pass a list of values?
                                             RandomForestClassifier)
        self._param_setted = False

    def parameter_tune(self, result, dataset, labels):
        random_grid = {p:np.arange(d.min_v, d.max_v, d.step) for p,d in self.parameters.items()}
        rf_random = RandomizedSearchCV(estimator=self._model, param_distributions=random_grid, verbose=2, n_jobs=-1, cv=KFold(5, shuffle=True))
        rf_random.fit(dataset, labels)
        for k,v in rf_random.best_params_.items():
            self.parameters[k].value = v


class IRLogisticRegression(IRClassification):
    def __init__(self):
        super(IRLogisticRegression, self).__init__("logisticRegression",
                                                   [IRNumPar("max_iter", 100, "int", 100, 1000, 100),
                                                    IRCatPar("penalty", "l2", ["l1","l2","elasticnet","None"])],  # TODO: if I want to pass a list of values?
                                                   LogisticRegression)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        random_grid = {p:np.arange(d.min_v, d.max_v, d.step) for p,d in self.parameters.items() if d.v_type!='categorical'}
        # Random search of parameters, using 5 fold cross validation, search across 100 different combinations, and use all available cores
        lr_random = RandomizedSearchCV(estimator=self._model, param_distributions=random_grid, n_iter=100, cv=KFold(5, shuffle=True), n_jobs=-1)
        lr_random.fit(dataset, labels.values)
        print(lr_random.best_params_.items)
        for k in lr_random.best_params_:
            self.parameters[k].value = lr_random.best_params_[k]
        return self.parameters


class IRKNeighborsClassifier(IRClassification):
    def __init__(self):
        super(IRKNeighborsClassifier, self).__init__("kNeighborsClassifier",
                                                   [IRNumPar("n_neighbors", 5, "int", 2, 10, 1)],  # TODO: if I want to pass a list of values?
                                                   KNeighborsClassifier)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        random_grid = {p:np.arange(d.min_v, d.max_v, d.step) for p,d in self.parameters.items() if d.v_type!='categorical'}
        # Random search of parameters, using 5 fold cross validation, search across 100 different combinations, and use all available cores
        kn_random = RandomizedSearchCV(estimator=self._model, param_distributions=random_grid, n_iter=100, cv=KFold(5, shuffle=True), n_jobs=-1)
        kn_random.fit(dataset, labels.values)
        print(kn_random.best_params_.items)
        for k in kn_random.best_params_:
            self.parameters[k].value = kn_random.best_params_[k]
        return self.parameters


class IRAdaBoostClassifier(IRClassification):
    def __init__(self):
        super(IRAdaBoostClassifier, self).__init__("adaBoostClassifier",
                                                   [IRNumPar("n_estimators", 50, "int", 50, 150, 10)],  # TODO: if I want to pass a list of values?
                                                   AdaBoostClassifier)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        random_grid = {p:np.arange(d.min_v, d.max_v, d.step) for p,d in self.parameters.items() if d.v_type!='categorical'}
        # Random search of parameters, using 5 fold cross validation, search across 100 different combinations, and use all available cores
        kn_random = RandomizedSearchCV(estimator=self._model, param_distributions=random_grid, n_iter=100, cv=KFold(5, shuffle=True), n_jobs=-1)
        kn_random.fit(dataset, labels.values)
        print(kn_random.best_params_.items)
        for k in kn_random.best_params_:
            self.parameters[k].value = kn_random.best_params_[k]
        return self.parameters

class IRGenericClassification(IROpOptions):
    def __init__(self):
        super(IRGenericClassification, self).__init__([IRRandomForest(), IRLogisticRegression(), IRKNeighborsClassifier(), IRAdaBoostClassifier()], "randomForest")



