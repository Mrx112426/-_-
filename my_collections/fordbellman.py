import math
from dataclasses import dataclass
from typing import Generic, Optional

from graph import Graph, T, Edge

@dataclass
class _Node(Generic[T]):#Создаем узел
    cost: int
    predecessor: Optional[T]


def ford_bellman(graph: Graph[T], start: T, end: T) -> tuple[list[T], int]: #
    nodes: dict[T, _Node[T]] = {} #создается словарь

    def foreach(vertex: T) -> None:#метод обхода (нужно обойти все вершины, сформировать словарь и в качестве стоимости присвоить бесконечность)
        nodes[vertex] = _Node[T](math.inf, None)

    graph.for_each_vertex(foreach)
    nodes[start].cost = 0 #первая стартовая вершина значение 0

    amount_vertex = graph.amount_vertexes() #количество вершин понадобится для следующего образа (каждый шаг алгоритма начинается с полного обхода всего)

    def calc(edge: Edge[T]) -> None:#
        cost = nodes[edge.start_edge].cost + edge.weight#высчитываем стоимость движения по ребрам
        if cost < nodes[edge.finish_edge].cost:#смотрим она меньше существуещей или не меньше
            nodes[edge.finish_edge].cost = cost
            vertex = edge.start_edge
            nodes[edge.finish_edge].predecessor = vertex#присваем сыллку на нужную вершину

    for i in range(0, amount_vertex - 1):
        graph.for_each_edge(calc)

    # проверка на наличие отрицательного (негативного) цикла
    has_negative_loop = False

    def negative_search(edge: Edge[T]) -> None:
        nonlocal has_negative_loop
        if (nodes[edge.start_edge].cost + edge.weight <
                nodes[edge.finish_edge].cost):
            has_negative_loop = True
    graph.for_each_edge(negative_search)

    if has_negative_loop:
        return [], 0

    vertex: Optional[T] = end
    path: list[T] = []
    while vertex is not None:
        path.append(vertex)
        vertex = nodes[vertex].predecessor
    path.reverse()
    return path, nodes[end].cost


if __name__ == '__main__':
    vertexes: list[Edge[str]] = [
        Edge("A", "B", -3),
        Edge("B", "A", 4),
        Edge("B", "C", 5),
        Edge("B", "F", 7),
        Edge("C", "E", 1),
        Edge("C", "A", 6),
        Edge("E", "B", 5),
        Edge("E", "F", 6),
        Edge("F", "A", -4),
        Edge("F", "C", 8),
    ]

    graph: Graph[str] = Graph[str](is_directed=True) #True = направленный

    for it in vertexes:
        graph.add_edge(it.start_edge, it.finish_edge, it.weight)

    path, cost = ford_bellman(graph, "E", "C")
    print(f"Path: {path} with cost: {cost}")

    path, cost = ford_bellman(graph, "E", "A")
    print(f"Path: {path} with cost: {cost}")

    path, cost = ford_bellman(graph, "A", "E")
    print(f"Path: {path} with cost: {cost}")