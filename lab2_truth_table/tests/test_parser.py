import pytest
from src.parser import standardize_expr, is_var, is_valid_expression, get_rpn, evaluate_rpn

@pytest.mark.parametrize("input_str, expected", [
    ("a -> b", "a>b"),
    ("a & b | !c", "a&b|!c"),
    ("  a  |  b  ", "a|b"),
])
def test_standardize_expr(input_str, expected):
    assert standardize_expr(input_str) == expected

def test_is_var():
    assert is_var('a') is True
    assert is_var('e') is True
    assert is_var('z') is False
    assert is_var('&') is False

def test_is_valid_expression_valid():
    is_valid_expression("a&b|!c>(d~e)")

def test_is_valid_expression_invalid_char():
    with pytest.raises(ValueError, match="Недопустимый символ"):
        is_valid_expression("a&b$c")

def test_is_valid_expression_consecutive_vars():
    with pytest.raises(ValueError, match="Подряд идущие переменные"):
        is_valid_expression("ab&c")

@pytest.mark.parametrize("expr, expected_rpn", [
    ("a&b", ["a", "b", "&"]),
    ("!a|b", ["a", "!", "b", "|"]),
    ("a&b|c", ["a", "b", "&", "c", "|"]),
    ("a|(b&c)", ["a", "b", "c", "&", "|"]),
    ("a->b~c", ["a", "b", ">", "c", "~"]),
])
def test_get_rpn_logic(expr, expected_rpn):
    assert get_rpn(expr) == expected_rpn

def test_get_rpn_mismatched_brackets():
    with pytest.raises(ValueError, match="Пропущена открывающая скобка"):
        get_rpn("a&b)")
    with pytest.raises(ValueError, match="пропущена закрывающая скобка"):
        get_rpn("(a&b")

def test_evaluate_rpn_simple():
    rpn = ["a", "b", "&"]
    assert evaluate_rpn(rpn, {'a': 1, 'b': 1}) == 1
    assert evaluate_rpn(rpn, {'a': 1, 'b': 0}) == 0

def test_evaluate_rpn_complex():
    # !a | (b ~ c)
    rpn = ["a", "!", "b", "c", "~", "|"]
    # a=1 (!1=0), b=1, c=1 (1~1=1). 0|1 = 1
    assert evaluate_rpn(rpn, {'a': 1, 'b': 1, 'c': 1}) == 1
    # a=1, b=1, c=0 (1~0=0). 0|0 = 0
    assert evaluate_rpn(rpn, {'a': 1, 'b': 1, 'c': 0}) == 0

def test_evaluate_rpn_constants():
    rpn = ["1", "0", "|"]
    assert evaluate_rpn(rpn, {}) == 1