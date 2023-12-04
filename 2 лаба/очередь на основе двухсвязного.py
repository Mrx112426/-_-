from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Generic, Optional, Callable
from random import choice
import pickle
import timeit
class IKey(ABC):

    @abstractmethod
    def key(self) -> int:
        ...


T = TypeVar("T", bound=IKey)


class Color(Enum):
    RED = 0
    BLACK = 1


@dataclass
class Node(Generic[T]):
    data: T
    parent: Optional['Node[T]'] = None
    left: Optional['Node[T]'] = None
    right: Optional['Node[T]'] = None
    color: Color = Color.RED

    def key(self) -> int:
        return self.data.key()

    def grandfather(self) -> Optional['Node[T]']:
        if self.parent is not None:
            return self.parent.parent
        return None

    def uncle(self) -> Optional['Node[T]']:
        if self.parent is None or self.parent.parent is None:
            return None
        return self.parent.brother()

    def brother(self) -> Optional['Node[T]']:
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left


def _get_color(node: Optional['Node[T]']) -> Color:
    if node is None:
        return Color.BLACK
    return node.color


class KeyNotFoundException(Exception):
    pass


class EmptyTreeException(Exception):
    pass


class EmptyNodeException(Exception):
    pass


@dataclass
class Car(IKey):
    brand: str
    vin: str
    engine_volume: float
    price: float
    average_speed: float

    def key(self) -> float:
        return self.price


class RBTree(Generic[T]):

    def __init__(self) -> None:
        self._length: int = 0
        self._root: Optional[Node[T]] = None

    def is_empty(self) -> bool:
        return self._length == 0

    def get_size(self) -> int:
        return self._length

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

    def __rotate_left(self, node: Node[T]) -> None:
        right = node.right
        self.__replace_node(node, right)
        node.right = right.left
        if right.left is not None:
            right.left.parent = node
        right.left = node
        node.parent = right

    def __rotate_right(self, node: Node[T]) -> None:
        left = node.left
        self.__replace_node(node, left)
        node.left = left.right
        if left.right is not None:
            left.right.parent = node
        left.right = node
        node.parent = left

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

    def __insert_case1(self, node: Node[T]) -> None:
        if node.parent is None:
            node.color = Color.BLACK
        else:
            self.__insert_case2(node)

    def __insert_case2(self, node: Node[T]) -> None:
        if _get_color(node.parent) == Color.BLACK:
            return
        self.__insert_case3(node)

    def __insert_case3(self, node: Node[T]) -> None:
        uncle = node.uncle()
        if _get_color(uncle) == Color.RED:
            node.parent.color = Color.BLACK
            uncle.color = Color.BLACK
            node.grandfather().color = Color.RED
            self.__insert_case1(node.grandfather())
        else:
            self.__insert_case4(node)

    def __insert_case4(self, node: Node[T]) -> None:
        grandfather = node.grandfather()
        if (node == node.parent.right and
                node.parent == grandfather.left):
            self.__rotate_left(node.parent)
            node = node.left
        elif (node == node.parent.left and
              node.parent == grandfather.right):
            self.__rotate_right(node.parent)
            node = node.right
        self.__insert_case5(node)

    def __insert_case5(self, node: Node[T]) -> None:
        node.parent.color = Color.BLACK
        grandfather = node.grandfather()
        grandfather.color = Color.RED
        if (node == node.parent.left and
                node.parent == grandfather.left):
            self.__rotate_right(grandfather)
        elif (node == node.parent.right and
              node.parent == grandfather.right):
            self.__rotate_left(grandfather)

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

    def __find_left_maximum_node(self, node: Node[T]) -> tuple[Optional[Node[T]], bool]:
        current_node = node.left
        if current_node is None:
            return None, False
        while current_node.right is not None:
            current_node = current_node.right
        return current_node, True

    def remove(self, key: int) -> None:
        if self.is_empty():
            raise EmptyTreeException("EmptyTreeException")

        child_node: Optional[Node[T]] = None
        removing_node, ok = self.__find_node(key)
        if not ok:
            raise KeyNotFoundException("KeyNotFoundException")

        if removing_node.left is not None and removing_node.right is not None:
            successor, ok = self.__find_left_maximum_node(removing_node)
            if not ok:
                raise EmptyNodeException("EmptyNodeException")

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

    def __remove_case1(self, node: Node[T]) -> None:
        if node.parent is None:
            return
        self.__remove_case2(node)

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

    def __remove_case5(self, node: Node[T]) -> None:
        brother = node.brother()
        if (node == node.parent.left and
                _get_color(brother) == Color.BLACK and
                _get_color(brother.left) == Color.RED and
                _get_color(brother.right) == Color.BLACK):
            brother.color = Color.RED
            brother.left.color = Color.BLACK
            self.__rotate_right(brother)
        elif (node == node.parent.right and
                _get_color(brother) == Color.BLACK and
                _get_color(brother.left) == Color.BLACK and
                _get_color(brother.right) == Color.RED):
            brother.color = Color.RED
            brother.right.color = Color.BLACK
            self.__rotate_left(brother)
        self.__remove_case6(node)

    def __remove_case6(self, node: Node[T]) -> None:
        brother = node.brother()
        brother.color = _get_color(node.parent)
        node.parent.color = Color.BLACK
        if (node == node.parent.left and
                _get_color(brother.right) == Color.RED):
            brother.right.color = Color.BLACK
            self.__rotate_left(node.parent)
        elif _get_color(brother.left) == Color.RED:
            brother.left.color = Color.BLACK
            self.__rotate_right(node.parent)

    # Он выполняет поиск, начиная с корня дерева и двигаясь вниз по дереву в соответствии с ключом.
    def find(self, key: int) -> tuple[Optional[T], bool]:
        if self.is_empty():
            raise EmptyTreeException("EmptyTreeException")

        current_node = self._root
        while current_node.key() != key:
            if key < current_node.key():
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node is None:
                return None, False
        return current_node.data, True

    # ------------ симетричный обход дерева ------------
    def symmetric_traversal(self, func: Callable[[T], None]) -> None:
        if self.is_empty():
            raise EmptyTreeException("EmptyTreeException")
        self.__symmetric_traversal(self._root, func)

    def __symmetric_traversal(self, local_root: Optional[Node[T]],
                              func: Callable[[T], None]) -> None:
        if local_root is not None:
            self.__symmetric_traversal(local_root.left, func)
            func(local_root.data)
            self.__symmetric_traversal(local_root.right, func)

    # ------------ Неупорядоченный обход ------------
    def traversal_after_processing(self, func: Callable[[T], None]) -> None:
        if self.is_empty():
            raise EmptyTreeException("EmptyTreeException")
        self.__traversal_after_processing(self._root, func)

    def __traversal_after_processing(self, local_root: Optional[Node[T]],
                                     func: Callable[[T], None]) -> None:
        if local_root is not None:
            func(local_root.data)
            self.__symmetric_traversal(local_root.left, func)
            self.__symmetric_traversal(local_root.right, func)

    def traversal_before_processing(self, func: Callable[[T], None]) -> None:
        if self.is_empty():
            raise EmptyTreeException("EmptyTreeException")
        self.__traversal_before_processing(self._root, func)

    def __traversal_before_processing(self, local_root: Optional[Node[T]],
                                      func: Callable[[T], None]) -> None:
        if local_root is not None:
            self.__symmetric_traversal(local_root.left, func)
            self.__symmetric_traversal(local_root.right, func)
            func(local_root.data)

    # -------------------------------------------------

    def minimum(self) -> T:
        if self.is_empty():
            raise EmptyTreeException("EmptyTreeException")
        current_node = self._root
        last_node: Optional[Node[T]] = None
        while current_node is not None:
            last_node = current_node
            current_node = current_node.left
        return last_node.data

    def maximum(self) -> T:
        if self.is_empty():
            raise EmptyTreeException("EmptyTreeException")
        current_node = self._root
        last_node: Optional[Node[T]] = None
        while current_node is not None:
            last_node = current_node
            current_node = current_node.right
        return last_node.data

    def print_tree(self) -> None:
        result: list[str] = ["RBTree\n"]
        if not self.is_empty():
            self.__create_str_tree(result, "", self._root, True)
        print("".join(result))

    def __create_str_tree(self, result: list[str], prefix: str,
                          node: Optional[Node[T]], is_tail: bool):
        if node.right is not None:
            new_prefix = prefix
            if is_tail:
                new_prefix += "│   "
            else:
                new_prefix += "    "
            self.__create_str_tree(result, new_prefix, node.right, False)

        result.append(prefix)
        if is_tail:
            result.append("└── ")
        else:
            result.append("┌── ")
        result.append(str(node.key()) + "\n")

        if node.left is not None:
            new_prefix = prefix
            if is_tail:
                new_prefix += "    "
            else:
                new_prefix += "│   "
            self.__create_str_tree(result, new_prefix, node.left, True)





if __name__ == '__main__':
    cars: list[Car] = [
        Car("Toyota", "VIN1", 2.0, 0.3, 120),
        Car("Ford", "VIN2", 2.5, 1, 130),
        Car("Nissan", "VIN1", 2.5, 2, 120),
        Car("Porsche", "VIN2", 2.0, 10, 130),
        Car("Audi", "VIN3", 2.4, 4, 125),
        Car("Hyundai", "VIN1", 2.5, 2, 120),
        Car("Ford", "VIN2", 2.0, 0.7, 130),
        Car("Volkswagen", "VIN3", 2.4, 0.5, 125),
        Car("Honda", "VIN1", 2.5, 1, 120),
        Car("Mercedes-Benz", "VIN2", 2.0, 8, 130),
        Car("Toyota", "VIN3", 2.4, 3, 125),
        Car("Ferrari", "VIN3", 2.4, 12, 125)
        # Другие экземпляры класса Car
    ]

    car_tree: RBTree[Car] = RBTree[Car]()
    for car in cars:
        car_tree.insert(car)
        print(f"Добавлен элемент: {car}")
    print("\n Дерево после добавления элемента")
    car_tree.print_tree()

    print("----- Поиск элемента по стоимости------")
    key_to_find = 30000  # Это стоимость автомобиля, который вы ищете
    found_car, found = car_tree.find(key_to_find)

    if found:
        print(f"Автомобиль с ценой {key_to_find} найдет: {found_car}")
    else:
        print(f"Автомобиль с ценой {key_to_find} не найден.")

    print("\n Удаление элемета по стоимости")
    car_tree.remove(0.7)
    print("Дерево после удаления элемента со стоимостью: 0.7")
    car_tree.print_tree()
    # Сохранить состояние дерева в файл
    with open("car_tree.pkl", "wb") as file:
        pickle.dump(car_tree, file)

    # Загрузить данные из файла
    with open("car_tree.pkl", "rb") as file:
        loaded_tree = pickle.load(file)

    # Теперь `loaded_tree` содержит загруженное дерево

    # Предполагая, что у вас уже есть заполненное красно-черное дерево (tree)
    print("\nБенчмарки")
    # Бенчмарки
    def insert_benchmark():
        for car in cars:
            car_tree.insert(car)


    insert_time = timeit.timeit(insert_benchmark, number=100000)
    print(f"Время вставки для 100000 элементов : {insert_time:.6f} секунд")



    def search_benchmark():
        for car in cars:
            car_tree.find(car.key())


    search_time = timeit.timeit(search_benchmark, number=100000)
    print(f"Время поиска для 100000 элементов: {search_time:.6f} seconds")