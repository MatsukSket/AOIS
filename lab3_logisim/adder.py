from minimizer import minimize_function

def run_adder():
    print('\n=== Adder ===')
    vars = ['a', 'b', 'p_in']

    inputs = [[int(bit) for bit in format(i, "03b")] for i in range(8)]
    table_s = [row + [sum(row) % 2] for row in inputs]
    table_p_out = [row + [1 if sum(row) > 1 else 0] for row in inputs]

    s_mknf = minimize_function(table_s, vars, is_dnf=False)
    p_out_mknf = minimize_function(table_p_out, vars, is_dnf=False)

    print(f"Сумма в МКНФ:    {s_mknf}")
    print(f"Перенос в МКНФ: {p_out_mknf}\n")

if __name__ == '__main__':
    run_adder()