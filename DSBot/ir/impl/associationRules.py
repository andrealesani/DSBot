import pandas as pd


from ir.ir_operations import IROp, IROpOptions
from ir.ir_parameters import IRNumPar
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth


class IRRules(IROp):
    def __init__(self, name, parameters, model=None):
        super(IRRules, self).__init__(name, parameters)
        #self._model = model(**{v.name: v.value for v in parameters})


class IRAssociationRules(IRRules):
    def __init__(self):
        super(IRAssociationRules, self).__init__("associationRules", [IRNumPar('min_support', 0.2, 'float', min_v=0, max_v=1, step=0.1),
                                                        IRNumPar('min_threshold',0.6,'float',min_v=0.5,max_v=1, step=0.1)])  # TODO: before, model was passed to IROp.parameters. is this correct?



    def run(self, result, session_id):
        if 'transformed_ds' in result:
            dataset = result['transformed_ds']
        elif 'new_dataset' in result:
            dataset = result['new_dataset']
        else:
            dataset = result['original_dataset'].ds

        dataset_bool = dataset.replace({0:False, 1:True})
        numerical_col = []
        for i in dataset_bool.columns:
            if not dataset_bool[i].dtype==bool:
                numerical_col.append(i)

        dataset = pd.get_dummies(dataset, columns=numerical_col)
        dataset = dataset.replace({0: False, 1: True})

        freq_items = apriori(dataset, min_support=self.parameters['min_support'].value, use_colnames=True)
        rules = association_rules(freq_items, metric="confidence", min_threshold=self.parameters['min_support'].value)
        if result['original_dataset'].hasLabel:
            rules['consequents'] = [list(y)[0] for y in rules['consequents']]
            rules = rules[rules['consequents'].str.startswith(result['original_dataset'].label)]

        result['associationRules'] = rules
        print('rules', rules)
        return result

class IRGenericRuleLearning(IROpOptions):
    def __init__(self):
        super(IRGenericRuleLearning, self).__init__([IRAssociationRules()], "associationRules")