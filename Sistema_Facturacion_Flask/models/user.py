from __future__ import annotations

from dataclasses import dataclass

from flask_login import UserMixin


@dataclass
class User(UserMixin):
    id: int
    nombre: str
    email: str
    password_hash: str

    def get_id(self) -> str:
        return str(self.id)
