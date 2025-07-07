class Vehiculo:
    def __init__(self, marca):
        self.marca = marca

    def mover(self):
        return "El vehículo se está moviendo."

class Coche(Vehiculo):
    def mover(self):
        return "El coche está rodando por la carretera."

class Barco(Vehiculo):
    def mover(self):
        return "El barco navega por el agua."

# Interacción con el usuario
print("Selecciona un vehículo:")
print("1. Coche")
print("2. Barco")
opcion = int(input("Ingresa el número de tu elección: "))

marca = input("Ingresa la marca del vehículo: ")

if opcion == 1:
    vehiculo = Coche(marca)
elif opcion == 2:
    vehiculo = Barco(marca)
else:
    print("Opción no válida")
    exit()

print(f"Has elegido un {vehiculo.marca}. {vehiculo.mover()}")
