"""
Programación dinámica — Mochila ilimitada («Unbounded knapsack»)
Nivel: Básico
Ejecutar: python mochila_ilimitada.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Hay n TIPOS de objetos (peso p_i, valor v_i) y de cada tipo se pueden
    tomar todas las copias que se quiera. Con capacidad W, maximizar el
    valor total con peso ≤ W (o con peso exactamente W).
    Señales: «cantidad ilimitada», «infinitas copias», «se puede comprar
    varias veces», «cortar una varilla en piezas con precio por largo»,
    W ≤ ~10^6–10^7 / n. Es el mismo esquema que el cambio de monedas pero
    maximizando valor.

FUNCIÓN
    mochila_ilimitada(pesos, valores, W) -> (int, list)
        Valor máximo con peso total ≤ W y cuántas copias de cada tipo
        (lista de largo n) logran ese valor.
    mochila_ilimitada_exacta(pesos, valores, W) -> int | None
        Valor máximo con peso EXACTAMENTE W; None si W no se puede llenar.

IDEA Y ALGORITMO
    ESTADO      dp[c] = máximo valor con peso total ≤ c.
    TRANSICIÓN  mirar UNA copia cualquiera de la solución (la «última»):
                dp[c] = max(0, max_{i: p_i ≤ c} dp[c - p_i] + v_i).
    CASO BASE   dp[0] = 0.
    ORDEN       c creciente (dp[c] usa capacidades menores).
    RESPUESTA   dp[W].
    Por qué basta: si una solución óptima para c usa al menos una copia de
    i, al quitarla queda una solución de peso ≤ c - p_i, que vale a lo sumo
    dp[c - p_i]. Si no usa nada vale 0. Como los tipos se pueden repetir, el
    subproblema c - p_i puede volver a usar i: por eso NO hace falta el
    índice del objeto en el estado (a diferencia de la mochila 0/1).
    Diferencia con 0/1 en la versión «objetos por fuera»: con un bucle
    externo por objeto, recorrer c CRECIENTE (dp[c - p] ya puede incluir el
    objeto actual -> repetición permitida); en 0/1 se recorre al revés.
    Reconstrucción: eleccion[c] = tipo usado en el óptimo de c (-1 = no
    agregar nada más); se baja c -= p de ese tipo hasta llegar a -1.
    Peso exacto: igual, pero dp empieza en -infinito salvo dp[0] = 0 y sin
    la opción «0»; la respuesta es dp[W] (-infinito = imposible).

MACROALGORITMO
    1. dp = [0] * (W+1); eleccion = [-1] * (W+1).
    2. Para c = 1..W: para cada tipo i con p_i ≤ c, si dp[c-p_i] + v_i
       mejora dp[c], actualizar dp[c] y eleccion[c] = i.
    3. Respuesta dp[W]; reconstruir siguiendo eleccion desde W.

COMPLEJIDAD
    Tiempo O(n · W), memoria O(W). En Python n · W ≤ ~10^7.
    Truco: si dos tipos tienen el mismo peso, solo sirve el de mayor valor.

EJEMPLO A MANO
    pesos = [3, 4], valores = [5, 7], W = 10
      c    0 1 2 3 4 5 6  7  8  9 10
      dp   0 0 0 5 7 7 10 12 14 15 17
    dp[10] = max(dp[7] + 5, dp[6] + 7) = max(17, 17) = 17 (3+3+4).

ERRORES TÍPICOS
    - Recorrer c al revés con objetos por fuera (eso es 0/1: una copia).
    - Confundir «≤ W» con «exactamente W» (inicialización con -infinito).
    - Olvidar que el valor puede ser 0 o que W puede no llenarse.
    - Usar float('inf') y luego compararlo como entero en la salida.

VARIANTES Y RELACIONADOS
    - Corte de varilla: tipos = largos 1..L con su precio (ver
      reconstruccion_solucion.py).
    - Mochila acotada (k_i copias): dividir en potencias de 2 y hacer 0/1.
    - cambio_monedas_dp.py (minimizar cantidad / contar formas),
      mochila_01.py.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/A - Alice's Travels II (mochila ilimitada por
      costo, más máximos en caminos de árbol).
    - ICPC/OMP 2017 Murcia/E - Prime Darts (mínimo de «monedas» ilimitadas).
    - 2025-2/maraton_problemas/p10306_e_coins.py (UVa 10306: ilimitada en 2D).
    - Externos: UVa 10306 «e-Coins».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (enumerar copias de cada tipo) en 500
      casos aleatorios + casos borde (python mochila_ilimitada.py)
"""
import itertools
import random


def mochila_ilimitada(pesos, valores, W):
    """(valor máximo con peso ≤ W, copias de cada tipo)."""
    n = len(pesos)
    dp = [0] * (W + 1)              # dp[c] = máximo valor con peso ≤ c
    eleccion = [-1] * (W + 1)       # tipo agregado en el óptimo de c (-1: ninguno)
    for c in range(1, W + 1):
        for i in range(n):
            p = pesos[i]
            if p <= c and dp[c - p] + valores[i] > dp[c]:
                dp[c] = dp[c - p] + valores[i]
                eleccion[c] = i
    copias, c = [0] * n, W
    while eleccion[c] != -1:        # bajar por las decisiones guardadas
        i = eleccion[c]
        copias[i] += 1
        c -= pesos[i]
    return dp[W], copias


def mochila_ilimitada_exacta(pesos, valores, W):
    """Máximo valor con peso EXACTAMENTE W, o None si no se puede llenar."""
    NEG = float("-inf")
    dp = [0] + [NEG] * W            # -inf = ese peso exacto no se puede formar
    for p, v in zip(pesos, valores):
        for c in range(p, W + 1):   # creciente: copias ilimitadas
            if dp[c - p] + v > dp[c]:
                dp[c] = dp[c - p] + v
    return None if dp[W] == NEG else dp[W]


def demo():
    pesos, valores, W = [3, 4], [5, 7], 10
    print("pesos", pesos, "valores", valores, "W =", W)
    print("mochila_ilimitada ->", mochila_ilimitada(pesos, valores, W))   # (17, [2, 1])
    print("exacta W = 5 ->", mochila_ilimitada_exacta(pesos, valores, 5))  # None
    print("exacta W = 11 ->", mochila_ilimitada_exacta(pesos, valores, 11))  # 19


def pruebas():
    random.seed(10306)

    def bruta(pesos, valores, W):
        mejor, exacta = 0, None
        for k in itertools.product(*[range(W // p + 1) for p in pesos]):
            peso = sum(a * p for a, p in zip(k, pesos))
            if peso <= W:
                val = sum(a * v for a, v in zip(k, valores))
                mejor = max(mejor, val)
                if peso == W and (exacta is None or val > exacta):
                    exacta = val
        return mejor, exacta

    # Casos borde
    assert mochila_ilimitada([5], [3], 0) == (0, [0])
    assert mochila_ilimitada([5], [3], 4) == (0, [0])
    assert mochila_ilimitada([1], [2], 7) == (14, [7])
    assert mochila_ilimitada_exacta([2], [1], 3) is None
    assert mochila_ilimitada_exacta([2], [1], 0) == 0

    for _ in range(500):
        n = random.randint(1, 4)
        pesos = [random.randint(1, 8) for _ in range(n)]
        valores = [random.randint(0, 15) for _ in range(n)]
        W = random.randint(0, 15)
        mejor, exacta = bruta(pesos, valores, W)
        val, copias = mochila_ilimitada(pesos, valores, W)
        assert val == mejor
        assert sum(a * p for a, p in zip(copias, pesos)) <= W
        assert sum(a * v for a, v in zip(copias, valores)) == val
        assert mochila_ilimitada_exacta(pesos, valores, W) == exacta


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
