from unittest import TestCase

from graph import Graph, DepthFirstSearch, is_dag, topological_sort


class GraphTest(TestCase):

    def test_create_graph(self):
        g = Graph(n_vertices=5)

        self.assertEqual(g.n_vertices, 5)
        self.assertEqual(g.n_edges, 0)

        g.add_edge((1, 2))
        self.assertEqual(g.n_edges, 1)

        self.assertTrue(g.edge_exists((1, 2)))
        self.assertFalse(g.edge_exists((2, 1)))

        g.add_edge((2, 1))
        self.assertEqual(g.n_edges, 2)
        self.assertTrue(g.edge_exists((2, 1)))

        g = Graph(n_vertices=5, edges=[(1, 2), (1, 3), (3, 2), (2, 1), (4, 5), (4, 2)])

        # Test iteration
        vertices = [v for v in g]
        self.assertEqual(len(vertices), g.n_vertices)

        edges = [e for e in g.edges(1)]
        self.assertEqual(len(edges), 2)

        edges = [e for e in g.edges(2)]
        self.assertEqual(len(edges), 1)

        edges = [e for e in g.edges(3)]
        self.assertEqual(len(edges), 1)

        edges = [e for e in g.edges(4)]
        self.assertEqual(len(edges), 2)

        edges = [e for e in g.edges(5)]
        self.assertEqual(len(edges), 0)

    def test_dfs(self):
        # Single Vertex, No Edges
        g = Graph(n_vertices=1, edges=[])

        dfs = DepthFirstSearch(g)
        self.assertEqual(dfs.n_visited, 0)

        dfs.execute()
        self.assertEqual(dfs.n_visited, g.n_vertices)

        self.assertEqual(dfs.pre[1], 1)
        self.assertEqual(dfs.post[1], 2)

        # Two vertices, no edges
        g = Graph(n_vertices=2, edges=[])

        dfs = DepthFirstSearch(g)
        self.assertEqual(dfs.n_visited, 0)

        dfs.execute()
        self.assertEqual(dfs.n_visited, g.n_vertices)

        self.assertEqual(dfs.pre[1], 1)
        self.assertEqual(dfs.post[1], 2)

        self.assertEqual(dfs.pre[2], 3)
        self.assertEqual(dfs.post[2], 4)

        # Two vertices, one edge
        g = Graph(n_vertices=2, edges=[(1, 2)])

        dfs = DepthFirstSearch(g)
        self.assertEqual(dfs.n_visited, 0)

        dfs.execute()
        self.assertEqual(dfs.n_visited, g.n_vertices)

        self.assertEqual(dfs.pre[1], 1)
        self.assertEqual(dfs.post[1], 4)

        self.assertEqual(dfs.pre[2], 2)
        self.assertEqual(dfs.post[2], 3)

        # Two vertices, two edges (cycle)
        g = Graph(n_vertices=2, edges=[(1, 2), (2, 1)])

        dfs = DepthFirstSearch(g)
        self.assertEqual(dfs.n_visited, 0)

        dfs.execute()
        self.assertEqual(dfs.n_visited, g.n_vertices)

        self.assertEqual(dfs.pre[1], 1)
        self.assertEqual(dfs.post[1], 4)

        self.assertEqual(dfs.pre[2], 2)
        self.assertEqual(dfs.post[2], 3)

        # 5 vertex disconnected DAG
        g = Graph(n_vertices=5, edges=[(1, 2), (3, 1), (3, 4)])

        dfs = DepthFirstSearch(g)
        self.assertEqual(dfs.n_visited, 0)

        dfs.execute()
        self.assertEqual(dfs.n_visited, g.n_vertices)

        self.assertEqual(dfs.pre[1], 1)
        self.assertEqual(dfs.post[1], 4)

        self.assertEqual(dfs.pre[2], 2)
        self.assertEqual(dfs.post[2], 3)

        self.assertEqual(dfs.pre[3], 5)
        self.assertEqual(dfs.post[3], 8)

        self.assertEqual(dfs.pre[4], 6)
        self.assertEqual(dfs.post[4], 7)

        self.assertEqual(dfs.pre[5], 9)
        self.assertEqual(dfs.post[5], 10)

    def test_is_back_edge(self):

        g = Graph(n_vertices=3, edges=[(1, 2), (2, 3), (3, 1)])

        dfs = DepthFirstSearch(g)
        dfs.execute()

        self.assertFalse(dfs.is_backedge((1, 2)))
        self.assertFalse(dfs.is_backedge((2, 3)))
        self.assertTrue(dfs.is_backedge((3, 1)))

    def test_is_dag(self):

        # No cycle - DAG
        g = Graph(n_vertices=3, edges=[(1, 2)])
        self.assertTrue(is_dag(g))

        # Cycle - not a DAG
        g = Graph(n_vertices=3, edges=[(1, 2), (2, 3), (3, 1)])
        self.assertFalse(is_dag(g))

        # No cycle, but disconnected - DAG
        g = Graph(n_vertices=5, edges=[(1, 2), (3, 1), (3, 4)])
        self.assertTrue(is_dag(g))

    def test_topo_sort(self):
        g = Graph(n_vertices=3, edges=[(1, 2)])
        l = topological_sort(g)
        self.verify_linearization(l, g)

        g = Graph(n_vertices=5, edges=[(1, 2), (3, 1), (3, 4)])
        l = topological_sort(g)
        self.verify_linearization(l, g)

        g = Graph(n_vertices=6, edges=[(1, 3), (2, 1), (2, 4), (4, 3), (3, 6), (3, 5)])
        l = topological_sort(g)
        print(l)
        self.verify_linearization(l, g)

        # Raise exception if cycle
        g = Graph(n_vertices=3, edges=[(1, 2), (2, 3), (3, 1)])
        self.assertRaises(ValueError, topological_sort, g)

    def test_longest_path_in_dag(self):
        g = Graph(n_vertices=6, edges=[(1, 3), (2, 1), (2, 4), (4, 3), (3, 6), (3, 5)])
        p = find_longest_path(g)



    def verify_linearization(self, l, g):
        # Check that nodes later in the linearization do not have edges to any of the earlier nodes
        for i in range(len(l)):
            for j in range(i):
                self.assertFalse(g.edge_exists((l[i], l[j])))
