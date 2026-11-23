"""Módulo 2 - Práctica 2, parte A: adivina el número."""

import random

MINIMO = 1
MAXIMO = 100
MAX_INTENTOS = 7


def evaluar_intento(secreto: int, intento: int) -> str:
    """Compara el intento con el número secreto.

    Devuelve "acierto", "mayor" si el secreto es mayor que el intento o
    "menor" si el secreto es menor.

    >>> evaluar_intento(50, 30)
    'mayor'
    """
    if intento == secreto:
        return "acierto"
    if secreto > intento:
        return "mayor"
    return "menor"


def es_intento_valido(texto: str) -> bool:
    """Indica si ``texto`` es un entero entre MINIMO y MAXIMO.

    >>> es_intento_valido("50"), es_intento_valido("abc"), es_intento_valido("101")
    (True, False, False)
    """
    try:
        numero = int(texto.strip())
    except ValueError:
        return False
    return MINIMO <= numero <= MAXIMO


def jugar(secreto: int, max_intentos: int = MAX_INTENTOS) -> bool:
    """Juega una partida y devuelve True si el jugador acierta.

    En cada turno pide un número con input(). Una entrada no válida no
    consume intento. Tras cada intento fallido imprime una pista.
    """
    intentos_usados = 0

    while intentos_usados < max_intentos:
        entrada = input(f"Intento {intentos_usados + 1} de {max_intentos}: ")

        if not es_intento_valido(entrada):
            print(f"Escribe un número entre {MINIMO} y {MAXIMO}.")
            continue

        intento = int(entrada.strip())
        intentos_usados += 1
        resultado = evaluar_intento(secreto, intento)

        if resultado == "acierto":
            print(f"¡Correcto! Lo has adivinado en {intentos_usados} intentos.")
            return True
        if resultado == "mayor":
            print("El número secreto es mayor.")
        else:
            print("El número secreto es menor.")

    print(f"Has agotado los intentos. El número era {secreto}.")
    return False


def main() -> None:
    """Genera un número secreto al azar y lanza una partida."""
    secreto = random.randint(MINIMO, MAXIMO)
    jugar(secreto)


"""==========================================="""
"""Ampliación Opcional"""
"""==========================================="""


def jugar_ordenador(
    minimo: int = MINIMO,
    maximo: int = MAXIMO,
    max_intentos: int = MAX_INTENTOS,
) -> bool:
    """El ordenador intenta adivinar un número pensado por el usuario."""
    print(f"Piensa un número entre {minimo} y {maximo}.")
    bajo = minimo
    alto = maximo
    intentos_usados = 0

    while bajo <= alto and intentos_usados < max_intentos:
        intentos_usados += 1
        propuesta = (bajo + alto) // 2
        respuesta = input(
            f"Intento {intentos_usados} de {max_intentos}: ¿Es {propuesta}? "
            "(acierto / mayor / menor): "
        ).strip().lower()

        if respuesta in ("acierto", "=", "si", "sí"):
            print(f"¡Lo adiviné en {intentos_usados} intentos!")
            return True
        if respuesta in ("mayor", ">", "+"):
            bajo = propuesta + 1
        elif respuesta in ("menor", "<", "-"):
            alto = propuesta - 1
        else:
            print("Responde con 'acierto', 'mayor' o 'menor'.")
            intentos_usados -= 1

    print("No he podido adivinarlo. ¿Seguro que no cambiaste de número?")
    return False


def main_ampliado() -> None:
    """Permite elegir modo de juego y repetir partidas."""
    while True:
        print("\n--- Adivina el número ---")
        print("1. Adivinas tú")
        print("2. Adivina el ordenador")
        modo = input("Elige un modo (1-2): ").strip()

        if modo == "2":
            jugar_ordenador()
        else:
            secreto = random.randint(MINIMO, MAXIMO)
            jugar(secreto)

        otra = input("¿Quieres jugar otra vez? (s/n): ").strip().lower()
        if otra not in ("s", "si", "sí"):
            break


if __name__ == "__main__":
    main_ampliado()