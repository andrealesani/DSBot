import pandas as pd
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