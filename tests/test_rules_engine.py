"""Unit tests for the rules engine."""


from api_reflector.rules_engine import Operator, evaluators


def test_operators():
    cases = [
        (Operator.EQUAL, (8, 32), False),
        (Operator.EQUAL, (16, 16), True),
        (Operator.LESS_THAN, (16, 8), False),
        (Operator.LESS_THAN, (16, 16), False),
        (Operator.LESS_THAN, (8, 16), True),
        (Operator.LESS_THAN_EQUAL, (16, 8), False),
        (Operator.LESS_THAN_EQUAL, (16, 16), True),
        (Operator.LESS_THAN_EQUAL, (8, 16), True),
        (Operator.GREATER_THAN, (8, 16), False),
        (Operator.GREATER_THAN, (16, 16), False),
        (Operator.GREATER_THAN, (16, 8), True),
        (Operator.GREATER_THAN_EQUAL, (8, 16), False),
        (Operator.GREATER_THAN_EQUAL, (16, 16), True),
        (Operator.GREATER_THAN_EQUAL, (16, 8), True),
        (Operator.IS_EMPTY, ([16],), False),
        (Operator.IS_EMPTY, ([],), True),
        (Operator.IS_EMPTY, ("test",), False),
        (Operator.IS_EMPTY, ("",), True),
        (Operator.IS_NOT_EMPTY, ([],), False),
        (Operator.IS_NOT_EMPTY, ([16],), True),
        (Operator.IS_NOT_EMPTY, ("",), False),
        (Operator.IS_NOT_EMPTY, ("test",), True),
        (Operator.CONTAINS, ([8, 16, 32], 64), False),
        (Operator.CONTAINS, ([8, 16, 32], 16), True),
        (Operator.NOT_CONTAINS, ([8, 16, 32], 16), False),
        (Operator.NOT_CONTAINS, ([8, 16, 32], 64), True),
    ]
    for operator, args, result in cases:
        evaluator = evaluators[operator]
        assert evaluator(*args) == result
