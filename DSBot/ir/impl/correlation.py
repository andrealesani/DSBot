from ir.ir_exceptions import CorrelationNotAvailable
from ir.ir_operations import IROp, IROpOptions


class IRCorrelation(IROp):
    def __init__(self, name, model = None):
        super(IRCorrelation, self).__init__(name, [])  # TODO: before, model was passed to IROp.parameters. is this correct?
        self._model = model
        self.correlation = None

    def get_correlation(self):
        if self.correlation is None:
            raise CorrelationNotAvailable
        return self.correlation

    #TDB cosa deve restituire questa funzione?
    def run(self, result, session_id):
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds
        self.correlation = dataset.corr(method=self._model)
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
