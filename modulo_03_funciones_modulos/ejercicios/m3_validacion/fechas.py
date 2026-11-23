from datetime import date

MAYORIA_DE_EDAD = 18


def es_fecha(texto: str) -> bool:
    try:
        date.fromisoformat(texto.strip())
        return True
    except (ValueError, AttributeError):
        return False


def edad(fecha_nacimiento: str, hoy: date | None = None) -> int:
    if hoy is None:
        hoy = date.today()
    nacimiento = date.fromisoformat(fecha_nacimiento.strip())
    anios = hoy.year - nacimiento.year
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        anios -= 1
    return anios


def es_mayor_de_edad(fecha_nacimiento: str, hoy: date | None = None) -> bool:
    return edad(fecha_nacimiento, hoy=hoy) >= MAYORIA_DE_EDAD