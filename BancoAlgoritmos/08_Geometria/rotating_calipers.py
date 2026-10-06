r"""
Geometría — Calibradores rotatorios: diámetro y triángulo de área máxima («rotating calipers»)
Nivel: Avanzado
Ejecutar: python rotating_calipers.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Resolver problemas de «los puntos más alejados» sobre un conjunto de
    puntos recorriendo su envolvente convexa con dos (o tres) punteros que
    solo avanzan: el DIÁMETRO (par de puntos más lejanos) en O(n log n) y el
    TRIÁNGULO DE ÁREA MÁXIMA con vértices en el conjunto en O(n log n + h²).
    Señales en el enunciado: «máxima distancia entre dos puntos» con n hasta
    10^5 (O(n²) no alcanza), «ancho mínimo», «triángulo/cuadrilátero de área
    máxima con vértices en los puntos», «rectángulo mínimo que los encierra».

FUNCIÓN
    envolvente(puntos) -> list   (copiada: Andrew, sin colineales, CCW)
    diametro2(puntos) -> (int, (p, q))
        Mayor distancia AL CUADRADO entre dos puntos (exacta) y el par.
        Con un solo punto distinto devuelve (0, (p, p)).
    triangulo_max2(puntos) -> int
        DOBLE del área máxima de un triángulo con vértices en los puntos
        (0 si todos son colineales o hay menos de 3 distintos).

IDEA Y ALGORITMO
    1) Los puntos óptimos están en la envolvente: la distancia a un punto
       fijo y el área (con dos vértices fijos) son funciones convexas en el
       tercer punto, y una función convexa sobre un polígono alcanza su
       máximo en un vértice.
    2) DIÁMETRO. Para cada arista (h[i], h[i+1]) de la envolvente, el
       vértice más lejano de esa arista (su «antípoda») es el que maximiza
       el área del triángulo (h[i], h[i+1], h[j]). Al avanzar i en sentido
       antihorario, la antípoda j también avanza (nunca retrocede): por eso
       basta un puntero j que da una sola vuelta. Los pares (vértice,
       antípoda) se llaman antipodales y el diámetro es uno de ellos.

              h[j]  <- calibrador paralelo a la arista, del otro lado
          .--------.
         /          \          Se «rota» la arista i y el calibrador
        /            \         opuesto avanza j mientras el área
        '------------'         (h[i], h[i+1], h[j+1]) no baje.
      h[i]  ======  h[i+1]     <- calibrador apoyado en la arista i

    3) TRIÁNGULO MÁXIMO. Fijado i, para j = i+1, i+2, … el k óptimo (el que
       maximiza el área (i, j, k) con k > j) es unimodal en k (es la
       distancia de h[k] a la recta i–j, que sobre un arco convexo sube y
       luego baja) y no retrocede cuando j avanza. Así, para cada i, j y k
       solo avanzan: O(h) por i y O(h²) en total.
       (El famoso algoritmo O(n) de «tres punteros rotando» es INCORRECTO en
       algunos polígonos —se publicó y luego se refutó—; esta versión O(h²)
       sí es correcta.)
    Todo con productos cruz y distancias al cuadrado enteras: exacto.

MACROALGORITMO
    Diámetro:
    1. h = envolvente sin colineales; si h tiene 1 o 2 puntos, responder directo.
    2. j = 1. Para cada i: mientras área(h[i], h[i+1], h[j+1]) >
       área(h[i], h[i+1], h[j]), avanzar j (circular).
    3. Actualizar con dist²(h[i], h[j]) y dist²(h[i+1], h[j]).
    Triángulo máximo:
    4. Para cada i: k = i + 2; para j = i+1 .. h−2: k = max(k, j+1);
       avanzar k mientras área(i, j, k+1) >= área(i, j, k); actualizar.

COMPLEJIDAD
    Diámetro: O(n log n) por la envolvente + O(h) el recorrido.
    Triángulo: O(n log n + h²). En Python h = 2000 (todos en posición
    convexa) tarda ~1 s; con puntos aleatorios h es pequeño (~O(log n)).
    Memoria O(n).

EJEMPLO A MANO
    Puntos (0,0) (4,0) (5,2) (3,5) (0,3) (2,2):
    Envolvente: (0,0) (4,0) (5,2) (3,5) (0,3)  [(2,2) queda dentro].
    Diámetro: arista (0,0)-(4,0): j avanza hasta (3,5) (dobles áreas 8, 20, luego 12):
      candidatos dist²((0,0),(3,5)) = 34, dist²((4,0),(3,5)) = 26; …
      al final el máximo es 34 = dist²((0,0),(3,5)) -> diámetro √34 ≈ 5.83.
    Triángulo máximo: (0,0) (5,2) (3,5)? 2A = 5·5 − 2·3 = 19;
      (0,0) (4,0) (3,5): 2A = 20 <- máximo -> área 10.

ERRORES TÍPICOS
    - Usar la envolvente CON puntos colineales: aristas de largo/área 0
      pueden detener el puntero antes de tiempo.
    - Olvidar los casos con 1 o 2 puntos (o todos colineales): la
      envolvente tiene < 3 vértices.
    - Comparar con >= en el diámetro (puede dar vueltas infinitas si todos
      los puntos tienen el mismo área, p. ej. en un rectángulo): avanzar
      solo si el área sube estrictamente.
    - Implementar el triángulo máximo con el O(n) de tres punteros
      publicado en 1979 (Dobkin–Snyder): es incorrecto.
    - Sacar sqrt antes de comparar: comparar distancias al cuadrado.

VARIANTES Y RELACIONADOS
    - Ancho mínimo (menor distancia entre dos rectas paralelas que
      encierran los puntos): para cada arista, la distancia a su antípoda;
      tomar el mínimo.
    - Rectángulo de área/perímetro mínimo que encierra los puntos: 4
      calibradores (uno por lado).
    - Distancia máxima entre dos polígonos convexos.
    - Envolvente (envolvente_convexa.py), par más cercano (par_mas_cercano.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/H - Ghost Hunting (triángulo de área máxima con
      dos punteros sobre la envolvente, N <= 2000)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta O(n²) (diámetro) y O(n³) (triángulo)
      en 1500 conjuntos aleatorios pequeños (duplicados, colineales) y 200
      conjuntos de hasta 40 puntos en posición casi convexa (sobre elipses
      redondeadas a enteros), donde la envolvente es grande
      (python rotating_calipers.py)
"""
import math
import random


def cruz(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def dist2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def envolvente(puntos):
    """Andrew, sin colineales, sentido antihorario."""
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


def diametro2(puntos):
    """(mayor distancia², (p, q)) con calibradores rotatorios."""
    h = envolvente(puntos)
    n = len(h)
    if n == 1:
        return 0, (h[0], h[0])
    if n == 2:
        return dist2(h[0], h[1]), (h[0], h[1])
    mejor, par = -1, None
    j = 1
    for i in range(n):
        a, b = h[i], h[(i + 1) % n]
        # Avanzar la antípoda mientras el área con la arista (a, b) CREZCA.
        while cruz(a, b, h[(j + 1) % n]) > cruz(a, b, h[j]):
            j = (j + 1) % n
        for p in (a, b):
            d = dist2(p, h[j])
            if d > mejor:
                mejor, par = d, (p, h[j])
    return mejor, par


def triangulo_max2(puntos):
    """Doble del área del mayor triángulo con vértices en los puntos."""
    P = envolvente(puntos)
    h = len(P)
    if h < 3:
        return 0
    mejor = 0
    for i in range(h - 2):
        k = i + 2
        for j in range(i + 1, h - 1):
            if k <= j:
                k = j + 1
            # P es antihorario y k está «después» de j: el área es positiva.
            actual = cruz(P[i], P[j], P[k])
            while k + 1 < h:
                sig = cruz(P[i], P[j], P[k + 1])
                if sig < actual:          # unimodal: empezó a bajar
                    break
                actual = sig
                k += 1
            if actual > mejor:
                mejor = actual
    return mejor


def demo():
    pts = [(0, 0), (4, 0), (5, 2), (3, 5), (0, 3), (2, 2)]
    print("puntos:", pts)
    print("envolvente:", envolvente(pts))
    d2, par = diametro2(pts)
    print("diámetro² =", d2, "entre", par, "-> diámetro = %.4f" % math.sqrt(d2))  # 34
    t2 = triangulo_max2(pts)
    print("triángulo máximo: 2A =", t2, "-> área =", t2 / 2)                     # 20 -> 10


def pruebas():
    random.seed(2018)

    def bruto_diam(pts):
        return max(dist2(p, q) for p in pts for q in pts)

    def bruto_tri(pts):
        u = list(set(pts))
        n = len(u)
        return max([abs(cruz(u[i], u[j], u[k])) for i in range(n)
                    for j in range(i + 1, n) for k in range(j + 1, n)], default=0)

    # Casos borde
    assert diametro2([(3, 3)]) == (0, ((3, 3), (3, 3)))
    assert diametro2([(0, 0), (0, 0), (1, 1)])[0] == 2
    assert diametro2([(0, 0), (1, 1), (2, 2), (5, 5)])[0] == 50
    assert triangulo_max2([(0, 0), (1, 1), (2, 2)]) == 0
    assert triangulo_max2([(0, 0), (0, 0)]) == 0
    rect = [(0, 0), (4, 0), (4, 2), (0, 2)]               # áreas iguales: no se cuelga
    assert diametro2(rect)[0] == 20 and triangulo_max2(rect) == 8

    for _ in range(1500):
        r = random.choice([2, 4, 10, 1000])
        pts = [(random.randint(-r, r), random.randint(-r, r))
               for _ in range(random.randint(1, 12))]
        d2, (p, q) = diametro2(pts)
        assert d2 == bruto_diam(pts) == dist2(p, q) and p in pts and q in pts
        assert triangulo_max2(pts) == bruto_tri(pts)

    for _ in range(200):                                # casi convexos: h grande
        n = random.randint(3, 40)
        A, B = random.randint(5, 1000), random.randint(5, 1000)
        fase = random.random() * 6.3
        pts = [(round(A * math.cos(fase + 2 * math.pi * t / n + random.random() * 0.05)),
                round(B * math.sin(fase + 2 * math.pi * t / n + random.random() * 0.05)))
               for t in range(n)]
        assert diametro2(pts)[0] == bruto_diam(pts)
        assert triangulo_max2(pts) == bruto_tri(pts)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
