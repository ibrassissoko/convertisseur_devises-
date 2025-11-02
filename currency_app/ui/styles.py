"""
styles.py — Modern UI Styling for PySide6
Theme: Dark / Orange / White
Style: Hybrid Material + Fluent + Tailwind Spacing
"""

from PySide6 import QtGui

# ---- Color Palette ----
ACCENT = "#FF8C00"       # Orange primaire
ACCENT_HOVER = "#FFA733" # Orange hover plus clair
BG = "#0D0D0D"           # Noir profond
SURFACE = "#181818"      # Surface gris foncé (cards, inputs)
TEXT = "#FFFFFF"         # Texte blanc pur
TEXT_MUTED = "#C7C7C7"   # Texte secondaire
BORDER = "#303030"       # Bordure discrète
ERROR = "#FF4C4C"        # Erreur rouge
SUCCESS = "#4CAF50"      # Vert succès (rare)
FONT = "Segoe UI, Inter, Roboto, Arial"

def apply_black_orange_white(widget):
    """
    Apply the global modern dark theme to the PySide6 UI.
    """

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(BG))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(SURFACE))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(ACCENT))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor("#000000"))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(TEXT))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(TEXT))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(ACCENT))
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#000000"))

    widget.setPalette(palette)

    # ---- StyleSheet ----
    widget.setStyleSheet(f"""
        /* GLOBAL */
        QWidget {{
            background: {BG};
            color: {TEXT};
            font-family: {FONT};
            font-size: 14px;
        }}

        QLabel {{
            color: {TEXT};
            padding: 2px;
        }}

        /* GROUPBOX (Card UI) */
        QGroupBox {{
            border: 1px solid {ACCENT};
            border-radius: 8px;
            margin-top: 16px;
            padding: 12px;
            font-weight: 600;
        }}
        QGroupBox::title {{
            left: 10px;
            top: -8px;
            background: {BG};
            padding: 0 6px;
        }}

        /* INPUTS */
        QLineEdit, QComboBox, QDoubleSpinBox {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            padding: 8px;
            border-radius: 8px;
            min-height: 34px;
            color: {TEXT};
        }}

        QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {{
            border: 1px solid {ACCENT};
            outline: 0;
        }}

        /* BUTTONS */
        QPushButton {{
            background: {ACCENT};
            border: none;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
            color: #000;
        }}
        QPushButton:hover {{
            background: {ACCENT_HOVER};
        }}
        QPushButton:disabled {{
            background: #444;
            color: #999;
        }}

        /* TABLE */
        QTableWidget {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            gridline-color: {BORDER};
            selection-background-color: {ACCENT};
            selection-color: black;
        }}
        QHeaderView::section {{
            background: {ACCENT};
            color: black;
            padding: 6px;
            font-weight: 600;
            border: none;
        }}
        QTableWidget::item {{
            padding: 6px;
        }}

        /* CHECKBOX */
        QCheckBox {{
            color: {TEXT};
        }}

        /* SCROLLBAR */
        QScrollBar:vertical {{
            width: 8px;
            background: {BG};
        }}
        QScrollBar::handle:vertical {{
            background: {ACCENT};
            border-radius: 4px;
        }}
        QScrollBar::handle:hover {{
            background: {ACCENT_HOVER};
        }}

        /* DROPDOWN LIST */
        QComboBox QAbstractItemView {{
            background: {SURFACE};
            border: 1px solid {ACCENT};
            selection-background-color: {ACCENT};
            color: {TEXT};
        }}
    """)
