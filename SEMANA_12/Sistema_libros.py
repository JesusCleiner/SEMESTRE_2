# Clase Libro: Representa un libro en la biblioteca
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.titulo_autor = (titulo, autor)  # Usamos una tupla para almacenar título y autor
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"{self.titulo_autor[0]} por {self.titulo_autor[1]} (ISBN: {self.isbn}, Categoría: {self.categoria})"

# Clase Usuario: Representa un usuario de la biblioteca
class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []  # Lista de libros prestados al usuario

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.id_usuario}), Libros Prestados: {len(self.libros_prestados)}"

# Clase Biblioteca: Gestiona los libros, usuarios y préstamos
class Biblioteca:
    def __init__(self):
        self.libros = {}  # Diccionario de libros disponibles, clave: ISBN, valor: objeto Libro
        self.usuarios = {}  # Diccionario de usuarios registrados, clave: ID usuario, valor: objeto Usuario
        self.historial_prestamos = []  # Historial de préstamos

    def agregar_libro(self, libro):
        """Agregar un libro a la biblioteca"""
        if libro.isbn in self.libros:
            print(f"El libro con ISBN {libro.isbn} ya está en la biblioteca.")
        else:
            self.libros[libro.isbn] = libro
            print(f"Libro '{libro.titulo_autor[0]}' añadido a la biblioteca.")

    def quitar_libro(self, isbn):
        """Eliminar un libro de la biblioteca"""
        if isbn in self.libros:
            libro = self.libros.pop(isbn)
            print(f"Libro '{libro.titulo_autor[0]}' eliminado de la biblioteca.")
        else:
            print(f"No se encontró un libro con ISBN {isbn} en la biblioteca.")

    def registrar_usuario(self, usuario):
        """Registrar un nuevo usuario"""
        if usuario.id_usuario in self.usuarios:
            print(f"El usuario con ID {usuario.id_usuario} ya está registrado.")
        else:
            self.usuarios[usuario.id_usuario] = usuario
            print(f"Usuario '{usuario.nombre}' registrado con éxito.")

    def dar_baja_usuario(self, id_usuario):
        """Dar de baja a un usuario"""
        if id_usuario in self.usuarios:
            usuario = self.usuarios.pop(id_usuario)
            print(f"Usuario '{usuario.nombre}' dado de baja.")
        else:
            print(f"No se encontró un usuario con ID {id_usuario}.")

    def prestar_libro(self, id_usuario, isbn):
        """Prestar un libro a un usuario"""
        if id_usuario not in self.usuarios:
            print(f"El usuario con ID {id_usuario} no está registrado.")
            return

        if isbn not in self.libros:
            print(f"El libro con ISBN {isbn} no está disponible.")
            return

        libro = self.libros[isbn]
        usuario = self.usuarios[id_usuario]
        usuario.libros_prestados.append(libro)
        self.historial_prestamos.append((id_usuario, libro.isbn))
        print(f"Libro '{libro.titulo_autor[0]}' prestado a '{usuario.nombre}'.")
        del self.libros[isbn]  # Quita el libro de los disponibles

    def devolver_libro(self, id_usuario, isbn):
        """Devolver un libro prestado"""
        if id_usuario not in self.usuarios:
            print(f"El usuario con ID {id_usuario} no está registrado.")
            return

        usuario = self.usuarios[id_usuario]
        libro_prestado = None

        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                libro_prestado = libro
                break

        if libro_prestado:
            usuario.libros_prestados.remove(libro_prestado)
            self.libros[isbn] = libro_prestado  # Devuelve el libro a la biblioteca
            print(f"Libro '{libro_prestado.titulo_autor[0]}' devuelto por '{usuario.nombre}'.")
        else:
            print(f"El usuario '{usuario.nombre}' no tiene prestado un libro con ISBN {isbn}.")

    def buscar_libros(self, criterio, tipo="titulo"):
        """Buscar libros por título, autor o categoría"""
        resultados = []
        for libro in self.libros.values():
            if tipo == "titulo" and criterio.lower() in libro.titulo_autor[0].lower():
                resultados.append(libro)
            elif tipo == "autor" and criterio.lower() in libro.titulo_autor[1].lower():
                resultados.append(libro)
            elif tipo == "categoria" and criterio.lower() in libro.categoria.lower():
                resultados.append(libro)

        if resultados:
            print(f"Se encontraron {len(resultados)} libros:")
            for libro in resultados:
                print(libro)
        else:
            print(f"No se encontraron libros con {tipo} '{criterio}'.")

    def listar_libros_prestados(self, id_usuario):
        """Listar libros prestados a un usuario"""
        if id_usuario not in self.usuarios:
            print(f"El usuario con ID {id_usuario} no está registrado.")
            return

        usuario = self.usuarios[id_usuario]
        if usuario.libros_prestados:
            print(f"Libros prestados a '{usuario.nombre}':")
            for libro in usuario.libros_prestados:
                print(libro)
        else:
            print(f"El usuario '{usuario.nombre}' no tiene libros prestados.")


# Menú interactivo
def mostrar_menu():
    print("\nSistema de Gestión de Biblioteca Digital")
    print("1. Agregar libro")
    print("2. Quitar libro")
    print("3. Registrar usuario")
    print("4. Dar de baja usuario")
    print("5. Prestar libro")
    print("6. Devolver libro")
    print("7. Buscar libros")
    print("8. Listar libros prestados")
    print("9. Salir")

# Función principal del menú
def ejecutar_sistema():
    biblioteca = Biblioteca()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor del libro: ")
            categoria = input("Ingrese la categoría del libro: ")
            isbn = input("Ingrese el ISBN del libro: ")
            libro = Libro(titulo, autor, categoria, isbn)
            biblioteca.agregar_libro(libro)

        elif opcion == "2":
            isbn = input("Ingrese el ISBN del libro a quitar: ")
            biblioteca.quitar_libro(isbn)

        elif opcion == "3":
            nombre = input("Ingrese el nombre del usuario: ")
            id_usuario = input("Ingrese el ID del usuario: ")
            usuario = Usuario(nombre, id_usuario)
            biblioteca.registrar_usuario(usuario)

        elif opcion == "4":
            id_usuario = input("Ingrese el ID del usuario a dar de baja: ")
            biblioteca.dar_baja_usuario(id_usuario)

        elif opcion == "5":
            id_usuario = input("Ingrese el ID del usuario: ")
            isbn = input("Ingrese el ISBN del libro a prestar: ")
            biblioteca.prestar_libro(id_usuario, isbn)

        elif opcion == "6":
            id_usuario = input("Ingrese el ID del usuario: ")
            isbn = input("Ingrese el ISBN del libro a devolver: ")
            biblioteca.devolver_libro(id_usuario, isbn)

        elif opcion == "7":
            criterio = input("Ingrese el criterio de búsqueda: ")
            tipo_busqueda = input("Buscar por (titulo, autor, categoria): ").lower()
            biblioteca.buscar_libros(criterio, tipo_busqueda)

        elif opcion == "8":
            id_usuario = input("Ingrese el ID del usuario: ")
            biblioteca.listar_libros_prestados(id_usuario)

        elif opcion == "9":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")

# Ejecutar el sistema
if __name__ == "__main__":
    ejecutar_sistema()
