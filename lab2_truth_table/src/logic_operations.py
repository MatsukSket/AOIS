def l_and(a: int, b: int) -> int:
    return a * b

def l_or(a: int, b: int) -> int:
    return 1 if (a + b) > 0 else 0

def l_imp(a: int, b: int) -> int:
    return 0 if (a > b) else 1

def l_eq(a: int, b: int) -> int:
    return 1 if (a == b) else 0

def l_not(a: int) -> int:
    return 0 if (a == 1) else 1
