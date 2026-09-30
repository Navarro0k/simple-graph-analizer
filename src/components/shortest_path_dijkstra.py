import heapq as hq

def dijkstra(graph, start, end):
    for u, v, w in graph.edges(data="weight", default=1):
        if w < 0:
            raise ValueError("Dijkstra no soporta aristas con pesos negativos. "
                             "Usa Bellman-Ford.")

    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    predecessors = {node: None for node in graph.nodes}

    pq = [(0, start)]

    while pq:
        current_dist, current_node = hq.heappop(pq)

        if current_dist > distances[current_node]:
            continue
        if current_node == end:
            break

        for n in graph.neighbors(current_node):
            weight = graph[current_node][n].get("weight", 1)
            distance = current_dist + weight

            if distance < distances[n]:
                distances[n] = distance
                predecessors[n] = current_node
                hq.heappush(pq, (distance, n))

    if distances[end] == float('inf'):
        return [], float('inf')   

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()

    return path, distances[end]