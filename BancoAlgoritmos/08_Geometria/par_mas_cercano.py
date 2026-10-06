r"""
Geometría — Par de puntos más cercano en O(n log n) («closest pair, divide and conquer»)
Nivel: Avanzado
Ejecutar: python par_mas_cercano.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar los dos puntos más cercanos entre n puntos del plano en
    O(n log n), cuando comparar todos los pares (O(n²)) no alcanza.
    Señales en el enunciado: «distancia mínima entre dos de los n puntos»,
    «las dos ciudades/estrellas/antenas más cercanas», n hasta 10^5 (o más),
    «¿hay dos puntos a distancia menor que d?».

FUNCIÓN
    par_mas_cercano(puntos) -> (int, (p, q))
        Menor distancia AL CUADRADO (exacta con enteros) y un par que la
        logra. Puntos repetidos dan distancia 0. Requiere n >= 2.

IDEA Y ALGORITMO
    Divide y vencerás:
    1) Ordenar por x y partir por la mitad con una recta vertical x = xm.
    2) Resolver cada mitad recursivamente: δ = mínimo de las dos respuestas.
    3) Falta el mejor par que CRUZA la recta. Solo pueden mejorar δ los
       puntos de la franja |x − xm| < δ. Ordenados por y, cada punto solo
       necesita compararse con los siguientes cuyo y esté a menos de δ.

                     |      Franja de ancho 2δ alrededor de x = xm.
            ·    · · | ·    Para un punto p de la franja, los candidatos
              ·   ┌──┼──┐   están en el rectángulo δ × 2δ de arriba;
           ·      │· │ ·│   en cada mitad (cuadrado δ × δ) caben a lo
                · │  │· │   sumo 4 puntos a distancia >= δ entre sí,
            ·     └──┼──┘   así que hay <= 7 candidatos: O(1) por punto.
                  p  |
                <-δ->|<-δ->

    Por qué es correcto: cualquier par a distancia < δ que cruce la recta
    tiene ambos puntos en la franja y diferencia de y menor que δ; el
    recorrido los compara. Y por el argumento de empaquetamiento (puntos
    de una misma mitad están a distancia >= δ), el bucle interno hace O(1)
    pasos por punto.
    Para no reordenar por y en cada nivel (que daría O(n log² n)), cada
    llamada devuelve sus puntos ya ordenados por y y el padre MEZCLA las
    dos listas (como en merge sort). En Python, sorted() sobre la
    concatenación de dos listas ordenadas hace exactamente esa mezcla en
    O(n) (Timsort detecta las dos corridas).
    Todo con distancias al cuadrado enteras: exacto, sin sqrt.

MACROALGORITMO
    1. Ordenar los puntos por x (una vez).
    2. rec(l, r): si hay <= 3 puntos, fuerza bruta y devolverlos ordenados por y.
    3. m = mitad, xm = x de P[m]; resolver [l, m) y [m, r); δ² = mejor.
    4. Mezclar por y las dos listas devueltas.
    5. Franja = puntos (en orden de y) con (x − xm)² < δ².
    6. Para cada i en la franja, para j > i mientras (yj − yi)² < δ²:
       actualizar con dist²(i, j).
    7. Devolver (δ², par, lista por y).

COMPLEJIDAD
    O(n log n) tiempo, O(n) memoria; profundidad de recursión log2(n) (no hay
    problema de pila). En Python, 10^5 puntos en ~0.7 s.

EJEMPLO A MANO
    Puntos: (0,0) (10,0) (3,4) (7,1) (2,9) (8,8) (5,5) (6,3).
    Por x: (0,0) (2,9) (3,4) (5,5) | (6,3) (7,1) (8,8) (10,0); xm = 6.
    Izquierda: mejor (3,4)-(5,5), d² = 5. Derecha: (6,3)-(7,1), d² = 5.
    δ² = 5. Franja (x − 6)² < 5: x en {5, 6, 7, 8} -> (7,1) (6,3) (5,5) (8,8).
    (7,1)-(6,3): 5; (6,3)-(5,5): d² = 1 + 4 = 5; nada menor.
    Respuesta: d² = 5 (d = √5 ≈ 2.236).

ERRORES TÍPICOS
    - Comparar en la franja contra TODOS los puntos (vuelve a O(n²)): cortar
      el bucle interno cuando la diferencia de y ya es >= δ.
    - Reordenar por y en cada llamada: O(n log² n) (suele pasar igual, pero
      es más lento en Python).
    - Usar < vs <= mal en la franja con puntos repetidos: con δ = 0 la
      franja queda vacía, lo cual es correcto (ya no se puede mejorar).
    - Sacar sqrt antes de terminar: comparar distancias al cuadrado.

VARIANTES Y RELACIONADOS
    - Barrido con un conjunto ordenado por y (std::set): también O(n log n).
    - Aleatorizado con rejilla (hash de celdas de lado δ): O(n) esperado.
    - Para «¿hay dos puntos a distancia < d?» con d fijo: rejilla de celdas
      de lado d y revisar las 9 celdas vecinas.
    - Par más LEJANO: no se hace así, sino con la envolvente y calibradores
      (rotating_calipers.py).
    - K vecinos más cercanos de cada punto: con n pequeño, fuerza bruta con
      distancias al cuadrado; con n grande, k-d tree.
    - Línea de barrido (linea_de_barrido.py).

DÓNDE PRACTICAR
    - CSES «Minimum Euclidean Distance» (exactamente este archivo; pide d²)
    - UVa 10245 «The Closest Pair Problem»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta O(n²) en 2000 conjuntos aleatorios
      (n <= 60, muchas coordenadas repetidas y colineales; también rangos
      grandes) y 3 conjuntos de 2000 puntos; además un caso de 10^5 puntos
      se resuelve en pocos segundos (python par_mas_cercano.py)
"""
import random
import time


def dist2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def par_mas_cercano(puntos):
    """(menor distancia², (p, q)) en O(n log n). n >= 2."""
    P = sorted(puntos)                      # por x (y luego por y)
    porY = lambda p: p[1]

    def rec(l, r):
        if r - l <= 3:                      # caso base: fuerza bruta
            mejor, par = float("inf"), None
            for i in range(l, r):
                for j in range(i + 1, r):
                    d = dist2(P[i], P[j])
                    if d < mejor:
                        mejor, par = d, (P[i], P[j])
            return mejor, par, sorted(P[l:r], key=porY)
        m = (l + r) // 2
        xm = P[m][0]
        d1, p1, izq = rec(l, m)
        d2, p2, der = rec(m, r)
        mejor, par = (d1, p1) if d1 <= d2 else (d2, p2)
        ys = sorted(izq + der, key=porY)    # mezcla O(n): dos corridas ordenadas
        franja = [p for p in ys if (p[0] - xm) ** 2 < mejor]
        for i in range(len(franja)):
            xi, yi = franja[i]
            for j in range(i + 1, len(franja)):
                xj, yj = franja[j]
                if (yj - yi) ** 2 >= mejor:
                    break                   # más arriba ya no puede mejorar
                d = (xj - xi) ** 2 + (yj - yi) ** 2
                if d < mejor:
                    mejor, par = d, (franja[i], franja[j])
        return mejor, par, ys

    mejor, par, _ = rec(0, len(P))
    return mejor, par


def demo():
    pts = [(0, 0), (10, 0), (3, 4), (7, 1), (2, 9), (8, 8), (5, 5), (6, 3)]
    d2, (p, q) = par_mas_cercano(pts)
    print("puntos:", pts)
    print("par más cercano:", p, q, " d² =", d2, " d = %.4f" % d2 ** 0.5)   # 5


def pruebas():
    random.seed(10245)

    def bruto(pts):
        return min(dist2(pts[i], pts[j]) for i in range(len(pts)) for j in range(i + 1, len(pts)))

    # Casos borde
    assert par_mas_cercano([(0, 0), (3, 4)]) == (25, ((0, 0), (3, 4)))
    assert par_mas_cercano([(1, 1), (5, 5), (1, 1)])[0] == 0              # repetidos
    assert par_mas_cercano([(0, y * y) for y in range(50)])[0] == 1       # vertical
    assert par_mas_cercano([(x, 7) for x in range(0, 100, 3)])[0] == 9    # horizontal

    for _ in range(2000):
        n = random.randint(2, 60)
        r = random.choice([3, 20, 10 ** 9])
        pts = [(random.randint(-r, r), random.randint(-r, r)) for _ in range(n)]
        if random.random() < 0.2:
            pts = [(random.randint(-2, 2), random.randint(-r, r)) for _ in range(n)]
        d, (p, q) = par_mas_cercano(pts)
        assert d == bruto(pts) == dist2(p, q)
        assert p in pts and q in pts and (p != q or pts.count(p) >= 2)

    for _ in range(3):
        pts = [(random.randint(-10 ** 6, 10 ** 6), random.randint(-10 ** 6, 10 ** 6))
               for _ in range(2000)]
        assert par_mas_cercano(pts)[0] == bruto(pts)

    # Rendimiento: 10^5 puntos
    pts = [(random.randint(-10 ** 9, 10 ** 9), random.randint(-10 ** 9, 10 ** 9))
           for _ in range(10 ** 5)]
    t = time.time()
    par_mas_cercano(pts)
    assert time.time() - t < 10


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
