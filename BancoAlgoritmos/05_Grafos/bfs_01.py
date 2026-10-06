"""
Grafos — BFS 0-1 con deque («0-1 BFS»)
Nivel: Intermedio
Ejecutar: python bfs_01.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Distancias mínimas desde un origen cuando cada arista cuesta 0 o 1. Es
    Dijkstra sin montículo: O(n + m) en vez de O(m log m).
    Señales en el enunciado: «mínimo número de paredes a romper», «mínimo
    número de cambios de dirección / de giros», «mínimo de flechas a
    invertir para llegar», «moverse en la dirección de la flecha es gratis,
    cambiarla cuesta 1», «gratis por el mismo color, 1 al cambiar de color».
    Es decir: algunos movimientos son gratis y otros cuestan una unidad.

FUNCIÓN
    bfs01(adj, s) -> dist
        adj[u] = [(v, w)] con w ∈ {0, 1}. dist[v] = costo mínimo de s a v,
        INF = float('inf') si no se llega.
    paredes_a_romper(grilla, origen, destino) -> int
        Ejemplo clásico: grilla de '.' y '#'; entrar a una celda '#' cuesta 1
        (romper la pared), a una '.' cuesta 0. Mínimo de paredes rotas para
        ir de origen a destino (4 vecinos).

IDEA Y ALGORITMO
    Dijkstra necesita sacar siempre el vértice con menor distancia. Con
    pesos 0/1, en todo momento las distancias de los vértices pendientes son
    solo d o d+1 (como en BFS). Una deque mantiene ese orden sin heap:
      · arista de peso 0 → el vecino tiene distancia d: va AL FRENTE;
      · arista de peso 1 → distancia d+1: va AL FINAL.
    Así la deque queda siempre ordenada (frente con d, final con d+1) y
    sacar del frente equivale al heappop de Dijkstra. Igual que en Dijkstra,
    un vértice puede entrar varias veces (si mejora); se guarda (d, v) y se
    descarta la entrada si d > dist[v]. Cada vértice se procesa una vez con
    su distancia final y cada arista se relaja O(1) veces → O(n + m).
    BFS normal NO sirve (contaría las aristas de costo 0 como pasos), y
    Dijkstra sirve pero con un factor log y más constante.

MACROALGORITMO
    1. dist = [INF]*n; dist[s] = 0; dq = deque([(0, s)]).
    2. Mientras dq: (d, u) = dq.popleft(); si d > dist[u], descartar.
    3. Para cada (v, w): si d + w < dist[v]: dist[v] = d + w;
       si w == 0: dq.appendleft((dist[v], v)); si no: dq.append((dist[v], v)).
    4. dist es la respuesta.

COMPLEJIDAD
    O(n + m) tiempo, O(n + m) memoria. En Python ~10^6 aristas por segundo
    (grillas de 1000×1000 en un par de segundos).

EJEMPLO A MANO
    Grilla (S origen, T destino):   S.#.
                                    ##.#
                                    ..#T
    Desde S (0,0): (0,1) gratis; luego (0,2)# o (1,1)# cuestan 1; desde
    (1,2) '.' gratis… El mejor recorrido rompe 2 paredes, p. ej.
    (0,0)→(0,1)→(1,1)#→(1,2)→(2,2)#→(2,3): costo 2. Ninguno rompe solo 1:
    para salir de la zona libre de S {(0,0), (0,1)} hay que entrar a
    (0,2), (1,0) o (1,1), y para llegar a T hay que pasar por (1,3) o
    (2,2); son paredes distintas, así que mínimo 2.

ERRORES TÍPICOS
    - Marcar visitado al meter (como BFS): un vértice metido con d+1 puede
      mejorar después a d por una arista 0.
    - Meter las aristas de costo 0 al final: se rompe el orden de la deque y
      las distancias salen mal.
    - Aplicarlo con pesos distintos de 0 y 1 (p. ej. 0 y 2): usar Dijkstra
      (o dividir pesos si todos son múltiplos).
    - En grillas, poner el costo en la celda de SALIDA en vez de en la de
      llegada (o contar la celda inicial).

VARIANTES Y RELACIONADOS
    - Pesos 0..K pequeños: «Dial» (K+1 cubetas en círculo).
    - Pesos todos 1: bfs.py. Pesos arbitrarios ≥ 0: dijkstra.py.
    - Estados con dirección (mínimo de giros): vértice = (celda, dirección),
      seguir recto cuesta 0 y girar cuesta 1 (ver bfs_estados.py).

DÓNDE PRACTICAR
    - Codeforces 1063B «Labyrinth» (izquierda/derecha limitadas; arriba y
      abajo son gratis → BFS 0-1)
    - Codeforces 173B «Chamber of Secrets»
    - CSES «Labyrinth» como contraste (allí basta BFS normal)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (Bellman-Ford hasta que nada cambie) en
      1500 grafos aleatorios con pesos 0/1 y 500 grillas aleatorias; ejemplo
      de la grilla (python bfs_01.py)
"""
import random
from collections import deque

INF = float("inf")


def bfs01(adj, s):
    """Distancias mínimas desde s con pesos 0/1 usando una deque."""
    n = len(adj)
    dist = [INF] * n
    dist[s] = 0
    dq = deque([(0, s)])
    while dq:
        d, u = dq.popleft()
        if d > dist[u]:                    # entrada vieja (u mejoró después)
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft((nd, v))  # misma distancia: al frente
                else:
                    dq.append((nd, v))      # una más: al final
    return dist


def paredes_a_romper(grilla, origen, destino):
    """Mínimo de celdas '#' que hay que atravesar (4 vecinos); entrar a '#' cuesta 1."""
    F, C = len(grilla), len(grilla[0])
    dist = [[INF] * C for _ in range(F)]
    f0, c0 = origen
    dist[f0][c0] = 0
    dq = deque([(0, f0, c0)])
    while dq:
        d, f, c = dq.popleft()
        if d > dist[f][c]:
            continue
        if (f, c) == destino:              # sale con su distancia definitiva
            return d
        for nf, nc in ((f - 1, c), (f + 1, c), (f, c - 1), (f, c + 1)):
            if 0 <= nf < F and 0 <= nc < C:
                w = 1 if grilla[nf][nc] == '#' else 0   # costo de ENTRAR a la celda
                if d + w < dist[nf][nc]:
                    dist[nf][nc] = d + w
                    if w == 0:
                        dq.appendleft((d, nf, nc))
                    else:
                        dq.append((d + 1, nf, nc))
    return dist[destino[0]][destino[1]]


def demo():
    grilla = ["S.#.",
              "##.#",
              "..#T"]
    for fila in grilla:
        print("   ", fila)
    print("paredes a romper de S a T:", paredes_a_romper(grilla, (0, 0), (2, 3)))  # 2
    adj = [[(1, 1), (2, 0)], [(3, 0)], [(1, 0), (3, 1)], []]
    print("grafo 0→1(1), 0→2(0), 1→3(0), 2→1(0), 2→3(1): dist =", bfs01(adj, 0))  # [0,0,0,0]


def pruebas():
    random.seed(173)
    casos = 0

    assert bfs01([[]], 0) == [0]
    assert bfs01([[(1, 1)], []], 0) == [0, 1]
    assert bfs01([[], []], 0) == [0, INF]
    assert paredes_a_romper(["#"], (0, 0), (0, 0)) == 0
    assert paredes_a_romper(["S#T"], (0, 0), (0, 2)) == 1

    for _ in range(1500):
        n = random.randint(1, 9)
        m = random.randint(0, 20)
        adj = [[] for _ in range(n)]
        lista = []
        for _ in range(m):
            u, v, w = random.randrange(n), random.randrange(n), random.randint(0, 1)
            adj[u].append((v, w))
            lista.append((u, v, w))
        s = random.randrange(n)
        # Fuerza bruta: relajar todas las aristas hasta que nada cambie
        bf = [INF] * n
        bf[s] = 0
        cambio = True
        while cambio:
            cambio = False
            for u, v, w in lista:
                if bf[u] + w < bf[v]:
                    bf[v] = bf[u] + w
                    cambio = True
        assert bfs01(adj, s) == bf
        casos += 1

    for _ in range(500):
        F, C = random.randint(1, 5), random.randint(1, 5)
        grilla = ["".join(random.choice("..#") for _ in range(C)) for _ in range(F)]
        o = (random.randrange(F), random.randrange(C))
        t = (random.randrange(F), random.randrange(C))
        # Bruta: Bellman-Ford sobre las celdas
        dist = {(f, c): INF for f in range(F) for c in range(C)}
        dist[o] = 0
        cambio = True
        while cambio:
            cambio = False
            for (f, c), d in list(dist.items()):
                for nf, nc in ((f - 1, c), (f + 1, c), (f, c - 1), (f, c + 1)):
                    if (nf, nc) in dist:
                        w = 1 if grilla[nf][nc] == '#' else 0
                        if d + w < dist[(nf, nc)]:
                            dist[(nf, nc)] = d + w
                            cambio = True
        assert paredes_a_romper(grilla, o, t) == dist[t]
        casos += 1

    # Grilla grande: tiempo razonable
    N = 300
    g = ["".join(random.choice(".#") for _ in range(N)) for _ in range(N)]
    assert paredes_a_romper(g, (0, 0), (N - 1, N - 1)) < INF
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
