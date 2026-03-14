from src.integer_math import *
from src.ieee_754 import *
from src.gray_bcd import *


def format_bits(bits: list[int]) -> str:
    return "".join(str(b) for b in bits)


def integer_operations():
    """Работа с целыми числами в прямом и дополнительном кодах."""
    try:
        a = int(input("Введите первое целое число A: "))
        b = int(input("Введите второе целое число B: "))
    except ValueError:
        print("Вводите только целые числа!")
        return

    for name, val in [("A", a), ("B", b)]:
        print(f"\nЧисло {name} = {val}:")
        print(f"        Прямой код: {format_bits(dec_to_direct(val))}")
        print(f"      Обратный код: {format_bits(dec_to_ones_complement(val))}")
        print(f"Дополнительный код: {format_bits(dec_to_twos_complement(val))}")
    print('')

    sum_bits = add_bin(dec_to_twos_complement(a), dec_to_twos_complement(b))
    print(f"             Сумма: {format_bits(sum_bits)} {a+b}")

    sub_bits = sub_dec(a, b)
    print(f"          Разность: {format_bits(sub_bits)} {a-b}")

    mul_bits = mul_dec(a, b)
    print(f"      Произведение: {format_bits(mul_bits)} {a*b}")

    if b == 0:
        print("На 0 делить нельзя!")
    else:
        sign, q_bits, rem_bits = div_dec(a, b)
        sign_str = "-" if sign == 1 else "+"
        print(f"   Знак результата: {sign_str}")
        print(f"       Целая часть: {format_bits(q_bits)} {bin_int_to_dec(q_bits)}")
        print(f"     Дробная часть: {format_bits(rem_bits)}                {bin_frac_to_dec(rem_bits)}")


def float_operations():
    """Работа с числами с плавающей запятой в формате IEEE-754."""
    try:
        a_val = float(input("Введите первое число A: "))
        b_val = float(input("Введите второе число B: "))
    except ValueError:
        print("Вводите только числа!")
        return

    a = float_to_ieee754(a_val)
    b = float_to_ieee754(b_val)

    for name, val, bits in [("A", a_val, a), ("B", b_val, b)]:
        print(f"\nЧисло {name} = {val}:")
        print(f"{bits[0]} {format_bits(bits[1:9])} {format_bits(bits[9:])}")
    print('')

    res_add = add_ieee754(a, b)
    print(f"       Сумма: {res_add[0]} {format_bits(res_add[1:9])} {format_bits(res_add[9:])} {ieee754_to_float(res_add)}")

    b_inv = b.copy()
    b_inv[0] = 1 - b_inv[0]
    res_sub = add_ieee754(a, b_inv)
    print(f"    Разность: {res_sub[0]} {format_bits(res_sub[1:9])} {format_bits(res_sub[9:])} {ieee754_to_float(res_sub)}")

    res_mul = mul_ieee754(a, b)
    print(f"Произведение: {res_mul[0]} {format_bits(res_mul[1:9])} {format_bits(res_mul[9:])} {ieee754_to_float(res_mul)}")

    if b_val == 0:
        print("На 0 делить нельзя!")
    else:
        res_div = div_ieee754(a, b)
        print(f"     Частное: {res_div[0]} {format_bits(res_div[1:9])} {format_bits(res_div[9:])} {ieee754_to_float(res_div)}")


def gray_bcd_operations():
    """Работа с числами в формате GrayBCD."""

    def format_bits(bits: list[int]) -> str:
        # Склеиваем биты в строку
        res = "".join(str(b) for b in bits)
        # Разбиваем на блоки по 4 бита через пробел для читаемости
        blocks = [res[i:i + 4] for i in range(0, len(res), 4)]
        return " ".join(blocks)

    print("\n" + "=" * 45)
    print(" GRAY BCD АРИФМЕТИКА (ПОЛОЖИТЕЛЬНЫЕ ЧИСЛА) ")
    print("=" * 45)

    try:
        a_val = int(input("Введите первое положительное число (A): "))
        b_val = int(input("Введите второе положительное число (B): "))
        if a_val < 0 or b_val < 0:
            print("Только положительные числа!")
            return

    except ValueError:
        print("Ошибка: Вводите только целые числа!")
        return

    # 1. Перевод в Gray BCD
    a = dec_to_gray_bcd(a_val)
    b = dec_to_gray_bcd(b_val)

    # 2. Вывод представления в памяти
    for name, val, bits in [("A", a_val, a), ("B", b_val, b)]:
        print(f"\nЧисло {name} = {val}:")
        print(f"Gray BCD: {format_bits(bits)}")

    print('\n')

    # 3. Вызов нашей ручной функции сложения
    res_add = add_gray_bcd(a, b)

    # Обратный перевод для проверки
    res_dec = gray_bcd_to_dec(res_add)

    print(f"          Сумма: {format_bits(res_add)}  ({res_dec})")

    # Сверяем с обычным питоновским сложением
    if res_dec == (a_val + b_val):
        print("          Статус: УСПЕШНО (результаты совпадают)")
    else:
        print(f"          Статус: ОШИБКА (ожидалось {a_val + b_val})")

    print("\n" + "=" * 45 + "\n")

def main():
    while True:
        print('\n' + '=' * 30)
        print('Выберите тип операций:')
        print('1. Целые числа')
        print('2. IEEE-754')
        print('3. Gray BCD')
        print('0. Выход')
        print('=' * 30 + '\n')

        choice = int(input('Выберите тип операций: '))

        if choice == 1:
            integer_operations()
        elif choice == 2:
            float_operations()
        elif choice == 3:
            gray_bcd_operations()
        elif choice == 0:
            print('Завершение работы.')
            break
        else:
            print("Неверный ввод. Введите число от 0 до 3")

if __name__ == '__main__':
    main()