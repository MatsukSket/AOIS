def get_bin_implicants(truth_table, dnf_mode: bool=True) -> list:
    """
    Выбирает из таблицы наборы для минимизации.
    Для ДНФ строки 1, для КНФ 0.
    """
    target = 1 if dnf_mode else 0
    return ["".join(map(str, row[:-1])) for row in truth_table if row[-1] == target]


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


def calculate_method(table: list, variables: list, is_dnf: bool=True) -> list:
    """Расчетный метод. Выводит этапы склеивания и итоговую функцию."""
    name = "МДНФ" if is_dnf else "МКНФ"
    curr_imps = get_bin_implicants(table, is_dnf)
    all_primes = []

    while True:
        print(f"Текущие импликанты {name}: {curr_imps}")
        next_imps, primes = merge_implicants(curr_imps)
        all_primes.extend(primes)
        if not next_imps:
            all_primes.extend(curr_imps)
            break
        curr_imps = next_imps

    final_primes = list(set(all_primes))
    print(f"Импликанты до чистки: {final_primes}")

    min_form = get_min_cover(final_primes, get_bin_implicants(table, is_dnf))
    print(f"Результат: {format_string_formula(min_form, variables, is_dnf)}")
    return final_primes


def covers(implicant, minterm):
    """Проверяет, перекрывает ли импликант (с '-') конкретный бинарный набор."""
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
        return "1" if not is_dnf else "0"

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


def tabular_calc_method(table: list, prime_impls: list, variables: list, is_dnf: bool = True) -> None:
    """Расчетно-табличный метод."""
    target_bin = get_bin_implicants(table, is_dnf)
    if not target_bin:
        print("Функция константа, минимизация не требуется.")
        return

    print(f"=== {'ДНФ' if is_dnf else 'КНФ'} ===")

    col_width = len(target_bin[0])
    sep = " | "

    header = f"{'Импликанта':<12} | " + sep.join(target_bin)
    print(header)

    for prime in prime_impls:
        marks = []
        for term in target_bin:
            symbol = "X" if covers(prime, term) else "."
            marks.append(symbol.center(col_width))

        print(f"{prime:<12} | " + sep.join(marks))

    final_cover = get_min_cover(prime_impls, target_bin)
    print(f"Минимальное покрытие: {final_cover}")
    print(f"Итоговая формула: {format_string_formula(final_cover, variables, is_dnf)}")


def generate_gray_code(bits):
    """Рекурсивная генерация кода Грея для любого количества бит."""
    if bits == 0:
        return [""]
    if bits == 1:
        return ["0", "1"]
    previous = generate_gray_code(bits - 1)
    # Зеркальное отражение: добавляем 0 к прямой последовательности и 1 к обратной
    return ["0" + code for code in previous] + ["1" + code for code in reversed(previous)]


def print_karnaugh_map(table: list, variables: list) -> None:
    """
    Отрисовывает карту Карно для 1-5 переменных.
    Использует код Грея для обеспечения соседства клеток по одному биту.
    """
    num_vars = len(variables)
    if num_vars < 1 or num_vars > 5:
        print(f"Карта Карно для {num_vars} переменных не поддерживается (доступно 1-5).")
        return

    row_vars_count = num_vars // 2
    col_vars_count = num_vars - row_vars_count

    row_names = variables[:row_vars_count]
    col_names = variables[row_vars_count:]

    row_codes = generate_gray_code(row_vars_count)
    col_codes = generate_gray_code(col_vars_count)

    val_map = {"".join(map(str, row[:-1])): row[-1] for row in table}

    print(f"--- Карта Карно для ({''.join(row_names)} \\ {''.join(col_names)}) ---")

    col_width = max(len(col_codes[0]), 3)
    margin = " " * (max(len(row_names), 2) + 2)

    header = margin + "| " + " | ".join(code.center(col_width) for code in col_codes) + " |"
    print(header)

    for r_code in row_codes:
        row_label = r_code if r_code else "f"
        line = f" {row_label.center(len(margin) - 2)} | "

        for c_code in col_codes:
            full_key = r_code + c_code
            val = val_map.get(full_key, "?")
            line += str(val).center(col_width) + " | "

        print(line)

    primes_dnf = get_prime_implicants_karnaugh_map(table, True)
    min_cover_dnf = get_min_cover(primes_dnf, get_bin_implicants(table, True))
    print(f"\nРезультат по Карте Карно (МДНФ): {format_string_formula(min_cover_dnf, variables, True)}")

    primes_knf = get_prime_implicants_karnaugh_map(table, False)
    min_cover_knf = get_min_cover(primes_knf, get_bin_implicants(table, False))
    print(f"Результат по Карте Карно (МКНФ): {format_string_formula(min_cover_knf, variables, False)}")


def get_grid_cells(row_codes: list, col_codes: list, r_start: int, c_start: int, h: int, w: int) -> list:
    """Собирает ячейки прямоугольника размером h на w."""
    R = len(row_codes)
    C = len(col_codes)
    cells = []

    for i in range(h):
        for j in range(w):
            r = (r_start + i) % R
            c = (c_start + j) % C
            cells.append(row_codes[r] + col_codes[c])

    return cells


def get_karnaugh_map_rectangles(table: list, is_dnf: bool = True) -> list:
    """Поиск прямоугольных областей (импликант) на карте Карно."""
    target = 1 if is_dnf else 0
    val_map = {"".join(map(str, row[:-1])): row[-1] for row in table}

    if not table:
        return []

    num_vars = len(table[0]) - 1
    row_vars_count = num_vars // 2
    col_vars_count = num_vars - row_vars_count

    row_codes = generate_gray_code(row_vars_count)
    col_codes = generate_gray_code(col_vars_count)

    R = len(row_codes)
    C = len(col_codes)

    valid_rects = []
    sizes = [1, 2, 4, 8]

    for h in sizes:
        if h > R: continue
        for w in sizes:
            if w > C: continue

            for r in range(R):
                for c in range(C):
                    cells = get_grid_cells(row_codes, col_codes, r, c, h, w)
                    if all(val_map.get(cell, -1) == target for cell in cells):
                        valid_rects.append(set(cells))

    prime_rects = []
    for rect in valid_rects:
        is_prime = True
        for other_rect in valid_rects:
            if rect != other_rect and rect.issubset(other_rect):
                is_prime = False
                break

        if is_prime and rect not in prime_rects:
            prime_rects.append(rect)

    return prime_rects


def rect_to_mask(rect_cells: set, num_vars: int) -> str:
    """Формиует бинарную маску для прямоугольника."""
    cells_list = list(rect_cells)
    mask = ""

    for i in range(num_vars):
        bits_at_i = set(cell[i] for cell in cells_list)

        if len(bits_at_i) == 1:
            mask += bits_at_i.pop()
        else:
            mask += "-"

    return mask


def get_prime_implicants_karnaugh_map(table: list, is_dnf: bool = True) -> list:
    """Возвращает список импликант, масок."""
    if not table:
        return []

    num_vars = len(table[0]) - 1
    prime_rects = get_karnaugh_map_rectangles(table, is_dnf)

    implicants = []
    for rect in prime_rects:
        implicants.append(rect_to_mask(rect, num_vars))

    return list(set(implicants))