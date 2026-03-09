from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class FacturaForm:
    cliente: str = ""
    ruc: str = ""
    destino: str = ""
    producto: str = ""
    cantidad_cajas: int = 0
    precio_caja: float = 0.0
    estado: str = "Emitida"

    @classmethod
    def from_request(cls, request):
        cliente = request.form.get("cliente", "").strip()
        ruc = request.form.get("ruc", "").strip()
        destino = request.form.get("destino", "").strip()
        producto = request.form.get("producto", "").strip()
        cantidad_raw = request.form.get("cantidad_cajas", "0").strip()
        precio_raw = request.form.get("precio_caja", "0").strip()
        estado = request.form.get("estado", "Emitida").strip()

        cantidad_cajas = int(cantidad_raw) if cantidad_raw.isdigit() else -1
        try:
            precio_caja = float(precio_raw)
        except ValueError:
            precio_caja = -1.0

        return cls(
            cliente=cliente,
            ruc=ruc,
            destino=destino,
            producto=producto,
            cantidad_cajas=cantidad_cajas,
            precio_caja=precio_caja,
            estado=estado,
        )

    def validate(self) -> list[str]:
        errores: list[str] = []
        if not self.cliente:
            errores.append("El cliente es obligatorio.")
        if len(self.ruc) < 10:
            errores.append("El RUC debe tener al menos 10 dígitos.")
        if not self.destino:
            errores.append("El destino de exportación es obligatorio.")
        if not self.producto:
            errores.append("El producto facturado es obligatorio.")
        if self.cantidad_cajas <= 0:
            errores.append("La cantidad de cajas debe ser mayor a 0.")
        if self.precio_caja <= 0:
            errores.append("El precio por caja debe ser mayor a 0.")
        if self.estado not in {"Emitida", "Pagada", "Pendiente"}:
            errores.append("Estado de factura no válido.")
        return errores


@dataclass
class RegistroOperacionForm:
    fecha: str = ""
    numero_factura: str = ""
    cliente: str = ""
    destino: str = ""
    total: float = 0.0
    formato: str = "txt"

    @classmethod
    def from_request(cls, request):
        fecha = request.form.get("fecha", str(date.today())).strip()
        numero_factura = request.form.get("numero_factura", "").strip()
        cliente = request.form.get("cliente", "").strip()
        destino = request.form.get("destino", "").strip()
        total_raw = request.form.get("total", "0").strip()
        formato = request.form.get("formato", "txt").strip().lower()

        try:
            total = float(total_raw)
        except ValueError:
            total = -1.0

        return cls(
            fecha=fecha,
            numero_factura=numero_factura,
            cliente=cliente,
            destino=destino,
            total=total,
            formato=formato,
        )

    def validate(self) -> list[str]:
        errores: list[str] = []
        if not self.fecha:
            errores.append("La fecha es obligatoria.")
        if not self.numero_factura:
            errores.append("El número de factura es obligatorio.")
        if not self.cliente:
            errores.append("El cliente es obligatorio.")
        if not self.destino:
            errores.append("El destino es obligatorio.")
        if self.total <= 0:
            errores.append("El total debe ser mayor a 0.")
        if self.formato not in {"txt", "json", "csv"}:
            errores.append("Formato no válido. Usa TXT, JSON o CSV.")
        return errores
