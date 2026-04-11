import pytest
from src.analisis import (
    build_next_layer,
    get_zhegalkin_coefficients,
    build_zhegalkin_string,
    get_zhegalkin,
    get_post_classes
)

def test_build_next_layer():
    assert build_next_layer([0, 1, 1, 0]) == [1, 0, 1]
    assert build_next_layer([1, 1]) == [0]
    assert build_next_layer([0, 0, 0]) == [0, 0]

def test_get_zhegalkin_coefficients():
    assert get_zhegalkin_coefficients([0, 0, 0, 1]) == [0, 0, 0, 1]
    assert get_zhegalkin_coefficients([1, 1, 1, 1]) == [1, 0, 0, 0]
    assert get_zhegalkin_coefficients([0, 1, 1, 0]) == [0, 1, 1, 0]

def test_build_zhegalkin_string():
    assert build_zhegalkin_string(["a", "b"], [1, 0, 0, 1]) == "1 ⊕ ab"
    assert build_zhegalkin_string(["a", "b"], [0, 1, 1, 0]) == "b ⊕ a"
    assert build_zhegalkin_string(["a", "b"], [0, 0, 0, 0]) == "0"

def test_get_zhegalkin_integration():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]]
    poly, coeffs = get_zhegalkin(["a", "b"], table)
    assert poly == "b ⊕ a"
    assert coeffs == [0, 1, 1, 0]

def test_get_post_classes_complex():
    table = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]]
    coeffs = [0, 0, 0, 1]
    res = get_post_classes(table, coeffs)
    assert res["T0"] is True
    assert res["T1"] is True
    assert res["S"] is False
    assert res["M"] is True
    assert res["L"] is False

def test_get_post_classes_linear_self_dual():
    table = [[0, 1], [1, 0]]
    coeffs = [1, 1]
    res = get_post_classes(table, coeffs)
    assert res["T0"] is False
    assert res["T1"] is False
    assert res["S"] is True
    assert res["M"] is False
    assert res["L"] is True

def test_get_post_classes_monotonic_check():
    table = [[0, 0, 0], [0, 1, 1], [1, 0, 0], [1, 1, 0]]
    coeffs = [0, 1, 0, 1]
    res = get_post_classes(table, coeffs)
    assert res["M"] is False