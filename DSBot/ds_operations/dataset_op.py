import os
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.decomposition import PCA

def missingValuesFill(dataset, col=[]):
    imp = IterativeImputer(max_iter=10, random_state=0)
    if len(col) > 1:
        values_col = dataset.dataset.columns.difference(col)
        values_dataset = pd.DataFrame(imp.fit_transform(dataset.dataset[values_col]))
        values_dataset.columns = values_col
        values_dataset = pd.concat([dataset.dataset, values_dataset])
    else:
        values_dataset = pd.DataFrame(imp.fit_transform(dataset.dataset))
    return values_dataset

def missingValuesRemove(dataset):
    dataset.dataset = dataset.dataset.dropna()
    return dataset.dataset


def oneHotEncode(dataset):
    cols = dataset.dataset.columns
    num_cols = dataset.dataset._get_numeric_data().columns
    dataset.dataset = pd.get_dummies(dataset.dataset, columns=list(set(cols) - set(num_cols)))
    return dataset