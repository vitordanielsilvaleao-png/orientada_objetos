import unicodedata

def normalizar_texto(texto: str):
    texto = texto.strip().lower()

    texto = unicodedata.normalize("NFD", texto)

    return "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )