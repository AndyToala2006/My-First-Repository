# Sistema de Gestión de Inventarios Mejorado

import os
import json

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: ${self.precio:.2f}"


class Inventario:
    ARCHIVO = "inventario.txt"

    def __init__(self):
        self.productos = []
        self.cargar_inventario()

    def guardar_inventario(self):
        try:
            with open(self.ARCHIVO, "w") as archivo:
                json.dump([vars(p) for p in self.productos], archivo)
        except PermissionError:
            print("Error: No tienes permisos para escribir en el archivo.")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def cargar_inventario(self):
        try:
            if os.path.exists(self.ARCHIVO):
                with open(self.ARCHIVO, "r") as archivo:
                    self.productos = [Producto(**p) for p in json.load(archivo)]
        except FileNotFoundError:
            print("Archivo de inventario no encontrado. Se creará uno nuevo al guardar.")
        except json.JSONDecodeError:
            print("Error: El archivo de inventario está corrupto.")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")

    def agregar_producto(self, producto):
        if any(p.id_producto == producto.id_producto for p in self.productos):
            print("Error: El ID del producto ya existe.")
        else:
            self.productos.append(producto)
            self.guardar_inventario()
            print("Producto agregado con éxito.")

    def eliminar_producto(self, id_producto):
        self.productos = [p for p in self.productos if p.id_producto != id_producto]
        self.guardar_inventario()
        print("Producto eliminado, si existía en el inventario.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        for producto in self.productos:
            if producto.id_producto == id_producto:
                if cantidad is not None:
                    producto.cantidad = cantidad
                if precio is not None:
                    producto.precio = precio
                self.guardar_inventario()
                print("Producto actualizado con éxito.")
                return
        print("Producto no encontrado.")

    def buscar_producto(self, nombre):
        encontrados = [p for p in self.productos if nombre.lower() in p.nombre.lower()]
        if encontrados:
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_productos(self):
        if self.productos:
            for producto in self.productos:
                print(producto)
        else:
            print("El inventario está vacío.")


def menu():
    inventario = Inventario()
    while True:
        print("\nSistema de Gestión de Inventarios")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos los productos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                id_producto = input("Ingrese ID único: ")
                nombre = input("Ingrese nombre: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.agregar_producto(producto)

            elif opcion == "2":
                id_producto = input("Ingrese ID del producto a eliminar: ")
                inventario.eliminar_producto(id_producto)

            elif opcion == "3":
                id_producto = input("Ingrese ID del producto a actualizar: ")
                cantidad = input("Nueva cantidad (deje en blanco para no cambiar): ")
                precio = input("Nuevo precio (deje en blanco para no cambiar): ")
                cantidad = int(cantidad) if cantidad else None
                precio = float(precio) if precio else None
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

        except ValueError:
            print("Error: Ingrese datos válidos.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    menu()