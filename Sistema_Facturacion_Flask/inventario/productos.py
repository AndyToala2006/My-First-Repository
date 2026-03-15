class Factura:
    def __init__(
        self,
        factura_id: int,
        numero_factura: str,
        cliente: str,
        producto: str,
        cantidad_cajas: int,
        precio_caja: float,
        total: float,
    ):
        self._id = factura_id
        self._numero_factura = numero_factura
        self._cliente = cliente
        self._producto = producto
        self._cantidad_cajas = cantidad_cajas
        self._precio_caja = precio_caja
        self._total = total

    def get_id(self) -> int:
        return self._id

    def get_numero_factura(self) -> str:
        return self._numero_factura

    def get_cliente(self) -> str:
        return self._cliente

    def set_cliente(self, cliente: str) -> None:
        self._cliente = cliente

    def get_producto(self) -> str:
        return self._producto

    def set_producto(self, producto: str) -> None:
        self._producto = producto

    def get_cantidad_cajas(self) -> int:
        return self._cantidad_cajas

    def set_cantidad_cajas(self, cantidad_cajas: int) -> None:
        self._cantidad_cajas = cantidad_cajas

    def get_precio_caja(self) -> float:
        return self._precio_caja

    def set_precio_caja(self, precio_caja: float) -> None:
        self._precio_caja = precio_caja

    def get_total(self) -> float:
        return self._total

    def set_total(self, total: float) -> None:
        self._total = total

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "numero_factura": self._numero_factura,
            "cliente": self._cliente,
            "producto": self._producto,
            "cantidad_cajas": self._cantidad_cajas,
            "precio_caja": self._precio_caja,
            "total": self._total,
        }
