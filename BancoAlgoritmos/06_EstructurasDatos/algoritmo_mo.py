"""
Estructuras de datos — Algoritmo de Mo («Mo's algorithm»)
Nivel: Avanzado
Ejecutar: python algoritmo_mo.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Responder Q consultas OFFLINE sobre rangos a[l..r-1] de un arreglo
    fijo cuando la respuesta se puede mantener al AGREGAR o QUITAR un
    elemento en un extremo en O(1), pero no se puede combinar a partir de
    dos mitades (por eso no sirve un segment tree). Ejemplos: número de
    valores distintos, Σ cnt[v]²·v («potencia» del subarreglo), cuántos
    pares de elementos iguales, moda con conteos…
    Señales en el enunciado: N, Q hasta ~10^5 (en Python mejor <= 5·10^4),
    consultas de rango sin actualizaciones y conocidas de antemano, una
    estadística basada en FRECUENCIAS dentro del rango.

FUNCIÓN
    orden_mo(consultas, n) -> list[int]
        Índices de las consultas (l, r) en el orden de Mo.
    mo_distintos(a, consultas) -> list[int]
        Valores distintos en a[l:r] para cada consulta, en orden original.
    mo_potencia(a, consultas) -> list[int]
        Σ_v cnt_v² · v sobre a[l:r] (Codeforces 86D «Powerful array»).
    Rangos semiabiertos [l, r), índices desde 0.

IDEA Y ALGORITMO
    Se mantiene una ventana actual [L, R) con sus frecuencias y la
    respuesta. Pasar de una consulta a otra cuesta |ΔL| + |ΔR| pasos de
    agregar/quitar. La clave es el ORDEN de las consultas:
      - Partir los índices en bloques de tamaño B; ordenar por bloque de
        l y, dentro del bloque, por r.
      - Dentro de un bloque, R solo avanza (a lo sumo N pasos por bloque,
        N/B bloques → N²/B en total) y L se mueve a lo sumo B por consulta
        (Q·B en total).
      - Total O(N²/B + Q·B), mínimo con B ≈ N/√Q: O(N·√Q).
    Truco par/impar: en bloques impares ordenar r DECRECIENTE; así R no
    vuelve al principio al cambiar de bloque (≈ 2x más rápido).
    Siempre EXTENDER antes de ENCOGER (primero agrandar la ventana, luego
    achicarla) para que nunca quede con l > r y los conteos negativos.
    El ingenuo recorre cada rango: O(N·Q). Con N = Q = 10^5 son 10^10
    contra ~3·10^7 de Mo.

MACROALGORITMO
    1. B = max(1, N // √Q). Ordenar consultas por (l // B, r o -r según la
       paridad del bloque).
    2. L = R = 0, cnt = {}, actual = 0.
    3. Para cada consulta (l, r) en ese orden:
       a. mientras R < r: agregar a[R]; R += 1
       b. mientras L > l: L -= 1; agregar a[L]
       c. mientras R > r: R -= 1; quitar a[R]
       d. mientras L < l: quitar a[L]; L += 1
       e. resp[id] = actual.
    4. Devolver resp en el orden original.

COMPLEJIDAD
    O((N + Q)·√N) operaciones de agregar/quitar (más precisamente
    O(N·√Q + Q·B)), memoria O(N + Q). En Python es la parte delicada:
    ~10^7 pasos simples por segundo, así que N = Q = 5·10^4 va en ~1–2 s;
    con 10^5/10^5 puede pasar de 3 s. Escribir agregar/quitar EN LÍNEA (sin
    llamar funciones) y usar listas en vez de diccionarios.

EJEMPLO A MANO
    a = [1, 1, 2, 1, 3], consultas (0,2) (1,5) (2,4); N = 5, Q = 3 →
    B = 5 // isqrt(3) = 5: todas en el bloque 0, orden por r:
    (0,2), (2,4), (1,5)
      (0,2): agregar a[0]=1, a[1]=1                 → {1:2}         → 1
      (2,4): agregar a[2]=2, a[3]=1; quitar a[0], a[1] → {1:1, 2:1} → 2
      (1,5): agregar a[4]=3; L baja a 1: agregar a[1]=1
                                       → {1:2, 2:1, 3:1}            → 3
    Respuestas en orden original: [1, 3, 2].
    Potencia de (1,5) = [1,2,1,3]: 2²·1 + 1²·2 + 1²·3 = 9.

ERRORES TÍPICOS
    - Encoger antes de extender: la ventana queda «negativa» y los conteos
      se rompen (o hay que cuidar mucho el orden).
    - Bloque fijo B = √N con Q mucho menor que N: B ≈ N/√Q es mejor.
    - Usarlo con actualizaciones (hace falta Mo con tiempo, O(N^(5/3))) o
      con consultas en línea.
    - Funciones agregar/quitar como lambdas: en Python la llamada cuesta
      más que el trabajo; escribirlas en el cuerpo del ciclo.

VARIANTES Y RELACIONADOS
    - Mo con actualizaciones (tercera dimensión: tiempo).
    - Mo en árboles (sobre el recorrido de Euler).
    - Orden de Hilbert: ordena por la posición en la curva de Hilbert; aún
      más rápido en la práctica.
    - Si la consulta es «distintos en rango», también sale offline con
      Fenwick en O((N+Q) log N): 06_EstructurasDatos/consultas_offline.py.
    - 06_EstructurasDatos/descomposicion_raiz.py (la misma idea de √N).

DÓNDE PRACTICAR
    - (No hay problemas del repo ICPC/ que lo usen.)
    - Codeforces 86D «Powerful array» (mo_potencia); SPOJ DQUERY «D-query».

VERIFICACIÓN
    - Pruebas (python algoritmo_mo.py): contra el cálculo directo con
      Counter sobre a[l:r] en 500 arreglos aleatorios con 40 consultas cada
      uno (rangos vacíos incluidos), más casos borde y N = Q = 3·10^4.
"""
import random
from collections import Counter
from math import isqrt


def orden_mo(consultas, n):
    """Índices de consultas (l, r) ordenados por bloque de l (r alternando)."""
    q = max(1, len(consultas))
    b = max(1, n // max(1, isqrt(q)))           # B ≈ N / √Q
    def clave(i):
        l, r = consultas[i]
        bloque = l // b
        return (bloque, r if bloque % 2 == 0 else -r)   # truco par/impar
    return sorted(range(len(consultas)), key=clave)


def mo_distintos(a, consultas):
    """Número de valores distintos en a[l:r] para cada consulta."""
    # Comprimir valores a 0..K-1 para usar una lista de conteos (más rápida).
    ids = {v: k for k, v in enumerate(set(a))}
    c = [ids[v] for v in a]
    cnt = [0] * len(ids)
    resp = [0] * len(consultas)
    L = R = actual = 0                          # ventana actual [L, R)
    for qi in orden_mo(consultas, len(a)):
        l, r = consultas[qi]
        # Primero extender…
        while R < r:
            v = c[R]; R += 1
            cnt[v] += 1
            if cnt[v] == 1: actual += 1
        while L > l:
            L -= 1; v = c[L]
            cnt[v] += 1
            if cnt[v] == 1: actual += 1
        # …luego encoger.
        while R > r:
            R -= 1; v = c[R]
            cnt[v] -= 1
            if cnt[v] == 0: actual -= 1
        while L < l:
            v = c[L]; L += 1
            cnt[v] -= 1
            if cnt[v] == 0: actual -= 1
        resp[qi] = actual
    return resp


def mo_potencia(a, consultas):
    """Σ cnt_v² · v sobre a[l:r] (Codeforces 86D)."""
    # Agregar v con conteo k → k+1 suma ((k+1)² - k²)·v = (2k+1)·v.
    ids = {v: k for k, v in enumerate(set(a))}
    c = [ids[v] for v in a]
    cnt = [0] * len(ids)
    resp = [0] * len(consultas)
    L = R = actual = 0
    for qi in orden_mo(consultas, len(a)):
        l, r = consultas[qi]
        while R < r:
            v = c[R]; actual += (2 * cnt[v] + 1) * a[R]; cnt[v] += 1; R += 1
        while L > l:
            L -= 1; v = c[L]; actual += (2 * cnt[v] + 1) * a[L]; cnt[v] += 1
        while R > r:
            R -= 1; v = c[R]; cnt[v] -= 1; actual -= (2 * cnt[v] + 1) * a[R]
        while L < l:
            v = c[L]; cnt[v] -= 1; actual -= (2 * cnt[v] + 1) * a[L]; L += 1
        resp[qi] = actual
    return resp


def demo():
    a = [1, 1, 2, 1, 3]
    cons = [(0, 2), (1, 5), (2, 4)]
    print("a =", a, " consultas =", cons)
    print("orden de Mo  =", [cons[i] for i in orden_mo(cons, len(a))])
    print("distintos    =", mo_distintos(a, cons))     # [1, 3, 2]
    print("potencia     =", mo_potencia(a, cons))      # [4, 9, 3]


def _potencia_bruta(seg):
    return sum(k * k * v for v, k in Counter(seg).items())


def pruebas():
    random.seed(86)

    # Casos borde
    assert mo_distintos([], []) == [] and mo_potencia([], [(0, 0)]) == [0]
    assert mo_distintos([7], [(0, 1), (0, 0), (1, 1)]) == [1, 0, 0]
    assert mo_distintos([2, 2, 2, 2], [(0, 4), (1, 3)]) == [1, 1]
    assert mo_potencia([2, 2, 2, 2], [(0, 4)]) == [32]

    for _ in range(500):
        n = random.randint(0, 25)
        a = [random.randint(1, 6) for _ in range(n)]
        cons = []
        for _ in range(40):
            l = random.randint(0, n)
            cons.append((l, random.randint(l, n)))
        assert mo_distintos(a, cons) == [len(set(a[l:r])) for l, r in cons]
        assert mo_potencia(a, cons) == [_potencia_bruta(a[l:r]) for l, r in cons]

    # N = Q = 3·10^4: tiempo y una muestra contra la fuerza bruta
    n = 30000
    a = [random.randint(1, 1000) for _ in range(n)]
    cons = []
    for _ in range(n):
        l = random.randrange(n)
        cons.append((l, random.randint(l, n)))
    res = mo_distintos(a, cons)
    for i in random.sample(range(n), 50):
        l, r = cons[i]
        assert res[i] == len(set(a[l:r]))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
