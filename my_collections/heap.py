from typing import Callable, Optional, Generic
from dataclasses import dataclass
from my_collections import MySet
from graph import Graph, T

__is_found: bool = False

@dataclass
class Edge(Generic[T]):
    start_edge: T
    finish_edge: T
    weight: int = 0


@dataclass
class AdjacentEdge(Generic[T]):
    finish_edge: T
    weight: int = 0

    def __hash__(self) -> int:
        return hash((self.finish_edge, self.weight))


def dsf(graph: Graph[T], start: T, target: T, visitfunc: Callable[[T], None] = None) -> None:
    global __is_found
    visited = MySet[T]()
    __is_found = False
    __dsf(graph, start, target, visited, visitfunc)


def __dsf(graph: Graph[T], current: T, target: T, visited: MySet[T], visitfunc: Callable[[T], None]) -> None:
    global __is_found
    visited.add(current)

    if visitfunc:
        visitfunc(current)

    if current == target:
        __is_found = True
        return

    def __foreach(edge: AdjacentEdge[T]) -> None:
        if not __is_found and edge.finish_edge not in visited:
            __dsf(graph, edge.finish_edge, target, visited, visitfunc)

    graph.for_each_adjacent_edge(current, __foreach)


if __name__ == '__main__':
    vertexes: list[Edge[str]] = [
        Edge("A", "B"),
        Edge("A", "C"),
        Edge("C", "F"),
        Edge("C", "G"),
        Edge("G", "M"),
        Edge("G", "N"),
        Edge("B", "D"),
        Edge("B", "E"),
        Edge("D", "H"),
        Edge("D", "I"),
        Edge("D", "J"),
        Edge("E", "K"),
        Edge("E", "L"),
    ]

    graph: Graph[str] = Graph[str]()

    for it in vertexes:
        graph.add_edge_without_weight(it.start_edge, it.finish_edge)

    def dsf_walk(vertex: str) -> bool:
        print(vertex + " ", end='')
        return vertex == "K"

    dsf(graph, "A", "K", dsf_walk)
    print()
