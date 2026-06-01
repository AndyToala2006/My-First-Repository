import tkinter as tk
from tkinter import messagebox

def agregar_tarea(event=None):
    tarea = entrada_tarea.get().strip()
    if tarea:
        lista_tareas.insert(tk.END, tarea)
        entrada_tarea.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "No puedes añadir una tarea vacía.")

def marcar_completada():
    try:
        seleccion = lista_tareas.curselection()[0]
        tarea = lista_tareas.get(seleccion)
        lista_tareas.delete(seleccion)
        lista_tareas.insert(seleccion, f"✔ {tarea}")
    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una tarea para marcarla como completada.")

def eliminar_tarea():
    try:
        seleccion = lista_tareas.curselection()[0]
        lista_tareas.delete(seleccion)
    except IndexError:
        messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar.")

# Configurar la ventana principal
root = tk.Tk()
root.title("Lista de Tareas")
root.geometry("400x300")

# Campo de entrada
etiqueta = tk.Label(root, text="Nueva Tarea:")
etiqueta.pack()
entrada_tarea = tk.Entry(root, width=40)
entrada_tarea.pack()
entrada_tarea.bind("<Return>", agregar_tarea)  # Permitir agregar con Enter

# Lista de tareas
lista_tareas = tk.Listbox(root, width=50, height=10)
lista_tareas.pack()

# Botones
btn_agregar = tk.Button(root, text="Añadir Tarea", command=agregar_tarea)
btn_agregar.pack()
btn_completar = tk.Button(root, text="Marcar como Completada", command=marcar_completada)
btn_completar.pack()
btn_eliminar = tk.Button(root, text="Eliminar Tarea", command=eliminar_tarea)
btn_eliminar.pack()

# Ejecutar la aplicación
root.mainloop()
