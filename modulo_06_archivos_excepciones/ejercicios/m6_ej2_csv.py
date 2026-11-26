"""Módulo 6 - Ejercicio 2: CSV.

Todos los ficheros se abren con ``encoding="utf-8"`` y ``newline=""``.
"""

import csv
from pathlib import Path


def leer_csv(ruta, delimitador: str = ",") -> list[dict]:
    """Devuelve las filas del CSV como lista de diccionarios.

    Las claves son los nombres de la cabecera y todos los valores son cadenas.
    """
    with Path(ruta).open(mode="r", encoding="utf-8", newline="") as fichero:
        lector = csv.DictReader(fichero, delimiter=delimitador)
        return list(lector)


def cabecera(ruta) -> list[str]:
    """Devuelve la lista de nombres de columna. Con el fichero vacío, lista vacía."""
    with Path(ruta).open(mode="r", encoding="utf-8", newline="") as fichero:
        lector = csv.reader(fichero)
        return next(lector, [])


def escribir_csv(ruta, registros: list[dict], campos: list[str]) -> None:
    """Escribe los registros en un CSV con la cabecera indicada en ``campos``.

    Las claves de los registros que no estén en ``campos`` se ignoran.
    """
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open(mode="w", encoding="utf-8", newline="") as fichero:
        escritor = csv.DictWriter(fichero, fieldnames=campos, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(registros)


def leer_ventas(ruta) -> list[dict]:
    """Lee un CSV de ventas y convierte ``unidades`` a ``int`` y ``precio`` a ``float``.

    El resto de los campos se dejan como cadenas.
    """
    ventas = leer_csv(ruta)
    for venta in ventas:
        venta["unidades"] = int(venta["unidades"])
        venta["precio"] = float(venta["precio"])
    return ventas


def total_columna(ruta, columna: str) -> float:
    """Devuelve la suma de los valores de una columna numérica, con dos decimales."""
    with Path(ruta).open(mode="r", encoding="utf-8", newline="") as fichero:
        lector = csv.DictReader(fichero)
        total = sum(float(fila[columna]) for fila in lector)
    return round(total, 2)


def filtrar_csv(origen, destino, columna: str, valor: str) -> int:
    """Copia en ``destino`` las filas de ``origen`` en las que ``columna`` vale ``valor``.

    El fichero de destino conserva la cabecera y el orden de las columnas.
    Devuelve el número de filas copiadas.
    """
    ruta_origen = Path(origen)
    ruta_destino = Path(destino)
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)

    copiadas = 0
    with (
        ruta_origen.open(mode="r", encoding="utf-8", newline="") as entrada,
        ruta_destino.open(mode="w", encoding="utf-8", newline="") as salida,
    ):
        lector = csv.DictReader(entrada)
        campos = lector.fieldnames or []
        escritor = csv.DictWriter(salida, fieldnames=campos)
        if campos:
            escritor.writeheader()
        for fila in lector:
            if fila.get(columna) == valor:
                escritor.writerow(fila)
                copiadas += 1
    return copiadas


def convertir_delimitador(origen, destino, de: str = ";", a: str = ",") -> None:
    """Reescribe un CSV cambiando el delimitador.

    Tiene que funcionar aunque algún campo contenga cualquiera de los dos
    delimitadores: usa ``csv.reader`` y ``csv.writer``, no ``replace``.
    """
    ruta_origen = Path(origen)
    ruta_destino = Path(destino)
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)

    with (
        ruta_origen.open(mode="r", encoding="utf-8", newline="") as entrada,
        ruta_destino.open(mode="w", encoding="utf-8", newline="") as salida,
    ):
        lector = csv.reader(entrada, delimiter=de)
        escritor = csv.writer(salida, delimiter=a)
        escritor.writerows(lector)