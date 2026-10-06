r"""
Geometría — Capas convexas: «pelar la cebolla» («convex layers / onion peeling»)
Nivel: Avanzado
Ejecutar: python capas_convexas.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Partir un conjunto de puntos en capas: la capa 1 es el borde de la
    envolvente convexa; se quitan esos puntos y la capa 2 es el borde de la
    envolvente de los que quedan; y así hasta vaciar. La capa de un punto
    mide su «profundidad» dentro de la nube.
    Señales en el enunciado: «capas», «cebolla», «se quitan los puntos del
    borde y se repite», «nivel de profundidad», «anillos convexos anidados»,
    estadística robusta (profundidad de Tukey aproximada), dibujar
    «cebollas» de puntos.

FUNCIÓN
    capas_convexas(puntos, colineales=True) -> list[list[(x, y)]]
        Lista de capas, de afuera hacia adentro; cada capa en sentido
        antihorario. Los puntos repetidos se toman una sola vez.
        colineales=True : la capa incluye TODOS los puntos del borde (los que
                          están en medio de un lado también). Es lo usual.
        colineales=False: solo las esquinas; los puntos en medio de un lado
                          pasan a capas interiores.
    profundidad(puntos, colineales=True) -> dict {punto: número de capa (1..)}

IDEA Y ALGORITMO
    Aplicar la envolvente convexa (cadena monótona de Andrew) repetidamente.

          · · · · · ·  capa 1    Ejemplo: 3 cuadrados anidados
          · ┌─────┐ ·            (y un punto en el centro):
          · │ ┌─┐ │ ·            capa 1 = cuadrado grande,
          · │ │·│ │ ·            capa 2 = cuadrado mediano,
          · │ └─┘ │ ·            capa 3 = cuadrado chico,
          · └─────┘ ·            capa 4 = el centro.
          · · · · · ·

    Detalles que deciden si la respuesta es correcta:
    1) Con colineales=True, en la cadena solo se saca un punto cuando el
       giro es ESTRICTAMENTE a la derecha (cruz < 0); con cruz = 0 el punto
       está sobre un lado y pertenece a la capa.
    2) Si los puntos que quedan son todos colineales, el «polígono» es un
       segmento y TODOS están en su borde: la capa es entera (la cadena
       inferior ya los contiene todos; no duplicarlos con la superior).
    3) Basta ordenar una sola vez por (x, y): al quitar puntos de una lista
       ordenada, el resto sigue ordenado. Cada capa cuesta O(m) con m =
       puntos restantes.
    Por qué es correcto: cada capa es, por definición, el borde de la
    envolvente de los puntos que quedan; la cadena monótona calcula
    exactamente ese borde (con o sin puntos colineales según la regla de
    sacar). Todo con productos cruz enteros: exacto.

MACROALGORITMO
    1. Quitar duplicados y ordenar por (x, y).
    2. Mientras queden puntos:
    3.   Calcular el borde de la envolvente de los restantes (cadena monótona,
         con la regla de colineales elegida; si todos son colineales, son
         todos).
    4.   Guardarlo como capa nueva.
    5.   Quitar esos puntos de la lista (filtrando, sin reordenar).

COMPLEJIDAD
    O(n log n + n·K), con K el número de capas (K <= n/3 + 1, así que el peor
    caso es O(n²)). Existe un algoritmo O(n log n) (Chazelle 1985) pero es
    complicado; en maratón se usa este. En Python, n = 3000 en el peor caso
    (1000 triángulos anidados) tarda ~1.5 s. Memoria O(n).

EJEMPLO A MANO
    Puntos: (0,0) (6,0) (6,6) (0,6) (3,0)  (1,1) (5,1) (3,5)  (3,2) (3,3).
    Capa 1 (con colineales): (0,0) (3,0) (6,0) (6,6) (0,6)   [(3,0) va en
      medio de un lado].
    Restan (1,1) (5,1) (3,5) (3,2) (3,3): capa 2 = (1,1) (5,1) (3,5).
    Restan (3,2) (3,3): colineales -> capa 3 = (3,2) (3,3).
    Con colineales=False, (3,0) NO está en la capa 1: queda en la capa 2,
    que pasa a ser (1,1) (3,0) (5,1) (3,5) [(3,0) es esquina de esa capa].

ERRORES TÍPICOS
    - Usar la envolvente que descarta colineales cuando el enunciado dice
      que los puntos «sobre el borde» también son de la capa (o al revés).
    - Duplicar puntos cuando la capa degenera en un segmento (cadena
      inferior + superior recorren los mismos puntos).
    - Reordenar en cada capa (O(n log n) por capa: más lento sin necesidad).
    - Puntos repetidos: decidir explícitamente qué hacer con ellos.

VARIANTES Y RELACIONADOS
    - DP por capas: con las capas como niveles, «saltar de una capa a la
      siguiente» es un DAG por niveles (Colombia 2026 C).
    - Envolvente convexa (envolvente_convexa.py).
    - Profundidad de Tukey / «halfspace depth» (otra noción de profundidad).
    - Capas de Pareto (maxima layers): misma idea con dominancia en vez de
      convexidad, se calcula con LIS / ordenamiento.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/C - Into the Onion (capas con colineales + DP por
      capas)

VERIFICACIÓN
    - Pruebas: OK en 1500 nubes aleatorias pequeñas (muchos colineales y
      duplicados) contra fuerza bruta capa por capa: con colineales, p está
      en el borde si existe otro punto q con todos los restantes en un mismo
      lado cerrado de la recta pq (o es el único); sin colineales, p es
      esquina si no está en ningún triángulo/segmento cerrado de otros
      restantes. Además: capas en sentido antihorario y convexas, y un caso
      de 300 triángulos anidados (python capas_convexas.py)
"""
import random


def cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _borde(pts, colineales):
    """Borde de la envolvente de pts YA ORDENADOS y sin repetidos."""
    if len(pts) <= 2:
        return list(pts)
    lim = -1 if colineales else 0           # sacar si cruz <= lim

    def cadena(secuencia):
        pila = []
        for p in secuencia:
            while len(pila) >= 2 and cruz(pila[-2], pila[-1], p) <= lim:
                pila.pop()
            pila.append(p)
        return pila

    inferior = cadena(pts)
    if colineales and len(inferior) == len(pts) and \
            all(cruz(pts[0], pts[-1], p) == 0 for p in pts):
        return list(pts)                    # todos colineales: un segmento
    superior = cadena(reversed(pts))
    return inferior[:-1] + superior[:-1]


def capas_convexas(puntos, colineales=True):
    """Capas convexas de afuera hacia adentro (cada una antihoraria)."""
    pts = sorted(set(puntos))               # se ordena UNA sola vez
    capas = []
    while pts:
        capa = _borde(pts, colineales)
        capas.append(capa)
        quitar = set(capa)
        pts = [p for p in pts if p not in quitar]   # sigue ordenado
    return capas


def profundidad(puntos, colineales=True):
    """{punto: capa (1 = la de afuera)}."""
    return {p: i + 1 for i, capa in enumerate(capas_convexas(puntos, colineales)) for p in capa}


def demo():
    pts = [(0, 0), (6, 0), (6, 6), (0, 6), (3, 0), (1, 1), (5, 1), (3, 5), (3, 2), (3, 3)]
    print("puntos:", pts)
    for i, capa in enumerate(capas_convexas(pts), 1):
        print("  capa", i, ":", capa)
    print("sin colineales:")
    for i, capa in enumerate(capas_convexas(pts, colineales=False), 1):
        print("  capa", i, ":", capa)
    print("profundidad de (3,3):", profundidad(pts)[(3, 3)])


def _en_triangulo_cerrado(p, a, b, c):
    if cruz(a, b, c) == 0:
        for u, v in ((a, b), (b, c), (a, c)):
            if cruz(u, v, p) == 0 and min(u[0], v[0]) <= p[0] <= max(u[0], v[0]) \
                    and min(u[1], v[1]) <= p[1] <= max(u[1], v[1]):
                return True
        return False
    s1, s2, s3 = cruz(a, b, p), cruz(b, c, p), cruz(c, a, p)
    return (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)


def _capas_bruto(puntos, colineales):
    resto = set(puntos)
    capas = []
    while resto:
        u = sorted(resto)
        if colineales:
            capa = set()
            for p in u:
                if len(u) == 1:
                    capa.add(p)
                for q in u:
                    if q == p:
                        continue
                    s = [cruz(p, q, w) for w in u]
                    if all(v >= 0 for v in s) or all(v <= 0 for v in s):
                        capa.add(p)
                        break
        else:
            capa = set()
            for p in u:
                o = [q for q in u if q != p]
                if not any(_en_triangulo_cerrado(p, o[i], o[j], o[k])
                           for i in range(len(o)) for j in range(i, len(o))
                           for k in range(j, len(o))):
                    capa.add(p)
        capas.append(capa)
        resto -= capa
    return capas


def pruebas():
    random.seed(2026)

    # Casos borde
    assert capas_convexas([]) == []
    assert capas_convexas([(1, 1), (1, 1)]) == [[(1, 1)]]
    assert capas_convexas([(0, 0), (2, 2), (1, 1), (3, 3)]) == [[(0, 0), (1, 1), (2, 2), (3, 3)]]
    assert capas_convexas([(0, 0), (2, 2), (1, 1)], colineales=False) == [[(0, 0), (2, 2)], [(1, 1)]]
    rejilla = [(x, y) for x in range(5) for y in range(5)]
    assert [len(c) for c in capas_convexas(rejilla)] == [16, 8, 1]

    for _ in range(1500):
        r = random.choice([1, 2, 3, 4])
        pts = [(random.randint(-r, r), random.randint(-r, r)) for _ in range(random.randint(1, 10))]
        for col in (True, False):
            capas = capas_convexas(pts, col)
            bruto = _capas_bruto(pts, col)
            assert [set(c) for c in capas] == bruto
            assert sum(len(c) for c in capas) == len(set(pts))
            for c in capas:                 # antihorario y convexa (sin retrocesos)
                m = len(c)
                if m >= 3 and any(cruz(c[0], c[1], q) != 0 for q in c):
                    assert all(cruz(c[i], c[(i + 1) % m], c[(i + 2) % m]) >= 0 for i in range(m))
                    if not col:
                        assert all(cruz(c[i], c[(i + 1) % m], c[(i + 2) % m]) > 0
                                   for i in range(m))

    # Triángulos anidados: 300 capas de 3 puntos (peor caso de número de capas)
    anidados = []
    for k in range(1, 301):
        anidados += [(-2 * k, -k), (2 * k, -k), (0, 2 * k)]
    capas = capas_convexas(anidados)
    assert len(capas) == 300 and all(len(c) == 3 for c in capas)
    assert set(capas[0]) == {(-600, -300), (600, -300), (0, 600)}


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
