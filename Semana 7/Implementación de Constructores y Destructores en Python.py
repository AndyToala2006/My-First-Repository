class Archivo:
    def __init__(self, nombre_archivo):
        # Constructor: inicializa el objeto con el nombre del archivo.
        self.nombre_archivo = nombre_archivo
        self.archivo = None
        print(f"Constructor: Se ha creado el archivo {self.nombre_archivo}")

    def abrir(self):
        # Método para abrir el archivo.
        try:
            self.archivo = open(self.nombre_archivo, 'w')  # Abre el archivo en modo escritura.
            print(f"Archivo {self.nombre_archivo} abierto exitosamente.")
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")

    def escribir(self, contenido):
        # Método para escribir en el archivo.
        if self.archivo:
            self.archivo.write(contenido)
            print(f"Contenido '{contenido}' escrito en {self.nombre_archivo}.")
        else:
            print("El archivo no está abierto para escribir.")

    def cerrar(self):
        # Método para cerrar el archivo.
        if self.archivo:
            self.archivo.close()
            print(f"Archivo {self.nombre_archivo} cerrado exitosamente.")
        else:
            print("El archivo no está abierto.")

    def __del__(self):
        # Destructor: se llama cuando el objeto es destruido.
        if self.archivo:
            self.archivo.close()
            print(f"Destructor: El archivo {self.nombre_archivo} se cerró.")
        print(f"Destructor: El objeto {self.nombre_archivo} ha sido destruido.")


# Función interactiva para interactuar con el usuario
def menu():
    print("\n--- Menú de operaciones con archivos ---")
    print("1. Crear y abrir un archivo")
    print("2. Escribir en el archivo")
    print("3. Cerrar el archivo")
    print("4. Salir")

    eleccion = input("Seleccione una opción (1-4): ")

    return eleccion


# Función principal para controlar el flujo interactivo
def main():
    archivo = None

    while True:
        eleccion = menu()

        if eleccion == "1":
            nombre_archivo = input("Ingrese el nombre del archivo: ")
            archivo = Archivo(nombre_archivo)
            archivo.abrir()

        elif eleccion == "2":
            if archivo:
                contenido = input("Ingrese el contenido para escribir en el archivo: ")
                archivo.escribir(contenido)
            else:
                print("Primero debe crear y abrir un archivo.")

        elif eleccion == "3":
            if archivo:
                archivo.cerrar()
                del archivo  # Destructor llamado explícitamente
                archivo = None
            else:
                print("No hay archivo abierto.")

        elif eleccion == "4":
            print("Saliendo del programa...")
            if archivo:
                archivo.cerrar()  # Asegurarse de cerrar el archivo si está abierto
                del archivo  # Llamar al destructor antes de salir
            break

        else:
            print("Opción no válida. Por favor, elija una opción entre 1 y 4.")


if __name__ == "__main__":
    main()

