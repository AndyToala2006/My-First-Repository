# Definir una matriz de 3x3 con valores numéricos
matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]


def buscar_valor(matriz, valor):
    """
    Busca un valor en la matriz y muestra su posición si se encuentra.

    Parámetros:
    matriz (list of lists): Matriz bidimensional con valores numéricos.
    valor (int): Valor a buscar en la matriz.
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == valor:
                return (i, j)  # Retorna la posición (fila, columna)
    return None  # Retorna None si no encuentra el valor


# Valor a buscar
valor_a_buscar = 5

# Buscar el valor en la matriz
posicion = buscar_valor(matriz, valor_a_buscar)

# Mostrar el resultado
if posicion:
    print(f"El valor {valor_a_buscar} se encontró en la posición ({posicion[0]}, {posicion[1]}) de la matriz.")
else:
    print(f"El valor {valor_a_buscar} no se encontró en la matriz.")