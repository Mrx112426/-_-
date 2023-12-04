import ctypes
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")

class IndexOutRangeException(Exception):
    pass

@dataclass
class Cat:
    name : str
    age : int


    def __str__(self) -> str:
        return f"Cat({self.name},{self.age})"


class DynamicArray(Generic[T]):


    def __init__(self, capacity : int) -> None:
        self._lengt : int = 0
        self._capacity: int = capacity
        self._arr: ctypes.Array[T] = (capacity * ctypes.py_object)()

    def get_lengt(self) -> int:#длина
        return self._lengt

    def get_capacity(self) -> int:#вместимость
        return self._capacity

    def _check_range(self, index: int) -> bool:#проверка на выход из-за границ
        if index >= self._lengt or index <0:
            return False
        return True

    def _resize(self, new_capacity: int ) -> None: #изменение размера массива
        new_array: ctypes.Array[T] = (new_capacity * ctypes.py_object)()
        for it in range(self._lengt):
            new_array[it] = self._arr[it]

        self._arr = new_array
        self._capacity = new_capacity
        print(f"New_capacity = {new_capacity}")

    def is_empy(self) -> bool:#проверка на пустоту
        return self._lengt == 0

    def add(self, element : T) -> None: #добавление нового элемента
        if self._lengt == self._capacity:
            self._resize(self._capacity * 2)

        self._arr[self._lengt] = element
        self._lengt +=1
        print(self)

    def get(self, index : int) -> T:
        ok : bool = self._check_range(index)
        if not ok:
            raise IndexOutRangeException("wtf")

        return self._arr[index]

    def remove(self, index : int) -> bool:
        ok : bool = self._check_range(index)
        if not ok:
            return False

        for i in range(index, self._lengt-1):
            self.arr[i] = self.arr[i+1]
        self._lengt -=1
        return ok

    def put(self, index : int, element : T) ->bool:
        ok : bool = self._check_range(index)
        if not ok:
            return False
        self._arr[index] = element
        return ok

    def __str__(self) -> str:
        my_str : str = ""
        for it in range(self._lengt):
            my_str += str(self._arr[it]) + " "
        return f"Current state [{my_str}]"

if __name__ == "__main__":
    dynamic_array = DynamicArray[Cat](capacity = 3)
    dynamic_array.add(Cat("Max", 4))
    dynamic_array.add(Cat("Tom", 4))
    dynamic_array.add(Cat("Katya", 4))
    dynamic_array.put(2, Cat("Lexa", 4))
    print(dynamic_array)

