import timeit
import ctypes
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

K = TypeVar("K", str, int)
V = TypeVar("V")


@dataclass
class Cat:
    name: str
    age: int

    def __str__(self) -> str:
        return f"Cat({self.name},{self.age})"


@dataclass
class Node(Generic[K, V]):
    key: K
    value: V
    next_ptr: Optional['Node[K, V]'] = None


class HashTable(Generic[K, V]):

    def __init__(self, capacity: int) -> None:
        self._size: int = 0
        self._capacity: int = capacity
        self._table: ctypes.Array[Optional[Node[K, V]]] = (
            capacity * ctypes.py_object)()
        for i in range(0, capacity):
            self._table[i] = None

    def _hash(self, key: K) -> int:
        h = hash(key)
        return (self._capacity - 1) & (h ^ (h >> 16))

    def _resolve_put_collision(self, key: K, value: V, index: int) -> None:
        self._table[index] = Node(
            key=key, value=value, next_ptr=self._table[index])
        print(f"Collision: (index: {index}, key: {key}, value: {value})")

    def capacity(self) -> int:
        return self._capacity

    def _resolve_put_collision(self, key: K, value: V, index: int) -> None:
        if self._table[index] is None:
            self._table[index] = Node(key=key, value=value)
        else:
            # Перезапись существующих данных по ключу
            current_node: Node[K, V] = self._table[index]
            while current_node is not None:
                if current_node.key == key:
                    current_node.value = value
                    return
                current_node = current_node.next_ptr

        # Если ключ не был найден в цепочке, добавляем новый элемент в начало цепочки
        self._table[index] = Node(key=key, value=value, next_ptr=self._table[index])

    def put(self, key: K, value: V):
        index: int = self._hash(key)

        if self._table[index] is None:
            self._table[index] = Node(key=key, value=value)
        else:
            self._resolve_put_collision(key, value, index)  # Коллизия
        self._size += 1

    def get(self, key: K) -> Optional[V]:
        index: int = self._hash(key)
        if self._table[index] is None:
            return None

        current_node: Node[K, V] = self._table[index]
        while current_node is not None:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next_ptr

        return None

    def contains(self, key: K) -> bool:
        return self.get(key) is not None

    def remove(self, key: K) -> bool:
        index: int = self._hash(key)
        if self._table[index] is None:
            return False

        current_node: Node[K, V] = self._table[index]
        if current_node.key == key:
            self._table[index] = current_node.next_ptr
            del current_node
            self._size -= 1
            return True

        prev_node: Optional[Node[K, V]] = None
        del_node: Optional[Node[K, V]] = None
        while current_node.next_ptr is not None:
            if current_node.next_ptr.key == key:
                prev_node = current_node
                del_node = current_node.next_ptr
                break
            current_node = current_node.next_ptr

        if prev_node is None and del_node is None:
            return False

        prev_node.next_ptr = del_node.next_ptr
        del del_node
        self._size -= 1
        return True

    def keys(self) -> list[K]:
        keys: list[K] = []
        for it in self._table:
            if it is not None:
                current_node: Node[K, V] = it
                while current_node is not None:
                    keys.append(current_node.key)
                    current_node = current_node.next_ptr

        return keys

    def values(self) -> list[V]:
        values: list[V] = []
        for it in self._table:
            if it is not None:
                current_node: Node[K, V] = it
                while current_node is not None:
                    values.append(current_node.value)
                    current_node = current_node.next_ptr

        return values

    def clear(self) -> None:
        self._size = 0
        self._table: ctypes.Array[Optional[Node[K, V]]] = ((self._capacity *
                                                            ctypes.py_object)(None))
        for i in range(0, self._capacity):
            self._table[i] = None

    def for_each(self, func: Callable[[K, V], None]) -> None:
        if self._size == 0:
            return
        for it in self._table:
            if it is not None:
                current_node: Node[K, V] = it
                while current_node is not None:
                    func(current_node.key, current_node.value)
                    current_node = current_node.next_ptr

    def __contains__(self, key: K) -> bool:
        return self.contains(key)

    def __getitem__(self, key: K) -> Optional[V]:
        return self.get(key)


if __name__ == '__main__':
    def print_hash_table(key: K, value: V) -> None:
        print(f"Table element: {key}:{value}")

    hash_table: HashTable = HashTable[str, Cat](10)
    hash_table.put("Home", Cat("Alex", 4))
    hash_table.put("1", Cat("Tom", 6))
    hash_table.put("2", Cat("Tommy", 6))
    hash_table.put("2", Cat("Max", 1))
    hash_table.put("3", Cat("Alex", 4))
    hash_table.put("4", Cat("Tom", 6))
    hash_table.put("5", Cat("Tommy", 6))
    hash_table.put("Work", Cat("Max", 1))
    hash_table.for_each(print_hash_table)
    print("Check 1 in hash_table:", hash_table.contains("1"))
    print("Check Work in hash_table:", hash_table.contains("Work"))

    print("-----Get Value------")
    print(hash_table.get("1"))  # поменяйте на 0

    print("-----Remove ------")
    print(hash_table.remove("Work"))
    print(hash_table.remove("5"))
    hash_table.for_each(print_hash_table)

    print("-----Keys  ------")
    print(hash_table.keys())
    print("-----Values ------")
    print(hash_table.values())

    print("-----Сontains ------")
    print(hash_table.contains("2"))

    # Добавляем бенчмарки сюда:
    import timeit

    def benchmark_put():
        hash_table = HashTable[str, Cat](1000)
        for i in range(1000):
            key = f"Ключ_{i}"
            value = Cat(f"Кот_{i}", i)
            hash_table.put(key, value)

    def benchmark_get():
        hash_table = HashTable[str, Cat](1000)
        for i in range(1000):
            key = f"Ключ_{i}"
            value = Cat(f"Кот_{i}", i)
            hash_table.put(key, value)

        for i in range(1000):
            key = f"Ключ_{i}"
            полученное_значение = hash_table.get(key)

    put_time = timeit.timeit(benchmark_put, number=1000)
    print(f"Среднее время для 1000 операций 'put': {put_time} секунд")

    get_time = timeit.timeit(benchmark_get, number=1000)
    print(f"Среднее время для 1000 операций 'get': {get_time} секунд")









