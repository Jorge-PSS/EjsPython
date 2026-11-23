"""Funciones de validación y cálculo con fechas."""

from datetime import date

MAYORIA_DE_EDAD = 18


def es_fecha(texto: str) -> bool:
    """Indica si ``texto`` es una fecha válida en formato ISO (AAAA-MM-DD)."""
    try:
        date.fromisoformat(texto.strip())
        return True
    except (ValueError, AttributeError):
        return False


def edad(fecha_nacimiento: str, hoy: date | None = None) -> int:
    """Calcula los años cumplidos desde ``fecha_nacimiento`` hasta ``hoy``."""
    if hoy is None:
        hoy = date.today()
    nacimiento = date.fromisoformat(fecha_nacimiento.strip())
    anios = hoy.year - nacimiento.year
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        anios -= 1
    return anios


def es_mayor_de_edad(fecha_nacimiento: str, hoy: date | None = None) -> bool:
    """Indica si la persona nacida en ``fecha_nacimiento`` es mayor de edad."""
    return edad(fecha_nacimiento, hoy=hoy) >= MAYORIA_DE_EDAD