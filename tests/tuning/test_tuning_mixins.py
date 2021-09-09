import json
from pathlib import Path
from unittest import TestCase

import DSBot.tuning.tuning_mixins as mixins
from DSBot.ir.ir_operations import IROp, IROpOptions
from DSBot.ir.ir_parameters import IRPar


def change_file():
    with open(Path(__file__).parent / 'test_tuning_kb.json', 'r') as tuning_kb_file:
        mixins.tuning_kb = json.loads(tuning_kb_file.read())


class IROpImpl(IROp):
    def run(self, result):
        print('Implemented')


class TestTuningOpMixin(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        change_file()

    def test_pretty_name(self):
        mod = IROpImpl('mod1', {})
        self.assertEqual(mod.pretty_name, 'Module 1')

    def test_pretty_name_missing(self):
        mod = IROpImpl('mod3', {})
        self.assertEqual(mod.pretty_name, 'mod3')

    def test_is_highlighted(self):
        mod = IROpImpl('mod', {})
        mod.is_highlighted = True
        self.assertTrue(mod.is_highlighted)
        mod.is_highlighted = False
        self.assertFalse(mod.is_highlighted)
        mod.is_highlighted = True
        self.assertTrue(mod.is_highlighted)

    def test_is_highlighted_not_set(self):
        mod = IROpImpl('mod', {})
        self.assertFalse(mod.is_highlighted)

    def test_tojson(self):
        mod = IROpImpl('mod4', [IRPar('param4.1', 0, 'float', 0, 1)])
        self.assertDictEqual(mod.to_json(), {
            'name': 'mod4',
            'pretty_name': 'Module 4',
            'parameters': {
                'param4.1': {
                    'name': 'param4.1',
                    'pretty_name': 'Param 4.1',
                    'value': 0,
                    'min': 0,
                    'max': 1,
                    'default': 0,
                    'description': 'Parameter 1 of module 4',
                    'is_highlighted': False,
                    'type': 'float'
                },
            },
            'is_highlighted': False
        })


# noinspection PyStatementEffect
class TestTuningParMixin(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        change_file()

    def test_get_param_data_missing_module(self):
        par = IRPar('param', 0, 'float', 0, 1)
        with self.assertRaises(mixins.MissingModuleNameError):
            par._get_param_data()

    def test_get_param_data_none_module(self):
        par = IRPar('param', 0, 'float', 0, 1)
        par.module = None
        with self.assertRaises(mixins.MissingModuleNameError):
            par._get_param_data()

    def test_get_param_data_missing_module_data(self):
        par = IRPar('param', 0, 'float', 0, 1)
        par.module = 'missing'
        with self.assertRaises(mixins.IncorrectKbError):
            par._get_param_data()

    def test_get_param_data_missing_params_data(self):
        par = IRPar('param', 0, 'float', 0, 1)
        par.module = 'mod2'
        with self.assertRaises(mixins.IncorrectKbError):
            par._get_param_data()

    def test_get_param_data_missing_data(self):
        par = IRPar('param', 0, 'float', 0, 1)
        par.module = 'mod1'
        with self.assertRaises(mixins.IncorrectKbError):
            par._get_param_data()

    def test_pretty_name(self):
        par = IRPar('param1.1', 0, 'float', 0, 1)
        par.module = 'mod1'
        self.assertEqual(par.pretty_name, 'Param 1.1')

    def test_pretty_name_missing(self):
        par = IRPar('param1.2', 0, 'float', 0, 1)
        par.module = 'mod1'
        self.assertEqual(par.pretty_name, 'param1.2')

    def test_pretty_name_missing_mod(self):
        par = IRPar('param1.1', 0, 'float', 0, 1)
        with self.assertRaises(mixins.MissingModuleNameError):
            par.pretty_name

    def test_description(self):
        par = IRPar('param1.1', 0, 'float', 0, 1)
        par.module = 'mod1'
        self.assertEqual(par.description, 'Parameter 1 of module 1')

    def test_description_missing(self):
        par = IRPar('param1.2', 0, 'float', 0, 1)
        par.module = 'mod1'
        self.assertEqual(par.description, '')

    def test_description_missing_mod(self):
        par = IRPar('param1.1', 0, 'float', 0, 1)
        with self.assertRaises(mixins.MissingModuleNameError):
            par.description

    def test_is_highlighted(self):
        par = IRPar('param3', 0, 'float', 0, 1)
        par.is_highlighted = True
        self.assertTrue(par.is_highlighted)
        par.is_highlighted = False
        self.assertFalse(par.is_highlighted)
        par.is_highlighted = True
        self.assertTrue(par.is_highlighted)

    def test_is_highlighted_not_set(self):
        par = IRPar('param3', 0, 'float', 0, 1)
        self.assertFalse(par.is_highlighted)

    def test_tojson(self):
        par = IRPar('param4.1', 0, 'float', 0, 1)
        par.module = 'mod4'
        self.assertDictEqual(par.to_json(), {
            'name': 'param4.1',
            'pretty_name': 'Param 4.1',
            'value': 0,
            'min': 0,
            'max': 1,
            'default': 0,
            'description': 'Parameter 1 of module 4',
            'is_highlighted': False,
            'type': 'float'
        })


class TestTuningOpOptionsMixin(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        change_file()

    def test_tojson(self):
        opt = IROpOptions([IROpImpl('mod4', [IRPar('param4.1', 0, 'float', 0, 1)])], 'mod4')
        res = {
            'name': 'mod4',
            'pretty_name': 'Module 4',
            'parameters': {
                'param4.1': {
                    'name': 'param4.1',
                    'pretty_name': 'Param 4.1',
                    'value': 0,
                    'min': 0,
                    'max': 1,
                    'default': 0,
                    'description': 'Parameter 1 of module 4',
                    'is_highlighted': False,
                    'type': 'float'
                },
            },
            'is_highlighted': False
        }
        res['models'] = {'mod4': res.copy()}
        self.assertDictEqual(opt.to_json(), res)


class TestUpdatePipeline(TestCase):

    def setUp(self) -> None:
        super().setUp()
        pipeline = [
            IROpImpl('m1', [IRPar('p1', 0, '', 0, 1), IRPar('p2', 0, '', 0, 1), IRPar('p3', 0, '', 0, 1)]),
            IROpImpl('m2', [IRPar('p1', 0, '', 0, 1), IRPar('p2', 0, '', 0, 1), IRPar('p3', 0, '', 0, 1)]),
            IROpImpl('m3', [IRPar('p1', 0, '', 0, 1), IRPar('p2', 0, '', 0, 1), IRPar('p3', 0, '', 0, 1)]),
        ]
        relevant = ['m1.p1', 'm1.p2', 'm3.p1', 'm3.p3']
        self.pipeline = mixins.update_pipeline(pipeline, relevant)

    def test_update_pipeline_params(self):
        result = {}
        for m in self.pipeline:
            result[m.name] = {}
            for k, v in m.parameters.items():
                result[m.name][k] = v.is_highlighted
        expected = {
            'm1': {'p1': True, 'p2': True, 'p3': False},
            'm2': {'p1': False, 'p2': False, 'p3': False},
            'm3': {'p1': True, 'p2': False, 'p3': True}
        }
        self.assertDictEqual(result, expected)

    def test_update_pipeline_modules(self):
        result = {m.name: m.is_highlighted for m in self.pipeline}
        expected = {
            'm1': True,
            'm2': False,
            'm3': True
        }
        self.assertDictEqual(result, expected)
