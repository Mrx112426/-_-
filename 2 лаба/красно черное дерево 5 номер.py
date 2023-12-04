import timeit
import pickle

from dataclasses import dataclass
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class QueueOverFlowException(Exception):
    pass

class EmptyQueueException(Exception):
    pass

@dataclass
class Student:
    name: str
    group: int
    course: int
    age: int
    average_grade: float

    def __str__(self) -> str:
        return f"Student({self.name}, {self.group}, {self.course}, {self.age}, {self.average_grade})"

@dataclass
class DoublyNode(Generic[T]):
    data: T
    next_ptr: Optional['DoublyNode[T]'] = None
    prev_ptr: Optional['DoublyNode[T]'] = None

class PriorityQueue(Generic[T]):

    def __init__(self) -> None:
        self._length: int = 0
        self._head: Optional[DoublyNode[T]] = None
        self._tail: Optional[DoublyNode[T]] = None

    def get_size(self) -> int:
        return self._length

    def is_empty(self) -> bool:
        return self._length == 0

    def push(self, data: T) -> None:
        """
        Метод для вставки элемента с приоритетом в очередь.
        :param data: Элемент, который требуется вставить.
        """
        node = DoublyNode[T](data)
        if self.is_empty():
            # Если очередь пуста, устанавливаем новый элемент как первый и последний
            self._head = node
            self._tail = node
        elif data.average_grade >= self._head.data.average_grade:
            # Если новый элемент имеет более высокий приоритет, чем текущий первый элемент,
            # он становится новым первым элементом
            node.next_ptr = self._head
            self._head.prev_ptr = node
            self._head = node
        else:
            # Вставка нового элемента в соответствии с его приоритетом
            current = self._head
            while current.next_ptr is not None and current.next_ptr.data.average_grade > data.average_grade:
                current = current.next_ptr
            node.next_ptr = current.next_ptr
            node.prev_ptr = current
            if current.next_ptr is not None:
                current.next_ptr.prev_ptr = node
            current.next_ptr = node
        self._length += 1

    def pop(self) -> T:
        """
        Метод для извлечения элемента с наивысшим приоритетом из очереди.
        :return: Элемент с наивысшим приоритетом.
        """
        if self.is_empty():
            raise EmptyQueueException("Queue is empty")
        data = self._head.data
        self._head = self._head.next_ptr
        if self._head is not None:
            self._head.prev_ptr = None
        self._length -= 1
        return data

    def peek(self) -> T:
        """
        Метод для просмотра элемента с наивысшим приоритетом в очереди без его удаления.
        :return: Элемент с наивысшим приоритетом.
        """
        if self.is_empty():
            raise EmptyQueueException("Queue is empty")
        return self._head.data

    def print_queue(self) -> None:
        """
        Метод для вывода содержимого очереди на экран.
        """
        current = self._head
        while current is not None:
            print(current.data)
            current = current.next_ptr

    def save_to_file(self, file_path: str) -> None:
        """
        Метод для сохранения структуры данных очереди в файл
        file_path: Путь к файлу, в который будет сохранена очередь.
        """
        with open(file_path, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_file(cls, file_path: str) -> 'PriorityQueue':
        """
        Метод для загрузки структуры данных очереди из файла
        file_path: Путь к файлу, из которого будет загружена очередь.
        """
        with open(file_path, 'rb') as file:
            return pickle.load(file)

if __name__ == '__main__':
    def print_student(data: Student):
        print(data)

    def benchmark_push():
        priority_queue = PriorityQueue[Student]()

        def push_operation():
            for _ in range(1000):
                student = Student("Benchmark Student", 4217, 2, 20, 90.0)
                priority_queue.push(student)

        # Измеряем время выполнения операции вставки 100 раз
        execution_time = timeit.timeit(push_operation, number=1000)
        print(f"Операция вставки заняла {execution_time:.6f} секунд для 1000 итераций")

    def benchmark_pop():
        priority_queue = PriorityQueue[Student]()

        def pop_operation():
            for _ in range(1000):
                priority_queue.push(Student("Benchmark Student", 4217, 2, 20, 90.0))
                priority_queue.pop()

        # Измеряем время выполнения операции удаления 100 раз
        execution_time = timeit.timeit(pop_operation, number=1000)
        print(f"Операция удаления заняла {execution_time:.6f} секунд для 1000 итераций")

    priority_queue = PriorityQueue[Student]()  # Создаем очередь с приоритетом

    # Добавляем студентов в приоритетную очередь
    priority_queue.push(Student("John", 4217, 2, 20, 85.5))
    priority_queue.push(Student("Alice", 4217, 1, 19, 90.0))
    priority_queue.push(Student("Bob", 4217, 3, 21, 78.0))
    priority_queue.push(Student("Eve", 4217, 2, 22, 95.5))
    priority_queue.push(Student("John", 4217, 2, 20, 73.5))
    priority_queue.push(Student("Alice", 4217, 1, 19, 22.0))
    priority_queue.push(Student("Bob", 4217, 3, 21, 99.0))
    priority_queue.push(Student("Eve", 4217, 2, 22, 34.5))
    priority_queue.push(Student("John", 4217, 2, 20, 21.5))
    priority_queue.push(Student("Alice", 4217, 1, 19, 32.0))
    priority_queue.push(Student("Bob", 4217, 3, 21, 78.0))
    priority_queue.push(Student("Eve", 4217, 2, 22, 90.5))

    print("\nОчередь с приоритетом:")
    priority_queue.print_queue()

    print("\nЭлемент с наибольшим приоритетом:")
    print_student(priority_queue.peek())

    print("\nУдаление из очереди:")
    student = priority_queue.pop()
    print(f"Студент, который будет удален: {student}")

    # Сохранение структуры данных в файл
    priority_queue.save_to_file('priority_queue_data.pkl')

    print("\nБенчмарк вставки:")
    benchmark_push()

    print("\nБенчмарк удаления:")
    benchmark_pop()
