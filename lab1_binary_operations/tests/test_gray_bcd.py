import pytest
from src.gray_bcd import *


def test_digit_to_bin_and_back():
    assert digit_to_bin(5) == [0, 1, 0, 1]
    assert bin_to_digit([0, 1, 0, 1]) == 5
    assert digit_to_bin(9) == [1, 0, 0, 1]


def test_gray_and_bin_conversions():
    original_bin = [0, 1, 1, 0]
    gray = bin_to_gray(original_bin)
    assert gray == [0, 1, 0, 1]
    assert gray_to_bin(gray) == original_bin


def test_dec_to_gray_bcd_and_back():
    assert dec_to_gray_bcd(0) == [0, 0, 0, 0]

    val = 45
    gray_bits = dec_to_gray_bcd(val)
    assert gray_bits == [0, 1, 1, 0, 0, 1, 1, 1]

    assert gray_bcd_to_dec(gray_bits) == val


def test_add_4bit_bin():
    a = [0, 1, 0, 1]
    b = [0, 0, 1, 1]
    res, carry = add_4bit_bin(a, b, 0)
    assert res == [1, 0, 0, 0]
    assert carry == 0

    c = [1, 0, 0, 1]
    d = [1, 0, 0, 0]
    res2, carry2 = add_4bit_bin(c, d, 0)
    assert carry2 == 1


def test_add_gray_bcd():
    a = dec_to_gray_bcd(15)
    b = dec_to_gray_bcd(27)
    res = add_gray_bcd(a, b)
    assert gray_bcd_to_dec(res) == 42

    c = dec_to_gray_bcd(99)
    d = dec_to_gray_bcd(2)
    res2 = add_gray_bcd(c, d)
    assert gray_bcd_to_dec(res2) == 101