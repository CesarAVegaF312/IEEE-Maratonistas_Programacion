"""
Grafos — Detección de ciclos (dirigido y no dirigido) («Cycle detection»)
Nivel: Intermedio
Ejecutar: python deteccion_ciclos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir si un grafo tiene un ciclo y, si lo tiene, ENTREGAR uno (la
    lista de vértices). Responde «¿hay dependencias circulares?», «¿se puede
    hacer un viaje que vuelva al inicio sin repetir carretera?», «¿el grafo
    es un árbol / bosque?», «¿se puede ganar indefinidamente?».
    Señales en el enunciado: «circular», «deadlock», «imprime un ciclo o
    IMPOSSIBLE», «round trip», «¿es un árbol?» (conexo y sin ciclos).

FUNCIÓN
    ciclo_dirigido(adj) -> list
        adj[u] = [v, ...] (aristas u→v). Devuelve [x0, …, xk-1] con aristas
        x0→x1→…→xk-1→x0, o [] si el grafo es acíclico (DAG). Un lazo u→u
        da [u].
    ciclo_no_dirigido(n, aristas) -> list
        aristas = [(u, v)]. Devuelve los vértices de un ciclo (consecutivos
        unidos por aristas DISTINTAS, el último con el primero), o [].
        Un lazo da [u]; dos aristas paralelas u–v dan [u, v].

IDEA Y ALGORITMO
    Dirigido — tres colores en un DFS:
      blanco (0) = no visitado, gris (1) = en la pila (la «llamada» está
      abierta), negro (2) = terminado.
    Hay ciclo ⇔ el DFS encuentra una arista u→v con v GRIS (arista de
    retroceso). Si v está gris, v es ancestro de u en la pila: el camino de
    la pila v → … → u más la arista u→v es un ciclo. Al revés, si hay un
    ciclo, sea v su primer vértice visitado: todo el ciclo se descubre
    mientras v está gris, y la arista del ciclo que entra a v se encuentra
    con v gris. Una arista a un vértice NEGRO no indica ciclo (es avance o
    cruce: lo de ese vértice ya se exploró completo sin volver aquí).
    No dirigido — basta «visitado»: en un DFS/BFS de un grafo no dirigido,
    toda arista que no es del árbol cierra un ciclo. Hay que ignorar SOLO la
    arista por la que se llegó (por su ÍNDICE, no por el vértice padre, para
    que dos aristas paralelas sí cuenten como ciclo). El ciclo se arma
    subiendo por padres desde ambos extremos hasta el ancestro común.
    Atajo de conteo: sin ciclos ⇔ m = n − (componentes) (bosque); o con
    union-find, la primera arista que une dos vértices ya juntos.

MACROALGORITMO
    Dirigido:
    1. color = 0 en todos; para cada raíz blanca, DFS iterativo con pila e
       índice de vecino; al entrar color = 1, al salir color = 2.
    2. Arista u→v con color[v] == 1: el ciclo es la pila desde v hasta u.
    3. Si nunca pasa, devolver [].
    No dirigido:
    1. BFS desde cada vértice no visitado guardando padre y arista de llegada.
    2. Arista (u, v, id) con v visitado e id ≠ arista de llegada de u: ciclo.
    3. Subir desde u y v por padres hasta el ancestro común y pegar.

COMPLEJIDAD
    O(n + m) tiempo y memoria en ambos casos.

EJEMPLO A MANO
    Dirigido 0→1, 1→2, 2→3, 3→1, 0→4:
      entra 0 (gris), 1 (gris), 2 (gris), 3 (gris); 3→1 con 1 GRIS → ciclo
      = pila desde 1: [1, 2, 3].
    Si en vez de 3→1 fuera 3→4 y 4→… sin volver: 4 estaría negro o blanco
    → sin ciclo.
    No dirigido 0-1, 1-2, 2-0, 2-3: BFS desde 0 descubre 1 y 2; al revisar
    la arista 1-2 desde 1, 2 ya está visitado y no es la arista de llegada →
    ciclo 1 → 0 → 2 (y de vuelta a 1).

ERRORES TÍPICOS
    - Dirigido con solo «visitado»: cualquier arista a un vértice visitado
      parecería ciclo (falso positivo con 0→1, 0→2, 1→2).
    - No dirigido: ignorar al PADRE en vez de a la ARISTA de llegada: dos
      aristas paralelas u–v no se detectan como ciclo.
    - DFS recursivo: con 10^5 vértices en cadena revienta la pila de Python.
    - Grafo no conexo: arrancar solo desde el vértice 0.

VARIANTES Y RELACIONADOS
    - Orden topológico (si no hay ciclo): orden_topologico.py.
    - Grafo funcional (cada vértice con UNA arista de salida): grafo_funcional.py.
    - Ciclo negativo: bellman_ford.py. Ciclo impar: bipartito.py.
    - Todos los vértices que están en algún ciclo dirigido: scc.py
      (componentes de tamaño > 1 o con lazo).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/K - kewl Texting (grafo funcional con detección de
      ciclos; ver también grafo_funcional.py)
    - CSES «Round Trip» (no dirigido), «Round Trip II» (dirigido)

VERIFICACIÓN
    - Pruebas: OK en 2000 grafos aleatorios contra fuerza bruta (dirigido:
      clausura transitiva, hay ciclo ⇔ algún v se alcanza a sí mismo con ≥ 1
      arista; no dirigido: hay ciclo ⇔ m > n − componentes); cada ciclo
      devuelto se valida arista por arista; cadenas de 200000 vértices
      (python deteccion_ciclos.py)
"""
import random
from collections import deque


def ciclo_dirigido(adj):
    """Algún ciclo dirigido como lista de vértices en orden, o [] si es un DAG."""
    n = len(adj)
    color = [0] * n            # 0 blanco, 1 gris (en la pila), 2 negro (terminado)
    it = [0] * n
    for r in range(n):
        if color[r]:
            continue
        pila = [r]
        color[r] = 1
        while pila:
            u = pila[-1]
            if it[u] < len(adj[u]):
                v = adj[u][it[u]]
                it[u] += 1
                if color[v] == 0:
                    color[v] = 1
                    pila.append(v)
                elif color[v] == 1:        # arista de retroceso: v está en la pila
                    return pila[pila.index(v):]
            else:
                color[u] = 2
                pila.pop()
    return []


def ciclo_no_dirigido(n, aristas):
    """Algún ciclo de un grafo no dirigido (lista de vértices) o []."""
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(aristas):
        if u == v:
            return [u]                     # un lazo ya es un ciclo
        adj[u].append((v, i))
        adj[v].append((u, i))
    padre = [-1] * n
    llegada = [-1] * n                     # índice de la arista por la que se llegó
    prof = [-1] * n
    for s in range(n):
        if prof[s] != -1:
            continue
        prof[s] = 0
        cola = deque([s])
        while cola:
            u = cola.popleft()
            for v, i in adj[u]:
                if i == llegada[u]:        # la misma arista de ida: no es ciclo
                    continue
                if prof[v] == -1:
                    prof[v] = prof[u] + 1
                    padre[v] = u
                    llegada[v] = i
                    cola.append(v)
                else:
                    # Arista que no es del árbol: subir hasta el ancestro común
                    a, b = u, v
                    lado_a, lado_b = [], []
                    while prof[a] > prof[b]:
                        lado_a.append(a)
                        a = padre[a]
                    while prof[b] > prof[a]:
                        lado_b.append(b)
                        b = padre[b]
                    while a != b:
                        lado_a.append(a)
                        lado_b.append(b)
                        a, b = padre[a], padre[b]
                    # u … (sube) … ancestro … (baja) … v, y la arista v–u cierra
                    return lado_a + [a] + lado_b[::-1]
    return []


def demo():
    adj = [[1, 4], [2], [3], [1], []]
    print("dirigido 0→1, 0→4, 1→2, 2→3, 3→1:", ciclo_dirigido(adj))        # [1, 2, 3]
    print("dirigido 0→1, 0→2, 1→2 (sin ciclo):", ciclo_dirigido([[1, 2], [2], []]))
    ar = [(0, 1), (1, 2), (2, 0), (2, 3)]
    print("no dirigido", ar, "->", ciclo_no_dirigido(4, ar))               # [1, 0, 2]
    print("no dirigido árbol [(0,1),(1,2)] ->", ciclo_no_dirigido(3, [(0, 1), (1, 2)]))
    print("aristas paralelas [(0,1),(1,0)] ->", ciclo_no_dirigido(2, [(0, 1), (1, 0)]))


def _componentes(n, aristas):
    etiqueta = list(range(n))
    cambio = True
    while cambio:
        cambio = False
        for u, v in aristas:
            m = min(etiqueta[u], etiqueta[v])
            if etiqueta[u] != m or etiqueta[v] != m:
                etiqueta[u] = etiqueta[v] = m
                cambio = True
    return len(set(etiqueta))


def pruebas():
    random.seed(1678)
    casos = 0

    assert ciclo_dirigido([]) == [] and ciclo_no_dirigido(0, []) == []
    assert ciclo_dirigido([[0]]) == [0] and ciclo_no_dirigido(1, [(0, 0)]) == [0]
    assert ciclo_dirigido([[1], [0]]) == [0, 1]
    assert ciclo_no_dirigido(2, [(0, 1)]) == []

    # Cadenas largas sin ciclo, y cerradas
    n = 200000
    cadena = [[i + 1] for i in range(n - 1)] + [[]]
    assert ciclo_dirigido(cadena) == []
    cadena[-1] = [0]
    assert len(ciclo_dirigido(cadena)) == n
    ar = [(i, i + 1) for i in range(n - 1)]
    assert ciclo_no_dirigido(n, ar) == []
    assert len(ciclo_no_dirigido(n, ar + [(n - 1, 0)])) == n

    for _ in range(2000):
        n = random.randint(1, 8)
        m = random.randint(0, 10)
        aristas = [(random.randrange(n), random.randrange(n)) for _ in range(m)]

        # --- Dirigido: bruta con clausura transitiva (caminos de ≥ 1 arista)
        adj = [[] for _ in range(n)]
        for u, v in aristas:
            adj[u].append(v)
        R = [[False] * n for _ in range(n)]
        for u, v in aristas:
            R[u][v] = True
        for k in range(n):
            for i in range(n):
                if R[i][k]:
                    for j in range(n):
                        if R[k][j]:
                            R[i][j] = True
        hay = any(R[v][v] for v in range(n))
        c = ciclo_dirigido(adj)
        assert bool(c) == hay
        if c:
            assert len(set(c)) == len(c)
            assert all(c[(i + 1) % len(c)] in adj[c[i]] for i in range(len(c)))

        # --- No dirigido: hay ciclo ⇔ m > n − componentes
        hay = m > n - _componentes(n, aristas)
        c = ciclo_no_dirigido(n, aristas)
        assert bool(c) == hay
        if c:
            k = len(c)
            assert len(set(c)) == k
            if k == 1:
                assert (c[0], c[0]) in aristas
            elif k == 2:                   # necesita dos aristas distintas entre ellos
                assert sum(1 for e in aristas if set(e) == set(c)) >= 2
            else:
                for i in range(k):
                    a, b = c[i], c[(i + 1) % k]
                    assert (a, b) in aristas or (b, a) in aristas
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
