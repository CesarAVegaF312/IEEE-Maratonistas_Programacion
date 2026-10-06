"""
Programación dinámica — Caminos en grilla («Grid paths»)
Nivel: Básico
Ejecutar: python caminos_grilla.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    En una grilla n×m con obstáculos, moviéndose solo a la DERECHA o hacia
    ABAJO desde la esquina superior izquierda hasta la inferior derecha:
      (1) contar cuántos caminos hay (normalmente módulo 10^9+7);
      (2) encontrar el camino de suma mínima (cada celda tiene un costo) y
          mostrarlo.
    Señales: «solo puede moverse a la derecha o abajo», «robot en una
    cuadrícula», «trampas / celdas bloqueadas», n·m ≤ ~10^6–10^7.
    Si se puede mover en las 4 direcciones NO es DP (hay ciclos): es BFS o
    Dijkstra.

FUNCIÓN
    contar_caminos(grilla, mod=None) -> int
        grilla: lista de cadenas, '.' libre y '#' obstáculo.
    camino_suma_minima(costos) -> (int | None, list)
        costos[i][j]: entero, o None si la celda está bloqueada.
        Devuelve (suma mínima incluyendo origen y destino, lista de celdas
        (i, j) del camino); (None, []) si no hay camino.

IDEA Y ALGORITMO
    Contar:
      ESTADO      dp[i][j] = número de caminos de (0,0) a (i,j).
      TRANSICIÓN  a (i,j) se llega desde arriba o desde la izquierda:
                  dp[i][j] = dp[i-1][j] + dp[i][j-1]   (0 si es obstáculo).
      CASO BASE   dp[0][0] = 1 si está libre (0 si es obstáculo).
      ORDEN       fila por fila, de izquierda a derecha (arriba e izquierda
                  ya están listos).
      RESPUESTA   dp[n-1][m-1].
      Los dos conjuntos de caminos (último paso desde arriba / desde la
      izquierda) son disjuntos y cubren todo: por eso se suman.
    Suma mínima:
      ESTADO      dp[i][j] = menor suma de un camino de (0,0) a (i,j).
      TRANSICIÓN  dp[i][j] = costo[i][j] + min(dp[i-1][j], dp[i][j-1]).
      CASO BASE   dp[0][0] = costo[0][0]; bloqueadas = infinito.
      ORDEN y RESPUESTA iguales. Reconstrucción: desde el destino, ir hacia
      el vecino (arriba o izquierda) con menor dp; invertir.
    Sin obstáculos, contar = C(n+m-2, n-1) (elegir cuáles pasos son «abajo»).

MACROALGORITMO
    1. Tabla n×m.
    2. Recorrer filas y columnas en orden.
    3. Celda bloqueada: 0 caminos / infinito.
    4. Celda libre: combinar arriba e izquierda (suma o mínimo).
    5. Leer la esquina final; reconstruir si se pide el camino.

COMPLEJIDAD
    O(n·m) tiempo y memoria (O(m) si solo se necesita el número, con una
    fila). En Python, 10^6 celdas en ~0,5 s.

EJEMPLO A MANO
    grilla        dp (caminos)
      . . .        1 1 1
      . # .        1 0 1
      . . .        1 1 2      -> 2 caminos (bordeando el obstáculo)

ERRORES TÍPICOS
    - Origen o destino bloqueado: la respuesta es 0 (o sin camino).
    - Olvidar el módulo en cada suma (en Python no desborda, pero se
      vuelve lento).
    - Primera fila/columna: después de un obstáculo, todo lo que sigue en
      esa fila/columna queda en 0 (no inicializar con 1 a ciegas).
    - Aplicarla con movimientos en 4 direcciones.

VARIANTES Y RELACIONADOS
    - Máximo de monedas recogidas, número de caminos con suma par, dos
      caminos simultáneos (DP con dos robots: estado (paso, fila1, fila2)).
    - Muchas consultas sin obstáculos: coeficiente binomial con factoriales.
    - dp_dag.py (la grilla con estos movimientos es un DAG),
      reconstruccion_solucion.py.

DÓNDE PRACTICAR
    - Externos: CSES «Grid Paths» (sección de DP, con trampas); AtCoder
      Educational DP Contest H «Grid 1».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (enumerar todas las secuencias de
      pasos derecha/abajo) en 600 grillas aleatorias hasta 6×6 + casos borde
      (python caminos_grilla.py)
"""
import itertools
import random
from math import comb


def contar_caminos(grilla, mod=None):
    """Número de caminos derecha/abajo de (0,0) a (n-1,m-1) evitando '#'."""
    n, m = len(grilla), len(grilla[0])
    dp = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if grilla[i][j] == '#':
                continue                                # obstáculo: 0 caminos
            if i == 0 and j == 0:
                dp[i][j] = 1                            # caso base
                continue
            v = (dp[i - 1][j] if i else 0) + (dp[i][j - 1] if j else 0)
            dp[i][j] = v % mod if mod else v
    return dp[n - 1][m - 1]


def camino_suma_minima(costos):
    """(suma mínima, celdas del camino) o (None, []) si no hay camino."""
    n, m = len(costos), len(costos[0])
    INF = float("inf")
    dp = [[INF] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if costos[i][j] is None:
                continue                                # bloqueada: queda infinito
            if i == 0 and j == 0:
                dp[0][0] = costos[0][0]
                continue
            mejor = min(dp[i - 1][j] if i else INF, dp[i][j - 1] if j else INF)
            dp[i][j] = mejor + costos[i][j]             # inf + x sigue siendo inf
    if dp[n - 1][m - 1] == INF:
        return None, []
    camino, i, j = [(n - 1, m - 1)], n - 1, m - 1
    while (i, j) != (0, 0):                             # retroceder al mejor vecino
        if j == 0 or (i > 0 and dp[i - 1][j] <= dp[i][j - 1]):
            i -= 1
        else:
            j -= 1
        camino.append((i, j))
    camino.reverse()
    return dp[n - 1][m - 1], camino


def demo():
    g = ["...", ".#.", "..."]
    print("grilla:", *g, sep="\n  ")
    print("contar_caminos ->", contar_caminos(g))                  # 2
    costos = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    print("costos", costos, "->", camino_suma_minima(costos))      # 7 por la fila de arriba


def pruebas():
    random.seed(1638)

    def caminos_brutos(n, m):
        """Todas las secuencias de pasos: elegir qué n-1 de los n+m-2 pasos son 'abajo'."""
        for abajos in itertools.combinations(range(n + m - 2), n - 1):
            celdas, i, j = [(0, 0)], 0, 0
            for p in range(n + m - 2):
                if p in abajos:
                    i += 1
                else:
                    j += 1
                celdas.append((i, j))
            yield celdas

    # Casos borde
    assert contar_caminos(["."]) == 1 and contar_caminos(["#"]) == 0
    assert contar_caminos([".#", "#."]) == 0
    assert contar_caminos(["." * 5] * 5) == comb(8, 4)
    assert contar_caminos(["." * 20] * 20, 10**9 + 7) == comb(38, 19) % (10**9 + 7)
    assert camino_suma_minima([[5]]) == (5, [(0, 0)])
    assert camino_suma_minima([[1, None], [None, 1]]) == (None, [])

    for _ in range(600):
        n, m = random.randint(1, 6), random.randint(1, 6)
        p = random.choice([0.0, 0.15, 0.3])
        costos = [[None if random.random() < p else random.randint(0, 9) for _ in range(m)]
                  for _ in range(n)]
        grilla = ["".join('#' if c is None else '.' for c in fila) for fila in costos]
        cuenta, mejor = 0, None
        for celdas in caminos_brutos(n, m):
            if all(costos[i][j] is not None for i, j in celdas):
                cuenta += 1
                s = sum(costos[i][j] for i, j in celdas)
                mejor = s if mejor is None else min(mejor, s)
        assert contar_caminos(grilla) == cuenta
        assert contar_caminos(grilla, 7) == cuenta % 7
        suma, camino = camino_suma_minima(costos)
        assert suma == mejor
        if suma is not None:
            assert camino[0] == (0, 0) and camino[-1] == (n - 1, m - 1)
            assert len(camino) == n + m - 1
            for (a, b), (c, d) in zip(camino, camino[1:]):
                assert (c - a, d - b) in ((1, 0), (0, 1))
            assert sum(costos[i][j] for i, j in camino) == suma


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
