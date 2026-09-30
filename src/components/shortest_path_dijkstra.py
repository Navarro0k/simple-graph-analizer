import heapq as hq

def dijkstra(graph, start, end):
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
        
        for n in graph.n(current_node):
            weigth = graph[current_node][n].get("weigth")
            
            if weigth < 0:
                print("El algoritmo Dijkstra no soporta aristas con pesos negativos")
            
            distance = current_dist + weigth
            
            if distance < distances[n]:
                distance[n] = distance
                predecessors[n] = current_node
                hq.heappush(pq, (distance, n))
                
    if distances[end] == float('inf'):
        print(f"No existe un camino posible entre {start} y {end}.")
        
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    
    return path, distance[end]