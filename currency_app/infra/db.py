"""
Module: db.py
Responsabilité:
    Gestion de la base SQLite locale
    Pattern Repository

Design:
    - Isolé de l'UI
    - Appels simples (pas d'ORM volontairement pour la lisibilité)
"""

import sqlite3
from typing import Iterable
from currency_app.domain.models import ConversionRecord


DDL = """
CREATE TABLE IF NOT EXISTS conversions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    from_cur TEXT NOT NULL,
    to_cur TEXT NOT NULL,
    amount REAL NOT NULL,
    result REAL NOT NULL,
    rate REAL NOT NULL
)
"""


class SQLiteRepository:
    """Repository SQLite basique (CRUD minimal)."""

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(DDL)
        self.conn.commit()

    def insert(self, rec: ConversionRecord) -> None:
        """Insère un enregistrement dans l'historique."""
        self.conn.execute(
            "INSERT INTO conversions (ts, from_cur, to_cur, amount, result, rate) VALUES (?,?,?,?,?,?)",
            (rec.ts, rec.from_cur, rec.to_cur, rec.amount, rec.result, rec.rate),
        )
        self.conn.commit()

    def fetch_all(self) -> Iterable[ConversionRecord]:
        """Retourne l'historique complet."""
        cur = self.conn.cursor()
        cur.execute("SELECT ts, from_cur, to_cur, amount, result, rate FROM conversions ORDER BY ts ASC")
        for ts, f, t, a, r, rate in cur.fetchall():
            yield ConversionRecord(ts, f, t, a, r, rate)

    def clear(self) -> None:
        """Supprime tout l'historique."""
        self.conn.execute("DELETE FROM conversions")
        self.conn.commit()
