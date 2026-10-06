"""
ACM ICPC Guangzhou Summer Series 2017 — C: Count Equation Solutions («Contar las soluciones de una ecuación»)
Ejecutar: python countequation.py < countequation.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Contar las soluciones enteras de
        a1·x1 − a2·x2 + a3·x3 − a4·x4 + a5·x5 − a6·x6 = 0
    con cada variable en 1 ≤ xi ≤ M.

QUÉ HAY QUE HACER
    Entrada: hasta 600 casos hasta fin de archivo; cada uno es M en una
    línea y los 6 coeficientes en la siguiente.
    Salida:  por caso, el número de soluciones.
    Restricciones clave: 1 ≤ M ≤ 100, 1 ≤ ai ≤ 10^6. Probar las M^6 = 10^12
    asignaciones es imposible.

IDEA Y ALGORITMO
    Encuentro en el medio (meet in the middle). Se pasa la mitad negativa
    al otro lado:
        a1·x1 + a3·x3 + a5·x5  =  a2·x2 + a4·x4 + a6·x6.
    Sea cI(v) cuántas ternas (x1, x3, x5) dan suma v en el lado izquierdo y
    cD(v) lo mismo para el derecho. La respuesta es Σ_v cI(v)·cD(v): cada
    terna izquierda se combina con cada terna derecha de igual suma.
    Cada lado tiene M³ ≤ 10^6 sumas, así que se pasa de 10^12 a ~2·10^6.
    Para que Python lo haga rápido todo el trabajo pesado va por funciones
    en C: las sumas se generan con map(int.__add__, …) sobre la lista de
    sumas de dos variables y el lado izquierdo se cuenta con
    collections.Counter; las sumas del lado derecho se filtran con
    filter(dict.__contains__) y se suman sus conteos con map/sum, sin
    bucles de Python por elemento.

MACROALGORITMO
    1. Leer M y los coeficientes.
    2. Lado izquierdo: lista de a3·x3 + a5·x5 (M² valores); para cada x1
       sumarle a1·x1 y contar todo en un Counter (M³ valores).
    3. Lado derecho: para cada x2, generar las M² sumas a2·x2 + a4·x4 +
       a6·x6, quedarse con las que están en el Counter y sumar sus conteos
       (eso es Σ_v cI(v)·cD(v)).
    5. Imprimir la suma. (Casos repetidos idénticos se responden de caché.)

COMPLEJIDAD
    O(M³) tiempo y memoria por caso. Con M = 100 son 2·10^6 sumas: 0.3–0.5 s
    por caso en Python (0.5 s con ai aleatorios hasta 10^6, 0.3 s con ai
    pequeños y muchas sumas repetidas). 600 casos con M = 100 tomarían
    ~3–5 minutos: muy por encima del límite de 5 s (en C++ también sería
    pesado: 1.2·10^9 operaciones de hash). Si la mayoría de los casos
    tienen M pequeño, va mejor (M = 30: ~0.01 s por caso; 600 casos con
    M = 30 ≈ 6 s).

EJEMPLO A MANO
    M = 2, todos los ai = 1: x1+x3+x5 = x2+x4+x6 con xi ∈ {1,2}. Las sumas
    3,4,5,6 aparecen 1,3,3,1 veces en cada lado → 1+9+9+1 = 20. ✔

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/C")
    - Fuerza bruta: OK en 300 casos aleatorios (M ≤ 6, ai ≤ 6 para forzar
      muchas colisiones, y ai ≤ 10^6) contra el recorrido de las M^6
      asignaciones.
"""
import sys
from collections import Counter


def contar_lado(M, a, b, c):
    """Counter con la cantidad de ternas (x, y, z) ∈ [1,M]³ para cada valor
    de a·x + b·y + c·z. Todo el trabajo masivo ocurre en funciones de C."""
    rango = range(1, M + 1)
    dobles = [b * y + c * z for y in rango for z in rango]   # M² sumas
    conteo = Counter()
    for x in rango:
        # map(int.__add__, ...) suma a·x a cada valor sin bucle en Python;
        # Counter.update cuenta el iterable en C.
        conteo.update(map((a * x).__add__, dobles))
    return conteo


def resolver(M, coef):
    a1, a2, a3, a4, a5, a6 = coef
    izquierdo = contar_lado(M, a1, a3, a5)
    # Lado derecho: no hace falta contarlo. Cada terna derecha con suma v
    # aporta cI(v) soluciones, así que se recorren sus M³ sumas, se filtran
    # las que existen en el lado izquierdo (búsqueda en dict hecha en C) y
    # se suman sus conteos. Equivale a Σ_v cI(v)·cD(v).
    rango = range(1, M + 1)
    dobles = [a4 * y + a6 * z for y in rango for z in rango]
    presente = izquierdo.__contains__
    conteo_de = izquierdo.__getitem__
    total = 0
    for x in rango:
        sumas = map((a2 * x).__add__, dobles)
        total += sum(map(conteo_de, filter(presente, sumas)))
    return total


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    cache = {}
    pos = 0
    while pos + 7 <= len(datos):
        M = int(datos[pos])
        coef = tuple(int(v) for v in datos[pos + 1:pos + 7])
        pos += 7
        clave = (M, coef)
        if clave not in cache:
            cache[clave] = resolver(M, coef)
        salida.append(str(cache[clave]))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
