import networkx as nx
def bellman(graph: nx.Graph | nx.DiGraph, start, end, directed=False):
    
    distances = {} #Distancias a iterar
    predecessors = {} #Nodos Predecesores
    num_nodos = len(graph.nodes)

    #Inicializacion
    for node in graph.nodes:
        if node == start:
            distances[node] = 0 #El primer elemento se asigna 1 cero
        else:
            distances[node] = float('inf') #Infinito a los demas

        predecessors[node] = None
  

    #Bellman-Ford (V - 1 iteraciones)
    for _ in range(num_nodos - 1):
        for u, v, data in graph.edges(data=True):

            peso = data.get('weight', 1) 
            
            if distances[u] + peso < distances[v]:
                distances[v] = distances[u] + peso
                predecessors[v] = u

            if not directed:
                if distances[v] + peso < distances[u]:
                    distances[u] = distances[v] + peso
                    predecessors[u] = v

    if distances[end] == float('inf'):
        return [], float('inf')

    #Devolver camino optimo
    path = []
    current_node = end

    while current_node is not None:
        path.append(current_node)
        current_node = predecessors[current_node]

    path.reverse()

    return path, distances[end]
            
    