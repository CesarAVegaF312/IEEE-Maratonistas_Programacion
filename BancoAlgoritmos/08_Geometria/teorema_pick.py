r"""
Geometría — Teorema de Pick y puntos enteros en el borde («Pick's theorem»)
Nivel: Intermedio
Ejecutar: python teorema_pick.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Contar en O(n log C) cuántos puntos de coordenadas enteras hay dentro y
    sobre el borde de un polígono simple cuyos vértices son enteros, sin
    recorrerlos uno a uno (el polígono puede medir 10^9 × 10^9).
    Señales en el enunciado: «¿cuántos árboles/postes/celdas (puntos de la
    cuadrícula) quedan dentro del terreno?», «puntos de red», vértices
    enteros, coordenadas enormes (no se puede recorrer la caja).

FUNCIÓN
    puntos_en_segmento(a, b) -> int     puntos enteros en [a, b] (extremos
                                        incluidos) = gcd(|dx|, |dy|) + 1
    puntos_borde(poli) -> int           B: puntos enteros sobre el borde
    puntos_interiores(poli) -> int      I: puntos enteros estrictamente dentro
    area2(poli) -> int                  doble del área (zapato), exacto
    poli: vértices enteros en orden (CW o CCW), polígono simple, área > 0.

IDEA Y ALGORITMO
    Teorema de Pick: para un polígono simple con vértices enteros,
        A = I + B/2 − 1      ->      I = (2A − B + 2) / 2.
    2A sale exacto de la fórmula del zapato, así que I es entero exacto.
    Puntos enteros de un segmento: de a a b con (dx, dy) = b − a, y
    g = gcd(|dx|, |dy|), el paso mínimo entero es (dx/g, dy/g) (no se puede
    dividir más, porque dx/g y dy/g son coprimos). Hay g pasos, así que
    g + 1 puntos contando ambos extremos. En el polígono, cada vértice se
    compartiría entre dos lados: B = Σ gcd(|dx_i|, |dy_i|) (contando un
    extremo por lado).

        · · · · · ·        triángulo (0,0) (4,0) (0,4):
        * · · · · ·          2A = 16, B = 4 + 4 + 4 = 12
        * * · · · ·          (gcd(4,0) + gcd(4,4) + gcd(0,4))
        * o * · · ·          I = (16 − 12 + 2)/2 = 3   ( o = interiores:
        * o o * · ·                               (1,1), (2,1), (1,2) )
        * * * * * ·

    Por qué vale Pick (idea): es ADITIVO al pegar polígonos por un lado (los
    puntos del lado común pasan de borde a interior y la fórmula se
    conserva), vale para rectángulos alineados y triángulos rectángulos
    (contando directamente), y todo triángulo entero se obtiene de un
    rectángulo quitando triángulos rectángulos; todo polígono se triangula.

MACROALGORITMO
    1. 2A = |Σ (xi·yi+1 − xi+1·yi)| (fórmula del zapato).
    2. B = Σ gcd(|xi+1 − xi|, |yi+1 − yi|).
    3. I = (2A − B + 2) // 2.
    4. Total de puntos enteros en el polígono cerrado = I + B.

COMPLEJIDAD
    O(n log C) (un gcd por lado, C = tamaño de las coordenadas); memoria O(1).
    10^6 vértices en ~1 s en Python.

EJEMPLO A MANO
    Triángulo (0,0) (4,0) (0,4): 2A = 16, B = 12, I = 3, total = 15.
    Cuadrado (0,0) (3,0) (3,3) (0,3): 2A = 18, B = 12, I = (18 − 12 + 2)/2 = 4
    (los puntos (1,1) (1,2) (2,1) (2,2)).

ERRORES TÍPICOS
    - Contar g + 1 puntos por lado y sumar: cada vértice queda contado dos
      veces. Por lado se suma g (sin el extremo final).
    - gcd con negativos: usar valores absolutos (math.gcd ya lo hace en
      Python 3, pero no en todos los lenguajes).
    - Aplicarlo con vértices NO enteros o polígonos con huecos (para un
      polígono con h huecos: A = I + B/2 + h − 1).
    - Dividir el área por 2 antes de tiempo y perder exactitud: trabajar con 2A.

VARIANTES Y RELACIONADOS
    - Puntos enteros sobre un segmento: gcd + 1 (también sirve para saber si
      una recta entre dos puntos enteros pasa por otros puntos enteros).
    - Área de polígonos (area_poligono.py); punto en polígono para contar
      a fuerza bruta en cajas pequeñas (punto_en_poligono.py).
    - Contar puntos bajo una recta (floor_sum / sumas tipo «Euclides»).

DÓNDE PRACTICAR
    - CSES «Polygon Lattice Points» (exactamente este archivo)
    - UVa 10088 «Trees on My Island»

VERIFICACIÓN
    - Pruebas: OK en 1500 polígonos simples aleatorios (estrellados, no
      convexos, con lados oblicuos) contra conteo directo de todos los
      puntos enteros de la caja con punto-en-polígono (borde/dentro), y
      puntos_en_segmento contra enumeración de la caja del segmento
      (python teorema_pick.py)
"""
import math
import random


def puntos_en_segmento(a, b):
    """Puntos enteros del segmento cerrado [a, b] (a, b enteros)."""
    return math.gcd(abs(b[0] - a[0]), abs(b[1] - a[1])) + 1


def area2(poli):
    n = len(poli)
    return abs(sum(poli[i][0] * poli[(i + 1) % n][1] - poli[(i + 1) % n][0] * poli[i][1]
                   for i in range(n)))


def puntos_borde(poli):
    """B = Σ gcd(|dx|, |dy|) sobre los lados (un extremo por lado)."""
    n = len(poli)
    return sum(math.gcd(abs(poli[(i + 1) % n][0] - poli[i][0]),
                        abs(poli[(i + 1) % n][1] - poli[i][1])) for i in range(n))


def puntos_interiores(poli):
    """Pick: I = (2A − B + 2) / 2."""
    return (area2(poli) - puntos_borde(poli) + 2) // 2


def demo():
    T = [(0, 0), (4, 0), (0, 4)]
    print("triángulo", T, ": 2A =", area2(T), " B =", puntos_borde(T),
          " I =", puntos_interiores(T))                     # 16 12 3
    C = [(0, 0), (3, 0), (3, 3), (0, 3)]
    print("cuadrado", C, ": I =", puntos_interiores(C), " B =", puntos_borde(C))  # 4 12
    print("puntos enteros en [(0,0),(6,4)]:", puntos_en_segmento((0, 0), (6, 4)))  # 3
    G = [(0, 0), (10 ** 9, 0), (0, 10 ** 9)]
    print("triángulo gigante: I =", puntos_interiores(G))


# ---------------------------------------------------------------- pruebas
def _estrella(rng, k, r):
    dirs = set()
    while len(dirs) < k:
        dx, dy = rng.randint(-4, 4), rng.randint(-4, 4)
        if (dx, dy) != (0, 0) and math.gcd(dx, dy) == 1:
            dirs.add((dx, dy))
    dirs = sorted(dirs, key=lambda d: math.atan2(d[1], d[0]))
    angs = [math.atan2(d[1], d[0]) for d in dirs]
    huecos = [angs[i + 1] - angs[i] for i in range(k - 1)] + [angs[0] + 2 * math.pi - angs[-1]]
    if max(huecos) >= math.pi - 1e-12:
        return None
    pts = []
    for d in dirs:
        s = rng.randint(1, r)
        pts.append((d[0] * s, d[1] * s))
    return pts


def _cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _ubicar(poli, p):
    """1 dentro, 0 borde, −1 fuera (ray casting entero)."""
    n = len(poli)
    dentro = False
    for i in range(n):
        a, b = poli[i], poli[(i + 1) % n]
        if _cruz(a, b, p) == 0 and \
                (a[0] - p[0]) * (b[0] - p[0]) + (a[1] - p[1]) * (b[1] - p[1]) <= 0:
            return 0
        if (a[1] > p[1]) != (b[1] > p[1]):
            if (_cruz(a, b, p) > 0) == (b[1] > a[1]):
                dentro = not dentro
    return 1 if dentro else -1


def pruebas():
    random.seed(10088)
    rng = random.Random(8)

    # Casos borde
    assert puntos_en_segmento((0, 0), (0, 0)) == 1
    assert puntos_en_segmento((5, -3), (-1, 6)) == 4                 # gcd(6, 9) = 3
    assert puntos_interiores([(0, 0), (1, 0), (0, 1)]) == 0
    assert puntos_interiores([(0, 0), (2, 0), (0, 2)]) == 0           # B = 6, 2A = 4
    assert puntos_interiores([(0, 0), (0, 3), (3, 3), (3, 0)]) == 4   # sentido horario
    n = 10 ** 9
    assert puntos_interiores([(0, 0), (n, 0), (n, n), (0, n)]) == (n - 1) ** 2

    hechos = 0
    while hechos < 1500:
        poli = _estrella(rng, rng.randint(3, 8), rng.randint(1, 4))
        if poli is None:
            continue
        hechos += 1
        if rng.random() < 0.5:
            poli = poli[::-1]
        xs, ys = [p[0] for p in poli], [p[1] for p in poli]
        dentro = borde = 0
        for x in range(min(xs), max(xs) + 1):
            for y in range(min(ys), max(ys) + 1):
                u = _ubicar(poli, (x, y))
                dentro += u == 1
                borde += u == 0
        assert puntos_borde(poli) == borde
        assert puntos_interiores(poli) == dentro, (poli, dentro)

    for _ in range(2000):
        a = (random.randint(-12, 12), random.randint(-12, 12))
        b = (random.randint(-12, 12), random.randint(-12, 12))
        cuenta = sum(1 for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1)
                     for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1)
                     if _cruz(a, b, (x, y)) == 0)
        assert puntos_en_segmento(a, b) == cuenta


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
