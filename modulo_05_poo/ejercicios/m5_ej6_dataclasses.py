"""Módulo 5 - Ejercicio 6: dataclasses y composición.

En este ejercicio las clases se escriben enteras: no hay plantilla. El
enunciado está en ejercicios/README.md.
"""

from dataclasses import dataclass, field
import math


@dataclass(frozen=True)
class Punto:
    """Representa un punto inmutable en el plano cartesiano."""

    x: float = 0.0
    y: float = 0.0

    def distancia(self, otro: "Punto") -> float:
        """Devuelve la distancia euclídea hasta ``otro`` punto, con dos decimales."""
        return round(math.hypot(self.x - otro.x, self.y - otro.y), 2)


@dataclass
class LineaPedido:
    """Representa una línea de pedido con producto, unidades y precio unitario."""

    producto: str
    unidades: int
    precio: float

    def __post_init__(self) -> None:
        if self.unidades <= 0:
            raise ValueError("Las unidades deben ser un número positivo.")

    @property
    def importe(self) -> float:
        """Devuelve el importe de la línea (unidades * precio), con dos decimales."""
        return round(self.unidades * self.precio, 2)


@dataclass
class Pedido:
    """Representa un pedido compuesto por número, cliente y líneas."""

    numero: int
    cliente: str
    lineas: list[LineaPedido] = field(default_factory=list)

    def anadir(self, producto: str, unidades: int, precio: float) -> LineaPedido:
        """Crea una línea de pedido, la añade al pedido y la devuelve."""
        linea = LineaPedido(producto=producto, unidades=unidades, precio=precio)
        self.lineas.append(linea)
        return linea

    @property
    def total(self) -> float:
        """Devuelve la suma de los importes de todas las líneas, con dos decimales."""
        return round(sum(linea.importe for linea in self.lineas), 2)

    def __len__(self) -> int:
        """Devuelve el número de líneas del pedido."""
        return len(self.lineas)

    def productos(self) -> list[str]:
        """Devuelve los nombres de los productos sin repetir y en orden alfabético."""
        return sorted({linea.producto for linea in self.lineas})