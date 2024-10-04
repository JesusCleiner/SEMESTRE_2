import tkinter as tk
from tkinter import messagebox

class TareaApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Administrar  Tareas")

        # Crear la entrada para añadir tareas
        self.entry_tarea = tk.Entry(ventana, width=40)
        self.entry_tarea.grid(row=0, column=0, padx=10, pady=10)
        self.entry_tarea.bind("<Return>", self.agregar_tarea)  # Permite añadir tareas con Enter

        # Crear botón para añadir tarea
        self.btn_agregar = tk.Button(ventana, text="Añadir &Tarea", command=self.agregar_tarea)  # Subrayar la letra A
        self.btn_agregar.grid(row=0, column=1, padx=10, pady=10)

        # Crear Listbox para mostrar las tareas
        self.lista_tareas = tk.Listbox(ventana, width=50, height=10, selectmode=tk.SINGLE)
        self.lista_tareas.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Crear botón para marcar tarea como completada
        self.btn_completar = tk.Button(ventana, text="Marcar como &Completada", command=self.marcar_completada)  # Subrayar la letra M
        self.btn_completar.grid(row=2, column=0, padx=10, pady=10)

        # Crear botón para eliminar tarea
        self.btn_eliminar = tk.Button(ventana, text="Eliminar &Tarea", command=self.eliminar_tarea)  # Subrayar la letra E
        self.btn_eliminar.grid(row=2, column=1, padx=10, pady=10)

        # Crear etiqueta para instruccion de salir de aplicacio
        self.label_instrucciones = tk.Label(ventana, text="Presiona Esc para salir", fg="blue", font=("Arial",16))
        self.label_instrucciones.grid(row=3, column=0, columnspan=2, pady=10)

        # Crear etiqueta para instruccion de propietario
        self.label_creadorapp = tk.Label(ventana, text="Por, JESUS GUTIERREZ RIVERA, segundo semestre paralelo D", fg="green", font=("Arial",10))
        self.label_creadorapp.grid(row=7, column=0, columnspan=2, pady=10)


        # Atajos de teclado
        self.ventana.bind("<Escape>", self.cerrar_aplicacion)  # Cerrar aplicación con Esc
        self.ventana.bind("<c>", lambda event: self.marcar_completada())  # Marcar como completada con 'C'
        self.ventana.bind("<Delete>", lambda event: self.eliminar_tarea())  # Eliminar tarea con 'Delete'
        self.ventana.bind("<d>", lambda event: self.eliminar_tarea())  # Eliminar tarea con 'D'

    def agregar_tarea(self, event=None):
        tarea = self.entry_tarea.get().strip()
        if tarea:
            self.lista_tareas.insert(tk.END, tarea)
            self.entry_tarea.delete(0, tk.END)  # Limpiar campo de entrada
        else:
            messagebox.showwarning("Entrada vacía", "No puedes añadir una tarea vacía.")

    def marcar_completada(self):
        try:
            seleccion = self.lista_tareas.curselection()
            tarea = self.lista_tareas.get(seleccion)
            self.lista_tareas.delete(seleccion)
            self.lista_tareas.insert(tk.END, f"{tarea} (Completada)")
        except IndexError:
            messagebox.showwarning("Selección no válida", "Selecciona una tarea para marcar como completada.")

    def eliminar_tarea(self):
        try:
            seleccion = self.lista_tareas.curselection()
            self.lista_tareas.delete(seleccion)
        except IndexError:
            messagebox.showwarning("Selección no válida", "Selecciona una tarea para eliminar.")

    def cerrar_aplicacion(self, event=None):
        self.ventana.quit()  # Cierra la aplicación

# Inicializar la aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.geometry("400x400")

    app = TareaApp(ventana)
    ventana.mainloop()
