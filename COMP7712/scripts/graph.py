import sys


class Graph(object):

    def __init__(self, n_vertices, edges=None):
        self.n_vertices = n_vertices
        self.n_edges = 0

        self.adjacency_list = {}
        for i in range(1, self.n_vertices + 1):
            self.adjacency_list[i] = set()

        if edges:
            for e in edges:
                self.add_edge(e)

    def add_edge(self, e):
        if e[0] not in self.adjacency_list:
            raise Exception('Invalid source vertex: ' + e[0])

        self.adjacency_list[e[0]].add(e)
        self.n_edges += 1

    def edge_exists(self, e):
        return e in self.adjacency_list[e[0]]

    def __iter__(self):
        return iter(self.adjacency_list.keys())

    def edges(self, u):
        return self.adjacency_list[u]


class DepthFirstSearch(object):

    def __init__(self, graph):
        self.graph = graph
        self.visited = [False] * (self.graph.n_vertices + 1)
        self.pre = [-1] * (self.graph.n_vertices + 1)
        self.post = [-1] * (self.graph.n_vertices + 1)
        self.clock = 1

    @property
    def n_visited(self):
        return sum(v == True for v in self.visited)

    def execute(self):
        for v in self.graph:
            if not self.visited[v]:
                self.explore(v)

    def previsit(self, v):
        self.pre[v] = self.clock
        self.clock += 1

    def postvisit(self, v):
        self.post[v] = self.clock
        self.clock += 1

    def explore(self, v):
        self.visited[v] = True

        self.previsit(v)

        for e in self.graph.edges(v):
            if not self.visited[e[1]]:
                self.explore(e[1])

        self.postvisit(v)

    def is_backedge(self, e):
        return self.graph.edge_exists(e) and self.post[e[0]] < self.post[e[1]]


def is_dag(g):
    dfs = DepthFirstSearch(g)
    dfs.execute()

    has_cycle = False
    for v in g:
        for e in g.edges(v):
            if dfs.is_backedge(e):
                has_cycle = True

    return not has_cycle


def topological_sort(g):
    if not is_dag(g):
        raise ValueError('Graph contains cycles and can not be linearized')

    dfs = DepthFirstSearch(g)
    dfs.execute()

    return sorted(range(1, g.n_vertices + 1), key=lambda k: dfs.post[k], reverse=True)


def find_longest_path_distance(g, v):
    if not is_dag(g):
        raise ValueError('Graph contains cycles and can not be linearized')

    dist = [sys.maxsize] * (g.n_vertices + 1)
    prev = [-1] * (g.n_vertices + 1)

    dist[v] = 0
    l = topological_sort(g)
    for u in l:
        for e in g.edges(u):
            # Perform update
            if dist[e[1]] > dist[u] - 1:
                dist[e[1]] = dist[u] - 1
                prev[e[1]] = u

    dist = list(map(lambda x: x*-1, dist))
    return max(dist)