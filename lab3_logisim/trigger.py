from minimizer import minimize_function


def run_trigger():
    print("\n=== T-Trigger ===")

    variables = ['Q2', 'Q1', 'Q0']

    tables = {
        "T2": [],
        "T1": [],
        "T0": []
    }

    for state in range(8):
        q_curr = [int(x) for x in format(state, '03b')]

        next_state = (state + 1) % 8
        q_next = [int(x) for x in format(next_state, '03b')]

        t_vals = [q_curr[i] ^ q_next[i] for i in range(3)]

        tables["T2"].append(q_curr + [t_vals[0]])
        tables["T1"].append(q_curr + [t_vals[1]])
        tables["T0"].append(q_curr + [t_vals[2]])

    for name, table in tables.items():
        min_form = minimize_function(table, variables, is_dnf=True)
        print(f"{name} = {min_form}")


if __name__ == "__main__":
    run_trigger()