# Función para obtener las temperaturas diarias
def obtener_temperaturas():
    temperaturas = []
    for dia in range(1, 8):  # 7 días de la semana
        temperatura = float(input(f"Introduce la temperatura del día {dia}: "))
        temperaturas.append(temperatura)
    return temperaturas

# Función para calcular el promedio de las temperaturas
def calcular_promedio(temperaturas):
    return sum(temperaturas) / len(temperaturas)

# Función principal que organiza el flujo
def main():
    print("Bienvenido al programa para calcular el promedio semanal del clima.")
    temperaturas = obtener_temperaturas()  # Obtener las temperaturas de la semana
    promedio = calcular_promedio(temperaturas)  # Calcular el promedio
    print(f"El promedio de la temperatura semanal es: {promedio:.2f}°C")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
