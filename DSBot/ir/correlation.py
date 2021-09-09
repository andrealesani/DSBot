from ir.ir_exceptions import CorrelationNotAvailable
from ir.ir_operations import IROp, IROpOptions


class IRCorrelation(IROp):
    def __init__(self, name, model = None):
        super(IRCorrelation, self).__init__(name, model)  # FIXME: model is passed to IROp.parameters. Change to []?
        self._model = model
        self.correlation = None

    def get_correlation(self):
        if self.correlation is None:
            raise CorrelationNotAvailable
        return self.correlation

    #TDB cosa deve restituire questa funzione?
    def run(self, result):
        dataset = result['original_dataset']
        self.correlation = dataset.ds.corr(method=self._model)
        result['correlation'] = self.correlation
        return result

class IRPearson(IRCorrelation):
    def __init__(self):
        super(IRPearson, self).__init__("pearson", 'pearson')


class IRSpearman(IRCorrelation):
    def __init__(self):
        super(IRSpearman, self).__init__("spearman", 'spearman')


class IRGenericCorrelation(IROpOptions):
    def __init__(self):
        super(IRGenericCorrelation, self).__init__([IRPearson(), IRSpearman()], "pearson")
