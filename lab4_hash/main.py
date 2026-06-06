import sys
from hash_table import HashTable


class Menu:
    def __init__(self):
        self.hash_table = HashTable(size=20)
        self.preload_data()

    def preload_data(self):
        data = [
            ("Абаев", "Сергей"),        # V=1, h=1
            ("Бобков", "Тимур"),        # V=48, h=18
            ("Витко", "Евгений"),       # V=75, h=15
            ("Гракова", "Иван"),        # V=116, h=16
            ("Кожевников", "Максим"),   # V=378, h=18 (Коллизия с Бобковым)
            ("Азимов", "Александр")     # V=8, h=8
        ]
        print("Загрузка данных...")
        for key, value in data:
            try:
                self.hash_table.insert(key, value)
            except Exception as e:
                print(f"Ошибка при добавлении {key}: {e}")
        print("Загрузка завершена.\n")

    def run(self):
        while True:
            self.print_menu()
            choice = input("\nВыберите действие: ").strip()

            match choice:
                case "1": self.insert()
                case "2": self.search()
                case "3": self.update()
                case "4": self.delete()
                case "5": self.display()
                case "6": self.clear_table()
                case "7": self.load_factor()
                case "0":
                    print("Выход из программы...")
                    sys.exit(0)
                case _: print("Неверный ввод!")

    def print_menu(self):
        print("\n" + "=" * 45)
        print(" МЕНЮ: ХЕШ-ТАБЛИЦА")
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
        key = input("Введите ключ: ").strip()
        value = input("Введите значение: ").strip()
        try:
            self.hash_table.insert(key, value)
            print("Запись добавлена.")
        except Exception as e:
            print(f"Ошибка при добавлении записи: {e}")

    def search(self):
        key = input("Введите ключ для поиска: ").strip()
        try:
            value = self.hash_table.search(key)
            v_val = self.hash_table.get_v_value(key)
            h_val = self.hash_table.get_hash(key)
            print(f"Значение для '{key}': {value}")
            print(f"    (Информация: v = {v_val}, h(v) = {h_val})")
        except Exception as e:
            print(f"Ошибка: {e}")

    def update(self):
        key = input("Введите ключ для обновления: ").strip()
        new_value = input("Введите новое значение: ").strip()
        try:
            self.hash_table.update(key, new_value)
            print("Запись обновлена.")
        except Exception as e:
            print(f"Ошибка при обновлении: {e}")

    def delete(self):
        key = input("Введите ключ для удаления: ").strip()
        try:
            self.hash_table.delete(key)
            print("Запись удалена (Установлен флаг D=1, U=0). Указатель сохранен.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def display(self):
        print("\nСтруктура хеш-таблицы (Метод внутренних цепочек):")

        row_format = "{:<3} | {:<14} | {:<4} | {:<4} | {:<3} | {:<3} | {:<3} | {:<3} | {:<5} | {}"

        header_str = row_format.format("Idx", "key", "v", "h", "c", "u", "t", "d", "next", "Data")
        separator = "-" * len(header_str)

        print(separator)
        print(header_str)
        print(separator)

        for i in range(self.hash_table.size):
            entry = self.hash_table.table[i]

            # Если ячейка полностью пустая
            if entry.u == 0 and entry.d == 0 and not entry.key:
                print(row_format.format(i, "-", "-", "-", 0, 0, 0, 0, "-", "Пусто"))
            else:
                v_val = str(self.hash_table.get_v_value(entry.key)) if entry.key else "-"
                h_val = str(self.hash_table.get_hash(entry.key)) if entry.key else "-"
                next_str = str(entry.next) if entry.next is not None else "-"

                data_display = entry.pi if entry.u == 1 else f"(Удалено: {entry.pi})"

                print(row_format.format(
                    i,
                    entry.key,
                    v_val,
                    h_val,
                    entry.c,
                    entry.u,
                    entry.t,
                    entry.d,
                    next_str,
                    data_display
                ))

        print(separator)

    def clear_table(self):
        self.hash_table.clear()
        print("Таблица очищена.")

    def load_factor(self):
        factor = self.hash_table.get_load_factor()
        print(f"Коэффициент заполнения: {factor:.2f}")


if __name__ == "__main__":
    menu = Menu()
    menu.run()