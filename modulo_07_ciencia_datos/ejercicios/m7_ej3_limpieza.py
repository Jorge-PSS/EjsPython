"""Módulo 7 - Ejercicio 3: limpieza de datos.

Se trabaja con ``datos/ventas_sucias.csv``, leído con todas las columnas como
texto. Ninguna función modifica el DataFrame que recibe.
"""

from pathlib import Path

import pandas as pd

COLUMNAS_TEXTO = ["vendedor", "region", "producto", "categoria"]


def cargar_en_bruto(ruta: str | Path) -> pd.DataFrame:
    """Lee el CSV con todas las columnas como texto, sin que pandas interprete nada.

    Las celdas vacías quedan como valores ausentes.
    """
    return pd.read_csv(ruta, encoding="utf-8", dtype=str)


def contar_ausentes(df: pd.DataFrame) -> dict[str, int]:
    """Devuelve cuántos valores ausentes tiene cada columna. Solo las que tienen alguno."""
    nulos = df.isna().sum()
    return {str(col): int(cantidad) for col, cantidad in nulos.items() if cantidad > 0}


def normalizar_texto(df: pd.DataFrame, columnas: list[str] = COLUMNAS_TEXTO) -> pd.DataFrame:
    """Devuelve una copia con las columnas indicadas sin espacios sobrantes y con la inicial en mayúscula.

    "  ada " y "ADA" pasan a ser "Ada". Los valores ausentes siguen ausentes.
    """
    copia = df.copy()
    for col in columnas:
        if col in copia.columns:
            copia[col] = copia[col].str.strip().str.capitalize()
    return copia


def convertir_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una copia con ``fecha``, ``unidades`` y ``precio`` convertidos.

- ``fecha``: fecha a partir del formato "AAAA-MM-DD". Lo que no lo cumple queda ausente.
- ``unidades``: número. Lo que no es un número queda ausente.
- ``precio``: número. Admite coma decimal: "29,5" es 29.5.
    """
    copia = df.copy()
    if "fecha" in copia.columns:
        fechas_limpias = copia["fecha"].astype("string").str.strip()
        copia["fecha"] = pd.to_datetime(fechas_limpias, format="%Y-%m-%d", errors="coerce")

    if "unidades" in copia.columns:
        unidades_limpias = copia["unidades"].astype("string").str.strip()
        copia["unidades"] = pd.to_numeric(unidades_limpias, errors="coerce")

    if "precio" in copia.columns:
        precios_limpios = copia["precio"].astype("string").str.strip().str.replace(",", ".", regex=False)
        copia["precio"] = pd.to_numeric(precios_limpios, errors="coerce")

    return copia


def quitar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el DataFrame sin filas repetidas. Se conserva la primera de cada grupo."""
    return df.drop_duplicates(keep="first").copy()


def rellenar_region(df: pd.DataFrame, valor: str = "Sin región") -> pd.DataFrame:
    """Devuelve una copia en la que las regiones ausentes se sustituyen por ``valor``."""
    copia = df.copy()
    if "region" in copia.columns:
        copia["region"] = copia["region"].fillna(valor)
    return copia


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica toda la limpieza y devuelve un DataFrame listo para analizar.

    Pasos, en este orden:

1. Normalizar el texto.
2. Quitar duplicados.
3. Convertir los tipos.
4. Rellenar las regiones ausentes con "Sin región".
5. Descartar las filas sin fecha, sin vendedor, sin unidades o sin precio,
       y las que tienen unidades o precio menores o iguales que cero.
6. Dejar ``unidades`` como entero y renumerar el índice desde 0.
    """
    datos = normalizar_texto(df)
    datos = quitar_duplicados(datos)
    datos = convertir_tipos(datos)
    datos = rellenar_region(datos, "Sin región")

    datos = datos.dropna(subset=["fecha", "vendedor", "unidades", "precio"])
    datos = datos.loc[(datos["unidades"] > 0) & (datos["precio"] > 0)].copy()

    datos["unidades"] = datos["unidades"].astype(int)
    return datos.reset_index(drop=True)