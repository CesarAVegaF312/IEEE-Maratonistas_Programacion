r"""
Geometría — Punto en polígono: dentro, fuera o borde («ray casting / winding number»)
Nivel: Intermedio
Ejecutar: python punto_en_poligono.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir si un punto está dentro, fuera o sobre el borde de un polígono
    simple (convexo o NO convexo) en O(n). Para polígonos convexos y muchas
    consultas hay una versión O(log n) (punto_en_convexo_logn.py).
    Señales en el enunciado: «¿el punto está dentro del terreno/zona?»,
    «cuántos puntos quedan dentro», polígono dado por sus vértices en orden,
    distinción explícita de los puntos «sobre la cerca».

FUNCIÓN
    punto_en_poligono(poli, p) -> int
        1 si p está estrictamente dentro, 0 si está en el borde, −1 si fuera.
        poli: lista de tuplas (x, y) enteras en orden (CW o CCW), simple.
    numero_de_vueltas(poli, p) -> int
        Winding number: cuántas veces el borde da la vuelta alrededor de p
        (±1 dentro de un polígono simple, 0 fuera). p no debe estar en el
        borde. Sirve también para polígonos que se cruzan a sí mismos.

IDEA Y ALGORITMO
    RAY CASTING: lanzar un rayo horizontal desde p hacia la derecha y contar
    cuántas aristas cruza. Cada cruce alterna dentro/fuera, así que un
    número IMPAR de cruces significa «dentro» (teorema de la curva de
    Jordan: el borde separa el plano en dos regiones).

               _________
              |    __   |          p ·-------x---x------x--->  3 cruces
              |   |  |  |                                       -> dentro
         p ·--x---x  x--x-->

    El problema son los casos en que el rayo toca un vértice o corre sobre
    una arista horizontal. Se resuelven con la regla SEMIABIERTA: una arista
    (a, b) cuenta si y solo si (ay > py) != (by > py), es decir, uno de sus
    extremos está estrictamente arriba del rayo y el otro no. Así un
    vértice donde el borde «atraviesa» el rayo se cuenta exactamente una
    vez, un vértice que solo lo toca («pico») se cuenta 0 o 2 veces, y las
    aristas horizontales nunca cuentan. Todo correcto en paridad.
    Para saber si el cruce está a la DERECHA de p sin dividir, se mira el
    lado: si la arista sube (by > ay), el cruce está a la derecha de p
    exactamente cuando p está a la IZQUIERDA de a→b (cruz(a, b, p) > 0); si
    baja, cuando cruz(a, b, p) < 0. Todo con enteros: exacto.
    Antes se revisa si p está sobre alguna arista (borde -> 0).
    WINDING NUMBER: mismo recorrido, pero en vez de alternar se suma +1 si
    una arista que sube pasa a la derecha de p y −1 si una que baja lo hace.
    En polígonos simples |vueltas| = 1 dentro y 0 fuera; en polígonos que se
    cruzan da cuántas veces se rodea p (la paridad sería la regla even-odd).

MACROALGORITMO
    1. Para cada arista (a, b) del polígono (incluida la que cierra):
    2.   Si p está sobre el segmento [a, b] -> devolver 0 (borde).
    3.   Si (ay > py) != (by > py) (la arista cruza la altura de p):
    4.     c = cruz(a, b, p); si (c > 0) == (by > ay): el cruce está a la
           derecha de p -> alternar «dentro».
    5. Devolver 1 si dentro, −1 si no.

COMPLEJIDAD
    O(n) por consulta, O(1) memoria. Con n·q hasta ~10^7 en Python (~5 s es
    el límite); para muchas consultas en un convexo usar O(log n).

EJEMPLO A MANO
    Polígono en U: (0,0) (6,0) (6,4) (4,4) (4,2) (2,2) (2,4) (0,4).
    p = (3, 3) (en el hueco de la U): rayo y = 3 hacia la derecha cruza
      (6,0)-(6,4) en x=6 (derecha) y (4,4)-(4,2) en x=4 (derecha):
      2 cruces -> fuera (−1).
    p = (1, 3): cruza x=2, x=4, x=6 -> 3 -> dentro (1).
    p = (3, 2): está sobre la arista (4,2)-(2,2) -> borde (0).
    p = (1, 0): rayo sobre la arista horizontal de abajo, pero primero se
      detecta que está en el borde -> 0.

ERRORES TÍPICOS
    - Contar dos veces un vértice que el rayo atraviesa (usar >= en ambos
      extremos) o no contarlo: la regla semiabierta lo arregla.
    - Calcular la x del cruce con división de floats y comparar sin cuidado;
      con el signo de cruz es exacto.
    - Olvidar el caso «borde» cuando el enunciado lo distingue.
    - Usar el algoritmo «todos los cruces del mismo signo» (solo vale para
      convexos) en un polígono cóncavo.

VARIANTES Y RELACIONADOS
    - Polígono convexo y muchas consultas: O(log n)
      (punto_en_convexo_logn.py).
    - Orientación y punto sobre segmento (orientacion_ccw.py).
    - Contar puntos enteros dentro de un polígono sin recorrerlos: Pick
      (teorema_pick.py).
    - Regla par/impar (even-odd) vs. no-cero (nonzero) en polígonos que se
      cruzan: dan resultados distintos en las zonas rodeadas dos veces.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/H - Half the Polygon (paridad de cruces sobre una
      recta para saber qué tramos de una cuerda son interiores)
    - CSES «Point in Polygon» (exactamente este archivo)

VERIFICACIÓN
    - Pruebas: OK en 600 polígonos simples aleatorios (estrellados no
      convexos y «histogramas» rectilíneos, que fuerzan rayos sobre
      vértices y aristas horizontales) consultando todos los puntos enteros
      de su caja (~90000 consultas) contra una fuerza bruta independiente:
      borde = enumeración de los puntos enteros de cada arista; dentro =
      suma de ángulos atan2 (≈ ±2π) (python punto_en_poligono.py)
"""
import math
import random


def cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def en_segmento(p, a, b):
    """¿p está en el segmento cerrado [a, b]?"""
    return (cruz(a, b, p) == 0 and
            (a[0] - p[0]) * (b[0] - p[0]) + (a[1] - p[1]) * (b[1] - p[1]) <= 0)


def punto_en_poligono(poli, p):
    """1 dentro, 0 en el borde, −1 fuera. Polígono simple, coordenadas enteras."""
    n = len(poli)
    dentro = False
    py = p[1]
    for i in range(n):
        a, b = poli[i], poli[(i + 1) % n]
        if en_segmento(p, a, b):
            return 0
        # Regla semiabierta: la arista cruza la horizontal y = py
        if (a[1] > py) != (b[1] > py):
            c = cruz(a, b, p)
            # Sube y p a su izquierda, o baja y p a su derecha: el cruce
            # está a la derecha de p.
            if (c > 0) == (b[1] > a[1]):
                dentro = not dentro
    return 1 if dentro else -1


def numero_de_vueltas(poli, p):
    """Winding number de poli alrededor de p (p fuera del borde)."""
    n = len(poli)
    w = 0
    for i in range(n):
        a, b = poli[i], poli[(i + 1) % n]
        if a[1] <= p[1] < b[1] and cruz(a, b, p) > 0:
            w += 1                      # arista que sube, pasa a la derecha de p
        elif b[1] <= p[1] < a[1] and cruz(a, b, p) < 0:
            w -= 1                      # arista que baja, pasa a la derecha de p
    return w


def demo():
    U = [(0, 0), (6, 0), (6, 4), (4, 4), (4, 2), (2, 2), (2, 4), (0, 4)]
    print("polígono U:", U)
    nombres = {1: "dentro", 0: "borde", -1: "fuera"}
    for p in [(3, 3), (1, 3), (3, 2), (1, 0), (7, 2), (5, 1)]:
        print(p, "->", nombres[punto_en_poligono(U, p)])
    print("vueltas alrededor de (1, 3):", numero_de_vueltas(U, (1, 3)))      # 1 (CCW)
    print("vueltas, polígono al revés:", numero_de_vueltas(U[::-1], (1, 3)))  # -1


# ---------------------------------------------------------------- pruebas
def _estrella(rng, k, r):
    """Polígono simple estrellado (no convexo en general), orden CCW."""
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


def _histograma(alturas):
    n = len(alturas)
    poli = [(0, 0), (n, 0)]
    for i in range(n - 1, -1, -1):
        poli.append((i + 1, alturas[i]))
        poli.append((i, alturas[i]))
    limpio = []
    for p in poli:
        if not limpio or limpio[-1] != p:
            limpio.append(p)
    if limpio[0] == limpio[-1]:
        limpio.pop()
    return limpio


def _bruto(poli, p):
    # Borde: p es uno de los puntos enteros de alguna arista
    n = len(poli)
    for i in range(n):
        a, b = poli[i], poli[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        g = math.gcd(dx, dy)
        for k in range(g + 1):
            if (a[0] + k * dx // g, a[1] + k * dy // g) == p:
                return 0
    # Dentro: la suma de ángulos vistos desde p es ±2π (fuera: 0)
    total = 0.0
    for i in range(n):
        a, b = poli[i], poli[(i + 1) % n]
        u = (a[0] - p[0], a[1] - p[1])
        v = (b[0] - p[0], b[1] - p[1])
        total += math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1])
    return 1 if abs(total) > math.pi else -1


def pruebas():
    random.seed(11)
    rng = random.Random(3)

    # Casos borde: triángulo, vértices, punto lejano
    T = [(0, 0), (4, 0), (0, 4)]
    assert punto_en_poligono(T, (0, 0)) == 0 and punto_en_poligono(T, (2, 2)) == 0
    assert punto_en_poligono(T, (1, 1)) == 1 and punto_en_poligono(T, (3, 3)) == -1
    assert punto_en_poligono(T, (-1, 0)) == -1 and punto_en_poligono(T, (5, 0)) == -1
    assert punto_en_poligono(T[::-1], (1, 1)) == 1
    big = 10 ** 12
    assert punto_en_poligono([(0, 0), (big, 1), (0, 2)], (big - 1, 1)) == 1

    consultas = 0
    poligonos = 0
    while poligonos < 600:
        if poligonos % 2 == 0:
            poli = _estrella(rng, rng.randint(3, 9), rng.randint(1, 4))
            if poli is None:
                continue
        else:
            poli = _histograma([random.randint(1, 5) for _ in range(random.randint(1, 6))])
            if random.random() < 0.5:
                poli = [(y, x) for x, y in poli]          # reflejar: queda CW
        poligonos += 1
        xs, ys = [q[0] for q in poli], [q[1] for q in poli]
        sentido = 1 if sum(cruz((0, 0), poli[i], poli[(i + 1) % len(poli)])
                           for i in range(len(poli))) > 0 else -1
        for x in range(min(xs) - 1, max(xs) + 2):
            for y in range(min(ys) - 1, max(ys) + 2):
                p = (x, y)
                esperado = _bruto(poli, p)
                assert punto_en_poligono(poli, p) == esperado, (poli, p)
                if esperado != 0:
                    w = numero_de_vueltas(poli, p)
                    assert w == (sentido if esperado == 1 else 0)
                consultas += 1
    assert consultas > 80000


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
