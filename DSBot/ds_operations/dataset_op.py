import os
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.decomposition import PCA

def missingValuesFill(dataset):
    imp = IterativeImputer(max_iter=10, random_state=0)

    if len(dataset.col) > 0:
        values_col = dataset.ds.columns.difference(dataset.col)
        values_dataset = pd.DataFrame(imp.fit_transform(dataset.ds[values_col]))
        values_dataset.columns = values_col
        dataset.ds = dataset.ds.apply(lambda col: col.fillna(col.value_counts().index[0]))
        values_dataset = pd.concat([dataset.ds, values_dataset])
    else:
        values_dataset = pd.DataFrame(imp.fit_transform(dataset.ds))

    dataset.ds = values_dataset
    return dataset

def missingValuesRemove(dataset):
    dataset.ds = dataset.ds.dropna()
    return dataset

def oneHotEncode(dataset):
    cols = dataset.ds.columns
    num_cols = dataset.ds._get_numeric_data().columns
    dataset.ds = pd.get_dummies(dataset.ds, columns=list(set(cols) - set(num_cols)))
    return dataset

def standardScaler(dataset):
    values = StandardScaler().fit_transform(dataset.ds.values)
    dataset.ds = pd.DataFrame(values, index=dataset.ds.index, columns=dataset.ds.columns)
    return dataset.ds