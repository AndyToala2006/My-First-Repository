# Clase Producto: Define los productos en la tienda.
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


# Clase Carrito: Administra los productos que el usuario agrega al carrito.
class Carrito:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)
        print(f"{producto.nombre} ha sido agregado a tu carrito.")

    def mostrar_carrito(self):
        if not self.productos:
            print("Tu carrito está vacío.")
        else:
            print("\nTu carrito contiene:")
            for producto in self.productos:
                print(producto)

    def total(self):
        return sum(producto.precio for producto in self.productos)


# Clase Tienda: Simula las operaciones de la tienda.
class Tienda:
    def __init__(self):
        self.productos_disponibles = [
            Producto("Laptop", 1000),
            Producto("Smartphone", 500),
            Producto("Auriculares", 50),
            Producto("Teclado", 30),
            Producto("Ratón", 20)
        ]
        self.carrito = Carrito()

    def mostrar_productos(self):
        print("\nProductos disponibles en la tienda:")
        for index, producto in enumerate(self.productos_disponibles, 1):
            print(f"{index}. {producto}")

    def seleccionar_producto(self):
        while True:
            try:
                seleccion = int(
                    input("\nSelecciona el número del producto que deseas agregar al carrito (0 para terminar): "))
                if seleccion == 0:
                    break
                elif 1 <= seleccion <= len(self.productos_disponibles):
                    self.carrito.agregar_producto(self.productos_disponibles[seleccion - 1])
                else:
                    print("Seleccion no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor ingresa un número.")

    def realizar_compra(self):
        self.carrito.mostrar_carrito()
        total = self.carrito.total()
        if total > 0:
            print(f"\nTotal a pagar: ${total}")
            print("¡Gracias por tu compra!")
        else:
            print("No hay productos en tu carrito para comprar.")


# Función principal para ejecutar la tienda
def main():
    tienda = Tienda()

    while True:
        print("\nBienvenido a la Tienda en Línea")
        tienda.mostrar_productos()
        tienda.seleccionar_producto()

        # Pregunta si el usuario quiere continuar
        continuar = input("\n¿Quieres continuar comprando? (s/n): ").strip().lower()
        if continuar != 's':
            break

    tienda.realizar_compra()


# Ejecutar el programa
if __name__ == "__main__":
    main()
