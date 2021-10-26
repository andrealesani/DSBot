from abc import abstractmethod

import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.model_selection import GridSearchCV, KFold

from ir.ir_exceptions import LabelsNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar, IRCatPar


class IRClustering(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRClustering, self).__init__(name,parameters)
        self._model = model(**{v.name: v.value for v in parameters})
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, dataset):
        #print(dataset)
        #dataset = result['original_dataset']
        self.parameter_tune(dataset)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,v.value)
        # self._param_setted = True

        #if self.labels is None:
        #    raise LabelsNotAvailable
        #return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        print('clustering')
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        # if not self._param_setted:
        self.set_model(dataset)
        try:
            y= self._model.fit_predict(dataset.values)
        except:
            y= self._model.fit_predict(dataset.values)
        self.labels = self._model.labels_
        result['labels'] = self.labels
        print('labels', result['labels'])
        clusters = self._model.fit_predict(dataset)
        result['silhouette'] = metrics.silhouette_score(dataset, clusters)
        result['original_dataset'].measures['num_clusters'] = self.parameters['n_clusters'].value
        result['original_dataset'].measures['silhouette'] = result['silhouette']
        self._param_setted = False
        return result

class IRKMeans(IRClustering):
    def __init__(self):
        super(IRKMeans, self).__init__("kmeans",
                                       [IRNumPar("n_clusters", 2, "int", 2, 10, 1)],  # TODO: what is the maximum?
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
                                 param_grid={"n_clusters": np.arange(self.parameters['n_clusters'].min_v,
                                                                     self.parameters['n_clusters'].max_v,
                                                                     self.parameters['n_clusters'].step)},
                                 scoring=silhouette_score, cv=KFold(10, shuffle=True))
        grid = optimizer.fit(dataset)
        self.parameters['n_clusters'].value = grid.best_estimator_.n_clusters

        return self.parameters

class IRAgglomerativeClustering(IRClustering):
    def __init__(self):
        super(IRAgglomerativeClustering, self).__init__("agglomerativeClustering",
                                                        [IRNumPar("n_clusters", 2, "int", 2, 10, 1),
                                                         IRCatPar("linkage", "single", ['single','complete','ward'])],  # TODO: what is the maximum?
                                                        AgglomerativeClustering)


    def parameter_tune(self, dataset):
        def silhouette_score(estimator, X):
            try:
                clusters = estimator.fit_predict(X)
                score = metrics.silhouette_score(X, clusters)
            except:
                score = np.nan
            return score

        optimizer = GridSearchCV(AgglomerativeClustering(),
                                 param_grid={"n_clusters": np.arange(self.parameters['n_clusters'].min_v, self.parameters['n_clusters'].max_v, self.parameters['n_clusters'].step)},
                                 scoring=silhouette_score, cv=KFold(10, shuffle=True))
        grid = optimizer.fit(dataset)
        self.parameters['n_clusters'].value = grid.best_estimator_.n_clusters
        return self.parameters


class IRDBSCAN(IRClustering):
    def __init__(self):
        super(IRDBSCAN, self).__init__("dbscan",
                                       [IRNumPar("eps", 0.1, "float", 0, 1, 0.1)],  # TODO: what is the maximum?
                                       DBSCAN)

    def parameter_tune(self, dataset):
        from sklearn.neighbors import NearestNeighbors
        neigh = NearestNeighbors(n_neighbors=2)
        nbrs = neigh.fit(dataset)
        distances, indices = nbrs.kneighbors(dataset)
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
            eps = self.parameters['eps'].default_value

        self.parameters['eps'].value = eps
        return self.parameters


class IRGenericClustering(IROpOptions):
    def __init__(self):
        super(IRGenericClustering, self).__init__([IRKMeans(), IRDBSCAN(), IRAgglomerativeClustering()], "kmeans")
