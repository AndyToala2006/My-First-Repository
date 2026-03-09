# Sistema de Facturación - Litobanano S.A.

Aplicación Flask profesional para gestión de facturación de exportación de banano.

## Funcionalidades
- Dashboard con métricas de facturación.
- CRUD completo de facturas con SQLite + SQLAlchemy.
- Rutas dinámicas: `/cliente/<nombre>` y `/factura/<numero>`.
- Persistencia adicional con TXT, JSON y CSV.
- Módulo POO con colecciones (`dict`, `list`, `set`, `tuple`) y menú de consola.

## Estructura académica cubierta
- Semana 9: Flask, rutas, GitHub/Render.
- Semana 10: Plantillas con herencia (`base.html`).
- Semana 11: POO, colecciones y CRUD.
- Semana 12: Persistencia en archivos + SQLite con ORM.

## Ejecución local
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Deploy en Render
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Variables opcionales: `SECRET_KEY`, `DATABASE_URL`
