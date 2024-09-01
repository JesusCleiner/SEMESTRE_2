import os

class Producto:
    def __init__(self, id_producto, nombre_producto, cantidad_producto, precio_producto):
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.cantidad_producto = cantidad_producto
        self.precio_producto = precio_producto

    def obtener_id(self):
        return self.id_producto

    def obtener_nombre(self):
        return self.nombre_producto

    def obtener_cantidad(self):
        return self.cantidad_producto

    def obtener_precio(self):
        return self.precio_producto

    def establecer_cantidad(self, cantidad_producto):
        self.cantidad_producto = cantidad_producto

    def establecer_precio(self, precio_producto):
        self.precio_producto = precio_producto

    def __str__(self):
        return f"ID: {self.id_producto}, Nombre: {self.nombre_producto}, Cantidad: {self.cantidad_producto}, Precio: {self.precio_producto}"


class Inventario:
    def __init__(self):
        self.productos = {}

    def añadir_producto(self, producto):
        if producto.obtener_id() in self.productos:
            raise ValueError("El ID del producto ya existe en el inventario.")
        self.productos[producto.obtener_id()] = producto
        print(f"Producto con ID {producto.obtener_id()} añadido al inventario.")

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
            print(f"Producto con ID {id_producto} eliminado del inventario.")
        else:
            raise ValueError("El ID del producto no existe en el inventario.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto].establecer_cantidad(cantidad)
                print(f"Cantidad del producto con ID {id_producto} actualizada a {cantidad}.")
            if precio is not None:
                self.productos[id_producto].establecer_precio(precio)
                print(f"Precio del producto con ID {id_producto} actualizado a {precio}.")
        else:
            raise ValueError("El ID del producto no existe en el inventario.")

    def buscar_producto_por_nombre(self, nombre_producto):
        resultados = [producto for producto in self.productos.values() if nombre_producto.lower() in producto.obtener_nombre().lower()]
        return resultados

    def mostrar_todos_los_productos(self):
        return list(self.productos.values())

    def guardar_en_archivo(self, filename="inventario.txt"):
        try:
            with open(filename, 'w') as file:
                for producto in self.productos.values():
                    # Reemplazar comas en el nombre para evitar conflictos
                    nombre_sanitizado = producto.obtener_nombre().replace(',', ';')
                    file.write(f"{producto.obtener_id()},{nombre_sanitizado},{producto.obtener_cantidad()},{producto.obtener_precio()}\n")
            print(f"Inventario guardado correctamente en '{filename}'.")
        except Exception as e:
            print(f"Error al guardar el inventario: {e}")

    def cargar_desde_archivo(self, filename="inventario.txt"):
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    for linea in file:
                        partes = linea.strip().split(',')
                        if len(partes) != 4:
                            print(f"Línea malformada ignorada: {linea}")
                            continue
                        id_producto, nombre_producto, cantidad_producto, precio_producto = partes
                        # Reemplazar puntos y comas en el nombre si fueron sanitizados
                        nombre_producto = nombre_producto.replace(';', ',')
                        producto = Producto(id_producto, nombre_producto, int(cantidad_producto), float(precio_producto))
                        self.productos[id_producto] = producto
                print(f"Inventario cargado correctamente desde '{filename}'.")
            except Exception as e:
                print(f"Error al cargar el inventario: {e}")
        else:
            print(f"El archivo '{filename}' no existe. Se iniciará con un inventario vacío.")


def mostrar_menu():
    print("\n--- Sistema de Gestión de Inventario ---")
    print("1. Añadir producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar producto por nombre")
    print("5. Mostrar todos los productos")
    print("6. Guardar inventario en archivo")
    print("7. Cargar inventario desde archivo")
    print("8. Salir")


def main():
    inventario = Inventario()
    inventario.cargar_desde_archivo()

    while True:
        try:
            mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                id_producto = input("Ingrese el ID del producto: ").strip()
                nombre_producto = input("Ingrese el nombre del producto: ").strip()
                try:
                    cantidad_producto = int(input("Ingrese la cantidad del producto: ").strip())
                    precio_producto = float(input("Ingrese el precio del producto: ").strip())
                except ValueError:
                    print("Cantidad y precio deben ser números. Operación cancelada.")
                    continue

                try:
                    producto = Producto(id_producto, nombre_producto, cantidad_producto, precio_producto)
                    inventario.añadir_producto(producto)
                except ValueError as e:
                    print(e)

            elif opcion == "2":
                id_producto = input("Ingrese el ID del producto a eliminar: ").strip()
                try:
                    inventario.eliminar_producto(id_producto)
                except ValueError as e:
                    print(e)

            elif opcion == "3":
                id_producto = input("Ingrese el ID del producto a actualizar: ").strip()
                cantidad_input = input("Ingrese la nueva cantidad del producto (deje en blanco para no cambiar): ").strip()
                precio_input = input("Ingrese el nuevo precio del producto (deje en blanco para no cambiar): ").strip()

                cantidad_producto = None
                precio_producto = None

                if cantidad_input:
                    try:
                        cantidad_producto = int(cantidad_input)
                    except ValueError:
                        print("Cantidad debe ser un número. Operación cancelada.")
                        continue

                if precio_input:
                    try:
                        precio_producto = float(precio_input)
                    except ValueError:
                        print("Precio debe ser un número. Operación cancelada.")
                        continue

                if cantidad_producto is None and precio_producto is None:
                    print("No se proporcionaron nuevos valores. Operación cancelada.")
                    continue

                try:
                    inventario.actualizar_producto(id_producto, cantidad_producto, precio_producto)
                except ValueError as e:
                    print(e)

            elif opcion == "4":
                nombre_producto = input("Ingrese el nombre del producto a buscar: ").strip()
                resultados = inventario.buscar_producto_por_nombre(nombre_producto)
                if resultados:
                    print("\n--- Resultados de la búsqueda ---")
                    for producto in resultados:
                        print(producto)
                else:
                    print("No se encontraron productos con ese nombre.")

            elif opcion == "5":
                productos = inventario.mostrar_todos_los_productos()
                if productos:
                    print("\n--- Lista de Productos en el Inventario ---")
                    for producto in productos:
                        print(producto)
                else:
                    print("No hay productos en el inventario.")

            elif opcion == "6":
                inventario.guardar_en_archivo()

            elif opcion == "7":
                inventario.cargar_desde_archivo()

            elif opcion == "8":
                print("Guardando inventario antes de salir...")
                inventario.guardar_en_archivo()
                print("Saliendo del sistema...")
                break

            else:
                print("Opción no válida, por favor seleccione una opción válida.")

        except KeyboardInterrupt:
            print("\nOperación interrumpida por el usuario.")
            print("Guardando inventario antes de salir...")
            inventario.guardar_en_archivo()
            print("Saliendo del sistema...")
            break
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            print("Intentando continuar...")

if __name__ == "__main__":
    main()
