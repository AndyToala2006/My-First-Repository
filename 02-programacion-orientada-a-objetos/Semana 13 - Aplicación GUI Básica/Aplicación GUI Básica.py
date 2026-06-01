import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Aplicación GUI Básica")

# Crear una lista para almacenar los datos ingresados
datos = []

# Función para agregar información
def agregar_dato():
    dato = campo_texto.get()  # Obtener el texto ingresado en el campo
    if dato:  # Si el campo no está vacío
        datos.append(dato)  # Agregar el dato a la lista
        actualizar_lista()  # Actualizar la lista mostrada
        campo_texto.delete(0, tk.END)  # Limpiar el campo de texto
    else:
        messagebox.showwarning("Entrada vacía", "Por favor ingrese un dato.")

# Función para limpiar la información
def limpiar():
    campo_texto.delete(0, tk.END)  # Limpiar el campo de texto
    lista_datos.delete(0, tk.END)  # Limpiar la lista de datos

# Función para actualizar la lista con los datos actuales
def actualizar_lista():
    lista_datos.delete(0, tk.END)  # Limpiar la lista
    for dato in datos:  # Agregar todos los datos a la lista
        lista_datos.insert(tk.END, dato)

# Crear los componentes GUI
etiqueta = tk.Label(ventana, text="Ingrese un dato:")
etiqueta.pack(pady=10)

campo_texto = tk.Entry(ventana, width=30)
campo_texto.pack(pady=5)

boton_agregar = tk.Button(ventana, text="Agregar", command=agregar_dato)
boton_agregar.pack(pady=5)

boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar)
boton_limpiar.pack(pady=5)

# Crear la lista para mostrar los datos agregados
lista_datos = tk.Listbox(ventana, width=40, height=10)
lista_datos.pack(pady=10)

# Iniciar la aplicación
ventana.mainloop()