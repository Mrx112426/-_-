from dataclasses import dataclass
from typing import TypeVar, List, Optional, Tuple

T = TypeVar("T")

@dataclass
class _PrimNode:
    start: T
    finish: T
    weight: int

class Graph:
    def __init__(self, is_directed: bool = False) -> None:
        # Список вершин графа
        self.vertexes: List[T] = []
        # Матрица смежности (веса ребер между вершинами)
        self.edges: List[List[Optional[int]]] = []
        # Флаг для определения направленности графа
        self.is_not_directed: bool = not is_directed


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

    def prim(self, start: T) -> 'Graph':
        mst = Graph(is_directed=self.is_not_directed)

        # Добавляем все вершины в mst
        for vertex in self.vertexes:
            mst.add_vertex(vertex)

        # Множество посещенных вершин
        visited = set()
        visited.add(start)

        while len(visited) < len(self.vertexes):
            heap = []

            for i, vertex in enumerate(self.vertexes):
                if vertex in visited:
                    for j, weight in enumerate(self.edges[i]):
                        if self.vertexes[j] not in visited and weight is not None:
                            # Добавляем ребра из текущей вершины в не посещенные
                            heap.append(_PrimNode(vertex, self.vertexes[j], weight))

            if not heap:
                break

            # Сортируем ребра по весу
            heap.sort(key=lambda x: x.weight)
            # Выбираем минимальное ребро
            edge = heap[0]

            # Добавляем ребра в mst
            mst.add_edge(edge.start, edge.finish, edge.weight)
            visited.add(edge.finish)

        return mst

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
        else:
            print(f"Вершина {vertex} уже добавлена в граф")

if __name__ == '__main__':
    # Создаем граф
    graph = Graph(is_directed=False)
    new_graph = Graph(is_directed=False)

    # Добавляем вершины
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("E")
    graph.add_vertex("F")

    # Добавляем ребра
    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 6)
    graph.add_edge("A", "F", -4)
    graph.add_edge("B", "A", 4)
    graph.add_edge("B", "C", 5)
    graph.add_edge("B", "E", 5)
    graph.add_edge("B", "F", 7)
    graph.add_edge("C", "A", 6)
    graph.add_edge("C", "B", 5)
    graph.add_edge("C", "E", 1)
    graph.add_edge("C", "F", 8)
    graph.add_edge("E", "B", 5)
    graph.add_edge("E", "C", 1)
    graph.add_edge("E", "F", 6)
    graph.add_edge("F", "A", -4)
    graph.add_edge("F", "B", 7)
    graph.add_edge("F", "C", 8)
    graph.add_edge("F", "E", 6)

    # Выводим информацию о графе
    print("Исходный граф:")
    graph.print_all_vertexes()
    graph.print_all_edges()
    graph.print_matrix()

    # Применяем алгоритм Прима, начиная с вершины "A"
    mst = graph.prim("A")

    # Добавляем вершины в новый граф (если их еще нет)
    for vertex in mst.vertexes:
        new_graph.add_vertex(vertex)

    # Применяем алгоритм Прима, начиная с вершины "A"
    mst = new_graph.prim("A")

    # Выводим результат
    print("\nМинимальное остовное дерево:")
    mst.print_all_vertexes()
    mst.print_all_edges()
    mst.print_matrix()


