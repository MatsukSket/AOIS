def get_char_code(char: str) -> int:
    char = char.upper()
    if 'А' <= char <= 'Е':
        return ord(char) - ord('А')
    elif char == 'Ё':
        return 6
    elif 'Ж' <= char <= 'Я':
        return ord(char) - ord('А') + 1
    return 0


class HashEntry:
    def __init__(self):
        self.key = ""
        self.pi = ""
        self.c = 0
        self.u = 0
        self.t = 0
        self.d = 0
        self.next = None

class HashTable:
    def __init__(self, size: int = 20):
        self.size = size
        self.table = [HashEntry() for _ in range(self.size)]
        self.elements_count = 0

    def get_v_value(self, key: str) -> int:
        if not key:
            return 0
        val_1 = get_char_code(key[0]) if len(key) > 0 else 0
        val_2 = get_char_code(key[1]) if len(key) > 1 else 0

        return val_1 * 33 + val_2

    def get_hash(self, key: str) -> int:
        return self.get_v_value(key) % self.size

    def insert(self, key: str, value: str):
        if not key.strip():
            raise ValueError("Ключ не может быть пустым.")
        if self.elements_count >= self.size:
            raise OverflowError("Таблица переполнена! Невозможно добавить элемент.")

        h = self.get_hash(key)

        if self.table[h].u == 0 and self.table[h].d == 0:
            self.table[h].key = key
            self.table[h].pi = value
            self.table[h].u = 1
            self.table[h].t = 1
            self.elements_count += 1
            return

        curr = h
        while True:
            if self.table[curr].u == 1 and self.table[curr].key == key:
                raise ValueError(f"Запись с ключом '{key}' уже существует.")
            if self.table[curr].next is None:
                break
            curr = self.table[curr].next

        free_idx = (h + 1) % self.size
        while (self.table[free_idx].u == 1 or self.table[free_idx].d == 1) and free_idx != h:
            free_idx = (free_idx + 1) % self.size

        if free_idx == h:
            raise OverflowError("Нет свободных ячеек.")

        self.table[free_idx].key = key
        self.table[free_idx].pi = value
        self.table[free_idx].u = 1
        self.table[free_idx].t = 1
        self.table[free_idx].next = None
        self.table[curr].next = free_idx
        self.table[curr].t = 0
        self.table[h].c = 1
        self.elements_count += 1

    def search(self, key: str) -> str:
        curr = self.get_hash(key)

        while curr is not None:
            entry = self.table[curr]
            if entry.u == 1 and entry.key == key:
                return entry.pi
            curr = entry.next

        raise KeyError(f"Элемент с ключом '{key}' не найден.")

    def update(self, key: str, new_value: str):
        curr = self.get_hash(key)

        while curr is not None:
            entry = self.table[curr]
            if entry.u == 1 and entry.key == key:
                entry.pi = new_value
                return
            curr = entry.next

        raise KeyError(f"Элемент с ключом '{key}' не найден для обновления.")

    def delete(self, key: str):
        curr = self.get_hash(key)

        while curr is not None:
            entry = self.table[curr]
            if entry.u == 1 and entry.key == key:
                entry.d = 1
                entry.u = 0
                self.elements_count -= 1
                return
            curr = entry.next

        raise KeyError(f"Элемент с ключом '{key}' не найден для удаления.")

    def clear(self):
        self.table = [HashEntry() for _ in range(self.size)]
        self.elements_count = 0

    def get_load_factor(self) -> float:
        return self.elements_count / self.size