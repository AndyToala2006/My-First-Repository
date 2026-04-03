from __future__ import annotations

import io
import csv
import json
import os
from datetime import date\n\nfrom dotenv import load_dotenv\nfrom pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for, send_file
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from Conexión.conexion import (
    get_connection,
    init_schema,
    is_configured,
    ensure_facturas_columns,
    ensure_clientes_columns,
    ensure_productos_columns,
    ensure_detalle_columns,
    ensure_usuarios_columns,
)
from forms.auth_forms import LoginForm, RegisterForm, ProductoForm
from form import FacturaForm, RegistroOperacionForm
from inventario.bd import FacturaDB, db
from inventario.inventario import Inventario
from inventario.productos import Factura
from services.user_service import create_user, get_user_by_id, get_user_by_email, validate_login
from services.producto_service import list_productos, get_producto, create_producto, update_producto, delete_producto
from services.report_service import productos_pdf

load_dotenv()\n\nBASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "inventario" / "data"
TXT_PATH = DATA_DIR / "datos.txt"
JSON_PATH = DATA_DIR / "datos.json"
CSV_PATH = DATA_DIR / "datos.csv"


def _build_database_uri() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            return database_url.replace("postgres://", "postgresql://", 1)
        return database_url
    return f"sqlite:///{BASE_DIR / 'inventario.db'}"


def _generar_numero_factura() -> str:
    ultimo_id = db.session.query(func.max(FacturaDB.id)).scalar() or 0
    return f"LIT-{ultimo_id + 1:06d}"


def _append_txt(registro: dict[str, str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    linea = (
        f"{registro['fecha']} | {registro['numero_factura']} | "
        f"{registro['cliente']} | {registro['destino']} | ${registro['total']}\n"
    )
    with TXT_PATH.open("a", encoding="utf-8") as archivo:
        archivo.write(linea)


def _append_json(registro: dict[str, str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    registros: list[dict[str, str]] = []
    if JSON_PATH.exists() and JSON_PATH.read_text(encoding="utf-8-sig").strip():
        with JSON_PATH.open("r", encoding="utf-8-sig") as archivo:
            registros = json.load(archivo)
    registros.append(registro)
    with JSON_PATH.open("w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, ensure_ascii=False, indent=2)


def _append_csv(registro: dict[str, str]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    existe = CSV_PATH.exists() and CSV_PATH.read_text(encoding="utf-8-sig").strip()
    with CSV_PATH.open("a", encoding="utf-8", newline="") as archivo:
        writer = csv.DictWriter(
            archivo,
            fieldnames=["fecha", "numero_factura", "cliente", "destino", "total"],
        )
        if not existe:
            writer.writeheader()
        writer.writerow(registro)


def _read_txt() -> list[str]:
    if not TXT_PATH.exists():
        return []
    with TXT_PATH.open("r", encoding="utf-8-sig") as archivo:
        return [linea.strip() for linea in archivo.readlines() if linea.strip()]


def _read_json() -> list[dict[str, str]]:
    if not JSON_PATH.exists() or not JSON_PATH.read_text(encoding="utf-8-sig").strip():
        return []
    with JSON_PATH.open("r", encoding="utf-8-sig") as archivo:
        return json.load(archivo)


def _read_csv() -> list[dict[str, str]]:
    if not CSV_PATH.exists() or not CSV_PATH.read_text(encoding="utf-8-sig").strip():
        return []
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as archivo:
        reader = csv.DictReader(archivo)
        return list(reader)


def _mysql_ready() -> bool:
    if not is_configured():
        flash(
            "MySQL no está configurado. Define MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD y MYSQL_DATABASE.",
            "error",
        )
        return False
    try:
        init_schema()
        ensure_clientes_columns()
        ensure_productos_columns()
        ensure_facturas_columns()
        ensure_detalle_columns()
        ensure_usuarios_columns()
        return True
    except Exception as exc:
        flash(f"No se pudo conectar a MySQL: {exc}", "error")
        return False


def _mysql_fetch_all(query: str, params: tuple = ()) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def _mysql_fetch_one(query: str, params: tuple = ()) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def _mysql_execute(query: str, params: tuple = ()) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()


def _mysql_execute_returning_id(query: str, params: tuple = ()) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "litobanano-dev-key")
app.config["SQLALCHEMY_DATABASE_URI"] = _build_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

db.init_app(app)
inventario_memoria = Inventario()

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id: str):
    try:
        return get_user_by_id(int(user_id))
    except Exception:
        return None


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm.from_request(request)
    if request.method == "POST":
        errores = form.validate()
        if errores:
            for error in errores:
                flash(error, "error")
        else:
            user = validate_login(form.email, form.password)
            if user:
                login_user(user)
                flash("Bienvenido al sistema.", "ok")
                return redirect(url_for("index"))
            flash("Credenciales incorrectas.", "error")
    return render_template("auth/login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm.from_request(request)
    if request.method == "POST":
        errores = form.validate()
        if errores:
            for error in errores:
                flash(error, "error")
        else:
            if get_user_by_email(form.email):
                flash("Ese email ya está registrado.", "error")
            else:
                create_user(form.nombre, form.email, form.password)
                flash("Usuario registrado. Ahora inicia sesión.", "ok")
                return redirect(url_for("login"))
    return render_template("auth/register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "ok")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    total_facturas = FacturaDB.query.count()
    total_cajas = db.session.query(func.coalesce(func.sum(FacturaDB.cantidad_cajas), 0)).scalar()
    total_facturado = db.session.query(func.coalesce(func.sum(FacturaDB.total), 0.0)).scalar()
    ultimas_facturas = FacturaDB.query.order_by(FacturaDB.id.desc()).limit(5).all()
    return render_template(
        "index.html",
        total_facturas=total_facturas,
        total_cajas=total_cajas,
        total_facturado=total_facturado,
        ultimas_facturas=ultimas_facturas,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contactos")
def contactos():
    return render_template("contactos.html")


@app.route("/usuario/<nombre>")
@login_required
def usuario(nombre: str):
    return render_template("usuario.html", nombre=nombre, mensaje=f"Bienvenido, {nombre}.")


@app.route("/cliente/<nombre>")
@login_required
def cliente(nombre: str):
    return render_template(
        "usuario.html",
        nombre=nombre,
        mensaje=f"Cliente {nombre}: su proceso de facturación de exportación está activo.",
    )


@app.route("/factura/<numero>")
@login_required
def factura_por_numero(numero: str):
    factura_db = FacturaDB.query.filter_by(numero_factura=numero).first()
    if not factura_db:
        flash("No existe una factura con ese número.", "error")
        return redirect(url_for("facturas"))
    return render_template(
        "usuario.html",
        nombre=factura_db.cliente,
        mensaje=(
            f"Factura {factura_db.numero_factura}: {factura_db.producto} "
            f"destino {factura_db.destino}, total ${factura_db.total:.2f}."
        ),
    )


@app.route("/facturas")
@login_required
def facturas():
    facturas_db = FacturaDB.query.order_by(FacturaDB.id.desc()).all()
    return render_template("productos.html", facturas=facturas_db)


@app.route("/productos")
@login_required
def productos_list():
    if not _mysql_ready():
        return render_template("productos/list.html", productos=[])
    productos = list_productos()
    return render_template("productos/list.html", productos=productos)


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def productos_nuevo():
    if not _mysql_ready():
        return redirect(url_for("productos_list"))
    form = ProductoForm.from_request(request)
    if request.method == "POST":
        errores = form.validate()
        if errores:
            for error in errores:
                flash(error, "error")
        else:
            create_producto(form.nombre, form.precio, form.stock)
            flash("Producto creado.", "ok")
            return redirect(url_for("productos_list"))
    return render_template("productos/form.html", form=form, accion="Crear")


@app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
@login_required
def productos_editar(producto_id: int):
    if not _mysql_ready():
        return redirect(url_for("productos_list"))
    producto = get_producto(producto_id)
    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("productos_list"))
    form = ProductoForm(nombre=producto.nombre, precio=producto.precio, stock=producto.stock)
    if request.method == "POST":
        form = ProductoForm.from_request(request)
        errores = form.validate()
        if errores:
            for error in errores:
                flash(error, "error")
        else:
            update_producto(producto_id, form.nombre, form.precio, form.stock)
            flash("Producto actualizado.", "ok")
            return redirect(url_for("productos_list"))
    return render_template("productos/form.html", form=form, accion="Editar")


@app.route("/productos/<int:producto_id>/eliminar", methods=["POST"])
@login_required
def productos_eliminar(producto_id: int):
    if not _mysql_ready():
        return redirect(url_for("productos_list"))
    delete_producto(producto_id)
    flash("Producto eliminado.", "ok")
    return redirect(url_for("productos_list"))


@app.route("/reportes/productos.pdf")
@login_required
def reporte_productos_pdf():
    pdf_bytes = productos_pdf()
    return send_file(
        io.BytesIO(pdf_bytes),
        download_name="reporte_productos.pdf",
        mimetype="application/pdf",
        as_attachment=True,
    )


@app.route("/facturas/nueva", methods=["GET", "POST"])
@login_required
def factura_nueva():
    form = FacturaForm.from_request(request)
    if request.method == "POST":
        errores = form.validate()
        if errores:
            for error in errores:
                flash(error, "error")
        else:
            total = round(form.cantidad_cajas * form.precio_caja, 2)
            factura_db = FacturaDB(
                numero_factura=_generar_numero_factura(),
                fecha_emision=date.today(),
                cliente=form.cliente,
                ruc=form.ruc,
                destino=form.destino,
                producto=form.producto,
                cantidad_cajas=form.cantidad_cajas,
                precio_caja=form.precio_caja,
                total=total,
                estado=form.estado,
            )
            db.session.add(factura_db)
            db.session.commit()

            inventario_memoria.agregar_factura(
                Factura(
                    factura_db.id,
                    factura_db.numero_factura,
                    factura_db.cliente,
                    factura_db.producto,
                    factura_db.cantidad_cajas,
                    factura_db.precio_caja,
                    factura_db.total,
                )
            )

            flash("Factura registrada correctamente.", "ok")
            return redirect(url_for("facturas"))

    return render_template("producto_form.html", form=form, accion="Crear")


@app.route("/facturas/<int:factura_id>/editar", methods=["GET", "POST"])
@login_required
def factura_editar(factura_id: int):
    factura_db = FacturaDB.query.get_or_404(factura_id)

    if request.method == "POST":
        form = FacturaForm.from_request(request)
        errores = form.validate()
        if errores:
            for error in errores:
                flash(error, "error")
            return render_template("producto_form.html", form=form, accion="Editar")

        factura_db.cliente = form.cliente
        factura_db.ruc = form.ruc
        factura_db.destino = form.destino
        factura_db.producto = form.producto
        factura_db.cantidad_cajas = form.cantidad_cajas
        factura_db.precio_caja = form.precio_caja
        factura_db.total = round(form.cantidad_cajas * form.precio_caja, 2)
        factura_db.estado = form.estado
        db.session.commit()

        inventario_memoria.actualizar_factura(
            factura_db.id,
            cantidad_cajas=factura_db.cantidad_cajas,
            precio_caja=factura_db.precio_caja,
            total=factura_db.total,
        )

        flash("Factura actualizada correctamente.", "ok")
        return redirect(url_for("facturas"))

    form = FacturaForm(
        cliente=factura_db.cliente,
        ruc=factura_db.ruc,
        destino=factura_db.destino,
        producto=factura_db.producto,
        cantidad_cajas=factura_db.cantidad_cajas,
        precio_caja=factura_db.precio_caja,
        estado=factura_db.estado,
    )
    return render_template("producto_form.html", form=form, accion="Editar")


@app.route("/facturas/<int:factura_id>/eliminar", methods=["POST"])
@login_required
def factura_eliminar(factura_id: int):
    factura_db = FacturaDB.query.get_or_404(factura_id)
    db.session.delete(factura_db)
    db.session.commit()
    inventario_memoria.eliminar_factura(factura_id)
    flash("Factura eliminada.", "ok")
    return redirect(url_for("facturas"))


@app.route("/datos", methods=["GET", "POST"])
@login_required
def datos():
    form = RegistroOperacionForm.from_request(request)

    if request.method == "POST":
        errores = form.validate()
        if errores:
            for error in errores:
                flash(error, "error")
        else:
            registro = {
                "fecha": form.fecha,
                "numero_factura": form.numero_factura,
                "cliente": form.cliente,
                "destino": form.destino,
                "total": f"{form.total:.2f}",
            }
            if form.formato == "txt":
                _append_txt(registro)
            elif form.formato == "json":
                _append_json(registro)
            else:
                _append_csv(registro)
            flash(f"Registro almacenado en {form.formato.upper()}.", "ok")
            return redirect(url_for("datos"))

    return render_template(
        "datos.html",
        form=form,
        datos_txt=_read_txt(),
        datos_json=_read_json(),
        datos_csv=_read_csv(),
        resumen_memoria=inventario_memoria.resumen_colecciones(),
    )


@app.route("/mysql/usuarios")
@login_required
def mysql_usuarios():
    if not _mysql_ready():
        return render_template("usuarios_mysql.html", usuarios=[])

    usuarios = _mysql_fetch_all(
        "SELECT id_usuario, nombre, email, password FROM usuarios ORDER BY id_usuario DESC"
    )
    return render_template("usuarios_mysql.html", usuarios=usuarios)


@app.route("/mysql/usuarios/nuevo", methods=["GET", "POST"])
@login_required
def mysql_usuario_nuevo():
    if not _mysql_ready():
        return redirect(url_for("mysql_usuarios"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios.", "error")
        else:
            password_hash = generate_password_hash(password)
            _mysql_execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, password_hash),
            )
            flash("Usuario creado en MySQL.", "ok")
            return redirect(url_for("mysql_usuarios"))

    return render_template("usuario_mysql_form.html", usuario=None, accion="Crear")


@app.route("/mysql/usuarios/<int:usuario_id>/editar", methods=["GET", "POST"])
@login_required
def mysql_usuario_editar(usuario_id: int):
    if not _mysql_ready():
        return redirect(url_for("mysql_usuarios"))

    usuario = _mysql_fetch_one(
        "SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario = %s",
        (usuario_id,),
    )
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("mysql_usuarios"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios.", "error")
        else:
            password_hash = generate_password_hash(password)
            _mysql_execute(
                "UPDATE usuarios SET nombre=%s, email=%s, password=%s WHERE id_usuario=%s",
                (nombre, email, password_hash, usuario_id),
            )
            flash("Usuario actualizado.", "ok")
            return redirect(url_for("mysql_usuarios"))

    return render_template("usuario_mysql_form.html", usuario=usuario, accion="Editar")


@app.route("/mysql/usuarios/<int:usuario_id>/eliminar", methods=["POST"])
@login_required
def mysql_usuario_eliminar(usuario_id: int):
    if not _mysql_ready():
        return redirect(url_for("mysql_usuarios"))

    _mysql_execute("DELETE FROM usuarios WHERE id_usuario=%s", (usuario_id,))
    flash("Usuario eliminado.", "ok")
    return redirect(url_for("mysql_usuarios"))


@app.route("/mysql/facturas")
@login_required
def mysql_facturas():
    if not _mysql_ready():
        return render_template("facturas_mysql.html", facturas=[])

    facturas = _mysql_fetch_all(
        """
        SELECT
            f.id_factura,
            f.numero_factura,
            f.fecha,
            c.nombre AS cliente,
            c.ruc,
            f.destino,
            GROUP_CONCAT(p.nombre SEPARATOR ', ') AS productos,
            SUM(df.cantidad) AS total_cajas,
            SUM(df.precio_unitario) / COUNT(df.id_detalle) AS precio_caja,
            f.total,
            f.estado
        FROM facturas f
        JOIN clientes c ON f.id_cliente = c.id_cliente
        JOIN detalle_factura df ON f.id_factura = df.id_factura
        JOIN productos p ON df.id_producto = p.id_producto
        GROUP BY f.id_factura
        ORDER BY f.id_factura DESC
        """
    )
    return render_template("facturas_mysql.html", facturas=facturas)


@app.route("/mysql/facturas/nueva", methods=["GET", "POST"])
@login_required
def mysql_factura_nueva():
    if not _mysql_ready():
        return redirect(url_for("mysql_facturas"))

    if request.method == "POST":
        numero_factura = request.form.get("numero_factura", "").strip()
        fecha_emision = request.form.get("fecha_emision", str(date.today())).strip()
        cliente = request.form.get("cliente", "").strip()
        ruc = request.form.get("ruc", "").strip()
        destino = request.form.get("destino", "").strip()
        producto = request.form.get("producto", "").strip()
        cantidad_cajas = request.form.get("cantidad_cajas", "0").strip()
        precio_caja = request.form.get("precio_caja", "0").strip()
        estado = request.form.get("estado", "Emitida").strip()

        try:
            cantidad_cajas_int = int(cantidad_cajas)
            precio_caja_float = float(precio_caja)
        except ValueError:
            cantidad_cajas_int = -1
            precio_caja_float = -1

        if (
            not numero_factura
            or not cliente
            or not ruc
            or not destino
            or not producto
            or cantidad_cajas_int <= 0
            or precio_caja_float <= 0
        ):
            flash("Completa todos los campos con valores válidos.", "error")
        else:
            total = round(cantidad_cajas_int * precio_caja_float, 2)
            cliente_row = _mysql_fetch_one(
                "SELECT id_cliente FROM clientes WHERE ruc = %s",
                (ruc,),
            )
            if cliente_row:
                id_cliente = cliente_row["id_cliente"]
                _mysql_execute(
                    "UPDATE clientes SET nombre=%s WHERE id_cliente=%s",
                    (cliente, id_cliente),
                )
            else:
                id_cliente = _mysql_execute_returning_id(
                    "INSERT INTO clientes (nombre, ruc) VALUES (%s, %s)",
                    (cliente, ruc),
                )

            producto_row = _mysql_fetch_one(
                "SELECT id_producto FROM productos WHERE nombre = %s",
                (producto,),
            )
            if producto_row:
                id_producto = producto_row["id_producto"]
            else:
                id_producto = _mysql_execute_returning_id(
                    "INSERT INTO productos (nombre) VALUES (%s)",
                    (producto,),
                )

            id_factura = _mysql_execute_returning_id(
                """
                INSERT INTO facturas (
                    numero_factura, fecha, id_cliente, destino, total, estado
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    numero_factura,
                    fecha_emision,
                    id_cliente,
                    destino,
                    total,
                    estado,
                ),
            )

            _mysql_execute(
                """
                INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    id_factura,
                    id_producto,
                    cantidad_cajas_int,
                    precio_caja_float,
                ),
            )
            flash("Factura creada en MySQL.", "ok")
            return redirect(url_for("mysql_facturas"))

    return render_template("factura_mysql_form.html", factura=None, accion="Crear")


@app.route("/mysql/facturas/<int:factura_id>/editar", methods=["GET", "POST"])
@login_required
def mysql_factura_editar(factura_id: int):
    if not _mysql_ready():
        return redirect(url_for("mysql_facturas"))

    factura = _mysql_fetch_one(
        """
        SELECT
            f.id_factura,
            f.numero_factura,
            f.fecha,
            f.destino,
            f.total,
            f.estado,
            c.id_cliente,
            c.nombre AS cliente,
            c.ruc,
            p.id_producto,
            p.nombre AS producto,
            df.cantidad,
            df.precio_unitario
        FROM facturas f
        JOIN clientes c ON f.id_cliente = c.id_cliente
        JOIN detalle_factura df ON f.id_factura = df.id_factura
        JOIN productos p ON df.id_producto = p.id_producto
        WHERE f.id_factura = %s
        """,
        (factura_id,),
    )
    if not factura:
        flash("Factura no encontrada.", "error")
        return redirect(url_for("mysql_facturas"))

    if request.method == "POST":
        numero_factura = request.form.get("numero_factura", "").strip()
        fecha_emision = request.form.get("fecha_emision", str(factura["fecha"])).strip()
        cliente = request.form.get("cliente", "").strip()
        ruc = request.form.get("ruc", "").strip()
        destino = request.form.get("destino", "").strip()
        producto = request.form.get("producto", "").strip()
        cantidad_cajas = request.form.get("cantidad_cajas", "0").strip()
        precio_caja = request.form.get("precio_caja", "0").strip()
        estado = request.form.get("estado", "Emitida").strip()

        try:
            cantidad_cajas_int = int(cantidad_cajas)
            precio_caja_float = float(precio_caja)
        except ValueError:
            cantidad_cajas_int = -1
            precio_caja_float = -1

        if (
            not numero_factura
            or not cliente
            or not ruc
            or not destino
            or not producto
            or cantidad_cajas_int <= 0
            or precio_caja_float <= 0
        ):
            flash("Completa todos los campos con valores válidos.", "error")
        else:
            total = round(cantidad_cajas_int * precio_caja_float, 2)
            _mysql_execute(
                "UPDATE clientes SET nombre=%s, ruc=%s WHERE id_cliente=%s",
                (cliente, ruc, factura["id_cliente"]),
            )
            _mysql_execute(
                "UPDATE productos SET nombre=%s WHERE id_producto=%s",
                (producto, factura["id_producto"]),
            )
            _mysql_execute(
                """
                UPDATE facturas
                SET numero_factura=%s, fecha=%s, id_cliente=%s, destino=%s, total=%s, estado=%s
                WHERE id_factura=%s
                """,
                (
                    numero_factura,
                    fecha_emision,
                    factura["id_cliente"],
                    destino,
                    total,
                    estado,
                    factura_id,
                ),
            )
            _mysql_execute(
                """
                UPDATE detalle_factura
                SET id_producto=%s, cantidad=%s, precio_unitario=%s
                WHERE id_factura=%s
                """,
                (
                    factura["id_producto"],
                    cantidad_cajas_int,
                    precio_caja_float,
                    factura_id,
                ),
            )
            flash("Factura actualizada.", "ok")
            return redirect(url_for("mysql_facturas"))

    return render_template("factura_mysql_form.html", factura=factura, accion="Editar")


@app.route("/mysql/facturas/<int:factura_id>/eliminar", methods=["POST"])
@login_required
def mysql_factura_eliminar(factura_id: int):
    if not _mysql_ready():
        return redirect(url_for("mysql_facturas"))

    _mysql_execute("DELETE FROM detalle_factura WHERE id_factura=%s", (factura_id,))
    _mysql_execute("DELETE FROM facturas WHERE id_factura=%s", (factura_id,))
    flash("Factura eliminada.", "ok")
    return redirect(url_for("mysql_facturas"))


if __name__ == "__main__":
    app.run(debug=True)




