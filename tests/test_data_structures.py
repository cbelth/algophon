import unittest
import sys

sys.path.append('../')
from algophon.data_structures import Graph

class TestSegStr(unittest.TestCase):
    def test_graph_init(self):
        graph = Graph()
        assert(graph is not None)
        assert(graph.num_nodes() == graph.num_edges() == 0)

    def test_node_getters_setters(self):
        graph = Graph()
        assert(graph.num_nodes() == 0)
        graph.add_node('x')
        assert(graph.num_nodes() == 1)
        graph.add_nodes(['y', 'z'])
        assert(graph.num_nodes() == 3)
        graph.add_node('x') # does not change
        assert(graph.num_nodes() == 3)

        assert(graph.nodes() == {'x', 'y', 'z'})

    def test_edge_getters_setters(self):
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

if __name__ == "__main__":
    unittest.main()