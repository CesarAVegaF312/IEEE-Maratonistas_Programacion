"""
Programación dinámica — Subsecuencia creciente más larga («Longest Increasing Subsequence», LIS)
Nivel: Básico/Intermedio
Ejecutar: python lis.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Dado un arreglo, encontrar la subsecuencia (no necesariamente contigua,
    respetando el orden) estrictamente creciente más larga, y mostrarla.
    Señales: «la cadena más larga de… donde cada uno es mayor que el
    anterior», «apilar cajas / sobres / torres», «mínimo de elementos a
    borrar para que quede ordenado» (= n - LIS), «cuántas secuencias
    decrecientes cubren el arreglo» (= LIS, teorema de Dilworth). Con
    n ≤ 5000 basta O(n²); con n ≤ 2·10^5 hace falta O(n log n).

FUNCIÓN
    lis_cuadratica(a, estricta=True) -> list
    lis_nlogn(a, estricta=True) -> list
        Devuelven UNA subsecuencia creciente de largo máximo (los valores).
        estricta=False: no decreciente (permite iguales).

IDEA Y ALGORITMO
    O(n²):
      ESTADO      largo[i] = largo de la LIS que TERMINA en a[i].
      TRANSICIÓN  largo[i] = 1 + max{ largo[j] : j < i, a[j] < a[i] }
                  (o 1 si no hay tal j); previo[i] = el j que dio el máximo.
      CASO BASE   largo[i] ≥ 1 (a[i] solo).
      ORDEN       i creciente.
      RESPUESTA   max_i largo[i]; se reconstruye siguiendo previo[] desde el
                  i del máximo y se invierte.
    O(n log n) («paciencia»):
      colas[k] = el MENOR valor en que puede terminar una subsecuencia
      creciente de largo k+1 vista hasta ahora. colas es estrictamente
      creciente (si una de largo k+1 termina en x, quitándole el último
      queda una de largo k que termina en algo < x). Al llegar x:
      con búsqueda binaria se busca el primer k con colas[k] ≥ x; x extiende
      la mejor de largo k (que termina en colas[k-1] < x) y la reemplaza o
      agrega al final. El largo de colas es el largo de la LIS.
      Reconstrucción: se guarda el ÍNDICE que ocupa cada colas[k] y, para
      cada i, previo[i] = índice que estaba en colas[k-1] cuando llegó a[i].
      Para no estricta se usa bisect_right (permite iguales encadenados).

MACROALGORITMO
    (n log n)
    1. colas = [], idx = [], previo = [-1]*n.
    2. Para cada i: k = bisect_left(colas, a[i]).
    3.    Si k == len(colas): agregar; si no: colas[k] = a[i], idx[k] = i.
    4.    previo[i] = idx[k-1] si k > 0.
    5. Reconstruir desde idx[-1] siguiendo previo e invertir.

COMPLEJIDAD
    O(n²) tiempo (n ≤ ~3000 en Python en 1 s) y O(n) memoria.
    O(n log n) tiempo (n = 10^6 en ~1 s con bisect) y O(n) memoria.

EJEMPLO A MANO
    a = [3, 1, 4, 1, 5, 9, 2, 6]
      x=3 colas [3]        x=1 colas [1]        x=4 colas [1,4]
      x=1 colas [1,4]      x=5 colas [1,4,5]    x=9 colas [1,4,5,9]
      x=2 colas [1,2,5,9]  x=6 colas [1,2,5,6]  -> largo 4
    Reconstrucción: 6 <- 5 <- 4 <- 1 (o 3): una LIS es [1, 4, 5, 6].
    OJO: colas al final ([1,2,5,6]) NO es una subsecuencia válida.

ERRORES TÍPICOS
    - Devolver colas como si fuera la subsecuencia (2 aparece después de 5).
    - bisect_left vs bisect_right: left = estrictamente creciente, right =
      no decreciente.
    - LIS en 2D (cajas con dos dimensiones): ordenar por la primera
      creciente y, si empatan, por la segunda DECRECIENTE, y luego LIS
      estricta sobre la segunda (evita encadenar cajas con igual ancho).
    - Olvidar el arreglo vacío.

VARIANTES Y RELACIONADOS
    - Decreciente: LIS sobre los valores negados.
    - Contar cuántas LIS hay: O(n²) guardando también cantidades.
    - Torres de cajas con altura (peso): DP O(n²) con suma (dp_dag.py).
    - lcs.py (LIS de una permutación = LCS con la ordenada), dp_dag.py.

DÓNDE PRACTICAR
    - 2025-2/maraton_problemas/p437_tower_babylon.py (UVa 437: «LIS» de
      cajas en 2D maximizando la altura, O(n²)).
    - Externos: CSES «Increasing Subsequence», «Towers» (Dilworth);
      UVa 481 «What Goes Up» (reconstrucción, n log n); UVa 111 «History
      Grading».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todos los subconjuntos, n ≤ 12) en 800
      casos aleatorios, estrictas y no estrictas, + casos borde; se valida que
      la subsecuencia devuelta sea creciente y esté en a (python lis.py)
"""
import random
from bisect import bisect_left, bisect_right


def lis_cuadratica(a, estricta=True):
    """LIS en O(n²) con reconstrucción por el arreglo previo."""
    n = len(a)
    if n == 0:
        return []
    largo = [1] * n                     # largo[i]: mejor LIS que termina en a[i]
    previo = [-1] * n                   # de dónde vino ese óptimo
    for i in range(n):
        for j in range(i):
            menor = a[j] < a[i] if estricta else a[j] <= a[i]
            if menor and largo[j] + 1 > largo[i]:
                largo[i] = largo[j] + 1
                previo[i] = j
    i = max(range(n), key=largo.__getitem__)
    sec = []
    while i != -1:
        sec.append(a[i])
        i = previo[i]
    return sec[::-1]


def lis_nlogn(a, estricta=True):
    """LIS en O(n log n) con reconstrucción (colas + índices + previo)."""
    busca = bisect_left if estricta else bisect_right
    colas = []                          # colas[k]: menor final de una creciente de largo k+1
    idx = []                            # idx[k]: índice en a de ese final
    previo = [-1] * len(a)
    for i, x in enumerate(a):
        k = busca(colas, x)
        if k == len(colas):
            colas.append(x)
            idx.append(i)
        else:
            colas[k] = x                # x es un final más chico para largo k+1
            idx[k] = i
        previo[i] = idx[k - 1] if k > 0 else -1
    sec = []
    i = idx[-1] if idx else -1
    while i != -1:
        sec.append(a[i])
        i = previo[i]
    return sec[::-1]


def demo():
    a = [3, 1, 4, 1, 5, 9, 2, 6]
    print("a =", a)
    print("lis_cuadratica ->", lis_cuadratica(a))      # largo 4
    print("lis_nlogn      ->", lis_nlogn(a))           # [1, 4, 5, 6]
    print("no estricta de [2, 2, 1, 2] ->", lis_nlogn([2, 2, 1, 2], estricta=False))  # [2, 2, 2]


def pruebas():
    random.seed(481)

    def es_subsecuencia(s, a):
        it = iter(a)
        return all(x in it for x in s)

    def creciente(s, estricta):
        return all((s[i] < s[i + 1]) if estricta else (s[i] <= s[i + 1]) for i in range(len(s) - 1))

    def bruta(a, estricta):
        n, mejor = len(a), 0
        for mask in range(1 << n):
            s = [a[i] for i in range(n) if mask >> i & 1]
            if creciente(s, estricta):
                mejor = max(mejor, len(s))
        return mejor

    # Casos borde
    assert lis_nlogn([]) == lis_cuadratica([]) == []
    assert lis_nlogn([5]) == [5]
    assert len(lis_nlogn([7, 7, 7])) == 1 and len(lis_nlogn([7, 7, 7], False)) == 3
    assert lis_nlogn(list(range(10))) == list(range(10))
    assert len(lis_nlogn(list(range(10, 0, -1)))) == 1

    for _ in range(800):
        n = random.randint(0, 12)
        a = [random.randint(-5, 5) for _ in range(n)]
        for estricta in (True, False):
            esperado = bruta(a, estricta)
            for f in (lis_cuadratica, lis_nlogn):
                s = f(a, estricta)
                assert len(s) == esperado
                assert creciente(s, estricta) and es_subsecuencia(s, a)

    # Arreglos medianos: ambas versiones dan el mismo largo
    for _ in range(30):
        a = [random.randint(1, 1000) for _ in range(300)]
        assert len(lis_cuadratica(a)) == len(lis_nlogn(a))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
