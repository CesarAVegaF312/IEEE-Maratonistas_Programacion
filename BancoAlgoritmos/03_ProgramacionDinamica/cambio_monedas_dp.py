"""
Programación dinámica — Cambio de monedas («Coin change»)
Nivel: Básico
Ejecutar: python cambio_monedas_dp.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Con monedas de ciertos valores (cada una se puede usar las veces que se
    quiera) se quiere formar exactamente la cantidad x:
      (1) con el MÍNIMO número de monedas;
      (2) contar de cuántas FORMAS, donde 2+1 y 1+2 son la misma (no importa
          el orden: se cuentan multiconjuntos);
      (3) contar de cuántas formas si 2+1 y 1+2 son distintas (importa el
          orden: se cuentan secuencias).
    Señales: «monedas / sellos / dardos / pesos con valores dados, ilimitados,
    formar exactamente x», x ≤ ~10^6. El voraz («tomar siempre la mayor
    moneda») NO sirve en general: con {1, 3, 4} y x = 6 da 4+1+1 (3 monedas)
    y lo óptimo es 3+3 (2).

FUNCIÓN
    min_monedas(monedas, x) -> (int, list)
        Mínimo número de monedas y una lista de monedas que lo logra;
        (-1, []) si x no se puede formar.
    formas_sin_orden(monedas, x, mod=None) -> int   multiconjuntos (CSES
        «Coin Combinations II»).
    formas_con_orden(monedas, x, mod=None) -> int   secuencias (CSES «Coin
        Combinations I»).
    Las monedas son enteros positivos distintos.

IDEA Y ALGORITMO
    Mínimo de monedas:
      ESTADO      dp[s] = mínimo número de monedas que suman exactamente s.
      TRANSICIÓN  la última moneda fue c: dp[s] = min_c dp[s - c] + 1.
      CASO BASE   dp[0] = 0; los demás empiezan en «infinito» (imposible).
      ORDEN       s creciente.      RESPUESTA  dp[x] (o -1 si quedó infinito).
      Correcto porque quitar la última moneda de una solución óptima para s
      deja una solución óptima para s - c (subestructura óptima).
      Para reconstruir se guarda en ultima[s] la moneda que dio el mínimo.
    Número de formas — el ORDEN DE LOS BUCLES decide qué se cuenta:
      ESTADO      dp[s] = número de formas de sumar s; CASO BASE dp[0] = 1.
      Con orden (secuencias): para cada s (bucle externo), sumar dp[s - c]
        de cada moneda c: es «elegir la última moneda», y secuencias que
        terminan en monedas distintas son distintas.
      Sin orden (multiconjuntos): para cada moneda c (bucle EXTERNO), para
        s creciente: dp[s] += dp[s - c]. Tras procesar las primeras k
        monedas, dp[s] cuenta las formas que usan solo esas k monedas; las
        monedas se «agregan» siempre en el orden de la lista, así que cada
        multiconjunto aparece exactamente una vez (como una secuencia
        ordenada por tipo de moneda).
      RESPUESTA dp[x]. Recorrer s CRECIENTE permite reusar la moneda c
      varias veces (dp[s - c] ya puede incluir monedas c).

MACROALGORITMO
    1. Crear dp de tamaño x+1 con el caso base en dp[0].
    2. Mínimo / con orden: para s = 1..x, para cada moneda c ≤ s, relajar
       dp[s] con dp[s - c].
    3. Sin orden: para cada moneda c, para s = c..x: dp[s] += dp[s - c].
    4. (Mínimo) reconstruir saltando s -> s - ultima[s] hasta llegar a 0.
    5. Aplicar módulo si el enunciado lo pide.

COMPLEJIDAD
    Tiempo O(x · k) con k monedas, memoria O(x). En Python ~10^7 pasos por
    segundo: x·k ≤ ~10^7.

EJEMPLO A MANO
    monedas = {1, 3, 4}, x = 6:
      s      0 1 2 3 4 5 6
      dp     0 1 2 1 1 2 2      -> mínimo 2 (3 + 3)
    monedas = {1, 2}, x = 3: sin orden 2 (1+1+1, 1+2); con orden 3
    (1+1+1, 1+2, 2+1).

ERRORES TÍPICOS
    - Intercambiar los bucles y contar secuencias cuando se pedían
      multiconjuntos (o al revés).
    - Usar el voraz con monedas que no son «canónicas».
    - Iniciar dp con 0 en vez de infinito para el mínimo.
    - Olvidar el módulo en cada suma: en Python no desborda pero se vuelve
      lento con números de miles de dígitos.
    - Si cada moneda se puede usar UNA vez, es mochila 0/1 (s decreciente).

VARIANTES Y RELACIONADOS
    - Monedas limitadas (c_i usada a lo sumo k_i veces): mochila acotada.
    - mochila_ilimitada.py (mismo patrón con valores), mochila_01.py,
      memoizacion.py (dado = monedas {1..6} con orden).
    - Monedas con dos coordenadas (e-coins): dp en 2D dp[x][y].

DÓNDE PRACTICAR
    - ICPC/OMP 2017 Murcia/E - Prime Darts (mínimo de monedas, tablas
      incrementales).
    - 2025-2/maraton_problemas/p10306_e_coins.py (UVa 10306, mínimo de
      monedas en 2D).
    - Externos: CSES «Minimizing Coins», «Coin Combinations I», «Coin
      Combinations II»; UVa 674 «Coin Change», UVa 357 «Let Me Count The Ways».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (enumerar cuántas veces se usa cada
      moneda y enumerar secuencias) en 600 casos aleatorios + casos borde
      (python cambio_monedas_dp.py)
"""
import itertools
import random


def min_monedas(monedas, x):
    """(mínimo de monedas que suman exactamente x, lista de monedas); (-1, []) si no se puede."""
    INF = float("inf")
    dp = [0] + [INF] * x            # dp[s] = mínimo de monedas para sumar s
    ultima = [0] * (x + 1)          # ultima[s] = moneda usada al final en el óptimo
    for s in range(1, x + 1):
        for c in monedas:
            if c <= s and dp[s - c] + 1 < dp[s]:
                dp[s] = dp[s - c] + 1
                ultima[s] = c
    if dp[x] == INF:
        return -1, []
    usadas, s = [], x
    while s > 0:                    # reconstrucción: quitar la última moneda
        usadas.append(ultima[s])
        s -= ultima[s]
    return dp[x], usadas


def formas_sin_orden(monedas, x, mod=None):
    """Número de multiconjuntos de monedas que suman x (1+2 = 2+1)."""
    dp = [1] + [0] * x
    for c in monedas:               # moneda POR FUERA: cada multiconjunto una vez
        for s in range(c, x + 1):   # s creciente: la moneda c se puede repetir
            dp[s] += dp[s - c]
            if mod:
                dp[s] %= mod
    return dp[x]


def formas_con_orden(monedas, x, mod=None):
    """Número de secuencias de monedas que suman x (1+2 ≠ 2+1)."""
    dp = [1] + [0] * x
    for s in range(1, x + 1):       # suma POR FUERA: se elige la última moneda
        total = 0
        for c in monedas:
            if c <= s:
                total += dp[s - c]
        dp[s] = total % mod if mod else total
    return dp[x]


def demo():
    m, x = [1, 3, 4], 6
    print(f"monedas={m}, x={x}: min_monedas ->", min_monedas(m, x))       # (2, [3, 3])
    print("formas sin orden {1,2}, 3 ->", formas_sin_orden([1, 2], 3))   # 2
    print("formas con orden {1,2}, 3 ->", formas_con_orden([1, 2], 3))   # 3
    print("UVa 674 (1,5,10,25,50), 11 ->", formas_sin_orden([1, 5, 10, 25, 50], 11))  # 4


def pruebas():
    random.seed(674)

    def brutas(monedas, x):
        """Enumera cuántas veces se usa cada moneda: mínimo y número de multiconjuntos."""
        mejor, cuenta = None, 0
        for usos in itertools.product(*[range(x // c + 1) for c in monedas]):
            if sum(u * c for u, c in zip(usos, monedas)) == x:
                cuenta += 1
                if mejor is None or sum(usos) < mejor:
                    mejor = sum(usos)
        return (-1 if mejor is None else mejor), cuenta

    def secuencias_bruta(monedas, x):
        if x == 0:
            return 1
        return sum(secuencias_bruta(monedas, x - c) for c in monedas if c <= x)

    # Casos borde
    assert min_monedas([5], 0) == (0, [])
    assert min_monedas([2], 3) == (-1, [])
    assert formas_sin_orden([3], 0) == formas_con_orden([3], 0) == 1
    assert formas_sin_orden([2, 4], 7) == formas_con_orden([2, 4], 7) == 0

    for _ in range(600):
        k = random.randint(1, 4)
        monedas = random.sample(range(1, 10), k)
        x = random.randint(0, 14)
        mejor, cuenta = brutas(monedas, x)
        cant, usadas = min_monedas(monedas, x)
        assert cant == mejor
        if cant != -1:
            assert len(usadas) == cant and sum(usadas) == x
            assert all(c in monedas for c in usadas)
        assert formas_sin_orden(monedas, x) == cuenta
        assert formas_con_orden(monedas, x) == secuencias_bruta(monedas, x)
        assert formas_sin_orden(monedas, x, 7) == cuenta % 7

    # Valores conocidos: CSES ejemplos (2,3,5) x=9 -> 8 secuencias, 3 multiconjuntos
    assert formas_con_orden([2, 3, 5], 9) == 8
    assert formas_sin_orden([2, 3, 5], 9) == 3
    assert min_monedas([1, 5, 7], 11)[0] == 3


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
