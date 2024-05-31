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

    def nodes(self, sort_key=None, reverse=False) -> set: # getter
        '''
        :sort_key: (Optional; default None) a function to sort the nodes according to
        :reverse: (Optional; default False) determines whether nodes are sorted in ascending (False) or descending (True) order
            - Only used if :sort_key: is provided

        :return: a set of the nodes in the graph (or sorted list of :sort_key: is not None)
        '''
        if sort_key is not None:
            return sorted(self._nodes.keys(), reverse=reverse, key=sort_key)
        return set(self._nodes.keys())
    
    def edges(self, sort_key=None, reverse=False) -> Union[set, list]: # getter
        '''
        :sort_key: (Optional; default None) a function to sort the edges according to
        :reverse: (Optional; default False) determines whether edges are sorted in ascending (False) or descending (True) order
            - Only used if :sort_key: is provided

        :return: a set of the edges in the graph (or sorted list if :sort_key: is not None)
        '''
        if sort_key is not None:
            return sorted(self._edges, reverse=reverse, key=sort_key)
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
    
    def neighbors(self, node: object) -> list:
        '''
        :node: a node in the graph
        
        :return: a list of the neighbors of :node: sorted lexicographically
        '''
        return sorted(self._neighbors[node], key=lambda neigh: f'{neigh}')

    def _search(self, start_node: object, typ: str='bfs') -> Generator:
        '''
        Implements a breadth/depth-first search over the graph. Ties in order are broken by str(node) lexicographic order.

        :start_node: a node to start the search at
        :typ: either a "bfs" (breadth-first search) or "dfs" (depth-first search)

        :return: a Generator that yields the nodes in :typ: order starting at the :start_node:
        '''
        if typ not in {'bfs', 'dfs'}:
            raise ValueError(f'Search Type "{typ}" is not implemented.')
        if start_node is None: # if no start node, choose lexicographically first node
            start_node = self.nodes(sort_key=lambda node: f'{node}')[0]
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
            
            if len(frontier) == 0: # see if there are any other components to search
                diff = self.nodes().difference(visited)
                if len(diff) > 0: # if visited (hence unreachable) nodes, add the lexiocographically first to the frontier
                    frontier = [self._nodes[sorted(diff, key=lambda node: f'{node}')[0]]]

    def bfs(self, start_node=None) -> Generator:
        '''
        :start_node: (Optional; default None) a node to start the search at
            - If None, starts at lexicographically first node

        :return: a Generator that yields the nodes in bredth-first order starting at the :start_node:
        '''
        return self._search(start_node=start_node, typ='bfs')
    
    def dfs(self, start_node=None) -> Generator:
        '''
        :start_node: (Optional; default None) a node to start the search at
            - If None, starts at lexicographically first node

        :return: a Generator that yields the nodes in depth-first order starting at the :start_node:
        '''
        return self._search(start_node=start_node, typ='dfs')
    
    def _acyclic(self, node=None, visited: set=None, stack: set=None) -> bool:
        '''
        Checks whether a graph is acyclic using a recursive DFS.

        :return: True if the graph is acyclic, False if not
        '''
        if not self.directed:
            raise NotImplementedError('_acyclic() is not implemented for undirected graphs.')
        if self.num_edges() == 0: # a graph with no edges is trivially acyclic
            return True  
        # make sure sets are fresh references
        visited = set() if visited is None else visited
        stack = set() if stack is None else stack
        # if no node, see if there are other components to search
        if node is None:
            diff = self.nodes().difference(visited)
            if len(diff) == 0: # if we made it here, there are no cycles
                return True
            node = self._nodes[sorted(diff, key=lambda node: f'{node}')[0]]
        
        if node in stack: # if node is in the stack, we have a cycle
            return False
        if node in visited: # do not revist nodes
            return True
        # update sets
        visited.add(node)
        stack.add(node)
        for neigh in node.neighbors(): # recurse over neighbors
            if not self._acyclic(node=neigh, visited=visited, stack=stack):
                return False
        stack.discard(node) # remove the visiting node from the stack

        if len(stack) == 0: # recurse to make sure there is nothing else to traverse
            return self._acyclic(visited=visited)
        return True # if we made it here, there are no cycles

    def is_dag(self) -> bool:
        '''
        Checks whether a graph is a directed, acyclic graph (DAG)

        :return: True if :self: is a DAG, False if not
        '''
        return self.directed and self._acyclic()
    
    def topological_sort(self) -> list:
        '''
        :return: a toplogical sort of the graphs nodes
        '''
        if not self.is_dag():
            raise ValueError('The graph is not a DAG, and thus cannot be topologically sorted.')

        stack = set()
        def _recursive_topological_sort(node=None, _sorted: list=None, visited: set=None) -> list:
            # make sure sets/lists are fresh references
            _sorted = list() if _sorted is None else _sorted
            visited = set() if visited is None else visited
            # if no node, compute the next node to visit
            if node is None:
                diff = self.nodes().difference(visited)
                if len(diff) == 0: # if no remaining nodes, return _sorted
                    return _sorted
                node = self._nodes[sorted(diff, key=lambda node: f'{node}', reverse=True)[0]]

            if node in visited: # node already visited
                return _sorted
            stack.add(node) # add node to stack
            visited.add(node) # mark node as visited
            for neigh in reversed(node.neighbors()):
                _recursive_topological_sort(node=neigh, _sorted=_sorted, visited=visited)
            _sorted.insert(0, node)
            stack.discard(node) # remove node from stack
            if len(stack) == 0 and len(visited) != self.num_nodes(): # if there is nothing on the stack, recurse on remaining nodes
                return _recursive_topological_sort(_sorted=_sorted, visited=visited)
            return _sorted

        # compute topological sort recursively
        return list(node.name for node in _recursive_topological_sort())

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
    
    def neighbors(self) -> set:
        '''
        :return: a list of the neighbors of :node: sorted lexicographically
        '''
        return self.graph.neighbors(self)
