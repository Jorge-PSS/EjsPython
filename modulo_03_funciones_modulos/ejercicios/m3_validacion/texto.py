LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"


def esta_vacio(texto: str | None) -> bool:
    return texto is None or texto.strip() == ""


def normalizar_nombre(nombre: str) -> str:
    return " ".join(nombre.strip().split()).title()


def es_email(texto: str) -> bool:
    if esta_vacio(texto):
        return False
    correo = texto.strip()
    if " " in correo or correo.count("@") != 1:
        return False
    usuario, dominio = correo.split("@")
    if not usuario or "." not in dominio:
        return False
    partes_dominio = dominio.split(".")
    return all(partes_dominio) and len(partes_dominio[-1]) >= 2


def es_dni(texto: str) -> bool:
    if esta_vacio(texto):
        return False
    limpio = texto.strip().upper()
    if len(limpio) != 9 or not limpio[:8].isdigit():
        return False
    numero = int(limpio[:8])
    return limpio[8] == LETRAS_DNI[numero % 23]