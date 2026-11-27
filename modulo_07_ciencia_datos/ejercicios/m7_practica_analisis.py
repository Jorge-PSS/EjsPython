"""Módulo 7 - Práctica 7: análisis de las ventas del año.

Un pequeño proceso de análisis completo: cargar, limpiar, calcular indicadores,
generar gráficos y exportar los resultados.

Uso:

    python m7_practica_analisis.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATOS = Path(__file__).resolve().parent.parent / "datos"
SALIDA = Path(__file__).resolve().parent / "salida_practica_7"
COLUMNAS_TEXTO = ["vendedor", "region", "producto", "categoria"]


def cargar(ruta: str | Path) -> pd.DataFrame:
    """Lee el CSV de ventas con todas las columnas como texto."""
    return pd.read_csv(ruta, encoding="utf-8", dtype=str)


def preparar(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve las ventas limpias y con las columnas calculadas.

1. Texto sin espacios sobrantes y con la inicial en mayúscula.
2. Sin filas duplicadas.
3. ``fecha`` como fecha (formato "AAAA-MM-DD"), ``unidades`` y ``precio``
       como números. ``precio`` admite coma decimal.
4. Las regiones ausentes pasan a ser "Sin región".
5. Se descartan las filas sin fecha, vendedor, unidades o precio válidos, y
       las que tienen unidades o precio menores o iguales que cero.
6. ``unidades`` queda como entero.
7. Columnas nuevas: ``importe`` (unidades por precio) y ``mes`` ("AAAA-MM").
8. Filas ordenadas por fecha, con el índice renumerado desde 0. A igual
       fecha se conserva el orden original.

    No modifica el DataFrame recibido.
    """
    datos = df.copy()

    # 1. Normalizar texto
    for col in COLUMNAS_TEXTO:
        if col in datos.columns:
            datos[col] = datos[col].str.strip().str.capitalize()

    # 2. Quitar duplicados
    datos = datos.drop_duplicates(keep="first")

    # 3. Conversión de tipos
    if "fecha" in datos.columns:
        fechas_limpias = datos["fecha"].astype("string").str.strip()
        datos["fecha"] = pd.to_datetime(fechas_limpias, format="%Y-%m-%d", errors="coerce")

    if "unidades" in datos.columns:
        unidades_limpias = datos["unidades"].astype("string").str.strip()
        datos["unidades"] = pd.to_numeric(unidades_limpias, errors="coerce")

    if "precio" in datos.columns:
        precios_limpios = (
            datos["precio"].astype("string").str.strip().str.replace(",", ".", regex=False)
        )
        datos["precio"] = pd.to_numeric(precios_limpios, errors="coerce")

    # 4. Rellenar regiones ausentes
    if "region" in datos.columns:
        datos["region"] = datos["region"].fillna("Sin región")

    # 5. Descartar filas inválidas o con valores no positivos
    datos = datos.dropna(subset=["fecha", "vendedor", "unidades", "precio"])
    datos = datos.loc[(datos["unidades"] > 0) & (datos["precio"] > 0)].copy()

    # 6. Unidades como entero
    datos["unidades"] = datos["unidades"].astype(int)

    # 7. Columnas calculadas
    datos["importe"] = (datos["unidades"] * datos["precio"]).round(2)
    datos["mes"] = datos["fecha"].dt.strftime("%Y-%m")

    # 8. Ordenar por fecha preservando el orden relativo original y renumerar índice
    datos = datos.sort_values(by="fecha", kind="mergesort").reset_index(drop=True)
    return datos


def indicadores(df: pd.DataFrame) -> dict:
    """Devuelve los indicadores principales de unas ventas preparadas.

    Claves:

- "ventas": número de ventas (int).
- "importe_total": float con dos decimales.
- "ticket_medio": importe medio por venta, float con dos decimales.
- "mejor_vendedor": el de mayor importe total.
- "mejor_mes": el mes "AAAA-MM" de mayor importe total.
- "producto_mas_vendido": el de más unidades.
    """
    ventas = int(len(df))
    importe_total = round(float(df["importe"].sum()), 2)
    ticket_medio = round(float(df["importe"].mean()), 2) if ventas > 0 else 0.0
    mejor_vendedor = str(df.groupby("vendedor")["importe"].sum().idxmax())
    mejor_mes = str(df.groupby("mes")["importe"].sum().idxmax())
    producto_mas_vendido = str(df.groupby("producto")["unidades"].sum().idxmax())

    return {
        "ventas": ventas,
        "importe_total": importe_total,
        "ticket_medio": ticket_medio,
        "mejor_vendedor": mejor_vendedor,
        "mejor_mes": mejor_mes,
        "producto_mas_vendido": producto_mas_vendido,
    }


def ranking_vendedores(df: pd.DataFrame, objetivos: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una fila por vendedor, de mayor a menor importe.

    Columnas, en este orden: vendedor, ventas, importe, objetivo, cumplimiento
    y cumplido. ``importe`` va redondeado a dos decimales, ``cumplimiento`` es
    el porcentaje del objetivo alcanzado con un decimal y ``cumplido`` indica
    si el importe llega al objetivo. El índice va de 0 en adelante.

    ``objetivos`` tiene las columnas vendedor y objetivo.
    """
    agrupado = (
        df.groupby("vendedor", as_index=False)
        .agg(
            ventas=("importe", "count"),
            importe=("importe", "sum"),
        )
        .sort_values(by="importe", ascending=False)
        .reset_index(drop=True)
    )
    agrupado["importe"] = agrupado["importe"].round(2)

    mapa_objetivos = objetivos.set_index("vendedor")["objetivo"]
    agrupado["objetivo"] = agrupado["vendedor"].map(mapa_objetivos)
    agrupado["cumplimiento"] = ((agrupado["importe"] / agrupado["objetivo"]) * 100).round(1)
    agrupado["cumplido"] = agrupado["importe"] >= agrupado["objetivo"]

    return agrupado[["vendedor", "ventas", "importe", "objetivo", "cumplimiento", "cumplido"]]


def evolucion_mensual(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una fila por mes, en orden, con las columnas mes, importe y variacion.

    ``importe`` va redondeado a dos decimales. ``variacion`` es el cambio en
    porcentaje respecto al mes anterior, con un decimal; en el primer mes es
    un valor ausente. El índice va de 0 en adelante.
    """
    mensual = (
        df.groupby("mes", as_index=False)["importe"]
        .sum()
        .sort_values(by="mes", ascending=True)
        .reset_index(drop=True)
    )
    mensual["importe"] = mensual["importe"].round(2)
    mensual["variacion"] = (mensual["importe"].pct_change() * 100).round(1)
    return mensual[["mes", "importe", "variacion"]]


def generar_graficos(df: pd.DataFrame, carpeta: str | Path) -> list[Path]:
    """Guarda dos gráficos en ``carpeta`` y devuelve sus rutas, en este orden.

1. ``importe_por_vendedor.png``: barras, de mayor a menor importe.
2. ``evolucion_mensual.png``: líneas con el importe de cada mes.

    Crea la carpeta si no existe. Cada gráfico lleva título y etiqueta en el
    eje Y. Las figuras se cierran después de guardarlas.
    """
    destino = Path(carpeta)
    destino.mkdir(parents=True, exist_ok=True)

    # 1. Gráfico de barras: importe por vendedor de mayor a menor
    por_vendedor = df.groupby("vendedor")["importe"].sum().sort_values(ascending=False)
    ruta_vendedores = destino / "importe_por_vendedor.png"

    fig_vend, ax_vend = plt.subplots()
    ax_vend.bar(por_vendedor.index.astype(str), por_vendedor.values)
    ax_vend.set_title("Importe por vendedor")
    ax_vend.set_ylabel("Importe (€)")
    fig_vend.tight_layout()
    fig_vend.savefig(ruta_vendedores, format="png", dpi=150)
    plt.close(fig_vend)

    # 2. Gráfico de líneas: evolución mensual
    mensual = df.groupby("mes")["importe"].sum().sort_index()
    ruta_mensual = destino / "evolucion_mensual.png"

    fig_mes, ax_mes = plt.subplots()
    ax_mes.plot(mensual.index.astype(str), mensual.values, marker="o")
    ax_mes.set_title("Evolución mensual de ventas")
    ax_mes.set_ylabel("Importe (€)")
    ax_mes.grid(True)
    fig_mes.tight_layout()
    fig_mes.savefig(ruta_mensual, format="png", dpi=150)
    plt.close(fig_mes)

    return [ruta_vendedores, ruta_mensual]


def exportar(tabla: pd.DataFrame, ruta: str | Path) -> None:
    """Escribe la tabla en un CSV en UTF-8, sin la columna del índice.

    Crea la carpeta de destino si no existe.
    """
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(destino, index=False, encoding="utf-8")


def main() -> None:
    """Ejecuta el análisis completo con los datos del módulo."""
    ventas = preparar(cargar(DATOS / "ventas_2026.csv"))
    objetivos = pd.read_csv(DATOS / "objetivos.csv")

    print("INDICADORES")
    for nombre, valor in indicadores(ventas).items():
        print(f"  {nombre:<22}{valor}")
    print()
    print("RANKING DE VENDEDORES")
    ranking = ranking_vendedores(ventas, objetivos)
    print(ranking.to_string(index=False))
    print()
    print("EVOLUCIÓN MENSUAL")
    print(evolucion_mensual(ventas).to_string(index=False))

    exportar(ranking, SALIDA / "ranking_vendedores.csv")
    exportar(evolucion_mensual(ventas), SALIDA / "evolucion_mensual.csv")
    for ruta in generar_graficos(ventas, SALIDA):
        print(f"Gráfico guardado en {ruta}")


if __name__ == "__main__":
    main()