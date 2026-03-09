from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class FacturaDB(db.Model):
    __tablename__ = "facturas"

    id = db.Column(db.Integer, primary_key=True)
    numero_factura = db.Column(db.String(20), unique=True, nullable=False)
    fecha_emision = db.Column(db.Date, nullable=False)
    cliente = db.Column(db.String(120), nullable=False)
    ruc = db.Column(db.String(20), nullable=False)
    destino = db.Column(db.String(80), nullable=False)
    producto = db.Column(db.String(120), nullable=False)
    cantidad_cajas = db.Column(db.Integer, nullable=False)
    precio_caja = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="Emitida")

    def __repr__(self) -> str:
        return f"FacturaDB(id={self.id}, numero='{self.numero_factura}')"
