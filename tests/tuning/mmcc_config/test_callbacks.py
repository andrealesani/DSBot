import json
from asyncio import Future
from pathlib import Path
from unittest import TestCase

import pandas as pd
from mmcc_framework import Framework

import DSBot.tuning.mmcc_integration as integration
import DSBot.tuning.tuning_mixins as mixins
from ir.ir_operations import IROp
from ir.ir_parameters import IRPar


class IROpImpl(IROp):
    def run(self, result):
        print('Implemented')


# noinspection DuplicatedCode
pipeline = [
    IROpImpl('m1', [IRPar('p1', 0, '', 0, 1), IRPar('p2', 0, '', 0, 1), IRPar('p3', 0, '', 0, 1)]),
    IROpImpl('m2', [IRPar('p1', 0, '', 0, 1), IRPar('p2', 0, '', 0, 1), IRPar('p3', 0, '', 0, 1)]),
    IROpImpl('m3', [IRPar('p1', 0, '', 0, 1), IRPar('p2', 0, '', 0, 1), IRPar('p3', 0, '', 0, 1)]),
]


def build_framework() -> (Framework, Future):
    future = Future()
    return integration.get_framework(
        pipeline=pipeline,
        result='previous result',
        start_work=lambda p: future.set_result(p)
    ), future


def change_file():
    with open(Path(__file__).parent.parent / 'test_tuning_kb.json', 'r') as tuning_kb_file:
        mixins.tuning_kb = json.loads(tuning_kb_file.read())
    with open(Path(__file__).parent / 'test_process_kb.json', "r") as process_file:
        integration.kb = json.loads(process_file.read())


class TestStart(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        change_file()
        cls.test_p = pd.read_csv(Path(__file__).parent.parent / 'test_problem_kb.csv', sep=";")

    def setUp(self) -> None:
        super().setUp()
        mixins.update_pipeline(pipeline, [])
        self.fr, self.ftr = build_framework()

    def test_correct_payload(self):
        res = self.fr.handle_data_input({})
        self.assertEqual(res['payload']['status'], 'choose_problem')
        self.assertEqual(res['payload']['result'], 'previous result')
        self.assertEqual(res['utterance'], 'choose_problem sentence')
        self.assertFalse(self.ftr.done())


class TestChooseProblem(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        change_file()
        cls.test_p = pd.read_csv(Path(__file__).parent.parent / 'test_problem_kb.csv', sep=";")

    def setUp(self) -> None:
        super().setUp()
        mixins.update_pipeline(pipeline, [])
        self.fr, self.ftr = build_framework()
        self.fr.handle_data_input({})

    def test_missing_intent(self):
        res = self.fr.handle_data_input({})
        self.assertEqual(res['utterance'], 'Received data without intent: {}')
        self.assertFalse(self.ftr.done())

    def test_skip(self):
        res = self.fr.handle_data_input({'test_p': self.test_p, 'intent': 'skip'})
        expected = {
            'payload': {'status': 'edit_param', 'pipeline': pipeline},
            'utterance': 'no_highlights_sentence sentence'
        }
        self.assertDictEqual(res, expected)
        self.assertFalse(self.ftr.done())

    def test_known_problem(self):
        res = self.fr.handle_data_input({'test_p': self.test_p, 'intent': 'prob'})
        expected = {
            'utterance': 'Solution sentence edit_param_sentence sentence',
            'payload': {'status': 'edit_param', 'pipeline': pipeline}
        }
        self.assertDictEqual(res, expected)
        self.assertFalse(self.ftr.done())

    def test_not_known_problem(self):
        res = self.fr.handle_data_input({'test_p': self.test_p, 'intent': 'unknown'})
        expected = {'utterance': 'problem_err sentence', 'payload': {}}
        self.assertDictEqual(res, expected)
        self.assertFalse(self.ftr.done())


class TestEditParam(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        change_file()
        cls.test_p = pd.read_csv(Path(__file__).parent.parent / 'test_problem_kb.csv', sep=";")

    def setUp(self) -> None:
        super().setUp()
        mixins.update_pipeline(pipeline, [])
        self.fr, self.ftr = build_framework()
        self.fr.handle_data_input({})
        self.fr.handle_data_input({'intent': 'skip'})

    def test_missing_intent(self):
        res = self.fr.handle_data_input({})
        self.assertEqual(res['utterance'], 'Received data with missing intent or entities: {}')
        self.assertFalse(self.ftr.done())

    def test_run(self):
        res = self.fr.handle_data_input({'test_p': self.test_p, 'intent': 'run'})
        expected = {
            'payload': {'status': 'end'},
            'utterance': 'end sentence'
        }
        self.assertDictEqual(res, expected)
        self.assertTrue(self.ftr.done())
        self.assertEqual(self.ftr.result(), pipeline)

    def test_not_known_intent(self):
        res = self.fr.handle_data_input({'test_p': self.test_p, 'intent': 'abc'})
        self.assertEqual(res['utterance'], 'values_intent_err sentence')
        self.assertFalse(self.ftr.done())

    def test_edit_ok(self):
        res = self.fr.handle_data_input({'test_p': self.test_p,
                                         'intent': 'set',
                                         'module': 'm1',
                                         'parameter': 'p2',
                                         'value': 1})
        expected = {
            'payload': {'pipeline': pipeline},
            'utterance': 'values_updated sentence'
        }
        self.assertDictEqual(res, expected)
        self.assertFalse(self.ftr.done())

    def test_edit_missing_module(self):
        res = self.fr.handle_data_input({'test_p': self.test_p,
                                         'intent': 'set',
                                         'module': 'm0',
                                         'parameter': 'p2',
                                         'value': 1})
        self.assertEqual(res['utterance'], 'no_module_err sentence m0')
        self.assertFalse(self.ftr.done())

    def test_edit_missing_param(self):
        res = self.fr.handle_data_input({'test_p': self.test_p,
                                         'intent': 'set',
                                         'module': 'm1',
                                         'parameter': 'p0',
                                         'value': 1})
        self.assertEqual(res['utterance'], 'no_param_err sentence p0')
        self.assertFalse(self.ftr.done())

    def test_edit_wrong_value(self):
        res = self.fr.handle_data_input({'test_p': self.test_p,
                                         'intent': 'set',
                                         'module': 'm1',
                                         'parameter': 'p2',
                                         'value': -1})
        self.assertEqual(res['utterance'], 'value_err sentence')
        self.assertFalse(self.ftr.done())
