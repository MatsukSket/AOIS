def get_sdnf(vars_list: list[str], table: list[list[int]]) -> str:
    """Строит сднф."""
    if all(row[-1] == 0 for row in table):
        return "сднф не существует."

    minterms = []
    for row in table:
        if row[-1] == 1:
            term = []
            for j in range(len(vars_list)):
                if row[j] == 1:
                    term.append(vars_list[j])
                else:
                    term.append(f"!{vars_list[j]}")
            minterms.append("(" + "&".join(term) + ")")

    return "|".join(minterms)


def get_sknf(vars_list: list[str], table: list[list[int]]) -> str:
    """Строит скнф."""
    if all(row[-1] == 1 for row in table):
        return "скнф не существует"

    maxterms = []
    for row in table:
        if row[-1] == 0:
            term = []
            for j in range(len(vars_list)):
                if row[j] == 0:
                    term.append(vars_list[j])
                else:
                    term.append(f"!{vars_list[j]}")
            maxterms.append("(" + "|".join(term) + ")")

    return "&".join(maxterms)


def get_numeric_sdnf(table: list[list[int]]) -> str:
    """Возвращает числовую форму сднф."""
    indices = [str(i) for i, row in enumerate(table) if row[-1] == 1]
    return f"|({', '.join(indices)})" if indices else "|()"


def get_numeric_sknf(table: list[list[int]]) -> str:
    """Возвращает числовую форму скнф."""
    indices = [str(i) for i, row in enumerate(table) if row[-1] == 0]
    return f"&({', '.join(indices)})" if indices else "&()"


def get_index_form(table: list[list[int]]) -> int:
    """Возвращает индексную форму."""
    binary_str = "".join(str(row[-1]) for row in table)
    return int(binary_str, 2)


if __name__ == '__main__':
    from parser import get_rpn
    from truth_table import generate_truth_table, extract_variables

    expr = "a&b&!c|c"
    print(f"Функция: {expr}\n")

    table = generate_truth_table(expr)
    vars_list = extract_variables(get_rpn(expr))

    print(f"СДНФ: {get_sdnf(vars_list, table)}")
    print(f"СКНФ: {get_sknf(vars_list, table)}")
    print(f"Числовая СДНФ: {get_numeric_sdnf(table)}")
    print(f"Числовая СКНФ: {get_numeric_sknf(table)}")
    print(f"Индексная форма: {get_index_form(table)}")
