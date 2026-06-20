import urllib.parse
import re


def get_whatsapp_link(phone: str, message: str) -> str:
    clean = re.sub(r"[\s\-\(\)]", "", phone or "")
    if not clean.startswith("+"):
        clean = "+51" + clean
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{clean}?text={encoded}"
