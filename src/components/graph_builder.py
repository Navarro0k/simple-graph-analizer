import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class GraphBuilder:
    def __init__(self, directed=False):
        self.directed = directed
        self.graph = nx.DiGraph() if directed else nx.Graph()

    def add_node(self, node):
        self.graph.add_node(node)

    def add_edge(self, node1, node2, weight=1):
        self.graph.add_edge(node1, node2, weight=weight)

    def get_nodes(self):
        return list(self.graph.nodes)

    def get_edges(self):
        return list(self.graph.edges(data="weight"))

    def get_graph(self):
        return self.graph

    def build_graph_matrix(self, matrix: np.ndarray):
        if not isinstance(matrix, np.ndarray):
            raise ValueError("Input must be a numpy ndarray.")
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Adjacency matrix must be square.")
        if not self.directed and not np.allclose(matrix, matrix.T):
            raise ValueError(
                "Un grafo no dirigido necesita una matriz simétrica "
                "(el valor [i][j] debe ser igual a [j][i])."
            )

        self.graph = nx.from_numpy_array(
            matrix,
            create_using=nx.DiGraph if self.directed else nx.Graph,
        )

    def math_representation(self):
        nodes = sorted(self.graph.nodes)
        V = "{" + ", ".join(map(str, nodes)) + "}"

        if self.directed:
            edges = sorted(self.graph.edges(data="weight"))
            U = "{" + ", ".join(f"({u},{v})" for u, v, _ in edges) + "}"
            W = ", ".join(f"w({u},{v})={w}" for u, v, w in edges)
        else:
            edges = sorted((min(u, v), max(u, v), w)
                           for u, v, w in self.graph.edges(data="weight"))
            U = "{" + ", ".join(f"{{{u},{v}}}" for u, v, _ in edges) + "}"
            W = ", ".join(f"w({u},{v})={w}" for u, v, w in edges)

        return (f"G = (V, U)\n"
                f"V = {V}\n"
                f"U = {U}\n"
                f"Pesos: {W if W else '—'}")

    def plot_graph(self, path=None):
        if self.graph.number_of_nodes() == 0:
            raise ValueError("El grafo está vacío. Primero debes construirlo con una matriz.")

        fig = plt.figure("Grafo", figsize=(8, 7))
        fig.clf()
        ax = fig.add_subplot(111)

        pos = nx.spring_layout(self.graph, seed=42)  
        nx.draw_networkx(self.graph, pos, ax=ax, node_color="#9ecae1",
                         arrows=self.directed)

        labels = {(u, v): w for u, v, w in self.graph.edges(data="weight")}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, ax=ax)

        if path and len(path) > 1:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(self.graph, pos, nodelist=path,
                                   node_color="#ff7f0e", ax=ax)
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges,
                                   edge_color="red", width=3, ax=ax,
                                   arrows=self.directed)

        ax.set_title(self.math_representation(), fontsize=9, loc="left",
                     family="monospace")
        ax.axis("off")
        fig.tight_layout()
        plt.show(block=False)   
        fig.canvas.draw_idle()