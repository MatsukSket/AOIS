import sys
from hash_table import HashTable


class Menu:
    def __init__(self):
        self.hash_table = HashTable(size=20)
        self.preload_data()

    def preload_data(self):
        data = [
            ("Абаев", "Сергей"),  # ID1, V=1, h=1
            ("Бобков", "Тимур"),  # ID2, V=48, h=18 (h=18)
            ("Видерт", "Евгений"),  # ID3, V=75, h=15
            ("Гракова", "Иван"),  # ID4, V=116, h=16
            ("Кожевников", "Максим"),  # ID5, V=388, h=18 (Коллизия с Бобковым)
            ("Азимов", "Александр")  # ID13, V=8, h=8
        ]
        print("Загрузка данных...")
        for key, value in data:
            try:
                self.hash_table.insert(key, value)
            except Exception as e:
                print(f"[!] Ошибка при добавлении {key}: {e}")
        print("Загрузка завершена.\n")

    def run(self):
        while True:
            self.print_menu()
            choice = input("\nВыберите действие: ").strip()

            match choice:
                case "1":
                    self.insert()
                case "2":
                    self.search()
                case "3":
                    self.update()
                case "4":
                    self.delete()
                case "5":
                    self.display()
                case "6":
                    self.clear_table()
                case "7":
                    self.load_factor()
                case "0":
                    print("Выход из программы...")
                    sys.exit(0)
                case _:
                    print("[!] Неверный ввод!")

    def print_menu(self):
        print("\n" + "=" * 45)
        print(" МЕНЮ: ХЕШ-ТАБЛИЦА (ВНУТРЕННЯЯ АДРЕСАЦИЯ)")
        print("=" * 45)
        print("1. Добавить запись")
        print("2. Найти запись")
        print("3. Обновить запись")
        print("4. Удалить запись")
        print("5. Показать таблицу")
        print("6. Очистить таблицу")
        print("7. Коэффициент заполнения")
        print("0. Выход")
        print("=" * 45)

    def insert(self):
        key = input("Введите ключ (Фамилия): ").strip()
        value = input("Введите значение (Имя/Данные): ").strip()
        try:
            self.hash_table.insert(key, value)
            print("[+] Запись успешно добавлена.")
        except Exception as e:
            print(f"[-] Ошибка при добавлении записи: {e}")

    def search(self):
        key = input("Введите ключ для поиска: ").strip()
        try:
            value = self.hash_table.search(key)
            v_val = self.hash_table.get_v_value(key)
            h_val = self.hash_table.get_hash(key)
            print(f"[+] Значение для '{key}': {value}")
            print(f"    (Информация: V = {v_val}, h(V) = {h_val})")
        except Exception as e:
            print(f"[-] Ошибка: {e}")

    def update(self):
        key = input("Введите ключ для обновления: ").strip()
        new_value = input("Введите новое значение: ").strip()
        try:
            self.hash_table.update(key, new_value)
            print("[+] Запись успешно обновлена.")
        except Exception as e:
            print(f"[-] Ошибка при обновлении: {e}")

    def delete(self):
        key = input("Введите ключ для удаления: ").strip()
        try:
            self.hash_table.delete(key)
            print("[+] Запись удалена (Установлен флаг D=1, U=0).")
        except Exception as e:
            print(f"[-] Ошибка: {e}")

    def display(self):
        print("\nСтруктура хеш-таблицы (согласно Рисунку 1 ЛР №6):")
        headers = ["Idx", "ID", "V", "h", "C", "U", "T", "L", "D", "P0", "Pi (Данные)"]

        # Форматирование шапки
        header_str = " | ".join(
            f"{h:<5}" if h in ("V", "h") else f"{h:<3}" if len(h) <= 2 else f"{h:<12}" for h in headers)
        print("-" * len(header_str))
        print(header_str)
        print("-" * len(header_str))

        for i in range(self.hash_table.size):
            entry = self.hash_table.table[i]

            # Если ячейка пустая (никогда не использовалась)
            if entry.u == 0 and entry.d == 0 and not entry.id:
                print(f"{i:<3} | {'-':<12} | {'-':<5} | {'-':<5} | 0   | 0   | 0   | 0   | 0   | {'-':<3} | Пусто")
            else:
                # Вычисляем V и h только для непустых ключей
                v_val = str(self.hash_table.get_v_value(entry.id)) if entry.id else "-"
                h_val = str(self.hash_table.get_hash(entry.id)) if entry.id else "-"
                p0_str = str(entry.p0) if entry.p0 is not None else "-"

                # Добавляем пометку, если запись удалена
                pi_display = entry.pi if entry.u == 1 else f"({entry.pi})"

                print(
                    f"{i:<3} | "
                    f"{entry.id:<12} | "
                    f"{v_val:<5} | "
                    f"{h_val:<5} | "
                    f"{entry.c:<3} | "
                    f"{entry.u:<3} | "
                    f"{entry.t:<3} | "
                    f"{entry.l:<3} | "
                    f"{entry.d:<3} | "
                    f"{p0_str:<3} | "
                    f"{pi_display}"
                )
        print("-" * len(header_str))

    def clear_table(self):
        confirm = input("Вы уверены, что хотите очистить таблицу? (y/n): ").strip().lower()
        if confirm == 'y':
            self.hash_table.clear()
            print("[+] Таблица очищена.")
        else:
            print("[-] Отмена.")

    def load_factor(self):
        factor = self.hash_table.get_load_factor()
        print(f"[i] Коэффициент заполнения: {factor:.2f}")


if __name__ == "__main__":
    menu = Menu()
    menu.run()