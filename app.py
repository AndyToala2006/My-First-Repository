from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Bienvenido al Sistema de Turnos – Clínica XYZ"

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f"Bienvenido, {nombre}. Tu turno está en proceso."

if __name__ == '__main__':
    app.run(debug=True)
