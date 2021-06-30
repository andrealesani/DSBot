import importlib
from abc import ABC, abstractmethod
from sklearn import metrics
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.model_selection import GridSearchCV
import numpy as np

class IROp(ABC):
    def __init__(self, type = str, name = str):
        self.type = type
        self.name = name

    def get_algorithm(self):
        return self.name

    def set_algorithm(self, algorithm):
        self.name = algorithm
        return self.name

    @abstractmethod
    def get_parameters(self):
        pass

    @abstractmethod
    def set_parameter(self, name, value):
        pass

    @abstractmethod
    def get_hyperparameters_search_space(self):
        pass

    @abstractmethod
    def set_hyperparameter_search_space(self, name, value_min=None, value_max=None):
        pass


class Clustering(IROp):
    def __init__(self):
        self.type = 'clustering'

    def run(self, dataset):
        def silhouette_score(estimator, X):
            try:
                clusters = estimator.fit_predict(X)
                score = metrics.silhouette_score(X, clusters)
            except:
                score = np.nan
            return score

        optimizer = GridSearchCV(self.model, param_grid=self.param_grid, scoring=silhouette_score)
        grid = optimizer.fit(dataset.ds.values)
        best_est = grid.best_estimator_
        dataset.labels = best_est.fit_predict(dataset.ds.values)
        return dataset

class KMeans(Clustering):
    def __init__(self):
        self.name = 'kmeans'
        self.n_clusters = None
        self.min_n_clusters = 0
        self.max_n_clusters = 5

    def run(self, dataset):

class IR:
    def __init__(self, pipeline):
        self.pipeline = self.create_IR(pipeline)

    def create_IR(self, pipeline):
        dict_pipeline = {}
        package = importlib.import_module('ds_operations')
        for i in pipeline:
            dict_pipeline[i] = getattr(package, pipeline[i])(self.dataset)

    def run(self, dataset):
        if len(self.pipeline) == 1:
            self.pipeline[0](dataset)
        else:
            self.run(self.pipeline[0](dataset), self.pipeline[1:])

    def modify_IR(self, **kwargs):
        for k,v in kwargs:
            for k1, v1 in self.pipeline:
                if v1.__class__.__name__ == k:
                    self.pipeline[k1] = v1.modify_parameter(v)