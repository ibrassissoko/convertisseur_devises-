"""
Module: models.py
Responsabilité:
    Définir les structures de données du domaine (Business Models)
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class ConversionRecord:
    """
    Modèle métier représentant une ligne d'historique de conversion.
    
    Attributes:
        ts (str): timestamp format "YYYY-MM-DD HH:MM:SS"
        from_cur (str): devise d'origine (ex: EUR)
        to_cur (str): devise cible (ex: USD)
        amount (float): montant à convertir
        result (float): résultat de la conversion
        rate (float): taux utilisé
    """
    ts: str
    from_cur: str
    to_cur: str
    amount: float
    result: float
    rate: float
