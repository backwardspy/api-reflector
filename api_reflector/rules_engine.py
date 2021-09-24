"""
Defines the rules engine.
"""

from enum import Enum
from typing import Any, Callable, Mapping, NamedTuple, TypeVar, Union

from jinja2 import Template


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


class TemplatableRequest(NamedTuple):
    """
    A collection of request data that can be used in template context.
    """

    params: Mapping[str, Any]
    json: Mapping[str, Any]


class ScoringRule(NamedTuple):
    """
    Represents a database model-agnostic rule to be evaluated.
    """

    operator: Operator
    arguments: list[str]


def score_response(request: TemplatableRequest, rules: list[ScoringRule]) -> float:
    """
    Applies the given response rules to a request and returns the score.
    Scores are between -1 and 1.
    """

    # if there are no rules, this request gets a score of 0
    if not rules:
        return 0

    template_context = {
        "request": request,
    }

    score = 0
    for rule in rules:
        args = [Template(arg).render(**template_context) for arg in rule.arguments]
        evaluator = evaluators[rule.operator]
        if evaluator(*args):
            score += 1
        else:
            score -= 1
    return score / len(rules)


ResponseType = TypeVar("ResponseType")


def find_best_response(
    scoreable_request: TemplatableRequest, response_rules: list[tuple[ResponseType, list[ScoringRule]]]
) -> ResponseType:
    """
    Using the given collection of responses & rules, returns the highest scoring response for the given request.
    """
    # score each response
    scores = [
        (
            score_response(scoreable_request, rules),
            response,
        )
        for response, rules in response_rules
    ]

    # sort by score
    scores = sorted(scores, key=lambda score: score[0], reverse=True)

    # return the best
    return scores[0][1]
