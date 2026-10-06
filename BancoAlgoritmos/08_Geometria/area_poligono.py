r"""
Geometría — Área de un polígono: fórmula del zapato («shoelace formula»)
Nivel: Básico
Ejecutar: python area_poligono.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular en O(n) el área de un polígono simple (sin autointersecciones,
    convexo o no) dados sus vértices en orden, saber si está orientado en
    sentido antihorario u horario, y hallar su centroide (centro de masa de
    la lámina).
    Señales en el enunciado: «área del polígono/terreno/lote», «vértices en
    orden», «¿en qué sentido se recorren?», «centro de gravedad»; también
    como pieza dentro de otros algoritmos (envolvente, Pick, recortes).

FUNCIÓN
    area2_con_signo(poli) -> int     DOBLE del área con signo (entero exacto
                                     si las coordenadas son enteras):
                                     > 0 antihorario (CCW), < 0 horario (CW)
    area(poli) -> float              |area2| / 2
    orientar_ccw(poli) -> list       el mismo polígono en sentido antihorario
    centroide(poli) -> (float, float)  centro de masa de la región (área > 0)
    poli: lista de tuplas (x, y) en orden (sin repetir el primero al final).

IDEA Y ALGORITMO
    Triangular «en abanico» desde el ORIGEN: el área con signo del triángulo
    (O, Pi, Pi+1) es cruz(Pi, Pi+1)/2. Sumando sobre todas las aristas, los
    pedazos que quedan fuera del polígono se suman una vez con signo + y una
    vez con signo −, y se cancelan; queda exactamente el área, con signo
    positivo si el recorrido es antihorario.

          P3 _______ P2         2A = Σ (xi·yi+1 − xi+1·yi)
            |       \                 i
            |   +    \  P1      (se cruzan los productos como los
            |_________\/        cordones de un zapato: x con la y
          P4      ·O   P0        siguiente, menos y con la x siguiente)

    Con enteros, 2A es entero exacto; el área real es 2A/2 (termina en .0 o
    .5). Por eso conviene trabajar con area2 e imprimir al final.
    Centroide: cada triángulo (O, Pi, Pi+1) tiene centroide (O + Pi + Pi+1)/3
    y peso su área con signo; el promedio ponderado da
        Cx = Σ (xi + xi+1)·ci / (3·2A),   Cy = Σ (yi + yi+1)·ci / (3·2A),
    con ci = cruz(Pi, Pi+1). (Es el centroide de la REGIÓN, no el promedio
    de los vértices: ese solo coincide en triángulos.)

MACROALGORITMO
    1. s = 0; para i = 0..n−1: j = (i + 1) mod n, s += xi·yj − xj·yi.
    2. s es el doble del área con signo; s > 0 -> CCW, s < 0 -> CW.
    3. Área = |s| / 2.
    4. Centroide: acumular (xi + xj)·ci y (yi + yj)·ci; dividir por 3·s.

COMPLEJIDAD
    O(n) tiempo, O(1) memoria extra. 10^6 vértices en ~0.5 s en Python.

EJEMPLO A MANO
    Polígono en L: (0,0) (4,0) (4,1) (1,1) (1,3) (0,3), antihorario.
      cruces: 0·0−4·0=0, 4·1−4·0=4, 4·1−1·1=3, 1·3−1·1=2, 1·3−0·3=3, 0·0−0·3=0
      2A = 12 -> área 6 (rectángulo 4×1 + rectángulo 1×2). CCW.
      Recorrido al revés: 2A = −12 (CW).
      Centroide, comprobado partiendo la L en dos rectángulos: 4×1 (centro
      (2, 0.5), área 4) y 1×2 (centro (0.5, 2), área 2):
        C = ((4·2 + 2·0.5)/6, (4·0.5 + 2·2)/6) = (1.5, 1.0).

ERRORES TÍPICOS
    - Olvidar cerrar el ciclo (la arista del último vértice al primero).
    - Dividir por 2 con // y perder el .5; o dividir al comienzo y usar
      floats sin necesidad. Guardar 2A como entero.
    - Tomar abs() antes de sumar (da basura en polígonos no convexos).
    - Usar el promedio de los vértices como «centroide» del polígono.
    - Vértices desordenados: la fórmula exige el orden del borde (si solo
      se tienen puntos de un convexo, ordenarlos por ángulo o usar la
      envolvente).

VARIANTES Y RELACIONADOS
    - Área de un triángulo: |cruz(a, b, c)| / 2 (orientacion_ccw.py).
    - Polígonos con autointersecciones: la fórmula da el área «con
      multiplicidad» (regiones contadas por su número de vueltas).
    - Sumas prefijas de cruces: área de una cadena de vértices i..j en O(1)
      (útil para cortes de polígonos).
    - Teorema de Pick: puntos enteros interiores a partir de 2A
      (teorema_pick.py).
    - Envolvente convexa, perímetro y área (envolvente_convexa.py).

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/H - Half the Polygon (zapato con sumas prefijas)
    - ICPC/Colombia 2018/H - Ghost Hunting (doble del área entero, salida
      con .0/.5)
    - ICPC/Colombia 2026/F - Heist (áreas de celdas convexas)
    - CSES «Polygon Area»

VERIFICACIÓN
    - Pruebas: OK en 1500 polígonos «histograma» rectilíneos aleatorios
      (rotados/reflejados al azar) contra conteo de celdas unitarias cuyo
      centro está dentro (par/impar de cruces) y centroide contra la suma
      ponderada de las columnas con Fraction; 1500 polígonos estrellados
      contra la fórmula independiente de los trapecios; triángulos contra
      Herón (python area_poligono.py)
"""
import math
import random
from fractions import Fraction


def area2_con_signo(poli):
    """Doble del área con signo: > 0 antihorario, < 0 horario."""
    s = 0
    n = len(poli)
    for i in range(n):
        x1, y1 = poli[i]
        x2, y2 = poli[(i + 1) % n]          # cerrar el ciclo
        s += x1 * y2 - x2 * y1
    return s


def area(poli):
    return abs(area2_con_signo(poli)) / 2


def orientar_ccw(poli):
    """Devuelve el polígono recorrido en sentido antihorario."""
    return poli[::-1] if area2_con_signo(poli) < 0 else list(poli)


def centroide(poli):
    """Centro de masa de la región poligonal (exige área distinta de 0)."""
    s = sx = sy = 0
    n = len(poli)
    for i in range(n):
        x1, y1 = poli[i]
        x2, y2 = poli[(i + 1) % n]
        c = x1 * y2 - x2 * y1               # doble área (con signo) de O, Pi, Pi+1
        s += c
        sx += (x1 + x2) * c                 # 3·centroide del triángulo · peso
        sy += (y1 + y2) * c
    return (sx / (3 * s), sy / (3 * s))     # los signos se cancelan: vale en CW


def demo():
    L = [(0, 0), (4, 0), (4, 1), (1, 1), (1, 3), (0, 3)]
    print("polígono L:", L)
    print("2A con signo =", area2_con_signo(L), "-> área", area(L), "(CCW)")
    print("al revés: 2A =", area2_con_signo(L[::-1]), "(CW)")
    print("centroide =", centroide(L))                    # (1.5, 1.0)
    print("orientar_ccw(al revés) =", orientar_ccw(L[::-1]))


# ---------------------------------------------------------------- pruebas
def _histograma(alturas):
    """Polígono rectilíneo CCW: columnas [i, i+1] × [0, h_i] (h_i >= 1)."""
    n = len(alturas)
    poli = [(0, 0), (n, 0)]
    for i in range(n - 1, -1, -1):          # subir por la derecha, ir a la izq.
        poli.append((i + 1, alturas[i]))
        poli.append((i, alturas[i]))
    # quitar vértices repetidos consecutivos (no cambian el área)
    limpio = []
    for p in poli:
        if not limpio or limpio[-1] != p:
            limpio.append(p)
    if limpio[0] == limpio[-1]:
        limpio.pop()
    return limpio


def _dentro_paridad(poli, x, y):
    """Fuerza bruta: paridad de cruces de un rayo horizontal hacia +x.

    Se usa solo con (x, y) en centros de celda (medio entero), que nunca
    caen sobre el borde de un polígono rectilíneo de vértices enteros.
    """
    dentro = False
    n = len(poli)
    for i in range(n):
        (x1, y1), (x2, y2) = poli[i], poli[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xc = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xc > x:
                dentro = not dentro
    return dentro


def _estrella(rng, k):
    """Polígono simple estrellado: direcciones distintas ordenadas por ángulo."""
    dirs = set()
    while len(dirs) < k:
        dx, dy = rng.randint(-4, 4), rng.randint(-4, 4)
        if (dx, dy) != (0, 0) and math.gcd(dx, dy) == 1:
            dirs.add((dx, dy))
    dirs = sorted(dirs, key=lambda d: math.atan2(d[1], d[0]))
    angs = [math.atan2(d[1], d[0]) for d in dirs]
    huecos = [angs[i + 1] - angs[i] for i in range(k - 1)] + [angs[0] + 2 * math.pi - angs[-1]]
    if max(huecos) >= math.pi - 1e-12:
        return None                           # el origen no queda dentro: descartar
    escalas = [rng.randint(1, 3) for _ in dirs]           # mismo factor en x e y
    return [(d[0] * k, d[1] * k) for d, k in zip(dirs, escalas)]


def pruebas():
    random.seed(31)
    rng = random.Random(5)

    # Casos borde
    assert area2_con_signo([]) == 0 and area2_con_signo([(3, 4)]) == 0
    assert area2_con_signo([(0, 0), (5, 5)]) == 0
    assert area2_con_signo([(0, 0), (1, 0), (0, 1)]) == 1          # área 0.5
    assert area([(0, 0), (0, 1), (1, 0)]) == 0.5
    assert area2_con_signo([(0, 0), (1, 1), (2, 2)]) == 0           # colineales
    big = 10 ** 9
    assert area2_con_signo([(-big, -big), (big, -big), (big, big), (-big, big)]) == 8 * big * big

    transformaciones = [lambda x, y: (x, y), lambda x, y: (-y, x), lambda x, y: (-x, -y),
                        lambda x, y: (y, -x), lambda x, y: (-x, y), lambda x, y: (x, -y)]
    for _ in range(1500):
        h = [random.randint(1, 6) for _ in range(random.randint(1, 7))]
        poli = _histograma(h)
        f = random.choice(transformaciones)
        dx, dy = random.randint(-5, 5), random.randint(-5, 5)
        poli = [(f(x, y)[0] + dx, f(x, y)[1] + dy) for x, y in poli]
        if random.random() < 0.5:
            poli = poli[::-1]
        r = random.randrange(len(poli))
        poli = poli[r:] + poli[:r]             # rotar el punto de inicio
        # Fuerza bruta: contar celdas unitarias con el centro dentro
        xs, ys = [p[0] for p in poli], [p[1] for p in poli]
        celdas = [(cx, cy) for cx in range(min(xs), max(xs)) for cy in range(min(ys), max(ys))
                  if _dentro_paridad(poli, cx + 0.5, cy + 0.5)]
        assert abs(area2_con_signo(poli)) == 2 * len(celdas)
        assert area(poli) == len(celdas)
        assert area2_con_signo(orientar_ccw(poli)) > 0
        # Centroide = promedio de los centros de las celdas (exacto con Fraction)
        cx = sum(Fraction(2 * c[0] + 1, 2) for c in celdas) / len(celdas)
        cy = sum(Fraction(2 * c[1] + 1, 2) for c in celdas) / len(celdas)
        gx, gy = centroide(poli)
        assert abs(gx - cx) < 1e-9 and abs(gy - cy) < 1e-9

    hechos = 0
    while hechos < 1500:
        poli = _estrella(rng, rng.randint(3, 9))
        if poli is None:
            continue
        hechos += 1
        # Fuerza bruta independiente: fórmula de los trapecios
        # 2A = Σ (x_i − x_{i+1})·(y_i + y_{i+1})
        n = len(poli)
        trap = sum((poli[i][0] - poli[(i + 1) % n][0]) * (poli[i][1] + poli[(i + 1) % n][1])
                   for i in range(n))
        assert area2_con_signo(poli) == trap > 0          # se generan en orden CCW
        assert area2_con_signo(poli[::-1]) == -trap

    for _ in range(1000):
        a, b, c = [(random.randint(-20, 20), random.randint(-20, 20)) for _ in range(3)]
        la, lb, lc = math.dist(b, c), math.dist(a, c), math.dist(a, b)
        s = (la + lb + lc) / 2
        heron = math.sqrt(max(0.0, s * (s - la) * (s - lb) * (s - lc)))
        assert abs(area([a, b, c]) - heron) < 1e-6
        if area2_con_signo([a, b, c]) != 0:      # centroide del triángulo = promedio
            gx, gy = centroide([a, b, c])
            assert abs(gx - (a[0] + b[0] + c[0]) / 3) < 1e-9
            assert abs(gy - (a[1] + b[1] + c[1]) / 3) < 1e-9


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
