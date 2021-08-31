import logging
from typing import Union, List, Set

import pandas as pd

from ir.ir_operations import IROp, IROpOptions


class ProblemError(Exception):
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

    def __init__(self, problem: Set[str], pipeline: List[str], relevant_params: List[str], sentence: str):
        self.problem = problem
        self.pipeline = pipeline
        self.relevant_param = relevant_params
        self.sentence = sentence


Problem = Union[str, Set[str], List[str]]
"""A type representing a string or a list or set of strings."""

Pipeline = Union[List[Union[IROp, IROpOptions]], Set[Union[IROp, IROpOptions]]]
"""A type representing a list or set of IROp or IROpOptions objects."""


def get_data(problem: Problem, pipeline: Pipeline, source="problem_kb.csv") -> SolutionDetails:
    """Given a problem keyword and the pipeline in use, this returns the relevant solution details.

    The solution is taken from the `problem_kb` file or the source provided; it contains the names of the parameters
    that are linked to the problem and an utterance that presents the solution.

    This returns the first row in the table that has all the problem keywords in the query (or more) and whose modules
    are all in the pipeline.

    :param problem: the problem keyword or a list or set of problem keywords
    :param pipeline: the pipeline used
    :param source: the problem table kb, used for testing
    :raise ProblemError: if the queried problem and pipeline do not have a solution
    """

    # Uniform params types
    if isinstance(problem, str):
        problem = {problem}
    elif isinstance(problem, list):
        problem = set(problem)
    pipeline = [o.name for o in pipeline]
    pipeline_s = set(pipeline)

    # Scan table and return first result
    df = pd.read_csv(source, sep=";")
    for i, r in df.iterrows():
        if problem <= set(r['problemKeyword'].split()) and set(r['pipeline'].split()) <= pipeline_s:
            return SolutionDetails(problem, pipeline, r['param'].spit(), r['sentence'])

    # No results: raise
    error = ProblemError(problem, pipeline)
    logging.getLogger(__name__).error(error)
    raise error
