# Función para calcular el descuento
def calcular_descuento(monto_total, porcentaje_descuento=10):
    descuento = monto_total * (porcentaje_descuento / 100)
    return descuento

# Función principal que interactúa con el usuario
def main():
    # Primera llamada: usando el valor predeterminado del 10%
    monto1 = float(input("Ingresa el monto total de la primera compra: $"))
    descuento1 = calcular_descuento(monto1)
    monto_final1 = monto1 - descuento1
    print(f"\nPrimera compra:")
    print(f"Monto total: ${monto1:.2f}")
    print(f"Descuento aplicado (10%): ${descuento1:.2f}")
    print(f"Monto final a pagar: ${monto_final1:.2f}\n")

    # Segunda llamada: el usuario elige el porcentaje de descuento
    monto2 = float(input("Ingresa el monto total de la segunda compra: $"))
    porcentaje2 = float(input("Ingresa el porcentaje de descuento para la segunda compra: "))
    descuento2 = calcular_descuento(monto2, porcentaje2)
    monto_final2 = monto2 - descuento2
    print(f"\nSegunda compra:")
    print(f"Monto total: ${monto2:.2f}")
    print(f"Descuento Aplicado ({porcentaje2}%): ${descuento2:.2f}")
    print(f"Monto final a pagar: ${monto_final2:.2f}")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
