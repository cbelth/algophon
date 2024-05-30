import unittest
import sys

sys.path.append('../')
from algophon.data_structures import Node, Graph

class TestDataStructures(unittest.TestCase):
    def test_node_init(self):
        node = Node('x', Graph())
        assert(node is not None)
        assert(node == 'x')
        assert(node != 'y')

    def test_node_neighbors(self):
        graph = Graph()
        graph.add_edges([(1, 2), (1, 'a'), (2, 3), (3, 1), ('z', 1)])
        assert(graph._nodes[1].neighbors() == [2, 3, 'a', 'z'])
        assert(graph._nodes[2].neighbors() == [1, 3])
        assert(graph._nodes[3].neighbors() == [1, 2])
        assert(graph._nodes['a'].neighbors() == [1])
        assert(graph._nodes['z'].neighbors() == [1])

        # directed version

        graph = Graph(directed=True)
        graph.add_edges([(1, 2), (1, 'a'), (2, 3), (3, 1), ('z', 1)])
        assert(graph._nodes[1].neighbors() == [2, 'a'])
        assert(graph._nodes[2].neighbors() == [3])
        assert(graph._nodes[3].neighbors() == [1])
        assert(graph._nodes['a'].neighbors() == [])
        assert(graph._nodes['z'].neighbors() == [1])

    def test_graph_init(self):
        graph = Graph()
        assert(graph is not None)
        assert(graph.num_nodes() == graph.num_edges() == 0)

    def test_graph_node_getters_setters(self):
        graph = Graph()
        assert(graph.num_nodes() == 0)
        graph.add_node('x')
        assert(graph.num_nodes() == 1)
        graph.add_nodes(['y', 'z'])
        assert(graph.num_nodes() == 3)
        graph.add_node('x') # does not change
        assert(graph.num_nodes() == 3)

        assert(graph.nodes() == {'x', 'y', 'z'})

    def test_graph_edge_getters_setters(self):
        graph = Graph()
        assert(graph.num_nodes() == 0)
        assert(graph.num_edges() == 0)

        graph.add_edge(1, 2)
        assert(graph.num_edges() == 1)
        graph.add_edge(('x', 'y'))
        assert(graph.num_edges() == 2)
        graph.add_edges([(2, 3), (1, 'x')])
        assert(graph.num_edges() == 4)
        graph.add_edge(1, 2) # does not change
        assert(graph.num_edges() == 4)
        
        assert(graph.nodes() == {1, 2, 3, 'x', 'y'})
        assert(graph.edges() == {(1, 2), (2, 3), ('x', 'y'), (1, 'x')})

        graph.add_edge(2, 1) # does not change in undirected graph
        assert(graph.edges() == {(1, 2), (2, 3), ('x', 'y'), (1, 'x')})

        # directed version

        graph = Graph(directed=True)
        assert(graph.num_nodes() == 0)
        assert(graph.num_edges() == 0)

        graph.add_edge(1, 2)
        assert(graph.num_edges() == 1)
        graph.add_edge(('x', 'y'))
        assert(graph.num_edges() == 2)
        graph.add_edges([(2, 3), (1, 'x')])
        assert(graph.num_edges() == 4)
        graph.add_edge(1, 2) # does not change
        assert(graph.num_edges() == 4)
        
        assert(graph.nodes() == {1, 2, 3, 'x', 'y'})
        assert(graph.edges() == {(1, 2), (2, 3), ('x', 'y'), (1, 'x')})

        graph.add_edge(2, 1) # changes in directed graph
        assert(graph.edges() == {(1, 2), (2, 3), ('x', 'y'), (1, 'x'), (2, 1)})

    def test_graph_search(self):
        graph = Graph()
        graph.add_edges([(0, 1), (0, 2), (1, 3), (1, 4), (3, 5), (5, 6), (6, 7)])
        assert(list(graph.bfs(start_node=0)) == [0, 1, 2, 3, 4, 5, 6, 7])
        assert(list(graph.dfs(start_node=0)) == [0, 1, 3, 5, 6, 7, 4, 2])

        graph.add_edges([(3, 'a'), (3, 'z'), ('a', 'b'), ('b', 'c')])
        assert(list(graph.bfs(start_node=0)) == [0, 1, 2, 3, 4, 5, 'a', 'z', 6, 'b', 7, 'c'])
        assert(list(graph.dfs(start_node=0)) == [0, 1, 3, 5, 6, 7, 'a', 'b', 'c', 'z', 4, 2])

        # directed version

        graph = Graph()
        graph.add_edges([(0, 1), (0, 2), (1, 3), (1, 4), (3, 5), (5, 6), (6, 7)])
        assert(list(graph.bfs(start_node=0)) == [0, 1, 2, 3, 4, 5, 6, 7])
        assert(list(graph.dfs(start_node=0)) == [0, 1, 3, 5, 6, 7, 4, 2])

        graph.add_edges([(3, 'a'), (3, 'z'), ('a', 'b'), ('b', 'c')])
        assert(list(graph.bfs(start_node=0)) == [0, 1, 2, 3, 4, 5, 'a', 'z', 6, 'b', 7, 'c'])
        assert(list(graph.dfs(start_node=0)) == [0, 1, 3, 5, 6, 7, 'a', 'b', 'c', 'z', 4, 2])

        # graph with > 1 component

        graph = Graph()
        graph.add_edges([(1, 2), (1, 3), (3, 4), # CC1
                         (5, 6), (6, 7), (6, 8), (7, 9)]) # CC2
        assert(list(graph.bfs()) == [1, 2, 3, 4, 5, 6, 7, 8, 9])
        assert(list(graph.dfs()) == [1, 2, 3, 4, 5, 6, 7, 9, 8])

    def test_graph_is_dag(self):
        graph = Graph()
        assert(not graph.is_dag()) # undirected graphs are not DAGs

        # digraph 1
        graph = Graph(directed=True)
        assert(graph.is_dag()) # digraph with no edges is trivially a DAG
        graph.add_edges([(0, 1), (1, 2), (2, 3)])
        assert(graph.is_dag())
        graph.add_edge((2, 0)) # add cyclce
        assert(not graph.is_dag())

        # digraph 2
        graph = Graph(directed=True)
        assert(graph.is_dag()) # digraph with no edges is trivially a DAG
        graph.add_edges([('a', 'c'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('b', 'g'), ('g', 'h'), ('h', 'f')])
        assert(graph.is_dag())
        graph.add_edge(('h', 'g')) # add cyclce
        assert(not graph.is_dag())
        graph.add_edge(('e', 'c')) # add cyclce
        assert(not graph.is_dag())

        # digraph 3
        graph = Graph(directed=True)
        assert(graph.is_dag()) # digraph with no edges is trivially a DAG
        graph.add_edges([
            (1, 2), (2, 3), (2, 4), (3, 5), (3, 6), 
            (4, 6), # cross edge
            ('a', 'b'),
            ('b', 2) # cross edge
        ])
        assert(graph.is_dag())
        graph.add_edge(4, 1) # add cylce
        assert(not graph.is_dag())

        # digraph 4
        graph = Graph(directed=True)
        assert(graph.is_dag()) # digraph with no edges is trivially a DAG
        graph.add_edges([
            (1, 2), (2, 3), (2, 4), (3, 5), (3, 6), 
            (4, 6), # cross edge
            ('a', 'b'),
            ('b', 2) # cross edge
        ])
        assert(graph.is_dag())
        graph.add_edge(6, 'b') # add cylce
        assert(not graph.is_dag())

        # digraph 5
        graph = Graph(directed=True)
        assert(graph.is_dag()) # digraph with no edges is trivially a DAG
        graph.add_edges([
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), 
        ])
        assert(graph.is_dag())
        graph.add_edge(6, 1) # add cylce
        assert(not graph.is_dag())


if __name__ == "__main__":
    unittest.main()