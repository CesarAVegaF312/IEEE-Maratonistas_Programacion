r"""
Geometría — Intersección de segmentos y de rectas («segment intersection»)
Nivel: Intermedio
Ejecutar: python interseccion_segmentos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Saber si dos segmentos se tocan (incluyendo tocarse en un extremo o
    solaparse sobre la misma recta) y, si se cortan, en qué punto; y hallar
    el punto de corte de dos rectas.
    Señales en el enunciado: «¿se cruzan los cables/caminos/paredes?»,
    «¿la línea de visión atraviesa el obstáculo?», «¿el polígono es
    simple?», «punto donde se cortan las rectas», «tocar cuenta como cruzar».

FUNCIÓN
    se_intersecan(a, b, c, d) -> bool
        ¿Los segmentos CERRADOS [a, b] y [c, d] comparten algún punto?
        (Extremos incluidos; segmentos de largo 0 permitidos.)
    interseccion_rectas(a, b, c, d) -> (Fraction, Fraction) | None
        Corte de la recta por a, b con la recta por c, d; None si paralelas.
    interseccion_segmentos(a, b, c, d) -> list
        []      si no se tocan,
        [p]     si se tocan en un solo punto,
        [p, q]  si se solapan en el segmento [p, q] (colineales), p < q.
        Puntos como tuplas de Fraction (exactas); float(x) para imprimir.

IDEA Y ALGORITMO
    Caso general: [a, b] y [c, d] se cruzan si c y d quedan en lados
    OPUESTOS de la recta ab, y a y b en lados opuestos de la recta cd:
        o1 = orient(a, b, c), o2 = orient(a, b, d)
        o3 = orient(c, d, a), o4 = orient(c, d, b)
        se cruzan «propiamente» si o1·o2 < 0 y o3·o4 < 0.

            c                 c
            |                  \       d     a, b del mismo lado de cd:
      a ----+---- b       a ----- b     \    no se cortan
            |                            \
            d                             c

    Casos especiales (alguna orientación es 0): un extremo está sobre la
    recta del otro segmento; entonces se tocan si y solo si ese extremo
    está DENTRO del otro segmento (en_segmento). Esto cubre tocar en un
    extremo, la T, los colineales que se solapan y los que no, y los
    segmentos de largo 0. Todo con enteros: exacto.
    Punto de corte de rectas: p = a + t·(b − a). Para que p esté en la
    recta cd, (p − c)×(d − c) = 0, de donde
        t = (c − a)×(d − c) / (b − a)×(d − c).
    Si el denominador es 0 las rectas son paralelas (o la misma). Con datos
    enteros t es racional: Fraction lo da exacto (o usar floats al final).
    Solape colineal: los puntos del solape son extremos de alguno de los
    dos segmentos; basta quedarse con los extremos que están en ambos y
    tomar el menor y el mayor (en una recta, el orden (x, y) es monótono).

MACROALGORITMO
    1. Calcular o1, o2, o3, o4 con productos cruz enteros.
    2. Si o1·o2 < 0 y o3·o4 < 0 -> se cruzan en un punto interior.
    3. Si no, si algún extremo está sobre el otro segmento -> se tocan.
    4. Si no -> no se tocan.
    5. Para el punto: si (b − a)×(d − c) != 0, usar la fórmula de t.
    6. Si es 0 (colineales y se tocan): extremos comunes, menor y mayor.

COMPLEJIDAD
    O(1) por par de segmentos. Verificar todos los pares de n segmentos es
    O(n²) (~3000 segmentos en Python en ~1 s); para muchos segmentos existe
    el barrido de Shamos–Hoey / Bentley–Ottmann (O(n log n)).

EJEMPLO A MANO
    [(0,0),(4,4)] y [(0,4),(4,0)]: o1 = cruz((0,0),(4,4),(0,4)) = 16 > 0,
    o2 = −16 < 0; o3 = −16, o4 = 16 -> se cruzan. t = (0,4)×(4,−4) /
    (4,4)×(4,−4) = (0·(−4) − 4·4)/(4·(−4) − 4·4) = −16/−32 = 1/2 ->
    p = (0,0) + ½(4,4) = (2, 2).
    [(0,0),(4,0)] y [(2,0),(6,0)]: colineales, solape [(2,0), (4,0)].
    [(0,0),(2,0)] y [(3,0),(5,0)]: colineales sin solape -> [].

ERRORES TÍPICOS
    - Solo revisar o1·o2 < 0 y o3·o4 < 0: falla cuando se tocan en un
      extremo o son colineales (y ahí está la mitad de los casos de prueba).
    - Colineales: concluir «se tocan» solo porque las 4 orientaciones son 0
      (pueden estar en la misma recta pero separados).
    - Calcular el punto de corte con pendientes m = dy/dx: falla con rectas
      verticales. Usar la forma paramétrica con productos cruz.
    - Multiplicar o1·o2 con valores grandes en C++ (desborde): comparar
      signos. En Python da igual.

VARIANTES Y RELACIONADOS
    - Intersección estricta (sin contar el toque): solo el paso 2.
    - Segmento contra polígono convexo / rectángulo: probar contra cada lado
      y ver si un extremo está dentro (punto_en_poligono.py).
    - Muchos segmentos: barrido (linea_de_barrido.py, idea de eventos).
    - Orientación (orientacion_ccw.py), distancias entre segmentos
      (proyeccion_distancias.py: si no se cortan, la distancia mínima es de
      un extremo al otro segmento).

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/G - Guard Deployment (¿el segmento entre dos
      torres toca el rectángulo de un edificio?)
    - CSES «Line Segment Intersection» (exactamente se_intersecan)

VERIFICACIÓN
    - Pruebas: OK en 30000 pares de segmentos aleatorios con coordenadas
      chicas (muchos colineales, extremos compartidos, segmentos de largo 0)
      contra una fuerza bruta paramétrica independiente: sistema 2×2 por
      Cramer con Fraction y, si son paralelos, solape de intervalos de
      parámetros sobre la recta común (python interseccion_segmentos.py)
"""
import random
from fractions import Fraction


def cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def signo(v):
    return (v > 0) - (v < 0)


def en_segmento(p, a, b):
    """¿p está en el segmento cerrado [a, b]? (exacto)"""
    return (cruz(a, b, p) == 0 and
            (a[0] - p[0]) * (b[0] - p[0]) + (a[1] - p[1]) * (b[1] - p[1]) <= 0)


def se_intersecan(a, b, c, d):
    """¿Los segmentos cerrados [a, b] y [c, d] se tocan?"""
    o1, o2 = signo(cruz(a, b, c)), signo(cruz(a, b, d))
    o3, o4 = signo(cruz(c, d, a)), signo(cruz(c, d, b))
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True                     # cruce propio, en el interior de ambos
    # Algún extremo sobre la recta del otro: se tocan solo si está dentro.
    return (en_segmento(c, a, b) or en_segmento(d, a, b) or
            en_segmento(a, c, d) or en_segmento(b, c, d))


def interseccion_rectas(a, b, c, d):
    """Corte de las rectas ab y cd (Fractions exactas) o None si paralelas."""
    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = d[0] - c[0], d[1] - c[1]
    den = rx * sy - ry * sx             # (b − a) × (d − c)
    if den == 0:
        return None
    t = Fraction((c[0] - a[0]) * sy - (c[1] - a[1]) * sx, den)
    return (a[0] + t * rx, a[1] + t * ry)


def interseccion_segmentos(a, b, c, d):
    """[] si no se tocan, [p] si en un punto, [p, q] si se solapan."""
    if not se_intersecan(a, b, c, d):
        return []
    p = interseccion_rectas(a, b, c, d)
    if p is not None and a != b and c != d:
        return [p]
    # Paralelos que se tocan => colineales (o algún segmento es un punto).
    comunes = sorted({q for q in (a, b, c, d) if en_segmento(q, a, b) and en_segmento(q, c, d)})
    ini, fin = comunes[0], comunes[-1]
    ini, fin = (Fraction(ini[0]), Fraction(ini[1])), (Fraction(fin[0]), Fraction(fin[1]))
    return [ini] if ini == fin else [ini, fin]


def demo():
    casos = [((0, 0), (4, 4), (0, 4), (4, 0)),     # cruce en (2, 2)
             ((0, 0), (4, 0), (2, 0), (6, 0)),     # solape [(2,0), (4,0)]
             ((0, 0), (2, 0), (3, 0), (5, 0)),     # colineales sin tocarse
             ((0, 0), (4, 0), (2, 0), (2, 5)),     # forma de T
             ((0, 0), (1, 1), (0, 1), (1, 2))]     # paralelos
    for a, b, c, d in casos:
        res = interseccion_segmentos(a, b, c, d)
        texto = [tuple(str(v) for v in p) for p in res]
        print([a, b], [c, d], "->", se_intersecan(a, b, c, d), texto)
    p = interseccion_rectas((0, 0), (3, 1), (0, 2), (2, 0))
    print("rectas (0,0)-(3,1) y (0,2)-(2,0) se cortan en (%s, %s) = (%.4f, %.4f)"
          % (p[0], p[1], float(p[0]), float(p[1])))


def _bruto(a, b, c, d):
    """Fuerza bruta paramétrica: a + t(b − a) = c + s(d − c), t, s en [0, 1]."""
    u = (b[0] - a[0], b[1] - a[1])
    v = (d[0] - c[0], d[1] - c[1])
    w = (c[0] - a[0], c[1] - a[1])
    det = u[0] * (-v[1]) - u[1] * (-v[0])
    if det != 0:
        # Cramer sobre [u, −v]·(t, s) = w
        t = Fraction(w[0] * (-v[1]) - w[1] * (-v[0]), det)
        s = Fraction(u[0] * w[1] - u[1] * w[0], det)
        if 0 <= t <= 1 and 0 <= s <= 1:
            return [(a[0] + t * u[0], a[1] + t * u[1])]
        return []
    # Paralelos: elegir una dirección no nula de la recta común
    if u == (0, 0) and v == (0, 0):
        return [(Fraction(a[0]), Fraction(a[1]))] if a == c else []
    dirv, o = (u, a) if u != (0, 0) else (v, c)
    for q in (a, b, c, d):            # ¿todos sobre la misma recta?
        if dirv[0] * (q[1] - o[1]) - dirv[1] * (q[0] - o[0]) != 0:
            return []
    nn = dirv[0] ** 2 + dirv[1] ** 2

    def par(q):                       # parámetro de q sobre la recta o + λ·dirv
        return Fraction((q[0] - o[0]) * dirv[0] + (q[1] - o[1]) * dirv[1], nn)

    lo = max(min(par(a), par(b)), min(par(c), par(d)))
    hi = min(max(par(a), par(b)), max(par(c), par(d)))
    if lo > hi:
        return []
    pts = sorted({(o[0] + lo * dirv[0], o[1] + lo * dirv[1]),
                  (o[0] + hi * dirv[0], o[1] + hi * dirv[1])})
    return pts


def pruebas():
    random.seed(2017)

    # Casos borde
    assert se_intersecan((0, 0), (0, 0), (0, 0), (0, 0))
    assert not se_intersecan((0, 0), (0, 0), (1, 1), (1, 1))
    assert se_intersecan((1, 1), (1, 1), (0, 0), (2, 2))
    assert interseccion_segmentos((0, 0), (2, 2), (2, 2), (5, 0)) == [(2, 2)]
    assert interseccion_segmentos((0, 0), (4, 0), (4, 0), (0, 0)) == [(0, 0), (4, 0)]
    assert interseccion_rectas((0, 0), (1, 0), (0, 1), (5, 1)) is None
    big = 10 ** 18
    assert se_intersecan((-big, -big), (big, big), (-big, big), (big, -big))

    for _ in range(30000):
        r = random.choice([2, 3, 6])
        a, b, c, d = [(random.randint(-r, r), random.randint(-r, r)) for _ in range(4)]
        if random.random() < 0.2:         # forzar colineales
            dx, dy = random.randint(-1, 1), random.randint(-1, 1)
            o = a
            a, b, c, d = [(o[0] + k * dx, o[1] + k * dy)
                          for k in (random.randint(-3, 3) for _ in range(4))]
        esperado = _bruto(a, b, c, d)
        obtenido = interseccion_segmentos(a, b, c, d)
        assert obtenido == esperado, (a, b, c, d, obtenido, esperado)
        assert se_intersecan(a, b, c, d) == bool(esperado) == se_intersecan(c, d, b, a)
        if a != b and c != d:
            p = interseccion_rectas(a, b, c, d)
            if p is not None:     # el punto está en ambas rectas (exacto)
                assert (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) == 0
                assert (d[0] - c[0]) * (p[1] - c[1]) - (d[1] - c[1]) * (p[0] - c[0]) == 0


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
