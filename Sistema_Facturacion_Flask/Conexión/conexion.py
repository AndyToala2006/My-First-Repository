from __future__ import annotations

import os
import mysql.connector

from dataclasses import dataclass


@dataclass
class MysqlConfig:
    host: str
    user: str
    password: str
    database: str
    port: int


def _load_config() -> MysqlConfig:
    host = os.getenv("MYSQL_HOST", "")
    user = os.getenv("MYSQL_USER", "")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    return MysqlConfig(host=host, user=user, password=password, database=database, port=port)


def is_configured() -> bool:
    cfg = _load_config()
    return all([cfg.host, cfg.user, cfg.password, cfg.database])


def get_connection():
    cfg = _load_config()
    return mysql.connector.connect(
        host=cfg.host,
        user=cfg.user,
        password=cfg.password,
        database=cfg.database,
        port=cfg.port,
    )


def init_schema() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            mail VARCHAR(120) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(120) NOT NULL,
            ruc VARCHAR(20) NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(120) NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS facturas (
            id_factura INT AUTO_INCREMENT PRIMARY KEY,
            numero_factura VARCHAR(20) NOT NULL,
            fecha DATE NOT NULL,
            id_cliente INT NOT NULL,
            destino VARCHAR(80) NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            estado VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS detalle_factura (
            id_detalle INT AUTO_INCREMENT PRIMARY KEY,
            id_factura INT NOT NULL,
            id_producto INT NOT NULL,
            cantidad INT NOT NULL,
            precio_unitario DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (id_factura) REFERENCES facturas(id_factura),
            FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
        )
        """
    )

    conn.commit()
    cursor.close()
    conn.close()


def _column_exists(cursor, table_name: str, column_name: str) -> bool:
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.columns
        WHERE table_schema = %s AND table_name = %s AND column_name = %s
        """,
        (_load_config().database, table_name, column_name),
    )
    return cursor.fetchone()[0] > 0


def ensure_facturas_columns() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS facturas (
            id_factura INT AUTO_INCREMENT PRIMARY KEY,
            numero_factura VARCHAR(20) NOT NULL
        )
        """
    )

    required_columns = {
        "fecha": "DATE NOT NULL",
        "id_cliente": "INT NOT NULL",
        "destino": "VARCHAR(80) NOT NULL",
        "total": "DECIMAL(10,2) NOT NULL",
        "estado": "VARCHAR(20) NOT NULL",
    }

    for col, ddl in required_columns.items():
        if not _column_exists(cursor, "facturas", col):
            cursor.execute(f"ALTER TABLE facturas ADD COLUMN {col} {ddl}")

    conn.commit()
    cursor.close()
    conn.close()


def ensure_clientes_columns() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(120) NOT NULL,
            ruc VARCHAR(20) NOT NULL
        )
        """
    )

    required_columns = {
        "nombre": "VARCHAR(120) NOT NULL",
        "ruc": "VARCHAR(20) NOT NULL",
    }

    for col, ddl in required_columns.items():
        if not _column_exists(cursor, "clientes", col):
            cursor.execute(f"ALTER TABLE clientes ADD COLUMN {col} {ddl}")

    conn.commit()
    cursor.close()
    conn.close()


def ensure_productos_columns() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(120) NOT NULL
        )
        """
    )

    if not _column_exists(cursor, "productos", "nombre"):
        cursor.execute("ALTER TABLE productos ADD COLUMN nombre VARCHAR(120) NOT NULL")

    conn.commit()
    cursor.close()
    conn.close()


def ensure_detalle_columns() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS detalle_factura (
            id_detalle INT AUTO_INCREMENT PRIMARY KEY,
            id_factura INT NOT NULL,
            id_producto INT NOT NULL,
            cantidad INT NOT NULL,
            precio_unitario DECIMAL(10,2) NOT NULL
        )
        """
    )

    required_columns = {
        "id_factura": "INT NOT NULL",
        "id_producto": "INT NOT NULL",
        "cantidad": "INT NOT NULL",
        "precio_unitario": "DECIMAL(10,2) NOT NULL",
    }

    for col, ddl in required_columns.items():
        if not _column_exists(cursor, "detalle_factura", col):
            cursor.execute(f"ALTER TABLE detalle_factura ADD COLUMN {col} {ddl}")

    conn.commit()
    cursor.close()
    conn.close()
