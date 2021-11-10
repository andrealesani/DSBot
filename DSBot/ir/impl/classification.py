from abc import abstractmethod

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar

from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split, KFold
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

        print('PARAMETERSSSS', self.parameters)

        result['predicted_labels'] = []
        result['y_score'] = []
        for x_train, x_test, y_train,y_test in zip(result['x_train'],result['x_test'],result['y_train'],result['y_test']):
            try:
                result['predicted_labels'].append(list(self._model.fit(x_train, y_train).predict(x_test)))
                result['y_score'].append(self._model.predict_proba(x_test))
            except:
                result['predicted_labels'].append(list(self._model.fit(x_train, y_train).predict(x_test)))

        result['original_dataset'].measures.update({p: self.parameters[p].value for p, v in self.parameters.items()})
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
        # Number of trees in random forest
        n_estimators = [int(x) for x in np.linspace(start=self.parameters['n_estimators'].min_v, stop=self.parameters['n_estimators'].max_v, num=self.parameters['n_estimators'].step)]
        # Number of features to consider at every split
        #max_features = ['auto', 'sqrt']
        # Maximum number of levels in tree
        max_depth = [int(x) for x in np.linspace(self.parameters['max_depth'].min_v, self.parameters['max_depth'].max_v, num=self.parameters['max_depth'].step)]
        max_depth.append(None)
        # Minimum number of samples required to split a node
        min_samples_split = np.arange(self.parameters['min_samples_split'].min_v, self.parameters['min_samples_split'].max_v, self.parameters['min_samples_split'].step)
        # Minimum number of samples required at each leaf node
        min_samples_leaf = np.arange(self.parameters['min_samples_leaf'].min_v, self.parameters['min_samples_leaf'].max_v, self.parameters['min_samples_leaf'].step)
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
        best_param = {}
        for x_train, y_train in zip(result['x_train'], result['y_train']):
            # Random search of parameters, using 3 fold cross validation,
            # search across 100 different combinations, and use all available cores
            rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, cv=3, verbose=2, random_state=42, n_jobs=-1)
            # Fit the random search model
            rf_random.fit(x_train, y_train)
            for k,v in rf_random.best_params_.items():
                if k in best_param:
                    best_param[k].append(v)
                else:
                    best_param[k] = [v]

        for k in rf_random.best_params_:
            if self.parameters[k].v_type == "int":
                self.parameters[k].value = int(np.median(best_param[k]))
            elif self.parameters[k].v_type == "float":
                self.parameters[k].value = np.median(best_param[k])
            elif self.parameters[k].v_type == "str":
                c = Counter(best_param[k])
                self.parameters[k].value = c.most_common(1)[0][0]
        return self.parameters


class IRLogisticRegression(IRClassification):
    def __init__(self):
        super(IRLogisticRegression, self).__init__("logisticRegression",
                                                   [IRNumPar("max_iter", 100, "int", 100, 1000, 10)],  # TODO: if I want to pass a list of values?
                                                   LogisticRegression)
        self._param_setted = False

    def parameter_tune(self, dataset, labels):
        max_iter = [int(x) for x in np.linspace(self.parameters['max_iter'].min_v, self.parameters['max_iter'].max_v, num=self.parameters['max_iter'].step)]

        random_grid = {'max_iter': max_iter}


        # Use the random grid to search for best hyperparameters
        # First create the base model to tune
        lr = LogisticRegression()
        # Random search of parameters, using 3 fold cross validation,
        # search across 100 different combinations, and use all available cores
        lr_random = RandomizedSearchCV(estimator=lr, param_distributions=random_grid, n_iter=100, cv=3, verbose=2,
                                       random_state=42, n_jobs=-1)
        print('ds', dataset)
        print('labels', labels)
        # Fit the random search model
        print(dataset.shape)
        print(labels.shape)
        print(set(labels.values))
        lr_random.fit(dataset, labels.values)
        print(lr_random.best_params_.items)
        for k in lr_random.best_params_:
            self.parameters[k].value = lr_random.best_params_[k]
        return self.parameters

class IRGenericClassification(IROpOptions):
    def __init__(self):
        super(IRGenericClassification, self).__init__([IRRandomForest(), IRLogisticRegression()], "randomForest")