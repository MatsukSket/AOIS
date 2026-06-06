import pytest
from hash_table import HashTable, HashEntry  # Убедись, что импорт соответствует твоей структуре


@pytest.fixture
def ht():
    """Фикстура для создания чистой хеш-таблицы перед каждым тестом."""
    return HashTable(size=5)


class TestHashTable:

    def test_initialization(self, ht):
        """Проверка корректной инициализации таблицы."""
        assert ht.size == 5
        assert ht.elements_count == 0
        assert len(ht.table) == 5
        assert isinstance(ht.table[0], HashEntry)

    def test_get_v_value(self, ht):
        """Проверка вычисления числового значения V(K)."""
        # Пустой ключ
        assert ht.get_v_value("") == 0
        assert ht.get_v_value("А") == 0
        assert ht.get_v_value("Б") == 33
        assert ht.get_v_value("Я") == 32 * 33 + 0
        assert ht.get_v_value("АБ") == 1
        assert ht.get_v_value("БА") == 33
        assert ht.get_v_value("аб") == 1
        assert ht.get_v_value("ЁЖ") == 205
        assert ht.get_v_value("eng") == 0

    def test_insert_and_search_basic(self, ht):
        """Проверка базовой вставки и поиска."""
        ht.insert("Иванов", "Студент")
        assert ht.elements_count == 1
        assert ht.search("Иванов") == "Студент"

        idx = ht.get_hash("Иванов")
        assert ht.table[idx].u == 1
        assert ht.table[idx].t == 1
        assert ht.table[idx].c == 0

    def test_insert_empty_key(self, ht):
        """Проверка валидации пустого ключа."""
        with pytest.raises(ValueError, match="Ключ не может быть пустым"):
            ht.insert("   ", "Data")

    def test_insert_duplicate_key(self, ht):
        """Проверка защиты от дубликатов."""
        ht.insert("АБ", "Data 1")
        with pytest.raises(ValueError, match="уже существует"):
            ht.insert("АБ", "Data 2")

    def test_insert_collision(self, ht):
        """Проверка обработки коллизий (внутренние цепочки)."""
        ht.insert("АА", "Data 0")
        ht.insert("АА1", "Data 1")

        assert ht.elements_count == 2
        assert ht.search("АА") == "Data 0"
        assert ht.search("АА1") == "Data 1"

        base_idx = ht.get_hash("АА")
        assert ht.table[base_idx].c == 1
        assert ht.table[base_idx].t == 0

        next_idx = ht.table[base_idx].next
        assert next_idx is not None
        assert ht.table[next_idx].key == "АА1"
        assert ht.table[next_idx].t == 1

    def test_table_overflow(self):
        """Проверка исключения при переполнении таблицы."""
        small_ht = HashTable(size=2)
        small_ht.insert("А", "1")
        small_ht.insert("Б", "2")

        with pytest.raises(OverflowError, match="Таблица переполнена"):
            small_ht.insert("В", "3")

    def test_search_missing_key(self, ht):
        """Проверка поиска несуществующего ключа."""
        with pytest.raises(KeyError, match="не найден"):
            ht.search("Петров")

    def test_update(self, ht):
        """Проверка обновления данных."""
        ht.insert("АБ", "Old Value")
        ht.update("АБ", "New Value")
        assert ht.search("АБ") == "New Value"

        with pytest.raises(KeyError, match="не найден для обновления"):
            ht.update("ВГ", "Fail")

    def test_delete(self, ht):
        """Проверка удаления элемента (установка флагов вычеркивания)."""
        ht.insert("АБ", "Data")
        ht.delete("АБ")

        assert ht.elements_count == 0
        idx = ht.get_hash("АБ")
        assert ht.table[idx].u == 0
        assert ht.table[idx].d == 1

        with pytest.raises(KeyError, match="не найден"):
            ht.search("АБ")

        with pytest.raises(KeyError, match="не найден для удаления"):
            ht.delete("ВГ")

    def test_delete_within_collision_chain(self, ht):
        """Проверка удаления элемента, который находится в начале цепочки коллизий."""
        ht.insert("АА", "Root")
        ht.insert("АА1", "Child")

        ht.delete("АА")

        assert ht.search("АА1") == "Child"

    def test_clear(self, ht):
        """Проверка очистки таблицы."""
        ht.insert("АА", "Data")
        ht.clear()

        assert ht.elements_count == 0
        assert ht.table[0].key == ""
        assert ht.table[0].u == 0

    def test_get_load_factor(self, ht):
        """Проверка расчета коэффициента заполнения."""
        assert ht.get_load_factor() == 0.0
        ht.insert("АА", "Data")
        assert ht.get_load_factor() == 0.2
        ht.insert("ББ", "Data")
        assert ht.get_load_factor() == 0.4