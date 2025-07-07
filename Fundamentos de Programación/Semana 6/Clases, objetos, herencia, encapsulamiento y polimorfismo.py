# Clase base Vehiculo
class Vehiculo:
    def __init__(self, marca, modelo, velocidad_maxima):
        self.marca = marca
        self.modelo = modelo
        self.__velocidad_maxima = velocidad_maxima  # Atributo privado, encapsulación

    # Método getter para acceder a la velocidad máxima
    def obtener_velocidad_maxima(self):
        return self.__velocidad_maxima

    # Método setter para modificar la velocidad máxima
    def establecer_velocidad_maxima(self, velocidad):
        if velocidad > 0:
            self.__velocidad_maxima = velocidad
        else:
            print("La velocidad máxima debe ser positiva.")

    # Método general para mover el vehículo (polimorfismo)
    def mover(self):
        return f"El vehículo {self.marca} {self.modelo} se mueve a {self.__velocidad_maxima} km/h."


# Clase derivada Auto
class Auto(Vehiculo):
    def __init__(self, marca, modelo, velocidad_maxima, tipo_combustible):
        super().__init__(marca, modelo, velocidad_maxima)  # Llamamos al constructor de la clase base
        self.tipo_combustible = tipo_combustible

    # Sobrescritura del método mover (polimorfismo)
    def mover(self):
        return f"El auto {self.marca} {self.modelo} funciona con {self.tipo_combustible} y se mueve a {self.obtener_velocidad_maxima()} km/h."

    # Método adicional para mostrar información del auto
    def informacion(self):
        return f"{self.marca} {self.modelo} - Tipo de combustible: {self.tipo_combustible}"


# Clase derivada Bicicleta
class Bicicleta(Vehiculo):
    def __init__(self, marca, modelo, velocidad_maxima, tipo_frenos):
        super().__init__(marca, modelo, velocidad_maxima)  # Llamamos al constructor de la clase base
        self.tipo_frenos = tipo_frenos

    # Sobrescritura del método mover (polimorfismo)
    def mover(self):
        return f"La bicicleta {self.marca} {self.modelo} tiene frenos de tipo {self.tipo_frenos} y se mueve a {self.obtener_velocidad_maxima()} km/h."

    # Método adicional para mostrar información de la bicicleta
    def informacion(self):
        return f"{self.marca} {self.modelo} - Tipo de frenos: {self.tipo_frenos}"


# Función interactiva con el usuario para gestionar vehículos
def interactuar_con_usuario():
    print("¡Bienvenido al sistema de gestión de vehículos!")

    # Solicitar información del usuario
    tipo_vehiculo = input("¿Qué tipo de vehículo desea registrar? (Auto/Bicicleta): ").lower()

    marca = input("Ingrese la marca del vehículo: ")
    modelo = input("Ingrese el modelo del vehículo: ")
    velocidad_maxima = int(input("Ingrese la velocidad máxima del vehículo (km/h): "))

    if tipo_vehiculo == "auto":
        tipo_combustible = input("Ingrese el tipo de combustible (Gasolina/Eléctrico): ")
        auto = Auto(marca, modelo, velocidad_maxima, tipo_combustible)
        print(auto.informacion())
        print(auto.mover())
    elif tipo_vehiculo == "bicicleta":
        tipo_frenos = input("Ingrese el tipo de frenos (Disco/Caliper): ")
        bicicleta = Bicicleta(marca, modelo, velocidad_maxima, tipo_frenos)
        print(bicicleta.informacion())
        print(bicicleta.mover())
    else:
        print("Tipo de vehículo no válido. Solo se aceptan 'Auto' o 'Bicicleta'.")


# Ejecutar la interacción
interactuar_con_usuario()
