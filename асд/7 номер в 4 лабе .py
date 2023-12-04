import timeit
import random
from typing import List
from dataclasses import dataclass
from collections.abc import Callable

@dataclass
class Student:
    full_name: str
    group_number: int
    course: int
    age: int
    average_grade: float

def heapify(arr, n, i):
    """
    Функция для преобразования списка в max-кучу.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left].course < arr[largest].course:
        largest = left

    if right < n and arr[right].course < arr[largest].course:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort_books(students: List[Student]) -> None:
    """
    Функция сортировки кучей для студентов по полю "курс" в порядке убывания.
    """
    n = len(students)

    for i in range(n // 2 - 1, -1, -1):
        heapify(students, n, i)

    for i in range(n - 1, 0, -1):
        students[i], students[0] = students[0], students[i]
        heapify(students, i, 0)

def cocktail_sort(arr: List[Student], comp: Callable[[Student, Student], bool]) -> None:
    if len(arr) == 0:
        raise ValueError("Массив пуст")

    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]

    left = 0
    right = len(arr) - 1

    while left <= right:
        for i in range(right, left, -1):
            if comp(arr[i - 1], arr[i]):
                swap(i - 1, i)
        left += 1
        for i in range(left, right):
            if comp(arr[i], arr[i + 1]):
                swap(i, i + 1)
        right -= 1
def print_students(students: List[Student]) -> None:
    """
    Функция для вывода студентов в удобочитаемом формате.
    """
    for student in students:
        print(f"Полное имя: {student.full_name} Номер группы: {student.group_number} Курс: {student.course} Возраст: {student.age} Средняя оценка: {student.average_grade}")

if __name__ == '__main__':

    students = [
        Student("Суворов Максим Максимович", 4224, 4, 21, 3.2),
        Student("Евсеев Эрик Артёмович", 4324, 2, 21, 3.4),
        Student("Морозов Александр Егорович", 4324, 3, 20, 3.3),
        Student("Муравьев Фёдор Степанович", 4224, 1, 21, 3.7),
        Student("Медведева Виктория Александровна", 4324, 2, 21, 3.8),
        Student("Поляков Владимир Михайлович", 4324, 1, 20, 4.3),
        Student("Ковалев Константин Артёмович ", 4224, 4, 21, 5.6),
        Student("Иванова Анна Богдановна", 4324, 1, 21, 2.6),
        Student("Лазарев Вячеслав Константинович", 4324, 3, 20, 1.3),
        Student("Иванова Анна Богдановна Вячеслав Константинович", 4324, 3, 20, 3.3),
    ]

    print("Массив до сортировки:")
    print_students(students)

    heap_sort_books(students)
    print("\nМассив после сортировки кучей по убыванию курса:")
    print_students(students)

    cocktail_sort(students, lambda student1, student2: student1.full_name > student2.full_name)
    print("\nМассив после сортировки перемешиванием по возрастанию полного имени:")
    print_students(students)

    random_students = [Student(
        full_name="Student" + str(i),
        group_number=random.randint(100, 200),
        course=random.randint(1, 5),
        age=random.randint(18, 30),
        average_grade=random.uniform(3.0, 5.0)
    ) for i in range(1000)]


    