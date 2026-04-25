def get_bin_implicants(truth_table, dnf_mode: bool = True, include_dc: bool = False) -> list:
    """
    Выбирает из таблицы наборы для минимизации.
    Для ДНФ строки 1, для КНФ 0.
    Если include_dc=True, также захватывает строки с неопределенным выходом '-'.
    """
    target = 1 if dnf_mode else 0
    res = []
    for row in truth_table:
        if row[-1] == target or (include_dc and row[-1] == '-'):
            res.append("".join(map(str, row[:-1])))
    return res

def get_bit_diff(term1, term2):
    """
        Проверяет, отличаются ли два терма только в одной позиции.
        Возвращает индекс отличия, иначе -1.
    """
    diff_count = 0
    diff_pos = -1
    for i in range(len(term1)):
        if term1[i] != term2[i]:
            diff_count += 1
            diff_pos = i
    return diff_pos if diff_count == 1 else -1

def merge_implicants(implicants: list) -> tuple:
    """Один цикл склеивания всех возможных пар."""
    new_implicants = set()
    used = set()

    n = len(implicants)
    for i in range(n):
        for j in range(i + 1, n):
            diff_idx = get_bit_diff(implicants[i], implicants[j])

            if diff_idx != -1:
                merged = list(implicants[i])
                merged[diff_idx] = "-"
                new_implicants.add("".join(merged))

                used.add(i)
                used.add(j)
    primes = [implicants[k] for k in range(n) if k not in used]
    return list(new_implicants), primes

def covers(implicant, minterm):
    """Проверяет, перекрывает ли импликант конкретный бинарный набор."""
    for i in range(len(implicant)):
        if implicant[i] != "-" and implicant[i] != minterm[i]:
            return False
    return True

def get_min_cover(prime_implicants, target_minterms):
    """Находит минимальный набор импликант, покрывающий все целевые наборы."""
    if not prime_implicants or not target_minterms:
        return []
    uncovered = set(target_minterms)
    final_selection = []

    for m in list(uncovered):
        matches = [p for p in prime_implicants if covers(p, m)]
        if len(matches) == 1:
            prime = matches[0]
            if prime not in final_selection:
                final_selection.append(prime)
                for covered_m in list(uncovered):
                    if covers(prime, covered_m):
                        uncovered.discard(covered_m)

    while uncovered:
        best_p = max(prime_implicants, key=lambda p: len([m for m in uncovered if covers(p, m)]))
        final_selection.append(best_p)
        for covered_m in list(uncovered):
            if covers(best_p, covered_m):
                uncovered.discard(covered_m)

    return final_selection

def format_string_formula(implicants, variables, is_dnf=True):
    """Формирует формулу из списка масок."""
    if not implicants:
        return "0" if is_dnf else "1"

    terms = []
    for mask in implicants:
        parts = []
        for i, char in enumerate(mask):
            if char == "-":
                continue
            var_name = variables[i]
            if is_dnf:
                parts.append(var_name if char == '1' else f"!{var_name}")
            else:
                parts.append(var_name if char == '0' else f"!{var_name}")

        inner_op = " & " if is_dnf else " | "
        terms.append(f"({inner_op.join(parts)})")

    outer_op = " | " if is_dnf else " & "
    return outer_op.join(terms)

def minimize_function(table: list, variables: list, is_dnf: bool = True) -> str:
    """
    Главная функция минимизации.
    table: список списков, где последний элемент — результат (0, 1 или '-').
    """
    # 1. Извлекаем импликанты ДЛЯ СКЛЕЙКИ (включая неиспользуемые состояния '-')
    curr_imps = get_bin_implicants(table, is_dnf, include_dc=True)
    all_primes = []

    # 2. Итеративно склеиваем (Куайн-Маккласки)
    while True:
        next_imps, primes = merge_implicants(curr_imps)
        all_primes.extend(primes)
        if not next_imps:
            all_primes.extend(curr_imps)
            break
        curr_imps = next_imps

    final_primes = list(set(all_primes))

    # 3. Извлекаем импликанты ДЛЯ ПОКРЫТИЯ (строго целевые 0 или 1, БЕЗ '-')
    target_minterms = get_bin_implicants(table, is_dnf, include_dc=False)

    # 4. Находим минимальное покрытие
    min_form = get_min_cover(final_primes, target_minterms)

    # 5. Форматируем результат
    return format_string_formula(min_form, variables, is_dnf)