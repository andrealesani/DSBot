from sklearn import metrics
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.model_selection import GridSearchCV
import numpy as np
from scipy.optimize import curve_fit, minimize_scalar
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator
import matplotlib.pyplot as plt

def kmeans(dataset):
    def silhouette_score(estimator, X):
        clusters = estimator.fit_predict(dataset.ds.values)
        score = metrics.silhouette_score(dataset.ds.values, clusters)
        return score

    param_grid = {"n_clusters": range(2, int(len(dataset.ds)/2))}
    search = GridSearchCV(KMeans(), param_grid=param_grid, scoring=silhouette_score)
    grid = search.fit(dataset.ds.values)
    kmeans = grid.best_estimator_
    dataset.labels = kmeans.fit_predict(dataset.ds.values)
    return dataset

def agglomerativeClustering(dataset):
    def silhouette_score(estimator, X):
        clusters = estimator.fit_predict(dataset.ds.values)
        score = metrics.silhouette_score(dataset.ds.values, clusters)
        return score

    param_grid = {"n_clusters": range(2, int(len(dataset.ds)/2))}
    search = GridSearchCV(AgglomerativeClustering(), param_grid=param_grid, scoring=silhouette_score)
    grid = search.fit(dataset.ds.values)
    agg_clust = grid.best_estimator_
    dataset.labels = agg_clust.fit_predict(dataset.ds.values)
    return dataset


class Clustering:
    def __init__(self, dataset):
        self.dataset = dataset
        self.model = None
        self.param_grid = None

    def run(self):
        def silhouette_score(estimator, X):
            try:
                clusters = estimator.fit_predict(X)
                score = metrics.silhouette_score(X, clusters)
            except:
                score = np.nan
            return score

        optimizer = GridSearchCV(self.model, param_grid=self.param_grid, scoring=silhouette_score)
        grid = optimizer.fit(self.dataset.ds.values)
        best_est = grid.best_estimator_
        self.dataset.labels = best_est.fit_predict(self.dataset.ds.values)
        return self.dataset

class Kmeans(Clustering):
    def __init__(self, dataset, n_clusters = None):
        self.ds = dataset
        self.model = Kmeans()
        if n_clusters==None:
            self.param_grid = {"n_clusters": range(2, int(len(dataset.ds)/2))}
        else:
            self.n_clusters = n_clusters

class AgglomerativeClustering(Clustering):
    def __init__(self, dataset, n_clusters = None):
        self.ds = dataset
        self.model = AgglomerativeClustering()
        if n_clusters==None:
            self.param_grid = {"n_clusters": range(2, int(len(dataset.ds)/2))}
        else:
            self.n_clusters = n_clusters

class Dbscan(Clustering):
    def __init__(self, dataset, eps = None):
        self.ds = dataset
        self.model = DBSCAN()
        if eps==None:
            self.param_grid = {"eps": np.arange(0.3, 1, 0.1)}
        else:
            self.eps = eps

