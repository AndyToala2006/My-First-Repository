# 1. Crear un Diccionario
informacion_personal = {
    "nombre": "Juan Pérez",   # Nombre de la persona
    "edad": 30,               # Edad de la persona
    "ciudad": "Quito",        # Ciudad de residencia
    "profesion": "Ingeniero"  # Profesión de la persona
}

# 2. Acceder y Modificar Valores
def modificar_ciudad(nueva_ciudad):
    """Función para modificar la ciudad en el diccionario."""
    ciudad_actual = informacion_personal["ciudad"]
    print(f"Ciudad actual: {ciudad_actual}")  # Mostrar ciudad actual
    informacion_personal["ciudad"] = nueva_ciudad  # Actualizar ciudad
    print(f"Nueva ciudad: {informacion_personal['ciudad']}")  # Mostrar nueva ciudad

# Llamar a la función para modificar la ciudad
modificar_ciudad("Guayaquil")

# Agregar una nueva clave-valor para la profesión
informacion_personal["profesion"] = "Desarrollador de Software"

# 3. Verificar Existencia de Claves
def agregar_telefono(numero):
    """Función para agregar un número de teléfono si no existe."""
    if "telefono" not in informacion_personal:
        informacion_personal["telefono"] = numero  # Agregar número de teléfono ficticio
        print(f"Número de teléfono agregado: {informacion_personal['telefono']}")

# Llamar a la función para agregar el teléfono
agregar_telefono("0999999999")

# 4. Eliminar una Clave
def eliminar_edad():
    """Función para eliminar la clave 'edad' del diccionario."""
    if "edad" in informacion_personal:
        del informacion_personal["edad"]  # Eliminar clave 'edad'
        print("La clave 'edad' ha sido eliminada.")

# Llamar a la función para eliminar la edad
eliminar_edad()

# 5. Imprimir el Diccionario Final
def imprimir_diccionario():
    """Función para imprimir el diccionario final."""
    print("Diccionario final:")
    for clave, valor in informacion_personal.items():
        print(f"{clave}: {valor}")

# Llamar a la función para imprimir el diccionario final
imprimir_diccionario()
