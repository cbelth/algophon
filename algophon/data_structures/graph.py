from typing import Hashable, Iterable

class Graph:
    '''
    A Graph class.

    Internally, the nodes are stored as a dict mapping each Hashable to a Node object.
    '''
    def __init__(self) -> object:
        self._nodes = dict()
        self._edges = set()

    def nodes(self) -> set: # getter
        '''
        :return: a set of the nodes in the graph
        '''
        return set(self._nodes.keys())
    
    def edges(self) -> set: # getter
        '''
        :return: a set of the edges in the graph
        '''
        return self._edges

    def add_node(self, node: Hashable) -> None:
        '''
        :node: a Hashable object

        :return: None
        '''
        if node not in self._nodes:
            self._nodes[node] = Node()

    def add_edge(self, x: Hashable, y: Hashable) -> None:
        '''
        :x: a Hashable object
        :y: a Hashable object

        :return: None
        '''
        self.add_node(x)
        self.add_node(y)
        self._edges((x, y))

    def add_nodes(self, nodes: Iterable) -> None:
        '''

        :return: None
        '''
        for node in nodes:
            self.add_node(node=node)

    def add_edges(self, edges: Iterable) -> None:
        '''

        :return: None
        '''
        for edge in edges:
            self.add_edge(edge)

class Node:
    '''
    A Node class.
    '''
    def __init__(self) -> object:
        pass # TODO
