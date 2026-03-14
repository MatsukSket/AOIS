import pytest
from src.integer_math import *
from src.consts import BITNESS

def test_bin_int_to_dec():
    assert bin_int_to_dec([1, 0, 1]) == 5
    assert bin_int_to_dec([0]) == 0

def test_bin_frac_to_dec():
    assert bin_frac_to_dec([1, 0, 1]) == 0.625
    assert bin_frac_to_dec([0, 1]) == 0.25

def test_dec_to_direct_and_back():
    assert bin_direct_to_dec(dec_to_direct(5)) == 5
    assert bin_direct_to_dec(dec_to_direct(-5)) == -5
    assert bin_direct_to_dec(dec_to_direct(0)) == 0

def test_dec_to_ones_complement():
    pos = dec_to_ones_complement(5)
    assert pos[0] == 0
    neg = dec_to_ones_complement(-5)
    assert neg[0] == 1
    assert neg[-1] == 0

def test_twos_complement():
    assert direct_to_twos_complement(dec_to_direct(5)) == dec_to_direct(5)
    neg_tc = dec_to_twos_complement(-5)
    assert neg_tc[0] == 1

def test_add_bin():
    a = dec_to_direct(5)
    b = dec_to_direct(3)
    res = add_bin(a, b)
    assert bin_direct_to_dec(res) == 8

def test_sub_dec():
    res = sub_dec(10, 3)
    assert len(res) == BITNESS

def test_shift_left():
    bits = [0] * BITNESS
    bits[-2] = 1
    shifted = shift_left(bits, 1)
    assert shifted[-3] == 1
    assert shifted[-2] == 0

def test_mul_dec():
    res = mul_dec(3, 2)
    assert bin_direct_to_dec(res) == 6
    res_neg = mul_dec(-3, 2)
    assert bin_direct_to_dec(res_neg) == -6

def test_remove_zeros():
    assert remove_zeros([0, 0, 1, 0, 1]) == [1, 0, 1]
    assert remove_zeros([0, 0, 0]) == [0]

def test_compare_bin():
    assert compare_bin([1, 0], [0, 1]) is True
    assert compare_bin([0, 1], [1, 0]) is False
    assert compare_bin([1, 1], [1, 1]) is True

def test_sub_bin():
    assert sub_bin([1, 0, 1], [0, 1, 1]) == [1, 0]

def test_div_dec(capsys):
    div_dec(10, 0)
    captured = capsys.readouterr()
    assert "На 0 делить нельзя!" in captured.out

    sign, res, rem = div_dec(10, 3)
    assert sign == 0
    assert isinstance(res, list)
    assert isinstance(rem, list)