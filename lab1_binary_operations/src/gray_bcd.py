# ==========================================
# 1. БАЗОВЫЕ ФУНКЦИИ ТЕТРАД (4 БИТА)
# ==========================================

def digit_to_bin(digit: int) -> list[int]:
    """Цифра в прямой код."""
    res = [0, 0, 0, 0]
    temp = digit
    for i in range(3, -1, -1):
        res[i] = temp % 2
        temp //= 2
    return res


def bin_to_digit(bits: list[int]) -> int:
    """Прямой код в цифру."""
    return bits[0] * 8 + bits[1] * 4 + bits[2] * 2 + bits[3] * 1


def bin_to_gray(b: list[int]) -> list[int]:
    """Прямой код в код Грея."""
    return [b[0], b[0] ^ b[1], b[1] ^ b[2], b[2] ^ b[3]]


def gray_to_bin(g: list[int]) -> list[int]:
    """Код Грея в проямой код."""
    b0 = g[0]
    b1 = b0 ^ g[1]
    b2 = b1 ^ g[2]
    b3 = b2 ^ g[3]
    return [b0, b1, b2, b3]


def dec_to_gray_bcd(val: int) -> list[int]:
    """Десятичное число в список GrayBCD."""
    if val == 0:
        return [0, 0, 0, 0]

    digits = []
    temp = val
    while temp > 0:
        digits.insert(0, temp % 10)
        temp //= 10

    res = []
    for d in digits:
        res.extend(bin_to_gray(digit_to_bin(d)))

    return res


def gray_bcd_to_dec(bits: list[int]) -> int:
    """Список GrayBCD в десятичное число."""
    total_val = 0

    for i in range(0, len(bits), 4):
        gray_tetra = bits[i: i + 4]
        digit = bin_to_digit(gray_to_bin(gray_tetra))
        total_val = total_val * 10 + digit

    return total_val


def add_4bit_bin(a: list[int], b: list[int], carry: int) -> tuple[list[int], int]:
    """Побитовое сложение 4-битных списков."""
    res = [0, 0, 0, 0]
    c = carry
    for i in range(3, -1, -1):
        s = a[i] + b[i] + c
        res[i] = s % 2
        c = s // 2
    return res, c


def add_gray_bcd(a: list[int], b: list[int]) -> list[int]:
    """Сложение чисел в GrayBCD."""
    a_tetra = a.copy()
    b_tetra = b.copy()

    while len(a_tetra) < len(b_tetra):
        a_tetra = [0, 0, 0, 0] + a_tetra
    while len(b_tetra) < len(a_tetra):
        b_tetra = [0, 0, 0, 0] + b_tetra

    res_tetra = []
    carry = 0

    for i in range(len(a_tetra) - 4, -1, -4):
        gray_1 = a_tetra[i: i + 4]
        gray_2 = b_tetra[i: i + 4]

        bin_1 = gray_to_bin(gray_1)
        bin_2 = gray_to_bin(gray_2)

        sum_bin, c = add_4bit_bin(bin_1, bin_2, carry)
        val = bin_to_digit(sum_bin)

        if c == 1 or val > 9:
            sum_bin, _ = add_4bit_bin(sum_bin, [0, 1, 1, 0], 0)
            c = 1

        res_tetra = bin_to_gray(sum_bin) + res_tetra
        carry = c

    if carry == 1:
        res_tetra = bin_to_gray([0, 0, 0, 1]) + res_tetra

    return res_tetra