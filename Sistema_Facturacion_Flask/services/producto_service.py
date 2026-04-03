from __future__ import annotations

from models.producto import Producto
from Conexión.conexion import get_connection


def list_productos() -> list[Producto]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_producto, nombre, precio, stock FROM productos ORDER BY id_producto DESC"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        Producto(
            id_producto=row["id_producto"],
            nombre=row["nombre"],
            precio=float(row["precio"]),
            stock=int(row["stock"]),
        )
        for row in rows
    ]


def get_producto(producto_id: int) -> Producto | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_producto, nombre, precio, stock FROM productos WHERE id_producto = %s",
        (producto_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        return None
    return Producto(
        id_producto=row["id_producto"],
        nombre=row["nombre"],
        precio=float(row["precio"]),
        stock=int(row["stock"]),
    )


def create_producto(nombre: str, precio: float, stock: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
        (nombre, precio, stock),
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def update_producto(producto_id: int, nombre: str, precio: float, stock: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s",
        (nombre, precio, stock, producto_id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def delete_producto(producto_id: int) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto=%s", (producto_id,))
    conn.commit()
    cursor.close()
    conn.close()
