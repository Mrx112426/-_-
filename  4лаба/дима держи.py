import ctypes
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

T = TypeVar("T")


class IndexOutRangeException(Exception):
    pass


@dataclass
class Book:
    author: str
    publisher: str
    pages: int
    price: float
    ISBN: str

    def __str__(self) -> str:
        return f"Book({self.author}, {self.publisher}, {self.pages}, {self.price}, {self.ISBN})"


class DynamicArray(Generic[T]):

    def __init__(self, capacity: int) -> None:
        self._length: int = 0
        self._capacity: int = capacity
        self._arr: ctypes.Array[T] = (capacity * ctypes.py_object)()

    def get_length(self) -> int:
        return self._length

    def get_capacity(self) -> int:
        return self._capacity

    def _resize(self, new_capacity: int) -> None:
        new_array: ctypes.Array[T] = (new_capacity * ctypes.py_object)()
        for it in range(self._length):
            new_array[it] = self._arr[it]

        self._arr = new_array
        self._capacity = new_capacity
        print(f"New capacity = {new_capacity}")

    def _check_range(self, index: int) -> bool:
        if index >= self._length or index < 0:
            return False
        return True

    def is_empy(self) -> bool:
        return self._length == 0

    def add(self, element: T) -> None:
        if self._length == self._capacity:
            self._resize(self._capacity * 2)

        self._arr[self._length] = element
        self._length += 1
        print(self)

    def get(self, index: int) -> T:
        ok: bool = self._check_range(index)
        if not ok:
            raise IndexOutRangeException("-_-")

        return self._arr[index]

    def remove(self, index: int) -> bool:
        ok: bool = self._check_range(index)
        if not ok:
            return False

        for i in range(index, self._length - 1):
            self._arr[i] = self._arr[i + 1]
        self._length -= 1
        return ok

    def put(self, index: int, element: T) -> bool:
        ok: bool = self._check_range(index)
        if not ok:
            return False

        self._arr[index] = element
        return ok

    def quick_sort_price_desc(self) -> None:
        def comp(book1, book2):
            return book1.price > book2.price

        self._quick_sort(comp, 0, self._length - 1)

    def _quick_sort(self, comp: Callable[[T, T], bool], low: int, high: int) -> None:
        if low < high:
            pi = self._partition(comp, low, high)
            self._quick_sort(comp, low, pi - 1)
            self._quick_sort(comp, pi + 1, high)

    def cocktail_sort_ISBN(self) -> None:
        def comp(book1, book2):
            return book1.ISBN > book2.ISBN

        self._cocktail_sort(comp)

    def _cocktail_sort(self, comp: Callable[[T, T], bool]) -> None:
        left = 0
        right = self._length - 1

        while left <= right:
            for i in range(right, left, -1):
                if comp(self._arr[i - 1], self._arr[i]):
                    self._arr[i - 1], self._arr[i] = self._arr[i], self._arr[i - 1]
            left += 1
            for i in range(left, right):
                if comp(self._arr[i], self._arr[i + 1]):
                    self._arr[i], self._arr[i + 1] = self._arr[i + 1], self._arr[i]
            right -= 1

    def _partition(self, comp: Callable[[T, T], bool], low: int, high: int) -> int:
        pivot = self._arr[high]
        i = low - 1

        for j in range(low, high):
            if comp(self._arr[j], pivot):
                i = i + 1
                self._arr[i], self._arr[j] = self._arr[j], self._arr[i]

        self._arr[i + 1], self._arr[high] = self._arr[high], self._arr[i + 1]
        return i + 1

    def __str__(self) -> str:
        my_str = ""
        for it in range(self._length):
            my_str += str(self._arr[it]) + " "
        return f"Текущее состояние: [{my_str}]"


if __name__ == '__main__':
    dynamic_array = DynamicArray[Book](capacity=10)
    dynamic_array.add(Book("Автор1", "Издательство1", 300, 20.0, "1234567890"))
    dynamic_array.add(Book("Автор2", "Издательство2", 250, 15.0, "0987654321"))
    dynamic_array.add(Book("Автор3", "Издательство3", 400, 30.0, "1111111111"))

    print(dynamic_array)

    dynamic_array.quick_sort_price_desc()
    print("Быстрая сортировка по цене в убывающем порядке:")
    print(dynamic_array)

    dynamic_array.cocktail_sort_ISBN()
    print("Сортировка перемешиванием по ISBN в убывающем порядке:")
    print(dynamic_array)