"""
Defines the rules engine.
"""

import operator
import random
from enum import Enum
from typing import Any, Callable, Mapping, NamedTuple, TypeVar, Union

from api_reflector.templating import default_context, template_env


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
    Operator.EQUAL: operator.eq,
    Operator.NOT_EQUAL: operator.ne,
    Operator.LESS_THAN: lambda x, y: float(x) < float(y),
    Operator.LESS_THAN_EQUAL: lambda x, y: float(x) <= float(y),
    Operator.GREATER_THAN: lambda x, y: float(x) > float(y),
    Operator.GREATER_THAN_EQUAL: lambda x, y: float(x) >= float(y),
    Operator.IS_EMPTY: lambda x: not bool(x),
    Operator.IS_NOT_EMPTY: operator.truth,
    Operator.CONTAINS: operator.contains,
    Operator.NOT_CONTAINS: lambda x, y: y not in x,
}


class TemplatableRequest(NamedTuple):
    """
    A collection of request data that can be used in template context.
    """

    params: Mapping[str, Any]
    json: Mapping[str, Any]
    query: Mapping[str, Any]
    headers: Mapping[str, Any]


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

    template_context: dict[str, Any] = {
        "request": request,
        **default_context,
    }

    for rule in rules:
        args = [template_env.from_string(arg).render(**template_context) for arg in rule.arguments]
        evaluator = evaluators[rule.operator]
        if not evaluator(*args):
            return -1
    return len(rules)


ResponseT = TypeVar("ResponseT")


def find_best_response(
    scoreable_request: TemplatableRequest, response_rules: list[tuple[ResponseT, list[ScoringRule]]]
) -> ResponseT:
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
    scores = [(score, response) for score, response in scores if score >= 0]
    # sort by score
    scores = sorted(scores, key=lambda score: score[0], reverse=True)

    # pick a score from the best options
    return random.choice([score[1] for score in scores if score[0] == scores[0][0]])
