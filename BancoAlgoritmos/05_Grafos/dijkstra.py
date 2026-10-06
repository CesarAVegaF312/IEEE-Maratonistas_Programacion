"""
Grafos — Dijkstra con montículo («Dijkstra's algorithm»)
Nivel: Intermedio
Ejecutar: python dijkstra.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Distancias mínimas desde un origen a todos los vértices en un grafo
    (dirigido o no) con pesos NO NEGATIVOS, y reconstrucción del camino.
    Señales en el enunciado: «tiempo / costo / distancia mínima de A a B»,
    aristas con pesos distintos (latencias, kilómetros, peajes), n y m hasta
    ~10^5–2·10^5. Si todos los pesos son iguales basta bfs.py; si son 0/1,
    bfs_01.py; si hay pesos negativos, bellman_ford.py; si se piden TODOS
    los pares con n ≤ ~400, floyd_warshall.py.

FUNCIÓN
    dijkstra(adj, s) -> (dist, padre)
        adj[u] = [(v, w), ...] con w ≥ 0. dist[v] = costo mínimo de s a v
        (INF = float('inf') si no se llega). padre[v] = vértice anterior en
        un camino mínimo (-1 para s y los no alcanzados).
    camino(padre, dist, t) -> list    vértices de s a t; [] si no se llega.
    resolver_uva10986(texto) -> str
        UVa 10986 «Sending email» completo («Case #x: d» o «unreachable»).

IDEA Y ALGORITMO
    Se mantiene una estimación dist[v] (mejor costo conocido) y se extrae
    SIEMPRE el vértice no definitivo con dist más pequeña. Ese valor ya es
    óptimo: cualquier otro camino a u tiene que salir del conjunto de
    vértices definitivos por algún vértice x con dist[x] ≥ dist[u], y como
    los pesos son ≥ 0 el resto del camino no puede bajar el costo. (Con un
    peso negativo este argumento se rompe: por eso Dijkstra falla ahí.)
    Al fijar u se «relajan» sus aristas: si dist[u] + w < dist[v], se
    mejora dist[v] y se anota padre[v] = u.
    Implementación con heapq: Python no tiene «disminuir clave», así que
    cada mejora mete una entrada NUEVA (d, v) al montículo; las entradas
    viejas de v quedan adentro con d mayor y se DESCARTAN al sacarlas
    (si d > dist[v], ya se procesó v con un valor mejor). Hay a lo sumo m
    entradas en el montículo.

MACROALGORITMO
    1. dist = [INF]*n, dist[s] = 0, padre = [-1]*n, heap = [(0, s)].
    2. Mientras el heap no esté vacío: (d, u) = heappop(heap).
    3. Si d > dist[u]: entrada vieja, continuar.
    4. Para cada (v, w) de adj[u]: si d + w < dist[v]:
         dist[v] = d + w, padre[v] = u, heappush(heap, (dist[v], v)).
    5. Camino a t: seguir padre desde t e invertir.

COMPLEJIDAD
    O((n + m) log m) tiempo, O(n + m) memoria. En Python ~2–5·10^5 aristas
    por segundo (heapq está en C; el bucle de relajación es el costo).

EJEMPLO A MANO
    No dirigido: 0-1 (4), 0-2 (1), 2-1 (2), 1-3 (5), 2-3 (8); s = 0.
      heap [(0,0)]          saca 0: dist[1]=4, dist[2]=1
      heap [(1,2),(4,1)]    saca 2: dist[1]=1+2=3 ✓, dist[3]=1+8=9
      heap [(3,1),(4,1),(9,3)] saca 1: dist[3]=3+5=8 ✓
      heap [(4,1),(8,3),(9,3)] saca (4,1): 4 > dist[1]=3 → DESCARTAR
      saca (8,3): fija 3; saca (9,3): descartar.
    dist = [0, 3, 1, 8]; camino a 3: 0 → 2 → 1 → 3.

ERRORES TÍPICOS
    - No descartar entradas viejas (if d > dist[u]: continue): sigue siendo
      correcto pero puede volverse O(m²) en el peor caso.
    - Usar «visitado al meter» como en BFS: un vértice puede mejorar
      después de haberse metido; se fija al SACARLO.
    - Pesos negativos: respuestas incorrectas sin ningún error visible.
    - Comparar INF con enteros grandes mal elegidos (10^9 puede quedarse
      corto si los costos suman hasta 10^14); float('inf') o 1 << 62.
    - Guardar en el heap (v, d) en vez de (d, v): ordena por vértice.

VARIANTES Y RELACIONADOS
    - Multifuente: meter todas las fuentes con distancia 0.
    - Grafo de estados (vértice, cosas usadas): Dijkstra sobre pares
      (ver bfs_estados.py para la idea con BFS).
    - Número de caminos mínimos: contar al relajar con igualdad.
    - Pesos 0/1: bfs_01.py; negativos: bellman_ford.py; todos los pares:
      floyd_warshall.py.

DÓNDE PRACTICAR
    - 2026-1/problemas/10986 - Sending email (maratón interna 2026-1;
      UVa 10986 «Sending email»)
    - CSES «Shortest Routes I», «Flight Discount» (Dijkstra sobre estados)
    - Codeforces 20C «Dijkstra?» (reconstruir el camino)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (Bellman-Ford) en 1500 grafos
      aleatorios dirigidos y no dirigidos con pesos 0..20 y aristas
      repetidas, caminos validados (suma de pesos = dist), ejemplo de
      UVa 10986 de la maratón interna (python dijkstra.py)
"""
import heapq
import random

INF = float("inf")


def dijkstra(adj, s):
    """Distancias mínimas desde s con pesos >= 0; también padres para el camino."""
    n = len(adj)
    dist = [INF] * n
    padre = [-1] * n
    dist[s] = 0
    heap = [(0, s)]                       # (distancia, vértice): ordena por distancia
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                   # entrada vieja: u ya salió con algo mejor
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                padre[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, padre


def camino(padre, dist, t):
    """Vértices de la fuente a t por un camino mínimo; [] si no se llega."""
    if dist[t] == INF:
        return []
    ruta = []
    while t != -1:
        ruta.append(t)
        t = padre[t]
    ruta.reverse()
    return ruta


def resolver_uva10986(texto):
    """UVa 10986 Sending email: N casos «n m S T» + m aristas no dirigidas."""
    tokens = iter(texto.split())
    casos = int(next(tokens))
    salida = []
    for caso in range(1, casos + 1):
        n, m, S, T = (int(next(tokens)) for _ in range(4))
        adj = [[] for _ in range(n)]
        for _ in range(m):
            u, v, w = int(next(tokens)), int(next(tokens)), int(next(tokens))
            adj[u].append((v, w))
            adj[v].append((u, w))
        d = dijkstra(adj, S)[0][T]
        salida.append(f"Case #{caso}: " + ("unreachable" if d == INF else str(d)))
    return "\n".join(salida)


# Ejemplo de la maratón interna 2026-1 (5 casos)
EJEMPLO_10986 = """5
2 1 0 1
0 1 1000
3 3 2 1
0 1 1000
1 2 15
2 1 20
2 1 0 1
0 1 100
3 3 2 0
0 1 100
0 2 200
1 2 50
2 0 0 1
"""


def _adyacencia(n, aristas, dirigido=False):
    adj = [[] for _ in range(n)]
    for u, v, w in aristas:
        adj[u].append((v, w))
        if not dirigido:
            adj[v].append((u, w))
    return adj


def demo():
    aristas = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 5), (2, 3, 8)]
    dist, padre = dijkstra(_adyacencia(4, aristas), 0)
    print("aristas (u, v, w):", aristas)
    print("dist desde 0:", dist)                        # [0, 3, 1, 8]
    print("camino 0 → 3:", camino(padre, dist, 3))      # [0, 2, 1, 3]
    print("Ejemplo UVa 10986 (maratón interna 2026-1):")
    print(resolver_uva10986(EJEMPLO_10986))


def pruebas():
    random.seed(10986)
    casos = 0

    assert resolver_uva10986(EJEMPLO_10986) == "\n".join([
        "Case #1: 1000", "Case #2: 15", "Case #3: 100", "Case #4: 150",
        "Case #5: unreachable"])
    assert dijkstra([[]], 0) == ([0], [-1])
    assert dijkstra([[(0, 5)]], 0)[0] == [0]               # lazo
    assert dijkstra([[(1, 0)], []], 0)[0] == [0, 0]        # peso 0

    # Grafo grande: camino de 10^5 con atajos (tiempo razonable, sin recursión)
    n = 100000
    ar = [(i, i + 1, 1) for i in range(n - 1)] + [(0, n - 1, n)]
    assert dijkstra(_adyacencia(n, ar), 0)[0][n - 1] == n - 1

    for _ in range(1500):
        n = random.randint(1, 9)
        m = random.randint(0, 20)
        dirigido = random.random() < 0.5
        aristas = [(random.randrange(n), random.randrange(n), random.randint(0, 20))
                   for _ in range(m)]
        adj = _adyacencia(n, aristas, dirigido)
        s = random.randrange(n)
        dist, padre = dijkstra(adj, s)

        # Fuerza bruta: Bellman-Ford (relajar todas las aristas n veces)
        lista = aristas + ([] if dirigido else [(v, u, w) for u, v, w in aristas])
        bf = [INF] * n
        bf[s] = 0
        for _ in range(n):
            for u, v, w in lista:
                if bf[u] + w < bf[v]:
                    bf[v] = bf[u] + w
        assert dist == bf

        # El camino reconstruido existe y suma exactamente dist[t]
        peso = {}
        for u, v, w in lista:
            peso[(u, v)] = min(w, peso.get((u, v), INF))
        for t in range(n):
            ruta = camino(padre, dist, t)
            if dist[t] == INF:
                assert ruta == []
            else:
                assert ruta[0] == s and ruta[-1] == t
                assert sum(peso[(ruta[i], ruta[i + 1])] for i in range(len(ruta) - 1)) == dist[t]
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
