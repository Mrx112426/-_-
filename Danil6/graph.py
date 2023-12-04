#2.	Объявите структуру данных «Граф» на основе матрицы смежности с возможностью вывода ее текущего представления в терминал,
# после чего используйте его для реализации алгоритма
# поиска в глубину и алгоритма Прима. Добавьте возможность сохранения текущего представления графа в файл и загрузки из него.

import timeit
from dataclasses import dataclass
from typing import TypeVar, List, Optional

T = TypeVar("T")

@dataclass
class _PrimNode:
    start: T
    finish: T
    weight: int

@dataclass
class Edge:
    start_edge: T
    finish_edge: T
    weight: int = 0

class Graph:
    def __init__(self, is_directed: bool = False) -> None:
        self.vertexes: List[T] = []
        self.edges: List[List[Optional[int]]] = []
        self.is_not_directed: bool = not is_directed

    def add_edge(self, vertex1: T, vertex2: T, weight: int) -> None:
        if vertex1 not in self.vertexes or vertex2 not in self.vertexes:
            raise ValueError("Both vertices must be in the graph")

        index1 = self.vertexes.index(vertex1)
        index2 = self.vertexes.index(vertex2)

        self.edges[index1][index2] = weight
        if self.is_not_directed:
            self.edges[index2][index1] = weight

    def save_to_file(self, filename: str) -> None:
        with open(filename, "w") as file:
            file.write(f"{len(self.vertexes)}\n")
            for vertex in self.vertexes:
                file.write(f"{vertex}\n")

            for row in self.edges:
                file.write(" ".join(str(val) if val is not None else "inf" for val in row))
                file.write("\n")

    def load_from_file(self, filename: str) -> None:
        with open(filename, "r") as file:
            num_vertexes = int(file.readline())
            self.vertexes = [file.readline().strip() for _ in range(num_vertexes)]

            self.edges = []
            for _ in range(num_vertexes):
                row = file.readline().strip().split()
                row = [int(val) if val != "inf" else None for val in row]
                self.edges.append(row)

    def print_all_vertexes(self) -> None:
        print("\nВершины:", ", ".join(map(str, self.vertexes)))

    def print_all_edges(self) -> None:
        print("\nРёбра:")
        for i, row in enumerate(self.edges):
            for j, weight in enumerate(row):
                if weight is not None:
                    print(f"{self.vertexes[i]} --({weight})--> {self.vertexes[j]}")

    def print_matrix(self, matrix: List[List[Optional[int]]]) -> None:
        print("\n Матрица смежности:")
        for row in matrix:
            print(" ".join(str(val) if val is not None else "0" for val in row))

    # Внесем изменения в метод prim
    def prim(self, start: T) -> None:
        mst = Graph(is_directed=self.is_not_directed)

        for vertex in self.vertexes:
            mst.add_vertex(vertex)

        visited = set()
        visited.add(start)

        mst_matrix = [[None] * len(self.vertexes) for _ in range(len(self.vertexes))]

        while len(visited) < len(self.vertexes):
            heap = []

            for i, vertex in enumerate(self.vertexes):
                if vertex in visited:
                    for j, weight in enumerate(self.edges[i]):
                        if self.vertexes[j] not in visited and weight is not None:
                            heap.append(_PrimNode(vertex, self.vertexes[j], weight))

            if not heap:
                break

            heap.sort(key=lambda x: x.weight)
            edge = heap[0]

            mst.add_edge(edge.start, edge.finish, edge.weight)
            visited.add(edge.finish)

            index1 = self.vertexes.index(edge.start)
            index2 = self.vertexes.index(edge.finish)
            mst_matrix[index1][index2] = edge.weight
            if self.is_not_directed:
                mst_matrix[index2][index1] = edge.weight

        print("\nИспользование алгоритма Прима\nМинимальное остовное дерево:")
        mst.print_all_vertexes()
        mst.print_all_edges()
        mst.print_matrix(mst_matrix)

    def add_vertex(self, vertex: T) -> None:
        if vertex not in self.vertexes:
            self.vertexes.append(vertex)
            for row in self.edges:
                row.append(None)
            self.edges.append([None] * len(self.vertexes))
        else:
            print(f"Вершина {vertex} уже добавлена в граф")

    def dfs(self, start: T, visit_func: Optional[callable] = None) -> None:
        visited = set()

        def dfs_recursive(vertex: T, path: List[T]) -> None:
            visited.add(vertex)
            path.append(vertex)

            if visit_func:
                visit_func(vertex, path)

            for i, adjacent in enumerate(self.edges[self.vertexes.index(vertex)]):
                if adjacent is not None and self.vertexes[i] not in visited:
                    dfs_recursive(self.vertexes[i], path[:])  # передача копии пути

        dfs_recursive(start, [])

def print_path(vertex: str, path: List[str]) -> None:
    print(f"Path to {vertex}: {' -> '.join(path)}")

def benchmark_dfs(graph, start_vertex, num_trials=100):
    def run_dfs():
        graph.dfs(start_vertex)

    time = timeit.timeit(run_dfs, number=num_trials)
    print(f"Время выполнения поиска в глубину {num_trials} раз: {time} секунд")

def benchmark_prim(graph, start_vertex, num_trials=100):
    # Вызов алгоритма Прима один раз перед началом цикла
    prim_result = graph.prim(start_vertex)

    def run_prim():
        # Использование результата, сохраненного ранее
        prim_result

    time = timeit.timeit(run_prim, number=num_trials)
    print(f"Время выполнения алгоритма Прима {num_trials} раз: {time} секунд")


if __name__ == '__main__':
    graph = Graph(is_directed=False)

    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")
    graph.add_vertex("E")

    graph.add_edge("A", "B", 2)
    graph.add_edge("A", "C", 3)
    graph.add_edge("B", "A", 2)
    graph.add_edge("B", "C", 5)
    graph.add_edge("B", "D", 1)
    graph.add_edge("C", "A", 3)
    graph.add_edge("C", "B", 5)
    graph.add_edge("C", "D", 4)
    graph.add_edge("C", "E", 6)
    graph.add_edge("D", "B", 1)
    graph.add_edge("D", "C", 4)
    graph.add_edge("E", "C", 6)


    print("Исходный граф:")
    graph.print_all_vertexes()
    graph.print_all_edges()
    graph.print_matrix(graph.edges)

    print("\nDFS:")
    graph.dfs("A", visit_func=print_path)
    graph.prim("A")

    print("\nБЕНЧМАРКИ")
    benchmark_dfs(graph, "A")
    benchmark_prim(graph, "A")
