import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import Lasso

def lasso(dataset):
    param_grid = {'model__alpha': np.arange(0.1, 10, 0.1)}
    search = GridSearchCV(Lasso(),param_grid=param_grid,scoring="neg_mean_squared_error")
    search.fit(dataset.ds.values)
    coefficients = search.best_estimator_.named_steps['model'].coef_
    importance = np.abs(coefficients)
    dataset.features_selected = np.array(dataset.ds.columns)[importance > 0]
    return dataset