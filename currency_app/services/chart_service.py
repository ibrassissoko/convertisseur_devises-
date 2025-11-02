"""
Module: chart_service.py
Responsabilité:
    Service QtCharts encapsulé pour tracer les taux
"""

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QPainter

class RateChart:
    """Gère un graphique linéaire de taux"""

    def __init__(self):
        self.series = QLineSeries()
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.legend().hide()

        # Axes
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("dd/MM HH:mm")

        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%.4f")

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        self.view = QChartView(self.chart)
        self.view.setRenderHint(QPainter.Antialiasing)

    def widget(self):
        return self.view

    def add_point(self, ts_str: str, rate: float):
        """Ajoute un point (timestamp ms, taux)"""
        dt = QDateTime.fromString(ts_str, "yyyy-MM-dd HH:mm:ss")
        self.series.append(dt.toMSecsSinceEpoch(), rate)
        self.rescale()

    def clear(self):
        self.series.clear()

    def rescale(self):
        """Réajuste les axes selon les valeurs actuelles"""
        if self.series.count() == 0:
            return

        xs = [self.series.at(i).x() for i in range(self.series.count())]
        ys = [self.series.at(i).y() for i in range(self.series.count())]

        self.axis_x.setRange(
            QDateTime.fromMSecsSinceEpoch(int(xs[0])),
            QDateTime.fromMSecsSinceEpoch(int(xs[-1]))
        )

        mn, mx = min(ys), max(ys)
        pad = (mx - mn) * 0.1 if mx != mn else 0.1
        self.axis_y.setRange(mn - pad, mx + pad)
