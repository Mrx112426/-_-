from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Callable
import json
import timeit

T = TypeVar("T")

class IndexOutRangeException(Exception):
    pass

@dataclass
class Student:
    full_name: str
    group_number: str
    course: int
    age: int
    average_grade: float

    def __str__(self) -> str:
        return f"Student({self.full_name}, {self.group_number}, {self.course}, {self.age}, {self.average_grade})"

@dataclass
class DoubleNode(Generic[T]):
    data: T
    next_ptr: Optional['DoubleNode[T]'] = None
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

        if index == self._lenght - 1:
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

class MaxHeap(Generic[T]):
    def __init__(self):
        self._length: int = 0
        self._head: Optional['DoubleNode[T]'] = None
        self._tail: Optional['DoubleNode[T]'] = None

    # Добавление нового элемента в макс-кучу на основе средней оценки
    def push(self, data: T) -> None:
        node = DoubleNode[T](data)
        if self._length <= 0:
            self._head = node
            self._tail = node
            self._length += 1
        else:
            self._tail.next_ptr = node
            node.prev_ptr = self._tail
            self._tail = node
            self._length += 1
            self._heapify_up(node)

    # Поддержание свойства макс-кучи после добавления нового элемента
    def _heapify_up(self, node: DoubleNode[T]) -> None:
        while node.prev_ptr is not None and node.data.average_grade > node.prev_ptr.data.average_grade:
            node.data, node.prev_ptr.data = node.prev_ptr.data, node.data
            node = node.prev_ptr

    # Получение элемента с максимальной средней оценкой (корень макс-кучи)
    def get_max(self) -> T:
        if self._length == 0:
            raise Exception("Макс-куча пуста")
        return self._head.data

    # Удаление и возврат элемента с максимальной средней оценкой
    def pop_max(self) -> T:
        if self._length == 0:
            raise Exception("Макс-куча пуста")
        max_element = self._head.data
        self._head.data = self._tail.data
        self._remove_tail()
        self._heapify_down(self._head)

    # Поддержание свойства макс-кучи после удаления элемента
    def _heapify_down(self, node: DoubleNode[T]) -> None:
        while node.next_ptr is not None:
            left_child = node.next_ptr
            right_child = node.next_ptr.next_ptr if node.next_ptr.next_ptr is not None else node.next_ptr

            max_child = left_child if left_child.data.average_grade > right_child.data.average_grade else right_child

            if max_child.data.average_grade > node.data.average_grade:
                node.data, max_child.data = max_child.data, node.data
                node = max_child
            else:
                break

    def print_heap(self):
        if self._length == 0:
            print("Макс-куча пуста")
            return

        node = self._head
        while node is not None:
            print_student(node.data)
            node = node.next_ptr

    def pop_max(self) -> T:
        if self._length == 0:
            raise Exception("Макс-куча пуста")

        max_element = self._head.data
        self._head.data = self._tail.data
        self._remove_tail()
        self._heapify_down(self._head)

        return max_element

    def _remove_tail(self):
        if self._length == 0:
            return

        if self._length == 1:
            self._head = None
            self._tail = None
            self._length = 0
            return

        self._tail.prev_ptr.next_ptr = None
        self._tail = self._tail.prev_ptr
        self._length -= 1

    def print_heap_by_grade(self) -> None:
        if self._length == 0:
            print("Макс-куча пуста")
            return

        n_blanks, items_per_row, column, j = (32, 1, 0, 0)
        dots = 32 * "."

        sorted_data = []

        node = self._head
        while node is not None:
            sorted_data.append(node.data)
            node = node.next_ptr

        sorted_data.sort(key=lambda student: student.average_grade, reverse=True)

        print(dots * 2)

        for student in sorted_data:
            if column == 0:
                for _ in range(n_blanks):
                    print(" ", end='')
            print(f"{student.average_grade} ", end='')
            j += 1
            if j >= self._length:
                break
            column += 1
            if column == items_per_row:
                n_blanks //= 2
                items_per_row *= 2
                column = 0
                print("")
            else:
                for _ in range(n_blanks * 2 - 2):
                    print(" ", end='')
        print("\n" + dots * 2)

    def remove_student_by_grade(self, target_grade: float) -> None:
        if self._length == 0:
            return

        node = self._head
        while node is not None:
            if node.data.average_grade == target_grade:
                if node == self._head:
                    self.pop_max()
                else:
                    # Обмениваем данные студента с максимальной средней оценкой и удаляем максимальный
                    node.data = self._tail.data
                    self._remove_tail()
                    self._heapify_down(node)
                return
            node = node.next_ptr

    def contains_student_by_grade(self, target_grade: float) -> bool:
        node = self._head
        while node is not None:
            if node.data.average_grade == target_grade:
                return True
            node = node.next_ptr
        return False

    def contains_student(self, student: Student) -> bool:
        node = self._head
        while node is not None:
            if node.data == student:
                return True
            node = node.next_ptr
        return False

# Сериализация (сохранение) данных в файл
    def save_to_file(self, filename: str) -> None:
        data_to_save = []

        node = self._head
        while node is not None:
            data_to_save.append({
                "full_name": node.data.full_name,
                "group_number": node.data.group_number,
                "course": node.data.course,
                "age": node.data.age,
                "average_grade": node.data.average_grade
            })
            node = node.next_ptr

        with open(filename, 'w') as file:
            json.dump(data_to_save, file)

    # Десериализация (загрузка) данных из файла
    def load_from_file(self, filename: str) -> None:
        with open(filename, 'r') as file:
            data_to_load = json.load(file)

        for student_data in data_to_load:
            student = Student(
                student_data["full_name"],
                student_data["group_number"],
                student_data["course"],
                student_data["age"],
                student_data["average_grade"]
            )
            self.push(student)
def benchmark_push(max_heap, student, num_elements):
    setup_code = f"""
from __main__ import MaxHeap, Student
max_heap = MaxHeap[Student]()
student = Student("{student.full_name}", "{student.group_number}", {student.course}, {student.age}, {student.average_grade})
    """

    push_operation = """
max_heap.push(student)
    """

    execution_time = timeit.timeit(stmt=push_operation, setup=setup_code, number=num_elements)
    return execution_time

def benchmark_change(max_heap, student, num_elements):
    setup_code = f"""
from __main__ import MaxHeap, Student
max_heap = MaxHeap[Student]()
student = Student("{student.full_name}", "{student.group_number}", {student.course}, {student.age}, {student.average_grade})
for _ in range({num_elements}):
    max_heap.push(student)
    """

    change_operation = """
max_heap.pop_max()  # Удаляем элемент с максимальной средней оценкой
max_heap.push(student)  # Добавляем элемент обратно
    """

    execution_time = timeit.timeit(stmt=change_operation, setup=setup_code, number=num_elements)
    return execution_time

# Пример использования макс-кучи с классом Student
if __name__ == "__main__":
    max_heap = MaxHeap[Student]()
    max_heap.push(Student("Иванов Иван", "Группа 101", 2, 20, 88))
    max_heap.push(Student("Петров Петр", "Группа 102", 3, 21, 45))
    max_heap.push(Student("Сидоров Сидор", "Группа 103", 1, 19, 33))
    max_heap.push(Student("Dima", "4217", 2, 18, 5))
    max_heap.push(Student("Alexander", "4217", 3, 19, 12))
    max_heap.push(Student("Sherzod", "4217", 2, 19, 47))
    max_heap.push(Student("Nikita", "4217", 2, 19, 91))
    max_heap.push(Student("Lizza", "4217", 2, 19, 65))
    max_heap.push(Student("Nefor", "4217", 2, 19, 10))
    max_heap.push(Student("Nastya", "4217", 2, 19, 86))
    max_heap.push(Student("Nastasha", "4217", 2, 19, 76))
    max_heap.push(Student("Vladislav", "4217", 2, 18, 44))
    max_heap.push(Student("Umar", "4217", 2, 19, 97))
    max_heap.print_heap_by_grade()

    max_heap.remove_student_by_grade(97)
    print("Макс куча после удаления студента с баллом 97")
    max_heap.print_heap_by_grade()

    print("\nПроверка содержимого")
    student_to_check = Student("Umar", "4217", 2, 19, 97)
    grade_to_check = 91
    print(f"Студент {student_to_check.full_name} в макс-куче: {max_heap.contains_student(student_to_check)}")
    print(f"Оценка {grade_to_check} в макс-куче: {max_heap.contains_student_by_grade(grade_to_check)}")

    print("\nБенчмарки")

    """
    # Сохранение данных в файл
    max_heap.save_to_file("max_heap_data.json")

    # Очистка макс-кучи
    max_heap = MaxHeap[Student]()

    # Загрузка данных из файла
    max_heap.load_from_file("max_heap_data.json")

    # Вывод данных после загрузки
    max_heap.print_heap_by_grade()
    """
    student = Student("Иванов Иван", "Группа 101", 2, 20, 88)
    num_elements = 10000

    push_time = benchmark_push(MaxHeap, student, num_elements)
    print(f"Время операции push для {num_elements} элементов: {push_time:.6f} секунд")

    change_time = benchmark_change(MaxHeap, student, num_elements)
    print(f"Время операции change (удаление и добавление) для {num_elements} элементов: {change_time:.6f} секунд")



