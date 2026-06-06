from minimizer import minimize_function


def build_final_block():
    variables = ['S4', 'S3', 'S2', 'S1', 'S0']

    gray_map = {
        0: [0, 0, 0, 0],
        1: [0, 0, 0, 1],
        2: [0, 0, 1, 1],
        3: [0, 0, 1, 0],
        4: [0, 1, 1, 0],
        5: [0, 1, 1, 1],
        6: [0, 1, 0, 1],
        7: [0, 1, 0, 0],
        8: [1, 1, 0, 0],
        9: [1, 1, 0, 1]
    }

    outputs = {f"T{i}": [] for i in range(4)}
    outputs.update({f"U{i}": [] for i in range(4)})

    for i in range(32):
        bin_in = [int(x) for x in format(i, '05b')]

        if i <= 18:
            res = i + 9
            tens = res // 10
            units = res % 10

            t_gray = gray_map[tens]
            u_gray = gray_map[units]

            for j in range(4):
                outputs[f"T{3 - j}"].append(bin_in + [t_gray[j]])
                outputs[f"U{3 - j}"].append(bin_in + [u_gray[j]])
        else:
            for key in outputs:
                outputs[key].append(bin_in + ['-'])

    for name, table in outputs.items():
        formula = minimize_function(table, variables, is_dnf=True)
        print(f"{name} = {formula}")


build_final_block()