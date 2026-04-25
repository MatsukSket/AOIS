# Импортируем нашу функцию минимизации (убедись, что файл minimizer.py лежит рядом)
from minimizer import minimize_function


def run_gray_bcd():
    print("=== Gray BCD +9 ===")

    variables = ['x3', 'x2', 'x1', 'x0']

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

    tables = {
        "Переполнение": [],
        "y3": [],
        "y2": [],
        "y1": [],
        "y0": []
    }

    for i in range(16):
        bin_in = [int(x) for x in format(i, '04b')]

        dec_val = next((k for k, v in gray_map.items() if v == bin_in), None)

        if dec_val is not None:
            res = dec_val + 9

            tens = res // 10
            units = res % 10
            out_gray = gray_map[units]

            tables["Переполнение"].append(bin_in + [tens])
            tables["y3"].append(bin_in + [out_gray[0]])
            tables["y2"].append(bin_in + [out_gray[1]])
            tables["y1"].append(bin_in + [out_gray[2]])
            tables["y0"].append(bin_in + [out_gray[3]])
        else:
            for key in tables:
                tables[key].append(bin_in + ['-'])

    for name, table in tables.items():
        min_form = minimize_function(table, variables, is_dnf=True)
        print(f"{name} = {min_form}")


if __name__ == "__main__":
    run_gray_bcd()