import timeit
import random
from typing import List
from dataclasses import dataclass
from typing import Optional, Callable

@dataclass
class Student:
    full_name: str
    group_number: str
    course: int
    age: int
    average_grade: float

class DoubleNode:
    def __init__(self, student: Student):
        self.student = student
        self.prev: Optional['DoubleNode'] = None
        self.next: Optional['DoubleNode'] = None

class DoublyLinkedList:
    def __init__(self):
        self.head: Optional[DoubleNode] = None
        self.tail: Optional[DoubleNode] = None
        self.length = 0

    def is_empty(self) -> bool:
        return self.length == 0

    def push(self, student: Student):
        new_node = DoubleNode(student)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def display(self):
        current = self.head
        while current:
            print(f"ФИО: {current.student.full_name}, Группа: {current.student.group_number}, Курс: {current.student.course}, Возраст: {current.student.age}, Средняя оценка: {current.student.average_grade}")
            current = current.next

    def sort_heap(self):
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and arr[left].average_grade > arr[largest].average_grade:
                largest = left

            if right < n and arr[right].average_grade > arr[largest].average_grade:
                largest = right

            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        students = [node.student for node in self]
        n = len(students)

        for i in range(n // 2 - 1, -1, -1):
            heapify(students, n, i)

        for i in range(n - 1, 0, -1):
            students[i], students[0] = students[0], students[i]
            heapify(students, i, 0)

        current = self.head
        for student in students:
            current.student = student
            current = current.next

    def comb_sort(self, compare_func: Optional[Callable[[Student, Student], bool]] = None):
        if self.is_empty() or self.length == 1:
            return

        def get_gap(gap):
            gap = (gap * 10) // 13
            if gap < 1:
                return 1
            return gap

        gap = self.length
        swapped = True

        while gap != 1 or swapped:
            gap = get_gap(gap)
            swapped = False
            current = self.head

            for i in range(self.length - gap):
                next_node = current.next
                if compare_func(current.student, next_node.student):
                    current.student, next_node.student = next_node.student, current.student
                    swapped = True
                current = current.next

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next
def generate_random_students(num_students):
    students = DoublyLinkedList()
    for _ in range(num_students):
        full_name = f"Student-{random.randint(1, 100)}"
        group_number = f"Group-{random.randint(100, 999)}"
        course = random.randint(1, 5)
        age = random.randint(18, 30)
        average_grade = round(random.uniform(3.0, 5.0), 1)
        student = Student(full_name, group_number, course, age, average_grade)
        students.push(student)
    return students

def benchmark_heap_sort():
    num_students = 10000  # Измените на количество элементов, которые вы хотите использовать
    students = generate_random_students(num_students)

    def heap_sort_large_dataset():
        students.comb_sort(lambda student1, student2: student1.average_grade < student2.average_grade)

    time = timeit.timeit(heap_sort_large_dataset, number=100)
    print(f"Время выполнения сортировки кучей на {num_students} элементах: {time} секунд")

def benchmark_comb_sort():
    num_students = 10000  # Измените на количество элементов, которые вы хотите использовать
    students = generate_random_students(num_students)

    def comb_sort_large_dataset():
        students.comb_sort(lambda student1, student2: student1.full_name < student2.full_name)

    time = timeit.timeit(comb_sort_large_dataset, number=100)
    print(f"Время выполнения сортировки расческой на {num_students} элементах: {time} секунд")


if __name__ == '__main__':
    students_list = DoublyLinkedList()
    students_list.push(Student("Иванов Иван Иванович", "Группа 101", 2, 20, 4.5))
    students_list.push(Student("Петров Петр Петрович", "Группа 102", 3, 21, 4.2))
    students_list.push(Student("Сидоров Андрей Игоревич", "Группа 103", 1, 19, 4.7))
    students_list.push(Student("Суворов Максим Максимович", 4224, 4, 21, 3.2))
    students_list.push(Student("Евсеев Эрик Артёмович", 4324, 2, 21, 3.4))
    students_list.push(Student("Морозов Александр Егорович", 4324, 3, 20, 3.3))
    students_list.push(Student("Муравьев Фёдор Степанович", 4224, 1, 21, 3.7))
    students_list.push(Student("Медведева Виктория Александровна", 4324, 2, 21, 3.8))
    students_list.push(Student("Поляков Владимир Михайлович", 4324, 1, 20, 4.3))
    students_list.push(Student("Ковалев Константин Артёмович ", 4224, 4, 21, 5.6))

    # Добавьте еще студентов по аналогии

    print("Двусвязный список до сортировки:")
    students_list.display()

    students_list.sort_heap()  # Сортировка кучей по средней оценке
    print("\nДвусвязный список после сортировки кучей по возрастанию средней оценке:")
    students_list.display()

    students_list.comb_sort(lambda student1, student2: student1.full_name > student2.full_name)  # Сортировка расческой по ФИО
    print("\nДвусвязный список после сортировки расческой убыванию по ФИО (по убыванию):")
    students_list.display()

    print("\nБЕНЧМАРКИ")
    benchmark_heap_sort()
    benchmark_comb_sort()