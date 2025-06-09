from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def hacer_sonido(self):
        pass

class Perro(Animal):
    def hacer_sonido(self):
        return "Guau"

class Gato(Animal):
    def hacer_sonido(self):
        return "Miau"

# Interacción con el usuario
print("Selecciona un animal:")
print("1. Perro")
print("2. Gato")
opcion = int(input("Ingresa el número de tu elección: "))

if opcion == 1:
    animal = Perro()
elif opcion == 2:
    animal = Gato()
else:
    print("Opción no válida")
    exit()

print(f"El sonido del animal seleccionado es: {animal.hacer_sonido()}")
