# Sistema de Facturación - Litobanano S.A.

Aplicación Flask profesional para gestión de facturación de exportación de banano.

## Funcionalidades
- Dashboard con métricas de facturación.
- CRUD completo de facturas con SQLite + SQLAlchemy.
- Persistencia adicional con TXT, JSON y CSV.
- Integración MySQL (MariaDB) con CRUD de usuarios y facturas.
- Módulo POO con colecciones (`dict`, `list`, `set`, `tuple`).

## MySQL (MariaDB) - Variables de entorno
Configura estas variables antes de usar las rutas MySQL:
- `MYSQL_HOST`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
- `MYSQL_PORT` (opcional, por defecto 3306)

Las tablas se crean automáticamente en la primera conexión:
- `usuarios` (id_usuario, nombre, mail, password)
- `facturas` (id_factura, numero_factura, fecha_emision, cliente, ruc, destino, producto, cantidad_cajas, precio_caja, total, estado)

## Rutas MySQL
- `/mysql/usuarios`
- `/mysql/facturas`

## Ejecución local
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Deploy en Render
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
- Variables recomendadas: `SECRET_KEY`, `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_PORT`
