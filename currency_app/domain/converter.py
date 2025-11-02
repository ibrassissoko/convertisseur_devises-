"""
Module: converter.py
Responsabilité:
    Assure la logique métier de conversion de devises.

Notes d'architecte:
    - Cette couche ne doit jamais dépendre de PySide6 (UI)
    - Facilement testable unitairement
"""

from currency_converter import CurrencyConverter


class OfflineConverter:
    """Service métier responsable de la conversion offline."""

    def __init__(self):
        # Instancie le moteur de conversion
        self.cc = CurrencyConverter()

    def list_currencies(self) -> list[str]:
        """Retourne la liste triée des devises disponibles."""
        return sorted(list(self.cc.currencies))

    def convert(self, amount: float, frm: str, to: str) -> tuple[float, float]:
        """
        Effectue la conversion.
        Retour:
            (resultat, taux utilisé)

        Exception:
            Propagera si devise inconnue
        """
        result = float(self.cc.convert(amount, frm, to))
        rate = result / amount if amount != 0 else 0.0
        return result, rate
