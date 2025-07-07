# Clase Libro
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.titulo = titulo
        self.autor = tuple(autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"Título: {self.titulo}, Autor: {', '.join(self.autor)}, Categoría: {self.categoria}, ISBN: {self.isbn}"

# Clase Usuario
class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []

    def __str__(self):
        return f"Nombre: {self.nombre}, ID Usuario: {self.id_usuario}"

    def añadir_libro(self, libro):
        self.libros_prestados.append(libro)

    def devolver_libro(self, libro):
        self.libros_prestados.remove(libro)

# Clase Biblioteca
class Biblioteca:
    def __init__(self):
        self.libros = {}  # Diccionario para gestionar libros por ISBN
        self.usuarios = set()  # Conjunto para asegurar IDs únicos de usuarios

    def añadir_libro(self, libro):
        self.libros[libro.isbn] = libro

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            del self.libros[isbn]
        else:
            print("El libro con ese ISBN no está registrado.")

    def registrar_usuario(self, usuario):
        self.usuarios.add(usuario.id_usuario)

    def dar_baja_usuario(self, id_usuario):
        if id_usuario in self.usuarios:
            self.usuarios.remove(id_usuario)
        else:
            print("El usuario con ese ID no está registrado.")

    def prestar_libro(self, isbn, id_usuario):
        if isbn in self.libros:
            libro = self.libros[isbn]
            for usuario in self.usuarios:
                if usuario.id_usuario == id_usuario:
                    usuario.añadir_libro(libro)
                    del self.libros[isbn]  # El libro se retira de la biblioteca
                    print(f"Libro '{libro.titulo}' prestado a {usuario.nombre}")
                    return
        print("El libro no está disponible o el usuario no está registrado.")

    def devolver_libro(self, isbn, id_usuario):
        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario:
                for libro in usuario.libros_prestados:
                    if libro.isbn == isbn:
                        usuario.devolver_libro(libro)
                        self.libros[isbn] = libro  # El libro regresa a la biblioteca
                        print(f"Libro '{libro.titulo}' devuelto por {usuario.nombre}")
                        return
        print("El libro no está prestado o el usuario no está registrado.")

    def buscar_libro(self, criterio, valor):
        encontrados = []
        for libro in self.libros.values():
            if criterio == "titulo" and valor.lower() in libro.titulo.lower():
                encontrados.append(libro)
            elif criterio == "autor" and any(autor.lower() in valor.lower() for autor in libro.autor):
                encontrados.append(libro)
            elif criterio == "categoria" and valor.lower() in libro.categoria.lower():
                encontrados.append(libro)
        return encontrados

    def listar_libros_prestados(self, id_usuario):
        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario.libros_prestados
        return []

# Función de interacción con el usuario
def interactuar_con_usuario():
    biblioteca = Biblioteca()
    while True:
        print("\n--- Menú de la Biblioteca ---")
        print("1. Registrar nuevo usuario")
        print("2. Dar de baja usuario")
        print("3. Añadir libro")
        print("4. Eliminar libro")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libro")
        print("8. Listar libros prestados")
        print("9. Salir")

        opcion = input("Selecciona una opción (1-9): ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del usuario: ")
            id_usuario = input("Ingrese el ID del usuario: ")
            usuario = Usuario(nombre, id_usuario)
            biblioteca.registrar_usuario(usuario)
            print(f"Usuario {nombre} registrado exitosamente.")

        elif opcion == "2":
            id_usuario = input("Ingrese el ID del usuario a dar de baja: ")
            biblioteca.dar_baja_usuario(id_usuario)

        elif opcion == "3":
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor del libro (separado por coma si hay más de un autor): ").split(",")
            categoria = input("Ingrese la categoría del libro: ")
            isbn = input("Ingrese el ISBN del libro: ")
            libro = Libro(titulo, autor, categoria, isbn)
            biblioteca.añadir_libro(libro)
            print(f"Libro '{titulo}' añadido a la biblioteca.")

        elif opcion == "4":
            isbn = input("Ingrese el ISBN del libro a eliminar: ")
            biblioteca.quitar_libro(isbn)

        elif opcion == "5":
            isbn = input("Ingrese el ISBN del libro a prestar: ")
            id_usuario = input("Ingrese el ID del usuario que lo solicita: ")
            biblioteca.prestar_libro(isbn, id_usuario)

        elif opcion == "6":
            isbn = input("Ingrese el ISBN del libro a devolver: ")
            id_usuario = input("Ingrese el ID del usuario que devuelve el libro: ")
            biblioteca.devolver_libro(isbn, id_usuario)

        elif opcion == "7":
            criterio = input("Buscar por (titulo, autor, categoria): ")
            valor = input(f"Ingrese el {criterio} a buscar: ")
            libros_encontrados = biblioteca.buscar_libro(criterio, valor)
            if libros_encontrados:
                print("\nLibros encontrados:")
                for libro in libros_encontrados:
                    print(libro)
            else:
                print("No se encontraron libros con ese criterio.")

        elif opcion == "8":
            id_usuario = input("Ingrese el ID del usuario para ver los libros prestados: ")
            libros_prestados = biblioteca.listar_libros_prestados(id_usuario)
            if libros_prestados:
                print("\nLibros prestados:")
                for libro in libros_prestados:
                    print(libro)
            else:
                print("Este usuario no tiene libros prestados.")

        elif opcion == "9":
            print("Saliendo del sistema.")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

# Ejecutar la interacción con el usuario
interactuar_con_usuario()
