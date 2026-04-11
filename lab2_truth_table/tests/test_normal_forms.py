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
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    assert get_sdnf(vars_list, table) == "(!a&b)|(a&b)"


def test_get_sdnf_not_exists():
    vars_list = ["a", "b"]
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]]
    assert get_sdnf(vars_list, table) == "сднф не существует."


def test_get_sknf_standard():
    vars_list = ["a", "b"]
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    assert get_sknf(vars_list, table) == "(a|b)&(!a|b)"


def test_get_sknf_not_exists():
    vars_list = ["a", "b"]
    table = [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    assert get_sknf(vars_list, table) == "скнф не существует"


def test_get_numeric_sdnf_standard():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    assert get_numeric_sdnf(table) == "|(1, 3)"


def test_get_numeric_sdnf_empty():
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]]
    assert get_numeric_sdnf(table) == "|()"


def test_get_numeric_sknf_standard():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    assert get_numeric_sknf(table) == "&(0, 2)"


def test_get_numeric_sknf_empty():
    table = [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    assert get_numeric_sknf(table) == "&()"


def test_get_index_form():
    table1 = [[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 1]]
    assert get_index_form(table1) == 5

    table2 = [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]]
    assert get_index_form(table2) == 15