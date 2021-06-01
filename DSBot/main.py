import os
import pandas as pd
from kb import KnowledgeBase
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.decomposition import PCA

class Dataset:
    def __init__(self, ds):
        self.ds = ds
        if ds is not None:
            self.missingValues, self.categorical, self.zeroVariance = self.check_ds()
        self.label = None
        self.name_plot = None


    def missing_values(self):
        return (self.ds.isnull().sum().sum())>0

    def fill_missing_values(self, col=[]):
        imp = IterativeImputer(max_iter=10, random_state=0)
        if len(col)>1:
            values_col = self.ds.columns.difference(col)
            values_dataset = pd.DataFrame(imp.fit_transform(self.ds[values_col]))
            values_dataset.columns = values_col
            values_dataset = pd.concat([self.ds, values_dataset])
        else:
            values_dataset = pd.DataFrame(imp.fit_transform(self.ds))
        return values_dataset

    def fill_missing_cat(self, col):
        self.ds = self.ds.apply(lambda col: col.fillna(col.value_counts().index[0]))

    def del_missing_rows(self):
        self.ds = self.ds.dropna()

    def zero_variance(self):
        var = self.ds.std(axis=1)
        return (var==0).sum()>0

    def categorical_columns(self):
        cols = self.ds.columns
        num_cols = self.ds._get_numeric_data().columns
        return len(list(set(cols) - set(num_cols))) > 0, list(set(cols) - set(num_cols))

    def one_hot_encode(self):
        cols = self.ds.columns
        num_cols = self.ds._get_numeric_data().columns
        self.ds = pd.get_dummies(self.ds, columns=list(set(cols) - set(num_cols)))

    def curse_of_dim(self):
        data = StandardScaler().fit_transform(self.ds)
        eucl = squareform(pdist(data.values))
        max_dist = eucl.max()
        min_dist = eucl[eucl.nonzero()].min()
        res = (max_dist-min_dist)/min_dist
        return res<1

    def dim_reduction(self):
        self.ds = PCA(len(self.ds.index)).fit_transform(self.ds)

    def check_ds(self):
        missing_val = self.missing_values()
        categorical, cols = self.categorical_columns()
        zero_var = self.zero_variance()
        return missing_val, categorical, zero_var

    def filter_kb(self, kb):
        drop = []
        for i in self.__dict__:
            if (str(i) in ['missingValues','categorical','zeroVariance']):
                if getattr(self, i):
                    for j in range(len(kb)):
                        kb_val = [i.strip() for i in kb.values[j,0].split(',')]
                        if not i in kb_val:
                            drop.append(j)
        kb = kb.drop(drop)
        return kb

def filter_kb(kb, request):
    req = request.split(' ')
    indices = []
    for index, row in kb.iterrows():
        if  all(item in row.values for item in req):
            indices.append(index)
    kb = kb.T[indices].T
    return kb
'''
kb = KnowledgeBase().kb
print(kb)
import seaborn as sns
titanic = sns.load_dataset('titanic')
titanic_ds = Dataset(titanic)
titanic_ds.filter_kb(kb)
from needleman_wunsch import NW
print(kb.values[0,1:])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from pydataset import data
    import seaborn as sns
    from clustering import Kmeans
    from plot import Plot
    titanic = sns.load_dataset('titanic')
    titanic_ds = Dataset(titanic)
    #print('titanic', titanic_ds.missingValues, titanic_ds.categorical)
    #print(titanic_ds.one_hot_encode())
    #print(titanic_ds.dataset.head())
    #print(titanic_ds.dataset.shape)
    #kmeans = Kmeans(titanic_ds.dataset, n_clust=3).res
    #scatterplot = Plot(titanic_ds).scatter(kmeans.labels)

    #os.system("onmt_translate -model ./wf/run/model_step_1000.pt -src wf/try.txt -output ./wf/pred_1000.txt -gpu -1 -verbose")
   # with open("wf/pred_1000.txt", 'r') as f:
    #    x = f.readlines()
    #print(x)
    #workflow =  x[0].strip().split(' ')
    #print(workflow)

    #kb = KnowledgeBase().kb
    #print(kb)
    #request = 'kmeans scatterplot'
    #kb = filter_kb(kb, request)
    #print(kb)
'''

