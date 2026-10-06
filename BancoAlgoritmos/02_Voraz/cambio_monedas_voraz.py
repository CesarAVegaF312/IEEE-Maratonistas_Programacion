"""
Voraz — Cambio de monedas voraz («Greedy coin change» y sistemas canónicos)
Nivel: Básico
Ejecutar: python cambio_monedas_voraz.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Pagar una cantidad X con el MENOR número de monedas (monedas ilimitadas
    de cada denominación). Con monedas «normales» (1, 2, 5, 10, 20, 50…)
    basta tomar siempre la moneda más grande que quepa; con denominaciones
    arbitrarias eso puede fallar y hay que usar DP.
    Señales en el enunciado: «mínimo número de monedas / billetes /
    paquetes / dardos», denominaciones dadas en la entrada (→ casi siempre
    DP) o fijas y «bonitas» (→ quizá voraz, pero hay que comprobarlo).

FUNCIÓN
    cambio_voraz(monedas, x) -> int | None
        Monedas usadas por el voraz (None si el voraz se atasca).
    cambio_dp(monedas, x) -> int | None
        Mínimo real por DP (None si X no se puede formar).
    primer_contraejemplo(monedas) -> int | None
        Menor X donde el voraz NO es óptimo; None si el sistema es CANÓNICO
        (el voraz es óptimo para todo X). Exige que 1 esté entre las monedas.

IDEA Y ALGORITMO
    Voraz: con las monedas de mayor a menor, usar x // c monedas de c y
    seguir con x % c. Es O(número de monedas).
    ¿Cuándo es correcto? Un sistema es CANÓNICO si el voraz es óptimo para
    TODO X. Ejemplos canónicos: {1,2,5,10,20,50,100,200} (euro),
    {1,5,10,25} (dólar), cualquier {1, b, b², …}. No canónico: {1,3,4}
    con X = 6: voraz 4+1+1 (3 monedas), óptimo 3+3 (2 monedas). El voraz
    se «compromete» con la moneda 4 y ya no puede deshacerlo.
    Detectarlo (Kozen y Zaks, 1994): con monedas 1 = c1 < c2 < … < cn, si
    existe un contraejemplo, el MENOR está en el rango
    c3 + 1 < X < c_{n-1} + c_n. Así que basta comparar voraz contra DP para
    X < c_{n-1} + c_n: si coinciden en todo ese rango, el sistema es
    canónico. (Por qué la cota superior: sea X >= c_{n-1} + c_n el menor
    contraejemplo. Ningún óptimo de X usa c_n: si lo usara, X - c_n sería
    un contraejemplo menor. Tomemos una moneda c < c_n de un óptimo de X:
    X - c >= c_n, el voraz resuelve bien X - c (por minimalidad) y empieza
    con c_n; agregándole c sale un óptimo de X que SÍ usa c_n. Contradicción.)
    DP (siempre correcta): mejor[v] = 1 + min(mejor[v - c]) sobre monedas
    c <= v. Es O(X · n).
    Regla de competencia: si las monedas vienen en la entrada, usar DP.
    Si son fijas, correr primer_contraejemplo una vez en local y decidir.

MACROALGORITMO
    Voraz:
    1. Ordenar monedas de mayor a menor.
    2. Para cada c: cuenta += x // c; x %= c.
    3. Si x quedó en 0, devolver cuenta; si no, None.
    Detección de canonicidad:
    1. Ordenar monedas; si son 1 o 2, el sistema es canónico.
    2. Calcular la DP hasta L = c_{n-1} + c_n.
    3. Devolver el primer X < L con voraz(X) != dp(X), o None.

COMPLEJIDAD
    Voraz: O(n) por consulta (tras ordenar). DP: O(X · n) tiempo, O(X)
    memoria; en Python ~10^7 operaciones por segundo (X·n hasta ~10^7).
    Detección: O((c_{n-1} + c_n) · n).

EJEMPLO A MANO
    monedas {1, 3, 4}, X = 6:
      voraz: 6 // 4 = 1 (queda 2) → 2 // 3 = 0 → 2 // 1 = 2 → 3 monedas
      dp: mejor[3] = 1, mejor[6] = mejor[3] + 1 = 2   → el voraz falla.
    primer_contraejemplo({1,3,4}): rango X < 3 + 4 = 7; X = 6 es el primero.

ERRORES TÍPICOS
    - Aplicar el voraz a monedas que vienen en la entrada: casi nunca es
      canónico garantizado (el enunciado lo diseñó para que falle).
    - Sin moneda 1, el voraz puede atascarse aunque exista solución:
      {3, 5} con X = 9: toma 5, quedan 4, imposible; pero 3+3+3 = 9.
    - En la DP, inicializar mejor[0] = 0 y el resto en infinito (no en 0).
    - Confundir con «número de formas de dar el cambio» (otra DP, se suma
      en lugar de minimizar, y el orden de los ciclos importa).

VARIANTES Y RELACIONADOS
    - 03_ProgramacionDinamica/cambio_monedas_dp.py (la DP completa).
    - Número de formas: formas[v] += formas[v - c] recorriendo monedas por
      fuera (combinaciones) o por dentro (secuencias ordenadas).
    - Monedas limitadas: mochila acotada (DP).
    - Algoritmo de Pearson (1994): decide canonicidad en O(n³) sin la DP
      hasta c_{n-1} + c_n (útil si las monedas son enormes).
    - 02_Voraz/mochila_fraccionaria.py: el caso «divisible», donde el
      voraz sí es siempre óptimo.

DÓNDE PRACTICAR
    - ICPC/OMP 2017 Murcia/E - Prime Darts (monedas = 1 y los primeros
      primos: canónico hasta {1,…,11}, pero con {1,2,3,5,7,11,13} y X = 22
      el voraz da 13+7+2 = 3 dardos y el óptimo 11+11 = 2 → se resuelve con
      DP; ver demo)
    - CSES «Minimizing Coins» (DP); CSES «Coin Combinations I» (formas).
    - UVa 674 «Coin Change» (número de formas).

VERIFICACIÓN
    - Pruebas: voraz y DP contra búsqueda exhaustiva (BFS sobre sumas) en
      300 sistemas aleatorios; primer_contraejemplo contra un barrido
      completo hasta X = 300 en 400 sistemas aleatorios; sistemas canónicos
      conocidos y casos borde (python cambio_monedas_voraz.py)
"""
import random

INF = float("inf")


def cambio_voraz(monedas, x):
    """Número de monedas que usa el voraz (la mayor que quepa); None si se atasca."""
    cuenta = 0
    for c in sorted(monedas, reverse=True):
        cuenta += x // c        # todas las que quepan de esta denominación
        x %= c
    return cuenta if x == 0 else None


def cambio_dp_tabla(monedas, limite):
    """mejor[v] = mínimo de monedas para formar v (INF si no se puede), v <= limite."""
    mejor = [0] + [INF] * limite
    for v in range(1, limite + 1):
        b = INF
        for c in monedas:
            if c <= v and mejor[v - c] + 1 < b:
                b = mejor[v - c] + 1
        mejor[v] = b
    return mejor


def cambio_dp(monedas, x):
    """Mínimo de monedas para formar x por DP; None si es imposible."""
    r = cambio_dp_tabla(monedas, x)[x]
    return None if r == INF else r


def primer_contraejemplo(monedas):
    """Menor X donde el voraz no es óptimo; None si el sistema es canónico.

    Requiere que 1 esté en monedas. Usa la cota de Kozen–Zaks: el menor
    contraejemplo, si existe, es menor que c_{n-1} + c_n.
    """
    c = sorted(set(monedas))
    assert c[0] == 1, "el criterio exige la moneda 1"
    if len(c) <= 2:
        return None             # {1} y {1, b} siempre son canónicos
    limite = c[-1] + c[-2]
    mejor = cambio_dp_tabla(c, limite)
    for x in range(1, limite):
        if cambio_voraz(c, x) != mejor[x]:
            return x
    return None


def demo():
    print("monedas {1,3,4}, X = 6: voraz =", cambio_voraz([1, 3, 4], 6),
          " dp =", cambio_dp([1, 3, 4], 6))                          # 3 vs 2
    print("primer contraejemplo de {1,3,4}:", primer_contraejemplo([1, 3, 4]))  # 6
    print("euro {1,2,5,10,20,50,100,200} canónico:",
          primer_contraejemplo([1, 2, 5, 10, 20, 50, 100, 200]) is None)       # True
    print("{3,5}, X = 9: voraz =", cambio_voraz([3, 5], 9),
          " dp =", cambio_dp([3, 5], 9))                             # None vs 3
    # Monedas de Prime Darts (1 y los primeros primos)
    for areas in ([1, 2, 3, 5, 7], [1, 2, 3, 5, 7, 11, 13]):
        print("Prime Darts", areas, "-> primer contraejemplo:", primer_contraejemplo(areas))


def _optimo_bfs(monedas, x):
    """Fuerza bruta independiente: BFS sobre sumas parciales (cada arista = 1 moneda)."""
    if x == 0:
        return 0
    dist = {0: 0}
    frontera = [0]
    while frontera:
        nueva = []
        for s in frontera:
            for c in monedas:
                t = s + c
                if t <= x and t not in dist:
                    dist[t] = dist[s] + 1
                    if t == x:
                        return dist[t]
                    nueva.append(t)
        frontera = nueva
    return None


def pruebas():
    random.seed(7)

    # Casos borde
    assert cambio_voraz([1], 0) == 0 and cambio_dp([1], 0) == 0
    assert cambio_voraz([5], 3) is None and cambio_dp([5], 3) is None
    assert cambio_voraz([3, 5], 9) is None and cambio_dp([3, 5], 9) == 3
    assert primer_contraejemplo([1]) is None
    assert primer_contraejemplo([1, 7]) is None
    assert primer_contraejemplo([1, 3, 4]) == 6
    assert primer_contraejemplo([1, 5, 10, 25]) is None
    assert primer_contraejemplo([1, 2, 5, 10, 20, 50, 100, 200]) is None
    assert primer_contraejemplo([1, 3, 9, 27, 81]) is None          # potencias
    assert primer_contraejemplo([1, 10, 25]) == 30                  # 25+5·1 vs 10·3

    # Voraz y DP contra BFS exhaustivo
    for _ in range(300):
        monedas = random.sample(range(1, 25), random.randint(1, 5))
        for x in range(0, 40):
            opt = _optimo_bfs(monedas, x)
            assert cambio_dp(monedas, x) == opt
            v = cambio_voraz(monedas, x)
            assert v is None or opt is not None and v >= opt         # nunca mejor que el óptimo

    # primer_contraejemplo contra un barrido completo (la cota de Kozen–Zaks)
    for _ in range(400):
        monedas = [1] + random.sample(range(2, 40), random.randint(1, 5))
        mejor = cambio_dp_tabla(monedas, 300)
        real = next((x for x in range(1, 301) if cambio_voraz(monedas, x) != mejor[x]), None)
        assert primer_contraejemplo(monedas) == real


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
