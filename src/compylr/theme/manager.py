from .dark import DARK
from .light import LIGHT

def get_theme(mode: str) -> dict:
    return DARK if mode == 'dark' else LIGHT
