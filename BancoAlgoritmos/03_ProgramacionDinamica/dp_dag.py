"""
Programación dinámica — DP sobre un DAG con orden topológico («DP on DAG»)
Nivel: Intermedio
Ejecutar: python dp_dag.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Toda DP es, en el fondo, un cálculo sobre un grafo dirigido ACÍCLICO
    (DAG): los estados son nodos y «el estado v depende de u» es una arista
    u -> v. Cuando el problema YA es un grafo dirigido sin ciclos (tareas
    con prerrequisitos, vuelos que solo avanzan en el tiempo, cajas que se
    apilan, niveles de un juego), la DP se hace recorriendo los nodos en
    ORDEN TOPOLÓGICO. Dos clásicos:
      - Camino más largo (o de peso máximo): en grafos generales es NP-duro,
        en un DAG es lineal.
      - Número de caminos de s a t.
    Señales: «dirigido y sin ciclos», «solo se puede avanzar», «cada tarea
    depende de otras», «cuántas rutas distintas», n, m ≤ 2·10^5.

FUNCIÓN
    orden_topologico(n, aristas) -> list | None
        Kahn; None si hay un ciclo. aristas = [(u, v, peso)] o [(u, v)].
    camino_mas_largo(n, aristas) -> (int, list)
        Mayor peso de un camino (puede empezar y terminar en cualquier nodo;
        un solo nodo vale 0) y los nodos de ese camino.
    contar_caminos(n, aristas, s, t, mod=None) -> int
        Número de caminos dirigidos de s a t.

IDEA Y ALGORITMO
    Orden topológico (Kahn): repetidamente sacar un nodo sin aristas
    entrantes pendientes. En ese orden, toda arista va de un nodo anterior a
    uno posterior, así que al procesar v todos sus predecesores ya están
    terminados: es el ORDEN de la DP.
    Camino más largo:
      ESTADO      dp[v] = mayor peso de un camino que TERMINA en v.
      TRANSICIÓN  dp[v] = max(0, max_{u -> v} dp[u] + w(u, v)); se guarda
                  el predecesor que dio el máximo.
      CASO BASE   dp[v] = 0 (el camino formado solo por v).
      ORDEN       topológico (se «empuja» dp[u] por las aristas que salen
                  de u).
      RESPUESTA   max_v dp[v]; el camino sale siguiendo los predecesores.
    Número de caminos de s a t:
      ESTADO      cnt[v] = caminos de s a v.
      TRANSICIÓN  cnt[v] = Σ_{u -> v} cnt[u].
      CASO BASE   cnt[s] = 1.   ORDEN  topológico.   RESPUESTA  cnt[t].
    Por qué no funciona con ciclos: el valor de un nodo dependería de sí
    mismo (y habría infinitos caminos). Si Kahn no logra sacar todos los
    nodos, hay ciclo.

MACROALGORITMO
    1. Construir listas de adyacencia y grados de entrada.
    2. Cola con los nodos de grado 0; sacar, anotar, bajar el grado de los
       vecinos y encolar los que llegan a 0.
    3. Si no salieron los n nodos: hay ciclo.
    4. Inicializar dp (casos base).
    5. Para u en orden topológico: para cada arista u -> v, relajar dp[v].
    6. Leer la respuesta; reconstruir con los predecesores.

COMPLEJIDAD
    O(n + m) tiempo y memoria. 2·10^5 nodos y aristas en ~0,5 s en Python.

EJEMPLO A MANO
    Aristas 0->1 (3), 0->2 (2), 1->3 (4), 2->3 (6), 3->4 (1); orden 0 1 2 3 4.
      dp: 0:0  1:3  2:2  3:max(3+4, 2+6)=8  4:9  -> camino 0, 2, 3, 4 (peso 9).
      Caminos de 0 a 4: cnt = 0:1, 1:1, 2:1, 3:2, 4:2.

ERRORES TÍPICOS
    - Procesar en el orden de los índices en vez del topológico.
    - Usar Dijkstra con pesos negados para el camino más largo: no sirve.
    - Olvidar que el camino puede empezar en cualquier nodo (inicializar
      dp en 0 para todos) o, si debe empezar en s, inicializar en -infinito
      salvo s.
    - DFS recursivo para el orden topológico con n = 10^5: pila.

VARIANTES Y RELACIONADOS
    - Camino más largo desde s a t, camino más corto en DAG con pesos
      negativos (lineal, sin Dijkstra), juegos sobre DAG (ganador/perdedor).
    - lis.py (LIS = camino más largo en el DAG «i -> j si i < j y a[i] < a[j]»),
      caminos_grilla.py, dp_arboles.py.

DÓNDE PRACTICAR
    - 2025-2/maraton_problemas/p437_tower_babylon.py (UVa 437: cajas que se
      apilan = camino de altura máxima en un DAG).
    - ICPC/Colombia 2026/C - Into the Onion (DP por capas: DAG por niveles).
    - Externos: CSES «Longest Flight Route», «Game Routes»; AtCoder
      Educational DP Contest G «Longest Path».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (DFS que enumera todos los caminos) en
      400 DAG aleatorios + casos borde + detección de ciclos (python dp_dag.py)
"""
import random
from collections import deque


def orden_topologico(n, aristas):
    """Orden topológico por Kahn; None si el grafo tiene un ciclo."""
    ady = [[] for _ in range(n)]
    grado = [0] * n
    for e in aristas:
        ady[e[0]].append(e[1])
        grado[e[1]] += 1
    cola = deque(v for v in range(n) if grado[v] == 0)
    orden = []
    while cola:
        u = cola.popleft()
        orden.append(u)
        for v in ady[u]:
            grado[v] -= 1
            if grado[v] == 0:
                cola.append(v)
    return orden if len(orden) == n else None


def camino_mas_largo(n, aristas):
    """(mayor peso de un camino, nodos del camino) en un DAG con aristas (u, v, w)."""
    orden = orden_topologico(n, aristas)
    ady = [[] for _ in range(n)]
    for u, v, w in aristas:
        ady[u].append((v, w))
    dp = [0] * n                        # caso base: el camino de un solo nodo
    previo = [-1] * n
    for u in orden:                     # u ya es definitivo: empujarlo a sus vecinos
        for v, w in ady[u]:
            if dp[u] + w > dp[v]:
                dp[v] = dp[u] + w
                previo[v] = u
    fin = max(range(n), key=dp.__getitem__)
    camino = []
    while fin != -1:
        camino.append(fin)
        fin = previo[fin]
    camino.reverse()
    return dp[camino[-1]], camino


def contar_caminos(n, aristas, s, t, mod=None):
    """Número de caminos dirigidos de s a t en un DAG."""
    orden = orden_topologico(n, aristas)
    ady = [[] for _ in range(n)]
    for e in aristas:
        ady[e[0]].append(e[1])
    cnt = [0] * n
    cnt[s] = 1
    for u in orden:
        if cnt[u]:
            for v in ady[u]:
                cnt[v] = (cnt[v] + cnt[u]) % mod if mod else cnt[v] + cnt[u]
    return cnt[t]


def demo():
    aristas = [(0, 1, 3), (0, 2, 2), (1, 3, 4), (2, 3, 6), (3, 4, 1)]
    print("orden topológico:", orden_topologico(5, aristas))        # [0, 1, 2, 3, 4]
    print("camino más largo:", camino_mas_largo(5, aristas))        # (9, [0, 2, 3, 4])
    print("caminos de 0 a 4:", contar_caminos(5, aristas, 0, 4))    # 2


def pruebas():
    random.seed(1680)

    def dag_aleatorio(n):
        perm = list(range(n))
        random.shuffle(perm)             # perm[i] -> perm[j] con i < j: sin ciclos
        aristas = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.35:
                    aristas.append((perm[i], perm[j], random.randint(-5, 10)))
        return aristas

    # Casos borde
    assert orden_topologico(3, [(0, 1), (1, 2), (2, 0)]) is None
    assert orden_topologico(1, []) == [0]
    assert camino_mas_largo(1, []) == (0, [0])
    assert contar_caminos(2, [], 0, 1) == 0 and contar_caminos(2, [], 1, 1) == 1

    for _ in range(400):
        n = random.randint(1, 8)
        aristas = dag_aleatorio(n)
        ady = [[] for _ in range(n)]
        for u, v, w in aristas:
            ady[u].append((v, w))
        # Fuerza bruta: DFS desde cada nodo enumerando todos los caminos
        mejor = 0
        cuenta = [[0] * n for _ in range(n)]
        for s in range(n):
            pila = [(s, 0)]
            while pila:
                v, peso = pila.pop()
                mejor = max(mejor, peso)
                cuenta[s][v] += 1
                for u, w in ady[v]:
                    pila.append((u, peso + w))
        orden = orden_topologico(n, aristas)
        pos = {v: i for i, v in enumerate(orden)}
        assert all(pos[u] < pos[v] for u, v, _ in aristas)
        valor, camino = camino_mas_largo(n, aristas)
        assert valor == mejor
        pesos = {(u, v): w for u, v, w in aristas}
        assert sum(pesos[a, b] for a, b in zip(camino, camino[1:])) == valor
        for s in range(n):
            for t in range(n):
                assert contar_caminos(n, aristas, s, t) == cuenta[s][t]

    # Ciclos aleatorios: agregar una arista hacia atrás crea un ciclo
    for _ in range(100):
        n = random.randint(2, 8)
        aristas = [(i, i + 1) for i in range(n - 1)]
        a = random.randrange(1, n)
        aristas.append((a, random.randrange(a)))
        assert orden_topologico(n, aristas) is None


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
