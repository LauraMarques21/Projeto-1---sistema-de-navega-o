"""
grafo.py
Implementação de grafo por lista de adjacência.
- BFS (Busca em Largura)
- DFS (Busca em Profundidade)
- Dijkstra (caminho mínimo com heap)
Complexidades:
- BFS/DFS: O(V + E)
- Dijkstra: O(E log V) (usando heap)
"""

from collections import deque, defaultdict
import heapq
from typing import Dict, List, Tuple, Any, Set


class Graph:
    def __init__(self, directed: bool = False):
        # adj[u] = list of (v, weight)
        self.adj: Dict[Any, List[Tuple[Any, float]]] = defaultdict(list)
        self.directed = directed

    def add_vertex(self, v: Any):
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u: Any, v: Any, weight: float = 1.0):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def vertices(self) -> List[Any]:
        return list(self.adj.keys())

    def bfs(self, start) -> List[Any]:
        """Retorna ordem de visita BFS a partir de start."""
        visited: Set[Any] = set()
        order = []
        q = deque()
        q.append(start)
        visited.add(start)
        while q:
            u = q.popleft()
            order.append(u)
            for v, _ in self.adj.get(u, []):
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        return order

    def dfs(self, start) -> List[Any]:
        """Retorna ordem de visita DFS (iterativa)."""
        visited = set()
        order = []
        stack = [start]
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            order.append(u)
            # empilhar vizinhos (inverso para ordem natural)
            neighbors = [v for v, _ in self.adj.get(u, [])]
            for v in reversed(neighbors):
                if v not in visited:
                    stack.append(v)
        return order

    def dijkstra(self, source) -> Tuple[Dict[Any, float], Dict[Any, Any]]:
        """
        Retorna (dist, prev) onde:
        - dist[v] = distância mínima de source a v
        - prev[v] = predecessor de v no caminho mínimo
        Complexidade: O(E log V)
        """
        dist = {v: float('inf') for v in self.adj}
        prev = {v: None for v in self.adj}
        if source not in self.adj:
            return dist, prev
        dist[source] = 0
        heap = [(0, source)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in self.adj[u]:
                alt = dist[u] + w
                if alt < dist.get(v, float('inf')):
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(heap, (alt, v))
                    # se v não estava presente como chave, garantimos integridade
                    if v not in dist:
                        dist[v] = alt
        return dist, prev

    def shortest_path(self, source, target) -> Tuple[float, List[Any]]:
        """Reconstroi caminho mínimo de source a target (usando dijkstra)."""
        dist, prev = self.dijkstra(source)
        if dist.get(target, float('inf')) == float('inf'):
            return float('inf'), []
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = prev.get(cur)
        path.reverse()
        return dist[target], path
