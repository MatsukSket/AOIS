import pytest
from src.calculus import calc_derivative_vector, get_mixed_derivative, get_fictive_variables

def test_calc_derivative_vector_first_var():
    vector = [0, 0, 1, 1]
    res = calc_derivative_vector(vector, 0, 2)
    assert res == [1, 1]

def test_calc_derivative_vector_second_var():
    vector = [0, 1, 0, 1]
    res = calc_derivative_vector(vector, 1, 2)
    assert res == [1, 1]

def test_get_mixed_derivative_single():
    vars_list = ["a", "b"]
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 1], [1, 1, 1]]
    res = get_mixed_derivative(vars_list, table, ["a"])
    assert res == [1, 1]

def test_get_mixed_derivative_multiple():
    vars_list = ["a", "b"]
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
    res = get_mixed_derivative(vars_list, table, ["a", "b"])
    assert res == [1]

def test_get_mixed_derivative_error():
    vars_list = ["a", "b"]
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]]
    with pytest.raises(ValueError, match="отсутствует"):
        get_mixed_derivative(vars_list, table, ["c"])
    with pytest.raises(ValueError, match="уже продифференцирована"):
        get_mixed_derivative(vars_list, table, ["a", "a"])

def test_get_fictive_variables_none():
    vars_list = ["a", "b"]
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
    assert get_fictive_variables(vars_list, table) == []

def test_get_fictive_variables_exist():
    vars_list = ["a", "b"]
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 1], [1, 1, 1]]
    assert get_fictive_variables(vars_list, table) == ["b"]

def test_get_fictive_variables_all():
    vars_list = ["a"]
    table = [[0, 1], [1, 1]]
    assert get_fictive_variables(vars_list, table) == ["a"]