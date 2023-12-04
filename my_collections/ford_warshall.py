"""
Алгоритм
1) Инициализируем двоичную матрицу размером  V x V где V - кол-во вершин в графе.
2) Устанавливаем значение бесконечность для всех кратчайших путей между парами вершин (u,v) и 0 для всех остальных
3) Находим все пары кратчайших путей, в которых отсутствуют промежуточные вершины, затем кратчайшие пути с одной промежуточной вершиной и так далее.
4) На каждом шаге производим минимизацию значения кратчайшего пути между парами вершин (u, v), присваивая их пересечению в матрице следующее значение min(d[u][v], d[u][k]+d[k][v]),
где k, u, v = {0, 1, 2, ..., V }
"""
from graph import Graph, T, AdjacentEdge, Edge


def ford_warshall(graph: Graph[T]) -> dict[T, dict[T, int]]:
    cost_matrix: dict[T, dict[T, int]] = {} #создаем матрицу стоимости

    def vertex_init(vertex: T) -> None:#верхний уровень обход (создаем строку матрицы), движение по смежным ребрам, начиная с вершину, которую передали в функцию
        cost_matrix[vertex] = {}

        def edge_init(edge: AdjacentEdge[T]) -> None: #заполнение
            cost_matrix[vertex][edge.finish_edge] = edge.weight

        graph.for_each_adjacent_edge(vertex, edge_init)
    graph.for_each_vertex(vertex_init)

    for k, _ in graph.vertexes.items():#
        for u, _ in graph.vertexes.items():
            for v, _ in graph.vertexes.items():
                ok = ok1 = ok2 = False

                if u in cost_matrix:
                    if k in cost_matrix[u]:
                        ok1 = True

                if k in cost_matrix:
                    if v in cost_matrix[k]:
                        ok2 = True

                if not ok1 or not ok2:
                    continue

                old_cost: int = 0
                if u in cost_matrix:
                    if v in cost_matrix[u]:
                        old_cost = cost_matrix[u][v]
                        ok = True

                new_cost: int = cost_matrix[u][k] + cost_matrix[k][v]
                if ok:
                    if new_cost < old_cost:
                        cost_matrix[u][v] = new_cost
                else:
                    cost_matrix[u][v] = new_cost

    return cost_matrix


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

    graph: Graph[str] = Graph[str](is_directed=True)

    for it in vertexes:
        graph.add_edge(it.start_edge, it.finish_edge, it.weight)

    cost_matrix = ford_warshall(graph)
    for key, val in cost_matrix.items():
        print(f"Key: {key}, Val: {val}")