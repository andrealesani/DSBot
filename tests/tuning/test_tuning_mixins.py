import json
from pathlib import Path
from unittest import TestCase

import DSBot.tuning.tuning_mixins as mixins
from DSBot.ir.ir_operations import IROp
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
