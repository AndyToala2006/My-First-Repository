from __future__ import annotations

import csv
import json
import os
from datetime import date
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import func

from form import FacturaForm, RegistroOperacionForm
from inventario.bd import FacturaDB, db
from inventario.inventario import Inventario
from inventario.productos import Factura

BASE_DIR = Path(__file__).resolve().parent
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


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "litobanano-dev-key")
app.config["SQLALCHEMY_DATABASE_URI"] = _build_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
inventario_memoria = Inventario()

with app.app_context():
    db.create_all()


@app.route("/")
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
def usuario(nombre: str):
    return render_template("usuario.html", nombre=nombre, mensaje=f"Bienvenido, {nombre}.")


@app.route("/cliente/<nombre>")
def cliente(nombre: str):
    return render_template(
        "usuario.html",
        nombre=nombre,
        mensaje=f"Cliente {nombre}: su proceso de facturación de exportación está activo.",
    )


@app.route("/factura/<numero>")
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
def facturas():
    facturas_db = FacturaDB.query.order_by(FacturaDB.id.desc()).all()
    return render_template("productos.html", facturas=facturas_db)


@app.route("/productos")
def productos_legacy():
    return redirect(url_for("facturas"))


@app.route("/facturas/nueva", methods=["GET", "POST"])
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
def factura_eliminar(factura_id: int):
    factura_db = FacturaDB.query.get_or_404(factura_id)
    db.session.delete(factura_db)
    db.session.commit()
    inventario_memoria.eliminar_factura(factura_id)
    flash("Factura eliminada.", "ok")
    return redirect(url_for("facturas"))


@app.route("/datos", methods=["GET", "POST"])
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


if __name__ == "__main__":
    app.run(debug=True)
