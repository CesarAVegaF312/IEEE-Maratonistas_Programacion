"""
Colombia 2026 — B: Bankey («Clave bancaria»)
Ejecutar: python bankey.py < bankey.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Pedro esconde la clave del banco en una secuencia de N dígitos y un entero
    M: la clave es la mayor suma de M dígitos ubicados en posiciones
    consecutivas de la MISMA paridad (p. ej. posiciones 3, 5, 7, 9). Las
    posiciones fuera de la secuencia (antes del inicio o después del final)
    valen 0.

QUÉ HAY QUE HACER
    Entrada: varios casos; cada uno es "N M" y en la línea siguiente los N
             dígitos pegados. Termina con "0 0".
    Salida:  una línea por caso con la clave (un entero).
    Restricciones clave: 1 <= M <= N < 10^5.

IDEA Y ALGORITMO
    Separar los dígitos en dos listas: los de posiciones impares (1, 3, 5, …)
    y los de posiciones pares (2, 4, 6, …). "M posiciones consecutivas de la
    misma paridad" son exactamente M elementos SEGUIDOS de una de esas dos
    listas (más, quizá, posiciones de relleno que valen 0).
    → Ventana deslizante de tamaño fijo / sumas prefijas.

    ¿Y el relleno con ceros? Una ventana que se sale de la lista solo cubre
    MENOS dígitos reales (y los dígitos son >= 0), así que nunca supera a una
    ventana que esté completamente dentro. Por eso basta con:
        - si la lista tiene al menos M elementos: máxima suma de M seguidos;
        - si tiene menos de M: la suma de la lista entera (la ventana la
          cubre toda y el resto es relleno 0).
    Es decir, ventanas de tamaño w = min(M, longitud de la lista).

    Con sumas prefijas P (P[i] = suma de los primeros i elementos), la suma
    de la ventana que empieza en i es P[i+w] - P[i]; el máximo se calcula en
    una sola pasada (y en C, con map/max, para que Python sea rápido).

MACROALGORITMO
    1. Leer N, M y los N dígitos (hasta "0 0").
    2. impares = dígitos[0::2], pares = dígitos[1::2] (posiciones desde 1).
    3. Para cada lista v: w = min(M, len(v)); P = sumas prefijas de v;
       mejor(v) = max(P[i+w] - P[i]).
    4. Imprimir max(mejor(impares), mejor(pares)).

COMPLEJIDAD
    O(N) tiempo y memoria por caso. Caso grande (20 casos con N = 99 999):
    ≈ 0.3 s.

EJEMPLO A MANO
    "7210396", M = 3: impares = 7,1,3,6 → ventanas 7+1+3 = 11, 1+3+6 = 10;
    pares = 2,0,9 → 11. Respuesta 11. Con M = 4: impares completa = 17.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/B")
    - Fuerza bruta (para CADA posición final p de -M·2 a N + 2M, sumar
      literalmente los M valores p, p-2, p-4, … con 0 fuera de rango):
      idéntica en 1000 casos aleatorios con N <= 30.
"""
import sys
from itertools import accumulate
from operator import sub


def mejor_ventana(v, m):
    """Mayor suma de min(m, len(v)) elementos seguidos de v (0 si v vacía)."""
    if not v:
        return 0
    w = min(m, len(v))
    pref = [0]
    pref.extend(accumulate(v))           # pref[i] = v[0] + … + v[i-1]
    # pref[i+w] - pref[i] = suma de la ventana v[i .. i+w-1]
    return max(map(sub, pref[w:], pref))


def main():
    datos = sys.stdin.buffer.read().split()
    idx, salida = 0, []
    while idx + 1 < len(datos):
        n, m = int(datos[idx]), int(datos[idx + 1])
        idx += 2
        if n == 0 and m == 0:            # fin de la entrada
            break
        # Los dígitos vienen pegados en una línea; por robustez se juntan
        # tokens hasta tener N dígitos (por si vinieran partidos).
        cadena = b""
        while len(cadena) < n and idx < len(datos):
            cadena += datos[idx]
            idx += 1
        digitos = [c - 48 for c in cadena[:n]]   # byte '7' (55) -> 7
        impares = digitos[0::2]          # posiciones 1, 3, 5, … (desde 1)
        pares = digitos[1::2]            # posiciones 2, 4, 6, …
        salida.append(max(mejor_ventana(impares, m), mejor_ventana(pares, m)))
    sys.stdout.write("\n".join(map(str, salida)) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
