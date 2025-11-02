"""
Module: settings.py
Responsabilité:
    Paramètres centralisés de l'application.

Notes:
    - Remplace les constantes dispersées
    - Facilement surchargeable (env, config file)
"""

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    app_title: str = "💱 Convertisseur — PySide6"
    db_path: Path = Path("history.sqlite3")

    # Valeurs UX
    default_from: str = "EUR"
    default_to: str = "USD"
    default_amount: float = 100.0

    # Notifications
    notify_default_enabled: bool = False
    notify_default_threshold: float = 100.0
