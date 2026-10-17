"""Breadth-first traversal and unweighted shortest-hop path."""
from collections import deque

def bfs(graph, start, end=None):
    if start not in graph: return None if end is not None else []
    queue, seen, order, parent = deque([start]), {start}, [], {}
    while queue:
        node = queue.popleft(); order.append(node)
        if node == end: break
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor); parent[neighbor] = node; queue.append(neighbor)
    if end is None: return order
    if end not in seen: return None
    path, node = [end], end
    while node != start: node = parent[node]; path.append(node)
    return {"path": list(reversed(path)), "visited_nodes": len(order), "weight": len(path)-1}
