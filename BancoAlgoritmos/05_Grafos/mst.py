"""
Grafos — Árbol de expansión mínima: Kruskal y Prim («Minimum Spanning Tree»)
Nivel: Intermedio
Ejecutar: python mst.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    En un grafo NO dirigido y ponderado, elegir n−1 aristas que conecten a
    todos los vértices con el menor costo total (un árbol: sin ciclos).
    Señales en el enunciado: «conectar todas las ciudades / computadoras con
    el mínimo cable», «reparar carreteras para que todo quede conectado al
    menor costo», «la arista más pesada que hay que usar sea mínima»
    (el MST también minimiza la arista máxima), «quitar aristas maximizando
    lo ahorrado» (total − MST). Si el grafo es dirigido NO aplica.

FUNCIÓN
    kruskal(n, aristas) -> (costo, elegidas)
        aristas = [(u, v, w)]. elegidas = aristas (u, v, w) del bosque
        mínimo. Si len(elegidas) < n−1, el grafo NO es conexo (es el bosque
        de expansión mínima de cada componente).
    prim(adj) -> costo | None
        adj[u] = [(v, w)]. Costo del MST, None si el grafo no es conexo.

IDEA Y ALGORITMO
    Propiedad del corte: para cualquier partición de los vértices en dos
    lados, la arista MÁS BARATA que cruza el corte está en algún MST. (Si un
    MST no la usa, agregarla forma un ciclo que cruza el corte por otra
    arista más cara o igual; cambiar una por otra no empeora el costo.)
    Ambos algoritmos son voraces que aplican esa propiedad:
      · Kruskal: ordenar aristas por peso y agregar cada una si une dos
        componentes distintas (si cierra un ciclo, se descarta: es la más
        cara de ese ciclo). Las componentes se mantienen con union-find.
        Ideal cuando se tiene la LISTA de aristas.
      · Prim: crecer un solo árbol desde un vértice; en cada paso agregar la
        arista más barata que sale del árbol (corte = árbol vs. resto). Con
        heap y descarte de entradas viejas, como Dijkstra pero la clave es
        el peso de la arista, no la distancia acumulada.
    Ingenuo (probar todos los subconjuntos de n−1 aristas) es exponencial.

MACROALGORITMO
    Kruskal:
    1. Ordenar las aristas por peso.
    2. DSU con n elementos; costo = 0.
    3. Para cada (u, v, w) en orden: si unir(u, v): costo += w, guardarla.
    4. Si se eligieron n−1 aristas, es el MST; si no, el grafo no es conexo.
    Prim:
    1. en_arbol = [False]*n; heap = [(0, 0)].
    2. Sacar (w, u); si u ya está en el árbol, descartar.
    3. Agregar u (costo += w) y meter (w', v) por cada arista u–v con v afuera.
    4. Si al final no están los n vértices, el grafo no es conexo.

COMPLEJIDAD
    Kruskal: O(m log m) (domina el sort). Prim con heap: O(m log m).
    En Python ~2–5·10^5 aristas por segundo.

EJEMPLO A MANO
    Aristas: 0-1 (4), 0-2 (3), 1-2 (1), 1-3 (2), 2-3 (4), 3-4 (2), 2-4 (5).
    Kruskal en orden de peso:
      1-2 (1) ✓, 1-3 (2) ✓, 3-4 (2) ✓, 0-2 (3) ✓, 0-1 (4) ✗ ciclo,
      2-3 (4) ✗, 2-4 (5) ✗.     Costo = 1 + 2 + 2 + 3 = 8.

ERRORES TÍPICOS
    - No verificar conexidad: con k componentes Kruskal elige n−k aristas.
    - Ordenar tuplas (u, v, w) sin key: ordena por u. Usar key o (w, u, v).
    - Prim: marcar el vértice al METERLO al heap (como BFS) en vez de al
      sacarlo: da un árbol, pero no el mínimo.
    - Usar un DSU sin compresión ni unión por tamaño: O(n) por operación.

VARIANTES Y RELACIONADOS
    - Árbol de expansión MÁXIMA: ordenar al revés.
    - Cuello de botella: el MST minimiza el peso máximo usado; el camino en
      el MST entre u y v minimiza la arista máxima entre u y v.
    - Segundo mejor MST, MST con aristas obligatorias (unirlas primero).
    - union_find.py (estructura de Kruskal), dijkstra.py (estructura de Prim).

DÓNDE PRACTICAR
    - CSES «Road Reparation» (MST o «IMPOSSIBLE»)
    - UVa 11631 «Dark roads» (total − MST), UVa 10034 «Freckles» (puntos en
      el plano, grafo completo)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (probar todos los subconjuntos de n−1
      aristas y quedarse con el árbol más barato) en 1500 grafos aleatorios
      con n ≤ 6, m ≤ 10; Kruskal y Prim coinciden; las aristas elegidas
      forman un árbol (python mst.py)
"""
import heapq
import itertools
import random


def kruskal(n, aristas):
    """Bosque de expansión mínima: (costo, aristas elegidas)."""
    padre = list(range(n))
    tam = [1] * n

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]     # compresión por mitades
            x = padre[x]
        return x

    costo = 0
    elegidas = []
    for u, v, w in sorted(aristas, key=lambda a: a[2]):
        ru, rv = raiz(u), raiz(v)
        if ru == rv:                      # cerraría un ciclo: es la más cara de él
            continue
        if tam[ru] < tam[rv]:
            ru, rv = rv, ru
        padre[rv] = ru
        tam[ru] += tam[rv]
        costo += w
        elegidas.append((u, v, w))
        if len(elegidas) == n - 1:        # ya es un árbol: no hace falta seguir
            break
    return costo, elegidas


def prim(adj):
    """Costo del MST creciendo un árbol desde 0; None si el grafo no es conexo."""
    n = len(adj)
    if n == 0:
        return 0
    en_arbol = [False] * n
    heap = [(0, 0)]                       # (peso de la arista que lo conecta, vértice)
    costo = agregados = 0
    while heap:
        w, u = heapq.heappop(heap)
        if en_arbol[u]:                   # entrada vieja: u ya entró más barato
            continue
        en_arbol[u] = True
        costo += w
        agregados += 1
        for v, wv in adj[u]:
            if not en_arbol[v]:
                heapq.heappush(heap, (wv, v))
    return costo if agregados == n else None


def _adyacencia(n, aristas):
    adj = [[] for _ in range(n)]
    for u, v, w in aristas:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def _conexo(n, aristas):
    """¿Las aristas conectan los n vértices? (relleno simple, para la bruta)."""
    alc = {0}
    cambio = True
    while cambio:
        cambio = False
        for u, v, _ in aristas:
            if (u in alc) != (v in alc):
                alc |= {u, v}
                cambio = True
    return len(alc) == n


def demo():
    aristas = [(0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2), (2, 3, 4), (3, 4, 2), (2, 4, 5)]
    costo, elegidas = kruskal(5, aristas)
    print("aristas:", aristas)
    print("Kruskal: costo", costo, "aristas", elegidas)    # 8
    print("Prim:    costo", prim(_adyacencia(5, aristas)))  # 8
    print("no conexo (sin 3-4, 2-4):", kruskal(5, aristas[:5]),
          "Prim:", prim(_adyacencia(5, aristas[:5])))


def pruebas():
    random.seed(11631)
    casos = 0

    assert kruskal(1, []) == (0, []) and prim([[]]) == 0
    assert kruskal(2, []) == (0, []) and prim([[], []]) is None
    assert kruskal(2, [(0, 0, -5), (0, 1, 7), (1, 0, 2)]) == (2, [(1, 0, 2)])

    for _ in range(1500):
        n = random.randint(1, 6)
        m = random.randint(0, 10)
        aristas = [(random.randrange(n), random.randrange(n), random.randint(-3, 15))
                   for _ in range(m)]
        # Fuerza bruta: todos los subconjuntos de n-1 aristas que conectan todo
        mejor = None
        for sub in itertools.combinations(aristas, n - 1):
            if _conexo(n, sub):
                c = sum(w for _, _, w in sub)
                mejor = c if mejor is None else min(mejor, c)
        costo, elegidas = kruskal(n, aristas)
        p = prim(_adyacencia(n, aristas))
        if mejor is None:
            assert len(elegidas) < n - 1 and p is None
        else:
            assert len(elegidas) == n - 1 and _conexo(n, elegidas)
            assert costo == mejor == p
            assert sum(w for _, _, w in elegidas) == costo
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
