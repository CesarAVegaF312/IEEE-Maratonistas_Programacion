"""
Búsqueda completa — Encuentro en el medio («Meet in the middle»)
Nivel: Intermedio
Ejecutar: python meet_in_the_middle.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Bajar una búsqueda de 2^N a ~2·2^(N/2): partir los elementos en dos
    mitades, enumerar TODO lo de cada mitad por separado y combinar las dos
    listas con un diccionario, ordenamiento + búsqueda binaria o dos
    punteros. El ejemplo clásico: contar subconjuntos con suma X para
    N ≤ 40 (2^40 ≈ 10^12 imposible; 2·2^20 ≈ 2·10^6 sí).
    Señales en el enunciado: N ≈ 30–40 (demasiado para 2^N, muy poco para
    pensar en DP con sumas de hasta 10^9), valores grandes (no sirve la
    mochila por suma), «cuántos subconjuntos / combinaciones suman…»,
    ecuaciones con 4–6 variables en rangos chicos.

FUNCIÓN
    sumas_de(a) -> list[int]
        Las 2^len(a) sumas de subconjuntos de a (con repetidos).
    contar_subconjuntos_suma(a, x) -> int
        Cuántos subconjuntos (por índice, incluido el vacío) suman x.
    mejor_suma_hasta(a, limite) -> int
        Mayor suma de un subconjunto que no pase de limite (a ≥ 0, el
        vacío da 0). Combina con ordenamiento + dos punteros.

IDEA Y ALGORITMO
    Todo subconjunto S de a se parte en S ∩ izquierda y S ∩ derecha, y
    suma(S) = suma(izq) + suma(der). Por eso:
        #{S : suma(S) = x} = Σ_{s en sumas_izq}  #{d en sumas_der : d = x − s}
    Con un Counter de las sumas de la derecha, cada término es O(1). Se
    enumeran 2^(N/2) sumas por lado en vez de 2^N subconjuntos.
    Generar las sumas de una mitad en O(2^(N/2)): empezar con [0] y por
    cada elemento v duplicar la lista: sumas + [s + v for s in sumas]
    (cada subconjunto con o sin v).
    Mejor suma ≤ L: ordenar ambas listas; con i subiendo por la izquierda
    y j bajando por la derecha, para cada izquierda el mejor compañero es
    la mayor derecha con izq + der ≤ L, y ese índice solo baja al crecer
    izq (dos punteros).

MACROALGORITMO
    1. Partir a en izquierda = a[:n//2] y derecha = a[n//2:].
    2. Enumerar las sumas de cada mitad (2^(n/2) cada una).
    3. Contar las sumas de la derecha en un Counter.
    4. Para cada suma s de la izquierda, sumar cuenta[x − s].
    (Variante con límite)
    5. Ordenar ambas listas; i recorre la izquierda creciente, j empieza al
       final de la derecha y baja mientras izq[i] + der[j] > L.
    6. Actualizar la mejor suma con izq[i] + der[j] (si j ≥ 0).

COMPLEJIDAD
    Tiempo O(2^(N/2)) con diccionario (O(2^(N/2) · N) si se ordena);
    memoria O(2^(N/2)). N = 40: 2 listas de 2^20 ≈ 10^6 enteros, ~0,5–1 s
    en Python usando operaciones en C (Counter, comprensiones, map).

EJEMPLO A MANO
    a = [3, 1, 4, 2], x = 5
      izquierda = [3, 1] → sumas [0, 3, 1, 4]
      derecha   = [4, 2] → sumas [0, 4, 2, 6] → cuenta {0:1, 4:1, 2:1, 6:1}
      s = 0 → falta 5: 0    s = 3 → falta 2: 1  ({3, 2})
      s = 1 → falta 4: 1 ({1, 4})    s = 4 → falta 1: 0
    → 2 subconjuntos: {3, 2} y {1, 4}

ERRORES TÍPICOS
    - Guardar los subconjuntos como listas: solo hace falta la suma (u otro
      resumen pequeño), si no se acaba la memoria.
    - Generar cada suma recorriendo los bits (O(2^(N/2)·N)) en Python puro:
      es varias veces más lento que duplicar la lista.
    - Olvidar el subconjunto vacío en alguna mitad (o contarlo cuando el
      enunciado pide subconjuntos no vacíos: restar 1 si x == 0).
    - Usar set en vez de Counter: se pierden los repetidos y el conteo sale menor.

VARIANTES Y RELACIONADOS
    - 4 listas «A + B + C + D = 0»: sumas de A+B en Counter, recorrer C+D.
    - Mochila con N ≤ 40 y pesos enormes: dominancia en una mitad +
      búsqueda binaria.
    - BFS bidireccional: encuentro en el medio sobre grafos de estados.
    - Relacionados: subconjuntos_mascaras.py, 00_Base/dos_punteros.py,
      00_Base/conteo_diccionarios.py.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/C - Count Equation Solutions (6 variables partidas en 3 + 3)
    - CSES «Meet in the Middle»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (las 2^N máscaras) en 800 casos
      aleatorios con N ≤ 10 para cada función, casos borde y dos casos de
      N = 40 con respuesta conocida (C(40, 20) y 2^40; ~0,3 s cada uno)
      (python meet_in_the_middle.py)
"""
import random
from collections import Counter
from math import comb


def sumas_de(a):
    """Las 2^len(a) sumas de subconjuntos de a."""
    sumas = [0]
    for v in a:
        sumas += [s + v for s in sumas]     # cada subconjunto, sin v y con v
    return sumas


def contar_subconjuntos_suma(a, x):
    """Cuántos subconjuntos (por índice, incluido el vacío) suman x."""
    mitad = len(a) // 2
    izq = sumas_de(a[:mitad])
    cuenta_der = Counter(sumas_de(a[mitad:]))
    # Σ cuenta_der[x - s]; .get evita insertar claves nuevas en el Counter
    return sum(cuenta_der.get(x - s, 0) for s in izq)


def mejor_suma_hasta(a, limite):
    """Mayor suma de un subconjunto de a (a >= 0) que no pase de limite."""
    mitad = len(a) // 2
    izq = sorted(sumas_de(a[:mitad]))
    der = sorted(sumas_de(a[mitad:]))
    mejor = 0
    j = len(der) - 1
    for s in izq:                           # s crece -> el compañero máximo j solo baja
        while j >= 0 and s + der[j] > limite:
            j -= 1
        if j < 0:
            break                           # ni con la menor derecha cabe
        mejor = max(mejor, s + der[j])
    return mejor


def demo():
    a = [3, 1, 4, 2]
    print("a =", a)
    print("sumas izquierda:", sumas_de(a[:2]), " derecha:", sumas_de(a[2:]))
    print("contar_subconjuntos_suma(a, 5) =", contar_subconjuntos_suma(a, 5))       # 2
    print("mejor_suma_hasta([7, 11, 5, 9], 20) =", mejor_suma_hasta([7, 11, 5, 9], 20))  # 20


def pruebas():
    random.seed(40)

    # Casos borde
    assert sumas_de([]) == [0]
    assert contar_subconjuntos_suma([], 0) == 1 and contar_subconjuntos_suma([], 3) == 0
    assert contar_subconjuntos_suma([5], 5) == 1
    assert contar_subconjuntos_suma([2, 2, 2], 4) == 3
    assert mejor_suma_hasta([], 10) == 0
    assert mejor_suma_hasta([50], 10) == 0

    for _ in range(800):
        n = random.randint(0, 10)
        a = [random.randint(-10, 10) for _ in range(n)]
        x = random.randint(-20, 20)
        bruta = sum(1 for m in range(1 << n) if sum(a[i] for i in range(n) if m >> i & 1) == x)
        assert contar_subconjuntos_suma(a, x) == bruta

        b = [random.randint(0, 10**6) for _ in range(n)]
        lim = random.randint(0, 3 * 10**6)
        nb = len(b)
        bruta = max(s for s in (sum(b[i] for i in range(nb) if m >> i & 1) for m in range(1 << nb)) if s <= lim)
        assert mejor_suma_hasta(b, lim) == bruta

    # N = 40 con respuesta conocida (también mide el tiempo del caso grande)
    assert contar_subconjuntos_suma([1] * 40, 20) == comb(40, 20)
    assert contar_subconjuntos_suma([0] * 40, 0) == 2 ** 40


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
