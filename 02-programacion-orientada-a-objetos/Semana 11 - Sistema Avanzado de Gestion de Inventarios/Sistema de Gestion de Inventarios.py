import json
import os


class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        """Clase para representar un producto en el inventario."""
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id_producto} | {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"

    def to_dict(self):
        """Convierte el objeto Producto en un diccionario para facilitar la serialización."""
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        """Crea un objeto Producto desde un diccionario."""
        return Producto(
            data["id_producto"],
            data["nombre"],
            data["cantidad"],
            data["precio"]
        )


class Inventario:
    ARCHIVO = "inventario.json"

    def __init__(self):
        """Inicializa el inventario cargando los productos desde el archivo."""
        self.productos = {}
        self.cargar_inventario()

    def guardar_inventario(self):
        """Guarda los productos en un archivo JSON."""
        try:
            with open(self.ARCHIVO, "w") as archivo:
                json.dump({id_: p.to_dict() for id_, p in self.productos.items()}, archivo)
        except Exception as e:
            print(f"Error al guardar el inventario: {e}")

    def cargar_inventario(self):
        """Carga los productos desde un archivo JSON."""
        if os.path.exists(self.ARCHIVO):
            try:
                with open(self.ARCHIVO, "r") as archivo:
                    datos = json.load(archivo)
                    self.productos = {id_: Producto.from_dict(p) for id_, p in datos.items()}
            except json.JSONDecodeError:
                print("Error: Archivo de inventario corrupto.")
            except Exception as e:
                print(f"Error al cargar el inventario: {e}")

    def agregar_producto(self, producto):
        """Añade un producto al inventario si el ID no existe."""
        if producto.id_producto in self.productos:
            print("Error: El ID del producto ya existe.")
        else:
            self.productos[producto.id_producto] = producto
            self.guardar_inventario()
            print("Producto agregado correctamente.")

    def eliminar_producto(self, id_producto):
        """Elimina un producto del inventario por su ID."""
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_inventario()
            print("Producto eliminado.")
        else:
            print("Error: Producto no encontrado.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """Actualiza la cantidad y/o precio de un producto."""
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto].cantidad = cantidad
            if precio is not None:
                self.productos[id_producto].precio = precio
            self.guardar_inventario()
            print("Producto actualizado correctamente.")
        else:
            print("Error: Producto no encontrado.")

    def buscar_producto(self, nombre):
        """Busca productos por nombre."""
        encontrados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        if encontrados:
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_productos(self):
        """Muestra todos los productos del inventario."""
        if self.productos:
            print("\nInventario:")
            for producto in self.productos.values():
                print(producto)
        else:
            print("El inventario está vacío.")


def input_entero(mensaje):
    """Solicita un número entero al usuario."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número entero válido.")


def input_flotante(mensaje):
    """Solicita un número decimal al usuario."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número decimal válido.")


def menu():
    inventario = Inventario()

    while True:
        print("\nSistema Avanzado de Gestión de Inventarios")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos los productos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_producto = input("Ingrese ID único: ")
            nombre = input("Ingrese nombre: ")
            cantidad = input_entero("Ingrese cantidad: ")
            precio = input_flotante("Ingrese precio: ")
            producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar_producto(producto)

        elif opcion == "2":
            id_producto = input("Ingrese ID del producto a eliminar: ")
            confirmacion = input(f"¿Seguro que desea eliminar {id_producto}? (s/n): ").strip().lower()
            if confirmacion == "s":
                inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = input("Ingrese ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (deje en blanco para no cambiar): ")
            precio = input("Nuevo precio (deje en blanco para no cambiar): ")
            cantidad = int(cantidad) if cantidad.isdigit() else None
            precio = float(precio) if precio.replace(".", "", 1).isdigit() else None
            inventario.actualizar_producto(id_producto, cantidad, precio)

        elif opcion == "4":
            nombre = input("Ingrese nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_productos()

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu()
