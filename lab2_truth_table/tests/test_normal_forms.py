import pytest
from src.normal_forms import (
    get_sdnf,
    get_sknf,
    get_numeric_sdnf,
    get_numeric_sknf,
    get_index_form
)

def test_get_sdnf_standard():
    vars_list = ["a", "b"]
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    expected = "(!a&b)|(a&!b)"
    assert get_sdnf(vars_list, table) == expected

def test_get_sdnf_none():
    vars_list = ["a"]
    table = [[0, 0], [1, 0]]
    assert get_sdnf(vars_list, table) == "сднф не существует."

def test_get_sknf_standard():
    vars_list = ["a", "b"]
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    expected = "(a|b)&(!a|!b)"
    assert get_sknf(vars_list, table) == expected

def test_get_sknf_none():
    vars_list = ["a"]
    table = [[0, 1], [1, 1]]
    assert get_sknf(vars_list, table) == "скнф не существует"

def test_get_numeric_sdnf():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    assert get_numeric_sdnf(table) == "|(1, 2)"
    assert get_numeric_sdnf([[0, 0], [1, 0]]) == "|()"

def test_get_numeric_sknf():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    assert get_numeric_sknf(table) == "&(0, 3)"
    assert get_numeric_sknf([[0, 1], [1, 1]]) == "&()"

def test_get_index_form():
    table = [[0, 0, 1], [0, 1, 1], [1, 0, 0], [1, 1, 0]]
    assert get_index_form(table) == 12
    assert get_index_form([[0, 0], [1, 1]]) == 1