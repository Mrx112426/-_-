from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable

T = TypeVar("T")


class EmptyQueueException(Exception):
    pass


@dataclass
class SingleNode(Generic[T]):
    data: T
    next_ptr: Optional['SingleNode[T]'] = None


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._length: int = 0
        self._head: Optional[SingleNode[T]] = None
        self._tail: Optional[SingleNode[T]] = None

    def get_size(self) -> int:
        return self._length

    def is_empty(self) -> bool:
        return self._length == 0

    def enqueue(self, value: T):
        node = SingleNode[T](value, None)
        if self._length == 0:
            self._head = node
            self._tail = node
            self._length += 1
            return

        self._tail.next_ptr = node
        self._tail = node
        self._length += 1

    def dequeue(self) -> T:
        if self.is_empty():
            raise EmptyQueueException("EmptyQueueException")
        node = self._head
        self._head = node.next_ptr
        self._length -= 1
        return node.data

    def peak(self) -> T:
        if self.is_empty():
            raise EmptyQueueException("Queue is empty")
        return self._head.data

MySetType = dict[T, None]


class MySet(Generic[T]):

    def __init__(self, *arg) -> None:
        self._set: MySetType = {}
        if len(arg) == 0:
            return
        for it in list(arg):
            self.add(it)

    def add(self, value: T) -> bool:
        length = len(self._set)
        self._set[value] = None
        return length != len(self._set)

    def is_empty(self) -> bool:
        return len(self._set) == 0

    def size(self) -> int:
        return len(self._set)

    def remove_all(self) -> None:
        self._set: MySetType = {}

    def contains(self, value: T) -> bool:
        return value in self._set

    def for_each(self, func: Callable[[T], None]) -> None:
        if self.size() == 0:
            return
        for k in self._set.keys():
            func(k)