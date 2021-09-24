from pathlib import Path
from unittest import TestCase

import pandas as pd

import DSBot.ir.ir_operations
import DSBot.tuning.problem_helper as tuning


class TestGetData(TestCase):
    test_df = None

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        tuning.p_table = pd.read_csv(Path(__file__).parent / 'test_problem_kb.csv', sep=';')

    def test_get_data_with_exact_match(self):
        prb = ['pa']
        m_n = {'m1', 'm2'}
        mdl = make_irop(m_n)
        par = [('m1', 'p11'), ('m2', 'p21'), ('m2', 'p22')]
        utt = 'a11 a21 a22'
        res = tuning.solve_problem(prb, mdl)
        self.assertEqual(res.problem, prb)
        self.assertEqual(set(res.pipeline), m_n)
        self.assertEqual(res.relevant_params, par)
        self.assertEqual(res.sentence, utt)

    def test_get_data_with_exact_match_more(self):
        prb = ['missing', 'pc']
        m_n = {'m2'}
        mdl = make_irop(m_n)
        par = [('m2', 'p22')]
        utt = 'c22'
        res = tuning.solve_problem(prb, mdl)
        self.assertEqual(res.problem, prb)
        self.assertEqual(set(res.pipeline), m_n)
        self.assertEqual(res.relevant_params, par)
        self.assertEqual(res.sentence, utt)

    def test_get_data_with_missing_module(self):
        prb = ['pa']
        mdl = make_irop({'missing'})
        with self.assertRaises(tuning.MissingSolutionError):
            tuning.solve_problem(prb, mdl)

    def test_get_data_no_solution(self):
        prb = ['missing']
        mdl = make_irop({'m1'})
        with self.assertRaises(tuning.MissingSolutionError):
            tuning.solve_problem(prb, mdl)


class IROpImpl(DSBot.ir.ir_operations.IROp):
    def run(self, result, session_id):
        print('Implemented')


def make_irop(names):
    return {IROpImpl(n, {}) for n in names}
