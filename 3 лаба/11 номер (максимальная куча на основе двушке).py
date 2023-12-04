import timeit
import random
import pickle
import ctypes
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

class IKey(ABC):
    @abstractmethod
    def key(self) -> int:
        ...

T = TypeVar("T", bound=IKey)

class HeapOverflowException(Exception):
    pass

class EmptyHeapException(Exception):
    pass

class IndexOutOfRangeException(Exception):
    pass

@dataclass
class Student(IKey):
    name: str
    group_number: str
    course: int
    age: int
    average_grade: float

    def key(self) -> float:
        return self.average_grade

    def __str__(self) -> str:
        return f"Student({self.name}, {self.group_number}, {self.course}, {self.age}, {self.average_grade})"

def compare_students(a: Student, b: Student) -> bool:
    return a.average_grade <= b.average_grade

class MaxHeapNode(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self.prev = None  # Ссылка на предыдущий узел
        self.next = None  # Ссылка на следующий узел

class MaxHeap(Generic[T]):

    def __init__(self, size: int,
                 fixed: bool = False,
                 comp: Callable[[T, T], bool] = compare_students):
        self._length: int = 0
        self._capacity: int = size
        self._is_fixed: bool = fixed
        self._comp: Callable[[T, T], bool] = comp
        self._root: MaxHeapNode[T] = None

    @staticmethod
    def create_heap_from_list(data: list[T],
                              fixed: bool = True,
                              comp: Callable[[T, T], bool] = compare_students) -> 'MaxHeap[T]':
        heap: MaxHeap[T] = MaxHeap[T](size=len(data), fixed=fixed, comp=comp)
        for item in data:
            heap.insert(item)
        return heap

    def _check_range(self, index: int) -> bool:
        if index >= self._length or index < 0:
            return False
        return True

    def _resize(self, new_capacity: int) -> None:
        new_array: ctypes.Array[T] = (new_capacity * ctypes.py_object)()
        current = self._root
        i = 0
        while current is not None:
            new_array[i] = current.value
            current = current.next
            i += 1

        self._root = MaxHeapNode[T](new_array[0])
        current = self._root
        for j in range(1, new_capacity):
            new_node = MaxHeapNode[T](new_array[j])
            current.next = new_node
            new_node.prev = current  # Устанавливаем обратную связь
            current = current.next

        self._capacity = new_capacity

    def is_empty(self) -> bool:
        return self._length == 0

    def get_size(self) -> int:
        return self._length

    def trickle_up(self, index: int) -> None:
        parent: int = (index - 1) // 2
        bottom: T = self._get_node_at_index(index).value

        while index > 0 and self._comp(self._get_node_at_index(parent).value, bottom):
            self._get_node_at_index(index).value = self._get_node_at_index(parent).value
            index = parent
            parent = (parent - 1) // 2

        self._get_node_at_index(index).value = bottom

    def _get_node_at_index(self, index: int) -> MaxHeapNode[T]:
        current = self._root
        for _ in range(index):
            current = current.next
        return current

    def trickle_down(self, index: int) -> None:
        large_child: int = 0
        top: T = self._get_node_at_index(index).value
        while index < self._length // 2:
            left_child: int = 2 * index + 1
            right_child: int = left_child + 1
            if (right_child < self._length and
                    self._comp(self._get_node_at_index(large_child).value, self._get_node_at_index(right_child).value)):
                large_child = right_child
            else:
                large_child = left_child

            if not self._comp(top, self._get_node_at_index(large_child).value):
                break

            self._get_node_at_index(index).value = self._get_node_at_index(large_child).value
            index = large_child

        self._get_node_at_index(index).value = top

    def change(self, index: int, new_value: T) -> None:
        ok: bool = self._check_range(index)
        if not ok:
            raise IndexOutOfRangeException("IndexOutOfRangeException")

        old_value: T = self._get_node_at_index(index).value
        self._get_node_at_index(index).value = new_value
        if self._comp(old_value, new_value):
            self.trickle_up(index)
        else:
            self.trickle_down(index)

    def insert(self, value: T) -> None:
        if self._length >= self._capacity:
            if self._is_fixed:
                raise HeapOverflowException(f"HeapOverflowException: {value}")
            else:
                self._resize(self._capacity * 2)

        new_node = MaxHeapNode[T](value)
        if self._root is None:
            self._root = new_node
        else:
            new_node.prev = None  # Новый узел становится корнем
            new_node.next = self._root
            self._root.prev = new_node
            self._root = new_node

        self.trickle_up(self._length)
        self._length += 1

    def remove(self) -> T:
        if self.is_empty():
            raise EmptyHeapException("EmptyHeapException")

        root_value: T = self._root.value

        if self._length == 1:
            self._root = None
        else:
            self._root = self._root.next
            self._root.prev = None  # Удаляем ссылку на предыдущий корень

        self.trickle_down(0)
        self._length -= 1

        return root_value

    def print_heap(self) -> None:
        current = self._root
        while current is not None:
            print(f"{current.value.average_grade} ", end='')
            current = current.next
        print()
        n_blanks, items_per_row, column, j = (32, 1, 0, 0)
        dots = 32 * "."
        print(dots * 2)
        current = self._root
        while current is not None:
            if column == 0:
                for _ in range(n_blanks):
                    print(" ", end='')
            print(f"{current.value.average_grade} ", end='')
            current = current.next
            j += 1
            if j >= self._length:
                break
            column += 1
            if column == items_per_row:
                n_blanks //= 2
                items_per_row *= 2
                column = 0
                print("")
            else:
                for _ in range(n_blanks * 2 - 2):
                    print(" ", end='')
        print("\n" + dots * 2)

    def save_to_file(self, filename: str):
        try:
            with open(filename, 'wb') as file:
                # Сериализуем объект кучи и записываем его в файл
                pickle.dump(self, file)
            print(f"Куча сохранена в {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении кучи в файл: {e}")

    @staticmethod
    def load_from_file(filename: str) -> 'MaxHeap[T]':
        try:
            with open(filename, 'rb') as file:
                # Десериализуем объект кучи из файла
                heap = pickle.load(file)
            print(f"Куча загружена из файла {filename}")
            return heap
        except Exception as e:
            print(f"Ошибка при загрузке кучи из файла: {e}")
            return None

    def contains(self, key: int) -> bool:
        return any(item.value.key() == key for item in self._traverse_heap())

    def _traverse_heap(self):
        current = self._root
        while current is not None:
            yield current
            current = current.next

    def contains_recursive(self, key: int) -> bool:
        return self._contains_recursive(self._root, key)

    def _contains_recursive(self, current: MaxHeapNode[T], key: float) -> bool:
        if current is None:
            return False
        if current.value.key() == key:
            return True
        return self._contains_recursive(current.next, key)

def insertion_benchmark(heap, size):
    random_students = [
        Student(f"Student {i}", "Group", random.randint(1, 5), random.randint(18, 25), random.uniform(2, 5))
        for i in range(size)]

    def insert():
        for student in random_students:
            heap.insert(student)

    insert_time = timeit.timeit(insert, number=1)
    return insert_time



# Пример использования
if __name__ == '__main__':
    students = [
        Student("Dima", "4217", 2, 18, 5),
        Student("Alexander", "4217", 3, 19, 12),
        Student("Sherzod", "4217", 2, 19, 47),
        Student("Nikita", "4217", 2, 19, 91),
        Student("Lizza", "4217", 2, 19, 65),
        Student("Nefor", "4217", 2, 19, 10),
        Student("Nastya", "4217", 2, 19, 86),
        Student("Nastasha", "4217", 2, 19, 76),
        Student("Vladislav", "4217", 2, 18, 44),
        Student("Umar", "4217", 2, 19, 97),
    ]

    # Создание кучи и вставка студентов
    heap = MaxHeap.create_heap_from_list(students)
    heap.print_heap()
    print("\nПроверка вхождения элемента")
    # Проверка вхождения элемента с использованием метода contains
    key_to_check = 91.0
    if heap.contains(key_to_check):
        print(f"Элемент со средней оценкой {key_to_check} найден.")
    else:
        print(f"Элемент со средней оценкой {key_to_check} не найден.")

    # Проверка вхождения элемента с использованием метода contains_recursive
    key_to_check = 70.0
    if heap.contains_recursive(key_to_check):
        print(f"Элемент со средней оценкой {key_to_check} найден.")
    else:
        print(f"Элемент со средней оценкой {key_to_check} не найден.")

    print("\nСохранение кучи в файл")
    # Сохранение кучи в файл
    heap.save_to_file("heap_data.pkl")

    print("\nЗагрузка кучи из файла")
    # Загрузка кучи из файла
    loaded_heap = MaxHeap.load_from_file("../асд/heap_data.pkl")
    # if loaded_heap:
    #     loaded_heap.print_heap()

    print("\nСмена элемента")
    heap.change(2, Student("Nastasha", "4217", 2, 19, 99))
    heap.print_heap()

    print("\nУдаление элемента")  # он удаляет элемент из корня кучи
    heap.remove()
    heap.print_heap()

    student_to_add = Student("New Student", "1234", 1, 20, 95)
    print(f"\nДобавление элемента {student_to_add} ")
    heap.insert(student_to_add)
    heap.print_heap()

    benchmark_size = 1000  # Размер данных для бенчмарков

    print("\nBenchmark вставки элемента ")
    initial_capacity = benchmark_size + 1  # Установите начальную емкость больше, чем размер бенчмарка
    heap = MaxHeap(size=initial_capacity)  # Создаем кучу с начальной емкостью
    insert_time = insertion_benchmark(heap, benchmark_size)
    print(f"Время для вставки {benchmark_size} элементов: {insert_time:.6f} секунд")



