def bubble_sort(fila):
    """
    Ordena una lista en orden ascendente usando el algoritmo de Bubble Sort.

    Parámetros:
    fila (list): Lista de valores numéricos a ordenar.
    """
    n = len(fila)
    for i in range(n):
        for j in range(0, n - i - 1):
            if fila[j] > fila[j + 1]:
                fila[j], fila[j + 1] = fila[j + 1], fila[j]


def ordenar_fila(matriz, fila_index):
    """
    Ordena una fila específica de la matriz usando Bubble Sort.

    Parámetros:
    matriz (list of lists): Matriz bidimensional con valores numéricos.
    fila_index (int): Índice de la fila a ordenar.
    """
    if 0 <= fila_index < len(matriz):
        bubble_sort(matriz[fila_index])
    else:
        print("Índice de fila fuera de rango.")


# Definir una matriz de 3x3 con valores numéricos
matriz = [
    [9, 2, 5],
    [4, 7, 1],
    [8, 3, 6]
]

# Mostrar la matriz original
print("Matriz original:")
for fila in matriz:
    print(fila)

# Seleccionar el índice de la fila a ordenar
fila_a_ordenar = matriz.index([4, 7, 1])  # Encuentra el índice de la fila [4, 7, 1]

# Ordenar la fila específica
ordenar_fila(matriz, fila_a_ordenar)

# Mostrar la matriz con la fila ordenada
print("\nMatriz con la fila ordenada:")
for fila in matriz:
    print(fila)
