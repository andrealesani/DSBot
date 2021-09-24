import json
import logging
from pathlib import Path
from typing import List, Union, Tuple

import pandas as pd

from tuning.types import Pipeline

# Load the process description and kb from file.
p_table = pd.read_csv(Path(__file__).parent / 'problem_kb.csv', sep=',')
logging.getLogger(__name__).debug('Reading problem_kb file')
with open(Path(__file__).parent / 'problem_utt.json', "r") as utt_file:
    utt = json.loads(utt_file.read())
    logging.getLogger(__name__).debug('Reading problem_utt file')


class MissingSolutionError(Exception):
    """Raised when the queried problem and pipeline do not have a solution."""

    def __init__(self, problem, pipeline):
        super().__init__('The queried problem and pipeline do not have a solution. '
                         f'Problem: {problem}; Pipeline:{pipeline}')


class SolutionDetails:
    """The response of a problem query.

    :ivar problem: the problem keywords in the query request
    :ivar pipeline: the module names in the query request
    :ivar relevant_params: the list of relevant parameters names in the query response
    :ivar sentence: the sentence in the query response
    """

    def __init__(self, problem, pipeline: List[str], relevant_params: List[Tuple[str, str]], sentence: str):
        self.problem = problem
        self.pipeline = pipeline
        self.relevant_params = relevant_params
        self.sentence = sentence


def solve_problem(problem: Union[str, List[str]], pipeline: Pipeline):
    """Given a problem keyword and the pipeline in use, this returns the relevant solution details.

    The solution is taken from the `problem_kb` file; it contains the names of the parameters
    that are linked to the problem and an utterance that presents the solution.

    This first discards all the solutions whose parameters are not in the pipeline, then selects those that are linked
    with the first problem of the list, if possible, otherwise moves to the second problem and so on.

    :param problem: the problem keyword or a list or of problem keywords
    :param pipeline: the pipeline used
    :raise MissingSolutionError: if the queried problem and pipeline do not have a solution
    """
    # Uniform params types
    if isinstance(problem, str):
        problem = [problem]
    pipeline = [o.name for o in pipeline]

    # Filter modules
    filtered = p_table.loc[p_table['module'].isin(pipeline)]
    if filtered.empty:
        raise MissingSolutionError('any', pipeline)

    # Search solution iteratively
    res = _iter_solve(filtered, problem)
    if res is None:
        raise MissingSolutionError(problem, pipeline)

    # Return solution
    res = res.values.tolist()
    params = [tuple(i[:2]) for i in res]
    utterance = ' '.join([_get_utt(i[2]) for i in res])
    return SolutionDetails(problem, pipeline, params, utterance)


def _iter_solve(df, problems: List[str]):
    try:
        relevant = ['module', 'parameter', problems[0]]
        res = df.loc[:, relevant].dropna()
        if not res.empty:
            return res
    except IndexError:
        # Reached the end of problems
        return None
    except KeyError:
        pass

    # Missing problem or only NaN
    logging.getLogger(__name__).warning('No match for queried problem: %s', problems[0])
    return _iter_solve(df, problems[1:])


def _get_utt(key) -> str:
    try:
        return utt[key]
    except KeyError:
        logging.getLogger(__name__).warning('Missing problem utterance: %s', key)
        return key
