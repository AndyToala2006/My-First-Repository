# Abrir el archivo en modo 'write' para escribir el contenido
file = open("my_notes.txt", "w")  # 'w' es para escribir
# Escribir tres líneas de notas personales
file.write("Mi nombre es Andy Jair Toala Angulo, tengo 18 años de edad.\n")
file.write("Estudio la carrera de Ingeniería en Tecnologías de la Información en la Universidad Estatal Amazónica.\n")
file.write("Trabajo como Jefe de Bodegas en la empresa Litobanano S.A.\n")
file.write("Disfruto ir al gimnasio con mi familia.\n")
file.write("Me gusta divertirme los fines de semana que tengo tiempo libre.\n")
# Cerrar el archivo después de escribir
file.close()

# Abrir el archivo en modo lectura
file = open("my_notes.txt", "r")  # Abre el archivo en modo lectura
# Leer y mostrar cada línea del archivo
line = file.readline()  # Lee la primera línea
while line:
    print(line.strip())  # Muestra cada línea sin el salto de línea adicional
    line = file.readline()  # Lee la siguiente línea
# Cerrar el archivo después de leer
file.close()
