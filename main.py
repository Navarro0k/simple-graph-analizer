from graph_builder import GraphBuilder
import tkinter as tk
from tkinter import messagebox
import numpy as np

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Grafos")
        
        self.directed_var = tk.BooleanVar(value=False)
        self.matrix_entries = []

        # Frame superior
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10, padx=10)

        tk.Checkbutton(control_frame, text="Grafo Dirigido", variable=self.directed_var).grid(row=0, column=0, padx=10)
        tk.Label(control_frame, text="Cantidad de nodos:").grid(row=0, column=1, padx=5)
        
        self.n_nodes_spin = tk.Spinbox(control_frame, from_=1, to=15, width=5)
        self.n_nodes_spin.grid(row=0, column=2, padx=5)

        tk.Button(control_frame, text="Generar Matriz", command=self.generar_matriz_gui).grid(row=0, column=3, padx=10)

        # Frame central para la matriz
        self.matrix_frame = tk.Frame(root)
        self.matrix_frame.pack(pady=10, padx=10)

        tk.Button(root, text="Construir y Graficar", command=self.procesar_y_graficar, bg="lightblue").pack(pady=10)

    def generar_matriz_gui(self):
        for widget in self.matrix_framse.winfo_children():
            widget.destroy()
            
        try:
            n = int(self.n_nodes_spin.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad de nodos debe ser un número entero.")
            return

        self.matrix_entries = []
        for i in range(n):
            fila = []
            for j in range(n):
                entry = tk.Entry(self.matrix_frame, width=5, justify="center")
                entry.grid(row=i, column=j, padx=2, pady=2)
                # SE DEJA VACÍO A PROPÓSITO: una interfaz limpia. 
                # Si está vacío, luego se interpretará como 0.
                fila.append(entry)
            self.matrix_entries.append(fila)

    def procesar_y_graficar(self):
        if not self.matrix_entries:
            messagebox.showwarning("Advertencia", "Primero genera la matriz.")
            return

        n = len(self.matrix_entries)
        matriz_numpy = np.zeros((n, n))

        # Recorrer entradas: Casilla vacía = 0, de lo contrario se toma el número escrito
        for i in range(n):
            for j in range(n):
                valor = self.matrix_entries[i][j].get().strip()
                if valor == "":
                    matriz_numpy[i, j] = 0
                else:
                    try:
                        matriz_numpy[i, j] = float(valor)
                    except ValueError:
                        messagebox.showerror("Error de Entrada", f"Por favor ingresa un número válido en la fila {i+1}, columna {j+1}.")
                        return

        # Instanciar y enviar
        try:
            builder = GraphBuilder(directed=self.directed_var.get())
            builder.build_graph_matrix(matriz_numpy)
            builder.plot_graph()
        except Exception as e:
            messagebox.showerror("Error al graficar", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()