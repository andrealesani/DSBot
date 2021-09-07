from typing import List, Set, Union, Callable

Problem = Union[str, Set[str], List[str]]
"""A type representing a string or a list or set of strings."""

Pipeline = Union[List[Union['IROp', 'IROpOptions']], Set[Union['IROp', 'IROpOptions']]]
"""A type representing a list or set of IROp or IROpOptions objects."""

PipelineCallback = Callable[[Pipeline], None]
"""A type representing a callback that takes a `Pipeline` and returns `None`"""
