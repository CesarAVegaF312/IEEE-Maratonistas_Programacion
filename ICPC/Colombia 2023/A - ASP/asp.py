"""
Colombia 2023 — A: ASP («Contraseñas seguras»)
Ejecutar: python asp.py < asp.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    John arma sus contraseñas ("asp") con un alfabeto de N símbolos bajo dos
    reglas: ninguna subpalabra de 2 o más símbolos consecutivos aparece dos
    veces, y nunca hay dos símbolos iguales seguidos. Quiere saber qué tan
    larga puede ser una asp.

QUÉ HAY QUE HACER
    Entrada: varios casos, cada uno una línea con N (1 < N < 1000); termina
             con una línea "0".
    Salida:  por caso, la longitud máxima de una asp con N símbolos.
    Restricciones clave: N < 1000 (la respuesta llega a ~10^6, cabe en int).

IDEA Y ALGORITMO
    Grafo de De Bruijn / circuito euleriano.
    Observación 1: basta con que los PARES consecutivos (bigramas) sean todos
    distintos; si dos subpalabras más largas se repitieran, también se
    repetiría su primer bigrama. Y la regla de "no dos iguales seguidos"
    prohíbe los bigramas xx. Así que una asp es un camino en el grafo
    dirigido completo sin lazos sobre N vértices (arista x->y por cada
    bigrama xy con x != y) que no repite aristas.
    Observación 2: ese grafo tiene N(N-1) aristas y cada vértice tiene grado
    de entrada = grado de salida = N-1, y es fuertemente conexo, así que
    tiene un circuito euleriano que usa TODAS las aristas una vez.
    Un camino de E aristas es una palabra de E+1 símbolos, luego la máxima
    longitud es N(N-1) + 1 (no se puede más: no hay más bigramas válidos).

MACROALGORITMO
    1. Leer cada N hasta encontrar 0.
    2. Imprimir N*(N-1) + 1.

COMPLEJIDAD
    O(1) por caso, memoria O(1).

EJEMPLO A MANO
    N=2: aristas a->b, b->a; circuito "aba", longitud 3.
    N=3: 6 aristas, p. ej. "abacbca", longitud 7.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2023/A")
    - Fuerza bruta: búsqueda exhaustiva (DFS) de la asp más larga para
      N = 2, 3, 4 coincide con la fórmula (3, 7, 13).
"""
import sys


def longitud_maxima(n):
    # Número de bigramas válidos (aristas) + 1 símbolo inicial.
    return n * (n - 1) + 1


def main():
    salida = []
    for token in sys.stdin.buffer.read().split():
        n = int(token)
        if n == 0:
            break
        salida.append(str(longitud_maxima(n)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
