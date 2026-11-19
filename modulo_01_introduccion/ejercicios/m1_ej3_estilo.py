"""Módulo 1 - Ejercicio 3: código con estilo.

La función de abajo funciona, pero ignora PEP 8. Reescríbela siguiendo las
indicaciones del enunciado sin cambiar su comportamiento.
"""

IVA_GENERAL = 21


def precio_final(precio, iva=IVA_GENERAL, descuento=0):
    """Calcula el precio final aplicando un descuento e IVA."""
    precio_con_descuento = precio - precio * descuento / 100
    total = precio_con_descuento + precio_con_descuento * iva / 100
    return round(total, 2)