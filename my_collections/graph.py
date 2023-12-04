from dataclasses import dataclass
from typing import TypeVar, List, Optional, Tuple
import math
import timeit

T = TypeVar("T")

@dataclass
class _Node:
    cost: int
    predecessor: Optional[T]

class Graph:
    def __init__(self, is_directed: bool = False) -> None:
        # Список вершин графа
        self.vertexes: List[T] = []
        # Матрица смежности (веса ребер между вершинами)
        self.edges: List[List[Optional[int]]] = []
        # Флаг для определения направленности графа
        self.is_not_directed: bool = not is_directed

    def add_vertex(self, vertex: T) -> None:
        # Добавление новой вершины
        if vertex not in self.vertexes:
            # Добавляем вершину в список вершин
            self.vertexes.append(vertex)
            # Добавляем новый столбец в матрицу смежности
            for row in self.edges:
                row.append(None)
            # Добавляем новую строку в матрицу смежности
            self.edges.append([None] * len(self.vertexes))

    def add_edge(self, vertex1: T, vertex2: T, weight: int) -> None:
        # Добавление ребра между вершинами с указанным весом
        if vertex1 not in self.vertexes or vertex2 not in self.vertexes:
            # Проверка наличия обеих вершин в графе
            raise ValueError("Both vertices must be in the graph")

        index1 = self.vertexes.index(vertex1)
        index2 = self.vertexes.index(vertex2)

        # Установка веса ребра в матрице смежности
        self.edges[index1][index2] = weight
        if self.is_not_directed:
            # Если граф ненаправленный, установка веса в зеркальной ячейке
            self.edges[index2][index1] = weight

    def ford_bellman(self, start: T, end: T) -> Tuple[List[T], int]:
        # Алгоритм Форда-Беллмана для поиска кратчайшего пути
        nodes = {vertex: _Node(float('inf'), None) for vertex in self.vertexes}
        start_index = self.vertexes.index(start)
        nodes[start].cost = 0

        for _ in range(len(self.vertexes) - 1):
            for i in range(len(self.vertexes)):
                for j in range(len(self.vertexes)):
                    if self.edges[i][j] is not None:
                        new_cost = nodes[self.vertexes[i]].cost + self.edges[i][j]
                        if new_cost < nodes[self.vertexes[j]].cost:
                            nodes[self.vertexes[j]].cost = new_cost
                            nodes[self.vertexes[j]].predecessor = self.vertexes[i]

        has_negative_loop = any(
            nodes[self.vertexes[i]].cost + self.edges[i][j] < nodes[self.vertexes[j]].cost
            for i in range(len(self.vertexes))
            for j in range(len(self.vertexes))
            if self.edges[i][j] is not None
        )

        if has_negative_loop:
            return [], 0

        vertex = end
        path = []
        while vertex is not None:
            path.append(vertex)
            vertex = nodes[vertex].predecessor
        path.reverse()
        return path, nodes[end].cost

    def ford_warshall(self) -> List[List[int]]:
        # Алгоритм Флойда-Уоршелла для поиска кратчайших путей между всеми парами вершин
        cost_matrix = [[float("inf") if val is None else val for val in row] for row in self.edges]

        for k in range(len(self.vertexes)):
            for i in range(len(self.vertexes)):
                for j in range(len(self.vertexes)):
                    if cost_matrix[i][k] + cost_matrix[k][j] < cost_matrix[i][j]:
                        cost_matrix[i][j] = cost_matrix[i][k] + cost_matrix[k][j]

        return cost_matrix


    def save_to_file(self, filename: str) -> None:
        # Сохранение графа в файл
        with open(filename, "w") as file:
            file.write(f"{len(self.vertexes)}\n")
            for vertex in self.vertexes:
                file.write(f"{vertex}\n")

            for row in self.edges:
                file.write(" ".join(str(val) if val is not None else "inf" for val in row))
                file.write("\n")

    def load_from_file(self, filename: str) -> None:
        # Загрузка графа из файла
        with open(filename, "r") as file:
            num_vertexes = int(file.readline())
            self.vertexes = [file.readline().strip() for _ in range(num_vertexes)]

            self.edges = []
            for _ in range(num_vertexes):
                row = file.readline().strip().split()
                row = [int(val) if val != "inf" else None for val in row]
                self.edges.append(row)

    def print_all_vertexes(self) -> None:
        # Вывод всех вершин графа
        print("Вершины:\n", ", ".join(map(str, self.vertexes)))

    def print_all_edges(self) -> None:
        # Вывод всех ребер графа
        print("Рёбра:\n")
        for i, row in enumerate(self.edges):
            for j, weight in enumerate(row):
                if weight is not None:
                    print(f"{self.vertexes[i]} --({weight})--> {self.vertexes[j]}")

    def print_matrix(self) -> None:
        print("Матрица Смежности:")
        for row in self.edges:
            print(" ".join(str(val) if val is not None else "0" for val in row))

# Пример использования
def benchmark_ford_bellman(graph, start, end):
    def wrapper():
        graph.ford_bellman(start, end)

    time_taken = timeit.timeit(wrapper, number=1000)  # Измеряем время выполнения для 1000 вызовов
    print(f"Ford-Bellman Algorithm Time: {time_taken} seconds")

def benchmark_floyd_warshall(graph):
    def wrapper():
        graph.ford_warshall()

    time_taken = timeit.timeit(wrapper, number=1000)  # Измеряем время выполнения для 1000 вызовов
    print(f"Floyd-Warshall Algorithm Time: {time_taken} seconds")

if __name__ == '__main__':
    graph = Graph(is_directed=True)

    # Добавляем вершины
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("E")
    graph.add_vertex("F")

    # Добавляем ребра
    graph.add_edge("A", "B", -3)
    graph.add_edge("B", "A", 4)
    graph.add_edge("B", "C", 5)
    graph.add_edge("B", "F", 7)
    graph.add_edge("C", "E", 1)
    graph.add_edge("C", "A", 6)
    graph.add_edge("E", "B", 5)
    graph.add_edge("E", "F", 6)
    graph.add_edge("F", "A", -4)
    graph.add_edge("F", "C", 8)

    graph.print_all_vertexes()
    graph.print_all_edges()
    # Вывод матрицы смежности
    print("")
    graph.print_matrix()
    print("")
    # Сохраняем граф в файл и загружаем из файла
    graph.save_to_file("graph.txt")

    new_graph = Graph(is_directed=True)
    new_graph.load_from_file("graph.txt")

    new_graph.print_all_vertexes()
    new_graph.print_all_edges()

    # Пример использования алгоритмов
    print("\nАлгоритм Форда Беллмана")
    path, cost = new_graph.ford_bellman("E", "C")
    print(f"Path: {path} with cost: {cost}")

    path, cost = new_graph.ford_bellman("E", "A")
    print(f"Path: {path} with cost: {cost}")

    path, cost = new_graph.ford_bellman("A", "E")
    print(f"Path: {path} with cost: {cost}")

    print("\nАлгоритм Флойда-Уоршелла")
    cost_matrix = new_graph.ford_warshall()
    for i, row in enumerate(cost_matrix):
        for j, cost in enumerate(row):
            print(f"Cost from {new_graph.vertexes[i]} to {new_graph.vertexes[j]}: {cost}")
    print("\nБенчмарки\n")
    benchmark_ford_bellman(graph, "E", "C")
    benchmark_floyd_warshall(graph)

