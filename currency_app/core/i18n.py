"""
Module: i18n.py
Responsabilité:
    Gestion de l'internationalisation (FR/EN)

Concepts:
    - Enum_LANG : langue active
    - Table STRINGS : dictionnaire de traduction
    - Méthode t() : récupère la traduction

Design:
    - UI appelle t("clé", lang)
    - Facile à étendre (ajouter d'autres langues)
"""

from enum import Enum

class Lang(str, Enum):
    FR = "fr"
    EN = "en"


# Dictionnaire des traductions
STRINGS = {
    "title": {
        Lang.FR: "💱 Convertisseur — Noir & Orange",
        Lang.EN: "💱 Converter — Black & Orange"
    },
    "from": {Lang.FR:"De", Lang.EN:"From"},
    "to": {Lang.FR:"Vers", Lang.EN:"To"},
    "convert": {Lang.FR:"Convertir", Lang.EN:"Convert"},
    "rate": {Lang.FR:"Taux", Lang.EN:"Rate"},
    "export_pdf": {Lang.FR:"📄 Export PDF", Lang.EN:"📄 Export PDF"},
    "clear_history": {Lang.FR:"🧹 Effacer historique", Lang.EN:"🧹 Clear history"},
    "history_title": {Lang.FR:"Historique des conversions", Lang.EN:"Conversion History"},
    "menu_lang": {Lang.FR:"Langue", Lang.EN:"Language"},
    "lang_fr": {Lang.FR:"Français", Lang.EN:"French"},
    "lang_en": {Lang.FR:"Anglais", Lang.EN:"English"},
    "notify": {Lang.FR:"Notifications", Lang.EN:"Notifications"},
    "notify_enable": {Lang.FR:"Alerter si taux ≥ seuil", Lang.EN:"Notify if rate ≥ threshold"},
    "threshold": {Lang.FR:"Seuil", Lang.EN:"Threshold"},
    "notif_title": {Lang.FR:"Seuil atteint", Lang.EN:"Threshold reached"},
    "notif_body": {
        Lang.FR:"Le taux {frm}→{to} = {rate:.4f} (≥ {th:.4f})",
        Lang.EN:"{frm}→{to} rate = {rate:.4f} (≥ {th:.4f})"
    },
    "dialog_success": {Lang.FR:"Succès", Lang.EN:"Success"},
    "dialog_error": {Lang.FR:"Erreur", Lang.EN:"Error"},
    "pdf_done": {Lang.FR:"Export terminé ✅", Lang.EN:"Export finished ✅"},
}
    
def t(key: str, lang: Lang) -> str:
    """Retourne la traduction d'une clé"""
    return STRINGS.get(key, {}).get(lang, key)
