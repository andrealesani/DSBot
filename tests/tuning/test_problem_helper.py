from pathlib import Path
from unittest import TestCase

import pandas as pd

import DSBot.ir.ir_operations as ir
import DSBot.tuning.problem_helper as tuning


class TestGetData(TestCase):
    test_df = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.test_df = pd.read_csv(Path(__file__).parent / 'test_problem_kb.csv', sep=";")

    def test_get_data_with_exact_match(self):
        prb = {'e', 'd', 'f'}
        m_n = {'md1', 'md2', 'me1', 'me2'}
        mdl = make_irop(m_n)
        par = {'me2.1', 'me2.2'}
        utt = 'Sentence def'
        res = tuning.get_data(prb, mdl, self.test_df)
        self.assertEqual(res.problem, prb)
        self.assertEqual(set(res.pipeline), m_n)
        self.assertEqual(set(res.relevant_params), par)
        self.assertEqual(res.sentence, utt)

    def test_get_data_with_exact_match_more(self):
        prb = {'b', 'c'}
        m_n = {'mb1', 'mc1', 'mb2'}
        mdl = make_irop(m_n)
        par = {'mb1.1', 'mc1.2'}
        utt = 'Sentence bcde'
        res = tuning.get_data(prb, mdl, self.test_df)
        self.assertEqual(res.problem, prb)
        self.assertEqual(set(res.pipeline), m_n)
        self.assertEqual(set(res.relevant_params), par)
        self.assertEqual(res.sentence, utt)

    def test_get_data_with_missing_module(self):
        prb = {'b', 'c'}
        m_n = {'mb1', 'mc1'}
        mdl = make_irop(m_n)
        par = {'mb1.1', 'mc1.2'}
        utt = 'Sentence bc2'
        res = tuning.get_data(prb, mdl, self.test_df)
        self.assertEqual(res.problem, prb)
        self.assertEqual(set(res.pipeline), m_n)
        self.assertEqual(set(res.relevant_params), par)
        self.assertEqual(res.sentence, utt)


def make_irop(names):
    return {ir.IROp(n, {}) for n in names}
