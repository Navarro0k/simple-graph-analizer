import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from components.shortest_path_bellman import bellman
from components.shortest_path_dijkstra import dijkstra
from components.graph_builder import GraphBuilder

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")  

class GraphApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generador y Analizador de Grafos")
        self.geometry("750x760")
        
        self.builder = None
        self.matrix_entries = []

        ctk.CTkLabel(self, text="Analizador de Grafos", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(15, 5))

        config_frame = ctk.CTkFrame(self)
        config_frame.pack(pady=10, padx=20, fill="x")

        self.directed_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(config_frame, text="Grafo Dirigido", variable=self.directed_var, command=self.al_cambiar_dirigido).pack(side="left", padx=20, pady=15)
        
        ctk.CTkLabel(config_frame, text="Cantidad de nodos:").pack(side="left", padx=(10, 5))
        
        self.n_nodes_menu = ctk.CTkOptionMenu(config_frame, values=[str(i) for i in range(1, 16)], width=70)
        self.n_nodes_menu.set("4")
        self.n_nodes_menu.pack(side="left", padx=5)

        ctk.CTkButton(config_frame, text="Generar Matriz", command=self.generar_matriz_gui).pack(side="right", padx=20)

        self.matrix_container = ctk.CTkScrollableFrame(self, label_text="Matriz de Adyacencia")
        self.matrix_container.pack(pady=10, padx=20, fill="both", expand=True)

        self.matrix_frame = ctk.CTkFrame(self.matrix_container, fg_color="transparent")
        self.matrix_frame.pack(pady=10)

        ctk.CTkButton(self, text="Construir Grafo Base", command=self.procesar_y_graficar, fg_color="#2FA572", hover_color="#1F7A52").pack(pady=5)

        self.lbl_math = ctk.CTkLabel(self, text="G = (V, U)", justify="left", anchor="w",
                                     font=ctk.CTkFont(family="Consolas", size=13), wraplength=690)
        self.lbl_math.pack(pady=(0, 5), padx=25, fill="x")

        algo_frame = ctk.CTkFrame(self)
        algo_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(algo_frame, text="Inicio:").grid(row=0, column=0, padx=5, pady=15)
        self.cb_start = ctk.CTkOptionMenu(algo_frame, values=["-"], width=70)
        self.cb_start.grid(row=0, column=1, padx=5)

        ctk.CTkLabel(algo_frame, text="Destino:").grid(row=0, column=2, padx=(15, 5))
        self.cb_end = ctk.CTkOptionMenu(algo_frame, values=["-"], width=70)
        self.cb_end.grid(row=0, column=3, padx=5)

        ctk.CTkLabel(algo_frame, text="Algoritmo:").grid(row=0, column=4, padx=(15, 5))
        self.cb_algo = ctk.CTkOptionMenu(algo_frame, values=["Dijkstra", "Bellman-Ford"], width=130)
        self.cb_algo.set("Dijkstra")
        self.cb_algo.grid(row=0, column=5, padx=5)

        ctk.CTkButton(algo_frame, text="Calcular y Graficar", command=self.calcular_camino).grid(row=0, column=6, padx=20)

        self.lbl_result = ctk.CTkLabel(self, text="Esperando construcción de grafo...", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1E90FF")
        self.lbl_result.pack(pady=(0, 15))

        self.generar_matriz_gui()

    def generar_matriz_gui(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
            
        n = int(self.n_nodes_menu.get())

        self.matrix_entries = []
        for i in range(n):
            fila = []
            ctk.CTkLabel(self.matrix_frame, text=f"N{i}", font=ctk.CTkFont(weight="bold")).grid(row=i+1, column=0, padx=10, pady=2)
            ctk.CTkLabel(self.matrix_frame, text=f"N{i}", font=ctk.CTkFont(weight="bold")).grid(row=0, column=i+1, padx=2, pady=5)
            
            for j in range(n):
                entry = ctk.CTkEntry(self.matrix_frame, width=45, justify="center")
                entry.insert(0, "0") 
                entry.grid(row=i+1, column=j+1, padx=3, pady=3)
                entry.bind("<KeyRelease>", lambda e, i=i, j=j: self.sincronizar_simetria(i, j))
                fila.append(entry)
            self.matrix_entries.append(fila)
            
        self.cb_start.configure(values=["-"])
        self.cb_start.set("-")
        self.cb_end.configure(values=["-"])
        self.cb_end.set("-")
        self.builder = None
        self.lbl_math.configure(text="G = (V, U)")

    def sincronizar_simetria(self, i, j):
        if self.directed_var.get() or i == j:
            return
        espejo = self.matrix_entries[j][i]
        espejo.delete(0, "end")
        espejo.insert(0, self.matrix_entries[i][j].get())

    def al_cambiar_dirigido(self):
        if self.directed_var.get():
            return
        n = len(self.matrix_entries)
        for i in range(n):
            for j in range(i + 1, n):
                self.sincronizar_simetria(i, j)

    def procesar_y_graficar(self):
        if not self.matrix_entries:
            messagebox.showwarning("Advertencia", "Primero genera la matriz.")
            return

        n = len(self.matrix_entries)
        matriz_numpy = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                valor = self.matrix_entries[i][j].get().strip()
                if valor == "":
                    matriz_numpy[i, j] = 0
                else:
                    try:
                        matriz_numpy[i, j] = float(valor)
                    except ValueError:
                        messagebox.showerror("Error", f"Ingresa un número válido en la fila {i}, columna {j}.")
                        return

        try:
            self.builder = GraphBuilder(directed=self.directed_var.get())
            self.builder.build_graph_matrix(matriz_numpy)
            
            nodos = [str(node) for node in self.builder.get_nodes()] 
            if nodos:
                self.cb_start.configure(values=nodos)
                self.cb_end.configure(values=nodos)
                self.cb_start.set(nodos[0])
                self.cb_end.set(nodos[-1])
            
            self.lbl_math.configure(text=self.builder.math_representation())
            self.lbl_result.configure(text="Grafo construido exitosamente.", text_color="#2FA572")
            self.builder.plot_graph()
        except Exception as e:
            messagebox.showerror("Error al graficar", str(e))

    def calcular_camino(self):
        if not self.builder:
            messagebox.showwarning("Advertencia", "Primero debes construir el grafo base.")
            return
            
        if self.cb_start.get() == "-" or self.cb_end.get() == "-":
            messagebox.showwarning("Advertencia", "Selecciona nodos válidos para inicio y destino.")
            return

        start = int(self.cb_start.get())
        end = int(self.cb_end.get())
        algoritmo = self.cb_algo.get()
        grafo = self.builder.get_graph()

        try:
            if algoritmo == "Dijkstra":
                path, distance = dijkstra(grafo, start, end)
            else:
                path, distance = bellman(grafo, start, end, self.builder.directed)

            if not path or distance == float('inf'):
                self.lbl_result.configure(text=f"No hay camino entre N{start} y N{end}.", text_color="#FF4500")
            else:
                self.lbl_result.configure(text=f"Ruta: {' -> '.join(map(str, path))} | Costo: {distance:g}", text_color="#2E7A01")
                self.builder.plot_graph(path=path)
                
        except Exception as e:
            messagebox.showerror("Error de Algoritmo", str(e))

if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()