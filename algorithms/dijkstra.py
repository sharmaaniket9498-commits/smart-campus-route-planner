"""Dijkstra shortest path for non-negative edge weights."""
import heapq

def dijkstra(graph, start, end, weight="distance"):
    if start not in graph or end not in graph: return None
    if start == end: return {"path": [start], "weight": 0.0, "visited_nodes": 1}
    distances = {node: float("inf") for node in graph}; previous = {}; distances[start] = 0
    queue = [(0, start)]; visited = set()
    while queue:
        current_cost, node = heapq.heappop(queue)
        if current_cost != distances[node] or node in visited: continue
        visited.add(node)
        if node == end: break
        for neighbor, edge in graph[node].items():
            candidate = current_cost + float(edge.get(weight, 1))
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate; previous[neighbor] = node
                heapq.heappush(queue, (candidate, neighbor))
    if distances[end] == float("inf"): return None
    path, node = [end], end
    while node != start:
        if node not in previous: return None
        node = previous[node]; path.append(node)
    return {"path": list(reversed(path)), "weight": distances[end], "visited_nodes": len(visited)}
