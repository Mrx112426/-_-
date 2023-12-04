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
    print("\033[31m{}".format(text))

def out_white(text):
    print("\033[0m{}".format(text))

def out_blue(text):
    print("\033[34m{}".format(text))

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

def print_books(books: List[Book]) -> None:
    """
    Функция для вывода книг в удобочитаемом формате.
    """
    for book in books:
        out_white(f"Автор: {book.author} Издательство: {book.publisher} Количество страниц: {book.pages} Цена: {book.price} ISBN: {book.isbn}")

def binary_search_by_publisher(books: List[Book], target_publisher: str) -> int:
    """
    Бинарный поиск по полю "издательство" (publisher) в отсортированном списке книг.
    """
    if not books:
        raise ValueError("Список книг пуст")

    left, right = 0, len(books) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if books[mid].publisher == target_publisher:
            return mid
        elif books[mid].publisher < target_publisher:
            left = mid + 1
        else:
            right = mid - 1

    raise ValueError("Издательство не найдено")

def generate_sorted_books(n):
    books = []
    for i in range(n):
        author = f"Author{i}"
        publisher = f"Publisher{i}"
        pages = random.randint(100, 500)
        price = random.uniform(10, 100)
        isbn = f"ISBN{i}"
        books.append(Book(author, publisher, pages, price, isbn))
    return books

if __name__ == '__main__':

    books = [
        Book("Умар  ", "АБВ", 300, 3300, "ISBN1"),
        Book("Дима  ", "ЕЖЗ", 250, 3000, "ISBN2"),
        Book("Саня  ", "ТУФ", 240, 2083, "ISBN1"),
        Book("Лиза  ", "МНО", 230, 2999, "ISBN2"),
        Book("Настя ", "МНО", 220, 2100, "ISBN1"),
        Book("Влад  ", "ПРС", 235, 2200, "ISBN2"),
        Book("Лиза  ", "ТУФ", 293, 2900, "ISBN1"),
        Book("Шерзод", "ЦЧШ", 243, 2700, "ISBN2"),
        Book("Никита", "ЩЫЭ", 228, 2300, "ISBN1"),
        Book("Наташа", "ЮЯА", 289, 2100, "ISBN2"),
    ]

    out_blue("Массив до сортировки:")
    print_books(books)

    # Сортировка по издательству (обязательно перед бинарным поиском)
    books.sort(key=lambda book: book.publisher)

    out_blue("Массив после сортировки:")
    print_books(books)

    out_blue("Бинарный поиск по издательству")
    target_publisher = "МНО"  # Издательство, которое мы ищем
    try:
        index = binary_search_by_publisher(books, target_publisher)
        found_book = books[index]
        out_white(f"Найдено издательство '{target_publisher}' по индексу {index}:")
        out_white(f"Автор: {found_book.author} Издательство: {found_book.publisher} Количество страниц: {found_book.pages} Цена: {found_book.price} ISBN: {found_book.isbn}")
    except ValueError as e:
        out_white(f"Поиск по издательству '{target_publisher}' не удался: {e}")

    # Лучший случай: элемент находится в середине
    sorted_books = generate_sorted_books(1000)
    target_publisher_best = sorted_books[len(sorted_books) // 2].publisher

    out_blue("Бенчмарки")
    def benchmark_binary_search_best():
        binary_search_by_publisher(sorted_books, target_publisher_best)

    best_case_time = timeit.timeit(benchmark_binary_search_best, number=1000)
    out_white(f"Лучший случай: Время выполнения бинарного поиска ({target_publisher_best}) в среднем на запрос: {best_case_time:.6f} секунд")

    # Худший случай: элемент отсутствует
    sorted_books = generate_sorted_books(1000)
    target_publisher_worst = "NonExistentPublisher"  # Издательства, которого нет в списке


    def benchmark_binary_search():
        binary_search_by_publisher(books, target_publisher)


    binary_search_time = timeit.timeit(benchmark_binary_search, number=10000)
    out_white(f"Время выполнения бинарного поиска: {binary_search_time :.6f} секунд в среднем на запрос")
