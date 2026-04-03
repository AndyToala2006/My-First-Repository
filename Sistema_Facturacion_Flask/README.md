# Sistema de Facturación - Litobanano S.A.

Aplicación Flask profesional para gestión de facturación de exportación de banano.

## Funcionalidades
- Dashboard con métricas de facturación.
- CRUD completo de facturas (SQLite + SQLAlchemy).
- Persistencia adicional con TXT, JSON y CSV.
- Integración MySQL (MariaDB) con tablas relacionadas.
- Autenticación con Flask-Login (registro, login, logout).
- CRUD de productos en MySQL (capas models/services/forms).
- Reporte PDF de productos.

## Estructura por capas
- `conexion/` conexión MySQL
- `models/` entidades (User, Producto)
- `services/` lógica de acceso a datos
- `forms/` validación de formularios
- `templates/` vistas por módulo

## MySQL (MariaDB) - Variables de entorno
Configura estas variables antes de usar MySQL:
- `MYSQL_HOST`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`
- `MYSQL_PORT` (opcional, 3306)

## Rutas clave
- Auth: `/login`, `/register`, `/logout`
- Productos MySQL: `/productos`
- Facturas MySQL: `/mysql/facturas`
- PDF: `/reportes/productos.pdf`

## Script SQL
- `sql/litobanano.sql`

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
- Variables: `SECRET_KEY`, `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_PORT`
