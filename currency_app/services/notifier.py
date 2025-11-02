"""
Module: notifier.py
Responsabilité:
    Gérer les notifications système via QSystemTrayIcon
"""

from PySide6 import QtWidgets

class SystemNotifier:
    def __init__(self):
        self.tray = None
        self.last_rate = {}  # mémorise le dernier taux par paire

    def ensure(self, parent=None):
        """Initialise l'icône tray si pas encore créée"""
        if self.tray is None:
            self.tray = QtWidgets.QSystemTrayIcon(parent)
            icon = QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation)
            self.tray.setIcon(icon)
            self.tray.setVisible(True)

    def maybe_notify_threshold(self, frm, to, rate, threshold, enabled, title, body_tpl):
        """Envoie une alerte si un seuil a été franchi"""
        if not enabled:
            return

        key = f"{frm}->{to}"
        prev = self.last_rate.get(key)

        crossed = (prev is not None and prev < threshold <= rate) or (prev is None and rate >= threshold)
        self.last_rate[key] = rate

        if crossed and self.tray:
            self.tray.showMessage(title, body_tpl.format(frm=frm, to=to, rate=rate, th=threshold),
                                  QtWidgets.QSystemTrayIcon.Information, 5000)
