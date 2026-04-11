import itertools

from src.parser import get_rpn
from src.truth_table import extract_variables, generate_truth_table, print_truth_table
from src.normal_forms import get_sdnf, get_sknf, get_numeric_sdnf, get_numeric_sknf, get_index_form
from src.analisis import get_zhegalkin, get_post_classes
from src.calculus import get_fictive_variables, get_mixed_derivative
from src.minimization import calculate_method, tabular_calc_method, print_karnaugh_map

# ((a&b)|(!a&c)|(b&c))&(d|!d)
def run_analysis():
    user_input = input("Укажите логическое выражение: ")

    if len(user_input.strip()) == 0:
        print("Ввод пуст, работа завершена.")
        return

    print(f"\nАнализируемая функция: {user_input}")

    # 1 Получаем ОПЗ и список уникальных переменных
    postfix_notation = get_rpn(user_input)
    logic_vars = extract_variables(postfix_notation)

    if len(logic_vars) == 0:
        print("Переменные отсутствуют, функция является константой.")

    print(f"Найденные переменные: {logic_vars}\n")

    # 2 Генерация и вывод матрицы истинности
    matrix = generate_truth_table(postfix_notation, logic_vars)
    print("Сгенерированная таблица истинности:")
    print_truth_table(matrix, logic_vars)

    # 3 Формирование нормальных форм
    print(f"\nСДНФ: {get_sdnf(logic_vars, matrix)}")
    print(f"СКНФ: {get_sknf(logic_vars, matrix)}")

    # 4 Вывод числовых форм
    print(f"СДНФ (числовая): {get_numeric_sdnf(matrix)}")
    print(f"СКНФ (числовая): {get_numeric_sknf(matrix)}")

    # 5 Вывод индекса
    print(f"Индекс функции: {get_index_form(matrix)}")

    # 6 Вычисление полинома Жегалкина
    zheg_poly, coefficients = get_zhegalkin(logic_vars, matrix)
    print(f"\nПолином Жегалкина: {zheg_poly}")

    # 7 Проверка принадлежности классам Поста
    classes_dict = get_post_classes(matrix, coefficients)
    post_strings = []
    for key, val in classes_dict.items():
        sign = "+" if val else "-"
        post_strings.append(f"{key}: {sign}")
    print(f"Принадлежность классам Поста:\n{'\n'.join(post_strings)}")

    # 8 Проверка на наличие фиктивных переменных
    dummy_vars = get_fictive_variables(logic_vars, matrix)
    if dummy_vars:
        print(f"\nФиктивные переменные: {', '.join(dummy_vars)}")
    else:
        print("\nФиктивных переменных нет.")

    # 9 Расчет производных
    print("\nРезультаты булевой дифференциации:")
    if len(logic_vars) == 0:
        print("Для константы производная равна нулю.")
    else:
        limit_order = min(len(logic_vars) + 1, 5)
        for current_order in range(1, limit_order):
            for combination in itertools.combinations(logic_vars, current_order):
                diff_result = get_mixed_derivative(logic_vars, matrix, list(combination))
                vars_str = "".join(combination)
                print(f"d({vars_str}): {diff_result}")

    # 10. Расчетный метод
    print("\nРасчетный метод.")

    print("=== ДНФ ===")
    primes_dnf = calculate_method(matrix, logic_vars, is_dnf=True)

    print("=== КНФ ===")
    primes_knf = calculate_method(matrix, logic_vars, is_dnf=False)

    # 11. Расчетно-табличный метод
    print("\nРасчетно-табличный метод.")
    tabular_calc_method(matrix, primes_dnf, logic_vars, is_dnf=True)
    print('')
    tabular_calc_method(matrix, primes_knf, logic_vars, is_dnf=False)

    # 12. Карта Карно
    print("\nКарта Карно.")
    print_karnaugh_map(matrix, logic_vars)


if __name__ == "__main__":
    run_analysis()