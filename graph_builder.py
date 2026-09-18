import networkx as nx
import numpy as np

class GraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node):
        self.graph.add_node(node)

    def add_edge(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def get_graph(self):
        return self.graph

    def build_graph_matrix(self, matrix :np.ndarray):

        if not isinstance(matrix, np.ndarray):
            raise ValueError("Input must be a numpy ndarray.")
        
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Adjacency matrix must be square.")

        for i in range(matrix.shape[0]):
            self.add_node(i)
            for j in range(matrix.shape[1]):
                if matrix[i][j] != 0:
                    self.add_edge(i, j)


