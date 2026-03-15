from __future__ import annotations

from .productos import Factura


class Inventario:
    def __init__(self):
        self.facturas: dict[int, Factura] = {}
        self.ids_registrados: set[int] = set()
        self.historial: list[tuple[str, int]] = []

    def agregar_factura(self, factura: Factura) -> None:
        self.facturas[factura.get_id()] = factura
        self.ids_registrados.add(factura.get_id())
        self.historial.append(("agregar", factura.get_id()))

    def eliminar_factura(self, factura_id: int) -> bool:
        if factura_id not in self.facturas:
            return False
        del self.facturas[factura_id]
        self.ids_registrados.discard(factura_id)
        self.historial.append(("eliminar", factura_id))
        return True

    def actualizar_factura(
        self,
        factura_id: int,
        cantidad_cajas: int | None = None,
        precio_caja: float | None = None,
        total: float | None = None,
    ) -> bool:
        factura = self.facturas.get(factura_id)
        if not factura:
            return False
        if cantidad_cajas is not None:
            factura.set_cantidad_cajas(cantidad_cajas)
        if precio_caja is not None:
            factura.set_precio_caja(precio_caja)
        if total is not None:
            factura.set_total(total)
        self.historial.append(("actualizar", factura_id))
        return True

    def buscar_por_cliente(self, cliente: str) -> list[Factura]:
        filtro = cliente.lower()
        return [
            factura
            for factura in self.facturas.values()
            if filtro in factura.get_cliente().lower()
        ]

    def mostrar_todas(self) -> list[Factura]:
        return list(self.facturas.values())

    def resumen_colecciones(self) -> dict[str, object]:
        return {
            "total_facturas": len(self.facturas),
            "ids": sorted(self.ids_registrados),
            "ultima_accion": self.historial[-1] if self.historial else None,
            "ids_como_tupla": tuple(sorted(self.ids_registrados)),
        }


def menu_consola() -> None:
    sistema = Inventario()

    while True:
        print("\n--- MENU FACTURACION LITOBANANO ---")
        print("1. Agregar factura")
        print("2. Eliminar factura")
        print("3. Actualizar factura")
        print("4. Buscar por cliente")
        print("5. Mostrar todas")
        print("6. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            factura_id = int(input("ID: "))
            numero = input("Número factura: ").strip()
            cliente = input("Cliente: ").strip()
            producto = input("Producto: ").strip()
            cantidad = int(input("Cajas: "))
            precio = float(input("Precio caja: "))
            total = round(cantidad * precio, 2)
            sistema.agregar_factura(
                Factura(factura_id, numero, cliente, producto, cantidad, precio, total)
            )
            print("Factura agregada.")
        elif opcion == "2":
            factura_id = int(input("ID a eliminar: "))
            print("Eliminada." if sistema.eliminar_factura(factura_id) else "No existe ese ID.")
        elif opcion == "3":
            factura_id = int(input("ID a actualizar: "))
            cantidad = int(input("Nueva cantidad: "))
            precio = float(input("Nuevo precio caja: "))
            total = round(cantidad * precio, 2)
            print(
                "Actualizada."
                if sistema.actualizar_factura(
                    factura_id,
                    cantidad_cajas=cantidad,
                    precio_caja=precio,
                    total=total,
                )
                else "No existe ese ID."
            )
        elif opcion == "4":
            cliente = input("Cliente a buscar: ").strip()
            resultados = sistema.buscar_por_cliente(cliente)
            for factura in resultados:
                print(factura.to_dict())
            if not resultados:
                print("Sin coincidencias.")
        elif opcion == "5":
            todas = sistema.mostrar_todas()
            for factura in todas:
                print(factura.to_dict())
            if not todas:
                print("No hay facturas en memoria.")
        elif opcion == "6":
            print("Saliendo del menú...")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu_consola()
