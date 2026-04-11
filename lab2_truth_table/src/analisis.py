def build_next_layer(cur_row: list[int]) -> list[int]:
    """Строит следующий слой треугольника Жегалкина."""
    return [(cur_row[j] ^ cur_row[j + 1]) for j in range(len(cur_row) - 1)]


def get_zhegalkin_coefficients(f_vals: list[int]) -> list[int]:
    """Находит коэффициенты полинома Жегалкина методом треугольника."""
    triangle = [f_vals]
    for _ in range(len(f_vals) - 1):
        next_row = build_next_layer(triangle[-1])
        triangle.append(next_row)

    return [row[0] for row in triangle]


def build_zhegalkin_string(vars_list: list[str], coeffs: list[int]) -> str:
    """Строит полином Жегалкина на основе коэффициентов."""
    terms = []
    for i, coef in enumerate(coeffs):
        if coef == 1:
            if i == 0:
                terms.append("1")
            else:
                # Определяем, какие переменные входят в конъюнкцию по битам индекса
                bin_str = format(i, f'0{len(vars_list)}b')
                term_vars = [vars_list[j] for j, bit in enumerate(bin_str) if bit == '1']
                terms.append("".join(term_vars))

    return " ⊕ ".join(terms) if terms else "0"


def get_zhegalkin(vars_list: list[str], table: list[list[int]]) -> tuple[str, list[int]]:
    """Возвращает полином жигалкина и коэффициенты."""
    f_vals = [row[-1] for row in table]

    coeffs = get_zhegalkin_coefficients(f_vals)
    zhegalkin_str = build_zhegalkin_string(vars_list, coeffs)

    return zhegalkin_str, coeffs


def get_post_classes(table: list[list[int]], zhegalkin_coeffs: list[int]) -> dict[str, bool]:
    """
    Определяет принадлежность функции к пяти классам Поста:
    T0 (сохраняет 0), T1 (сохраняет 1), S (самодвойственная), M (монотонная), L (линейная).
    """
    f_vals = [row[-1] for row in table]
    n = len(f_vals)

    # T0
    t0 = (f_vals[0] == 0)

    # T1
    t1 = (f_vals[-1] == 1)

    # S - самодвойственность
    s = all(f_vals[i] != f_vals[n - 1 - i] for i in range(n // 2))

    # M - монотонность
    m = True
    for i in range(n):
        for j in range(i + 1, n):
            if (i & j) == i:
                if f_vals[i] > f_vals[j]:
                    m = False
                    break
        if not m:
            break

    # L - линейность
    l = True
    for i, coef in enumerate(zhegalkin_coeffs):
        if coef == 1:
            if bin(i).count('1') > 1:
                l = False
                break

    return {"T0": t0, "T1": t1, "S": s, "M": m, "L": l}


if __name__ == '__main__':
    from parser import get_rpn
    from truth_table import generate_truth_table, extract_variables

    expr = "a&b&!c|c"
    print(f"Функция: {expr}\n")

    table = generate_truth_table(expr)
    vars_list = extract_variables(get_rpn(expr))

    zhegalkin_str, coeffs = get_zhegalkin(vars_list, table)
    print(f"Полином Жегалкина: {zhegalkin_str}")

    classes = get_post_classes(table, coeffs)
    print("\nКлассы Поста:")
    for cls, is_in_class in classes.items():
        symbol = "+" if is_in_class else "-"
        print(f"{cls}: {symbol}")