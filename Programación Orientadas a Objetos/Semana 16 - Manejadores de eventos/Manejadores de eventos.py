import tkinter as tk
from tkinter import messagebox

def add_task(event=None):
    task = entry.get().strip()
    if task:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "No se puede añadir una tarea vacía.")

def mark_completed(event=None):
    try:
        selected = listbox.curselection()[0]
        task = listbox.get(selected)
        listbox.delete(selected)
        listbox.insert(selected, f"✔ {task}")
    except IndexError:
        messagebox.showwarning("Advertencia", "Seleccione una tarea para marcar como completada.")

def delete_task(event=None):
    try:
        selected = listbox.curselection()[0]
        listbox.delete(selected)
    except IndexError:
        messagebox.showwarning("Advertencia", "Seleccione una tarea para eliminar.")

def close_app(event=None):
    root.quit()

root = tk.Tk()
root.title("Gestor de Tareas")
root.geometry("400x400")

frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(frame, width=40)
entry.pack(side=tk.LEFT, padx=5)
entry.bind("<Return>", add_task)

add_button = tk.Button(frame, text="Añadir", command=add_task)
add_button.pack(side=tk.LEFT)

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

complete_button = tk.Button(button_frame, text="Marcar Completada", command=mark_completed)
complete_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Eliminar", command=delete_task)
delete_button.pack(side=tk.LEFT, padx=5)

root.bind("c", mark_completed)
root.bind("d", delete_task)
root.bind("<Delete>", delete_task)
root.bind("<Escape>", close_app)

root.mainloop()