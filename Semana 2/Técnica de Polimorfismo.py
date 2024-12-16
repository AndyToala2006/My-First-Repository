class Ave:
    def volar(self):
        return "Puede volar"

class Pingüino(Ave):
    def volar(self):
        return "No puede volar, pero nada muy bien"

class Aguila(Ave):
    def volar(self):
        return "Vuela alto y rápido"

# Interacción con el usuario
print("Selecciona un ave:")
print("1. Pingüino")
print("2. Águila")
opcion = int(input("Ingresa el número de tu elección: "))

if opcion == 1:
    ave = Pingüino()
elif opcion == 2:
    ave = Aguila()
else:
    print("Opción no válida")
    exit()

print(f"El comportamiento del ave seleccionada: {ave.volar()}")
