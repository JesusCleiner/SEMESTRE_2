import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry

class Interfaz_grafica():
    def __init__(self, ventana_primaria):
        self.frame_inicial = tk.Frame(ventana_primaria, padx=5, pady=5, bg="#D3D3D3")
        self.frame_inicial.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.crear_etiquetas()
        self.crear_campos_entrada()
        self.grupo_botones()
        self.crear_lista_eventos()

    def crear_etiquetas(self):
        tk.Label(self.frame_inicial, text="Movimientos de agenda personal", font=("Arial", 14), bg="#D3D3D3", fg="black").pack(pady=10, anchor="w")

    def crear_campos_entrada(self):
        frame_entrada = tk.Frame(self.frame_inicial, bg="#D3D3D3")
        frame_entrada.pack(pady=5, anchor="w")

        # Labels and Entries for event details
        tk.Label(frame_entrada, text="Fecha", font=("Arial", 12), bg="#D3D3D3").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(frame_entrada, text="Hora", font=("Arial", 12), bg="#D3D3D3").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_entrada, text="Descripción", font=("Arial", 12), bg="#D3D3D3").grid(row=0, column=2, padx=5, pady=5)

        self.fecha_entrada = DateEntry(frame_entrada, width=15, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
        self.fecha_entrada.grid(row=1, column=0, padx=5, pady=5)

        self.hora_entrada = tk.Entry(frame_entrada, width=10)
        self.hora_entrada.grid(row=1, column=1, padx=5, pady=5)

        self.descripcion_entrada = tk.Entry(frame_entrada, width=40)
        self.descripcion_entrada.grid(row=1, column=2, padx=5, pady=5)

    # Crear grupo de botones
    def grupo_botones(self):
        frame_botones = tk.Frame(self.frame_inicial, bg="#D3D3D3")
        frame_botones.pack(pady=10, anchor="e")

        tk.Button(frame_botones, text="Agregar tarea", command=self.agregar_elemento, font=("Arial", 14), bg="blue", fg="white", width=20).pack(pady=5)
        tk.Button(frame_botones, text="Eliminar Tarea", command=self.eliminar_elemento, font=("Arial", 14), bg="green", fg="white", width=20).pack(pady=5)
        tk.Button(frame_botones, text="Terminar sesión", command=self.cerrar_formulario, font=("Arial", 14), bg="red", fg="white", width=20).pack(pady=5)

    def crear_lista_eventos(self):
        # Crear el Treeview para listar eventos
        columnas = ("Fecha", "Hora", "Descripción")
        self.tabla_eventos = ttk.Treeview(self.frame_inicial, columns=columnas, show='headings', height=10)

        for col in columnas:
            self.tabla_eventos.heading(col, text=col)
            self.tabla_eventos.column(col, minwidth=100)

        self.tabla_eventos.pack(pady=10, fill=tk.BOTH, expand=True)

    def agregar_elemento(self):
        # Obtener los valores de las entradas
        fecha = self.fecha_entrada.get()
        hora = self.hora_entrada.get()
        descripcion = self.descripcion_entrada.get()

        if fecha and hora and descripcion:
            # Insertar los valores en el Treeview
            self.tabla_eventos.insert('', tk.END, values=(fecha, hora, descripcion))
            # Limpiar campos de entrada
            self.hora_entrada.delete(0, tk.END)
            self.descripcion_entrada.delete(0, tk.END)
        else:
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")

    def eliminar_elemento(self):
        # Obtener el elemento seleccionado en el Treeview
        seleccionado = self.tabla_eventos.selection()
        if seleccionado:
            respuesta = messagebox.askyesno("Eliminar", "¿Está seguro que desea eliminar este evento?")
            if respuesta:
                self.tabla_eventos.delete(seleccionado)
        else:
            messagebox.showwarning("Sin selección", "Por favor, seleccione un evento para eliminar.")

    def cerrar_formulario(self):
        self.frame_inicial.destroy()


class Administrar_formulario_principal():
    def __init__(self, ventana_primaria):
        self.ventana = ventana_primaria
        self.ventana.title("Agenda Personal de cleiner gutierrez")
        self.interfaz = Interfaz_grafica(self.ventana)


# Crear la ventana principal de la aplicación
ventana_primaria = tk.Tk()
ventana_primaria.geometry("700x500")  # Ajusta el tamaño de la ventana
app = Administrar_formulario_principal(ventana_primaria)

ventana_primaria.mainloop()
