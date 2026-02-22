class CuentaBancaria:
    def __init__(self, titular, saldo):
        self.__titular = titular  # atributo privado
        self.__saldo = saldo

    def depositar(self, cantidad):
        self.__saldo += cantidad
        print(f"Has depositado {cantidad}. Saldo actual: {self.__saldo}")

    def retirar(self, cantidad):
        if cantidad <= self.__saldo:
            self.__saldo -= cantidad
            print(f"Has retirado {cantidad}. Saldo actual: {self.__saldo}")
        else:
            print("Fondos insuficientes")

    def obtener_saldo(self):
        return self.__saldo

# Interacción con el usuario
titular = input("Ingresa el nombre del titular: ")
saldo_inicial = float(input("Ingresa el saldo inicial: "))
cuenta = CuentaBancaria(titular, saldo_inicial)

while True:
    print("\nOpciones:")
    print("1. Depositar dinero")
    print("2. Retirar dinero")
    print("3. Consultar saldo")
    print("4. Salir")
    opcion = int(input("Selecciona una opción: "))

    if opcion == 1:
        cantidad = float(input("Ingresa la cantidad a depositar: "))
        cuenta.depositar(cantidad)
    elif opcion == 2:
        cantidad = float(input("Ingresa la cantidad a retirar: "))
        cuenta.retirar(cantidad)
    elif opcion == 3:
        print(f"El saldo actual es: {cuenta.obtener_saldo()}")
    elif opcion == 4:
        print("¡Gracias por usar la cuenta bancaria!")
        break
    else:
        print("Opción no válida")
