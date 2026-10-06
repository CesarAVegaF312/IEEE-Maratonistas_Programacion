"""
Grafos — Componentes fuertemente conexas («Strongly Connected Components»: Tarjan y Kosaraju)
Nivel: Avanzado
Ejecutar: python scc.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    En un grafo DIRIGIDO, partir los vértices en grupos maximales donde
    cada uno llega a cada otro (u →* v y v →* u). Al contraer cada grupo en
    un solo nodo queda un DAG (el «grafo condensado»), sobre el que ya se
    puede hacer orden topológico, DP de caminos, contar fuentes/sumideros…
    Señales en el enunciado: «se puede ir y volver», «todos se comunican
    con todos», «ciclos de dependencias», «agrupar los que se alcanzan
    mutuamente»; 2-SAT; DP sobre un grafo dirigido que puede tener ciclos.

FUNCIÓN
    tarjan_scc(n, ady)   -> (c, comp)
    kosaraju_scc(n, ady) -> (c, comp)
        ady[u] = lista de vecinos v (aristas u → v), vértices 0..n-1.
        c = número de componentes; comp[v] en 0..c-1.
        Convención (ambas): la numeración es un ORDEN TOPOLÓGICO del grafo
        condensado: si hay arista u → v con comp[u] != comp[v], entonces
        comp[u] < comp[v]. (La componente 0 es una fuente, la c-1 un sumidero.)
    condensar(n, ady, c, comp) -> dag
        dag[x] = lista SIN repetidos de componentes y con arista x → y.

IDEA Y ALGORITMO
    Kosaraju (dos pasadas):
      1) DFS en el grafo original guardando el orden de FINALIZACIÓN.
      2) Recorrer el grafo TRANSPUESTO (aristas invertidas) tomando los
         vértices de mayor a menor tiempo de finalización; cada recorrido
         que arranca en un vértice sin componente marca exactamente una SCC.
      Por qué: el vértice que termina último está en una componente FUENTE
      del condensado. En el transpuesto esa componente es un sumidero: desde
      ella no se sale, así que el recorrido marca justo su componente. Se
      repite con el siguiente que termina más tarde (las componentes ya
      marcadas actúan como paredes). Las componentes salen en orden
      topológico.
    Tarjan (una pasada):
      DFS asignando a cada vértice indice[v] (orden de descubrimiento) y
      bajo[v] = menor índice alcanzable desde el subárbol de v usando a lo
      sumo una arista hacia un vértice que siga en la pila. Los vértices se
      apilan al descubrirse. Si al terminar v se tiene bajo[v] == indice[v],
      v es la «raíz» de su componente: nadie de su subárbol logra subir más
      arriba, así que se desapila hasta v y eso es una SCC completa.
      Tarjan las encuentra en orden topológico INVERSO (primero un
      sumidero); al final se renumeran con c-1-x para cumplir la convención.
    Ambos se escriben ITERATIVOS (pila explícita con un puntero al siguiente
    vecino por vértice): con N = 10^5 un DFS recursivo revienta la pila de
    Python aunque se suba el límite de recursión.
    Ingenuo: calcular alcanzabilidad desde cada vértice, O(N·(N+M)).

MACROALGORITMO
    Tarjan:
    1. Para cada vértice sin visitar, iniciar un DFS iterativo.
    2. Al descubrir v: indice[v] = bajo[v] = t (t++), apilar v, en_pila[v] = V.
    3. Al mirar la arista v → w: si w es nuevo, bajar a w; si w está en la
       pila, bajo[v] = min(bajo[v], indice[w]).
    4. Al terminar w y volver a su padre v: bajo[v] = min(bajo[v], bajo[w]).
    5. Al terminar v con bajo[v] == indice[v]: desapilar hasta v → una SCC.
    6. Renumerar las componentes para que queden en orden topológico.
    Kosaraju:
    1. DFS iterativo en el grafo y lista de vértices por fin de visita.
    2. Construir el transpuesto.
    3. Para v en orden inverso de finalización: si no tiene componente,
       recorrer el transpuesto desde v marcando la componente c; c++.

COMPLEJIDAD
    Tiempo O(N + M) ambos, memoria O(N + M) (Kosaraju además guarda el
    transpuesto). En Python, ~10^5–3·10^5 aristas por segundo.

EJEMPLO A MANO
    n = 8, aristas 0→1 1→2 2→0 2→3 3→4 4→5 5→3 6→5 6→7 7→6.
    Tarjan desde 0: indices 0,1,2 a 0,1,2; 2→0 da bajo[2]=0; 2→3 baja a
    3,4,5 (indices 3,4,5); 5→3 da bajo[5]=3, sube bajo[4]=3; termina 3 con
    bajo=indice=3 → SCC {3,4,5} (sumidero). Vuelve a 2,1,0; termina 0 con
    bajo=indice=0 → SCC {0,1,2}. Luego 6: 6→5 (ya no está en pila, se
    ignora), 6→7, 7→6 → SCC {6,7}.
    Tras renumerar: {6,7} = 0, {0,1,2} = 1, {3,4,5} = 2.
    Condensado: 0 → 2, 1 → 2.

ERRORES TÍPICOS
    - En Tarjan, actualizar bajo[v] con w que YA salió de la pila (pertenece
      a otra componente terminada): une componentes distintas. Hay que
      revisar en_pila[w].
    - En Kosaraju, recorrer el grafo original en la 2.ª pasada en vez del
      transpuesto, o en orden creciente de finalización.
    - Confundir el sentido del orden: Tarjan entrega las SCC de sumidero a
      fuente (orden topológico inverso).
    - Condensar sin quitar aristas repetidas ni lazos x → x (inflan los
      grados de entrada/salida y rompen la DP).
    - DFS recursivo con N grande: RecursionError o caída del intérprete.

VARIANTES Y RELACIONADOS
    - ¿Es fuertemente conexo? c == 1; o el truco de dos BFS: desde un vértice
      se alcanza todo en el grafo y en el transpuesto (ICPC Colombia 2018 I).
    - Mínimo de aristas para volverlo fuertemente conexo: si c > 1,
      max(#fuentes, #sumideros) del condensado.
    - DP en el condensado (p. ej. máxima suma de pesos en un camino).
    - dos_sat.py (2-SAT es SCC sobre el grafo de implicaciones).
    - orden_topologico.py, puentes_articulacion.py (análogo no dirigido:
      componentes biconexas), dfs.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/I - Impossible Communication (fuerte conexidad con
      dos BFS + nodos virtuales)
    - ICPC/Colombia 2024/G - Signal Coverage (2-SAT con Tarjan)
    - CSES «Flight Routes Check», «Planets and Kingdoms», «Coin Collector»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (alcanzabilidad por BFS desde cada
      vértice: u ~ v ⇔ se alcanzan mutuamente) en 600 grafos aleatorios,
      Tarjan == Kosaraju, propiedad de orden topológico del condensado,
      casos borde y una cadena/ciclo de 10^5 vértices (python scc.py)
"""
import random
from collections import deque


def tarjan_scc(n, ady):
    """SCC por Tarjan iterativo. Devuelve (c, comp) con comp en orden topológico."""
    indice = [-1] * n         # orden de descubrimiento (-1 = no visitado)
    bajo = [0] * n            # menor índice alcanzable que sigue en la pila
    en_pila = [False] * n
    sig = [0] * n             # puntero al siguiente vecino por revisar de cada v
    pila = []                 # vértices de componentes aún no cerradas
    comp = [-1] * n
    c = t = 0
    for r in range(n):
        if indice[r] != -1:
            continue
        indice[r] = bajo[r] = t
        t += 1
        pila.append(r)
        en_pila[r] = True
        llamadas = [r]        # pila explícita que reemplaza la recursión
        while llamadas:
            v = llamadas[-1]
            if sig[v] < len(ady[v]):
                w = ady[v][sig[v]]
                sig[v] += 1
                if indice[w] == -1:           # arista de árbol: "llamar" a w
                    indice[w] = bajo[w] = t
                    t += 1
                    pila.append(w)
                    en_pila[w] = True
                    llamadas.append(w)
                elif en_pila[w]:              # w sigue abierto: misma SCC posible
                    if indice[w] < bajo[v]:
                        bajo[v] = indice[w]
            else:                             # v terminó: "retornar"
                llamadas.pop()
                if llamadas:
                    p = llamadas[-1]
                    if bajo[v] < bajo[p]:
                        bajo[p] = bajo[v]
                if bajo[v] == indice[v]:      # v es raíz de una SCC
                    while True:
                        w = pila.pop()
                        en_pila[w] = False
                        comp[w] = c
                        if w == v:
                            break
                    c += 1
    # Tarjan cierra primero los sumideros: invertir para orden topológico
    return c, [c - 1 - x for x in comp]


def kosaraju_scc(n, ady):
    """SCC por Kosaraju iterativo. Devuelve (c, comp) con comp en orden topológico."""
    # 1) Orden de finalización de un DFS en el grafo original
    visto = [False] * n
    sig = [0] * n
    orden = []
    for r in range(n):
        if visto[r]:
            continue
        visto[r] = True
        pila = [r]
        while pila:
            v = pila[-1]
            if sig[v] < len(ady[v]):
                w = ady[v][sig[v]]
                sig[v] += 1
                if not visto[w]:
                    visto[w] = True
                    pila.append(w)
            else:
                pila.pop()
                orden.append(v)               # v termina
    # 2) Transpuesto
    tr = [[] for _ in range(n)]
    for u in range(n):
        for v in ady[u]:
            tr[v].append(u)
    # 3) Recorrer el transpuesto en orden inverso de finalización
    comp = [-1] * n
    c = 0
    for r in reversed(orden):
        if comp[r] != -1:
            continue
        comp[r] = c
        pila = [r]                            # aquí el orden de visita no importa
        while pila:
            v = pila.pop()
            for w in tr[v]:
                if comp[w] == -1:
                    comp[w] = c
                    pila.append(w)
        c += 1
    return c, comp


def condensar(n, ady, c, comp):
    """Grafo condensado (DAG) sin aristas repetidas ni lazos."""
    dag = [set() for _ in range(c)]
    for u in range(n):
        for v in ady[u]:
            if comp[u] != comp[v]:
                dag[comp[u]].add(comp[v])
    return [sorted(s) for s in dag]


def _lista_ady(n, aristas):
    ady = [[] for _ in range(n)]
    for u, v in aristas:
        ady[u].append(v)
    return ady


def demo():
    n = 8
    aristas = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3),
               (6, 5), (6, 7), (7, 6)]
    ady = _lista_ady(n, aristas)
    c, comp = tarjan_scc(n, ady)
    grupos = [[v for v in range(n) if comp[v] == x] for x in range(c)]
    print("Tarjan:   c =", c, "componentes (orden topológico):", grupos)
    c2, comp2 = kosaraju_scc(n, ady)
    print("Kosaraju: c =", c2, "componentes:",
          [[v for v in range(n) if comp2[v] == x] for x in range(c2)])
    print("Condensado (Tarjan):", condensar(n, ady, c, comp))   # [[2], [2], []]


def _particion(n, comp):
    """Partición como conjunto de frozensets (independiente de la numeración)."""
    g = {}
    for v in range(n):
        g.setdefault(comp[v], set()).add(v)
    return {frozenset(s) for s in g.values()}


def _fuerza_bruta(n, ady):
    """SCC desde la definición: alcanzabilidad por BFS desde cada vértice."""
    alc = []
    for s in range(n):
        vis = [False] * n
        vis[s] = True
        q = deque([s])
        while q:
            u = q.popleft()
            for w in ady[u]:
                if not vis[w]:
                    vis[w] = True
                    q.append(w)
        alc.append(vis)
    comp = [-1] * n
    c = 0
    for u in range(n):
        if comp[u] == -1:
            for v in range(n):
                if alc[u][v] and alc[v][u]:
                    comp[v] = c
            c += 1
    return c, comp


def _revisar(n, ady):
    cb, compb = _fuerza_bruta(n, ady)
    esperado = _particion(n, compb)
    for f in (tarjan_scc, kosaraju_scc):
        c, comp = f(n, ady)
        assert c == cb and sorted(set(comp)) == list(range(c))
        assert _particion(n, comp) == esperado
        # convención: numeración en orden topológico del condensado
        for u in range(n):
            for v in ady[u]:
                assert comp[u] <= comp[v]
        dag = condensar(n, ady, c, comp)
        assert all(x < y for x in range(c) for y in dag[x])


def pruebas():
    random.seed(2024)

    # Casos borde
    assert tarjan_scc(0, []) == (0, []) and kosaraju_scc(0, []) == (0, [])
    assert tarjan_scc(1, [[]]) == (1, [0]) and kosaraju_scc(1, [[0]]) == (1, [0])
    assert tarjan_scc(3, [[], [], []])[0] == 3                 # sin aristas
    assert tarjan_scc(3, [[1], [2], [0]])[0] == 1              # un ciclo
    assert tarjan_scc(3, [[1], [2], []]) == (3, [0, 1, 2])     # camino: topológico
    assert kosaraju_scc(3, [[1], [2], []]) == (3, [0, 1, 2])

    # Aleatorios contra fuerza bruta (incluye lazos y aristas repetidas)
    for _ in range(600):
        n = random.randint(1, 12)
        m = random.randint(0, 3 * n)
        aristas = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
        _revisar(n, _lista_ady(n, aristas))

    # Ejemplo del docstring
    ady = _lista_ady(8, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3),
                         (6, 5), (6, 7), (7, 6)])
    c, comp = tarjan_scc(8, ady)
    assert c == 3 and comp == [1, 1, 1, 2, 2, 2, 0, 0]
    assert condensar(8, ady, c, comp) == [[2], [2], []]

    # Grandes: cadena de 10^5 (10^5 componentes) y ciclo de 10^5 (una sola);
    # con DFS recursivo esto reventaría la pila
    N = 10 ** 5
    cadena = [[i + 1] for i in range(N - 1)] + [[]]
    assert tarjan_scc(N, cadena)[1] == list(range(N))
    assert kosaraju_scc(N, cadena)[1] == list(range(N))
    ciclo = [[(i + 1) % N] for i in range(N)]
    assert tarjan_scc(N, ciclo)[0] == 1 and kosaraju_scc(N, ciclo)[0] == 1


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
