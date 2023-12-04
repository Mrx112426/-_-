import timeit
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar("T")

# Исключение для обработки ситуации, когда индекс выходит за пределы допустимого диапазона
class IndexOutOfRangeException(Exception):
    pass

@dataclass
class Cat:
    name: str
    age: int

    def __str__(self) -> str:
        return f"Cat({self.name}, {self.age})"

@dataclass
class DoubleNode(Generic[T]):
    data: T
    next_ptr: Optional['DoubleNode[T]'] = None
    prev_ptr: Optional['DoubleNode[T]'] = None

class DoublyList(Generic[T]):

    def __init__(self):
        # Инициализация двусвязного списка
        self._length: int = 0  # Длина списка
        self._head: Optional['DoubleNode[T]'] = None  # Головной узел (первый элемент)
        self._tail: Optional['DoubleNode[T]'] = None  # Хвостовой узел (последний элемент)

    def get_size(self) -> int:
        # Возвращает текущую длину списка
        return self._length

    def check_range(self, index: int) -> bool:
        # Проверяет, находится ли индекс в допустимом диапазоне
        if index >= self._length or index < 0:
            return False
        return True

    def is_empty(self) -> bool:
        # Проверяет, пуст ли список
        return self._length == 0

    def push_tail(self, data: T) -> None:
        # Добавляет элемент в конец списка
        node = DoubleNode[T](data)
        if self._length == 0:
            # Если список пуст, новый элемент становится и головой, и хвостом
            self._head = node
            self._tail = node
        else:
            # В противном случае, новый элемент связывается с текущим хвостовым элементом
            self._tail.next_ptr = node
            node.prev_ptr = self._tail
            self._tail = node
        self._length += 1

    def push_head(self, data: T) -> None:
        # Добавляет элемент в начало списка
        node = DoubleNode[T](data)
        if self._length == 0:
            # Если список пуст, новый элемент становится и головой, и хвостом
            self._head = node
            self._tail = node
        else:
            # В противном случае, новый элемент связывается с текущей головой
            node.next_ptr = self._head
            self._head.prev_ptr = node
            self._head = node
        self._length += 1

    def insert(self, index: int, data: T) -> None:
        # Вставляет элемент в указанный индекс списка
        if index == 0:
            # Если индекс равен 0, элемент добавляется в начало списка
            self.push_head(data)
        elif index == self._length:
            # Если индекс равен текущей длине, элемент добавляется в конец списка
            self.push_tail(data)
        else:
            if not self.check_range(index):
                raise IndexOutOfRangeException("Index out of range")
            node = self._head
            for i in range(index):
                node = node.next_ptr

            insert_node = DoubleNode[T](data)
            # Перенаправляем связи так, чтобы элемент вставлялся в указанный индекс
            insert_node.next_ptr = node
            insert_node.prev_ptr = node.prev_ptr
            node.prev_ptr.next_ptr = insert_node
            node.prev_ptr = insert_node
            self._length += 1

    def get(self, index: int) -> T:
        # Получает элемент по индексу
        if not self.check_range(index):
            raise IndexOutOfRangeException("Index out of range")
        node = self._head
        for i in range(index):
            node = node.next_ptr
        return node.data

    def remove(self, index: int) -> bool:
        # Удаляет элемент по индексу
        if not self.check_range(index):
            return False
        if index == 0:
            # Если индекс 0, удаляем первый элемент
            if self._length == 1:
                # Если в списке всего один элемент, обнуляем голову и хвост
                self._head = None
                self._tail = None
            else:
                node = self._head
                self._head = node.next_ptr
                self._head.prev_ptr = None
            self._length -= 1
            return True
        elif index == self._length - 1:
            # Если индекс равен текущей длине - 1, удаляем последний элемент
            node = self._tail
            self._tail = node.prev_ptr
            self._tail.next_ptr = None
            self._length -= 1
            return True
        else:
            # Удаляем элемент из середины списка
            node = self._head
            for i in range(index - 1):
                node = node.next_ptr
            delete_node = node.next_ptr
            node.next_ptr = delete_node.next_ptr
            delete_node.next_ptr.prev_ptr = node
            self._length -= 1
            return True

    def for_each(self, func: Callable[[T], None]):
        # Проходит по всем элементам списка и применяет функцию к каждому элементу
        node = self._head
        while node is not None:
            func(node.data)
            node = node.next_ptr

    def reverse_for_each(self, func: Callable[[T], None]):
        # Проходит по всем элементам списка в обратном порядке и применяет функцию к каждому элементу
        node = self._tail
        while node is not None:
            func(node.data)
            node = node.prev_ptr

    def contains(self, item: T) -> bool:
        #Проверяет наличие элемента в списке.

        return item in  self

    def shift(self, direct: str, n: int) -> None:
        #Циклически сдвигает элементы в заданном направлении на n позиций
        if n == 0:
            return

        if direct not in ('left', 'right'):
            raise ValueError("Invalid direction. Use 'left' or 'right'.")

        n = n % self._length  # Обработка случая, когда n больше длины списка

        if direct == 'left':
            # Сдвиг влево
            for _ in range(n):
                self._tail.next_ptr = self._head
                self._head.prev_ptr = self._tail
                self._head = self._head.next_ptr
                self._tail = self._tail.next_ptr
                self._tail.next_ptr = None
                self._head.prev_ptr = None
        if direct == 'right':
            # Сдвиг вправо
            for _ in range(n):
                self._head.prev_ptr = self._tail
                self._tail.next_ptr = self._head
                self._tail = self._tail.prev_ptr
                self._head = self._head.prev_ptr
                self._head.prev_ptr = None
                self._tail.next_ptr = None

    def __len__(self) -> int:
        # Возвращает текущую длину списка
        return self._length
        """

k = 0
node = self._head
while node in not None:
    k+=1
    node = node.next_ptr
    return k
"""


    def __str__(self) -> str:
        # Возвращает строковое представление списка
        my_str = ""
        node = self._head
        while node is not None:
            my_str += str(node.data) + " "
            node = node.next_ptr
        return f"Current state: [{my_str}]"

    def __contains__(self, item: T) -> bool:
        # Проверяет, содержит ли список заданный элемент.
        node = self._head
        while node is not None:
            if node.data == item:
                return True
            node = node.next_ptr
        return False

    def __getitem__(self, index: int) -> T:
        # Получает элемент списка по индексу
        if not self.check_range(index):
            raise IndexError("Index out of range")

        node = self._head
        for i in range(index):
            node = node.next_ptr
        return node.data

if __name__ == "__main__":

    def print_list(data : T):
        print(data)
#ТЕСТЫ
    print("Тесты")
    db = DoublyList[Cat]()
    print(db, "- создали 2-х связный список")
    print(f"Size : {db.get_size()}")
    db.push_head(Cat("Max", 4))

    print(" ")
    print("Метод push head (добавления в начало)")
    print(db)

    print(" ")
    print("Метод push tail (добавления в конец)")
    db.push_tail(Cat("Tommy", 5))
    db.push_tail(Cat("Tommy", 4))
    print(db)

    print(" ")
    print("Метод вставки по индексу (insert), в данном случае index = 1")
    db.insert(1, Cat("Max", 3))
    print(db)

    print(" ")
    print("Определение размера в данный момент (get_size)")
    print(f"Size : {db.get_size()}")

    print(" ")
    print("Метод for_each с функцией print_list")
    db.for_each(print_list)

    print(" ")
    print("Метод удаления по индексу (remove), в данном случае index = 2")
    db.remove(2)
    print(db)

    print(" ")
    print("Метод вызова по индексу (get), в данном случае index = 2")
    print(db.get(2))

    print(" ")
    print("Метод is_empty (Проверяет пустой ли список)")
    print(db.is_empty())

    print(" ")
    print("Метод check_range (Проверяет, находится ли индекс в допустимом диапазоне),в данном случае index = 2")
    print(db.check_range(2))

    print(" ")
    print("Метод shift (Циклически сдвигает элементы в заданном направлении на n позиций")
    print(db, " до выполнения метода shift")
    db.shift('left', 2)
    print(db, "После выполнения метода shift(left, 2)")

    print(" ")
    print("Метод __contains__ (Проверяет есть ли элемент в списке), в данном случае проверяет есть ли (Tommy, 4) ")
    print(Cat("Tommy", 4) in db)

    print(" ")
    print("Метод __getitem__ (Получает элемент списка по индексу), в данном случае возвращает db[2]  ")
    print(db[2])

    print(" ")
    print("Метод __len__ (Возвращает текущую длину списка) ")
    print(len(db))

    print(" ")
    print("Метод __str__ (Возвращает строковое представление списка) ")
    print(str(db))

#ЗАМЕРЫ ВРЕМЕНИ (БЕНЧМАРКИ)
    print(" ")
    print("Бенчмарки")
    def benchmark_push_tail():
        benchList = DoublyList()
        for i in range(1000):
            benchList.push_tail(i)

    def benchmark_push_head():
        benchList = DoublyList()
        for i in range(1000):
            benchList.push_head(i)


    def benchmark_shift_left():
        benchList = DoublyList()
        for i in range(1000):
            benchList.push_tail(i)

        def shift_left():
            benchList.shift('left', 1)

        time_elapsed = timeit.timeit(shift_left, number=1000)
        print("Время затраченное на сдвиг влево 1000 раз - ", time_elapsed, "секунд")


    def benchmark_shift_right():
        benchList = DoublyList()
        for i in range(1000):
            benchList.push_tail(i)

        def shift_right():
            benchList.shift('right', 1)

        time_elapsed = timeit.timeit(shift_right, number=1000)
        print("Время затраченное на сдвиг вправо 1000 раз - ", time_elapsed, "секунд")

    print(" ")
    print("Время затраченное на заполнение списка 10000 элементами методом push_tail - ",timeit.timeit(benchmark_push_tail, number=10000), "секунд")
    print(" ")
    print("Время затраченное на заполнение списка 10000 элементами методом push_head - ",timeit.timeit(benchmark_push_head, number=10000), "секунд")
    print(" ")
    print("Бенчмарк для метода shift влево")
    benchmark_shift_left()
    print(" ")
    print("Бенчмарк для метода shift вправо")
    benchmark_shift_right()
