"""Paquete de validación y normalización de datos."""

from .fechas import edad, es_fecha, es_mayor_de_edad
from .numeros import a_decimal, en_rango, es_decimal, es_entero
from .texto import es_dni, es_email, esta_vacio, normalizar_nombre

__version__ = "1.0.0"

__all__ = [
    "esta_vacio",
    "normalizar_nombre",
    "es_email",
    "es_dni",
    "es_entero",
    "es_decimal",
    "a_decimal",
    "en_rango",
    "es_fecha",
    "edad",
    "es_mayor_de_edad",
]