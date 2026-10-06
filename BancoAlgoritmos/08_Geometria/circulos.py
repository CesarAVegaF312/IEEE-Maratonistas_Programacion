r"""
Geometría — Círculos: intersecciones, tangencias y punto en anillo («circles»)
Nivel: Intermedio
Ejecutar: python circulos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Resolver las preguntas típicas con círculos: ¿dónde se cortan dos
    círculos? ¿dónde corta una recta a un círculo? ¿son tangentes, uno
    contiene al otro? ¿un punto está dentro de un anillo (corona)?
    Señales en el enunciado: «radio», «alcance», «cobertura de una antena»,
    «brazo/cuerda de longitud L», «tangentes», «zona entre dos círculos»,
    «¿el disparo/trayectoria toca el obstáculo circular?».

FUNCIÓN
    relacion_circulos(c1, r1, c2, r2) -> int
        Cantidad de puntos comunes de las dos circunferencias: 0, 1
        (tangentes), 2 (secantes) o −1 (son la misma: infinitos). EXACTO
        con centros y radios enteros.
    interseccion_circulos(c1, r1, c2, r2) -> list[(float, float)]
        Los 0, 1 o 2 puntos de corte (lista vacía también si son iguales).
    interseccion_recta_circulo(a, b, c, r) -> list[(float, float)]
        Puntos donde la recta por a, b (a != b) corta al círculo (c, r),
        ordenados en la dirección de a hacia b.
    punto_en_anillo(p, c, r_in, r_out) -> bool
        r_in <= |p − c| <= r_out, comparando cuadrados (exacto).
    alcance_brazo(longitudes) -> (r_in, r_out)
        Distancias alcanzables por la punta de un brazo articulado
        (ICPC Colombia 2023 D): todo el anillo [r_in, r_out].

IDEA Y ALGORITMO
    Relación entre dos círculos: solo depende de d = |c1 − c2|:
      d > r1 + r2            separados             (0 puntos)
      d = r1 + r2            tangentes por fuera   (1)
      |r1 − r2| < d < r1+r2  secantes              (2)
      d = |r1 − r2| > 0      tangentes por dentro  (1)
      d < |r1 − r2|          uno dentro del otro   (0)
      d = 0 y r1 = r2        el mismo círculo      (infinitos)
    Comparando d² con (r1 ± r2)² todo queda en enteros: sin epsilon.

    Puntos de corte de dos círculos: sea a la distancia de c1 al pie M de la
    cuerda común sobre la recta c1c2, y h la mitad de la cuerda:

                 P1
                /|\
            r1 / |h\ r2       a² + h² = r1²,  (d − a)² + h² = r2²
              /  |  \         restando: a = (r1² − r2² + d²) / (2d)
           c1 ---M--- c2      h = √(r1² − a²)
              \  |  /         P1,2 = M ± h·(perpendicular unitaria)
                P2

    Recta–círculo: proyectar el centro sobre la recta (pie q, distancia
    dist); la recta corta si dist <= r y los puntos son q ± √(r² − dist²)·u
    con u la dirección unitaria de la recta. El número de puntos se decide
    exacto: dist² = cruz²/|b − a|², así que se compara cruz² con r²·|b − a|².
    Anillo: d² entre r_in² y r_out², sin raíces.
    Brazo (Colombia 2023 D): con secciones l1..lN, suma S y máximo L, la punta
    alcanza exactamente las distancias [max(0, 2L − S), S]: estirado da S;
    lo más cerca es 0 si L cabe plegada contra las demás (L <= S − L) y
    2L − S si no; por continuidad se alcanza todo valor intermedio.

    Precisión: la CLASIFICACIÓN (cuántos puntos) se hace con enteros; los
    puntos se calculan en float con max(0, ·) dentro de la raíz, para que una
    tangencia con error de redondeo (h² = −1e−12) no dé error de dominio.

MACROALGORITMO
    1. d² = |c1 − c2|²; clasificar comparando con (r1 + r2)² y (r1 − r2)².
    2. Si hay 0 puntos (o infinitos), devolver [].
    3. a = (r1² − r2² + d²)/(2d); h = √max(0, r1² − a²).
    4. M = c1 + a·(c2 − c1)/d; devolver M ± h·perp((c2 − c1)/d) (uno si tangentes).
    5. Recta–círculo: q = proyección de c; h = √max(0, r² − dist²); q ± h·u.

COMPLEJIDAD
    O(1) por consulta, memoria O(1).

EJEMPLO A MANO
    c1 = (0, 0), r1 = 5; c2 = (8, 0), r2 = 5: d = 8, a = (25 − 25 + 64)/16 = 4,
    h = √(25 − 16) = 3 -> puntos (4, 3) y (4, −3).
    Recta y = 3 (de (−10, 3) a (10, 3)) con el círculo (0, 0), r = 5:
    dist = 3, h = 4 -> (−4, 3) y (4, 3).
    Brazo 2, 5, 2: S = 9, L = 5 -> anillo [1, 9]. (4, 5): d² = 41 ∈ [1, 81]
    sí; (0, 0): 0 < 1 no; (9, −1): 82 > 81 no.

ERRORES TÍPICOS
    - Olvidar los casos «uno dentro del otro» y «mismo círculo» (d = 0:
      división por cero en a).
    - sqrt de un número levemente negativo en tangencias: usar max(0, ·).
    - Decidir tangencia comparando floats con ==: hacerlo con enteros.
    - En el anillo, olvidar que r_in puede ser 0 o que el borde cuenta.
    - Usar la distancia a la RECTA cuando el obstáculo se cruza con un
      SEGMENTO (ver proyeccion_distancias.py).

VARIANTES Y RELACIONADOS
    - Segmento–círculo: intersección recta–círculo y quedarse con los puntos
      de parámetro t en [0, 1].
    - Tangentes desde un punto a un círculo: el punto de tangencia T cumple
      |PT|² = |PC|² − r²; es la intersección del círculo con el de centro P y
      radio |PT|.
    - Área de intersección de dos círculos (segmentos circulares con acos).
    - Círculo mínimo que encierra puntos (Welzl, esperado O(n)).
    - Proyección (proyeccion_distancias.py), precisión (precision_flotantes.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/D - Robot Arm (alcance como anillo, todo entero)
    - ICPC/Colombia 2017/E - Rational Coins (tangencia de círculos de Ford:
      se decide comparando d² con (r1 + r2)²)

VERIFICACIÓN
    - Pruebas: OK en 5000 pares de círculos y 5000 rectas aleatorias
      (muchas tangencias y casos contenidos, coordenadas chicas): la
      cantidad de puntos coincide con la clasificación por floats
      (math.dist) y cada punto devuelto está a distancia r de cada centro
      (y sobre la recta) con error < 1e-6; punto_en_anillo contra math.dist
      y alcance_brazo contra la recurrencia por intervalos sección a sección
      en 2000 brazos aleatorios (python circulos.py)
"""
import math
import random


def relacion_circulos(c1, r1, c2, r2):
    """Puntos comunes de dos circunferencias: 0, 1, 2 o −1 (infinitos)."""
    d2 = (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2
    if d2 == 0 and r1 == r2:
        return -1
    suma2, resta2 = (r1 + r2) ** 2, (r1 - r2) ** 2
    if d2 > suma2 or d2 < resta2:
        return 0                        # separados o uno dentro del otro
    if d2 == suma2 or d2 == resta2:
        return 1                        # tangentes (por fuera o por dentro)
    return 2


def interseccion_circulos(c1, r1, c2, r2):
    """Puntos de corte (0, 1 o 2). [] si no se cortan o si son el mismo."""
    k = relacion_circulos(c1, r1, c2, r2)
    if k <= 0:
        return []
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dx, dy)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)   # de c1 al pie de la cuerda
    h = math.sqrt(max(0.0, r1 * r1 - a * a))    # media cuerda (0 si tangentes)
    mx, my = c1[0] + a * dx / d, c1[1] + a * dy / d
    if k == 1:
        return [(mx, my)]
    ox, oy = -dy / d * h, dx / d * h            # perpendicular de largo h
    return [(mx + ox, my + oy), (mx - ox, my - oy)]


def interseccion_recta_circulo(a, b, c, r):
    """Puntos de la recta ab sobre el círculo (c, r), en orden de a hacia b."""
    vx, vy = b[0] - a[0], b[1] - a[1]
    nn = vx * vx + vy * vy
    cr = vx * (c[1] - a[1]) - vy * (c[0] - a[0])   # dist = |cr| / √nn
    # Clasificación exacta: dist² vs r²  <=>  cr² vs r²·nn
    if cr * cr > r * r * nn:
        return []
    t = ((c[0] - a[0]) * vx + (c[1] - a[1]) * vy) / nn
    qx, qy = a[0] + t * vx, a[1] + t * vy          # pie de la perpendicular
    if cr * cr == r * r * nn:
        return [(qx, qy)]                          # tangente
    h = math.sqrt(max(0.0, r * r - cr * cr / nn))  # media cuerda
    ux, uy = vx / math.sqrt(nn), vy / math.sqrt(nn)
    return [(qx - h * ux, qy - h * uy), (qx + h * ux, qy + h * uy)]


def punto_en_anillo(p, c, r_in, r_out):
    """r_in <= |p − c| <= r_out, exacto con enteros."""
    d2 = (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2
    return r_in * r_in <= d2 <= r_out * r_out


def alcance_brazo(longitudes):
    """Radios del anillo alcanzable por un brazo articulado (Colombia 2023 D)."""
    s, l = sum(longitudes), max(longitudes)
    return max(0, 2 * l - s), s


def demo():
    print("círculos (0,0) r5 y (8,0) r5:", interseccion_circulos((0, 0), 5, (8, 0), 5))
    print("tangentes (0,0) r2 y (5,0) r3:", interseccion_circulos((0, 0), 2, (5, 0), 3))
    print("relación (0,0) r5 y (1,0) r2:", relacion_circulos((0, 0), 5, (1, 0), 2),
          "(uno dentro del otro)")
    print("recta y=3 y círculo (0,0) r5:",
          interseccion_recta_circulo((-10, 3), (10, 3), (0, 0), 5))
    r_in, r_out = alcance_brazo([2, 5, 2])
    print("brazo [2, 5, 2] -> anillo", (r_in, r_out))
    for p in [(4, 5), (0, 0), (9, -1)]:
        print("  ", p, "Y" if punto_en_anillo(p, (0, 0), r_in, r_out) else "N")


def pruebas():
    random.seed(2023)

    # Casos borde
    assert relacion_circulos((0, 0), 3, (0, 0), 3) == -1
    assert interseccion_circulos((0, 0), 3, (0, 0), 3) == []
    assert relacion_circulos((0, 0), 3, (0, 0), 5) == 0          # concéntricos
    assert relacion_circulos((0, 0), 5, (2, 0), 3) == 1          # tangente interior
    assert interseccion_circulos((0, 0), 5, (2, 0), 3) == [(5.0, 0.0)]
    assert interseccion_recta_circulo((0, 5), (1, 5), (0, 0), 5) == [(0.0, 5.0)]
    assert punto_en_anillo((0, 0), (0, 0), 0, 0)
    assert alcance_brazo([7]) == (7, 7) and alcance_brazo([3, 3]) == (0, 6)

    for _ in range(5000):
        c1 = (random.randint(-6, 6), random.randint(-6, 6))
        c2 = (random.randint(-6, 6), random.randint(-6, 6))
        r1, r2 = random.randint(0, 7), random.randint(0, 7)
        # Fuerza bruta: clasificar con la distancia en float (con enteros
        # chicos, d = r1 ± r2 solo si d² es un cuadrado y sqrt es exacta)
        d = math.dist(c1, c2)
        if d == 0 and r1 == r2:
            esperado = -1
        elif d > r1 + r2 or d < abs(r1 - r2):
            esperado = 0
        elif d == r1 + r2 or d == abs(r1 - r2):
            esperado = 1
        else:
            esperado = 2
        assert relacion_circulos(c1, r1, c2, r2) == esperado
        pts = interseccion_circulos(c1, r1, c2, r2)
        assert len(pts) == max(esperado, 0)
        for p in pts:
            assert abs(math.dist(p, c1) - r1) < 1e-6 and abs(math.dist(p, c2) - r2) < 1e-6
        if len(pts) == 2:
            assert math.dist(pts[0], pts[1]) > 1e-9

        a = (random.randint(-6, 6), random.randint(-6, 6))
        b = (random.randint(-6, 6), random.randint(-6, 6))
        if a == b:
            continue
        dist = abs((b[0] - a[0]) * (c1[1] - a[1]) - (b[1] - a[1]) * (c1[0] - a[0])) / math.dist(a, b)
        pts = interseccion_recta_circulo(a, b, c1, r1)
        if abs(dist - r1) > 1e-9:
            assert len(pts) == (2 if dist < r1 else 0)
        else:
            assert len(pts) == 1
        for p in pts:
            assert abs(math.dist(p, c1) - r1) < 1e-6
            assert abs((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) < 1e-6
        if len(pts) == 2:                     # ordenados de a hacia b
            v = (b[0] - a[0], b[1] - a[1])
            assert pts[0][0] * v[0] + pts[0][1] * v[1] < pts[1][0] * v[0] + pts[1][1] * v[1]

    for _ in range(2000):
        ls = [random.randint(1, 10) for _ in range(random.randint(1, 6))]
        # Fuerza bruta: intervalo de distancias alcanzables sección a sección
        lo, hi = 0, 0
        for l in ls:
            if lo <= l <= hi:
                nlo = 0
            else:
                nlo = min(abs(lo - l), abs(hi - l))
            lo, hi = nlo, hi + l
        assert alcance_brazo(ls) == (lo, hi)
        p = (random.randint(-30, 30), random.randint(-30, 30))
        assert punto_en_anillo(p, (0, 0), lo, hi) == (lo <= math.dist(p, (0, 0)) <= hi)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
