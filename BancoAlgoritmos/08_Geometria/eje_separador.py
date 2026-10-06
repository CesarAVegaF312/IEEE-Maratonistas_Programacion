r"""
Geometría — Teorema del eje separador: ¿se intersecan dos convexos? («SAT»)
Nivel: Avanzado
Ejecutar: python eje_separador.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir si dos polígonos CONVEXOS se tocan o están separados, y con eso
    si dos conjuntos de puntos se pueden separar con una recta (separabilidad
    lineal): basta mirar sus envolventes convexas.
    Señales en el enunciado: «¿se puede trazar una línea/pared/panel que
    deje a todos los A de un lado y a todos los B del otro?», «¿chocan los
    dos objetos convexos?», colisiones de cajas giradas, «sin tocar
    ningún punto».

FUNCIÓN
    se_intersecan_convexos(P, Q) -> bool
        P, Q: vértices de polígonos convexos (cualquier sentido), también
        degenerados: 1 vértice (punto) o 2 (segmento). True si comparten
        algún punto (tocarse en el borde CUENTA como intersecar).
    separables(A, B) -> bool
        ¿Existe una recta que deje los puntos de A estrictamente de un lado
        y los de B estrictamente del otro? (= envolventes disjuntas).

IDEA Y ALGORITMO
    Proyectar una figura sobre un eje (dirección u) da un intervalo
    [min p·u, max p·u]. Si para algún eje los intervalos de P y Q NO se
    solapan, una recta perpendicular a u por el hueco las separa.

           eje u  ----[====P====]----[===Q===]---->   intervalos disjuntos
                                   |
                         recta separadora (perpendicular a u)

    TEOREMA (SAT): dos convexos compactos son disjuntos si y solo si existe
    un eje con proyecciones disjuntas, y basta probar como ejes las NORMALES
    DE LAS ARISTAS de ambos polígonos.
    Por qué basta con esas normales: tome el par de puntos más cercanos
    (x en P, y en Q). La recta perpendicular a x − y por el punto medio
    separa. Si x o y está en el interior de una arista, x − y es normal a
    esa arista. Si ambos son vértices, se puede girar la recta separadora
    alrededor hasta apoyarla en una arista sin dejar de separar... salvo en
    figuras DEGENERADAS (punto o segmento), donde no hay arista en la que
    apoyarse en esa dirección: dos puntos, o dos segmentos colineales
    separados. Por eso, si alguna figura tiene <= 2 vértices, se agregan
    además como ejes las diferencias entre pares de vértices.
    Con coordenadas enteras, la normal de la arista (a, b) es
    (ay − by, bx − ax) y los productos punto son enteros: exacto.
    Separabilidad de conjuntos de puntos: A y B se separan estrictamente
    con una recta  <=>  conv(A) ∩ conv(B) = ∅  (un punto de A en el lado de
    B haría que la envolvente de A cruzara la recta).

MACROALGORITMO
    1. (Si vienen puntos sueltos) calcular la envolvente de cada conjunto.
    2. Ejes = normales de cada arista de P y de Q.
    3. Si P o Q tiene <= 2 vértices: agregar las diferencias p − q.
    4. Para cada eje u: proyectar todos los vértices de P y de Q.
    5. Si max(P) < min(Q) o max(Q) < min(P): separados -> False.
    6. Si ningún eje separa -> se intersecan (True).

COMPLEJIDAD
    O((n + m)²): n + m ejes, cada uno proyecta n + m vértices. Con 500
    puntos por conjunto, ~10^6 operaciones (bien en Python). Existe una
    versión O(n + m) (Minkowski) y otra O(log) para convexos, pero rara vez
    hace falta.

EJEMPLO A MANO
    P = cuadrado (0,0) (2,0) (2,2) (0,2); Q = triángulo (3,1) (5,0) (5,3).
    Eje de la arista (2,0)->(2,2) de P: normal (0 − 2, 2 − 2) = (−2, 0).
    Proyección de P: x·(−2) ∈ {0, −4} -> [−4, 0]. De Q: {−6, −10, −10} ->
    [−10, −6]. Disjuntos -> separados (la recta x = 2.5 los separa).
    Si Q = (2,1) (5,0) (5,3), en el eje (−2, 0) Q da [−10, −4] y se toca con
    [−4, 0]: ningún eje separa -> se intersecan (se tocan en (2, 1)).

ERRORES TÍPICOS
    - Probar solo las aristas de UNO de los polígonos: hacen falta las de
      ambos.
    - Olvidar los casos degenerados (punto, segmento, colineales): los ejes
      de aristas no bastan (ejemplo: dos segmentos sobre la misma recta).
    - Confundir separación estricta (no tocarse: <) con no estricta (<=),
      según pida el enunciado («sin tocar» = estricta).
    - Aplicarlo a polígonos NO convexos: el teorema no vale; habría que
      partirlos en convexos o usar intersección de segmentos.
    - Normalizar los ejes con sqrt sin necesidad: la comparación de
      intervalos es la misma con ejes sin normalizar (todo entero).

VARIANTES Y RELACIONADOS
    - Con floats: proyectar con normales unitarias; el solape mínimo da el
      vector para separar (respuesta de colisiones en juegos).
    - Intersección por segmentos: dos polígonos (convexos o no) se tocan si
      se cortan dos lados o uno contiene un vértice del otro
      (interseccion_segmentos.py + punto_en_poligono.py).
    - Envolvente (envolvente_convexa.py); proyección (proyeccion_distancias.py).
    - Separar con un MARGEN máximo: programación lineal / SVM.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/F - Fish (envolventes + eje separador, peces A y B
      separables por un panel recto)

VERIFICACIÓN
    - Pruebas: OK en 6000 pares de polígonos convexos aleatorios (como
      envolventes de puntos al azar, con muchos degenerados: puntos,
      segmentos, colineales, que se tocan en un vértice o un lado) contra
      fuerza bruta: se tocan si algún par de lados se corta o algún vértice
      de uno está dentro (cerrado) del otro; y separables en 150 casos
      contra búsqueda exhaustiva de rectas candidatas por pares de puntos,
      giradas y desplazadas un epsilon racional (python eje_separador.py)
"""
import random
from fractions import Fraction


def cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def envolvente(puntos):
    """Andrew, sin colineales, antihorario; 1 punto -> [p], colineales -> 2."""
    pts = sorted(set(puntos))
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


def se_intersecan_convexos(P, Q):
    """True si los convexos P y Q comparten algún punto (tocarse cuenta)."""
    ejes = []
    for F in (P, Q):
        k = len(F)
        if k >= 2:
            for i in range(k):
                (x1, y1), (x2, y2) = F[i], F[(i + 1) % k]
                ejes.append((y1 - y2, x2 - x1))        # normal de la arista
    if len(P) <= 2 or len(Q) <= 2:                     # degenerados
        for p in P:
            for q in Q:
                ejes.append((p[0] - q[0], p[1] - q[1]))
    for ex, ey in ejes:
        if ex == 0 and ey == 0:
            continue
        proy_p = [x * ex + y * ey for x, y in P]
        proy_q = [x * ex + y * ey for x, y in Q]
        if max(proy_p) < min(proy_q) or max(proy_q) < min(proy_p):
            return False                               # eje separador hallado
    return True


def separables(A, B):
    """¿Una recta deja A y B en lados estrictamente opuestos?"""
    return not se_intersecan_convexos(envolvente(A), envolvente(B))


def demo():
    P = [(0, 0), (2, 0), (2, 2), (0, 2)]
    Q = [(3, 1), (5, 0), (5, 3)]
    print("P =", P, " Q =", Q, "-> se intersecan:", se_intersecan_convexos(P, Q))  # False
    Q2 = [(2, 1), (5, 0), (5, 3)]
    print("P y", Q2, "-> se intersecan:", se_intersecan_convexos(P, Q2))           # True
    print("segmentos colineales (0,0)-(1,0) y (2,0)-(3,0):",
          se_intersecan_convexos([(0, 0), (1, 0)], [(2, 0), (3, 0)]))              # False
    A = [(0, 0), (1, 2), (2, 0)]
    B = [(3, 3), (4, 1), (5, 4)]
    print("A =", A, " B =", B, "-> separables:", separables(A, B))                 # True
    print("agregando (4,2) a A:", separables(A + [(4, 2)], B))                     # False


# ---------------------------------------------------------------- pruebas
def _en_segmento(p, a, b):
    return (cruz(a, b, p) == 0 and
            (a[0] - p[0]) * (b[0] - p[0]) + (a[1] - p[1]) * (b[1] - p[1]) <= 0)


def _segs_se_tocan(a, b, c, d):
    o1, o2, o3, o4 = cruz(a, b, c), cruz(a, b, d), cruz(c, d, a), cruz(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return (_en_segmento(c, a, b) or _en_segmento(d, a, b) or
            _en_segmento(a, c, d) or _en_segmento(b, c, d))


def _dentro_cerrado(F, p):
    """p dentro o en el borde del convexo F (antihorario, >= 3 vértices)."""
    k = len(F)
    return all(cruz(F[i], F[(i + 1) % k], p) >= 0 for i in range(k))


def _bruto_intersecan(P, Q):
    lados = lambda F: [(F[i], F[(i + 1) % len(F)]) for i in range(len(F))]
    for a, b in lados(P):
        for c, d in lados(Q):
            if _segs_se_tocan(a, b, c, d):
                return True
    if len(P) >= 3 and any(_dentro_cerrado(P, q) for q in Q):
        return True
    if len(Q) >= 3 and any(_dentro_cerrado(Q, p) for p in P):
        return True
    return False


def _bruto_separables(A, B):
    # Una recta separadora estricta puede tomarse «casi» por dos puntos del
    # conjunto: probamos las rectas por pares (p, q) de puntos (y por un punto
    # en todas las direcciones de pares) desplazadas/giradas un epsilon
    # racional, y verificamos con aritmética exacta.
    pts = list(set(A) | set(B))
    eps = Fraction(1, 1000)
    dirs = {(q[0] - p[0], q[1] - p[1]) for p in pts for q in pts if p != q} | {(1, 0), (0, 1)}
    for p in pts:
        for dx, dy in dirs:
            for gx, gy in ((dx, dy), (dx - eps * dy, dy + eps * dx), (dx + eps * dy, dy - eps * dx)):
                for corr in (-eps, eps):
                    # recta por p + corr·normal, dirección (gx, gy)
                    ox, oy = p[0] - corr * gy, p[1] + corr * gx
                    lado = lambda r: gx * (r[1] - oy) - gy * (r[0] - ox)
                    sa = [lado(r) for r in A]
                    sb = [lado(r) for r in B]
                    if (all(s > 0 for s in sa) and all(s < 0 for s in sb)) or \
                       (all(s < 0 for s in sa) and all(s > 0 for s in sb)):
                        return True
    return False


def pruebas():
    random.seed(2017)

    # Casos borde
    assert se_intersecan_convexos([(0, 0)], [(0, 0)])
    assert not se_intersecan_convexos([(0, 0)], [(1, 1)])
    assert se_intersecan_convexos([(1, 1)], [(0, 0), (2, 2)])            # punto en segmento
    assert not se_intersecan_convexos([(3, 3)], [(0, 0), (2, 2)])        # colineal, fuera
    assert se_intersecan_convexos([(0, 0), (2, 0)], [(2, 0), (4, 0)])    # se tocan en (2,0)
    assert se_intersecan_convexos([(0, 0), (4, 0), (0, 4)], [(1, 1)])    # punto dentro
    assert se_intersecan_convexos([(0, 0), (4, 0), (4, 4), (0, 4)],
                                  [(4, 4), (6, 4), (6, 6)])              # vértice con vértice

    for _ in range(6000):
        r = random.choice([2, 3, 5])
        A = [(random.randint(-r, r), random.randint(-r, r)) for _ in range(random.randint(1, 6))]
        B = [(random.randint(-r, r), random.randint(-r, r)) for _ in range(random.randint(1, 6))]
        P, Q = envolvente(A), envolvente(B)
        if random.random() < 0.5:
            P = P[::-1]                                  # el sentido no importa
        esperado = _bruto_intersecan(envolvente(A), envolvente(B))
        assert se_intersecan_convexos(P, Q) == esperado == se_intersecan_convexos(Q, P)

    for _ in range(150):
        A = [(random.randint(-2, 2), random.randint(-2, 2)) for _ in range(random.randint(1, 3))]
        B = [(random.randint(-2, 2), random.randint(-2, 2)) for _ in range(random.randint(1, 3))]
        if set(A) & set(B):
            assert not separables(A, B)
            continue
        assert separables(A, B) == _bruto_separables(A, B), (A, B)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
