from __future__ import annotations

from fpdf import FPDF

from services.producto_service import list_productos


def productos_pdf() -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Reporte de Productos - Litobanano S.A.", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", size=10)
    pdf.cell(20, 8, "ID", 1)
    pdf.cell(80, 8, "Nombre", 1)
    pdf.cell(30, 8, "Precio", 1)
    pdf.cell(30, 8, "Stock", 1, ln=True)

    for p in list_productos():
        pdf.cell(20, 8, str(p.id_producto), 1)
        pdf.cell(80, 8, p.nombre[:35], 1)
        pdf.cell(30, 8, f"{p.precio:.2f}", 1)
        pdf.cell(30, 8, str(p.stock), 1, ln=True)

    return pdf.output(dest="S").encode("latin-1")
