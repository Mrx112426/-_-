import timeit
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar("T")

@dataclass
class Cat:
    name: str
    age: int

    def __str__(self) -> str:
        return f"Cat({self.name},{self.age})"

@dataclass
class DoubleNode(Generic[T]):
    data: T
    next_ptr: Optional['DoubleNode[T]'] = None
    prev_ptr: Optional['DoubleNode[T]'] = None

class StackOverFlowException(Exception):
    pass

class EmptyStackException(Exception):
    pass

@dataclass
class DoublyList(Generic[T]):

    def __init__(self):
        self._length: int = 0
        self._head: Optional['DoubleNode[T]'] = None
        self._tail: Optional['DoubleNode[T]'] = None

    def push_head(self, data: T) -> None:
        node = DoubleNode[T](data)
        if self._length == 0:
            # Если список пуст, новый узел становится как головой, так и хвостом.
            self._head = node
            self._tail = node
        else:
            # Иначе, новый узел становится головой, и связывается с предыдущей головой.
            node.next_ptr = self._head
            self._head.prev_ptr = node
            self._head = node
        self._length += 1

    def get(self, index: int) -> T:
        if not self.check_range(index):
            raise IndexError("Index out of range")
        node = self._head
        for i in range(index):
            node = node.next_ptr
        return node.data

    def remove(self, index: int) -> bool:
        if not self.check_range(index):
            return False
        if index == 0:
            if self._length == 1:
                # Если список состоит из одного элемента, обнуляем голову и хвост.
                self._head = None
                self._tail = None
            else:
                # Иначе, обновляем голову и перераспределяем связи.
                node = self._head
                self._head = node.next_ptr
                self._head.prev_ptr = None
            self._length -= 1
            return True
        elif index == self._length - 1:
            # Если удаляем последний элемент, обновляем хвост и перераспределяем связи.
            node = self._tail
            self._tail = node.prev_ptr
            self._tail.next_ptr = None
            self._length -= 1
            return True
        else:
            # Если удаляем элемент посередине, перераспределяем связи.
            node = self._head
            for i in range(index - 1):
                node = node.next_ptr
            delete_node = node.next_ptr
            node.next_ptr = delete_node.next_ptr
            delete_node.next_ptr.prev_ptr = node
            self._length -= 1
            return True

    def reverse_for_each(self, func: Callable[[T], None]):
        node = self._tail
        while node is not None:
            # Проходимся по элементам списка в обратном порядке и применяем функцию func к каждому элементу.
            func(node.data)
            node = node.prev_ptr

    def __str__(self) -> str:
        my_str = ""
        node = self._head
        while node is not None:
            my_str += str(node.data) + " "
            node = node.next_ptr
        return f"Current state: [{my_str}]"

    def check_range(self, index: int) -> bool:
        # Проверка, находится ли индекс в пределах списка.
        if index >= self._length or index < 0:
            return False
        return True

@dataclass
class StackDoublyLinkedList(Generic[T]):

    def __init__(self, size: int) -> None:
        self._length: int = 0
        self.fixed_size: int = size
        self._list: DoublyList[T] = DoublyList[T]()

    def get_size(self) -> int:
        # Возвращает текущий размер стека.
        return self._length

    def is_empty(self) -> bool:
        # Проверяет, пуст ли стек.
        return self._length == 0

    def push(self, value: T):
        if self._length >= self.fixed_size:
            # Проверка на переполнение стека.
            raise StackOverFlowException(f"StackOverflowException : {value}")
        self._list.push_head(value)
        self._length += 1

    def pop(self) -> T:
        if self.is_empty():
            # Проверка на пустой стек.
            raise EmptyStackException("EmptyStackException")
        pop_value = self._list.get(0)
        self._list.remove(0)
        self._length -= 1
        return pop_value

    def peek(self) -> T:
        if self.is_empty():
            # Если стек пуст, выводим сообщение.
            print("Стек пуст")
        return self._list.get(0)

    def print_stack(self) -> None:
        if self.is_empty():
            # Если стек пуст, выводим сообщение.
            print("Стек пуст")
        else:
            # Иначе, вызываем функцию print_list для вывода элементов стека.
            self._list.reverse_for_each(print_list)

    def contains_element_iteration(self, value: T) -> bool:
        #Проверяет наличие элемента в стеке с использованием итерации.
        node = self._list._head  # Начинаем с головного элемента списка
        while node is not None:
            if node.data == value:
                return True  # Если элемент найден, возвращаем True
            node = node.next_ptr  # Переходим к следующему элементу
        return False  # Если элемент не найден, возвращаем False

    def contains_element_recursion(self, value: T, current_node: Optional['DoubleNode[T]'] = None) -> bool:
        #Проверяет наличие элемента в стеке с использованием рекурсии.
        if current_node is None:
            current_node = self._list._head  # Начинаем с головного элемента списка
        if current_node is None:
            return False  # Если дошли до конца списка и не нашли элемент, возвращаем False
        if current_node.data == value:
            return True  # Если элемент найден, возвращаем True
        return self.contains_element_recursion(value, current_node.next_ptr)  # Рекурсивно проверяем следующий элемент


if __name__ == "__main__":
    print("Тесты")
    def print_list(data: T) -> None:
        # Функция для вывода элемента стека.
        print(data)

    fix_size: int = 3
    stack = StackDoublyLinkedList[Cat](fix_size)
    try:
        stack.push(Cat("Tommy", 5))
        stack.push(Cat("Tommy", 4))
        stack.push(Cat("Tommy", 3))
        stack.print_stack()
        stack.push(Cat("Tommy", 2))
    except StackOverFlowException as ex:
        # Обработка исключения при переполнении стека.
        print(ex)

    print(" ")
    print("Проверка на вхождение элемента (Tommy, 4) в стэке - ",stack.contains_element_iteration(Cat("Tommy", 4)))  # Должно вернуть True
    print("Проверка на вхождение элемента (Tommy, 6) в стэке - ",stack.contains_element_iteration(Cat("Tommy", 6)))  # Должно вернуть False

    print(" ")
    print(f"Значение головного элемента стека: {stack.peek()}")
    print(" ")

    print("Извлечение элементов из стека")
    try:
        for i in range(0, fix_size + 1):
            pop_value = stack.pop()
            print(f"Значение головного элемента стека: {pop_value}")
    except EmptyStackException as ex:
        # Обработка исключения при извлечении из пустого стека.
        print(ex)

    print(" ")
    print("Проверка на вхождение элемента (Tommy, 4) в стэке",stack.contains_element_recursion(Cat("Tommy", 4)))  # Должно вернуть False
    print("Проверка на вхождение элемента (Tommy, 6) в стэке",stack.contains_element_recursion(Cat("Tommy", 6)))  # Должно вернуть False

#Замеры времени
    print(" ")
    print("БЕНЧМАРКИ")
    def benchmark_push():
        stack = StackDoublyLinkedList[Cat](10000)

        def push():
            stack.push(Cat("Tommy", 5))

        time_elapsed = timeit.timeit(push, number=10000)
        print("Время затраченное на 10000 операций push - ", time_elapsed, "секунд")

    benchmark_push()


    def benchmark_pop():
        stack = StackDoublyLinkedList[Cat](10000)
        for i in range(10000):
            stack.push(Cat("Tommy", 5))

        def pop():
            stack.pop()

        time_elapsed = timeit.timeit(pop, number=10000)
        print("Время затраченное на 10000 операций pop - ", time_elapsed, "секунд")


    benchmark_pop()


    def benchmark_contains_iteration():
        stack = StackDoublyLinkedList[Cat](10000)
        for i in range(10000):
            stack.push(Cat("Tommy", i))

        def contains_iteration():
            stack.contains_element_iteration(Cat("Tommy", 500))

        time_elapsed = timeit.timeit(contains_iteration, number=10000)
        print("Время затраченное на 10000 операций проверки наличия с использованием итерации - ", time_elapsed,
              "секунд")


    benchmark_contains_iteration()
