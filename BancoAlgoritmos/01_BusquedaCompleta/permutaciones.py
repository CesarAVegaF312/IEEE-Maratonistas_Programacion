"""
Búsqueda completa — Permutaciones («Permutations / next_permutation»)
Nivel: Básico
Ejecutar: python permutaciones.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Probar todos los ÓRDENES posibles de N elementos (N! en total) cuando el
    problema pide el mejor orden, o generar la permutación siguiente en
    orden lexicográfico (incluso con elementos repetidos).
    Señales en el enunciado: N ≤ 8–10, «en qué orden…», «visitar todas las
    ciudades», «todas las cadenas que se forman reordenando las letras»,
    «el siguiente código en orden alfabético».

FUNCIÓN
    siguiente_permutacion(a) -> bool
        Transforma la lista a EN SU LUGAR en la siguiente permutación
        lexicográfica (como next_permutation de C++). Si a ya es la última
        (no creciente), la deja ordenada ascendente y devuelve False.
        Funciona con repetidos (no genera duplicados).
    permutaciones_distintas(a) -> list[tuple]
        Todas las permutaciones distintas de a, en orden lexicográfico.
    ruta_minima(dist) -> int
        Viajante (TSP) por fuerza bruta: costo mínimo de un ciclo que sale
        de la ciudad 0, visita todas y vuelve. dist es una matriz n×n.

IDEA Y ALGORITMO
    itertools.permutations(a) genera las n! permutaciones por POSICIÓN:
    con repetidos produce duplicados (permutations("aab") da 6, no 3), y
    sigue el orden de entrada (lexicográfico solo si a está ordenada).
    Siguiente permutación (algoritmo de Narayana):
      1. Buscar desde la derecha el primer i con a[i] < a[i+1]. Todo lo que
         está a la derecha de i es NO CRECIENTE: ya es la permutación más
         grande de esos elementos, así que hay que cambiar a[i].
      2. Si no existe i: es la última; invertir todo (queda la primera).
      3. Buscar desde la derecha el primer j con a[j] > a[i] (el menor
         valor mayor que a[i] en la cola, y el más a la derecha si se repite).
      4. Intercambiar a[i] y a[j]: la cola sigue no creciente.
      5. Invertir la cola a[i+1:] para dejarla creciente (la más pequeña).
    Usar comparaciones estrictas (<, >) es lo que hace que con repetidos no
    se generen duplicados: siempre se salta a la siguiente DISTINTA.
    Viajante: fijar la ciudad inicial (0) evita contar n veces el mismo
    ciclo rotado: (n−1)! órdenes en vez de n!.

MACROALGORITMO
    (Siguiente permutación)
    1. i = n − 2; mientras i ≥ 0 y a[i] ≥ a[i+1]: i −= 1.
    2. Si i < 0: a.reverse(); devolver False.
    3. j = n − 1; mientras a[j] ≤ a[i]: j −= 1.
    4. Intercambiar a[i], a[j].
    5. Invertir a[i+1:]; devolver True.
    (Todas las distintas)
    6. Ordenar a; repetir: guardar tuple(a) mientras siguiente_permutacion(a).

COMPLEJIDAD
    siguiente_permutacion: O(n) en el peor caso, O(1) amortizado.
    Todas: O(n! · n). En Python, 8! = 40320 sin problema; 10! = 3,6·10^6
    con itertools (en C) ~1 s solo de generar; con lógica encima, apretado.
    ruta_minima: O((n−1)! · n); n ≤ 9–10.

EJEMPLO A MANO
    a = [1, 3, 5, 4, 2]
      1. i: desde la derecha, 4>2, 5>4, 3<5 → i = 1 (a[i] = 3)
      3. j: desde la derecha, el primero > 3 es 4 → j = 3
      4. intercambiar → [1, 4, 5, 3, 2]
      5. invertir la cola [5, 3, 2] → [1, 4, 2, 3, 5]
    Con repetidos: "aab" → "aba" → "baa" → (False, vuelve a "aab").

ERRORES TÍPICOS
    - Usar itertools.permutations con repetidos y contar duplicados (usar
      set(...) o siguiente_permutacion desde la lista ordenada).
    - Olvidar ordenar antes de iterar con siguiente_permutacion: se pierden
      las permutaciones «menores» que la inicial.
    - Usar ≤ / ≥ al revés en los pasos 1 y 3: con repetidos se cicla o se
      saltan permutaciones.
    - Intentar n = 12 (4,8·10^8 permutaciones): ahí va DP sobre máscaras
      (viajante en O(2^n · n²)) o backtracking con poda.

VARIANTES Y RELACIONADOS
    - Permutación anterior: mismo algoritmo con las comparaciones invertidas.
    - k-ésima permutación directa con el sistema factorial.
    - Combinaciones: itertools.combinations; subconjuntos: subconjuntos_mascaras.py.
    - Con restricciones que permiten cortar ramas: backtracking_poda.py.

DÓNDE PRACTICAR
    - UVa 146 «ID Codes» (siguiente permutación con repetidos)
    - CSES «Creating Strings» (todas las permutaciones distintas de una cadena)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (sorted(set(itertools.permutations)))
      en 1500 listas aleatorias con repetidos, contra el siguiente elemento
      de esa lista ordenada, y el viajante contra un DP sobre máscaras en
      300 matrices + casos borde (python permutaciones.py)
"""
import itertools
import random


def siguiente_permutacion(a):
    """Siguiente permutación lexicográfica de a, en su lugar. False si era la última."""
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1                      # a[i+1:] es no creciente: no se puede mejorar ahí
    if i < 0:
        a.reverse()                 # era la última: volver a la primera
        return False
    j = n - 1
    while a[j] <= a[i]:
        j -= 1                      # menor valor > a[i] en la cola (el de más a la derecha)
    a[i], a[j] = a[j], a[i]
    a[i + 1:] = a[i + 1:][::-1]     # la cola queda creciente: la menor posible
    return True


def permutaciones_distintas(a):
    """Todas las permutaciones distintas de a, en orden lexicográfico."""
    a = sorted(a)
    res = [tuple(a)]
    while siguiente_permutacion(a):
        res.append(tuple(a))
    return res


def ruta_minima(dist):
    """Costo mínimo de un ciclo desde la ciudad 0 por todas las ciudades (fuerza bruta)."""
    n = len(dist)
    if n == 1:
        return 0
    mejor = None
    for orden in itertools.permutations(range(1, n)):   # ciudad 0 fija: (n-1)! órdenes
        costo = dist[0][orden[0]] + dist[orden[-1]][0]
        for u, v in zip(orden, orden[1:]):
            costo += dist[u][v]
        if mejor is None or costo < mejor:
            mejor = costo
    return mejor


def demo():
    a = [1, 3, 5, 4, 2]
    print("siguiente de", a, end=" → ")
    siguiente_permutacion(a)
    print(a)                                                      # [1, 4, 2, 3, 5]
    print("permutaciones_distintas('aab') =", ["".join(p) for p in permutaciones_distintas("aab")])
    for codigo in ("abaacb", "cbbaa"):                            # ejemplo de UVa 146
        l = list(codigo)
        print(codigo, "→", "".join(l) if siguiente_permutacion(l) else "No Successor")
    dist = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
    print("ruta_minima (4 ciudades) =", ruta_minima(dist))        # 80


def _tsp_dp(dist):
    """Referencia independiente: DP de Held–Karp sobre máscaras."""
    n = len(dist)
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for m in range(1 << n):
        for u in range(n):
            if dp[m][u] == INF:
                continue
            for v in range(n):
                if not m >> v & 1:
                    nm = m | 1 << v
                    dp[nm][v] = min(dp[nm][v], dp[m][u] + dist[u][v])
    total = (1 << n) - 1
    return min(dp[total][u] + dist[u][0] for u in range(n)) if n > 1 else 0


def pruebas():
    random.seed(146)

    # Casos borde y ejemplo de UVa 146
    vacia = []
    assert siguiente_permutacion(vacia) is False and vacia == []
    uno = [7]
    assert siguiente_permutacion(uno) is False and uno == [7]
    l = list("abaacb")
    assert siguiente_permutacion(l) and "".join(l) == "ababac"
    l = list("cbbaa")
    assert not siguiente_permutacion(l) and "".join(l) == "aabbc"
    assert permutaciones_distintas([2, 2, 2]) == [(2, 2, 2)]
    assert len(permutaciones_distintas("aabb")) == 6

    for _ in range(1500):
        n = random.randint(0, 6)
        a = [random.randint(1, 3) for _ in range(n)]
        todas = sorted(set(itertools.permutations(a)))
        assert permutaciones_distintas(a) == todas
        # desde una permutación cualquiera, la siguiente es la de la lista
        b = list(random.choice(todas))
        k = todas.index(tuple(b))
        hay = siguiente_permutacion(b)
        if k + 1 < len(todas):
            assert hay and tuple(b) == todas[k + 1]
        else:
            assert not hay and tuple(b) == todas[0]

    for _ in range(300):
        n = random.randint(1, 7)
        dist = [[0 if i == j else random.randint(1, 50) for j in range(n)] for i in range(n)]
        assert ruta_minima(dist) == _tsp_dp(dist)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
