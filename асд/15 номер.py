import timeit
import random
from typing import List
from dataclasses import dataclass

@dataclass
class Book:
    author: str
    publisher: str
    pages: int
    price: float
    isbn: str


def out_red(text):
    print("\033[31m {}" .format(text))
def insertion_sort_books(books: List[Book]) -> None:
    """
    Функция сортировки вставками для списка книг по полю "стоимость" в порядке возрастания.
    """
    for i in range(1, len(books)):
        key = books[i]
        j = i - 1
        while j >= 0 and key.price < books[j].price:
            books[j + 1] = books[j]
            j -= 1
        books[j + 1] = key

def heapify(arr, n, i):
    """
    Функция для преобразования списка в max-кучу.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left].pages < arr[largest].pages:  # Сравниваем количество страниц в порядке убывания
        largest = left

    if right < n and arr[right].pages < arr[largest].pages:  # Сравниваем количество страниц в порядке убывания
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort_books(books: List[Book]) -> None:
    """
    Функция сортировки кучей для списка книг по полю "кол-во страниц" в порядке убывания.
    """
    n = len(books)

    for i in range(n // 2 - 1, -1, -1):
        heapify(books, n, i)

    for i in range(n - 1, 0, -1):
        books[i], books[0] = books[0], books[i]
        heapify(books, i, 0)

def generate_random_books(n):
    """
    Генерирует случайные книги для бенчмарка.
    """
    books = []
    for _ in range(n):
        author = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for  i in range(5))
        publisher = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(10))
        pages = random.randint(100, 500)
        price = random.uniform(10, 100)
        isbn = "".join(random.choice("0123456789") for _ in range(10))
        books.append(Book(author, publisher, pages, price, isbn))
    return books

def print_books(books: List[Book]) -> None:
    """
    Функция для вывода книг в удобочитаемом формате.
    """
    for book in books:
        out_white(f"Автор: {book.author} Издательство: {book.publisher} Количество страниц: {book.pages} Цена: {book.price} ISBN: {book.isbn}")

if __name__ == '__main__':
    def out_white(text):
        print("\033[0m{}".format(text))

    def out_blue(text):
        print("\033[34m{}".format(text))

    books = [
        Book("Умар  ", "Эксмо", 300, 3300, "ISBN1"),
        Book("Дима  ", "Эксмо", 250, 3000, "ISBN2"),
        Book("Саня  ", "Эксмо", 240, 2083, "ISBN1"),
        Book("Лиза  ", "Эксмо", 230, 2999, "ISBN2"),
        Book("Настя ", "Эксмо", 220, 2100, "ISBN1"),
        Book("Влад  ", "Эксмо", 235, 2200, "ISBN2"),
        Book("Лиза  ", "Эксмо", 293, 2900, "ISBN1"),
        Book("Шерзод", "Эксмо", 243, 2700, "ISBN2"),
        Book("Никита", "Эксмо", 228, 2300, "ISBN1"),
        Book("Наташа", "Эксмо", 289, 2100, "ISBN2"),

    ]

    out_blue("Массив до сортировки:")
    print_books(books)

    insertion_sort_books(books)
    out_blue("\nМассив после сортировки вставкой по цене (по возрастанию):")
    print_books(books)

    heap_sort_books(books)
    out_blue("\nМассив после сортировки кучей по количеству страниц (по убыванию):")
    print_books(books)

    books = generate_random_books(10000)
    out_red("\nБЕНЧМАРКИ")
    def benchmark_insertion_sort():
        insertion_sort_books(books)


    insertion_time = timeit.timeit(benchmark_insertion_sort, number=1)
    print(f"Время сортировки вставкой: {insertion_time:.6f} секунд")


    # Бенчмарк для сортировки кучей
    def benchmark_heap_sort():
        heap_sort_books(books)


    heap_time = timeit.timeit(benchmark_heap_sort, number=1)
    print(f"Время сортировки кучей: {heap_time:.6f} секунд")