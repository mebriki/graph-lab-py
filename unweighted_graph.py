""" Unweighted Graph Module.
    Graphs are represented as a dictionary,
    each node 'n' is a key which contain 
    a list of nodes that are reachable from
    that node 'n'."""

from collections import deque

class UGraph(object):
    """ Unweighted Graph implementation """
    def __init__(self, graph):
        self.graph = graph
        self.is_cyclic = None
        
    def isCyclic(self):
        """Check whether a directed graph contains a cycle."""
        visited = set()
        in_stack = set()

        def dfs(node):
            visited.add(node)
            in_stack.add(node)

            for neigh in self.graph.get(node, []):
                if neigh not in visited:
                    if dfs(neigh):
                        return True
                elif neigh in in_stack:
                    return True

            in_stack.remove(node)
            return False

        for node in self.graph:
            if node not in visited and dfs(node):
                self.is_cyclic = True
                return True

        self.is_cyclic = False
        return False
                        
    def setGraph(self, graph):
        self.graph = graph
        self.is_cyclic = None
        
    def bestPath(self, n_from, n_to):
        """Return the shortest path between two nodes using BFS."""
        if n_from not in self.graph or n_to not in self.graph:
            return []

        queue = deque([n_from])
        parents = {n_from: None}

        while queue:
            node = queue.popleft()
            if node == n_to:
                break

            for neigh in self.graph.get(node, []):
                if neigh not in parents:
                    parents[neigh] = node
                    queue.append(neigh)

        if n_to not in parents:
            return []

        path = []
        cursor = n_to
        while cursor is not None:
            path.append(cursor)
            cursor = parents[cursor]

        return path[::-1]
        
    def bfs(self, n_from):
    
        nodes = {i:False for i in self.graph.keys()} # node:visited?
        nodes[n_from] = True
        fifo = [[n_from,],]
        level = 0
        n_by_level = [{n_from: None}] # (node, parent)
        all_visited = False
        
        while not all_visited :
            all_visited = True
            l_node = fifo[level]
            l = {}
            
            for node in l_node:
                for n in self.graph[node]:
                    if not nodes[n]: #not visited
                        all_visited = False
                        nodes[n] = True
                        l[n] = node

            if len(l) != 0:
                fifo.append([i for i in l.keys()])              
                level += 1
                n_by_level.append(l)

        return n_by_level
        
    def findPath(self, n_from, n_to):
      
        paths = []        
        nodes = {i:False for i in self.graph.keys()}
        nodes[n_from] = True
        
        for n in self.graph[n_from]:
            if not nodes[n]:
                path = [n_from]
                pos = self.dfs(self.graph, nodes, n)
                
                for p in pos:
                    if n_to in p:
                        paths.append(path + p[:p.index(n_to)+1])
                        return paths
        return []                        
                        
    @staticmethod
    def dfs(graph, states, node):
        states[node] = True
        paths = []
        
        for n in graph[node]:
            if not states[n]:
                path = [node]
                pos = UGraph.dfs(graph, states, n)
                
                for p in pos:
                    paths.append(path + p) 
                                       
        if len(paths) == 0:
            return [[node,],]
        else:
            return paths

                
            

        
    
        
