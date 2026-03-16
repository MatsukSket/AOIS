from src.consts import *
from src.integer_math import compare_bin, sub_bin

def dec_to_bin_exp(val: int) -> list[int]:
    """Перевод десятичной величины exp в нужный формат."""
    res = [0] * IEEE_EXP_SIZE

    for i in range(IEEE_EXP_SIZE-1, -1, -1):
        res[i] = val % 2
        val //= 2

    return res


def bin_exp_to_dec(bits: list[int]) -> int:
    """Получение значения exp из числа в ieee форме."""
    res = 0
    for bit in bits[1:IEEE_EXP_SIZE+1]:
        res = res * 2 + bit
    return res


def float_to_ieee754(val: float) -> list[int]:
    """Принимает число с плавающей запятой и переводит его в формат IEEE-754.
    Возвращает список битов: знаковый бит, экспонента(8 бит), мантисса(23 бита)."""
    sign = 1 if val < 0 else 0
    val = abs(val)

    if val == 0:
        return [0] * BITNESS

    int_part = int(val)
    frac_part = val - int_part

    int_bits = []
    while int_part > 0:
        int_bits.insert(0, int_part % 2)
        int_part //= 2

    frac_bits = []
    while frac_part > 0 and len(frac_bits) < 30:
        frac_part *= 2
        if frac_part >= 1:
            frac_bits.append(1)
            frac_part -= 1
        else:
            frac_bits.append(0)

    exp = IEEE_EXP_CONST
    if int_bits:
        exp += len(int_bits) - 1
        mantissa_bits = int_bits[1:] + frac_bits
    else:
        if 1 in frac_bits:
            first_one = frac_bits.index(1)
            exp -= first_one + 1
            mantissa_bits = frac_bits[first_one + 1:]
        else:
            exp = 0
            mantissa_bits = []

    exp_bits = dec_to_bin_exp(exp)

    mantissa_bits = mantissa_bits[:IEEE_MANTISSA_SIZE]
    mantissa_bits += [0] * (IEEE_MANTISSA_SIZE - len(mantissa_bits))

    return [sign] + exp_bits + mantissa_bits


def ieee754_to_float(bits: list[int]) -> float:
    """Принимает число в виде списка битов в формате IEEE-754.
    Возвращает это же число во float."""
    if 1 not in bits[1:]:
        return 0.0

    sign = -1 if bits[0] else 1
    exp = bin_exp_to_dec(bits)
    exp -= IEEE_EXP_CONST

    mantissa = 1.0
    for i, bit in enumerate(bits[IEEE_EXP_SIZE+1:]):
        if bit:
            mantissa += 2 ** (-(i + 1))

    return sign * mantissa * (2 ** exp)


def add_mantissas(a: list[int], b: list[int]) -> list[int]:
    """Сложение мантисс. Возвращает их сумму.
    Не нормализует длину, но может работать со списками разных длин."""
    max_len = max(len(a), len(b))

    a_pad = [0] * (max_len - len(a)) + a
    b_pad = [0] * (max_len - len(b)) + b

    res = []
    carry = 0

    for i in range(max_len - 1, -1, -1):
        cur_sum = a_pad[i] + b_pad[i] + carry
        res.insert(0, cur_sum % 2)
        carry = cur_sum // 2
    if carry:
        res.insert(0, 1)

    return res


def add_ieee754(a: list[int], b: list[int]) -> list[int]:
    """Сложение чисел в формате IEEE-754. Возвращает число в этом же формате."""
    exp_a = bin_exp_to_dec(a)
    exp_b = bin_exp_to_dec(b)
    exp_res = max(exp_a, exp_b)

    mantissa_a = [1] + a[IEEE_EXP_SIZE+1:]
    mantissa_b = [1] + b[IEEE_EXP_SIZE+1:]

    diff = abs(exp_a - exp_b)# ... выравнивание (diff) ...
    if exp_a > exp_b:
        mantissa_a = mantissa_a + [0] * diff
        mantissa_b = [0] * diff + mantissa_b
    if exp_b > exp_a:
        mantissa_b = mantissa_b + [0] * diff
        mantissa_a = [0] * diff + mantissa_a

    base_len = len(mantissa_a)

    if a[0] == b[0]:
        sign_res = a[0]
        mantissas_sum = add_mantissas(mantissa_a, mantissa_b)

        if len(mantissas_sum) > base_len:
            exp_res += 1
    else:
        if compare_bin(mantissa_a, mantissa_b):
            sign_res = a[0]
            mantissas_sum = sub_bin(mantissa_a, mantissa_b)
        else:
            sign_res = b[0]
            mantissas_sum = sub_bin(mantissa_b, mantissa_a)

        if 1 not in mantissas_sum:
            return [0] * BITNESS

        exp_res -= base_len - len(mantissas_sum)

    exp_bits = dec_to_bin_exp(exp_res)
    mantissa_res = mantissas_sum[1:IEEE_MANTISSA_SIZE+1]
    mantissa_res += [0] * (IEEE_MANTISSA_SIZE - len(mantissa_res))

    return [sign_res] + exp_bits + mantissa_res


def mul_mantissas(a: list[int], b: list[int]) -> list[int]:
    """Умножение мантисс. Возвращает произведение."""
    res = [0]

    for i in range(len(b)):
        if b[i] == 1:
            shift = len(b) - 1 - i
            shifted_a = a + [0] * shift
            res = add_mantissas(res, shifted_a)

    return res


def mul_ieee754(a: list[int], b: list[int]) -> list[int]:
    """Умножение чисел в формате IEEE-754."""
    if 1 not in a[1:] or 1 not in b[1:]:
        sign_res = a[0] ^ b[0]
        return [sign_res] + [0] * (BITNESS - 1)

    sign_res = a[0] ^ b[0]

    exp_a = bin_exp_to_dec(a)
    exp_b = bin_exp_to_dec(b)
    exp_res = exp_a + exp_b - IEEE_EXP_CONST

    mantissa_a = [1] + a[IEEE_EXP_SIZE+1:]
    mantissa_b = [1] + b[IEEE_EXP_SIZE+1:]

    mantissa_prod = mul_mantissas(mantissa_a, mantissa_b)

    target_len = (IEEE_MANTISSA_SIZE+1) * 2

    if len(mantissa_prod) == target_len:
        exp_res += 1

    mantissa_res = mantissa_prod[1:IEEE_MANTISSA_SIZE+1]
    mantissa_res += [0] * (IEEE_MANTISSA_SIZE - len(mantissa_res))
    exp_bits = dec_to_bin_exp(exp_res)

    return [sign_res] + exp_bits + mantissa_res


def div_mantissas(a: list[int], b: list[int]) -> list[int]:
    """Деление мантисс. Возвращает список битов частного."""
    res = []
    cur = a.copy()

    for _ in range(IEEE_MANTISSA_SIZE + 2):
        if compare_bin(cur, b):
            res.append(1)
            cur = sub_bin(cur, b)
        else:
            res.append(0)
        cur.append(0)

    return res


def div_ieee754(a: list[int], b: list[int]) -> list[int]:
    """Деление чисел в формате IEEE-754. а - делимое, b - делитель"""
    if 1 not in b[1:]:
        print("На 0 делить нельзя!")
        return [0] * BITNESS

    if 1 not in a[1:]:
        return [a[0] ^ b[0]] + [0] * (BITNESS - 1)

    sign_res = a[0] ^ b[0]

    exp_a = bin_exp_to_dec(a)
    exp_b = bin_exp_to_dec(b)
    exp_res = exp_a - exp_b + IEEE_EXP_CONST

    mantissa_a = [1] + a[IEEE_EXP_SIZE+1:]
    mantissa_b = [1] + b[IEEE_EXP_SIZE+1:]

    mantissa_div = div_mantissas(mantissa_a, mantissa_b)

    if mantissa_div[0] == 1:
        mantissa_res = mantissa_div[1:IEEE_MANTISSA_SIZE+1]
    else:
        exp_res -= 1
        mantissa_res = mantissa_div[2:IEEE_MANTISSA_SIZE+2]

    mantissa_res += [0] * (IEEE_MANTISSA_SIZE - len(mantissa_res))
    exp_bits = dec_to_bin_exp(exp_res)

    return [sign_res] + exp_bits + mantissa_res