import tkinter as tk
from tkinter import messagebox

# Función para guardar los datos en el archivo txt
def guardar_datos():
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    correo = entry_correo.get()

    if not nombre or not edad or not correo:
        messagebox.showwarning("Datos incompletos", "Todos los campos son obligatorios")
        return

    try:
        # Abrir el archivo en modo 'a' para añadir datos sin sobrescribir
        with open("datos_usuario.txt", "a") as archivo:
            archivo.write(f"{nombre},{edad},{correo}\n")
        messagebox.showinfo("Éxito", "Datos guardados correctamente")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar los datos: {e}")

# Función para limpiar los campos de entrada después de guardar los datos
def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_correo.delete(0, tk.END)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ingreso de Datos de Usuario")
ventana.geometry("500x400")

# Etiqueta y campo para el nombre
label_nombre = tk.Label(ventana, text="Nombre:")
label_nombre.pack(pady=5)
entry_nombre = tk.Entry(ventana)
entry_nombre.pack(pady=5)

# Etiqueta y campo para la edad
label_edad = tk.Label(ventana, text="Edad:")
label_edad.pack(pady=5)
entry_edad = tk.Entry(ventana)
entry_edad.pack(pady=5)

# Etiqueta y campo para el correo
label_correo = tk.Label(ventana, text="Correo:")
label_correo.pack(pady=5)
entry_correo = tk.Entry(ventana)
entry_correo.pack(pady=5)

# Botón para guardar los datos
btn_guardar = tk.Button(ventana, text="Guardar Datos", command=guardar_datos)
btn_guardar.pack(pady=10)

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
