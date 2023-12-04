from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable
import random
import timeit
from typing import List
T = TypeVar("T")

class IndexOutRangeException(Exception):
    pass

@dataclass
class Car:
    brand: str # Марка
    vin: str # Объем двигателя
    engine_volume: float #Объем двигателя
    price: float # Цена
    average_speed: float # Средняя скорость

    def __str__(self) -> str:
        return f"Car({self.brand}, {self.vin}, {self.engine_volume}, {self.price}, {self.average_speed})"


@dataclass
class DoubleNode(Generic[T]):#Определяет узел двухсвязного списка
    data: T
    next_ptr: Optional['DoubleNode[T]'] = None
    prev_ptr: Optional['DoubleNode[T]'] = None

class DoublyList(Generic[T]):#Двухсвязный список

    def __init__(self):
        self._length: int = 0
        self._head: Optional['DoubleNode[T]'] = None
        self._tail: Optional['DoubleNode[T]'] = None

    def get_size(self) -> int:
        return self._length

    def __iter__(self):# Итератор, для того чтобы перебирать элементы списка
        current_node = self._head
        while current_node is not None:
            yield current_node.data
            current_node = current_node.next_ptr
    def check_range(self, index: int) -> bool:# Проверка на допустимое значение индекса
        if index >= self._length or index < 0:
            return False
        return True

    def is_empty(self) -> bool:#Проверку на пустоту
        return self._length == 0

    def push_tail(self, data: T) -> None:#Вставка в конец списка
        node = DoubleNode[T](data)
        if self._length <= 0:
            self._head = node
            self._tail = node
            self._length += 1
            return

        self._tail.next_ptr = node
        node.prev_ptr = self._tail
        self._tail = node
        self._length += 1

    def push_head(self, data: T) -> None:#Вставка в начало списка
        node = DoubleNode[T](data)
        if self._length <= 0:
            self._head = node
            self._tail = node
            self._length += 1
            return

        node.next_ptr = self._head
        self._head.prev_ptr = node
        self._head = node
        self._length += 1

    def insert(self, index: int, data: T) -> None:#Вставка в заданную позицию
        ok: bool = self.check_range(index)
        if not ok:
            raise IndexOutRangeException("Выход за границы индексов.")

        if index == 0:
            self.push_head(data)
            return
        elif index == self._length - 1:
            self.push_tail(data)
            return

        node = self._head
        for i in range(0, index):
            node = node.next_ptr

        insert_node = DoubleNode[T](data)
        insert_node.next_ptr = node.next_ptr
        node.next_ptr.prev_ptr = insert_node
        insert_node.prev_ptr = node
        node.next_ptr = insert_node
        self._length += 1



    def __str__(self) -> str:
        my_str: str = ""
        node = self._head
        while node is not None:
            my_str += str(node.data) + " "
            node = node.next_ptr
        return f"Текущее состояние: [{my_str}]"

    def merge_sort(self, compare_func):
        # Проверка на случаи, когда список пуст или содержит только один элемент
        if self.is_empty() or self._length == 1:
            return

        def merge_sort_impl(arr):
            # Рекурсивная функция для сортировки слиянием
            if len(arr) <= 1:
                return arr

            middle = len(arr) // 2
            left = arr[:middle]
            right = arr[middle:]

            left = merge_sort_impl(left)  # Сортировка левой половины
            right = merge_sort_impl(right)  # Сортировка правой половины

            return merge(left, right)

        def merge(left, right):
            # Функция объединения двух отсортированных списков в один
            result = []
            i = j = 0

            while i < len(left) and j < len(right):
                if compare_func(left[i], right[j]):
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1

            result.extend(left[i:])
            result.extend(right[j:])
            return result

        # Создаем список `arr`, содержащий элементы из двусвязного списка
        arr = [car for car in self]
        sorted_arr = merge_sort_impl(arr)  # Сортировка списка слиянием

        current_node = self._head
        for sorted_car in sorted_arr:
            current_node.data = sorted_car
            current_node = current_node.next_ptr


    def heap_sort(self, compare_func):
        # Проверка на случаи, когда список пуст или содержит только один элемент
        if self.is_empty() or self._length == 1:
            return

        def heapify(arr, n, i):
            # Преобразование массива в кучу
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and compare_func(arr[left], arr[largest]):
                largest = left

            if right < n and compare_func(arr[right], arr[largest]):
                largest = right

            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        def heap_sort_impl(arr):
            # Сортировка массива с использованием сортировки кучей
            n = len(arr)

            for i in range(n // 2 - 1, -1, -1):
                heapify(arr, n, i)

            for i in range(n - 1, 0, -1):
                arr[i], arr[0] = arr[0], arr[i]
                heapify(arr, i, 0)

        # Создаем список `arr`, содержащий элементы из двусвязного списка
        arr = [car for car in self]
        heap_sort_impl(arr)  # Сортировка списка кучей

        current_node = self._head
        for sorted_car in arr:
            current_node.data = sorted_car
            current_node = current_node.next_ptr
def generate_random_cars(num_cars):
    cars = DoublyList[Car]()
    for _ in range(num_cars):
        brand = f"Brand-{random.randint(1, 100)}"
        vin = f"VIN-{random.randint(1000, 9999)}"
        engine_volume = random.uniform(1.0, 4.0)
        price = random.uniform(15000, 50000)
        average_speed = random.uniform(80, 180)
        car = Car(brand, vin, engine_volume, price, average_speed)
        cars.push_tail(car)
    return cars

def benchmark_merge_dataset():
    num_cars = 1000  # Измените на количество элементов, которые вы хотите использовать
    cars = generate_random_cars(num_cars)

    def merge_sort_large_dataset():
        cars.merge_sort(lambda car1, car2: car1.price < car2.price)

    time = timeit.timeit(merge_sort_large_dataset, number=100)
    print(f"Время выполнения сортировки слиянием на {num_cars} элементах: {time} секунд")

def benchmark_heap():
    num_cars = 1000  # Измените на количество элементов, которые вы хотите использовать
    cars = generate_random_cars(num_cars)

    def heap_dataset():
        cars.heap_sort(lambda car1, car2: car1.price < car2.price)

    time = timeit.timeit(heap_dataset, number=100)
    print(f"Время выполнения сортировки кучи на {num_cars} элементах: {time} секунд")


def print_cars(cars: List[Car]) -> None:
    """
    Функция для вывода книг в удобочитаемом формате.
    """
    for car in cars:
        print(f" Марка: {car.brand}, VIN: {car.vin}, Объем двигателя: {car.engine_volume}, Цена: {car.price} Млн.$, Средняя скорость: {car.average_speed}")

if __name__ == "__main__":
    cars = DoublyList[Car]()
    cars.push_tail(Car("Nissan", "VIN1", 2.5, 2, 120))
    cars.push_tail(Car("Porsche", "VIN2", 2.0, 10, 130))
    cars.push_tail(Car("Audi", "VIN3", 2.4, 4, 125))
    cars.push_tail(Car("Hyundai", "VIN1", 2.5, 2, 120))
    cars.push_tail(Car("Ford", "VIN2", 2.0, 0.7, 130))
    cars.push_tail(Car("Volkswagen", "VIN3", 2.4, 0.5, 125))
    cars.push_tail(Car("Honda", "VIN1", 2.5, 1, 120))
    cars.push_tail(Car("Mercedes-Benz", "VIN2", 2.0, 8, 130))
    cars.push_tail(Car("Toyota", "VIN3", 2.4, 3, 125))
    cars.push_tail(Car("Ferrari", "VIN3", 2.4, 12, 125))

    print("\nСписок до сортировки")
    print_cars(cars)

    print("\nСортировка cлиянием по возрастанию цены  ")
    cars.merge_sort(lambda car1, car2: car1.price < car2.price)
    print_cars(cars)

    print("\nСортировка кучей по убыванию объема двигателя  ")
    cars.heap_sort(lambda car1, car2: car1.engine_volume < car2.engine_volume)
    print_cars(cars)

    print("\nБЕНЧМАРКИ")
    benchmark_merge_dataset()
    benchmark_heap()
