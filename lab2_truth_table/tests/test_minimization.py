import pytest
from src.minimization import (
    get_bin_implicants, get_bit_diff, merge_implicants,
    calculate_method, covers, get_min_cover,
    format_string_formula, tabular_calc_method,
    generate_gray_code, print_karnaugh_map
)

def test_get_bin_implicants():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    assert get_bin_implicants(table, True) == ["01", "10"]
    assert get_bin_implicants(table, False) == ["00", "11"]

def test_get_bit_diff():
    assert get_bit_diff("101", "100") == 2
    assert get_bit_diff("101", "011") == -1
    assert get_bit_diff("111", "111") == -1

def test_merge_implicants():
    imps = ["101", "100", "011"]
    new_imps, primes = merge_implicants(imps)
    assert "10-" in new_imps
    assert "011" in primes

def test_calculate_method(capsys):
    table = [[0, 0, 1], [0, 1, 1], [1, 0, 0], [1, 1, 0]]
    vars_list = ["a", "b"]
    res = calculate_method(table, vars_list, True)
    assert "0-" in res
    captured = capsys.readouterr()
    assert "МДНФ" in captured.out

def test_covers():
    assert covers("1-0", "110") is True
    assert covers("1-0", "100") is True
    assert covers("1-0", "010") is False

def test_get_min_cover():
    primes = ["1-", "-1"]
    minterms = ["10", "11", "01"]
    res = get_min_cover(primes, minterms)
    assert len(res) == 2
    assert "1-" in res
    assert "-1" in res

def test_format_string_formula():
    vars_list = ["a", "b"]
    assert format_string_formula(["1-"], vars_list, True) == "(a)"
    assert format_string_formula(["01"], vars_list, True) == "(!a & b)"
    assert format_string_formula(["1-"], vars_list, False) == "(!a)"
    assert format_string_formula([], vars_list, True) == "0"
    assert format_string_formula([], vars_list, False) == "1"

def test_tabular_calc_method(capsys):
    table = [[0, 0, 1], [1, 1, 0]]
    tabular_calc_method(table, ["00"], ["a", "b"], True)
    captured = capsys.readouterr()
    assert "=== ДНФ ===" in captured.out
    assert "X" in captured.out

def test_tabular_calc_method_empty(capsys):
    tabular_calc_method([[0, 0], [1, 0]], [], ["a"], True)
    captured = capsys.readouterr()
    assert "Функция константа" in captured.out

def test_generate_gray_code():
    assert generate_gray_code(0) == [""]
    assert generate_gray_code(1) == ["0", "1"]
    assert generate_gray_code(2) == ["00", "01", "11", "10"]

def test_print_karnaugh_map(capsys):
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    print_karnaugh_map(table, ["a", "b"])
    captured = capsys.readouterr()
    assert "Карта Карно" in captured.out
    assert "0" in captured.out
    assert "1" in captured.out

def test_print_karnaugh_map_invalid(capsys):
    print_karnaugh_map([], ["a", "b", "c", "d", "e", "f"])
    captured = capsys.readouterr()
    assert "не поддерживается" in captured.out

def test_print_karnaugh_map_1_var(capsys):
    table = [[0, 0], [1, 1]]
    print_karnaugh_map(table, ["a"])
    captured = capsys.readouterr()
    assert "f" in captured.out