"""
Grafos — Representación de grafos («Graph representation»)
Nivel: Básico
Ejecutar: python representacion_grafos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Antes de correr cualquier algoritmo de grafos hay que GUARDAR el grafo
    en una estructura. La elección decide la complejidad de todo lo demás:
    lista de adyacencia (casi siempre), matriz (N pequeño o grafo denso),
    lista de aristas (Kruskal, Bellman-Ford, ordenar aristas por peso).
    Señales en el enunciado: «ciudades y carreteras», «usuarios y amistades»,
    «N nodos y M aristas», «u v w», «una grilla de '.' y '#'» (también es un
    grafo: cada celda es un vértice y las celdas vecinas están conectadas).

FUNCIÓN
    leer_grafo(tokens, dirigido=False, ponderado=False, base=1)
        -> (n, adj, aristas)
        Lee «n m» y luego m aristas «u v» o «u v w» desde un iterador de
        tokens; convierte a índices desde 0 restando `base`.
        adj[u] = [v, ...]  o  [(v, w), ...] si ponderado.
        aristas = [(u, v)] o [(u, v, w)] tal como venían (ya en base 0).
    lista_adyacencia(n, aristas, dirigido=False) -> adj
        Acepta aristas (u, v) o (u, v, w); en el segundo caso guarda (v, w).
    matriz_adyacencia(n, aristas, dirigido=False) -> M   M[u][v] = 1/0
    matriz_pesos(n, aristas, dirigido=False) -> M   peso mínimo, INF si no hay,
        0 en la diagonal salvo un lazo negativo (punto de partida de
        Floyd–Warshall).
    vecinos_grilla(grilla, f, c, ocho=False) -> generador de (nf, nc)
        Celdas vecinas (4 u 8 direcciones) dentro de la grilla y no '#'.
    grilla_a_grafo(grilla, ocho=False) -> adj
        Numera la celda (f, c) como f*C + c y arma su lista de adyacencia.

IDEA Y ALGORITMO
    Un grafo es un conjunto de vértices 0..n-1 y de aristas (u, v), quizá
    con peso w. «No dirigido» = la arista se puede recorrer en ambos
    sentidos, por eso se guarda DOS veces (u→v y v→u). Tres formas de
    guardarlo:
      · Lista de adyacencia: adj[u] = vecinos de u. Memoria O(n + m) y
        recorrer los vecinos de u cuesta O(grado(u)), así que BFS/DFS/
        Dijkstra quedan en O(n + m). Es la opción por defecto.
      · Matriz de adyacencia: M[u][v]. Pregunta «¿hay arista u–v?» en O(1),
        pero memoria O(n²) y recorrer vecinos cuesta O(n). Sirve con
        n ≤ ~500 (Floyd–Warshall, grafos densos, clausura transitiva).
      · Lista de aristas: [(w, u, v), ...]. Cuando el algoritmo procesa
        aristas sin importar el vértice: Kruskal (ordenar por peso),
        Bellman-Ford (relajar todas).
    Grillas: NO hace falta construir el grafo. Las celdas son vértices y los
    vecinos se generan sumando desplazamientos (df, dc) de una tabla de 4 u
    8 direcciones y verificando que la celda quede dentro y sea transitable.
    Si un algoritmo exige vértices numerados, (f, c) ↦ f*C + c es una
    biyección con 0..F*C-1 (y de vuelta: f, c = divmod(id, C)).
    Lectura rápida: leer TODA la entrada con sys.stdin.buffer.read().split()
    y consumir tokens con un iterador; con m ~ 10^5–10^6 aristas, input()
    línea por línea es varias veces más lento.

MACROALGORITMO
    1. Leer n y m.
    2. Crear adj = [[] for _ in range(n)]   (NUNCA [[]] * n: misma lista).
    3. Por cada arista: leer u, v (y w), restar la base (1 si viene 1..n).
    4. adj[u].append(v) (o (v, w)); si no es dirigido, también adj[v].append(u).
    5. Si el algoritmo necesita matriz: M[u][v] = min(M[u][v], w) para
       quedarse con la arista más barata cuando hay repetidas.
    6. Grillas: recorrer DIR4/DIR8 y filtrar 0 ≤ nf < F, 0 ≤ nc < C, no '#'.

COMPLEJIDAD
    Lista de adyacencia: O(n + m) tiempo y memoria. Matriz: O(n²).
    En Python se leen y guardan ~10^6 aristas en ~1 s con lectura en bloque.

EJEMPLO A MANO
    Entrada (1..n, no dirigido, ponderado):  4 4 / 1 2 5 / 2 3 1 / 3 1 2 / 3 4 7
      adj[0] = [(1,5), (2,2)]      adj[1] = [(0,5), (2,1)]
      adj[2] = [(1,1), (0,2), (3,7)]   adj[3] = [(2,7)]
    Grilla  ".#."  vecinos 4 de (1,1): (0,1) es '#', quedan (2,1), (1,0), (1,2).
            "..."
            "..."

ERRORES TÍPICOS
    - adj = [[]] * n: las n entradas son LA MISMA lista; todo se mezcla.
    - Olvidar restar 1 cuando los vértices vienen numerados 1..n (IndexError
      o, peor, un grafo corrido sin error).
    - En no dirigido, agregar solo u→v. En dirigido, agregar también v→u.
    - Matriz con aristas repetidas: sobrescribir en vez de quedarse con el
      mínimo; o confundir 0 = «sin arista» con una arista de peso 0.
    - Grillas: confundir (fila, columna) con (x, y) o revisar límites con
      <= en vez de <.

VARIANTES Y RELACIONADOS
    - Guardar el índice de la arista: adj[u].append((v, id)) — necesario para
      puentes (puentes_articulacion.py) y ciclos con aristas repetidas.
    - Grafo transpuesto (aristas invertidas): scc.py, alcanzabilidad inversa.
    - Implícito: los vecinos se calculan al vuelo (grillas, bfs_estados.py).
    - Todo el resto de 05_Grafos parte de aquí: bfs.py, dfs.py, dijkstra.py…

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/C - Celestial Veins (armar el grafo de vínculos
      mutuos antes de recorrerlo)
    - ICPC/Colombia 2018/I - Impossible Communication (grafo + transpuesto,
      y un nodo virtual en vez de una clique)
    - 2026-1/problemas: UVa 10004 «Bicoloring» y UVa 10986 «Sending email»
      (lectura de varios casos con n, m y aristas)
    - CSES «Counting Rooms» (grilla como grafo)

VERIFICACIÓN
    - Pruebas: OK en 1500 grafos aleatorios (lista vs. matriz vs. lista de
      aristas, lectura desde texto, suma de grados = 2m) y 300 grillas
      aleatorias (vecinos contra fuerza bruta celda por celda)
      (python representacion_grafos.py)
"""
import random

INF = float("inf")

# Desplazamientos (df, dc): 4 vecinos (arriba, abajo, izquierda, derecha)
# y 8 vecinos (añade las diagonales).
DIR4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIR8 = DIR4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def lista_adyacencia(n, aristas, dirigido=False):
    """adj[u] = lista de vecinos (v) o de pares (v, w) si las aristas traen peso."""
    adj = [[] for _ in range(n)]          # NO usar [[]] * n
    for a in aristas:
        if len(a) == 2:
            u, v = a
            adj[u].append(v)
            if not dirigido:
                adj[v].append(u)
        else:
            u, v, w = a
            adj[u].append((v, w))
            if not dirigido:
                adj[v].append((u, w))
    return adj


def matriz_adyacencia(n, aristas, dirigido=False):
    """M[u][v] = 1 si hay arista u→v (o u–v), 0 si no."""
    M = [[0] * n for _ in range(n)]
    for a in aristas:
        u, v = a[0], a[1]
        M[u][v] = 1
        if not dirigido:
            M[v][u] = 1
    return M


def matriz_pesos(n, aristas, dirigido=False):
    """M[u][v] = peso mínimo de una arista u→v, INF si no hay, 0 en la diagonal."""
    M = [[INF] * n for _ in range(n)]
    for i in range(n):
        M[i][i] = 0
    for u, v, w in aristas:
        # Con aristas repetidas solo importa la más barata.
        if w < M[u][v]:
            M[u][v] = w
        if not dirigido and w < M[v][u]:
            M[v][u] = w
    return M


def leer_grafo(tokens, dirigido=False, ponderado=False, base=1):
    """Lee «n m» y m aristas desde un iterador de tokens (bytes o str).

    Uso típico en competencia:
        tokens = iter(sys.stdin.buffer.read().split())
        n, adj, aristas = leer_grafo(tokens)
    """
    n = int(next(tokens))
    m = int(next(tokens))
    aristas = []
    for _ in range(m):
        u = int(next(tokens)) - base      # pasar a índices desde 0
        v = int(next(tokens)) - base
        if ponderado:
            aristas.append((u, v, int(next(tokens))))
        else:
            aristas.append((u, v))
    return n, lista_adyacencia(n, aristas, dirigido), aristas


def vecinos_grilla(grilla, f, c, ocho=False):
    """Celdas vecinas de (f, c) dentro de la grilla y distintas de '#'."""
    F, C = len(grilla), len(grilla[0])
    for df, dc in (DIR8 if ocho else DIR4):
        nf, nc = f + df, c + dc
        if 0 <= nf < F and 0 <= nc < C and grilla[nf][nc] != '#':
            yield nf, nc


def grilla_a_grafo(grilla, ocho=False):
    """Lista de adyacencia de la grilla con la celda (f, c) numerada f*C + c.

    Las celdas '#' quedan como vértices aislados (sin aristas).
    """
    F, C = len(grilla), len(grilla[0])
    adj = [[] for _ in range(F * C)]
    for f in range(F):
        for c in range(C):
            if grilla[f][c] != '#':
                for nf, nc in vecinos_grilla(grilla, f, c, ocho):
                    adj[f * C + c].append(nf * C + nc)
    return adj


def demo():
    texto = "4 4\n1 2 5\n2 3 1\n3 1 2\n3 4 7\n"
    n, adj, aristas = leer_grafo(iter(texto.split()), ponderado=True)
    print("aristas (base 0):", aristas)
    for u in range(n):
        print(f"adj[{u}] =", adj[u])
    M = matriz_pesos(n, aristas)
    print("matriz de pesos:")
    for fila in M:
        print("   ", ["∞" if x == INF else x for x in fila])
    grilla = [".#.", "...", "..."]
    print("grilla:", grilla)
    print("vecinos 4 de (1,1):", list(vecinos_grilla(grilla, 1, 1)))
    print("vecinos 8 de (1,1):", list(vecinos_grilla(grilla, 1, 1, ocho=True)))


def pruebas():
    random.seed(2024)
    casos = 0

    # Casos borde
    assert lista_adyacencia(0, []) == []
    assert lista_adyacencia(1, []) == [[]]
    assert lista_adyacencia(1, [(0, 0)], dirigido=True) == [[0]]
    assert matriz_pesos(2, [(0, 1, 5), (0, 1, 3)]) == [[0, 3], [3, 0]]
    adj = lista_adyacencia(3, [])
    adj[0].append(1)
    assert adj[1] == [] and adj[2] == []     # listas independientes

    # Grafos aleatorios: las tres representaciones dicen lo mismo
    for _ in range(1500):
        n = random.randint(1, 8)
        m = random.randint(0, 12)
        dirigido = random.random() < 0.5
        ponderado = random.random() < 0.5
        aristas = []
        for _ in range(m):
            u, v = random.randrange(n), random.randrange(n)
            aristas.append((u, v, random.randint(-5, 9)) if ponderado else (u, v))
        adj = lista_adyacencia(n, aristas, dirigido)
        M = matriz_adyacencia(n, aristas, dirigido)
        # Fuerza bruta: ¿existe u→v? mirando directamente la lista de aristas
        for u in range(n):
            for v in range(n):
                existe = any((a[0] == u and a[1] == v) or
                             (not dirigido and a[0] == v and a[1] == u)
                             for a in aristas)
                vecinos = [x[0] if ponderado else x for x in adj[u]]
                assert (v in vecinos) == existe == (M[u][v] == 1)
        # Suma de grados (de salida) = m dirigido, 2m no dirigido
        assert sum(len(l) for l in adj) == (m if dirigido else 2 * m)
        if ponderado:
            P = matriz_pesos(n, aristas, dirigido)
            for u in range(n):
                for v in range(n):
                    ws = [a[2] for a in aristas if (a[0], a[1]) == (u, v) or
                          (not dirigido and (a[0], a[1]) == (v, u))]
                    # En la diagonal: 0, salvo un lazo negativo (ciclo negativo)
                    esperado = min(ws + [0]) if u == v else min(ws, default=INF)
                    assert P[u][v] == esperado
        # Leer desde texto en base 1 reproduce lo mismo
        lineas = [f"{n} {m}"] + [" ".join(str(x + 1) if i < 2 else str(x)
                                          for i, x in enumerate(a)) for a in aristas]
        n2, adj2, ar2 = leer_grafo(iter("\n".join(lineas).encode().split()),
                                   dirigido, ponderado)
        assert n2 == n and adj2 == adj and ar2 == aristas
        casos += 1

    # Grillas aleatorias: vecinos contra fuerza bruta
    for _ in range(300):
        F, C = random.randint(1, 6), random.randint(1, 6)
        grilla = ["".join(random.choice(".#") for _ in range(C)) for _ in range(F)]
        for ocho in (False, True):
            adj = grilla_a_grafo(grilla, ocho)
            for f in range(F):
                for c in range(C):
                    esperado = set()
                    if grilla[f][c] != '#':
                        for g in range(F):
                            for d in range(C):
                                df, dc = abs(g - f), abs(d - c)
                                cerca = (df + dc == 1) or (ocho and df == 1 and dc == 1)
                                if cerca and grilla[g][d] != '#':
                                    esperado.add(g * C + d)
                    assert set(adj[f * C + c]) == esperado
                    assert len(adj[f * C + c]) == len(esperado)   # sin repetidos
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
