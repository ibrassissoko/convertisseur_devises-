"""
Application Desktop PySide6 — Convertisseur de devises
Architecture Modulaire (UI / Domain / Infra / Services / Core)
Auteur: TonNom
Description:
    Point d'entrée principal de l'application.
    Initialise les services, configure l'interface, et démarre Qt.

Points Clés:
    - Injection de dépendances
    - Initialisation unique Qt
    - Clean Architecture
"""

from PySide6 import QtWidgets

from currency_app.core.logging_config import setup_logging
from currency_app.core.settings import Settings

from currency_app.infra.db import SQLiteRepository
from currency_app.domain.converter import OfflineConverter
from currency_app.services.notifier import SystemNotifier
from currency_app.services.chart_service import RateChart

from currency_app.ui.main_window import MainWindow


def main():
    """Boot de l'application et wiring des dépendances."""

    # Init logs
    setup_logging()

    # Init Qt
    app = QtWidgets.QApplication([])

    # Chargement configuration globale
    settings = Settings()

    # Injection des services (D.I)
    repo = SQLiteRepository(settings.db_path)
    converter = OfflineConverter()
    notifier = SystemNotifier()
    chart = RateChart()

    # Création de la fenêtre principale
    win = MainWindow(
        settings=settings,
        repo=repo,
        converter=converter,
        notifier=notifier,
        chart=chart
    )

    win.show()
    app.exec()  # boucle Qt


if __name__ == "__main__":
    main()
