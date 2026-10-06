"""
Grafos — Orden topológico con el algoritmo de Kahn («Topological sort, Kahn»)
Nivel: Intermedio
Ejecutar: python orden_topologico.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Ordenar los vértices de un grafo DIRIGIDO de modo que toda arista u→v
    quede con u antes que v (tareas con prerrequisitos). Existe si y solo si
    el grafo NO tiene ciclos (es un DAG); Kahn lo detecta de paso.
    Señales en el enunciado: «X debe hacerse antes que Y», «prerrequisitos»,
    «dependencias», «orden de compilación», «si hay varias respuestas,
    imprime la lexicográficamente menor», «imposible si hay dependencias
    circulares». También es el primer paso de cualquier DP sobre un DAG.

FUNCIÓN
    kahn(adj) -> list | None
        Un orden topológico de los n vértices (índices desde 0), o None si
        hay un ciclo.
    topologico_lexicografico(adj) -> list | None
        El orden topológico lexicográficamente MENOR (siempre elige el menor
        vértice disponible), o None si hay ciclo.

IDEA Y ALGORITMO
    Un DAG siempre tiene un vértice con grado de entrada 0 (si todos
    tuvieran una arista entrando, caminando hacia atrás se repetiría un
    vértice: ciclo). Ese vértice puede ir PRIMERO. Se quita con sus aristas
    (bajándole el grado de entrada a sus vecinos) y lo que queda sigue
    siendo un DAG: se repite.
    Implementación: indeg[v] = aristas que entran a v; una cola con los de
    indeg 0; al sacar u se agrega al orden y se decrementa indeg de cada
    vecino; el que llega a 0 entra a la cola.
    Detección de ciclo: los vértices de un ciclo nunca llegan a indeg 0 (cada
    uno espera al anterior), así que si al final el orden tiene menos de n
    vértices, HAY ciclo; y si hay ciclo, esos vértices faltan. ⇔ exacto.
    Lexicográficamente menor: usar un min-heap en vez de la cola. Es correcto
    por un argumento de intercambio: en cada paso el primer elemento de la
    respuesta tiene que ser un vértice de indeg 0, y el menor de ellos da el
    orden menor; luego se repite sobre el resto.
    (Alternativa con DFS: el orden inverso de los tiempos de salida es
    topológico; ver dfs.py.)

MACROALGORITMO
    1. indeg[v] = número de aristas u→v.
    2. cola = vértices con indeg 0 (heap si se pide el lexicográfico menor).
    3. Mientras la cola no esté vacía: sacar u, agregarlo al orden.
    4. Para cada u→v: indeg[v] −= 1; si llega a 0, meter v.
    5. Si len(orden) < n: hay ciclo (devolver None); si no, el orden.

COMPLEJIDAD
    O(n + m) con cola; O(n log n + m) con heap. ~10^6 aristas/s en Python.

EJEMPLO A MANO
    Aristas: 5→2, 5→0, 4→0, 4→1, 2→3, 3→1.   indeg = [2, 2, 1, 1, 0, 0]
      heap {4, 5}: saca 4 → indeg[0]=1, indeg[1]=1
      heap {5}:    saca 5 → indeg[2]=0, indeg[0]=0 → heap {0, 2}
      saca 0; saca 2 → indeg[3]=0; saca 3 → indeg[1]=0; saca 1.
    Lexicográfico menor: [4, 5, 0, 2, 3, 1]. Si se agrega 1→5: ciclo
    5→2→3→1→5 → None.

ERRORES TÍPICOS
    - Olvidar contar aristas repetidas en indeg (o contarlas en indeg pero
      decrementar una sola vez): deja vértices colgados.
    - Concluir «no hay ciclo» sin revisar len(orden) == n.
    - Pedir el menor lexicográfico y usar deque: da UN orden válido, no el menor.
    - Confundir el sentido: «A depende de B» es la arista B→A.

VARIANTES Y RELACIONADOS
    - DP en DAG (camino más largo, contar caminos): procesar en orden topológico.
    - Capas / «mínimo número de semestres»: BFS por niveles en Kahn.
    - ¿Orden único? Sí ⇔ en cada paso hay exactamente un vértice en la cola.
    - Ciclos con colores (y el ciclo concreto): deteccion_ciclos.py.
    - Condensación de un grafo con ciclos en un DAG: scc.py.

DÓNDE PRACTICAR
    - CSES «Course Schedule» (orden o «IMPOSSIBLE»)
    - UVa 10305 «Ordering Tasks», UVa 11060 «Beverages» (Kahn con prioridad)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las permutaciones, n ≤ 6) en
      1500 grafos aleatorios: existencia ⇔ alguna permutación válida, orden de
      Kahn válido, lexicográfico = mínima permutación válida; y una cadena de
      200000 vértices (python orden_topologico.py)
"""
import heapq
import itertools
import random
from collections import deque


def kahn(adj):
    """Un orden topológico (lista) o None si el grafo tiene un ciclo."""
    n = len(adj)
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    cola = deque(v for v in range(n) if indeg[v] == 0)
    orden = []
    while cola:
        u = cola.popleft()
        orden.append(u)
        for v in adj[u]:              # «quitar» u: sus aristas dejan de contar
            indeg[v] -= 1
            if indeg[v] == 0:
                cola.append(v)
    # Los vértices de un ciclo nunca llegan a indeg 0
    return orden if len(orden) == n else None


def topologico_lexicografico(adj):
    """El orden topológico lexicográficamente menor, o None si hay ciclo."""
    n = len(adj)
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    heap = [v for v in range(n) if indeg[v] == 0]
    heapq.heapify(heap)
    orden = []
    while heap:
        u = heapq.heappop(heap)       # el menor disponible
        orden.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)
    return orden if len(orden) == n else None


def _adyacencia(n, aristas):
    adj = [[] for _ in range(n)]
    for u, v in aristas:
        adj[u].append(v)
    return adj


def _es_topologico(orden, n, aristas):
    pos = {v: i for i, v in enumerate(orden)}
    return sorted(orden) == list(range(n)) and all(pos[u] < pos[v] for u, v in aristas)


def demo():
    aristas = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    adj = _adyacencia(6, aristas)
    print("aristas:", aristas)
    print("Kahn (cola):         ", kahn(adj))
    print("lexicográfico menor: ", topologico_lexicografico(adj))   # [4, 5, 0, 2, 3, 1]
    adj[1].append(5)
    print("con 1→5 (ciclo):     ", kahn(adj))                       # None


def pruebas():
    random.seed(10305)
    casos = 0

    assert kahn([]) == [] and topologico_lexicografico([]) == []
    assert kahn([[]]) == [0]
    assert kahn([[0]]) is None                                # lazo
    assert kahn([[1, 1], []]) == [0, 1]                       # arista repetida

    n = 200000
    adj = _adyacencia(n, [(i + 1, i) for i in range(n - 1)])
    assert kahn(adj) == list(range(n - 1, -1, -1))

    for _ in range(1500):
        n = random.randint(1, 6)
        m = random.randint(0, 10)
        if random.random() < 0.6:     # DAG seguro: aristas de menor a mayor en una permutación
            perm = list(range(n))
            random.shuffle(perm)
            aristas = []
            for _ in range(m):
                a, b = sorted(random.sample(range(n), 2)) if n > 1 else (0, 0)
                if a != b:
                    aristas.append((perm[a], perm[b]))
        else:
            aristas = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
        adj = _adyacencia(n, aristas)
        # Fuerza bruta: todas las permutaciones válidas (en orden lexicográfico)
        validas = [list(p) for p in itertools.permutations(range(n))
                   if _es_topologico(p, n, aristas)]
        o = kahn(adj)
        lex = topologico_lexicografico(adj)
        if validas:
            assert o is not None and _es_topologico(o, n, aristas)
            assert lex == validas[0]
        else:
            assert o is None and lex is None
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
