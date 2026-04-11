import pytest
from src.truth_table import extract_variables, generate_truth_table, print_truth_table

def test_extract_variables():
    assert extract_variables(["a", "b", "&"]) == ["a", "b"]
    assert extract_variables(["a", "!", "a", "|"]) == ["a"]
    assert extract_variables(["1", "0", "|"]) == []

def test_generate_truth_table_logic():
    rpn = ["a", "b", "|"]
    vars_list = ["a", "b"]
    table = generate_truth_table(rpn, vars_list)
    assert len(table) == 4
    assert table[0] == [0, 0, 0]
    assert table[1] == [0, 1, 1]
    assert table[2] == [1, 0, 1]
    assert table[3] == [1, 1, 1]

def test_generate_truth_table_single_var():
    rpn = ["a", "!"]
    vars_list = ["a"]
    table = generate_truth_table(rpn, vars_list)
    assert len(table) == 2
    assert table[0] == [0, 1]
    assert table[1] == [1, 0]

def test_generate_truth_table_error():
    with pytest.raises(ValueError, match="В выражении нет переменных."):
        generate_truth_table(["1", "0", "&"], [])

def test_print_truth_table_output(capsys):
    table = [[0, 0, 0], [1, 1, 1]]
    vars_list = ["a", "b"]
    print_truth_table(table, vars_list)
    captured = capsys.readouterr()
    lines = captured.out.strip().split('\n')
    assert lines[0] == "a b | f"
    assert lines[1] == "0 0 | 0"
    assert lines[2] == "1 1 | 1"