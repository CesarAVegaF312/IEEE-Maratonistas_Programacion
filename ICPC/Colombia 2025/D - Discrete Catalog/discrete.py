"""
Colombia 2025 — D: Discrete Catalog («Catálogo discreto»)
Ejecutar: python discrete.py < discrete.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un centro de crisis simula desastres sobre n sitios. Un (n,k)-escenario es
    un subconjunto de k sitios escrito en orden creciente; todos los
    escenarios de tamaño k se numeran desde 0 en orden lexicográfico.

QUÉ HAY QUE HACER
    Entrada: casos de dos líneas: "n k" y luego a1 < a2 < ... < ak.
             El enunciado dice "dos líneas", pero el ejemplo trae 9 casos
             seguidos sin marcador de fin → se lee hasta fin de archivo.
    Salida:  por caso, el ID (posición 0-indexada en orden lexicográfico).
    Restricciones clave: n ≤ 60, así que el ID puede llegar a C(60,30) ≈ 1.2·10^17
             (no cabe en 32 bits; en Python no hay problema).

IDEA Y ALGORITMO
    "Ranking" de combinaciones (sistema numérico combinatorio):
    el ID de un escenario = cuántos escenarios van ANTES que él.
    Un escenario b va antes que a si en la primera posición i donde difieren
    b_i < a_i. Fijando que las posiciones 1..i-1 coinciden con a y que en la
    posición i se pone un valor v con a_{i-1} < v < a_i, las k−i posiciones
    restantes se eligen libremente entre los n−v valores mayores que v:
    C(n−v, k−i) formas. Sumando sobre todas las i y todos esos v:

        ID = Σ_{i=1..k}  Σ_{v=a_{i-1}+1}^{a_i − 1}  C(n − v, k − i),   a_0 = 0.

    Cada escenario anterior se cuenta exactamente una vez (por su primera
    posición de diferencia), así que la suma es exacta.
    Enumerar todos los escenarios es imposible (≈10^17), por eso se cuenta.

MACROALGORITMO
    1. Leer todos los enteros; procesar casos mientras queden datos.
    2. Para cada caso, recorrer las posiciones i = 1..k con el valor previo.
    3. Para cada valor v estrictamente entre el previo y a_i, sumar C(n−v, k−i).
    4. Imprimir la suma.

COMPLEJIDAD
    Tiempo O(n) términos binomiales por caso (math.comb), memoria O(k).

EJEMPLO A MANO
    n=5, k=3, a=[1,3,5]: i=1: ningún v entre 0 y 1. i=2: v=2 → C(3,1)=3.
    i=3: v=4 → C(1,0)=1. ID = 4 ✔.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/D")
    - Fuerza bruta (itertools.combinations en orden lexicográfico y buscar el
      índice): OK en 1000 casos aleatorios con n ≤ 12.
    - Caso grande (20 000 casos con n = 60): ~0.3 s.
"""
import sys
from math import comb


def id_escenario(n, k, a):
    """Número de k-subconjuntos de {1..n} lexicográficamente menores que a."""
    total = 0
    previo = 0
    for i, ai in enumerate(a, start=1):
        # Valores que podrían ir en la posición i y que son menores que a_i:
        # cada uno deja k-i posiciones libres entre los n-v valores mayores.
        for v in range(previo + 1, ai):
            total += comb(n - v, k - i)
        previo = ai
    return total


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    # Se lee hasta EOF (el ejemplo trae varios casos sin marcador de fin).
    while pos + 1 < len(datos):
        n, k = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        a = [int(t) for t in datos[pos:pos + k]]
        pos += k
        salida.append(str(id_escenario(n, k, a)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
