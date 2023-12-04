import timeit
import ctypes
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar("T")

@dataclass
class Cat:
    name: str
    age: int

    def __str__(self) -> str:
        return f"Cat({self.name},{self.age})"

class QueueOverFlowException(Exception):
    pass

class EmptyQueueException(Exception):
    pass

class QueueArray(Generic[T]):

    def __init__(self, size : int) -> None:
        self._lenght : int = 0
        self._fixed_size: int = size
        self._arr: ctypes.Array[T] = (size * ctypes.py_object)()

    def get_size(self) -> int:
        return self._lenght

    def is_empty(self) -> bool:
        return self._lenght == 0

    def push(self, value: T):
        if self._lenght >= self._fixed_size:
            raise QueueOverFlowException(f"QueueOverFlowException {value}")
        self._arr[self._lenght] = value
        self._lenght += 1

    def pop(self) -> T:
        if self.is_empty():
            raise EmptyQueueException(f"EmptyQueueException ")
        data = self._arr[0]
        for i in range(1, self._lenght):
            self._arr[i-1] = self._arr[i]
        self._lenght -=1
        return data

    def peek(self) -> T:
        if self.is_empty():
            raise EmptyQueueException(f"EmptyQueueException ")
        return self._arr[0]

    def print_stack(self) -> None:
        if self.is_empty():
            print("is_empty")
        my_list : list[T] = []
        for i in range(0,self._lenght):
            my_list.append(self._arr[i])
        print(f"Queue : {my_list}")




if __name__ == "__main__":
    print("Тесты")
    fix_size : int = 3
    queue : QueueArray[Cat] = QueueArray[Cat](fix_size)
    try:
        queue.push(Cat("Max", 4))
        queue.push(Cat("Alec", 5))
        queue.push(Cat("Tom", 7))
        queue.print_stack()
        queue.push(Cat("Max", 4))
    except QueueOverFlowException as ex:
        print(ex)

    print(f"Head -  {queue.peek()}")

    print("POP")
    try:
        for i in range(0, fix_size + 1):
            pop_value = queue.pop()
        print(f"Queue head value : {pop_value}")

    except EmptyQueueException as ex:
        print(ex)