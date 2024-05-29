from typing import Hashable, Iterable, Union

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

    def num_nodes(self) -> int:
        '''
        :return: the number of nodes in the graph
        '''
        return len(self._nodes)
    
    def num_edges(self) -> int:
        '''
        :return: the number of edges in the graph
        '''
        return len(self._edges)

    def add_node(self, node: Hashable) -> None:
        '''
        :node: a Hashable object

        :return: None
        '''
        if node not in self._nodes:
            self._nodes[node] = Node(name=node)

    def add_edge(self, x: Union[tuple, Hashable], y: Union[None, Hashable]=None) -> None:
        '''
        :x: a Hashable object or tuple (x, y)
        :y: a Hashable object or none

        :return: None
        '''
        if isinstance(x, tuple) and len(x) == 2 and y is None:
            x, y = x
        self.add_node(x)
        self.add_node(y)
        self._edges.add((x, y))

    def add_nodes(self, nodes: Iterable) -> None:
        '''
        :nodes: an Iterable of objects to add as nodes

        :return: None
        '''
        for node in nodes:
            self.add_node(node=node)

    def add_edges(self, edges: Iterable[tuple]) -> None:
        '''
        :edges: an Iterable of tuples to add as edges
        
        :return: None
        '''
        for edge in edges:
            self.add_edge(edge)

class Node:
    '''
    A Node class.
    '''
    def __init__(self, name: Hashable) -> object:
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: object) -> bool:
        '''
        :other: an object to compare to :self:

        :return: True if :other: == :self:, False otherwise
        '''
        return self.__hash__() == other.__hash__()
        
    def __neq__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def __hash__(self) -> int:
        return hash(self.name)
