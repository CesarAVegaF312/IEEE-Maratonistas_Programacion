"""
Grafos — Búsqueda en anchura («Breadth-First Search, BFS»)
Nivel: Básico
Ejecutar: python bfs.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular la distancia mínima (en NÚMERO DE ARISTAS) desde un vértice a
    todos los demás en un grafo SIN pesos (o con todos los pesos iguales), y
    reconstruir un camino más corto. También decide alcanzabilidad.
    Señales en el enunciado: «mínimo número de pasos / movimientos / saltos /
    transbordos», laberintos y grillas, «cada movimiento cuesta 1», caballo
    de ajedrez, «¿se puede llegar de A a B?». Si las aristas tienen pesos
    distintos, NO sirve: ver dijkstra.py (o bfs_01.py si los pesos son 0/1).

FUNCIÓN
    bfs(adj, s) -> (dist, padre)
        dist[v] = mínimo número de aristas de s a v, -1 si no se llega.
        padre[v] = vértice anterior a v en un camino más corto (-1 para s y
        para los no alcanzados). Índices desde 0.
    camino(padre, dist, t) -> list
        Vértices de s a t por un camino más corto; [] si t no es alcanzable.
    bfs_multifuente(adj, fuentes) -> dist
        dist[v] = distancia a la fuente MÁS CERCANA (p. ej. «distancia de
        cada celda al fuego más cercano»).

IDEA Y ALGORITMO
    El BFS visita los vértices por CAPAS: primero s (distancia 0), luego
    todos sus vecinos (distancia 1), luego los vecinos de esos que no se
    hayan visto (distancia 2)… Una cola FIFO garantiza el orden: en la cola
    siempre hay vértices de a lo sumo dos distancias consecutivas d y d+1,
    con los de d adelante.
    Por qué la distancia es mínima: si v se descubre por primera vez desde u
    con dist[u] = d, entonces dist[v] ≤ d+1. Si existiera un camino más corto
    (de largo ≤ d), su penúltimo vértice tendría distancia < d y habría
    salido ANTES de la cola, descubriendo a v primero. Por eso basta marcar
    v la PRIMERA vez que se ve y nunca actualizarlo.
    Reconstrucción: guardar padre[v] = u en ese momento. Siguiendo padres
    desde t se vuelve a s por un camino más corto (se arma al revés y se
    invierte).
    Multifuente: meter TODAS las fuentes con distancia 0 en la cola inicial
    equivale a un vértice virtual unido a todas ellas.

MACROALGORITMO
    1. dist = [-1]*n, padre = [-1]*n; dist[s] = 0; cola = deque([s]).
    2. Mientras la cola no esté vacía: u = cola.popleft().
    3. Para cada vecino v de u con dist[v] == -1 (no visto):
       dist[v] = dist[u] + 1, padre[v] = u, cola.append(v).
    4. Para el camino a t: si dist[t] == -1 no hay; si no, seguir padre
       desde t hasta -1 e invertir.

COMPLEJIDAD
    O(n + m) tiempo, O(n) memoria extra. En Python ~10^6 aristas por segundo.

EJEMPLO A MANO
    Aristas (no dirigido): 0-1, 0-2, 1-3, 2-3, 3-4, 5-6; s = 0.
      cola [0]       → saca 0: descubre 1, 2 (dist 1)
      cola [1, 2]    → saca 1: descubre 3 (dist 2, padre 1)
      cola [2, 3]    → saca 2: 3 ya visto, no se toca
      cola [3]       → saca 3: descubre 4 (dist 3)
      dist = [0, 1, 1, 2, 3, -1, -1]; camino a 4: 0 → 1 → 3 → 4.

ERRORES TÍPICOS
    - Marcar como visitado al SACAR de la cola en vez de al METER: el mismo
      vértice entra muchas veces (puede ser exponencial en grillas).
    - Usar list.pop(0) como cola: es O(n) por operación; usar deque.
    - Aplicarlo con pesos distintos: da el camino con menos aristas, no el
      más barato.
    - En grillas, olvidar revisar límites o paredes antes de meter la celda.

VARIANTES Y RELACIONADOS
    - Grillas: vecinos con DIR4/DIR8 (representacion_grafos.py, flood_fill.py).
    - Pesos 0/1: bfs_01.py. Pesos no negativos: dijkstra.py.
    - Estados abstractos (restos, jarras, configuraciones): bfs_estados.py.
    - Componentes y bipartición: componentes_conexas.py, bipartito.py.
    - Fuertemente conexo con dos BFS (grafo y transpuesto); en general, scc.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/C - Knights (BFS en el grafo del caballo + paridad)
    - ICPC/Colombia 2018/I - Impossible Communication (dos BFS: grafo y
      transpuesto)
    - ICPC/Colombia 2018/C - Carrol's Scrabble (BFS por capas con cubetas)
    - ICPC/Colombia 2024/H - Only1s0s (BFS sobre restos, ver bfs_estados.py)
    - CSES «Labyrinth», «Message Route»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (Bellman-Ford con pesos 1) en 1500
      grafos aleatorios, caminos validados arista por arista, multifuente
      contra el mínimo de BFS individuales, y casos borde (python bfs.py)
"""
import random
from collections import deque


def bfs(adj, s):
    """Distancias mínimas (en aristas) desde s y padres para reconstruir caminos."""
    n = len(adj)
    dist = [-1] * n            # -1 = todavía no descubierto
    padre = [-1] * n
    dist[s] = 0
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for v in adj[u]:
            if dist[v] == -1:          # se marca al METER, no al sacar
                dist[v] = dist[u] + 1
                padre[v] = u
                cola.append(v)
    return dist, padre


def camino(padre, dist, t):
    """Camino más corto de la fuente a t (lista de vértices); [] si no se llega."""
    if dist[t] == -1:
        return []
    ruta = []
    while t != -1:             # la fuente es la única alcanzada con padre -1
        ruta.append(t)
        t = padre[t]
    ruta.reverse()
    return ruta


def bfs_multifuente(adj, fuentes):
    """dist[v] = distancia a la fuente más cercana (-1 si ninguna llega)."""
    dist = [-1] * len(adj)
    cola = deque()
    for s in fuentes:
        if dist[s] == -1:
            dist[s] = 0
            cola.append(s)
    while cola:
        u = cola.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                cola.append(v)
    return dist


def _adyacencia(n, aristas, dirigido=False):
    adj = [[] for _ in range(n)]
    for u, v in aristas:
        adj[u].append(v)
        if not dirigido:
            adj[v].append(u)
    return adj


def demo():
    aristas = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (5, 6)]
    adj = _adyacencia(7, aristas)
    dist, padre = bfs(adj, 0)
    print("aristas:", aristas)
    print("dist desde 0:", dist)                       # [0, 1, 1, 2, 3, -1, -1]
    print("camino 0 → 4:", camino(padre, dist, 4))     # [0, 1, 3, 4]
    print("camino 0 → 6:", camino(padre, dist, 6))     # []
    print("multifuente {4, 5}:", bfs_multifuente(adj, [4, 5]))


def pruebas():
    random.seed(7)
    casos = 0

    # Casos borde
    d, p = bfs([[]], 0)
    assert d == [0] and p == [-1] and camino(p, d, 0) == [0]
    d, p = bfs([[0]], 0)                               # lazo
    assert d == [0] and camino(p, d, 0) == [0]
    assert bfs_multifuente([[], []], []) == [-1, -1]

    # Grafo camino largo: sin recursión, no hay problema de profundidad
    n = 200000
    adj = _adyacencia(n, [(i, i + 1) for i in range(n - 1)])
    d, p = bfs(adj, 0)
    assert d[-1] == n - 1 and len(camino(p, d, n - 1)) == n

    for _ in range(1500):
        n = random.randint(1, 9)
        m = random.randint(0, 15)
        dirigido = random.random() < 0.5
        aristas = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
        adj = _adyacencia(n, aristas, dirigido)
        s = random.randrange(n)
        dist, padre = bfs(adj, s)

        # Fuerza bruta: Bellman-Ford con todos los pesos = 1
        INF = float("inf")
        bf = [INF] * n
        bf[s] = 0
        lista = aristas + ([] if dirigido else [(v, u) for u, v in aristas])
        for _ in range(n):
            for u, v in lista:
                if bf[u] + 1 < bf[v]:
                    bf[v] = bf[u] + 1
        assert dist == [-1 if x == INF else x for x in bf]

        # Cada camino reconstruido es válido y tiene largo dist[t]
        conjunto = set(lista)
        for t in range(n):
            ruta = camino(padre, dist, t)
            if dist[t] == -1:
                assert ruta == []
            else:
                assert ruta[0] == s and ruta[-1] == t and len(ruta) == dist[t] + 1
                assert all((ruta[i], ruta[i + 1]) in conjunto for i in range(len(ruta) - 1))

        # Multifuente = mínimo de los BFS individuales
        fuentes = random.sample(range(n), random.randint(1, n))
        esperado = []
        individuales = [bfs(adj, f)[0] for f in fuentes]
        for v in range(n):
            alc = [d[v] for d in individuales if d[v] != -1]
            esperado.append(min(alc) if alc else -1)
        assert bfs_multifuente(adj, fuentes) == esperado
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
