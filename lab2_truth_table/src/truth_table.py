from parser import get_rpn, evaluate_rpn
from config import VARS


def extract_variables(rpn: list[str]) -> list[str]:
    """Извлекает уникальные переменные из ОПЗ и сортирует их по алфавиту."""
    return sorted(list(set([token for token in rpn if token in VARS])))


def generate_truth_table(expr: str) -> list[list[int]]:
    """Генерирует таблицу истинности."""
    rpn = get_rpn(expr)
    vars_list = extract_variables(rpn)

    if not vars_list:
        raise ValueError("В выражении нет переменных.")

    num_vars = len(vars_list)
    total_rows = 2 ** num_vars
    table = []

    for i in range(total_rows):
        binary_str = format(i, f'0{num_vars}b')
        values = [int(bit) for bit in binary_str]

        var_values = dict(zip(vars_list, values))
        result = evaluate_rpn(rpn, var_values)

        row = values + [result]
        table.append(row)

    return table


def print_truth_table(expr: str):
    """Выводит единую таблицу в консоль."""
    try:
        table = generate_truth_table(expr)
        vars_list = extract_variables(expr)
    except ValueError as e:
        print(e)
        return

    header = " ".join(vars_list) + " | f"

    print(header)

    for row in table:
        inputs_str = " ".join(str(val) for val in row[:-1])
        print(f"{inputs_str} | {row[-1]}")


if __name__ == '__main__':
    expr = "a&b&!c|c"
    print(f"Функция: {expr}")
    print_truth_table(expr)