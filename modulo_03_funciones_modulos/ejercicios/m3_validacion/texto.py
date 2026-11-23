"""Funciones de validación y normalización de textos."""

LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"


def esta_vacio(texto: str | None) -> bool:
    """Indica si ``texto`` es None, vacío o solo contiene espacios."""
    return texto is None or texto.strip() == ""


def normalizar_nombre(nombre: str) -> str:
    """Quita espacios sobrantes y pone la inicial de cada palabra en mayúscula."""
    return " ".join(nombre.strip().split()).title()


def es_email(texto: str) -> bool:
    """Comprobación sencilla de la forma de un correo electrónico."""
    if esta_vacio(texto):
        return False
    correo = texto.strip()
    if " " in correo or correo.count("@") != 1:
        return False
    usuario, dominio = correo.split("@")
    if not usuario or "." not in dominio:
        return False
    partes_dominio = dominio.split(".")
    return all(partes_dominio)


def es_dni(texto: str) -> bool:
    """Indica si ``texto`` tiene ocho dígitos y la letra de control correcta."""
    if esta_vacio(texto):
        return False
    limpio = texto.strip().upper()
    if len(limpio) != 9 or not limpio[:8].isdigit():
        return False
    numero = int(limpio[:8])
    return limpio[8] == LETRAS_DNI[numero % 23]