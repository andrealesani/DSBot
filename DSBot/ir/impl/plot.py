from abc import abstractmethod

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from seaborn import scatterplot, clustermap
from matplotlib.pyplot import scatter
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score
from scipy import interp
from ir.ir_exceptions import LabelsNotAvailable, PCADataNotAvailable, CorrelationNotAvailable
from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRPar


class IRPlot(IROp):
    def __init__(self, name, parameters, model = None):
        super(IRPlot, self).__init__(name,parameters)
        self._model = model
        self.labels = None

    @abstractmethod
    def parameter_tune(self, dataset):
        pass

    def set_model(self, result):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        self.parameter_tune(dataset)
        for p,v in self.parameters.items():
            self._model.__setattr__(p,v.value)
        self._param_setted = True

    def get_labels(self):
        if self.labels is None:
            raise LabelsNotAvailable
        return self.labels

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        if 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        if not self._param_setted:
            self.set_model(dataset)
        try:
            self._model.fit_predict(dataset.ds.values)
        except:
            self._model.fit_predict(dataset)
        self.labels = self._model.labels_
        result['plot'] = self.labels
        return result

class IRScatterplot(IRPlot):
    def __init__(self):
        super(IRScatterplot, self).__init__("scatterplot",
                                            [],
                                            scatter)

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if 'labels' not in result:
            raise LabelsNotAvailable
        else:
            u_labels = np.unique(result['labels'])

        if 'transformed_ds' not in result:
            raise PCADataNotAvailable
        else:
            transformed_ds = result['transformed_ds']

        fig = plt.figure()
        for i in u_labels:
            ax = scatter(transformed_ds[result['labels'] == i, 0], transformed_ds[result['labels'] == i, 1], label=i)
        plt.savefig('./temp/temp_' + str(session_id) + '/scatter.png')
        if 'plot' not in result:
            result['plot'] = ['./temp/temp_' + str(session_id) + '/scatter.png']
            #result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
        else:
            result['plot'].append('./temp/temp_' + str(session_id) + '/scatter.png')
            #result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")

        result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/scatter.png'

        # plt.show()
        return  result


class IRClustermap(IRPlot):
    def __init__(self):
        super(IRClustermap, self).__init__("clustermap",
                                           [],
                                           clustermap)

    def parameter_tune(self, dataset):
        pass

    def run(self, result, session_id):
        if 'correlation' not in result:
            raise CorrelationNotAvailable
        else:
            correlation = result['correlation']

        plt.figure(figsize=(15, 15))
        matplotlib.rcParams.update({'font.size': 18})

        cg = clustermap(correlation, cmap='binary')#, xticklabels=False, yticklabels=False)
        cg.ax_row_dendrogram.set_visible(False)
        cg.ax_col_dendrogram.set_visible(False)
        ax = cg.ax_heatmap
        plt.savefig('./temp/temp_' + str(session_id) + '/clustermap.png')
        if 'plot' not in result:
            result['plot'] = ['./temp/temp_' + str(session_id) + '/clustermap.png']
            # result['plot'] = ["u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)"]
        else:
            result['plot'].append('./temp/temp_' + str(session_id) + '/clustermap.png')
            # result['plot'].append("u_labels = np.unique(result['labels'])\nfor i in u_labels:\n\tax = plt.scatter(result['transformed_ds'][result['labels'] == i, 0], result['transformed_ds'][result['labels'] == i, 1], label=i)")

        result['original_dataset'].name_plot = './temp/temp_' + str(session_id) + '/clustermap.png'

        return  result


class IRROC(IRPlot):
    def __init__(self):
        super(IRROC, self).__init__("roc",
                                           [],
                                           clustermap)

    def parameter_tune(self, dataset):
        pass

    def run(self, result):
        n_classes = set(result['label'])
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(result['y_test'][:, i], result['y_score'][:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(result['y_test'].ravel(), result['y_score'].ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
        # First aggregate all false positive rates
        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

        # Then interpolate all ROC curves at this points
        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += interp(all_fpr, fpr[i], tpr[i])

        # Finally average it and compute AUC
        mean_tpr /= n_classes

        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

        # Plot all ROC curves
        plt.figure()
        plt.plot(fpr["micro"], tpr["micro"],
                 label='micro-average ROC curve (area = {0:0.2f})'
                       ''.format(roc_auc["micro"]),
                 color='deeppink', linestyle=':', linewidth=4)

        plt.plot(fpr["macro"], tpr["macro"],
                 label='macro-average ROC curve (area = {0:0.2f})'
                       ''.format(roc_auc["macro"]),
                 color='navy', linestyle=':', linewidth=4)

        colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
        for i, color in zip(range(n_classes), colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=lw,
                     label='ROC curve of class {0} (area = {1:0.2f})'
                           ''.format(i, roc_auc[i]))

        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Some extension of Receiver operating characteristic to multi-class')
        plt.legend(loc="lower right")
        plt.show()
        if 'transformed_ds' not in result:
            raise PCADataNotAvailable
        else:
            transformed_ds = result['transformed_ds']

        plt.figure(figsize=(15, 15))
        matplotlib.rcParams.update({'font.size': 18})

        cg = clustermap(transformed_ds, cmap='binary', xticklabels=False, yticklabels=False)
        cg.ax_row_dendrogram.set_visible(False)
        ax = cg.ax_heatmap

        if 'plot' not in result:
            result['plot'] = ax

        return  result

# FIXME: this class was commented out because the implementation raises errors
class IRGenericPlot(IROpOptions):
     def __init__(self):
         super(IRGenericPlot, self).__init__([IRScatterplot(), IRClustermap()], "scatterplot")
