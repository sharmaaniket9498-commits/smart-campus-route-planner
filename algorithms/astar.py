"""A* shortest path with an admissible minimum-edge-weight heuristic."""
import heapq
from collections import deque

def astar(graph, start, end, weight="distance"):
    if start not in graph or end not in graph:
        return None
    if start == end:
        return {"path": [start], "weight": 0.0, "visited_nodes": 1}
    edge_weights = [float(e.get(weight, 1)) for edges in graph.values() for e in edges.values()]
    min_weight = min((w for w in edge_weights if w >= 0), default=0.0)
    # Minimum edge weight times the minimum remaining hop count is admissible.
    def heuristic(node):
        q, seen = deque([(node, 0)]), {node}
        while q:
            current, hops = q.popleft()
            if current == end:
                return hops * min_weight
            for nxt in graph.get(current, {}):
                if nxt not in seen:
                    seen.add(nxt); q.append((nxt, hops + 1))
        return 0.0
    g = {n: float("inf") for n in graph}; parent = {}; g[start] = 0.0
    queue = [(heuristic(start), 0.0, start)]; visited = set()
    while queue:
        _, cost, node = heapq.heappop(queue)
        if node in visited: continue
        visited.add(node)
        if node == end: break
        for nxt, edge in graph[node].items():
            candidate = cost + float(edge.get(weight, 1))
            if candidate < g[nxt]:
                g[nxt] = candidate; parent[nxt] = node
                heapq.heappush(queue, (candidate + heuristic(nxt), candidate, nxt))
    if g[end] == float("inf"): return None
    path, node = [end], end
    while node != start:
        node = parent[node]; path.append(node)
    return {"path": list(reversed(path)), "weight": g[end], "visited_nodes": len(visited)}
