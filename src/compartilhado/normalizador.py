import unicodedata

def normalizar_texto(texto: str):
    texto = texto.strip().lower()

    return texto