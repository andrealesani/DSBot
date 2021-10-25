import numpy
import pandas as pd
from scipy.sparse import *
from scipy.stats import pearsonr
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import kneighbors_graph as kng
from scipy.sparse.linalg import expm
from scipy.linalg import solve_banded
from scipy.spatial.distance import pdist
import scipy.spatial.distance
import math

import numpy as np
from scipy.sparse import *
from sklearn.metrics.pairwise import pairwise_distances
#from skfeature.function.similarity_based import lap_score


def construct_S(X, **kwargs):
    n_samples, n_features = np.shape(X)
    k = kwargs['neighbour_size']
    t = kwargs['t_param']

    # compute pairwise euclidean distances
    D = pairwise_distances(X)
    # print X
    D **= 2

    # sort the distance matrix D in ascending order
    Dsorted = np.sort(D, axis=1)
    idxSorted = np.argsort(D, axis=1)
    idx = idxSorted[:, 0:k + 1]  # returns the index of entire matrix
    dist = Dsorted[:, 0:k + 1]
    # compute the pairwise heat kernel distances
    Weight = np.exp(-dist / (t))
    G = np.zeros((n_samples * (k + 1), 3))
    G[:, 0] = np.tile(np.arange(n_samples), (k + 1, 1)).reshape(-1)
    G[:, 1] = np.ravel(idx, order='F')
    G[:, 2] = np.ravel(Weight, order='F')
    # build the sparse affinity matrix W
    S = csc_matrix((G[:, 2], (G[:, 0], G[:, 1])), shape=(n_samples, n_samples))
    bigger = np.transpose(S) > S
    S = S - S.multiply(bigger) + np.transpose(S).multiply(bigger)
    print(S)


def construct_W(X, **kwargs):
    n_samples, n_features = numpy.shape(X)
    k = kwargs['neighbour_size']
    t = kwargs['t_param']
    S = kng(X, k + 1, mode='distance',
            metric='euclidean')  # sqecludian distance works only with mode=connectivity  results were absurd
    S = (-1 * (S * S)) / (2 * t * t)
    S = S.tocsc()
    S = expm(S)
    S = S.tocsr()

    bigger = numpy.transpose(S) > S
    S = S - S.multiply(bigger) + numpy.transpose(S).multiply(bigger)
    return S


def lap_score(X, **kwargs):
    # if 'W' is not specified, use the default W
    if 'W' not in kwargs.keys():
        if 't_param' not in kwargs.keys():
            t_param = 1
        else:
            t = kwargs['t_param']
        if 'neighbour_size' not in kwargs.keys():
            neighbour_size = 5
        else:
            n = kwargs['neighbour_size']

        W = construct_W(X, t_param=t, neighbour_size=n)

    # construct the affinity matrix W
    else:
        W = kwargs['W']

    # build the diagonal D matrix from affinity matrix W
    D = numpy.array(W.sum(axis=1))

    L = W

    tmp = numpy.dot(numpy.transpose(D), X)
    D = diags(numpy.transpose(D), [0])
    Xt = numpy.transpose(X)
    t1 = numpy.transpose(numpy.dot(Xt, D.todense()))
    t2 = numpy.transpose(numpy.dot(Xt, L.todense()))
    # compute the numerator of Lr
    tmp = numpy.multiply(tmp, tmp) / D.sum()
    D_prime = numpy.sum(numpy.multiply(t1, X), 0) - tmp
    # compute the denominator of Lr
    L_prime = numpy.sum(numpy.multiply(t2, X), 0) - tmp
    # avoid the denominator of Lr to be 0
    D_prime[D_prime < 1e-12] = 10000
    # compute laplacian score for all features
    score = 1 - numpy.array(numpy.multiply(L_prime, 1 / D_prime))[0, :]
    return numpy.transpose(score)


"""
    Rank features in ascending order according to their laplacian scores, the smaller the laplacian score is, the more
    important the feature is
"""


def feature_ranking(score):
    idx = numpy.argsort(score, 0)
    return idx + 1


def LaplacianScore(X, **kwargs):
    if 'W' not in kwargs.keys():

        if 't_param' not in kwargs.keys():
            t = 1
        else:
            t = kwargs['t_param']

        if 'neighbour_size' not in kwargs.keys():
            n = 5
        else:
            n = kwargs['neighbour_size']

        W = construct_W(X, t_param=t, neighbour_size=n)
        n_samples, n_features = numpy.shape(X)
    # construct the affinity matrix W
    else:
        W = kwargs['W']

    # construct the diagonal matrix
    D = numpy.array(W.sum(axis=1))
    D = diags(numpy.transpose(D), [0])
    # construct graph Laplacian L
    L = D - W.toarray()

    # construct 1= [1,···,1]'
    I = numpy.ones((n_samples, n_features))

    # construct fr' => fr= [fr1,...,frn]'
    Xt = numpy.transpose(X)

    # construct fr^=fr-(frt D I/It D I)I
    t = numpy.matmul(numpy.matmul(Xt, D.toarray()), I) / numpy.matmul(numpy.matmul(numpy.transpose(I), D.toarray()), I)
    t = t[:, 0]
    t = numpy.tile(t, (n_samples, 1))
    fr = X - t

    # Compute Laplacian Score
    fr_t = numpy.transpose(fr)
    Lr = numpy.matmul(numpy.matmul(fr_t, L), fr) / numpy.matmul(numpy.dot(fr_t, D.toarray()), fr)

    return numpy.diag(Lr)

class Laplace:
    def __init__(self, percentage=None):
        self.percentage = percentage

    def fit_transform(self, X):
        print(X)
        n_samples, n_feature = X.shape
        data = X[:, 0:n_feature]

        L = lap_score(data)
        #print(L)
        #print(feature_ranking(L))
        if self.percentage==None:
            val = L.mean()
            for i in range(len(feature_ranking(L))):
                if L[i] < val:
                    if len(selected_k) == 0:
                        selected_k = [X[i].values]
                    else:
                        selected_k = np.concatenate((selected_k, [X[i].values]))
        else:
            val = val*X.shape[1]
            for i in range(len(feature_ranking(L))):
                if feature_ranking(L) < val:
                    if len(selected_k) == 0:
                        selected_k = [X[i].values]
                    else:
                        selected_k = np.concatenate((selected_k, [X[i].values]))
        selected_k = []

        selected_k = pd.DataFrame(selected_k).T
        X = selected_k
        print(X)
        return X