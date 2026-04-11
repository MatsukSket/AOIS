from src.parser import get_rpn, evaluate_rpn
from src.config import VARS


def extract_variables(rpn: list[str]) -> list[str]:
    """Извлекает уникальные переменные из ОПЗ и сортирует их по алфавиту."""
    return sorted(list(set([token for token in rpn if token in VARS])))


def generate_truth_table(rpn: list[str], vars_list: list[str]) -> list[list[int]]:
    """Генерирует таблицу истинности."""
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

        table.append(values + [result])

    return table


def print_truth_table(table: list[list[int]], vars_list: list[str]):
    """Выводит единую таблицу в консоль."""
    header = " ".join(vars_list) + " | f"
    print(header)
    for row in table:
        inputs_str = " ".join(str(val) for val in row[:-1])
        print(f"{inputs_str} | {row[-1]}")


if __name__ == '__main__':
    expr = "a&b&!c|c"
    print(f"Функция: {expr}")
    rpn = get_rpn(expr)
    vars = extract_variables(rpn)
    truth_table = generate_truth_table(rpn, vars)
    print_truth_table(truth_table, vars)