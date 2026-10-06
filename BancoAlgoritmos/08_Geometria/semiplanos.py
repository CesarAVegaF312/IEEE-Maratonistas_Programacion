r"""
Geometría — Intersección de semiplanos y recorte de convexos («half-plane intersection»)
Nivel: Avanzado
Ejecutar: python semiplanos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Hallar la región (convexa) de puntos que cumplen a la vez muchas
    restricciones lineales del tipo «estar a la izquierda de la recta a→b».
    Dos herramientas:
    - cortar: recortar un polígono convexo con UNA recta en O(n)
      (Sutherland–Hodgman). Aplicada k veces da la intersección en O(k·n),
      y también sirve para partir regiones con cuerdas (celdas).
    - interseccion_semiplanos: las n restricciones de golpe en O(n log n)
      (ordenar por ángulo + deque).
    Y una aplicación: el centro de Chebyshev (punto más «profundo» de la
    región: centro del mayor círculo inscrito).
    Señales en el enunciado: «región visible desde todos los lados», «zona
    segura entre láseres/rectas», «núcleo (kernel) de un polígono», «punto
    más alejado de todas las paredes», restricciones a·x + b·y <= c.

FUNCIÓN
    Un semiplano es un par de puntos (a, b): la recta orientada a→b y su
    lado IZQUIERDO, cerrado: {p : cruz(a, b, p) >= 0}.
    cortar(poli, a, b) -> list
        Parte del convexo poli (antihorario) a la izquierda de a→b, también
        antihoraria. [] si no queda nada. Con coordenadas Fraction es
        EXACTO; con int/float devuelve floats.
    interseccion_semiplanos(semiplanos) -> list[(Fraction, Fraction)]
        Vértices (antihorario) de la intersección, que debe estar ACOTADA
        (agregar los 4 lados de una caja grande si hace falta). [] si la
        intersección es vacía o de área 0 (punto o segmento). Puntos a, b
        enteros.
    centro_chebyshev(semiplanos, iteraciones=60) -> ((float, float), float)
        Centro y radio del mayor círculo dentro de la región (búsqueda
        binaria sobre el radio + cortes). Floats.

IDEA Y ALGORITMO
    CORTAR (O(n)): recorrer las aristas (p, q) del convexo; si p está del
    lado bueno se conserva; si p y q están en lados opuestos, se agrega el
    punto donde la arista cruza la recta: con cp = cruz(a, b, p) y
    cq = cruz(a, b, q), ese punto es p + (q − p)·cp/(cp − cq) (las cruces
    son distancias con signo escaladas, interpolación lineal).

           p ●───────●            recta a→b  ═══════>
             │  bueno │    ->     se conserva arriba (izquierda);
         ════●═══════●═══>        los cruces de las aristas con la
             │  malo  │           recta son vértices nuevos.
             ●───────● q

    INTERSECCIÓN EN O(n log n):
    1) Ordenar los semiplanos por el ángulo de su dirección b − a (exacto:
       por semiplano superior/inferior y luego por cruz). Entre paralelos
       de igual dirección, quedarse con el más restrictivo.
    2) Recorrerlos manteniendo en una DEQUE los semiplanos que forman el
       borde actual; los vértices son las intersecciones de vecinos.
       Al llegar uno nuevo H: mientras el último vértice (intersección de
       los dos últimos de la deque) quede FUERA de H, sacar el último;
       igual por el frente. Luego agregar H. Por qué: si el vértice queda
       fuera, el último semiplano ya no aporta borde (H lo «tapa» desde
       ese ángulo en adelante); y como las direcciones van girando, lo
       mismo puede pasar en el otro extremo del ciclo.
    3) Al final, limpiar el frente contra el fondo y viceversa (el ciclo se
       cierra). Si quedan < 3, la región es vacía o degenerada.
    Exactitud: las intersecciones se calculan con Fraction a partir de
    puntos enteros, y «fuera» es cruz < 0 exacto. Sin epsilon. (Con floats
    es más rápido: usar cruz < −eps como «fuera».)

    CENTRO DE CHEBYSHEV (idea): el mayor círculo de radio r con centro c
    cabe si c está a distancia >= r de cada recta, es decir, si c está en
    cada semiplano DESPLAZADO hacia adentro r unidades. «¿Cabe radio r?» es
    monótono en r -> búsqueda binaria sobre r, cortando una caja con los
    semiplanos desplazados y preguntando si queda algo. (Exacto: es un
    programa lineal en (x, y, r) cuyo óptimo está donde 3 restricciones
    son iguales: probar ternas; así lo resuelve Colombia 2026 F.)

MACROALGORITMO
    Cortar: para i: p = P[i], q = P[i+1]; si cruz(a,b,p) >= 0 agregar p;
      si cp·cq < 0 agregar el punto de cruce.
    Intersección:
    1. Ordenar por ángulo; deque vacía.
    2. Para cada H: sacar del fondo mientras el vértice del fondo esté fuera
       de H; sacar del frente mientras el vértice del frente esté fuera.
    3. Si H es paralelo al último: opuesto -> vacío; igual dirección ->
       dejar el más restrictivo. Si no, agregar H.
    4. Limpiar fondo contra frente y frente contra fondo.
    5. Vértices = intersecciones de vecinos consecutivos (cíclico).

COMPLEJIDAD
    cortar: O(n). Intersección: O(n log n) por el orden + O(n) la deque.
    Con Fraction cada operación es ~20 veces más cara: ~10^4 semiplanos en
    ~1 s; con floats ~10^5. Chebyshev: O(iteraciones · n²) con cortes
    sucesivos (n = número de semiplanos).

EJEMPLO A MANO
    Caja [0, 4] × [0, 4] como 4 semiplanos y además «x + y <= 6»
    (recta de (6,0) a (0,6), izquierda = abajo):
      se recorta la esquina (4,4): región (0,0) (4,0) (4,2) (2,4) (0,4),
      área 16 − 2 = 14.
    Cortar el cuadrado (0,0) (4,0) (4,4) (0,4) con la recta (0,1)→(4,3)
    (queda la parte de arriba): (4,3) (4,4) (0,4) (0,1).
    Chebyshev del triángulo (0,0) (4,0) (0,3): r = 2A/P = 12/12 = 1, centro (1, 1).

ERRORES TÍPICOS
    - Semiplanos con orientación mezclada (unos a la izquierda, otros a la
      derecha): fijar la convención y orientar todo así.
    - Región no acotada sin caja: la deque devuelve basura; agregar una caja.
    - Ordenar por atan2 con floats y tratar como distintos dos ángulos
      iguales (o al revés): comparar exacto con cruz.
    - Olvidar el paso final de limpieza (frente contra fondo).
    - En cortar, agregar el punto de cruce cuando p o q está exactamente
      sobre la recta (cp·cq = 0): duplica vértices; usar cp·cq < 0.

VARIANTES Y RELACIONADOS
    - Núcleo (kernel) de un polígono: intersección de los semiplanos de sus
      lados (el polígono es «estrellado» si el núcleo no es vacío).
    - Celdas de un arreglo de rectas: partir cada celda con cortar (las dos
      mitades: cortar con (a, b) y con (b, a)).
    - Diagrama de Voronoi de un punto: intersección de las mediatrices.
    - Programación lineal en 2D (Megiddo / Seidel aleatorizado, O(n)).
    - Distancias con signo a rectas (proyeccion_distancias.py), área
      (area_poligono.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/F - Heist (celdas convexas recortando con cada
      láser + centro de Chebyshev de cada celda)

VERIFICACIÓN
    - Pruebas: cortar OK en ~400 convexos aleatorios exactos (Fraction):
      área(izquierda) + área(derecha) = área total, y para una malla de
      puntos enteros, «está en el corte» == «está en el polígono y a la
      izquierda de la recta». interseccion_semiplanos OK en 400 conjuntos
      aleatorios de hasta 7 semiplanos (+ caja, en orden aleatorio, con
      paralelos y repetidos) contra cortes sucesivos de la caja (misma área
      exacta y misma pertenencia de los puntos de una malla).
      Chebyshev contra el inradio 2A/P de ~100 triángulos y contra 50
      rectángulos (python semiplanos.py)
"""
import math
import random
from collections import deque
from fractions import Fraction
from functools import cmp_to_key


def cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def cortar(poli, a, b):
    """Parte del convexo poli a la izquierda (cerrada) de la recta a→b."""
    res = []
    n = len(poli)
    for i in range(n):
        p, q = poli[i], poli[(i + 1) % n]
        cp, cq = cruz(a, b, p), cruz(a, b, q)
        if cp >= 0:
            res.append(p)
        if cp * cq < 0:                     # la arista cruza la recta
            t = cp / (cp - cq)
            res.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return res


def _interseccion(h1, h2):
    """Corte de las rectas de dos semiplanos (no paralelos), con Fraction."""
    (a, b), (c, d) = h1, h2
    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = d[0] - c[0], d[1] - c[1]
    t = Fraction((c[0] - a[0]) * sy - (c[1] - a[1]) * sx, rx * sy - ry * sx)
    return (a[0] + t * rx, a[1] + t * ry)


def _fuera(h, p):
    """¿p está estrictamente a la derecha de h (fuera del semiplano)?"""
    return cruz(h[0], h[1], p) < 0


def _comparar_angulo(h1, h2):
    """Orden exacto por el ángulo de la dirección en [0, 2π)."""
    d1 = (h1[1][0] - h1[0][0], h1[1][1] - h1[0][1])
    d2 = (h2[1][0] - h2[0][0], h2[1][1] - h2[0][1])
    s1 = 0 if (d1[1] > 0 or (d1[1] == 0 and d1[0] > 0)) else 1   # mitad superior
    s2 = 0 if (d2[1] > 0 or (d2[1] == 0 and d2[0] > 0)) else 1
    if s1 != s2:
        return s1 - s2
    c = d1[0] * d2[1] - d1[1] * d2[0]
    return -1 if c > 0 else (1 if c < 0 else 0)


def interseccion_semiplanos(semiplanos):
    """Vértices de la intersección (acotada) de semiplanos; [] si área 0."""
    H = sorted(semiplanos, key=cmp_to_key(_comparar_angulo))
    dq = deque()
    for h in H:
        while len(dq) >= 2 and _fuera(h, _interseccion(dq[-1], dq[-2])):
            dq.pop()
        while len(dq) >= 2 and _fuera(h, _interseccion(dq[0], dq[1])):
            dq.popleft()
        if dq:
            u = dq[-1]
            du = (u[1][0] - u[0][0], u[1][1] - u[0][1])
            dh = (h[1][0] - h[0][0], h[1][1] - h[0][1])
            if du[0] * dh[1] - du[1] * dh[0] == 0:          # paralelos
                if du[0] * dh[0] + du[1] * dh[1] < 0:
                    return []                               # opuestos: vacío/degenerado
                if _fuera(h, u[0]):                         # h es más restrictivo
                    dq.pop()
                else:
                    continue
        dq.append(h)
    # Cerrar el ciclo: el fondo contra el frente y viceversa.
    while len(dq) >= 3 and _fuera(dq[0], _interseccion(dq[-1], dq[-2])):
        dq.pop()
    while len(dq) >= 3 and _fuera(dq[-1], _interseccion(dq[0], dq[1])):
        dq.popleft()
    if len(dq) < 3:
        return []
    dq = list(dq)
    verts = [_interseccion(dq[i], dq[(i + 1) % len(dq)]) for i in range(len(dq))]
    # Quitar vértices repetidos (varias rectas por el mismo punto)
    limpio = []
    for v in verts:
        if not limpio or limpio[-1] != v:
            limpio.append(v)
    while len(limpio) > 1 and limpio[0] == limpio[-1]:
        limpio.pop()
    if len(limpio) < 3 or _area2(limpio) == 0:
        return []
    return limpio


def _area2(poli):
    n = len(poli)
    return sum(poli[i][0] * poli[(i + 1) % n][1] - poli[(i + 1) % n][0] * poli[i][1]
               for i in range(n))


def centro_chebyshev(semiplanos, iteraciones=60):
    """((cx, cy), r): mayor círculo dentro de la región (acotada), en floats."""
    m = max(max(abs(c) for h in semiplanos for p in h for c in p), 1) * 4
    caja = [(-m, -m), (m, -m), (m, m), (-m, m)]

    def region(r):
        poli = [(float(x), float(y)) for x, y in caja]
        for a, b in semiplanos:
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy)
            nx, ny = -dy / L * r, dx / L * r        # normal hacia la izquierda
            poli = cortar(poli, (a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny))
            if not poli:
                return []
        return poli

    lo, hi = 0.0, float(2 * m)
    for _ in range(iteraciones):                    # «¿cabe radio r?» es monótono
        mid = (lo + hi) / 2
        if region(mid):
            lo = mid
        else:
            hi = mid
    poli = region(lo) or region(0.0)
    cx = sum(p[0] for p in poli) / len(poli)
    cy = sum(p[1] for p in poli) / len(poli)
    return (cx, cy), lo


def caja(x1, y1, x2, y2):
    """Los 4 semiplanos (antihorarios) de la caja [x1, x2] × [y1, y2]."""
    return [((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)),
            ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))]


def demo():
    sp = caja(0, 0, 4, 4) + [((6, 0), (0, 6))]
    R = interseccion_semiplanos(sp)
    print("caja 4x4 ∩ {x + y <= 6}:", [(str(x), str(y)) for x, y in R],
          " área =", _area2(R) / 2)                                  # 14
    C = cortar([(0, 0), (4, 0), (4, 4), (0, 4)], (0, 1), (4, 3))
    print("cuadrado cortado por (0,1)->(4,3):", C)
    tri = [((0, 0), (4, 0)), ((4, 0), (0, 3)), ((0, 3), (0, 0))]
    (cx, cy), r = centro_chebyshev(tri)
    print("Chebyshev del triángulo (0,0)(4,0)(0,3): centro (%.4f, %.4f), r = %.4f"
          % (cx, cy, r))                                              # (1, 1), 1


# ---------------------------------------------------------------- pruebas
def _envolvente(puntos):
    pts = sorted(set(puntos))
    if len(pts) <= 2:
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


def _dentro_convexo(P, p):
    """p en el convexo cerrado P (antihorario, quizá con colineales)."""
    if len(P) < 3 or _area2(P) == 0:
        return False
    return all(cruz(P[i], P[(i + 1) % len(P)], p) >= 0 for i in range(len(P)))


def pruebas():
    random.seed(2026)

    # Casos borde
    cuad = [(0, 0), (4, 0), (4, 4), (0, 4)]
    assert cortar(cuad, (0, 5), (4, 5)) == []                         # todo fuera
    assert cortar(cuad, (0, -1), (4, -1)) == cuad                     # todo dentro
    assert cortar(cuad, (0, 0), (4, 0)) == cuad                       # recta sobre un lado
    assert interseccion_semiplanos(caja(0, 0, 4, 4) + [((-5, 4), (5, 4))]) == []   # segmento
    assert interseccion_semiplanos(caja(0, 0, 4, 4) + [((0, 5), (4, 5))]) == []    # vacío
    assert _area2(interseccion_semiplanos(caja(0, 0, 4, 4) * 2)) == 32             # repetidos

    for _ in range(400):
        # --- cortar, exacto con Fraction
        nube = [(random.randint(-5, 5), random.randint(-5, 5)) for _ in range(random.randint(3, 9))]
        P = _envolvente(nube)
        if len(P) < 3:
            continue
        P = [(Fraction(x), Fraction(y)) for x, y in P]
        a = (random.randint(-6, 6), random.randint(-6, 6))
        b = (random.randint(-6, 6), random.randint(-6, 6))
        if a == b:
            continue
        izq, der = cortar(P, a, b), cortar(P, b, a)
        assert abs(_area2(izq)) + abs(_area2(der)) == _area2(P)
        assert all(cruz(a, b, v) >= 0 for v in izq)
        for x in range(-6, 7, 2):
            for y in range(-6, 7, 2):
                q = (x, y)
                assert _dentro_convexo(izq, q) == (_dentro_convexo(P, q) and cruz(a, b, q) >= 0) \
                    or _area2(izq) == 0

    for _ in range(400):
        # --- intersección de semiplanos contra cortes sucesivos de la caja
        sp = caja(-8, -8, 8, 8)
        for _ in range(random.randint(0, 7)):
            a = (random.randint(-5, 5), random.randint(-5, 5))
            b = (random.randint(-5, 5), random.randint(-5, 5))
            if a != b:
                sp.append((a, b))
        random.shuffle(sp)
        R = interseccion_semiplanos(sp)
        poli = [(Fraction(-8), Fraction(-8)), (Fraction(8), Fraction(-8)),
                (Fraction(8), Fraction(8)), (Fraction(-8), Fraction(8))]
        for a, b in sp:
            poli = cortar(poli, a, b)
        area_bruta = abs(_area2(poli)) if len(poli) >= 3 else 0
        assert _area2(R) == area_bruta, (sp, R, poli)
        for v in R:
            assert all(cruz(a, b, v) >= 0 for a, b in sp)
        if R:
            for x in range(-8, 9, 4):
                for y in range(-8, 9, 4):
                    assert _dentro_convexo(R, (x, y)) == _dentro_convexo(poli, (x, y))

    # --- Chebyshev: inradio de triángulos = 2A / perímetro
    for _ in range(200):
        t = [(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(3)]
        A2 = _area2(t)
        if A2 == 0:
            continue
        if A2 < 0:
            t = t[::-1]
            A2 = -A2
        per = sum(math.dist(t[i], t[(i + 1) % 3]) for i in range(3))
        (cx, cy), r = centro_chebyshev([(t[i], t[(i + 1) % 3]) for i in range(3)])
        assert abs(r - A2 / per) < 1e-6
        # el centro está a distancia r de los tres lados
        for i in range(3):
            a, b = t[i], t[(i + 1) % 3]
            d = cruz(a, b, (cx, cy)) / math.dist(a, b)
            assert d > r - 1e-5
    for _ in range(50):
        w, h = random.randint(1, 20), random.randint(1, 20)
        (cx, cy), r = centro_chebyshev(caja(0, 0, w, h))
        assert abs(r - min(w, h) / 2) < 1e-6


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
