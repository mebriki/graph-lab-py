""" Weighted Graph Module.
    Graphs are represented as a dictionary,
    each node 'n' is a key which contain
    a list of nodes (node_value, weight) that are reachable from
    that node 'n'."""
from copy import deepcopy as dc
import heapq

class WGraph(object):
    """ Weighted Graph implementation """
    def __init__(self, graph):
        self.graph = graph
        self.is_cyclic = None

    def setGraph(self, graph):
        self.graph = graph
        self.is_cyclic = None

    def unoriented(self):
        """Create an undirected version of the graph."""
        unoriented_g = {k: list(v) for k, v in dc(self.graph).items()}
        for src, childs in self.graph.items():
            for dst, weight in childs:
                if dst not in unoriented_g:
                    unoriented_g[dst] = []
                if not any(n == src for n, _ in unoriented_g[dst]):
                    unoriented_g[dst].append((src, weight))
        return unoriented_g

    def isCyclic(self):
        """Check if the undirected view of the graph has any cycle."""
        unoriented_g = self.unoriented()
        visited = set()

        for start in unoriented_g:
            if start in visited:
                continue

            stack = [(start, None)]
            while stack:
                node, parent = stack.pop()
                if node in visited:
                    self.is_cyclic = True
                    return True

                visited.add(node)
                for neigh, _ in unoriented_g.get(node, []):
                    if neigh != parent:
                        stack.append((neigh, node))

        self.is_cyclic = False
        return False

    def kruskal(self):
        """Compute a minimum spanning tree using Kruskal (undirected)."""
        # Keep a single undirected edge per node pair with minimum weight.
        best = {}
        for src, childs in self.graph.items():
            for dst, weight in childs:
                if src == dst:
                    continue
                edge_key = tuple(sorted((src, dst)))
                if edge_key not in best or weight < best[edge_key]:
                    best[edge_key] = weight

        edges = sorted(
            [(u, v, w) for (u, v), w in best.items()],
            key=lambda x: x[2]
        )

        parent = {node: node for node in self.graph}
        rank = {node: 0 for node in self.graph}

        def find(node):
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        def union(a, b):
            root_a = find(a)
            root_b = find(b)
            if root_a == root_b:
                return False
            if rank[root_a] < rank[root_b]:
                parent[root_a] = root_b
            elif rank[root_a] > rank[root_b]:
                parent[root_b] = root_a
            else:
                parent[root_b] = root_a
                rank[root_a] += 1
            return True

        mst = {node: [] for node in self.graph}
        added = 0
        for src, dst, weight in edges:
            if union(src, dst):
                mst[src].append((dst, weight))
                mst[dst].append((src, weight))
                added += 1
                if added == len(self.graph) - 1:
                    break

        return WGraph(mst)

    def prim(self):
        """Compute a minimum spanning tree using Prim (undirected)."""
        unoriented_g = self.unoriented()
        if not unoriented_g:
            return WGraph({})

        start = next(iter(unoriented_g))
        visited = {start}
        heap = []
        for neigh, weight in unoriented_g[start]:
            heapq.heappush(heap, (weight, start, neigh))

        mst = {node: [] for node in unoriented_g}
        while heap and len(visited) < len(unoriented_g):
            weight, src, dst = heapq.heappop(heap)
            if dst in visited:
                continue

            visited.add(dst)
            mst[src].append((dst, weight))
            mst[dst].append((src, weight))

            for next_node, next_weight in unoriented_g[dst]:
                if next_node not in visited:
                    heapq.heappush(heap, (next_weight, dst, next_node))

        if len(visited) != len(unoriented_g):
            raise Exception("Graph is disconnected; Prim requires a connected graph")

        return WGraph(mst)

    def dijkstra(self, root):
        """Return shortest paths from root using Dijkstra's algorithm."""
        if root not in self.graph:
            raise KeyError("Unknown root node")

        for childs in self.graph.values():
            for _, weight in childs:
                if weight < 0:
                    raise Exception("Negative weight")

        dist = {node: float("inf") for node in self.graph}
        prev = {root: None}
        dist[root] = 0.0
        visited = set()
        heap = [(0.0, root)]

        while heap:
            current_dist, node = heapq.heappop(heap)
            if node in visited:
                continue
            visited.add(node)

            for neigh, weight in self.graph.get(node, []):
                new_dist = current_dist + weight
                if new_dist < dist.get(neigh, float("inf")):
                    dist[neigh] = new_dist
                    prev[neigh] = node
                    heapq.heappush(heap, (new_dist, neigh))

        result = {}
        for node, node_dist in dist.items():
            if node_dist == float("inf"):
                continue

            path = []
            cursor = node
            while cursor is not None:
                path.append(cursor)
                cursor = prev.get(cursor)

            result[node] = (path[::-1], node_dist)

        return result

    def bellman_ford(self, root):
        """Return shortest paths from root using Bellman-Ford."""
        if root not in self.graph:
            raise KeyError("Unknown root node")

        nodes = list(self.graph.keys())
        dist = {node: float("inf") for node in nodes}
        prev = {root: None}
        dist[root] = 0.0

        edges = []
        for src, childs in self.graph.items():
            for dst, weight in childs:
                edges.append((src, dst, weight))

        for _ in range(len(nodes) - 1):
            updated = False
            for src, dst, weight in edges:
                if dist[src] != float("inf") and dist[src] + weight < dist.get(dst, float("inf")):
                    dist[dst] = dist[src] + weight
                    prev[dst] = src
                    updated = True
            if not updated:
                break

        for src, dst, weight in edges:
            if dist[src] != float("inf") and dist[src] + weight < dist.get(dst, float("inf")):
                raise Exception("Negative cycle detected")

        result = {}
        for node, node_dist in dist.items():
            if node_dist == float("inf"):
                continue

            path = []
            cursor = node
            while cursor is not None:
                path.append(cursor)
                cursor = prev.get(cursor)

            result[node] = (path[::-1], node_dist)

        return result
