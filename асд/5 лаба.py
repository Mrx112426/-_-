from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, List
import timeit
import random
T = TypeVar("T")

@dataclass
class Car:
    brand: str
    vin: str
    engine_volume: float
    price: float
    average_speed: float

@dataclass
class DoubleNode(Generic[T]):
    data: T
    next_ptr: Optional['DoubleNode[T]'] = None
    prev_ptr: Optional['DoubleNode[T]'] = None

class DoublyList(Generic[T]):
    def __init__(self):
        self._length: int = 0
        self._head: Optional['DoubleNode[T]'] = None
        self._tail: Optional['DoubleNode[T]'] = None

    def get_size(self) -> int:
        return self._length

    def __iter__(self):
        current_node = self._head
        while current_node is not None:
            yield current_node.data
            current_node = current_node.next_ptr

    def is_empty(self) -> bool:
        return self._length == 0

    def push_tail(self, data: T) -> None:
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

    def push_head(self, data: T) -> None:
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

    def merge_sort(self, compare_func):
        if self.is_empty() or self._length == 1:
            return

        def merge_sort_impl(arr):
            if len(arr) <= 1:
                return arr

            middle = len(arr) // 2
            left = arr[:middle]
            right = arr[middle:]

            left = merge_sort_impl(left)
            right = merge_sort_impl(right)

            return merge(left, right)

        def merge(left, right):
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

        arr = [car for car in self]
        sorted_arr = merge_sort_impl(arr)

        current_node = self._head
        for sorted_car in sorted_arr:
            current_node.data = sorted_car
            current_node = current_node.next_ptr

    def quick_select(self, k: int) -> Car:
        if self.get_size() < k:
            raise ValueError("Индекс k выходит за пределы размера списка")

        car_list = [car for car in self]

        def partition(arr, low, high):
            pivot = arr[high].price
            i = low - 1
            for j in range(low, high):
                if arr[j].price <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        def kth_smallest(arr, low, high, k):
            if low < high:
                pivot_index = partition(arr, low, high)
                if k < pivot_index:
                    return kth_smallest(arr, low, pivot_index - 1, k)
                elif k > pivot_index:
                    return kth_smallest(arr, pivot_index + 1, high, k)
                else:
                    return arr[pivot_index]
            else:
                return arr[low]

        result_car = kth_smallest(car_list, 0, len(car_list) - 1, k - 1)
        return result_car

    def search_by_price(self, target_price):
        current_node = self._head
        while current_node is not None:
            if current_node.data.price == target_price:
                return current_node.data
            current_node = current_node.next_ptr
        return None

    def display(self):
        for car in self:
            print(f"Марка: {car.brand}, VIN: {car.vin}, Объем двигателя: {car.engine_volume}, Стоимость: {car.price}, Средняя скорость: {car.average_speed}")

def benchmark_search_average(cars, target_price):
    num_iterations = 1000
    total_time = 0

    for _ in range(num_iterations):
        random_price = random.uniform(15000, 50000)
        start_time = timeit.default_timer()
        cars.search_by_price(random_price)
        end_time = timeit.default_timer()
        total_time += end_time - start_time

    average_time = total_time / num_iterations
    print(f"Среднее время поиска по стоимости ({num_iterations} итераций): {average_time:.10f} секунд")

def benchmark_search_best(cars, target_price):
    num_iterations = 1000
    total_time = 0

    for _ in range(num_iterations):
        start_time = timeit.default_timer()
        cars.search_by_price(target_price)
        end_time = timeit.default_timer()
        total_time += end_time - start_time

    average_time = total_time / num_iterations
    print(f"Лучшее время поиска по стоимости ({num_iterations} итераций): {average_time:.10f} секунд")

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
    cars.display()

    print("\nСортировка слиянием по возрастанию стоимости")
    cars.merge_sort(lambda car1, car2: car1.price < car2.price)
    cars.display()

    print("\nБыстрый выбор по стоимости (второй элемент)")
    result_car = cars.quick_select(2)

    print(f"Марка: {result_car.brand}, VIN: {result_car.vin}, Объем двигателя: {result_car.engine_volume}, Стоимость: {result_car.price}, Средняя скорость: {result_car.average_speed}")

    # Пример использования quick_select для поиска медианы (средней по стоимости)
    median_index = cars.get_size() // 2
    median = cars.quick_select(median_index)
    print(f"\nМедиана (средняя по стоимости):")
    print(f"Марка: {median.brand}, VIN: {median.vin}, Объем двигателя: {median.engine_volume}, Стоимость: {median.price}, Средняя скорость: {median.average_speed}")

    target_price = 4  # Укажите цену для поиска
    benchmark_search_average(cars, target_price)
    benchmark_search_best(cars, target_price)
