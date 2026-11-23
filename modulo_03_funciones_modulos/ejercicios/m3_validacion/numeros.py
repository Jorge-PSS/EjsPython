def es_entero(texto: str) -> bool:
    if texto is None:
        return False
    limpio = texto.strip()
    if not limpio:
        return False
    if limpio[0] in "+-":
        limpio = limpio[1:]
    return limpio.isdigit()


def es_decimal(texto: str) -> bool:
    if texto is None:
        return False
    limpio = texto.strip().replace(",", ".", 1)
    if es_entero(limpio):
        return True
    if "." not in limpio:
        return False
    parte_entera, parte_decimal = limpio.split(".", 1)
    if not parte_decimal.isdigit():
        return False
    return parte_entera in ("", "+", "-") or es_entero(parte_entera)


def a_decimal(texto: str, por_defecto: float | None = None) -> float | None:
    if not es_decimal(texto):
        return por_defecto
    return float(texto.strip().replace(",", "."))


def en_rango(valor: float, minimo: float | None = None, maximo: float | None = None) -> bool:
    if minimo is not None and valor < minimo:
        return False
    if maximo is not None and valor > maximo:
        return False
    return True