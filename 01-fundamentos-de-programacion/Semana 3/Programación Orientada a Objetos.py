class ClimaDiario:
    def __init__(self, dia, temperatura):
        self.dia = dia
        self.temperatura = temperatura

    # Metodo para mostrar información del clima
    def mostrar_informacion(self):
        print(f"El clima del día {self.dia} fue de {self.temperatura}°C.")


class PromedioClima:
    def __init__(self):
        self.dias = []

    # Metodo para agregar un clima diario
    def agregar_clima(self, clima):
        self.dias.append(clima)

    # Metodo para calcular el promedio de temperaturas
    def calcular_promedio(self):
        total_temperaturas = sum(clima.temperatura for clima in self.dias)
        return total_temperaturas / len(self.dias)

    # Metodo para mostrar la información de todos los días
    def mostrar_informacion(self):
        for clima in self.dias:
            clima.mostrar_informacion()


# Función principal
def main():
    print("Bienvenido al programa de clima con Programación Orientada a Objetos.")

    # Crear una instancia de PromedioClima
    promedio_clima = PromedioClima()

    # Obtener las temperaturas diarias
    for dia in range(1, 8):
        temperatura = float(input(f"Introduce la temperatura del día {dia}: "))
        clima = ClimaDiario(dia, temperatura)
        promedio_clima.agregar_clima(clima)

    # Mostrar la información y calcular el promedio
    promedio_clima.mostrar_informacion()
    promedio = promedio_clima.calcular_promedio()
    print(f"El promedio de la temperatura semanal es: {promedio:.2f}°C")


# Ejecutar la función principal
if __name__ == "__main__":
    main()