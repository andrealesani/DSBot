import scipy.stats as ss
import pandas as pd
import numpy as np

def pearson(dataset):
    dataset.correlation = dataset.ds.corr()
    return dataset

def spearman(dataset):
    dataset.correlation = dataset.ds.corr(method='spearman')
    return dataset


# TODO: sistemare cramer, x e y dovrebbero essere le colonne categoriche tra cui si vuole calcolare la correlazione
def cramer(dataset):
    x = dataset.ds.columns
    y = dataset.ds.columns
    confusion_matrix = pd.crosstab(x, y)
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    dataset.correlation = np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))
    return dataset


class Correlation:
    def __init__(self, dataset):
        self.ds = dataset
        if self.ds.categorical:
            CramerV(self.ds)
        else:
            Pearson(self.ds)

class CramerV:
    def __init__(self, dataset):
        self.ds = dataset
        self.run()

    def run(self):
        correlation = self.ds.dataset.corr()

        return correlation
        #def cramers_v(x, y):
        # confusion_matrix = pd.crosstab(x, y)
        # chi2 = ss.chi2_contingency(confusion_matrix)[0]
        # n = confusion_matrix.sum().sum()
        # phi2 = chi2 / n
        # r, k = confusion_matrix.shape
        # phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
        # rcorr = r - ((r - 1) ** 2) / (n - 1)
        # kcorr = k - ((k - 1) ** 2) / (n - 1)
        # return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

class Pearson:
    def __init__(self, dataset):
        self.ds = dataset
        self.res = self.run()

    def run(self):
        correlation = self.ds.dataset.corr()

        return correlation