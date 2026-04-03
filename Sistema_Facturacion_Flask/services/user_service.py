from __future__ import annotations

from typing import Iterable

from werkzeug.security import check_password_hash, generate_password_hash

from Conexión.conexion import get_connection
from models.user import User


def get_user_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario = %s",
        (user_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        return None
    return User(
        id=row["id_usuario"],
        nombre=row["nombre"],
        email=row["email"],
        password_hash=row["password"],
    )


def get_user_by_email(email: str) -> User | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_usuario, nombre, email, password FROM usuarios WHERE email = %s",
        (email,),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        return None
    return User(
        id=row["id_usuario"],
        nombre=row["nombre"],
        email=row["email"],
        password_hash=row["password"],
    )


def create_user(nombre: str, email: str, password: str) -> User:
    password_hash = generate_password_hash(password)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
        (nombre, email, password_hash),
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return User(id=user_id, nombre=nombre, email=email, password_hash=password_hash)


def validate_login(email: str, password: str) -> User | None:
    user = get_user_by_email(email)
    if not user:
        return None
    if not check_password_hash(user.password_hash, password):
        return None
    return user


def list_users() -> list[User]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre, email, password FROM usuarios ORDER BY id_usuario DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        User(
            id=row["id_usuario"],
            nombre=row["nombre"],
            email=row["email"],
            password_hash=row["password"],
        )
        for row in rows
    ]
