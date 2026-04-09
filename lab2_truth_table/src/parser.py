from logic_operations import *
from config import *


def standardize_expr(expr: str) -> str:
    """Удаляет в строке пробелы и заменяет '->' на '>'."""
    return expr.replace(' ', '').replace(OP_IMP1, OP_IMP)


def is_var(c: str) -> bool:
    """Является ли символ переменной."""
    return c in VARS


def is_valid_expression(expr: str) -> None:
    """Проверяет валидность стандартизированного выражения."""
    prev_is_var = False

    valid_c = VARS.union({OP_AND, OP_OR, OP_IMP, OP_EQ, OP_NOT, '(', ')'})

    for c in expr:
        if c not in valid_c:
            raise ValueError(f"Ошибка ввода. Недопустимый символ '{c}'.")

        if is_var(c):
            if prev_is_var:
                raise ValueError(f"Синтаксическая ошибка. Подряд идущие переменные без оператора.")
            prev_is_var = True
        elif c not in ('(', OP_NOT):
            prev_is_var = False


def get_rpn(expr: str) -> list[str]:
    """Переводит выражение в опз."""
    clean_expr = standardize_expr(expr)
    is_valid_expression(clean_expr)

    output = []
    stack = []

    for char in clean_expr:
        if is_var(char):
            output.append(char)

        elif char == '(':
            stack.append(char)

        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
            else:
                raise ValueError("Синтаксическая ошибка. Пропущена открывающая скобка")

        elif char in PRIORITY:
            while stack and stack[-1] != '(':
                top_prio = PRIORITY[stack[-1]]
                char_prio = PRIORITY[char]

                if (char != OP_NOT and top_prio >= char_prio) or \
                        (char == OP_NOT and top_prio > char_prio):
                    output.append(stack.pop())
                else:
                    break
            stack.append(char)

    while stack:
        if stack[-1] == '(':
            raise ValueError("Синтаксическая ошибка: пропущена закрывающая скобка")
        output.append(stack.pop())

    return output


def evaluate_rpn(rpn: list[str], var_values: dict[str, int]) -> int:
    """Вычисляет значение по опз."""
    stack = []

    for token in rpn:
        if is_var(token):
            stack.append(var_values[token])
        elif token in ('0', '1'):
            stack.append(int(token))
        elif token == OP_NOT:
            val = stack.pop()
            stack.append(l_not(val))
        else:
            right = stack.pop()
            left = stack.pop()

            if token == OP_AND:
                stack.append(l_and(left, right))
            elif token == OP_OR:
                stack.append(l_or(left, right))
            elif token == OP_IMP:
                stack.append(l_imp(left, right))
            elif token == OP_EQ:
                stack.append(l_eq(left, right))

    return stack[0]


# === Блок для тестирования ===
if __name__ == '__main__':
    expr = "a&b&!c|c"
    print(f"выражение: {expr}")

    rpn = get_rpn(expr)
    print(f"опз: {rpn}")

    # Тестовый набор: a=1, b=0, c=1, d=0, e=0
    test_vars = {'a': 1, 'b': 0, 'c': 1, 'd': 0, 'e': 0}
    result = evaluate_rpn(rpn, test_vars)
    print(f"значение {test_vars}: {result}")