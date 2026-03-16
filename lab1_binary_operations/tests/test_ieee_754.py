import pytest
from src.ieee_754 import *
from src.consts import IEEE_EXP_SIZE, IEEE_EXP_CONST, BITNESS

def test_exp_conversion():
    bits = dec_to_bin_exp(127)
    assert bin_exp_to_dec([0] + bits) == 127

def test_float_conversion():
    assert float_to_ieee754(0.0) == [0] * BITNESS
    assert ieee754_to_float([0] * BITNESS) == 0.0

    val1 = 5.5
    bits1 = float_to_ieee754(val1)
    assert ieee754_to_float(bits1) == val1

    val2 = -3.25
    bits2 = float_to_ieee754(val2)
    assert ieee754_to_float(bits2) == val2

def test_add_mantissas():
    a = [1, 0, 1]
    b = [0, 1, 1]
    res = add_mantissas(a, b)
    assert res == [1, 0, 0, 0]

def test_add_ieee754():
    a = float_to_ieee754(2.0)
    b = float_to_ieee754(3.0)
    res = add_ieee754(a, b)
    assert len(res) == BITNESS

    c = float_to_ieee754(-2.0)
    res2 = add_ieee754(a, c)
    assert res2 == [0] * BITNESS

def test_mul_mantissas():
    a = [1, 1]
    b = [1, 0]
    res = mul_mantissas(a, b)
    assert isinstance(res, list)

def test_mul_ieee754():
    a = float_to_ieee754(2.0)
    b = float_to_ieee754(3.0)
    res = mul_ieee754(a, b)
    assert len(res) == BITNESS

    zero = float_to_ieee754(0.0)
    res_zero = mul_ieee754(a, zero)
    assert res_zero[1:] == [0] * (BITNESS - 1)

def test_div_mantissas():
    a = [1, 1, 0, 0]
    b = [1, 0]
    res = div_mantissas(a, b)
    assert isinstance(res, list)

def test_div_ieee754(capsys):
    a = float_to_ieee754(6.0)
    b = float_to_ieee754(2.0)
    res = div_ieee754(a, b)
    assert len(res) == BITNESS

    zero = float_to_ieee754(0.0)
    res_zero_div = div_ieee754(a, zero)
    captured = capsys.readouterr()
    assert "На 0 делить нельзя!" in captured.out

    res_zero_num = div_ieee754(zero, a)
    assert res_zero_num[1:] == [0] * (BITNESS - 1)