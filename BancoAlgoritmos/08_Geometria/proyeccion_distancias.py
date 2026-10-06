r"""
Geometría — Proyección y distancias punto–recta, punto–segmento («projection»)
Nivel: Intermedio
Ejecutar: python proyeccion_distancias.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar el punto de una recta (o de un segmento) más cercano a un
    punto dado, su distancia, el reflejo de un punto respecto a una recta,
    y la distancia entre dos segmentos.
    Señales en el enunciado: «distancia mínima de la casa a la carretera»,
    «¿qué tan cerca pasa el láser/la trayectoria?», «pie de la
    perpendicular», «reflejo/espejo», «radio de seguridad alrededor de un
    camino», «distancia entre dos tramos».

FUNCIÓN
    proyeccion(p, a, b) -> (float, float)   pie de la perpendicular de p
                                            sobre la recta ab (a != b)
    reflejo(p, a, b) -> (float, float)      simétrico de p respecto a ab
    distancia_punto_recta(p, a, b) -> float
    distancia_punto_segmento(p, a, b) -> float      (a == b permitido)
    dist2_punto_segmento(p, a, b) -> Fraction       distancia AL CUADRADO,
                                                    exacta con enteros
    distancia_segmentos(a, b, c, d) -> float        0 si se tocan

IDEA Y ALGORITMO
    Proyección: el punto de la recta a + t·(b − a) más cercano a p es aquel
    donde p − proyección es PERPENDICULAR a la recta:
        (p − a − t(b − a))·(b − a) = 0  ->  t = (p − a)·(b − a) / |b − a|².
    t es la «sombra» de p sobre la recta en unidades de |b − a|: t = 0 en a,
    t = 1 en b.

                   p                      p'
                   |                     /
                   | d              (t < 0: el más cercano
        a ---------+--------- b          del SEGMENTO es a)
                   q = a + t(b − a)

    Distancia a la recta: área del paralelogramo / base:
        d = |(b − a)×(p − a)| / |b − a|   (sin calcular q).
    Distancia al SEGMENTO: si t <= 0 el punto más cercano es a, si t >= 1 es
    b, y si no es q. Por qué: |p − (a + t(b − a))|² es una parábola en t con
    mínimo en el t de la proyección; restringida a [0, 1], el mínimo es ese
    t recortado a [0, 1].
    Con enteros, t = num/den es racional y la distancia AL CUADRADO también
    (cruz²/|b − a|²): se puede comparar distancias sin floats.
    Reflejo: p' = 2q − p.
    Distancia entre segmentos: si se cortan es 0; si no, el par más cercano
    siempre tiene un extremo de alguno de los dos, así que es el mínimo de
    las 4 distancias extremo–segmento.

MACROALGORITMO
    1. v = b − a, w = p − a.
    2. t = (w·v) / (v·v).
    3. Proyección = a + t·v; reflejo = 2·proyección − p.
    4. Distancia a la recta = |v×w| / |v|.
    5. Distancia al segmento: recortar t a [0, 1] y medir a a + t·v.
    6. Segmentos: 0 si se intersecan; si no, mínimo de 4 punto–segmento.

COMPLEJIDAD
    O(1) cada función. Memoria O(1).

EJEMPLO A MANO
    a = (0, 0), b = (4, 0):
      p = (1, 3): t = (1·4 + 3·0)/16 = 1/4 -> q = (1, 0), d = 12/4 = 3.
      p = (6, 2): t = 24/16 = 1.5 > 1 -> el más cercano del segmento es b:
                  distancia √(4 + 4) = √8 ≈ 2.828 (a la recta sería 2).
      reflejo de (1, 3) = 2·(1, 0) − (1, 3) = (1, −3).

ERRORES TÍPICOS
    - Usar la distancia a la RECTA cuando piden distancia al SEGMENTO (o al
      revés): con t fuera de [0, 1] dan distinto.
    - Dividir por |b − a|² cuando a == b (segmento de largo 0).
    - Comparar distancias con sqrt y floats teniendo enteros: comparar
      cuadrados (dist2_punto_segmento).
    - Distancia entre segmentos: olvidar el caso en que se cruzan (da 0,
      no la distancia entre extremos).

VARIANTES Y RELACIONADOS
    - Distancia CON SIGNO a una recta orientada: cruz/|v| (> 0 a la
      izquierda). Base del centro de Chebyshev (semiplanos.py).
    - Proyección sobre un eje: la base del eje separador (eje_separador.py).
    - Intersección de segmentos (interseccion_segmentos.py).
    - Distancia punto–polígono: mínimo sobre las aristas (0 si está dentro,
      ver punto_en_poligono.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/F - Heist (distancias con signo a láseres y
      paredes; proyección del origen sobre el segmento óptimo)
    - ICPC/Colombia 2017/F - Fish (proyectar puntos sobre ejes)

VERIFICACIÓN
    - Pruebas: OK en 3000 casos aleatorios: proyección comprobada exacta
      (perpendicularidad con Fraction), distancias punto–recta y
      punto–segmento contra búsqueda ternaria sobre el parámetro t,
      distancia exacta contra la versión float, y 300 pares de segmentos
      contra búsqueda ternaria anidada en (t, s) (python proyeccion_distancias.py)
"""
import math
import random
from fractions import Fraction


def cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def proyeccion(p, a, b):
    """Pie de la perpendicular de p sobre la recta ab (a != b)."""
    vx, vy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / (vx * vx + vy * vy)
    return (a[0] + t * vx, a[1] + t * vy)


def reflejo(p, a, b):
    """Simétrico de p respecto a la recta ab."""
    qx, qy = proyeccion(p, a, b)
    return (2 * qx - p[0], 2 * qy - p[1])


def distancia_punto_recta(p, a, b):
    """|(b − a) × (p − a)| / |b − a|  (área del paralelogramo / base)."""
    return abs(cruz(a, b, p)) / math.hypot(b[0] - a[0], b[1] - a[1])


def distancia_punto_segmento(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    wx, wy = p[0] - a[0], p[1] - a[1]
    t = wx * vx + wy * vy                       # sin dividir todavía
    if t <= 0:                                  # antes de a (o a == b)
        return math.hypot(wx, wy)
    nn = vx * vx + vy * vy
    if t >= nn:                                 # después de b
        return math.hypot(p[0] - b[0], p[1] - b[1])
    return abs(vx * wy - vy * wx) / math.sqrt(nn)   # el pie cae dentro


def dist2_punto_segmento(p, a, b):
    """Distancia al cuadrado, exacta (Fraction) si las coordenadas son enteras."""
    vx, vy = b[0] - a[0], b[1] - a[1]
    wx, wy = p[0] - a[0], p[1] - a[1]
    t = wx * vx + wy * vy
    if t <= 0:
        return Fraction(wx * wx + wy * wy)
    nn = vx * vx + vy * vy
    if t >= nn:
        return Fraction((p[0] - b[0]) ** 2 + (p[1] - b[1]) ** 2)
    c = vx * wy - vy * wx
    return Fraction(c * c, nn)


def _en_segmento(p, a, b):
    return (cruz(a, b, p) == 0 and
            (a[0] - p[0]) * (b[0] - p[0]) + (a[1] - p[1]) * (b[1] - p[1]) <= 0)


def _se_intersecan(a, b, c, d):
    o1, o2, o3, o4 = cruz(a, b, c), cruz(a, b, d), cruz(c, d, a), cruz(c, d, b)
    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and \
       ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
        return True
    return (_en_segmento(c, a, b) or _en_segmento(d, a, b) or
            _en_segmento(a, c, d) or _en_segmento(b, c, d))


def distancia_segmentos(a, b, c, d):
    """Distancia mínima entre los segmentos [a, b] y [c, d]."""
    if _se_intersecan(a, b, c, d):
        return 0.0
    return min(distancia_punto_segmento(a, c, d), distancia_punto_segmento(b, c, d),
               distancia_punto_segmento(c, a, b), distancia_punto_segmento(d, a, b))


def demo():
    a, b = (0, 0), (4, 0)
    print("proyección de (1,3) sobre ab:", proyeccion((1, 3), a, b))       # (1.0, 0.0)
    print("distancia (1,3)-recta:", distancia_punto_recta((1, 3), a, b))   # 3.0
    print("reflejo de (1,3):", reflejo((1, 3), a, b))                      # (1.0, -3.0)
    print("(6,2): a la recta %.3f, al segmento %.3f (exacta² = %s)" % (
        distancia_punto_recta((6, 2), a, b), distancia_punto_segmento((6, 2), a, b),
        dist2_punto_segmento((6, 2), a, b)))
    print("distancia entre [(0,0),(4,0)] y [(1,1),(3,5)]: %.3f"
          % distancia_segmentos(a, b, (1, 1), (3, 5)))                      # 1.0


def _ternaria(f, lo, hi, it=100):
    """Mínimo de una función convexa en [lo, hi] (fuerza bruta numérica)."""
    for _ in range(it):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(m1) <= f(m2):
            hi = m2
        else:
            lo = m1
    return f((lo + hi) / 2)


def pruebas():
    random.seed(77)

    # Casos borde
    assert distancia_punto_segmento((3, 4), (0, 0), (0, 0)) == 5.0       # a == b
    assert dist2_punto_segmento((3, 4), (0, 0), (0, 0)) == 25
    assert distancia_punto_segmento((2, 0), (0, 0), (4, 0)) == 0.0
    assert distancia_segmentos((0, 0), (4, 4), (0, 4), (4, 0)) == 0.0
    assert distancia_segmentos((0, 0), (1, 0), (3, 0), (5, 0)) == 2.0      # colineales
    assert reflejo((0, 5), (0, 0), (1, 1)) == (5.0, 0.0)

    def d(p, q):
        return math.hypot(p[0] - q[0], p[1] - q[1])

    for _ in range(3000):
        a, b, p = [(random.randint(-20, 20), random.randint(-20, 20)) for _ in range(3)]
        # Segmento (a == b incluido): ternaria sobre t en [0, 1]
        en = lambda t: d(p, (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
        ds = distancia_punto_segmento(p, a, b)
        assert abs(ds - _ternaria(en, 0.0, 1.0)) < 1e-6
        assert abs(math.sqrt(dist2_punto_segmento(p, a, b)) - ds) < 1e-9
        if a == b:
            continue
        # Recta: ternaria sobre t en un rango amplio
        assert abs(distancia_punto_recta(p, a, b) - _ternaria(en, -100.0, 100.0, 200)) < 1e-6
        # Proyección exacta: (p − q)·(b − a) = 0 y q en la recta (con Fraction)
        vx, vy = b[0] - a[0], b[1] - a[1]
        t = Fraction((p[0] - a[0]) * vx + (p[1] - a[1]) * vy, vx * vx + vy * vy)
        q = (a[0] + t * vx, a[1] + t * vy)
        assert (p[0] - q[0]) * vx + (p[1] - q[1]) * vy == 0
        qf = proyeccion(p, a, b)
        assert abs(qf[0] - q[0]) < 1e-9 and abs(qf[1] - q[1]) < 1e-9
        r = reflejo(p, a, b)                    # el reflejo equidista de a y b
        assert abs(d(r, a) - d(p, a)) < 1e-9 and abs(d(r, b) - d(p, b)) < 1e-9

    for _ in range(300):
        a, b, c, e = [(random.randint(-6, 6), random.randint(-6, 6)) for _ in range(4)]
        # Fuerza bruta: ternaria anidada en (t, s); la distancia es convexa en ambos
        def interior(t):
            P = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
            return _ternaria(lambda s: d(P, (c[0] + s * (e[0] - c[0]), c[1] + s * (e[1] - c[1]))),
                             0.0, 1.0, 50)
        assert abs(distancia_segmentos(a, b, c, e) - _ternaria(interior, 0.0, 1.0, 50)) < 1e-5


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
