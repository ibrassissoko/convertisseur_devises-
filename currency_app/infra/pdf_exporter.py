"""
Module: pdf_exporter.py
Responsabilité:
    Exporter le tableau d'historique en PDF
"""

from PySide6.QtGui import QPageSize, QPainter
from PySide6.QtPrintSupport import QPrinter

def export_table_to_pdf(path, title, headers, rows):
    """Exporte un tableau en PDF avec pagination"""

    printer = QPrinter(QPrinter.HighResolution)
    printer.setOutputFileName(path)
    printer.setPageSize(QPageSize(QPageSize.A4))
    printer.setOutputFormat(QPrinter.PdfFormat)

    painter = QPainter()
    try:
        painter.begin(printer)
        margin, y = 40, 40

        painter.setFont(QPainter().font())
        painter.drawText(margin, y, title)
        y += 30

        # Header row
        x = [margin, 180, 250, 330, 420, 500]
        for px, h in zip(x, headers):
            painter.drawText(px, y, h)
        y += 20

        page_height = printer.pageRect(QPrinter.DevicePixel).height()

        for row in rows:
            if y > page_height - margin:
                printer.newPage()
                y = margin

            for px, v in zip(x, row):
                painter.drawText(px, y, str(v))
            y += 18
    finally:
        painter.end()
