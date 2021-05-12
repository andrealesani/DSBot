import os
import pandas as pd
from kb import KnowledgeBase
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.decomposition import PCA

class Dataset:
    def __init__(self, dataset):
        print(dataset.head())
        self.dataset = dataset
        self.missingValues, self.categorical = self.check_ds()

    def missing_values(self):
        return (self.dataset.isnull().sum().sum())>0

    def fill_missing_values(self, col=[]):
        imp = IterativeImputer(max_iter=10, random_state=0)
        if len(col)>1:
            values_col = self.dataset.columns.difference(col)
            values_dataset = pd.DataFrame(imp.fit_transform(self.dataset[values_col]))
            values_dataset.columns = values_col
            values_dataset = pd.concat([self.dataset, values_dataset])
        else:
            values_dataset = pd.DataFrame(imp.fit_transform(self.dataset))
        return values_dataset

    def fill_missing_cat(self, col):
        self.dataset = self.dataset.apply(lambda col: col.fillna(col.value_counts().index[0]))

    def del_missing_rows(self):
        self.dataset = self.dataset.dropna()


    def zero_variance(self):
        var = self.dataset.std(axis=1)
        return (var==0).sum()>0

    def categorical_columns(self):
        cols = self.dataset.columns
        num_cols = self.dataset._get_numeric_data().columns
        return len(list(set(cols) - set(num_cols))) > 0, list(set(cols) - set(num_cols))

    def one_hot_encode(self):
        cols = self.dataset.columns
        num_cols = self.dataset._get_numeric_data().columns
        self.dataset = pd.get_dummies(self.dataset, columns=list(set(cols) - set(num_cols)))

    def curse_of_dim(self):
        data = StandardScaler().fit_transform(self.dataset)
        eucl = squareform(pdist(data.values))
        max_dist = eucl.max()
        min_dist = eucl[eucl.nonzero()].min()
        res = (max_dist-min_dist)/min_dist
        return res<1

    def dim_reduction(self):
        self.dataset = PCA(len(self.dataset.index)).fit_transform(self.dataset)

    def check_ds(self):
        missing_val = self.missing_values()
        categorical, cols = self.categorical_columns()
        return missing_val, categorical

def filter_kb(kb, request):
    req = request.split(' ')
    indices = []
    for index, row in kb.iterrows():
        if  all(item in row.values for item in req):
            indices.append(index)
    kb = kb.T[indices].T
    return kb


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from pydataset import data
    import seaborn as sns
    from clustering import Kmeans
    from plot import Plot
    titanic = sns.load_dataset('titanic')
    titanic_ds = Dataset(titanic)
    print('titanic', titanic_ds.missingValues, titanic_ds.categorical)
    #print(titanic_ds.one_hot_encode())
    #print(titanic_ds.dataset.head())
    #print(titanic_ds.dataset.shape)
    #kmeans = Kmeans(titanic_ds.dataset, n_clust=3).res
    #scatterplot = Plot(titanic_ds).scatter(kmeans.labels)

    os.system("onmt_translate -model ./wf/run/model_step_1000.pt -src wf/try.txt -output ./wf/pred_1000.txt -gpu -1 -verbose")
    with open("wf/pred_1000.txt", 'r') as f:
        x = f.readlines()
    #print(x)
    workflow =  x[0].strip().split(' ')
    print(workflow)

    #kb = KnowledgeBase().kb
    #print(kb)
    #request = 'kmeans scatterplot'
    #kb = filter_kb(kb, request)
    #print(kb)


