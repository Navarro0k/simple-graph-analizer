import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class GraphBuilder:
    def __init__(self, directed=False):
        self.directed = directed
        self.graph = nx.DiGraph() if directed else nx.Graph()

    def add_node(self, node):
        self.graph.add_node(node)

    def add_edge(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def get_nodes(self):
        return list(self.graph.nodes)

    def get_edges(self):
        return list(self.graph.edges(data="weight"))

    def get_graph(self):
        return self.graph

    def build_graph_matrix(self, matrix :np.ndarray):

        if not isinstance(matrix, np.ndarray):
            raise ValueError("Input must be a numpy ndarray.")
        
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Adjacency matrix must be square.")
        
        self.graph.clear()

        self.graph = nx.from_numpy_array(
            matrix, 
            create_using=nx.DiGraph if self.directed else nx.Graph
        )

    def plot_graph(self):
        if self.graph.number_of_nodes() == 0:
            raise ValueError("El grafo está vacío. Primero debes construirlo con una matriz.")
            
        #Limpiar Plotter
        plt.clf()
        
        pos = nx.spring_layout(self.graph)
        
        nx.draw_networkx(self.graph, pos)
        
        # Dibujo por defecto de los pesos
        pesos = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=pesos)
        
        plt.show()