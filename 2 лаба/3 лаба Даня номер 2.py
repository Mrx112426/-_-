from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Generic, Optional, Callable
from random import choice
import pickle
import timeit

# Определите абстрактный базовый класс (IKey) с единственным абстрактным методом 'key'.
class IKey(ABC):
    @abstractmethod
    def key(self) -> int:
        ...

# Определите типовую переменную T, которая привязана к IKey.
T = TypeVar("T", bound=IKey)

# Определите перечисление Color для представления цветов узлов в красно-черном дереве.
class Color(Enum):
    RED = 0
    BLACK = 1

# Определите dataclass Node, представляющий узел в красно-черном дереве.
@dataclass
class Node(Generic[T]):
    data: T
    parent: Optional['Node[T]'] = None
    left: Optional['Node[T]'] = None
    right: Optional['Node[T]'] = None
    color: Color = Color.RED

    # Метод key возвращает ключ узла.
    def key(self) -> int:
        return self.data.key()

    # Метод grandfather возвращает дедушку узла.
    def grandfather(self) -> Optional['Node[T]']:
        if self.parent is not None:
            return self.parent.parent
        return None

    # Метод uncle возвращает дядю узла.
    def uncle(self) -> Optional['Node[T]']:
        if self.parent is None or self.parent.parent is None:
            return None
        return self.parent.brother()

    # Метод brother возвращает брата узла.
    def brother(self) -> Optional['Node[T]']:
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left

# Функция _get_color возвращает цвет узла (красный или черный) или черный, если узел None.
def _get_color(node: Optional['Node[T]']) -> Color:
    if node is None:
        return Color.BLACK

# Определите исключение KeyNotFoundException (Исключение при отсутствии ключа).
class KeyNotFoundException(Exception):
    pass

# Определите исключение EmptyTreeException (Исключение при пустом дереве).
class EmptyTreeException(Exception):
    pass

# Определите исключение EmptyNodeException (Исключение при пустом узле).
class EmptyNodeException(Exception):
    pass

# Определите dataclass Car, реализующий интерфейс IKey.
@dataclass
class Car(IKey):
    brand: str
    vin: str
    engine_volume: float
    price: float
    average_speed: float

    # Метод key возвращает ключ (цену автомобиля).
    def key(self) -> float:
        return self.price

# Определите класс RBTree, представляющий собой красно-черное дерево для объектов T.
class RBTree(Generic[T]):

    # Конструктор класса RBTree.
    def __init__(self) -> None:
        self._length: int = 0
        self._root: Optional[Node[T]] = None

    # Метод is_empty возвращает True, если дерево пусто, иначе False.
    def is_empty(self) -> bool:
        return self._length == 0

    # Метод get_size возвращает размер дерева.
    def get_size(self) -> int:
        return self._length

    # Приватный метод __replace_node заменяет узел a узлом b.
    def __replace_node(self, a: Optional[Node[T]], b: Optional[Node[T]]) -> None:
        if a.parent is None:
            self._root = b
        else:
            if a == a.parent.left:
                a.parent.left = b
            else:
                a.parent.right = b

        if b is not None:
            b.parent = a.parent

    # Приватный метод __rotate_left выполняет левое вращение узла node.
    def __rotate_left(self, node: Node[T]) -> None:
        right = node.right
        self.__replace_node(node, right)
        node.right = right.left
        if right.left is not None:
            right.left.parent = node
        right.left = node
        node.parent = right

    # Приватный метод __rotate_right выполняет правое вращение узла node.
    def __rotate_right(self, node: Node[T]) -> None:
        left = node.left
        self.__replace_node(node, left)
        node.left = left.right
        if left.right is not None:
            left.right.parent = node
        left.right = node
        node.parent = left

    # Метод insert вставляет новое значение в дерево.
    def insert(self, value: T) -> None:
        new_node: Node[T] = Node(data=value, color=Color.RED)
        if self._root is None:
            self._root = new_node
            new_node = self._root
        else:
            current_node = self._root
            while True:
                if new_node.key() == current_node.key():
                    current_node.data = value
                    return
                if new_node.key() < current_node.key():
                    if current_node.left is None:
                        current_node.left = new_node
                        new_node = current_node.left
                        break
                    else:
                        current_node = current_node.left
                if new_node.key() > current_node.key():
                    if current_node.right is None:
                        current_node.right = new_node
                        new_node = current_node.right
                        break
                    else:
                        current_node = current_node.right
            new_node.parent = current_node
        self.__insert_case1(new_node)
        self._length += 1

    # Приватный метод __insert_case1 выполняет первое правило вставки в красно-черное дерево.
    def __insert_case1(self, node: Node[T]) -> None:
        if node.parent is None:
            node.color = Color.BLACK
        else:
            self.__insert_case2(node)

    # Приватный метод __insert_case2 выполняет второе правило вставки в красно-черное дерево.
    def __insert_case2(self, node: Node[T]) -> None:
        if _get_color(node.parent) == Color.BLACK:
            return
        self.__insert_case3(node)

    # Приватный метод __insert_case3 выполняет третье правило вставки в красно-черное дерево.
    def __insert_case3(self, node: Node[T]) -> None:
        uncle = node.uncle()
        if _get_color(uncle) == Color.RED:
            node.parent.color = Color.BLACK
            uncle.color = Color.BLACK
            node.grandfather().color = Color.RED
            self.__insert_case1(node.grandfather())
        else:
            self.__insert_case4(node)

    # Приватный метод __insert_case4 выполняет четвертое правило вставки в красно-черное дерево.
    def __insert_case4(self, node: Node[T]) -> None:
        grandfather = node.grandfather()
        if (node == node.parent.right and node.parent == grandfather.left):
            self.__rotate_left(node.parent)
            node = node.left
        elif (node == node.parent.left and node.parent == grandfather.right):
            self.__rotate_right(node.parent)
            node = node.right
        self.__insert_case5(node)

    # Приватный метод __insert_case5 выполняет пятое правило вставки в красно-черное дерево.
    def __insert_case5(self, node: Node[T]) -> None:
        node.parent.color = Color.BLACK
        grandfather = node.grandfather()
        grandfather.color = Color.RED
        if (node == node.parent.left and node.parent == grandfather.left):
            self.__rotate_right(grandfather)
        elif (node == node.parent.right and node.parent == grandfather.right):
            self.__rotate_left(grandfather)

    # Приватный метод __find_node выполняет поиск узла с заданным ключом.
    def __find_node(self, key: int) -> tuple[Optional[Node[T]], bool]:
        current_node = self._root
        while current_node.key() != key:
            if key < current_node.key():
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node is None:
                return None, False
        return current_node, True

    # Приватный метод __find_left_maximum_node выполняет поиск узла с максимальным ключом в левом поддереве.
    def __find_left_maximum_node(self, node: Node[T]) -> tuple[Optional[Node[T]], bool]:
        current_node = node.left
        if current_node is None:
            return None, False
        while current_node.right is not None:
            current_node = current_node.right
        return current_node, True

    # Метод remove удаляет узел с заданным ключом из дерева.
    def remove(self, key: int) -> None:
        if self.is_empty():
            raise EmptyTreeException("Дерево пусто")

        child_node: Optional[Node[T]] = None
        removing_node, ok = self.__find_node(key)
        if not ok:
            raise KeyNotFoundException("Ключ не найден")

        if removing_node.left is not None and removing_node.right is not None:
            successor, ok = self.__find_left_maximum_node(removing_node)
            if not ok:
                raise EmptyNodeException("Пустой узел")

            removing_node.data = successor.data
            removing_node = successor

        if removing_node.left is None or removing_node.right is None:
            if removing_node.right is None:
                child_node = removing_node.left
            else:
                child_node = removing_node.right

            if removing_node.color == Color.BLACK:
                removing_node.color = _get_color(child_node)
                self.__remove_case1(removing_node)
            self.__replace_node(removing_node, child_node)

            if removing_node.parent is None and child_node is not None:
                child_node.color = Color.BLACK
        self._length -= 1

    # Приватный метод __remove_case1 выполняет первое правило удаления в красно-черном дереве.
    def __remove_case1(self, node: Node[T]) -> None:
        if node.parent is None:
            return
        self.__remove_case2(node)

    # Приватный метод __remove_case2 выполняет второе правило удаления в красно-черном дереве.
    def __remove_case2(self, node: Node[T]) -> None:
        brother = node.brother()
        if _get_color(brother) == Color.RED:
            node.parent.color = Color.RED
            brother.color = Color.BLACK
            if node == node.parent.left:
                self.__rotate_left(node.parent)
            else:
                self.__rotate_right(node.parent)
        self.__remove_case3(node)

    # Приватный метод __remove_case3 выполняет третье правило удаления в красно-черном дереве.
    def __remove_case3(self, node: Node[T]) -> None:
        brother = node.brother()
        if (_get_color(node.parent) == Color.BLACK and
                _get_color(brother) == Color.BLACK and
                _get_color(brother.left) == Color.BLACK and
                _get_color(brother.right) == Color.BLACK):
            brother.color = Color.RED
            self.__remove_case1(node.parent)
        else:
            self.__remove_case4(node)

    # Приватный метод __remove_case4 выполняет четвертое правило удаления в красно-черном дереве.
    def __remove_case4(self, node: Node[T]) -> None:
        brother = node.brother()
        if (_get_color(node.parent) == Color.RED and
                _get_color(brother) == Color.BLACK and
                _get_color(brother.left) == Color.BLACK and
                _get_color(brother.right) == Color.BLACK):
            brother.color = Color.RED
            node.parent.color = Color.BLACK
        else:
            self.__remove_case5(node)