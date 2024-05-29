from typing import Hashable, Iterable, Union, Generator

class Graph:
    '''
    A Graph class.

    Internally, the nodes are stored as a dict mapping each Hashable to a Node object.
    '''
    def __init__(self, directed=False) -> object:
        '''
        :directed: if True, the graph is a directed graph (otherwise undirected)
        '''
        self._nodes = dict()
        self._edges = set()
        self._neighbors = dict()
        self.directed = directed

    def add_node(self, node: Hashable) -> None:
        '''
        :node: a Hashable object

        :return: None
        '''
        if node not in self._nodes:
            self._nodes[node] = Node(name=node, graph=self)
            self._neighbors[self._nodes[node]] = set()

    def add_edge(self, x: Union[tuple, Hashable], y: Union[None, Hashable]=None) -> None:
        '''
        :x: a Hashable object or tuple (x, y)
        :y: a Hashable object or none

        :return: None
        '''
        if isinstance(x, tuple) and len(x) == 2 and y is None:
            x, y = x
        # make sure x and y are in the graph's nodes
        self.add_node(x)
        self.add_node(y)
        x, y = self._nodes[x], self._nodes[y] # get the Node object versions
        if self.directed or (y, x) not in self._edges: # if directed, add x -> y ; if undirected and y - x not in edges, add x - y
            self._edges.add((x, y))
            self._neighbors[x].add(y)
        if not self.directed: # add y - x neighbor if undirected
            self._neighbors[y].add(x)

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
    
    def __str__(self) -> str:
        return f'Graph (n = {self.num_nodes()}, m = {self.num_edges()})'
    
    def neighbors(self, node: object):
        return sorted(self._neighbors[node], key=lambda neigh: f'{neigh}')

    def _search(self, start_node: object, typ: str='bfs') -> Generator:
        '''
        Implements a breadth/depth-first search over the graph. Ties in order are broken by str(node) lexiographic order.

        :start_node: a node to start the search at
        :typ: either a "bfs" (breadth-first search) or "dfs" (depth-first search)

        :return: a Generator that yields the nodes in :typ: order starting at the :start_node:
        '''
        if typ not in {'bfs', 'dfs'}:
            raise ValueError(f'Search Type "{typ}" is not implemented.')
        start_node = self._nodes[start_node]
        visited = set()
        frontier = [start_node]
        while len(frontier) > 0:
            node = frontier.pop(0 if typ == 'bfs' else -1) # pop in bfs=FIFO=0/dfs=LIFO=-1 order
            visited.add(node) # mark the node as visited
            for neigh in node.neighbors() if typ == 'bfs' else reversed(node.neighbors()):
                if neigh not in visited:
                    frontier.append(neigh)
            yield node

    def bfs(self, start_node) -> Generator:
        '''
        :start_node: a node to start the search at

        :return: a Generator that yields the nodes in bredth-first order starting at the :start_node:
        '''
        return self._search(start_node=start_node, typ='bfs')
    
    def dfs(self, start_node) -> Generator:
        '''
        :start_node: a node to start the search at

        :return: a Generator that yields the nodes in depth-first order starting at the :start_node:
        '''
        return self._search(start_node=start_node, typ='dfs')

class Node:
    '''
    A Node class.
    '''
    def __init__(self, name: Hashable, graph: Graph) -> object:
        '''
        '''
        self.name = name
        self.graph = graph

    def __str__(self) -> str:
        return f'{self.name}'
    
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
    
    def neighbors(self):
        return self.graph.neighbors(self)
