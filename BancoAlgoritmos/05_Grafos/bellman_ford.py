"""
Grafos — Bellman-Ford y ciclos negativos («Bellman-Ford algorithm»)
Nivel: Intermedio
Ejecutar: python bellman_ford.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Distancias mínimas desde un origen cuando hay pesos NEGATIVOS (donde
    Dijkstra falla), detectando además los ciclos negativos: si se puede
    dar vueltas en un ciclo de costo total < 0, algunas distancias son −∞.
    Señales en el enunciado: «ganancias y pérdidas», «agujeros de gusano que
    viajan al pasado», «arbitraje de monedas», «¿se puede ganar
    infinitamente?», «encuentra un ciclo de costo negativo», restricciones
    de diferencias xj − xi ≤ c. Tamaño típico n·m ≤ ~10^7 (en Python, menos).

FUNCIÓN
    bellman_ford(n, aristas, s) -> dist
        aristas = [(u, v, w)] DIRIGIDAS (para no dirigido con w ≥ 0 meter
        ambas; con w < 0 una arista no dirigida ya es un ciclo negativo).
        dist[v] = costo mínimo de s a v; INF si no se llega; -INF si se
        puede hacer tan pequeño como se quiera (un ciclo negativo alcanzable
        desde s que a su vez alcanza a v).
    ciclo_negativo(n, aristas) -> list
        Vértices [x0, x1, …, xk-1] de un ciclo negativo cualquiera del grafo
        (aristas x0→x1→…→xk-1→x0), o [] si no hay.

IDEA Y ALGORITMO
    «Relajar» una arista (u, v, w) = dist[v] = min(dist[v], dist[u] + w).
    Si no hay ciclos negativos, un camino mínimo es SIMPLE (sin repetir
    vértices) y tiene ≤ n−1 aristas. Tras la ronda i de relajar TODAS las
    aristas, dist[v] es ≤ el mejor costo con ≤ i aristas (inducción: el
    último tramo del camino óptimo de i aristas se relajó en la ronda i).
    Así, n−1 rondas bastan.
    Ciclo negativo: si en una ronda n TODAVÍA mejora algo, existe un ciclo
    negativo (sin él, todo estaba ya fijo). Para marcar los −∞: hacer n
    rondas más en las que cualquier vértice que mejore pasa a −INF; −INF se
    propaga por las aristas (−inf + w = −inf) a todo lo alcanzable.
    Encontrar el ciclo: arrancar con dist = 0 en todos (un origen virtual
    unido a todos con peso 0) y guardar padre[v] al relajar. Si en la ronda
    n se relaja x, retroceder n veces por padre desde x deja un vértice
    DENTRO del ciclo (la cadena de padres de largo n tiene que haber
    entrado en él); desde ahí se sigue padre hasta volver al mismo vértice.
    Mejora útil: cortar en cuanto una ronda no cambia nada.

MACROALGORITMO
    1. dist = [INF]*n; dist[s] = 0.
    2. Repetir n−1 veces: para cada (u, v, w): si dist[u] + w < dist[v],
       actualizar (si ninguna arista cambió, salir antes).
    3. Repetir n veces más: si dist[u] + w < dist[v] (con dist[u] ≠ INF),
       dist[v] = −INF (afectado por un ciclo negativo).
    4. Ciclo: dist = 0 en todos, n rondas con padre; si en la ronda n se
       relaja x: x = padre[x] n veces; recorrer padres hasta repetir x;
       invertir (los padres van hacia atrás).

COMPLEJIDAD
    O(n·m) tiempo, O(n) memoria. En Python ~10^6–10^7 relajaciones por
    segundo con bucles simples: n·m ≤ ~5·10^6 es seguro.

EJEMPLO A MANO
    Aristas: 0→1 (4), 0→2 (5), 2→1 (−3), 1→3 (2), 3→4 (1), 4→3 (−2); s = 0.
      Ronda 1 (en este orden): dist[1]=4, dist[2]=5, dist[1]=2, dist[3]=4,
               dist[4]=5, dist[3]=3.
      El ciclo 3→4→3 cuesta 1 − 2 = −1 < 0 y se alcanza desde 0, así que
      dist[3] y dist[4] = −INF; dist = [0, 2, 5, −INF, −INF].
      ciclo_negativo → [3, 4] (o [4, 3]).

ERRORES TÍPICOS
    - Relajar desde vértices con dist = INF: INF + (−5) sigue siendo INF con
      float, pero con un INF entero (10^18) produce valores falsos.
    - Concluir «hay ciclo negativo, todo es −∞»: solo lo son los vértices
      alcanzables DESDE el ciclo (y el ciclo debe ser alcanzable desde s).
    - Hacer solo n−1 rondas y no revisar la n-ésima.
    - Sacar el ciclo desde x directamente sin retroceder n veces: x puede
      estar FUERA del ciclo (colgando de él).

VARIANTES Y RELACIONADOS
    - SPFA (cola de vértices que cambiaron): más rápido en promedio, mismo
      peor caso.
    - Restricciones de diferencias: xj − xi ≤ c ↦ arista i→j con peso c;
      factible ⇔ no hay ciclo negativo.
    - Todos los pares con negativos: floyd_warshall.py (dist[i][i] < 0).
    - Sin negativos: dijkstra.py (mucho más rápido).

DÓNDE PRACTICAR
    - CSES «High Score» (−∞ y +∞ propagados), «Cycle Finding»
    - UVa 558 «Wormholes» (¿existe ciclo negativo?)

VERIFICACIÓN
    - Pruebas: OK en 2000 grafos aleatorios con pesos −6..9 contra fuerza
      bruta: enumerar TODOS los caminos simples (distancias sin ciclo
      negativo) y Floyd–Warshall con dist[c][c] < 0 para decidir qué
      vértices son −∞; ciclos devueltos validados (aristas existen, suma < 0)
      (python bellman_ford.py)
"""
import random

INF = float("inf")


def bellman_ford(n, aristas, s):
    """Distancias desde s con pesos negativos; -INF donde influye un ciclo negativo."""
    dist = [INF] * n
    dist[s] = 0
    for _ in range(n - 1):
        cambio = False
        for u, v, w in aristas:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                cambio = True
        if not cambio:              # ya estable: no hay ciclo negativo alcanzable
            return dist
    # n rondas más: lo que todavía mejora depende de un ciclo negativo.
    # -INF se propaga solo porque -inf + w = -inf < cualquier valor finito.
    for _ in range(n):
        cambio = False
        for u, v, w in aristas:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = -INF
                cambio = True
        if not cambio:
            break
    return dist


def ciclo_negativo(n, aristas):
    """Algún ciclo de peso total < 0 como lista de vértices en orden; [] si no hay."""
    dist = [0] * n                 # origen virtual unido a todos con peso 0
    padre = [-1] * n
    x = -1
    for _ in range(n):
        x = -1
        for u, v, w in aristas:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                padre[v] = u
                x = v
        if x == -1:                # una ronda sin cambios: no hay ciclo negativo
            return []
    # x se relajó en la ronda n: retroceder n veces asegura caer DENTRO del ciclo
    for _ in range(n):
        x = padre[x]
    ciclo = [x]
    v = padre[x]
    while v != x:
        ciclo.append(v)
        v = padre[v]
    ciclo.reverse()                # los padres recorren el ciclo al revés
    return ciclo


def demo():
    aristas = [(0, 1, 4), (0, 2, 5), (2, 1, -3), (1, 3, 2), (3, 4, 1), (4, 3, -2)]
    print("aristas (u, v, w):", aristas)
    print("bellman_ford desde 0:", bellman_ford(5, aristas, 0))  # [0, 2, 5, -inf, -inf]
    print("ciclo negativo:", ciclo_negativo(5, aristas))
    sin = aristas[:4]
    print("sin el ciclo 3↔4:", bellman_ford(5, sin, 0), "ciclo:", ciclo_negativo(5, sin))


def _bruta(n, aristas, s):
    """Distancias por fuerza bruta.

    - Floyd–Warshall: neg[c] = c está en un ciclo negativo (dist[c][c] < 0).
    - v es -INF ⇔ existe c con neg[c], s alcanza c y c alcanza v.
    - Si no, el mínimo es sobre caminos SIMPLES (se enumeran todos).
    """
    D = [[INF] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0
    for u, v, w in aristas:
        D[u][v] = min(D[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
    neg = [D[c][c] < 0 for c in range(n)]
    res = []
    for v in range(n):
        if any(neg[c] and D[s][c] < INF and D[c][v] < INF for c in range(n)):
            res.append(-INF)
            continue
        mejor = 0 if v == s else INF
        pila = [(s, 0, 1 << s)]          # enumerar todos los caminos simples
        while pila:
            u, costo, usados = pila.pop()
            for a, b, w in aristas:
                if a == u and not usados >> b & 1:
                    if b == v:
                        mejor = min(mejor, costo + w)
                    pila.append((b, costo + w, usados | 1 << b))
        res.append(mejor)
    return res, any(neg)


def pruebas():
    random.seed(558)
    casos = 0

    assert bellman_ford(1, [], 0) == [0]
    assert bellman_ford(1, [(0, 0, -1)], 0) == [-INF]        # lazo negativo
    assert ciclo_negativo(1, [(0, 0, -1)]) == [0]
    assert ciclo_negativo(2, [(0, 1, -5)]) == []
    assert bellman_ford(3, [(1, 2, -1), (2, 1, -1)], 0) == [0, INF, INF]  # ciclo no alcanzable

    for _ in range(2000):
        n = random.randint(1, 6)
        m = random.randint(0, 10)
        aristas = [(random.randrange(n), random.randrange(n), random.randint(-6, 9))
                   for _ in range(m)]
        s = random.randrange(n)
        esperado, hay_neg = _bruta(n, aristas, s)
        assert bellman_ford(n, aristas, s) == esperado

        ciclo = ciclo_negativo(n, aristas)
        assert bool(ciclo) == hay_neg
        if ciclo:
            assert len(set(ciclo)) == len(ciclo)            # vértices distintos
            peso_min = {}
            for u, v, w in aristas:
                peso_min[(u, v)] = min(w, peso_min.get((u, v), INF))
            k = len(ciclo)
            pares = [(ciclo[i], ciclo[(i + 1) % k]) for i in range(k)]
            assert all(p in peso_min for p in pares)
            assert sum(peso_min[p] for p in pares) < 0
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
