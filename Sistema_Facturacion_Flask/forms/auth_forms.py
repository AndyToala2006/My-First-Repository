from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LoginForm:
    email: str = ""
    password: str = ""

    @classmethod
    def from_request(cls, request):
        return cls(
            email=request.form.get("email", "").strip(),
            password=request.form.get("password", "").strip(),
        )

    def validate(self) -> list[str]:
        errores: list[str] = []
        if not self.email:
            errores.append("El email es obligatorio.")
        if not self.password:
            errores.append("La contraseña es obligatoria.")
        return errores


@dataclass
class RegisterForm:
    nombre: str = ""
    email: str = ""
    password: str = ""

    @classmethod
    def from_request(cls, request):
        return cls(
            nombre=request.form.get("nombre", "").strip(),
            email=request.form.get("email", "").strip(),
            password=request.form.get("password", "").strip(),
        )

    def validate(self) -> list[str]:
        errores: list[str] = []
        if not self.nombre:
            errores.append("El nombre es obligatorio.")
        if not self.email:
            errores.append("El email es obligatorio.")
        if len(self.password) < 6:
            errores.append("La contraseña debe tener al menos 6 caracteres.")
        return errores


@dataclass
class ProductoForm:
    nombre: str = ""
    precio: float = 0.0
    stock: int = 0

    @classmethod
    def from_request(cls, request):
        nombre = request.form.get("nombre", "").strip()
        precio_raw = request.form.get("precio", "0").strip()
        stock_raw = request.form.get("stock", "0").strip()
        try:
            precio = float(precio_raw)
        except ValueError:
            precio = -1.0
        stock = int(stock_raw) if stock_raw.isdigit() else -1
        return cls(nombre=nombre, precio=precio, stock=stock)

    def validate(self) -> list[str]:
        errores: list[str] = []
        if not self.nombre:
            errores.append("El nombre es obligatorio.")
        if self.precio <= 0:
            errores.append("El precio debe ser mayor a 0.")
        if self.stock < 0:
            errores.append("El stock debe ser mayor o igual a 0.")
        return errores
