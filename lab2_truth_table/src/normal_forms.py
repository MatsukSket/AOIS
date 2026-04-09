def get_sdnf(vars_list: list[str], table: list[list[int]]) -> str:
    """Строит СДНФ на основе единой таблицы истинности."""
    # Если функция всегда равна 0, СДНФ построить нельзя
    if all(row[-1] == 0 for row in table):
        return "Тождественный ноль (СДНФ не существует)"

    minterms = []
    for row in table:
        result = row[-1]

        # Для СДНФ ищем строки с результатом 1
        if result == 1:
            term = []
            for j in range(len(vars_list)):
                # 1 -> переменная, 0 -> !переменная
                if row[j] == 1:
                    term.append(vars_list[j])
                else:
                    term.append(f"!{vars_list[j]}")
            # Собираем терм через И
            minterms.append("(" + " & ".join(term) + ")")

    # Соединяем термы через ИЛИ
    return " | ".join(minterms)


def get_sknf(vars_list: list[str], table: list[list[int]]) -> str:
    """Строит СКНФ на основе единой таблицы истинности."""
    # Если функция всегда равна 1, СКНФ построить нельзя
    if all(row[-1] == 1 for row in table):
        return "Тождественная единица (СКНФ не существует)"

    maxterms = []
    for row in table:
        result = row[-1]

        # Для СКНФ ищем строки с результатом 0
        if result == 0:
            term = []
            for j in range(len(vars_list)):
                # 0 -> переменная, 1 -> !переменная
                if row[j] == 0:
                    term.append(vars_list[j])
                else:
                    term.append(f"!{vars_list[j]}")
            # Собираем терм через ИЛИ
            maxterms.append("(" + " | ".join(term) + ")")

    # Соединяем термы через И
    return " & ".join(maxterms)


def get_numeric_sdnf(table: list[list[int]]) -> str:
    """Возвращает числовую форму СДНФ (символ Σ и индексы единиц)."""
    indices = [str(i) for i, row in enumerate(table) if row[-1] == 1]
    return f"Σ({', '.join(indices)})" if indices else "Σ()"


def get_numeric_sknf(table: list[list[int]]) -> str:
    """Возвращает числовую форму СКНФ (символ Π и индексы нулей)."""
    indices = [str(i) for i, row in enumerate(table) if row[-1] == 0]
    return f"Π({', '.join(indices)})" if indices else "Π()"


def get_index_form(table: list[list[int]]) -> int:
    """Возвращает индексную форму функции (десятичный эквивалент вектора)."""
    binary_str = "".join(str(row[-1]) for row in table)
    return int(binary_str, 2)


# === Блок для тестирования ===
if __name__ == '__main__':
    # Нам понадобится импорт из предыдущего файла для тестов
    from truth_table import generate_truth_table

    # Возьмем простую функцию: импликация a -> b
    expr = "a > b"
    print(f"Функция: {expr}\n")

    # Генерируем данные
    vars_list, table = generate_truth_table(expr)

    print(f"Вектор значений: {[row[-1] for row in table]}")
    print("-" * 40)

    print(f"СДНФ: {get_sdnf(vars_list, table)}")
    print(f"СКНФ: {get_sknf(vars_list, table)}")
    print("-" * 40)

    print(f"Числовая СДНФ: {get_numeric_sdnf(table)}")
    print(f"Числовая СКНФ: {get_numeric_sknf(table)}")
    print(f"Индекс функции: {get_index_form(table)}")