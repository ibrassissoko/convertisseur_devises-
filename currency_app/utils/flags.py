"""
Module: flags.py
Responsabilité:
    Retourne un emoji drapeau selon la devise
"""

def flag_for_currency(code: str) -> str:
    """Renvoie un emoji drapeau associé à une devise ISO"""

    flags = {
        "USD":"🇺🇸","EUR":"🇪🇺","GBP":"🇬🇧","JPY":"🇯🇵","CNY":"🇨🇳",
        "CAD":"🇨🇦","AUD":"🇦🇺","CHF":"🇨🇭","XOF":"🌍","XAF":"🌍",
        "NGN":"🇳🇬","GHS":"🇬🇭","MAD":"🇲🇦","TND":"🇹🇳","MRU":"🇲🇷"
    }
    return flags.get(code.upper(), "🏳️")
