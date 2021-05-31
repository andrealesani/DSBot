import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib
matplotlib.use('agg')

def pca2(dataset):
    pca = PCA(2)
    dataset.ds = pca.fit_transform(dataset.ds.values)
    return dataset

def scatterplot(dataset):
    u_labels = np.unique(dataset.labels)
    for i in u_labels:
        plt.scatter(dataset.ds[dataset.labels == i, 0], dataset.ds[dataset.labels == i, 1], label=i)
    plt.legend()
    dataset.name_plot = 'scatter.png'
    plt.savefig('scatter.png')
    #plt.show()

def heatmap(matrix):
    plt.figure(figsize=(16, 16))
    cg = sns.clustermap(matrix, vmin=0, vmax=1, center=0.5)
    cg.ax_row_dendrogram.set_visible(False)
    cg.ax_col_dendrogram.set_visible(False)
    plt.show()

class Plot:
    def __init__(self, dataset):
        self.ds = dataset.ds

    def scatterplot(self, labels):
        pca = PCA(2)
        pca_data = pca.fit_transform(self.ds)
        u_labels = np.unique(labels)
        for i in u_labels:
            plt.scatter(pca_data[labels==i, 0], pca_data[labels==i, 1], label=i)
        plt.legend()
        plt.show()

    def heatmap(self,corr):
        plt.figure(figsize=(16, 16))
        cg = sns.clustermap(corr, vmin=0, vmax=1, center=0.5)
        cg.ax_row_dendrogram.set_visible(False)
        cg.ax_col_dendrogram.set_visible(False)
        plt.show()