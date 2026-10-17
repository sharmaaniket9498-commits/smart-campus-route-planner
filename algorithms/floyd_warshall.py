"""Floyd-Warshall all-pairs shortest paths."""
def floyd_warshall(graph, weight="distance"):
    nodes = list(graph)
    dist = {u: {v: (0 if u == v else float("inf")) for v in nodes} for u in nodes}
    for u in graph:
        for v, edge in graph[u].items():
            dist[u][v] = min(dist[u][v], float(edge.get(weight, 1)))
    for k in nodes:
        for i in nodes:
            for j in nodes:
                via = dist[i][k] + dist[k][j]
                if via < dist[i][j]:
                    dist[i][j] = via
    return dist
