r"""
Geometría — Envolvente convexa: cadena monótona de Andrew («convex hull, monotone chain»)
Nivel: Intermedio
Ejecutar: python envolvente_convexa.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Hallar el menor polígono convexo que contiene a un conjunto de puntos
    (la «liga elástica» que los rodea), en O(n log n). Es el primer paso de
    muchísimos problemas: perímetro mínimo de una cerca, diámetro, triángulo
    de área máxima, separar dos conjuntos, capas convexas…
    Señales en el enunciado: «cerca de longitud mínima que encierre todos
    los árboles», «polígono convexo que contenga», «puntos extremos», «los
    puntos del borde», o cualquier máximo/mínimo que solo puede alcanzarse
    en puntos «de afuera».

FUNCIÓN
    envolvente(puntos, colineales=False) -> list[(x, y)]
        Vértices de la envolvente en sentido ANTIHORARIO, empezando por el
        menor (x, y). Duplicados permitidos en la entrada.
        colineales=False: solo las esquinas (sin puntos en medio de un lado).
        colineales=True : TODOS los puntos del borde, en orden.
        Casos degenerados: 1 punto -> [p]; todos colineales -> los 2 extremos
        (o todos, en orden, con colineales=True).
    perimetro(h) -> float,  area2(h) -> int (doble del área, exacto)

IDEA Y ALGORITMO
    Ordenar los puntos por (x, y). La envolvente se parte en la cadena
    INFERIOR (de izquierda a derecha, por abajo) y la SUPERIOR (de derecha a
    izquierda, por arriba). Cada cadena se construye con una pila: al
    recorrer en orden, la cadena debe girar siempre a la IZQUIERDA; si el
    nuevo punto p hace que los dos últimos de la pila y p giren a la derecha
    (cruz <= 0), el último de la pila NO puede ser vértice (queda dentro del
    triángulo formado) y se saca. Repetir y luego apilar p.

          superior:  <-----------
              . ---- . ---- .
            /                  \            Al llegar p, si (a, b, p) gira
           .        .     .     .           a la derecha, b queda «hundido»
            \                  /            y se elimina.
              . ---- . ---- .
          inferior:  ----------->

    Por qué es correcto: el primer y el último punto del orden (x, y) son
    vértices; entre ellos, la cadena inferior es la «convexa por abajo»
    más alta posible, y la pila mantiene el invariante «todos los giros son
    a la izquierda»; un punto sacado está dentro de un triángulo de puntos
    del conjunto, así que nunca es vértice. Cada punto entra y sale de la
    pila a lo sumo una vez: O(n) después de ordenar.
    Colineales: con «sacar si cruz <= 0» los puntos en medio de un lado se
    eliminan; con «sacar si cruz < 0» se conservan (giro de 0 se permite).
    Ojo con el caso todos colineales en esa versión: la cadena inferior y
    la superior recorren los mismos puntos en sentidos opuestos, y se
    duplicarían: se detecta y se devuelven los puntos ordenados una vez.
    Todo con productos cruz enteros: exacto.

MACROALGORITMO
    1. Quitar duplicados y ordenar por (x, y). Si hay <= 1 punto, devolverlo.
    2. Cadena inferior: para p en orden, mientras haya >= 2 en la pila y
       cruz(pila[-2], pila[-1], p) <= 0 (o < 0 con colineales): sacar.
       Apilar p.
    3. Cadena superior: lo mismo recorriendo en orden inverso.
    4. Envolvente = inferior sin su último + superior sin su último (el
       último de cada una es el primero de la otra).
    5. Perímetro = suma de |h[i+1] − h[i]|; área con la fórmula del zapato.

COMPLEJIDAD
    O(n log n) por el ordenamiento; O(n) el resto. Memoria O(n).
    En Python, 10^5 puntos en ~0.3 s; 10^6 en unos 3–4 s.

EJEMPLO A MANO
    Puntos: (0,0) (2,0) (4,0) (1,1) (2,2) (4,4) (0,4) (3,1).
    Orden: (0,0) (0,4) (1,1) (2,0) (2,2) (3,1) (4,0) (4,4).
    Inferior (pila):
      (0,0) (0,4)                    llega (1,1): cruz = −4 -> saca (0,4)
      (0,0) (1,1)                    llega (2,0): cruz = −2 -> saca (1,1)
      (0,0) (2,0) (2,2)              llega (3,1): cruz = −2 -> saca (2,2)
      (0,0) (2,0) (3,1)              llega (4,0): saca (3,1) (cruz −2) y
                                     (2,0) (cruz 0: colineal)
      (0,0) (4,0) (4,4)              = cadena inferior.
    Superior (de derecha a izquierda): (4,4) (0,4) (0,0).
    Envolvente: (0,0) (4,0) (4,4) (0,4); perímetro 16, área 16.
    Con colineales=True: (0,0) (2,0) (4,0) (4,4) (0,4).

ERRORES TÍPICOS
    - No quitar duplicados: aparecen giros de cruz 0 «falsos» y vértices
      repetidos (sobre todo en la versión con colineales).
    - Usar < en vez de <= (o al revés) sin querer: cambia si se conservan
      los puntos colineales del borde.
    - Versión con colineales y todos los puntos sobre una recta: puntos
      repetidos en la salida.
    - Olvidar los casos con 1 o 2 puntos (o todos iguales) antes de usar la
      envolvente como polígono (área 0, no hay «lados»).
    - Usar floats en cruz cuando las coordenadas son enteras.

VARIANTES Y RELACIONADOS
    - Graham scan (ordenar por ángulo alrededor del punto más bajo):
      misma complejidad, más casos borde con ángulos iguales.
    - Diámetro y triángulo de área máxima sobre la envolvente
      (rotating_calipers.py); separar dos conjuntos (eje_separador.py).
    - Punto en el convexo en O(log n) (punto_en_convexo_logn.py).
    - Repetir la envolvente quitando el borde: capas_convexas.py.
    - Envolvente dinámica / trick de la envolvente convexa en DP
      (convex hull trick) usa la misma idea de pila con cruces.

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/G - Guard Deployment (cerca = envolvente, perímetro)
    - ICPC/Colombia 2017/F - Fish (envolventes de dos conjuntos)
    - ICPC/Colombia 2018/H - Ghost Hunting (envolvente + dos punteros)
    - ICPC/Colombia 2026/C - Into the Onion (con colineales, repetida)
    - CSES «Convex Hull» (pide los puntos del borde: colineales=True)

VERIFICACIÓN
    - Pruebas: OK en 3000 conjuntos aleatorios pequeños (muchos duplicados y
      colineales) contra fuerza bruta: p es vértice si no está en ningún
      triángulo/segmento cerrado de otros puntos; p está en el borde si
      existe una recta por p y otro punto con todos de un mismo lado. Se
      verifica además el orden antihorario y la convexidad, y área/perímetro
      contra un rectángulo y un triángulo conocidos (python envolvente_convexa.py)
"""
import math
import random


def cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def envolvente(puntos, colineales=False):
    """Cadena monótona de Andrew. Vértices en sentido antihorario."""
    pts = sorted(set(puntos))
    if len(pts) <= 1:
        return pts
    # Con colineales=False se saca con cruz <= 0 (giro a la derecha o recto);
    # con colineales=True solo con cruz < 0 (los rectos se quedan).
    lim = -1 if colineales else 0

    def cadena(secuencia):
        pila = []
        for p in secuencia:
            while len(pila) >= 2 and cruz(pila[-2], pila[-1], p) <= lim:
                pila.pop()
            pila.append(p)
        return pila

    inferior = cadena(pts)
    superior = cadena(reversed(pts))
    if colineales and len(inferior) == len(pts) and len(superior) == len(pts):
        # Solo pasa si TODOS son colineales: el borde es el segmento entero.
        if all(cruz(pts[0], pts[-1], p) == 0 for p in pts):
            return pts
    return inferior[:-1] + superior[:-1]


def perimetro(h):
    n = len(h)
    if n <= 1:
        return 0.0
    return sum(math.dist(h[i], h[(i + 1) % n]) for i in range(n))


def area2(h):
    """Doble del área (fórmula del zapato), entero exacto."""
    n = len(h)
    return sum(h[i][0] * h[(i + 1) % n][1] - h[(i + 1) % n][0] * h[i][1] for i in range(n))


def demo():
    pts = [(0, 0), (2, 0), (4, 0), (1, 1), (2, 2), (4, 4), (0, 4), (3, 1)]
    h = envolvente(pts)
    print("puntos:", pts)
    print("envolvente:", h)                                  # (0,0) (4,0) (4,4) (0,4)
    print("perímetro =", perimetro(h), " área =", area2(h) / 2)   # 16.0 16.0
    print("con colineales:", envolvente(pts, colineales=True))
    print("todos colineales:", envolvente([(2, 2), (0, 0), (1, 1), (3, 3)]),
          envolvente([(2, 2), (0, 0), (1, 1), (3, 3)], colineales=True))


def _en_triangulo_cerrado(p, a, b, c):
    """p en el triángulo cerrado abc (que puede ser degenerado)."""
    if cruz(a, b, c) == 0:
        # degenerado: p debe estar en alguno de los segmentos
        for u, v in ((a, b), (b, c), (a, c)):
            if cruz(u, v, p) == 0 and min(u[0], v[0]) <= p[0] <= max(u[0], v[0]) \
                    and min(u[1], v[1]) <= p[1] <= max(u[1], v[1]):
                return True
        return False
    s1, s2, s3 = cruz(a, b, p), cruz(b, c, p), cruz(c, a, p)
    return (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)


def pruebas():
    random.seed(4)

    # Casos borde
    assert envolvente([]) == [] and envolvente([(3, 3), (3, 3)]) == [(3, 3)]
    assert envolvente([(1, 1), (0, 0)]) == [(0, 0), (1, 1)]
    assert envolvente([(0, 0), (1, 1), (2, 2)]) == [(0, 0), (2, 2)]
    assert envolvente([(0, 0), (2, 2), (1, 1)], colineales=True) == [(0, 0), (1, 1), (2, 2)]
    assert envolvente([(0, 0), (0, 2), (0, 1)], colineales=True) == [(0, 0), (0, 1), (0, 2)]
    cuadrado = [(x, y) for x in range(3) for y in range(3)]
    assert envolvente(cuadrado) == [(0, 0), (2, 0), (2, 2), (0, 2)]
    assert envolvente(cuadrado, True) == [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2),
                                          (1, 2), (0, 2), (0, 1)]
    assert area2(envolvente(cuadrado)) == 8 and perimetro(envolvente(cuadrado)) == 8.0
    assert perimetro(envolvente([(0, 0), (3, 0), (0, 4)])) == 12.0

    for _ in range(3000):
        r = random.choice([1, 2, 3, 5])
        n = random.randint(1, 9)
        pts = [(random.randint(-r, r), random.randint(-r, r)) for _ in range(n)]
        u = sorted(set(pts))
        # Fuerza bruta de vértices: p no está en ningún triángulo (o segmento)
        # cerrado formado por otros puntos.
        otros = lambda p: [q for q in u if q != p]
        vertices = set()
        for p in u:
            o = otros(p)
            atrapado = any(_en_triangulo_cerrado(p, o[i], o[j], o[k])
                           for i in range(len(o)) for j in range(i, len(o))
                           for k in range(j, len(o)))
            if not atrapado:
                vertices.add(p)
        # Fuerza bruta del borde: existe q != p con todos de un lado cerrado de pq
        borde = set()
        for p in u:
            if len(u) == 1:
                borde.add(p)
            for q in otros(p):
                s = [cruz(p, q, w) for w in u]
                if all(v >= 0 for v in s) or all(v <= 0 for v in s):
                    borde.add(p)
                    break

        h = envolvente(pts)
        hc = envolvente(pts, colineales=True)
        assert set(h) == vertices and len(h) == len(vertices)
        assert set(hc) == borde and len(hc) == len(borde)
        assert h[0] == u[0] and hc[0] == u[0]
        # Orden antihorario y convexo: cruces > 0 (estricta) / >= 0 (colineales)
        if len(h) >= 3:
            m = len(h)
            assert all(cruz(h[i], h[(i + 1) % m], h[(i + 2) % m]) > 0 for i in range(m))
            m = len(hc)
            assert all(cruz(hc[i], hc[(i + 1) % m], hc[(i + 2) % m]) >= 0 for i in range(m))
            assert area2(hc) == area2(h) > 0
            assert abs(perimetro(hc) - perimetro(h)) < 1e-9


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
