# Programa para calcular el área de un círculo
# Este programa solicita el radio de un círculo y calcula su área.

import math  # Importamos el módulo math para usar la constante pi


def calcular_area_circulo(radio):
    """
    Función para calcular el área de un círculo.

    Parámetros:
    radio (float): El radio del círculo.

    Retorna:
    float: El área del círculo calculada con la fórmula pi * radio^2.
    """
    # Calculamos el área usando la fórmula
    area = math.pi * radio ** 2
    return area


def obtener_radio():
    """
    Función para obtener el radio del usuario.

    Retorna:
    float: El radio proporcionado por el usuario.
    """
    # Solicitamos al usuario el radio
    while True:
        try:
            radio = float(input("Ingresa el radio del círculo: "))
            if radio > 0:
                return radio
            else:
                print("El radio debe ser un número positivo.")
        except ValueError:
            print("Por favor, ingresa un número válido para el radio.")


def main():
    """
    Función principal para ejecutar el programa.
    """
    # Obtenemos el radio
    radio = obtener_radio()

    # Calculamos el área
    area = calcular_area_circulo(radio)

    # Mostramos el resultado
    print(f"El área del círculo con radio {radio} es: {area:.2f} unidades cuadradas.")


# Ejecutamos la función principal
if __name__ == "__main__":
    main()
