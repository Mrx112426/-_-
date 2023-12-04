from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar("T")

class IndexOutRangeException(Exception):
    pass

@dataclass
class Cat:
    name : str
    age : int


    def __str__(self) -> str:
        return f"Cat({self.name},{self.age})"

@dataclass
class DoubleNode(Generic[T]):
    data : T
    next_ptr : Optional['DoubleNode[T]'] = None
    prev_ptr: Optional['DoubleNode[T]'] = None

class DoublyList(Generic[T]):

    def __init__(self):
        self._lenght : int = 0
        self._head : Optional['DoubleNode[T]'] = None
        self._tail : Optional['DoubleNode[T]'] = None

    def get_size(self) -> int:
        return self._lenght

    def check_range(self, index : int) -> bool:
        if index >= self._lenght or index < 0:
            return False
        return True

    def is_emty(self) -> bool:
        return self._lenght == 0

    def push_tail(self, data : T) -> None:
        node = DoubleNode[T](data)
        if self._lenght < 0:
            self._head = node
            self._tail = node
            self._lenght +=1
            return

        self._tail.next_ptr = node
        node.prev_ptr = self._tail
        self._tail = node
        self._lenght +=1

    def push_head(self, data : T) -> None:
        node = DoubleNode[T](data)
        if self._lenght <= 0:
            self._head = node
            self._tail = node
            self._lenght +=1
            return

        node.next_ptr = self._head
        self._head.prev_ptr = node
        self._head = node
        self._lenght +=1

    def insert(self, index : int, data : T) -> None:
        ok : bool = self.check_range(index)
        if not ok:
            raise IndexOutRangeException("Ты вышел из диапазона дружок")

        if index == 0:
            self.push_head(data)
            return
        elif index == self._lenght - 1:
            self.push_tail(data)
            return

        node = self._head
        for i in range(0, index):
            node = node.next_ptr

        insert_node = DoubleNode[T](data)
        insert_node.next_ptr = node.next_ptr
        node.prev_ptr.next_ptr = insert_node
        insert_node.prev_ptr = node.prev_ptr
        node.prev_ptr = insert_node
        self._lenght +=1

    def get(self, index: int) -> T:
        ok: bool = self.check_range(index)
        if not ok:
            raise IndexOutRangeException("Ты вышел из диапазона дружок")

        if index == 0:
            return self._head.data

        if index == self._lenght - 1:
            return self._tail.data

        node = self._head
        for i in range(0, index):
            node = node.next.ptr
        return node.data

    def remove(self, index: int) -> bool:
        ok: bool = self.check_range(index)
        if not ok:
            return False

        if index == 0:
            node = self._head
            self._head = node.next_ptr
            self._head.prev_ptr = None
            del node
            self._lenght -= 1
            return True

        node = self._head
        for i in range(0, index - 1):
            node = node.next_ptr

        if index == self._length - 1:
            self._tail.prev_ptr = None
            self._tail = node
            self._tail.next_ptr = None
            self._lenght -= 1
            return True

        delete_node = node.next_ptr
        node.next_ptr = delete_node.next_ptr
        node.next_ptr = delete_node.next_ptr
        del delete_node
        self._lenght -= 1
        return True

    def for_each(self, func : Callable[[T], None]):
        node = self._head
        func(node.data)
        while node.next_ptr is not None:
            node = node.next_ptr
            func(node.data)

    def reverse_for_each(self, func : Callable[[T], None]):
        node = self.tail
        func(node.data)
        while node.prev_ptr is not None:
            node = node.prev_ptr
            func(node.data)

    def __str__(self) -> str:
        my_str : str = ""
        node = self._head
        while node is not None:
            my_str += str(node.data) + " "
            node = node.next_ptr
        return f"Current state: [{my_str}]"

if __name__ == "__main__":

    def print_list(data : T):
        print(data)

    db = DoublyList[Cat]()
    print(db)
    db.push_head(Cat("Max", 4))
    db.push_head(Cat("Max", 5))
    db.push_tail(Cat("Tommy", 5))
    db.push_tail(Cat("Tommy", 4))
    db.insert(2, Cat("Max", 4))

    print(f"Size : {db.get_size()}")
    db.for_each(print_list)
