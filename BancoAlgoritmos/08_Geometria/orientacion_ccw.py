r"""
Geometría — Orientación de tres puntos y punto sobre segmento («CCW test»)
Nivel: Básico
Ejecutar: python orientacion_ccw.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir si al ir de A a B y luego a C se gira a la izquierda
    (antihorario, CCW), a la derecha (horario, CW) o se sigue derecho
    (colineales). Es la pieza de la que dependen envolventes convexas,
    intersección de segmentos, punto en polígono y casi todo lo demás.
    Señales en el enunciado: «a la izquierda/derecha de», «gira»,
    «colineales», «¿está el punto sobre el segmento/cerca?», «en sentido
    horario».

FUNCIÓN
    cruz(o, a, b) -> int     (a − o)×(b − o): doble del área con signo de oab
    orientacion(a, b, c) -> int   1 si a→b→c gira a la izquierda (CCW),
                                  −1 si gira a la derecha (CW), 0 si colineales
    en_segmento(p, a, b) -> bool  p está sobre el segmento CERRADO [a, b]
                                  (incluye extremos; a == b permitido)
    giros(camino) -> list[int]    orientación en cada vértice interior

IDEA Y ALGORITMO
    cruz(o, a, b) = (ax−ox)(by−oy) − (ay−oy)(bx−ox) es |oa||ob| sen θ, con θ
    el ángulo de oa hacia ob. Su signo es el del seno: positivo si ob está a
    la izquierda de oa.

            c                       c
           /     CCW (> 0)           \      CW (< 0)      a ---- b ---- c
          /                           \                    colineales (= 0)
    a -- b                       a --- b

    Con coordenadas enteras el resultado es EXACTO (Python no desborda), así
    que no hay epsilon: el signo es correcto siempre. Es también el
    determinante | ax ay 1 ; bx by 1 ; cx cy 1 |.
    Punto sobre segmento: p está en [a, b] si y solo si
      (1) es colineal con a y b: cruz(a, b, p) == 0, y
      (2) está «entre» a y b: dentro de la caja min/max de x y de y
          (equivalente: (a − p)·(b − p) <= 0, los vectores hacia los
          extremos apuntan en sentidos opuestos o uno es nulo).
    Solo (1) no basta: p podría estar en la recta pero fuera del segmento.

MACROALGORITMO
    1. Calcular c = cruz(a, b, c) con enteros.
    2. Devolver el signo de c: 1, −1 o 0.
    3. Para «p en [a, b]»: exigir cruz(a, b, p) == 0.
    4. Y además (a − p)·(b − p) <= 0.

COMPLEJIDAD
    O(1), memoria O(1). Del orden de 10^6 llamadas por segundo en Python.

EJEMPLO A MANO
    a = (0, 0), b = (4, 0), c = (2, 3): cruz = 4·3 − 0·2 = 12 > 0 -> CCW.
    c = (2, −3): cruz = −12 -> CW.  c = (6, 0): cruz = 0 -> colineales.
    ¿(6, 0) en [a, b]? colineal pero (a − p)·(b − p) = (−6)(−2) = 12 > 0 -> no.
    ¿(3, 0) en [a, b]? (−3)(1) = −3 <= 0 -> sí.

ERRORES TÍPICOS
    - Restar al revés: cruz(o, a, b) usa (a − o) y (b − o); invertir a y b
      invierte el signo y todo el algoritmo queda «al revés».
    - Usar floats y comparar con == 0: con coordenadas reales hace falta
      epsilon (ver precision_flotantes.py); con enteros, nunca.
    - En en_segmento, olvidar la condición de «entre» (solo colinealidad).
    - En C++/Java el producto puede desbordar int con coordenadas ~10^9:
      usar long long. En Python no hay problema.

VARIANTES Y RELACIONADOS
    - Semiplano estricto vs cerrado: c > 0 (estrictamente a la izquierda) o
      c >= 0 (izquierda o sobre la recta).
    - Envolvente convexa: sacar puntos mientras cruz <= 0
      (envolvente_convexa.py).
    - Intersección de segmentos con 4 orientaciones (interseccion_segmentos.py).
    - Ordenar puntos por ángulo alrededor de un pivote: comparar con cruz.
    - Vectores y productos (vectores_productos.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/G - Guard Deployment (segmentos que tocan
      rectángulos, punto dentro de un convexo: todo con orientaciones)
    - ICPC/Colombia 2018/H - Ghost Hunting (envolvente con cruces enteros)
    - CSES «Point Location Test» (exactamente este archivo)

VERIFICACIÓN
    - Pruebas: OK en 20000 tripletas aleatorias contra el determinante 3×3
      desarrollado por cofactores, y en_segmento contra la enumeración de
      todos los puntos enteros del segmento (paso (dx, dy)/gcd)
      (python orientacion_ccw.py)
"""
import math
import random


def cruz(o, a, b):
    """(a − o) × (b − o): > 0 si o→a→b gira a la izquierda (CCW)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def orientacion(a, b, c):
    """1 = CCW (izquierda), −1 = CW (derecha), 0 = colineales."""
    v = cruz(a, b, c)
    return (v > 0) - (v < 0)


def en_segmento(p, a, b):
    """¿p está sobre el segmento cerrado [a, b]? Exacto con enteros."""
    if cruz(a, b, p) != 0:
        return False                    # no está ni en la recta
    # (a − p)·(b − p) <= 0  <=>  p está entre a y b (o es un extremo)
    return (a[0] - p[0]) * (b[0] - p[0]) + (a[1] - p[1]) * (b[1] - p[1]) <= 0


def giros(camino):
    """Orientación del giro en cada vértice interior de un camino."""
    return [orientacion(camino[i - 1], camino[i], camino[i + 1])
            for i in range(1, len(camino) - 1)]


def demo():
    a, b = (0, 0), (4, 0)
    for c in [(2, 3), (2, -3), (6, 0)]:
        nombre = {1: "CCW (izquierda)", -1: "CW (derecha)", 0: "colineales"}
        print(a, b, c, "->", nombre[orientacion(a, b, c)], " cruz =", cruz(a, b, c))
    print("(6,0) en [a,b]?", en_segmento((6, 0), a, b))     # False
    print("(3,0) en [a,b]?", en_segmento((3, 0), a, b))     # True
    print("giros del camino (0,0)(2,0)(3,1)(3,3)(2,2):",
          giros([(0, 0), (2, 0), (3, 1), (3, 3), (2, 2)]))   # [1, 1, 1]


def pruebas():
    random.seed(7)

    def det3(a, b, c):
        # Fuerza bruta: determinante 3x3 de [[ax, ay, 1], [bx, by, 1], [cx, cy, 1]]
        # desarrollado por cofactores de la primera fila.
        return (a[0] * (b[1] * 1 - 1 * c[1])
                - a[1] * (b[0] * 1 - 1 * c[0])
                + 1 * (b[0] * c[1] - b[1] * c[0]))

    def en_segmento_bruto(p, a, b):
        # Todos los puntos enteros del segmento: a + k·(dx/g, dy/g), k = 0..g
        dx, dy = b[0] - a[0], b[1] - a[1]
        g = math.gcd(dx, dy)
        if g == 0:
            return p == a
        sx, sy = dx // g, dy // g
        return any((a[0] + k * sx, a[1] + k * sy) == p for k in range(g + 1))

    # Casos borde
    assert orientacion((0, 0), (0, 0), (0, 0)) == 0
    assert en_segmento((1, 1), (1, 1), (1, 1))
    assert not en_segmento((1, 2), (1, 1), (1, 1))
    assert en_segmento((0, 0), (0, 0), (5, 5)) and en_segmento((5, 5), (0, 0), (5, 5))
    big = 10 ** 18
    assert orientacion((-big, -big), (big, big), (big, big - 1)) == -1

    for _ in range(20000):
        r = random.choice([2, 4, 30])
        a, b, c, p = [(random.randint(-r, r), random.randint(-r, r)) for _ in range(4)]
        d = det3(a, b, c)
        assert orientacion(a, b, c) == (d > 0) - (d < 0)
        # permutar los puntos: par conserva el signo, impar lo invierte
        assert orientacion(b, c, a) == orientacion(a, b, c) == -orientacion(b, a, c)
        assert en_segmento(p, a, b) == en_segmento_bruto(p, a, b)
        assert en_segmento(p, a, b) == en_segmento(p, b, a)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
