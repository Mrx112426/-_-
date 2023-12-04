import ctypes
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar("T")

class StackOverFlowException(Exception):#создаем исключения
    pass

class EmptyStackException(Exception):#создаем исключения
    pass

@dataclass
class Cat:
    name: str
    age: int

    def __str__(self) -> str:
        return f"Cat({self.name}, {self.age})"

@dataclass
class SingleNode(Generic[T]):
    data: T
    next_ptr: Optional['SingleNode[T]'] = None

class StackLinkedList(Generic[T]):

    def __init__(self, size: int) -> None:
        self._length: int = 0
        self.fixed_size: int = size
        self._head: Optional[SingleNode[T]] = None

    def get_size(self) -> int:#возвращает размер стэка
        return self._length

    def is_empty(self) -> bool:#проверка на пустоту
        return self._length == 0

    def push(self, value: T):#добавляет элемент в верхушку стека.
        if self._length >= self.fixed_size:
            raise StackOverFlowException(f"StackOverflowException : {value}")
        node = SingleNode[T](value, None)
        if self._length == 0:
            self._head = node
            self._length += 1
            return

        node.next_ptr = self._head
        self._head = node
        self._length += 1

    def pop(self) -> T:#удаляет и возвращает элемент из верхушки стека. Если стек пуст, он вызывает исключение
        if self.is_empty():
            raise EmptyStackException("EmptyStackException")
        node = self._head
        self._head = node.next_ptr
        node.next_ptr = None
        self._length -= 1
        return node.data

    def peek(self) -> T: #возвращает элемент из верхушки стека без его удаления. Если стек пуст, он выводит сообщение "Стек пуст".
        if self.is_empty():
            print("Стек пуст")
        return self._head.data

    def print_stack(self) -> None: #выводит содержимое стека в виде списка элементов. Если стек пуст, он выводит сообщение "Стек пуст"
        if self.is_empty():
            print("Стек пуст")
        my_list: list[T] = []
        current_node = self._head
        my_list.append(current_node.data)
        while current_node.next_ptr is not None:
            current_node = current_node.next_ptr
            my_list.append(current_node.data)
        print(f"Стек: {my_list}")

    def contains_element_iteration(self, value: T) -> bool:
        """
        Проверяет наличие элемента в стеке с использованием итерации.
        Args:
            value (T): Элемент, наличие которого нужно проверить.
        Returns:
            bool: True, если элемент найден в стеке, иначе False.
        """
        current_node = self._head
        while current_node is not None:
            if current_node.data == value:
                return True
            current_node = current_node.next_ptr
        return False

    def contains_element_recursion(self, value: T, current_node: Optional[SingleNode[T]] = None) -> bool:
        """
        Проверяет наличие элемента в стеке с использованием рекурсии.
        Args:
            value (T): Элемент, наличие которого нужно проверить.
            current_node (Optional[SingleNode[T]]): Текущий узел для рекурсии (используется внутренне).
        Returns:
            bool: True, если элемент найден в стеке, иначе False.
        """
        if current_node is None:
            current_node = self._head
        if current_node is None:
            return False
        if current_node.data == value:
            return True
        return self.contains_element_recursion(value, current_node.next_ptr)


if __name__ == "__main__":
    fix_size: int = 3
    stack = StackLinkedList[Cat](fix_size)
    try:
        stack.push(Cat("Tommy", 5))
        stack.push(Cat("Tommy", 4))
        stack.push(Cat("Tommy", 3))
        stack.print_stack()
        stack.push(Cat("Tommy", 2))
    except StackOverFlowException as ex:
        print(ex)

    print(f"Значение головного элемента стека: {stack.peek()}")
    print(" ")

    print("Проверка наличия элемента в стеке с использованием итерации:")
    print(stack.contains_element_iteration(Cat("Tommy", 4)))  # Должно вернуть True
    print(stack.contains_element_iteration(Cat("Tommy", 6)))  # Должно вернуть False
    print(" ")

    print("Извлечение элементов из стека")
    try:
        for i in range(0, fix_size + 1):
            pop_value = stack.pop()
            print(f"Значение головного элемента стека: {pop_value}")
    except EmptyStackException as ex:
        print(ex)

    print(" ")
    print("Проверка наличия элемента в стеке с использованием рекурсии:")
    print(stack.contains_element_recursion(Cat("Tommy", 4)))  # Должно вернуть False
    print(stack.contains_element_recursion(Cat("Tommy", 6)))  # Должно вернуть False



