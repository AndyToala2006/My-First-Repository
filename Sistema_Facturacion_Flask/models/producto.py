from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Producto:
    id_producto: int
    nombre: str
    precio: float
    stock: int
