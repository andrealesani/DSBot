from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV

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

class KMeansRes:
    def __init__(self, dataset, labels):
        self.ds = dataset
        self.labels = labels


class Kmeans:
    def __init__(self, dataset, n_clust=None, max=None):
        self.ds = dataset
        self.n_clust = n_clust
        self.max = max
        self.res = self.run()

    def run(self):
        if self.n_clust != None:
            from sklearn.decomposition import PCA
            #pca = PCA(2)
           # pca_data = pca.fit_transform(self.ds)
            #print(pca_data.shape)
            pca_data = self.ds.values
            kmeans = KMeans(n_clusters=self.n_clust)
            labels = kmeans.fit_predict(pca_data)
        else:
            def silhouette_score(estimator, X):
                clusters = estimator.fit_predict(self.ds.values)
                score = metrics.silhouette_score(self.ds.values, clusters)
                return score

            param_grid = {"n_clusters": range(2, self.max)}
            search = GridSearchCV(KMeans(), param_grid=param_grid, scoring=silhouette_score)
            grid = search.fit(self.ds.values)
            kmeans = grid.best_estimator_
            labels = kmeans.fit_predict(self.ds.values)

        return KMeansRes(self.ds, labels)

class Clustering:
    def __init__(self, dataset):
        self.ds = dataset
        self.run()

    def run(self):
        Kmeans(self.ds.dataset)



