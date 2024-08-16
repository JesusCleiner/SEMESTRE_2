import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

# Clase Producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Getters
    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Setters
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

# Clase Inventario
class Inventario:
    def __init__(self):
        self.productos = []

    def añadir_producto(self, producto):
        # Asegurarse de que el ID sea único
        for p in self.productos:
            if p.get_id() == producto.get_id():
                return False
        self.productos.append(producto)
        return True

    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                return True
        return False

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if cantidad is not None:
                    p.set_cantidad(cantidad)
                if precio is not None:
                    p.set_precio(precio)
                return True
        return False

    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        return resultados

    def mostrar_producto_por_id(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                return p
        return None

    def mostrar_productos(self):
        return [f"ID: {p.get_id()}, Nombre: {p.get_nombre()}, Cantidad: {p.get_cantidad()}, Precio: {p.get_precio()}" for p in self.productos]

# Clase Formulario_principal
class Formulario_principal(ABC):
    def __init__(self, ventana_principal):
        self.frame_principal = tk.Frame(ventana_principal, padx=5, pady=5, bg="#D3D3D3")
        self.frame_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.crear_interfaz()  # Llamar al método abstracto para crear la interfaz.

    @abstractmethod
    def crear_interfaz(self):
        pass

    def cerrar_aplicacion(self):
        self.frame_principal.destroy()

class Interfaz_grafica(Formulario_principal):
    def crear_interfaz(self):
        tk.Label(self.frame_principal, text="MOVIMIENTOS DIARIOS", font=("Arial", 14),
                 bg="#D3D3D3", fg="black").pack(pady=10, anchor="w")

        # Crear un frame para botones
        self.frame_botones = tk.Frame(self.frame_principal, bg="#D3D3D3")
        self.frame_botones.pack(pady=4, anchor="w")

        self.grupo_botones()

    def grupo_botones(self):
        tk.Button(self.frame_botones, text="ADQUISICIONES", command=self.ingreso_productos, font=("Arial", 14),
                  bg="blue", fg="white").pack(side=tk.LEFT, padx=1, pady=1)
        tk.Button(self.frame_botones, text="BUSCAR PRODUCTO", command=self.formulario_busqueda_producto, font=("Arial",14),
                  bg="blue", fg="white").pack(side=tk.LEFT, padx=1, pady=1)
        tk.Button(self.frame_botones, text="ELIMINAR PRODUCTO", command=self.formulario_eliminar_producto, font=("Arial", 14),
                  bg="blue", fg="white").pack(side=tk.LEFT, padx=1, pady=1)

    #def ingreso_productos(self):
    #   pass

# def formulario_busqueda_producto(self):
#   messagebox.showinfo("Formulario", "Formulario de búsqueda no implementado.")

#def formulario_eliminar_producto(self):
#  messagebox.showinfo("Formulario", "Formulario eliminar producto no implementado.")

# Clase Productos
class Productos(Interfaz_grafica):
    def __init__(self, ventana_principal):
        super().__init__(ventana_principal)
        self.inventario = Inventario()  # Instanciar el inventario

    def ingreso_productos(self):
        # Frame contenedor para etiqueta y entradas de texto
        self.frame_contenedor = tk.Frame(self.frame_principal, bg="yellow")
        self.frame_contenedor.pack(pady=10, anchor="w", fill=tk.X)

        tk.Label(self.frame_contenedor, text="INGRESO DE PRODUCTOS", font=("Arial", 14),
                 bg="yellow", fg="black").pack(pady=10, anchor="w")

        # Frame para entradas de texto
        self.frame_entrada = tk.Frame(self.frame_contenedor, bg="yellow")
        self.frame_entrada.pack(pady=10, anchor="w", fill=tk.X)

        # Etiquetas y entradas de texto
        self.id = self.crear_entrada("ID PRODUCTO :", 0)
        self.nombre = self.crear_entrada("NOMBRE  :", 1)
        self.cantidad = self.crear_entrada("CANTIDAD :", 2)
        self.precio = self.crear_entrada("PRECIO  :", 3)

        # Botones Guardar y Cerrar
        self.crea_botones()

    def crear_entrada(self, label_text, row):
        tk.Label(self.frame_entrada, text=label_text, font=("Arial", 10), bg="yellow").grid(row=row, column=0, padx=5, pady=3, sticky='w')
        entrada = tk.Entry(self.frame_entrada, font=("Arial", 10), width=40)
        entrada.grid(row=row, column=1, padx=5, pady=3, sticky='ew')
        return entrada

    def crea_botones(self):
        botones_frame = tk.Frame(self.frame_contenedor, bg="yellow")
        botones_frame.pack(pady=10, anchor="w")

        tk.Button(botones_frame, text="Guardar", command=self.guardar, font=("Arial", 14),
                  bg="green", fg="white").grid(row=0, column=0, pady=10, padx=5)
        tk.Button(botones_frame, text="Cerrar", command=self.cerrar_entrada, font=("Arial", 14),
                  bg="red", fg="white").grid(row=0, column=1, pady=10, padx=5)

    def guardar(self):
        id_producto = self.id.get()
        nombre_producto = self.nombre.get()
        cantidad_producto = self.cantidad.get()
        precio_producto = self.precio.get()

        # Encapsulamiento: Control de acceso a datos
        if not all([id_producto, nombre_producto, cantidad_producto, precio_producto]):
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")
            return

        producto_existente = self.inventario.mostrar_producto_por_id(id_producto)
        if producto_existente:
            # Actualizar el producto existente
            producto_existente.set_nombre(nombre_producto)
            producto_existente.set_cantidad(cantidad_producto)
            producto_existente.set_precio(precio_producto)
            messagebox.showinfo("Formulario", "Producto actualizado correctamente.")
        else:
            # Añadir el nuevo producto
            producto = Producto(id_producto, nombre_producto, cantidad_producto, precio_producto)
            if self.inventario.añadir_producto(producto):
                messagebox.showinfo("Formulario", "Producto añadido correctamente.")
            else:
                messagebox.showerror("Error", "ID del producto ya existe.")

        # Borrar los datos de las cajas de texto
        self.id.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.cantidad.delete(0, tk.END)
        self.precio.delete(0, tk.END)

    def formulario_busqueda_producto(self):
        self.frame_busqueda = tk.Frame(self.frame_principal, bg="yellow")
        self.frame_busqueda.pack(pady=10, anchor="w", fill=tk.X)

        tk.Label(self.frame_busqueda, text="BUSCAR PRODUCTO", font=("Arial", 14),
                 bg="yellow", fg="black").pack(pady=10, anchor="w")

        self.buscar_nombre = tk.Entry(self.frame_busqueda, font=("Arial", 10), width=40)
        self.buscar_nombre.pack(pady=5)

        tk.Button(self.frame_busqueda, text="Buscar", command=self.buscar_producto, font=("Arial", 14),
                  bg="green", fg="white").pack(pady=10)

        tk.Button(self.frame_busqueda, text="Cerrar", command=self.cerrar_entrada, font=("Arial", 14),
                  bg="red", fg="white").pack(pady=10)

    def buscar_producto(self):
        nombre = self.buscar_nombre.get()
        resultados = self.inventario.buscar_producto(nombre)
        if resultados:
            resultados_str = "\n".join([f"ID: {p.get_id()}, Nombre: {p.get_nombre()}, Cantidad: {p.get_cantidad()}, Precio: {p.get_precio()}" for p in resultados])
            messagebox.showinfo("Resultado de Búsqueda", resultados_str)
        else:
            messagebox.showinfo("Resultado de Búsqueda", "No se encontraron productos.")

    def formulario_eliminar_producto(self):
        self.frame_eliminar = tk.Frame(self.frame_principal, bg="yellow")
        self.frame_eliminar.pack(pady=10, anchor="w", fill=tk.X)

        tk.Label(self.frame_eliminar, text="ELIMINAR PRODUCTO", font=("Arial", 14),
                 bg="yellow", fg="black").pack(pady=10, anchor="w")

        self.eliminar_id = tk.Entry(self.frame_eliminar, font=("Arial", 10), width=40)
        self.eliminar_id.pack(pady=5)

        tk.Button(self.frame_eliminar, text="Eliminar", command=self.eliminar_producto, font=("Arial", 14),
                  bg="green", fg="white").pack(pady=10)

        tk.Button(self.frame_eliminar, text="Cerrar", command=self.cerrar_entrada, font=("Arial", 14),
                  bg="red", fg="white").pack(pady=10)

    def eliminar_producto(self):
        id_producto = self.eliminar_id.get()
        if self.inventario.eliminar_producto(id_producto):
            messagebox.showinfo("Formulario", "Producto eliminado correctamente.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def cerrar_entrada(self):
        if hasattr(self, 'frame_contenedor'):
            self.frame_contenedor.destroy()

        if hasattr(self, 'frame_busqueda'):
            self.frame_busqueda.destroy()
        if hasattr(self, 'frame_eliminar'):
            self.frame_eliminar.destroy()

class Administrar_tienda():
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Movimientos de la tienda Gutierrez")
        # Cambiar la instancia a Productos en lugar de Interfaz_grafica
        self.interfaz = Productos(self.ventana)

ventana_principal = tk.Tk()
ventana_principal.title("MOVIMIENTOS DE TIENDA")
ventana_principal.geometry("650x650")
#ventana_principal.state('zoomed')  # Maximizar la ventana
app = Administrar_tienda(ventana_principal)

ventana_principal.mainloop()
