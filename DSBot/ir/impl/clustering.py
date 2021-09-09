from abc import abstractmethod

import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans, DBSCAN
from sklearn.model_selection import GridSearchCV

from DSBot.ir.ir_exceptions import LabelsNotAvailable
from DSBot.ir.ir_operations import IROp, IROpOptions
from DSBot.ir.ir_parameters import IRPar


class IRClustering(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRClustering, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
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
    def run(self, result):
        dataset = result['original_dataset']
        if not self._param_setted:
            self.set_model(dataset)
        try:
            self._model.fit_predict(dataset.ds.values)
        except:
            self._model.fit_predict(dataset)
        self.labels = self._model.labels_
        result['labels'] = self.labels
        return result

class IRKMeans(IRClustering):
    def __init__(self):
        super(IRKMeans, self).__init__("kmeans",
                                       [IRPar("n_clusters", 8, "int", 1, 10)],  # TODO: what is the maximum?
                                       KMeans)

    def parameter_tune(self, dataset):
        def silhouette_score(estimator, X):
            try:
                clusters = estimator.fit_predict(X)
                score = metrics.silhouette_score(X, clusters)
            except:
                score = np.nan
            return score

        optimizer = GridSearchCV(KMeans(),
                                 param_grid={"n_clusters": np.arange(2, dataset.ds.shape[0]//2, 1)},
                                 scoring=silhouette_score)
        grid = optimizer.fit(dataset.ds)
        self.parameters['n_clusters'].value = grid.best_estimator_.n_clusters
        return self.parameters


class IRDBSCAN(IRClustering):
    def __init__(self):
        super(IRDBSCAN, self).__init__("dbscan",
                                       [IRPar("eps", 0.1, "float", 0, 1)],  # TODO: what is the maximum?
                                       DBSCAN)

    def parameter_tune(self, dataset):
        from sklearn.neighbors import NearestNeighbors
        neigh = NearestNeighbors(n_neighbors=2)
        nbrs = neigh.fit(dataset.ds)
        distances, indices = nbrs.kneighbors(dataset.ds)
        sorted_dist = sorted([x[1] for x in distances if x[1]>0])
        try:
            pos = 0
            max_dif = sorted_dist[1] - sorted_dist[0]
            for i in range(1, len(sorted_dist)-1):
                if (sorted_dist[i+1] - sorted_dist[i]) > max_dif:
                    max_dif = sorted_dist[i+1] - sorted_dist[i]
                    pos = i
            eps = sorted_dist[pos]
        except:
            eps = 0.1

        self.parameters['eps'].value = eps
        return self.parameters


class IRGenericClustering(IROpOptions):
    def __init__(self):
        super(IRGenericClustering, self).__init__([IRKMeans(), IRDBSCAN()], "kmeans")
