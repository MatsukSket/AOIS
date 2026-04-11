def calc_derivative_vector(vector: list[int], var_idx: int, num_vars: int) -> list[int]:
    """Считает производную по одной переменной, разбивая вектор на блоки."""
    deriv = []
    block_size = 2 ** (num_vars - 1 - var_idx)

    for i in range(0, len(vector), 2 * block_size):
        for j in range(block_size):
            idx0 = i + j
            idx1 = i + j + block_size
            deriv.append(vector[idx0] ^ vector[idx1])

    return deriv


def get_mixed_derivative(vars_list: list[str], table: list[list[int]], target_vars: list[str]) -> list[int]:
    """Вычисляет производную многих переменных (или одной)."""
    current_vector = [row[-1] for row in table]
    current_vars = vars_list[:]

    for var in target_vars:
        if var not in current_vars:
            raise ValueError(f"Переменная '{var}' уже продифференцирована или отсутствует.")

        var_idx = current_vars.index(var)
        num_vars = len(current_vars)

        current_vector = calc_derivative_vector(current_vector, var_idx, num_vars)
        current_vars.pop(var_idx)

    return current_vector


def get_fictive_variables(vars_list: list[str], table: list[list[int]]) -> list[str]:
    """Находит фиктивные переменные."""
    fictive = []

    for var in vars_list:
        deriv = get_mixed_derivative(vars_list, table, [var])

        if not any(deriv):
            fictive.append(var)

    return fictive


if __name__ == '__main__':
    from parser import get_rpn
    from truth_table import generate_truth_table, extract_variables

    expr = "a&(b|!b)"
    print(f"Функция: {expr}\n")

    table = generate_truth_table(expr)
    vars_list = extract_variables(get_rpn(expr))

    fictitious = get_fictive_variables(vars_list, table)
    print(f"Фиктивные переменные: {', '.join(fictitious) if fictitious else 'Нет'}")