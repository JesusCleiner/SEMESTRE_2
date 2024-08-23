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

    # Convertir el producto a una cadena para guardar en el archivo
    def a_cadena(self):
        return f"{self.id_producto},{self.nombre},{self.cantidad},{self.precio}"

    @staticmethod
    def from_cadena(product_str):
        id_producto, nombre, cantidad, precio = product_str.split(',')
        return Producto(id_producto, nombre, int(cantidad), float(precio))

# Clase Inventario
class Inventario:
    def __init__(self, archivo):
        self.archivo = archivo

    def añadir_producto(self, producto):
        if self.mostrar_producto_por_id(producto.id_producto):
            return False
        with open(self.archivo, 'a') as f:
            f.write(producto.a_cadena() + '\n')
        return True

    def eliminar_producto(self, id_producto):
        productos = self.leer_productos()
        productos_actualizados = [p for p in productos if p.id_producto != id_producto]
        if len(productos_actualizados) < len(productos):
            self.guardar_productos(productos_actualizados)
            return True
        return False

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        productos = self.leer_productos()
        for p in productos:
            if p.id_producto == id_producto:
                if cantidad is not None:
                    p.cantidad = cantidad
                if precio is not None:
                    p.precio = precio
                self.guardar_productos(productos)
                return True
        return False

    def buscar_producto(self, nombre):
        productos = self.leer_productos()
        resultados = [p for p in productos if nombre.lower() in p.nombre.lower()]
        return resultados

    def mostrar_producto_por_id(self, id_producto):
        productos = self.leer_productos()
        for p in productos:
            if p.id_producto == id_producto:
                return p
        return None

    def mostrar_productos(self):
        return self.leer_productos()

    def leer_productos(self):
        productos = []
        with open(self.archivo, 'r') as f:
            for line in f:
                productos.append(Producto.from_cadena(line.strip()))
        return productos

    def guardar_productos(self, productos):
        with open(self.archivo, 'w') as f:
            for p in productos:
                f.write(p.a_cadena() + '\n')

# Clase Formulario_principal
class Formulario_principal(ABC):
    def __init__(self, ventana_principal):
        self.frame_principal = tk.Frame(ventana_principal, padx=5, pady=5, bg="#D3D3D3")
        self.frame_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.crear_interfaz()

    @abstractmethod
    def crear_interfaz(self):
        pass

    def cerrar_aplicacion(self):
        self.frame_principal.destroy()

class Interfaz_grafica(Formulario_principal):
    def crear_interfaz(self):
        tk.Label(self.frame_principal, text="MOVIMIENTOS DIARIOS", font=("Arial", 14),
                 bg="#D3D3D3", fg="black").pack(pady=10, anchor="w")

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

# Clase Productos
class Productos(Interfaz_grafica):
    def __init__(self, ventana_principal, archivo):
        super().__init__(ventana_principal)
        self.inventario = Inventario(archivo)  # Instanciar el inventario con el archivo

    def ingreso_productos(self):
        self.frame_contenedor = tk.Frame(self.frame_principal, bg="yellow")
        self.frame_contenedor.pack(pady=10, anchor="w", fill=tk.X)

        tk.Label(self.frame_contenedor, text="INGRESO DE PRODUCTOS", font=("Arial", 14),
                 bg="yellow", fg="black").pack(pady=10, anchor="w")

        self.frame_entrada = tk.Frame(self.frame_contenedor, bg="yellow")
        self.frame_entrada.pack(pady=10, anchor="w", fill=tk.X)

        self.id = self.crear_entrada("ID PRODUCTO :", 0)
        self.nombre = self.crear_entrada("NOMBRE  :", 1)
        self.cantidad = self.crear_entrada("CANTIDAD :", 2)
        self.precio = self.crear_entrada("PRECIO  :", 3)

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

        if not all([id_producto, nombre_producto, cantidad_producto, precio_producto]):
            messagebox.showwarning("Advertencia", "Todos los campos deben ser completados.")
            return

        producto_existente = self.inventario.mostrar_producto_por_id(id_producto)
        if producto_existente:
            producto_existente.nombre = nombre_producto
            producto_existente.cantidad = int(cantidad_producto)
            producto_existente.precio = float(precio_producto)
            self.inventario.actualizar_producto(id_producto, producto_existente.cantidad, producto_existente.precio)
            messagebox.showinfo("Formulario", "Producto actualizado correctamente.")
        else:
            producto = Producto(id_producto, nombre_producto, int(cantidad_producto), float(precio_producto))
            if self.inventario.añadir_producto(producto):
                messagebox.showinfo("Formulario", "Producto añadido correctamente.")
            else:
                messagebox.showerror("Error", "ID del producto ya existe.")

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
            resultados_str = "\n".join([f"ID: {p.id_producto}, Nombre: {p.nombre}, Cantidad: {p.cantidad}, Precio: {p.precio}" for p in resultados])
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
        self.interfaz = Productos(self.ventana, "inventario.txt")  # Se especifica el archivo de texto

ventana_principal = tk.Tk()
ventana_principal.title("MOVIMIENTOS DE TIENDA")
ventana_principal.geometry("650x650")
app = Administrar_tienda(ventana_principal)

ventana_principal.mainloop()
