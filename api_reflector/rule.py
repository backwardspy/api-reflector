"""
Defines the rules engine.
"""

from enum import Enum
from typing import Callable, Union


class Operator(Enum):
    """
    Operators that are used in rule evaulation.
    """

    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    LESS_THAN_EQUAL = "LESS_THAN_EQUAL"
    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_EQUAL = "GREATER_THAN_EQUAL"
    IS_EMPTY = "IS_EMPTY"
    IS_NOT_EMPTY = "IS_NOT_EMPTY"
    CONTAINS = "CONTAINS"
    NOT_CONTAINS = "NOT_CONTAINS"

    def __str__(self) -> str:
        return self.value


n_args = {
    Operator.EQUAL: 2,
    Operator.NOT_EQUAL: 2,
    Operator.LESS_THAN: 2,
    Operator.LESS_THAN_EQUAL: 2,
    Operator.GREATER_THAN: 2,
    Operator.GREATER_THAN_EQUAL: 2,
    Operator.IS_EMPTY: 1,
    Operator.IS_NOT_EMPTY: 1,
    Operator.CONTAINS: 2,
    Operator.NOT_CONTAINS: 2,
}


EvaluatorFunction1 = Callable[[str], bool]
EvaluatorFunction2 = Callable[[str, str], bool]
EvaluatorFunction = Union[EvaluatorFunction1, EvaluatorFunction2]

evaluators: dict[Operator, EvaluatorFunction] = {
    Operator.EQUAL: lambda x, y: x == y,
    Operator.NOT_EQUAL: lambda x, y: x != y,
    Operator.LESS_THAN: lambda x, y: float(x) < float(y),
    Operator.LESS_THAN_EQUAL: lambda x, y: float(x) <= float(y),
    Operator.GREATER_THAN: lambda x, y: float(x) > float(y),
    Operator.GREATER_THAN_EQUAL: lambda x, y: float(x) >= float(y),
    Operator.IS_EMPTY: lambda x: bool(x) is False,
    Operator.IS_NOT_EMPTY: lambda x: bool(x) is True,
    Operator.CONTAINS: lambda x, y: y in x,
    Operator.NOT_CONTAINS: lambda x, y: y not in x,
}
