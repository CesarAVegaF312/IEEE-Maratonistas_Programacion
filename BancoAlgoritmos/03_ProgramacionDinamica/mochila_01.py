"""
Programación dinámica — Mochila 0/1 («0/1 knapsack»)
Nivel: Básico
Ejecutar: python mochila_01.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Hay n objetos, cada uno con peso p_i y valor v_i, y una mochila de
    capacidad W. Elegir un subconjunto (cada objeto a lo sumo UNA vez) de
    peso total ≤ W y valor máximo.
    Señales: «cada objeto se puede tomar o no», «presupuesto / capacidad /
    tiempo límite», n·W ≤ ~10^7. Si n ≤ 20–40 sin W pequeño, pensar en
    fuerza bruta o encuentro en el medio; si W es enorme pero los valores
    son pequeños, usar la mochila «por valor» (abajo).

FUNCIÓN
    mochila_2d(pesos, valores, W) -> (int, list)
        Valor máximo y los índices (crecientes) de los objetos elegidos.
    mochila_1d(pesos, valores, W) -> int
        Solo el valor, con memoria O(W).
    mochila_por_valor(pesos, valores, W) -> int
        Mismo problema con W gigante y Σ valores pequeña (O(n · Σv)).

IDEA Y ALGORITMO
    ESTADO      dp[i][c] = máximo valor usando solo los primeros i objetos
                con peso total ≤ c.
    TRANSICIÓN  el objeto i-1 se deja o se toma:
                dp[i][c] = max(dp[i-1][c], dp[i-1][c - p] + v)   (si p ≤ c).
    CASOS BASE  dp[0][c] = 0 para todo c (sin objetos no hay valor).
    ORDEN       i creciente; dentro de cada fila, c en cualquier orden.
    RESPUESTA   dp[n][W].
    Correcto porque en un óptimo para (i, c) el objeto i-1 o no está (el
    resto es óptimo para (i-1, c)) o está (el resto es óptimo para
    (i-1, c - p)): se prueban ambas.
    Reconstrucción: desde (n, W) hacia atrás; si dp[i][c] ≠ dp[i-1][c], el
    objeto i-1 SÍ se tomó (c -= p); si son iguales, no tomarlo es óptimo.
    Versión 1D: la fila i solo usa la fila i-1, así que se guarda una sola
    fila y se recorre c de W hacia p (AL REVÉS). Así, cuando se lee
    dp[c - p], todavía tiene el valor de la fila anterior (no incluye al
    objeto i): cada objeto se usa a lo sumo una vez. Si se recorriera c
    creciente, dp[c - p] ya podría incluir el objeto i y se tomaría varias
    veces (eso es la mochila ilimitada).
    Mochila por valor: mp[s] = peso mínimo para lograr valor EXACTO s
    (mismo truco 1D con s decreciente); respuesta = mayor s con mp[s] ≤ W.

MACROALGORITMO
    1. dp = fila de W+1 ceros (o tabla (n+1) × (W+1) si hay que reconstruir).
    2. Para cada objeto (p, v):
    3.    para c de W bajando hasta p: dp[c] = max(dp[c], dp[c-p] + v).
    4. Respuesta dp[W].
    5. (2D) Reconstruir desde (n, W) comparando dp[i][c] con dp[i-1][c].

COMPLEJIDAD
    Tiempo O(n · W). Memoria O(W) en 1D, O(n · W) en 2D.
    En Python: n · W ≤ ~10^7 por segundo (los bucles internos simples).
    Por valor: O(n · Σv).

EJEMPLO A MANO
    pesos = [3, 4, 2], valores = [30, 50, 15], W = 6
      c:          0  1  2  3  4  5  6
      i=0         0  0  0  0  0  0  0
      i=1 (3,30)  0  0  0 30 30 30 30
      i=2 (4,50)  0  0  0 30 50 50 50
      i=3 (2,15)  0  0 15 30 50 50 65
    Respuesta 65. Reconstrucción: dp[3][6]=65 ≠ 50 -> toma 2 (c=4);
    dp[2][4]=50 ≠ 30 -> toma 1 (c=0); dp[1][0]=0 = 0 -> no toma 0. -> [1, 2].

ERRORES TÍPICOS
    - En 1D recorrer c creciente: convierte el problema en mochila ilimitada.
    - Confundir «peso ≤ W» (dp inicial en 0) con «peso exactamente W» (dp
      inicial en -infinito salvo dp[0] = 0).
    - Reconstruir sobre la versión 1D: ya se perdieron las filas; usar 2D o
      guardar un bit «tomado[i][c]».
    - n · W demasiado grande (10^5 · 10^9): ver mochila por valor u otra idea.

VARIANTES Y RELACIONADOS
    - Peso exacto, mínimo costo para alcanzar valor ≥ V, contar subconjuntos
      con suma s (subset sum: mismo recorrido al revés sumando formas).
    - Subset sum con enteros grandes como bitset: bits |= bits << p.
    - mochila_ilimitada.py, cambio_monedas_dp.py, reconstruccion_solucion.py
      (subconjunto lexicográficamente menor), dp_arboles.py (mochila en árbol).

DÓNDE PRACTICAR
    - Externos: CSES «Book Shop», «Money Sums» (subset sum); AtCoder
      Educational DP Contest D «Knapsack 1» y E «Knapsack 2» (por valor);
      UVa 10130 «SuperSale».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todos los subconjuntos, n ≤ 10) en
      500 casos aleatorios + casos borde; se valida además que los índices
      reconstruidos respetan W y suman el óptimo (python mochila_01.py)
"""
import random


def mochila_2d(pesos, valores, W):
    """(valor máximo con peso ≤ W, índices elegidos). Tabla completa para reconstruir."""
    n = len(pesos)
    dp = [[0] * (W + 1) for _ in range(n + 1)]       # dp[0][*] = 0: caso base
    for i in range(1, n + 1):
        p, v = pesos[i - 1], valores[i - 1]
        ant, fila = dp[i - 1], dp[i]
        for c in range(W + 1):
            fila[c] = ant[c]                          # no tomar el objeto i-1
            if p <= c and ant[c - p] + v > fila[c]:
                fila[c] = ant[c - p] + v              # tomarlo
    elegidos, c = [], W
    for i in range(n, 0, -1):                         # retroceder sobre la tabla
        if dp[i][c] != dp[i - 1][c]:                  # cambió -> el objeto se tomó
            elegidos.append(i - 1)
            c -= pesos[i - 1]
    elegidos.reverse()
    return dp[n][W], elegidos


def mochila_1d(pesos, valores, W):
    """Valor máximo con peso ≤ W usando una sola fila."""
    dp = [0] * (W + 1)
    for p, v in zip(pesos, valores):
        for c in range(W, p - 1, -1):                 # AL REVÉS: cada objeto una vez
            if dp[c - p] + v > dp[c]:
                dp[c] = dp[c - p] + v
    return dp[W]


def mochila_por_valor(pesos, valores, W):
    """Para W enorme y Σ valores pequeña: mp[s] = peso mínimo para valor exacto s."""
    total = sum(valores)
    INF = float("inf")
    mp = [0] + [INF] * total
    for p, v in zip(pesos, valores):
        for s in range(total, v - 1, -1):             # al revés: 0/1
            if mp[s - v] + p < mp[s]:
                mp[s] = mp[s - v] + p
    return max(s for s in range(total + 1) if mp[s] <= W)


def demo():
    pesos, valores, W = [3, 4, 2], [30, 50, 15], 6
    print("pesos", pesos, "valores", valores, "W =", W)
    print("mochila_2d ->", mochila_2d(pesos, valores, W))           # (65, [1, 2])
    print("mochila_1d ->", mochila_1d(pesos, valores, W))           # 65
    print("por valor con W = 10^9 ->", mochila_por_valor(pesos, valores, 10**9))  # 95


def pruebas():
    random.seed(10130)

    def bruta(pesos, valores, W):
        n, mejor = len(pesos), 0
        for mask in range(1 << n):
            p = sum(pesos[i] for i in range(n) if mask >> i & 1)
            if p <= W:
                mejor = max(mejor, sum(valores[i] for i in range(n) if mask >> i & 1))
        return mejor

    # Casos borde
    assert mochila_2d([], [], 5) == (0, [])
    assert mochila_1d([], [], 0) == 0
    assert mochila_2d([7], [9], 6) == (0, [])
    assert mochila_2d([6], [9], 6) == (9, [0])
    assert mochila_1d([2, 2, 2], [5, 5, 5], 4) == 10    # iguales: no repetir objetos

    for _ in range(500):
        n = random.randint(1, 10)
        pesos = [random.randint(1, 10) for _ in range(n)]
        valores = [random.randint(0, 20) for _ in range(n)]
        W = random.randint(0, 30)
        esperado = bruta(pesos, valores, W)
        mejor, elegidos = mochila_2d(pesos, valores, W)
        assert mejor == esperado == mochila_1d(pesos, valores, W)
        assert mochila_por_valor(pesos, valores, W) == esperado
        assert elegidos == sorted(set(elegidos))
        assert sum(pesos[i] for i in elegidos) <= W
        assert sum(valores[i] for i in elegidos) == mejor


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
