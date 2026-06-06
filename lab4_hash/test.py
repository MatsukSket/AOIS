import pytest
from hash_table import HashTable, HashEntry, get_char_code

@pytest.fixture
def ht():
    return HashTable(size=5)

def test_get_char_code():
    assert get_char_code('А') == 0
    assert get_char_code('Б') == 1
    assert get_char_code('Ё') == 6
    assert get_char_code('Ж') == 7
    assert get_char_code('Я') == 32
    assert get_char_code('Z') == 0
    assert get_char_code('а') == 0

def test_get_v_value(ht):
    assert ht.get_v_value("") == 0
    assert ht.get_v_value("А") == 0
    assert ht.get_v_value("Б") == 33
    assert ht.get_v_value("Я") == 32 * 33
    assert ht.get_v_value("АБ") == 1
    assert ht.get_v_value("ЁЖ") == 6 * 33 + 7

def test_init(ht):
    assert ht.size == 5
    assert ht.elements_count == 0
    assert len(ht.table) == 5
    assert isinstance(ht.table[0], HashEntry)
    assert ht.table[0].u == 0
    assert ht.table[0].d == 0

def test_insert_basic(ht):
    ht.insert("АБ", "val1")
    assert ht.elements_count == 1
    idx = ht.get_hash("АБ")
    assert ht.table[idx].key == "АБ"
    assert ht.table[idx].pi == "val1"
    assert ht.table[idx].u == 1
    assert ht.table[idx].t == 1

def test_insert_empty_key(ht):
    with pytest.raises(ValueError):
        ht.insert("", "val")
    with pytest.raises(ValueError):
        ht.insert("   ", "val")

def test_insert_duplicate(ht):
    ht.insert("АБ", "val1")
    with pytest.raises(ValueError):
        ht.insert("АБ", "val2")

def test_insert_collision(ht):
    ht.insert("АА", "val1")
    ht.insert("АА1", "val2")
    assert ht.elements_count == 2
    idx1 = ht.get_hash("АА")
    assert ht.table[idx1].c == 1
    assert ht.table[idx1].t == 0
    idx2 = ht.table[idx1].next
    assert idx2 is not None
    assert ht.table[idx2].key == "АА1"
    assert ht.table[idx2].t == 1
    assert ht.table[idx2].next is None

def test_insert_overflow():
    h = HashTable(size=2)
    h.insert("А", "1")
    h.insert("Б", "2")
    with pytest.raises(OverflowError):
        h.insert("В", "3")

def test_insert_no_free_cells(ht):
    ht.elements_count = 0
    for i in range(5):
        ht.table[i].u = 1
    with pytest.raises(OverflowError):
        ht.insert("АА", "1")

def test_search(ht):
    ht.insert("АА", "1")
    ht.insert("АА1", "2")
    assert ht.search("АА") == "1"
    assert ht.search("АА1") == "2"

def test_search_not_found(ht):
    with pytest.raises(KeyError):
        ht.search("ББ")

def test_update(ht):
    ht.insert("АА", "1")
    ht.update("АА", "2")
    assert ht.search("АА") == "2"

def test_update_collision_chain(ht):
    ht.insert("АА", "1")
    ht.insert("АА1", "2")
    ht.update("АА1", "3")
    assert ht.search("АА1") == "3"

def test_update_not_found(ht):
    with pytest.raises(KeyError):
        ht.update("ББ", "2")

def test_delete(ht):
    ht.insert("АА", "1")
    ht.delete("АА")
    assert ht.elements_count == 0
    idx = ht.get_hash("АА")
    assert ht.table[idx].u == 0
    assert ht.table[idx].d == 1
    with pytest.raises(KeyError):
        ht.search("АА")

def test_delete_not_found(ht):
    with pytest.raises(KeyError):
        ht.delete("АА")

def test_delete_chain(ht):
    ht.insert("АА", "1")
    ht.insert("АА1", "2")
    ht.delete("АА")
    assert ht.search("АА1") == "2"

def test_clear(ht):
    ht.insert("АА", "1")
    ht.clear()
    assert ht.elements_count == 0
    assert ht.table[0].u == 0
    assert ht.table[0].key == ""

def test_get_load_factor(ht):
    assert ht.get_load_factor() == 0.0
    ht.insert("АА", "1")
    assert ht.get_load_factor() == 0.2
    ht.insert("ББ", "2")
    assert ht.get_load_factor() == 0.4