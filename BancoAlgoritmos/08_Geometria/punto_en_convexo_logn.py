r"""
Geometría — Punto en polígono convexo en O(log n) («point in convex polygon, binary search»)
Nivel: Avanzado
Ejecutar: python punto_en_convexo_logn.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Responder MUCHAS consultas «¿el punto p está dentro, en el borde o fuera
    del polígono convexo?» en O(log n) cada una, en vez de O(n). También es
    el patrón de «búsqueda binaria angular en un abanico» desde un vértice,
    útil para otras preguntas sobre convexos (qué dirección/arista ve un
    punto, en qué sector cae un rayo).
    Señales en el enunciado: un polígono (o envolvente) convexo de hasta
    10^5 vértices y hasta 10^5 consultas de puntos; «¿cuántos de estos
    puntos quedan dentro de la cerca?».

FUNCIÓN
    preparar(poli) -> list
        Deja el convexo en sentido antihorario, sin vértices colineales
        consecutivos (lo que exige la búsqueda). Si se tiene una nube de
        puntos, pasar su envolvente convexa.
    punto_en_convexo(P, p) -> int
        1 si p está estrictamente dentro, 0 en el borde, −1 fuera.
        P = preparar(...): antihorario, estrictamente convexo, >= 1 vértice.

IDEA Y ALGORITMO
    Desde el vértice P[0], las diagonales P[0]→P[1], P[0]→P[2], …,
    P[0]→P[n−1] parten el polígono en un ABANICO de triángulos, y las
    direcciones de esas diagonales están ordenadas por ángulo (porque el
    polígono es convexo y antihorario).

                  P3 ________ P2
                   /\       ,'|          p cae en el sector entre las
                  /  \    ,'  |          diagonales P0→P1 y P0→P2:
              P4 /    \ ,' p  |          basta ver de qué lado de la
                 \     ,'     |          arista P1→P2 está.
                  \  ,'  ____/ P1
                   P0 ---

    1) Si p está a la derecha de P0→P1 o a la izquierda de P0→P(n−1), está
       fuera del ángulo del abanico: FUERA.
    2) Búsqueda binaria del mayor i en [1, n−2] con cruz(P0, Pi, p) >= 0: p
       está en el sector del triángulo (P0, Pi, Pi+1). La condición «p está
       a la izquierda (o sobre) P0→Pi» es monótona en i (verdadera y luego
       falsa) porque las diagonales giran en un solo sentido.
    3) Dentro de ese sector, p está dentro del polígono si y solo si está a
       la izquierda de la arista Pi→Pi+1 (cruz > 0); sobre ella (= 0) es
       borde; a la derecha, fuera.
    4) Caso borde extra: si p está sobre la primera o la última diagonal
       (que son lados del polígono: P0P1 y P0Pn−1), es borde.
    Todo con productos cruz enteros: exacto.

MACROALGORITMO
    1. (Una vez) preparar: envolvente antihoraria sin colineales.
    2. n == 1 o 2: comparar con el punto / el segmento.
    3. Si cruz(P0, P1, p) < 0 o cruz(P0, Pn−1, p) > 0: FUERA.
    4. Búsqueda binaria: lo = 1, hi = n − 1; mientras hi − lo > 1:
       m = (lo + hi)//2; si cruz(P0, Pm, p) >= 0: lo = m, si no: hi = m.
    5. c = cruz(P_lo, P_lo+1, p): c < 0 FUERA, c == 0 BORDE.
    6. Si lo == 1 y cruz(P0, P1, p) == 0, o lo == n−2 y cruz(P0, Pn−1, p) == 0:
       BORDE (está sobre un lado que sale de P0).
    7. Si no, DENTRO.

COMPLEJIDAD
    Preparar: O(n log n) (una vez). Consulta: O(log n). Memoria O(n).
    En Python, ~10^5 consultas sobre un convexo de 10^5 vértices en ~1 s.

EJEMPLO A MANO
    P = (0,0) (4,0) (6,3) (3,6) (0,4) (antihorario), p = (4, 3):
      cruz(P0, P1, p) = 4·3 − 0·4 = 12 >= 0, cruz(P0, P4, p) = 0·3 − 4·4 =
      −16 <= 0 -> dentro del ángulo.
      lo=1, hi=4: m=2: cruz(P0,(6,3),(4,3)) = 6·3 − 3·4 = 6 >= 0 -> lo=2;
      m=3: cruz(P0,(3,6),(4,3)) = 3·3 − 6·4 = −15 < 0 -> hi=3.
      Sector (P0, P2, P3); arista (6,3)→(3,6): cruz = (−3)(0) − (3)(−2) = 6 > 0
      -> DENTRO.
    p = (5, 5): mismo sector, cruz((6,3),(3,6),(5,5)) = (−3)(2) − (3)(−1) =
      −3 < 0 -> FUERA.

ERRORES TÍPICOS
    - Polígono en sentido horario o con vértices colineales consecutivos:
      la búsqueda deja de ser monótona o el sector queda mal. Preparar antes.
    - Olvidar el caso en que p está sobre los lados P0P1 o P0Pn−1 (salen
      como «dentro» si solo se mira la arista del sector).
    - Usar >= y > al revés en la búsqueda binaria (sector equivocado cuando
      p está justo sobre una diagonal: ambos sectores son válidos, pero hay
      que ser consistente).
    - Polígonos con 1 o 2 vértices (envolventes degeneradas).

VARIANTES Y RELACIONADOS
    - Polígonos NO convexos: O(n) por consulta (punto_en_poligono.py).
    - Con muchas consultas offline también sirve ordenar los puntos por
      ángulo y barrer.
    - El mismo «abanico + búsqueda binaria» decide si un segmento desde un
      vértice toca un objeto (Colombia 2025 G) o qué arista ve un punto
      exterior (tangentes a un convexo en O(log n)).
    - Envolvente (envolvente_convexa.py), búsqueda binaria
      (00_Base/busqueda_binaria.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/G - Guard Deployment (envolvente + búsqueda
      binaria angular en el abanico de cada torre)
    - Codeforces 166B «Polygons» (cada vértice de B estrictamente dentro
      del convexo A, con n hasta 10^5 y m hasta 2·10^4)

VERIFICACIÓN
    - Pruebas: OK en 800 convexos aleatorios (envolventes de puntos al azar,
      también de 1 y 2 vértices y casi circulares grandes) con todas las
      consultas enteras de su caja ampliada (~210000 consultas) contra la
      fuerza bruta O(n): signo de cruz con cada arista
      (python punto_en_convexo_logn.py)
"""
import math
import random


def cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def preparar(poli):
    """Envolvente antihoraria sin colineales (Andrew). Sirve para nubes de
    puntos y para polígonos convexos en cualquier sentido."""
    pts = sorted(set(poli))
    if len(pts) <= 1:
        return pts
    inf, sup = [], []
    for p in pts:
        while len(inf) >= 2 and cruz(inf[-2], inf[-1], p) <= 0:
            inf.pop()
        inf.append(p)
    for p in reversed(pts):
        while len(sup) >= 2 and cruz(sup[-2], sup[-1], p) <= 0:
            sup.pop()
        sup.append(p)
    return inf[:-1] + sup[:-1]


def punto_en_convexo(P, p):
    """1 dentro, 0 borde, −1 fuera. P antihorario y estrictamente convexo."""
    n = len(P)
    if n == 1:
        return 0 if p == P[0] else -1
    if n == 2:
        a, b = P
        en = cruz(a, b, p) == 0 and \
            (a[0] - p[0]) * (b[0] - p[0]) + (a[1] - p[1]) * (b[1] - p[1]) <= 0
        return 0 if en else -1
    a = P[0]
    c1, c2 = cruz(a, P[1], p), cruz(a, P[n - 1], p)
    if c1 < 0 or c2 > 0:
        return -1                       # fuera del ángulo del abanico
    # Mayor lo en [1, n−2] con p a la izquierda (o sobre) de P0→P[lo].
    lo, hi = 1, n - 1
    while hi - lo > 1:
        m = (lo + hi) // 2
        if cruz(a, P[m], p) >= 0:
            lo = m
        else:
            hi = m
    c = cruz(P[lo], P[lo + 1], p)       # lado respecto a la arista del sector
    if c < 0:
        return -1
    if c == 0:
        return 0
    if (lo == 1 and c1 == 0) or (lo == n - 2 and c2 == 0):
        return 0                        # sobre los lados P0P1 o P0P(n−1)
    return 1


def demo():
    P = preparar([(0, 0), (4, 0), (6, 3), (3, 6), (0, 4)])
    print("convexo:", P)
    nombres = {1: "dentro", 0: "borde", -1: "fuera"}
    for p in [(4, 3), (5, 5), (2, 0), (0, 2), (0, 0), (-1, 1), (3, 3)]:
        print(p, "->", nombres[punto_en_convexo(P, p)])


def _bruto(P, p):
    n = len(P)
    if n == 1:
        return 0 if p == P[0] else -1
    if n == 2:
        a, b = P
        if cruz(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) \
                and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]):
            return 0
        return -1
    s = [cruz(P[i], P[(i + 1) % n], p) for i in range(n)]
    if any(v < 0 for v in s):
        return -1
    return 0 if any(v == 0 for v in s) else 1


def pruebas():
    random.seed(2025)

    # Casos borde
    T = preparar([(0, 0), (3, 0), (0, 3)])
    assert punto_en_convexo(T, (0, 0)) == 0 and punto_en_convexo(T, (1, 1)) == 1
    assert punto_en_convexo(T, (0, 2)) == 0 and punto_en_convexo(T, (2, 0)) == 0
    assert punto_en_convexo(T, (0, 4)) == -1 and punto_en_convexo(T, (-1, 0)) == -1
    assert punto_en_convexo(preparar([(2, 2)]), (2, 2)) == 0
    S = preparar([(0, 0), (4, 4), (2, 2)])
    assert S == [(0, 0), (4, 4)]
    assert punto_en_convexo(S, (3, 3)) == 0 and punto_en_convexo(S, (5, 5)) == -1
    # sentido horario y colineales en la entrada: preparar los arregla
    H = preparar([(0, 0), (0, 4), (0, 2), (4, 4), (4, 0), (2, 0)])
    assert H == [(0, 0), (4, 0), (4, 4), (0, 4)] and punto_en_convexo(H, (2, 0)) == 0

    consultas = 0
    for caso in range(800):
        if caso % 4 == 3:
            # casi circular: muchos vértices
            R, n = random.randint(8, 15), random.randint(5, 40)
            nube = [(round(R * math.cos(2 * math.pi * t / n)), round(R * math.sin(2 * math.pi * t / n)))
                    for t in range(n)]
        else:
            r = random.choice([1, 2, 4, 6])
            nube = [(random.randint(-r, r), random.randint(-r, r))
                    for _ in range(random.randint(1, 10))]
        P = preparar(nube)
        xs, ys = [q[0] for q in P], [q[1] for q in P]
        for x in range(min(xs) - 2, max(xs) + 3):
            for y in range(min(ys) - 2, max(ys) + 3):
                assert punto_en_convexo(P, (x, y)) == _bruto(P, (x, y)), (P, (x, y))
                consultas += 1
    assert consultas > 200000


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
