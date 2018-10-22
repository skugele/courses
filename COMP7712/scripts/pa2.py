import re

from graph import Graph, is_dag, topological_sort, find_longest_path_distance

n_vertices = None
edges = []

print("Specify a graph. (A blank line stops input)")
while True:
    value = input()

    # Stop input line only contains white space
    if re.match('^\s*$', value):
        break

    if n_vertices is None:
        n_vertices = int(value)
    else:
        u, v = map(int, value.split(','))
        edges.append((u, v))

graph = Graph(n_vertices, edges)
print('YES') if is_dag(graph) else print('NO')
print(*topological_sort(graph))
print(find_longest_path_distance(graph, 1))
