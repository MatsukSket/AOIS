from src.consts import *


def bin_int_to_dec(bits: list[int]) -> int:
    res = 0
    for bit in bits:
        res = res * 2 + bit
    return res


def bin_frac_to_dec(bits: list[int]) -> int:
    res = 0.0
    for i, bit in enumerate(bits):
        if bit == 1:
            res += 2 ** (-(i+1))
    return res



def dec_to_direct(dec_val: int) -> list[int]:
    """Прямой код."""
    bits = [0] * BITNESS
    if dec_val < 0:
        bits[0] = 1

    val = abs(dec_val)
    i = BITNESS - 1
    while val > 0 and i > 0:
        bits[i] = val % 2
        val = val // 2
        i -= 1

    return bits


def bin_direct_to_dec(bits: list[int]) -> int:
    """Прямой код в десятичное число."""
    res = 0
    for bit in bits[1:]:
        res = res * 2 + bit

    if bits[0] == 1:
        res *= -1

    return res


def dec_to_ones_complement(dec_val: int) -> list[int]:
    """Целое число в обратный код."""
    bits = dec_to_direct(dec_val)

    if bits[0] == 1:
        for i in range(1, BITNESS):
            bits[i] = 1 - bits[i]

    return bits


def direct_to_twos_complement(bits: list[int]) -> list[int]:
    """Из прямого кода в дополнительный и наоборот."""
    if bits[0] == 0:
        return bits.copy()

    res = bits.copy()
    x = 0
    for i in range(BITNESS - 1, 0, -1):
        if bits[i] == 1:
            x = i
            break

    for i in range(1, x):
        res[i] = 1 - res[i]

    return res


def dec_to_twos_complement(dec_val: int) -> list[int]:
    """Целое число в дополнительный код."""
    bits = dec_to_direct(dec_val)

    bits = direct_to_twos_complement(bits)

    return bits


def add_bin(a: list[int], b: list[int]) -> list[int]:
    """Принимает два списка битов, возвращает их сумму."""
    carry = 0
    res = [0] * BITNESS

    for i in range(BITNESS - 1, -1, -1):
        cur_sum = a[i] + b[i] + carry
        res[i] = cur_sum % 2
        carry = cur_sum // 2

    return res


def sub_dec(a: int, b: int) -> list[int]:
    """Первый аргумент - уменьшаемое, второй - вычитаемое, возвращает разность."""
    return add_bin(
        dec_to_twos_complement(a),
        dec_to_twos_complement(-b)
    )


def shift_left(bits: list[int], count: int) -> list[int]:
    res = [0] * BITNESS

    for i in range(1, BITNESS - count):
        res[i] = bits[i + count]

    return res

def mul_dec(a: int, b: int) -> list[int]:
    """Умножение левым сдвигом."""
    a_bits = dec_to_direct(a)
    b_bits = dec_to_direct(b)
    sign = a_bits[0] ^ b_bits[0]
    res = [0] * BITNESS

    a_bits[0] = 0

    for i in range(BITNESS - 1, 0, -1):
        if b_bits[i] == 1:
            shift_amount = BITNESS - 1 - i
            shifted = shift_left(a_bits, shift_amount)
            res = add_bin(res, shifted)

    res[0] = sign
    return res


def remove_zeros(bits: list[int]) -> list[int]:
    """Возвращает список без нулей в первых позициях и знакового бита."""
    for i, bit in enumerate(bits):
        if bit == 1:
            return bits[i:]
    return [0]


def compare_bin(a: list[int], b: list[int]) -> bool:
    """a >= b"""
    max_len = max(len(a), len(b))

    a_padded = [0] * (max_len - len(a)) + a
    b_padded = [0] * (max_len - len(b)) + b

    for i in range(max_len):
        if a_padded[i] < b_padded[i]:
            return False
        if a_padded[i] > b_padded[i]:
            return True

    return True


def sub_bin(a: list[int], b: list[int]) -> list[int]:
    """Бинарное вычитание. Возвращает разность БЕЗ знакового бита и первых нулей."""
    b = [0] * (len(a) - len(b)) + b

    res = []
    carry = 0

    for i in range(len(a) - 1, -1, -1):
        diff = a[i] - b[i] - carry
        if diff < 0:
            diff += 2
            carry = 1
        else:
            carry = 0
        res.insert(0, diff)

    return remove_zeros(res)


def div_dec(a: int, b:int) -> tuple[int, list[int], list[int]]:
    """Первый аргумент - делимое, второй - делитель, возвращает частное и остаток"""
    if b == 0:
        print('На 0 делить нельзя!')
        return 0, [0], [0]

    a_bits = dec_to_direct(a)
    b_bits = dec_to_direct(b)
    sign = a_bits[0] ^ b_bits[0]
    a_clean = remove_zeros(a_bits[1:])
    b_clean = remove_zeros(b_bits[1:])

    res = []
    remainder = []    # остаток
    cur = []

    for bit in a_clean:
        cur.append(bit)
        cur = remove_zeros(cur)

        if compare_bin(cur, b_clean):    # cur >= b_clean
            res.append(1)
            cur = sub_bin(cur, b_clean)
        elif res:
            res.append(0)

    res += [0] * (BITNESS - len(res))

    for _ in range(17):
        if not cur and cur == [0]:
            remainder.append(0)
            continue

        cur.append(0)
        cur = remove_zeros(cur)

        if compare_bin(cur, b_clean):
            remainder.append(1)
            cur = sub_bin(cur, b_clean)
        else:
            remainder.append(0)

    return sign, res, remainder

