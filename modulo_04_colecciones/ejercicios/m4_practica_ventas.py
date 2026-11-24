"""Módulo 4 - Práctica 4: análisis de ventas en memoria.

Cada venta es un diccionario con las claves "fecha", "vendedor", "region",
"producto", "categoria", "unidades" y "precio". Ninguna función modifica la
lista de ventas que recibe.
"""

from m4_datos_ventas import VENTAS

ANCHO = 44


def importe(venta: dict) -> float:
    """Devuelve el importe de una venta: unidades por precio, con dos decimales.

    >>> importe({"unidades": 3, "precio": 19.9})
    59.7
    """
    return round(venta["unidades"] * venta["precio"], 2)


def total_ventas(ventas: list[dict]) -> float:
    """Devuelve la suma de los importes de todas las ventas, con dos decimales."""
    return round(sum(importe(venta) for venta in ventas), 2)


def filtrar_ventas(ventas: list[dict], *, region: str | None = None,
                   categoria: str | None = None, vendedor: str | None = None,
                   desde: str | None = None, hasta: str | None = None) -> list[dict]:
    """Devuelve las ventas que cumplen todos los criterios indicados.

    Un criterio que vale ``None`` no se aplica. ``desde`` y ``hasta`` son
    fechas ISO y las dos están incluidas en el intervalo.
    """
    resultado = []
    for venta in ventas:
        if region is not None and venta["region"] != region:
            continue
        if categoria is not None and venta["categoria"] != categoria:
            continue
        if vendedor is not None and venta["vendedor"] != vendedor:
            continue
        if desde is not None and venta["fecha"] < desde:
            continue
        if hasta is not None and venta["fecha"] > hasta:
            continue
        resultado.append(venta)
    return resultado


def importe_por(ventas: list[dict], campo: str) -> dict[str, float]:
    """Agrupa las ventas por ``campo`` y devuelve el importe total de cada grupo.

    Los importes van redondeados a dos decimales.

    >>> importe_por([{"region": "Norte", "unidades": 2, "precio": 10.0}], "region")
    {'Norte': 20.0}
    """
    totales: dict[str, float] = {}
    for venta in ventas:
        clave = venta[campo]
        totales[clave] = round(totales.get(clave, 0.0) + importe(venta), 2)
    return totales


def unidades_por_producto(ventas: list[dict]) -> dict[str, int]:
    """Devuelve las unidades totales vendidas de cada producto."""
    totales: dict[str, int] = {}
    for venta in ventas:
        producto = venta["producto"]
        totales[producto] = totales.get(producto, 0) + venta["unidades"]
    return totales


def ranking(ventas: list[dict], campo: str, cantidad: int = 3) -> list[tuple[str, float]]:
    """Devuelve los ``cantidad`` grupos con mayor importe, como tuplas (clave, importe).

    De mayor a menor importe. A igual importe, por orden alfabético de la clave.
    """
    totales = importe_por(ventas, campo)
    ordenados = sorted(totales.items(), key=lambda item: (-item[1], item[0]))
    return ordenados[:cantidad]


def producto_mas_vendido(ventas: list[dict]) -> str | None:
    """Devuelve el producto con más unidades vendidas, o ``None`` si no hay ventas.

    En caso de empate, el primero por orden alfabético.
    """
    if not ventas:
        return None
    unidades = unidades_por_producto(ventas)
    return min(unidades.items(), key=lambda item: (-item[1], item[0]))[0]


def ticket_medio(ventas: list[dict]) -> float:
    """Devuelve el importe medio por venta, con dos decimales. Sin ventas, 0.0."""
    if not ventas:
        return 0.0
    return round(total_ventas(ventas) / len(ventas), 2)


def generar_informe(ventas: list[dict]) -> str:
    """Devuelve el informe de ventas como texto, con el formato del enunciado."""
    separador = "=" * ANCHO
    guion = "-" * ANCHO

    num_operaciones = len(ventas)
    total = total_ventas(ventas)
    medio = ticket_medio(ventas)
    estrella = producto_mas_vendido(ventas) or "-"

    lineas = [
        separador,
        "             INFORME DE VENTAS",
        separador,
        f"{'Ventas registradas':<24}{num_operaciones:>20}",
        f"{'Importe total':<24}{total:>20,.2f}",
        f"{'Ticket medio':<24}{medio:>20,.2f}",
        f"{'Producto más vendido':<24}{estrella:>20}",
        guion,
        "Por región",
    ]

    for region, imp in ranking(ventas, "region", cantidad=len(ventas) or 1):
        lineas.append(f"  {region:<22}{imp:>20,.2f}")

    lineas.extend([
        guion,
        "Por categoría",
    ])

    for categoria, imp in ranking(ventas, "categoria", cantidad=len(ventas) or 1):
        lineas.append(f"  {categoria:<22}{imp:>20,.2f}")

    lineas.extend([
        guion,
        "Por vendedor",
    ])

    for vendedor, imp in ranking(ventas, "vendedor", cantidad=len(ventas) or 1):
        lineas.append(f"  {vendedor:<22}{imp:>20,.2f}")

    lineas.append(separador)
    return "\n".join(lineas)

def main():
    print(generar_informe(VENTAS))
    print()
    print("Solo la región Sur, segunda quincena:")
    print(generar_informe(filtrar_ventas(VENTAS, region="Sur", desde="2026-10-16")))


if __name__ == "__main__":
    main()