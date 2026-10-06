"""
Grafos — Emparejamiento bipartito máximo: Kuhn y Hopcroft–Karp; teorema de König
         («Maximum bipartite matching»)
Nivel: Avanzado
Ejecutar: python emparejamiento_bipartito.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Dado un grafo bipartito (izquierda L, derecha R; p. ej. personas y
    tareas, alumnos y cupos), elegir el máximo número de aristas sin
    vértices en común: cada persona a lo sumo una tarea y viceversa.
    Por el teorema de König, en bipartitos ese número también es la
    COBERTURA MÍNIMA DE VÉRTICES (mínimo de vértices que tocan todas las
    aristas), y |L| + |R| − ese número es el CONJUNTO INDEPENDIENTE MÁXIMO.
    Señales en el enunciado: «asignar a cada uno a lo sumo uno», «parejas
    compatibles», «máximo de pares», tablero donde cada ficha ocupa dos
    casillas de distinto color, «mínimo de filas/columnas que cubren todas
    las marcas», «máximo de elementos sin conflicto» en un grafo bipartito.

FUNCIÓN
    kuhn(nl, nr, ady)          -> (tam, pareja_izq, pareja_der)
    hopcroft_karp(nl, nr, ady) -> (tam, pareja_izq, pareja_der)
        ady[u] = lista de vértices derechos (0..nr-1) compatibles con el
        izquierdo u (0..nl-1). pareja_izq[u] = derecho emparejado o -1;
        pareja_der[v] = izquierdo emparejado o -1.
    cobertura_minima(nl, nr, ady, pareja_izq, pareja_der) -> (cub_izq, cub_der)
        Listas de vértices de una cobertura mínima (König), a partir de un
        emparejamiento MÁXIMO. |cub_izq| + |cub_der| = tam.

IDEA Y ALGORITMO
    Camino de aumento: camino que empieza en un izquierdo libre, alterna
    arista NO usada / arista usada, y termina en un derecho libre. Si se
    «voltea» (las no usadas pasan a usadas y viceversa) el emparejamiento
    crece en 1. Teorema de Berge: un emparejamiento es máximo ⇔ no tiene
    camino de aumento.
    Kuhn: para cada izquierdo u, buscar con DFS un camino de aumento desde
    u (probar cada derecho v vecino: si está libre, listo; si no, intentar
    re-emparejar a su pareja actual en otro lado). Un vértice que falló
    una vez no ganará después (mientras no cambie u), así que basta un
    intento por izquierdo: O(V·E). Muy corto y suficiente para ~500×500.
    Hopcroft–Karp: por fases, como Dinic. BFS desde TODOS los izquierdos
    libres a la vez da capas (distancias); luego DFS solo por aristas que
    avanzan una capa encuentra un conjunto maximal de caminos de aumento
    más cortos y disjuntos. Hay O(√V) fases → O(E·√V).
    König: sea Z el conjunto de vértices alcanzables desde los izquierdos
    libres por caminos alternantes (L → R por aristas no usadas, R → L por
    aristas usadas). Cobertura = (L − Z) ∪ (R ∩ Z). Cubre todo: una arista
    u–v con u ∈ Z tiene v ∈ Z (se puede seguir), y si u ∉ Z, u está en la
    cobertura. Tamaño: cada vértice elegido es extremo de una arista usada
    distinta (los derechos de Z están emparejados, si no habría camino de
    aumento; los izquierdos fuera de Z están emparejados porque los libres
    están en Z) → tamaño = emparejamiento. Y nunca puede ser menor
    (cada arista usada necesita su propio vértice): es mínima.

MACROALGORITMO
    Kuhn:
    1. pareja_izq = pareja_der = −1.
    2. Para cada izquierdo s: marcar todos los derechos como no vistos.
    3. DFS iterativo desde s: tomar un derecho v vecino no visto, marcarlo;
       si está libre, voltear el camino de la pila; si no, apilar pareja_der[v].
    4. Si un izquierdo agota sus vecinos, desapilarlo.
    Hopcroft–Karp:
    1. BFS desde todos los izquierdos libres (dist 0) siguiendo
       u → v (cualquier arista) → pareja_der[v] (dist + 1).
    2. Si ningún derecho libre fue alcanzado: terminar.
    3. Desde cada izquierdo libre, DFS que solo baja de u a w = pareja_der[v]
       si dist[w] = dist[u] + 1; un izquierdo sin salida se descarta (dist = −1).
    4. Voltear cada camino encontrado y repetir desde 1.

COMPLEJIDAD
    Kuhn O(V·E); Hopcroft–Karp O(E·√V); König O(V + E). Memoria O(V + E).
    En Python: Hopcroft–Karp con 10^5 aristas en ~1 s; Kuhn para unos
    pocos miles de aristas.

EJEMPLO A MANO
    L = {0,1,2}, R = {0,1,2}; ady: 0:[0,1], 1:[0], 2:[1,2].
    Kuhn: s=0 → v=0 libre: 0–0.
          s=1 → v=0 ocupado por 0; intentar 0 en otro: v=1 libre.
                Voltear: 1–0, 0–1.
          s=2 → v=1 ocupado por 0; 0 prueba v=0, ocupado por 1, y 1 no
                tiene otra opción → falla; v=2 libre: 2–2.  Tamaño 3.
    König con el grafo ady 0:[0], 1:[0], 2:[0,1] (máximo 2: 0–0, 2–1):
    izquierdo libre 1 → Z = {L1, R0, L0}. Cobertura = (L − Z) ∪ (R ∩ Z)
    = {L2} ∪ {R0}: dos vértices que tocan las 4 aristas.

ERRORES TÍPICOS
    - En Kuhn, no reiniciar «visto» para cada nuevo s (falla) o
      reiniciarlo dentro del DFS (exponencial).
    - Mezclar índices de izquierda y derecha en un mismo arreglo sin
      desplazarlos.
    - Aplicar König o «tam = cobertura» en grafos NO bipartitos (ahí la
      cobertura mínima es NP-difícil).
    - Calcular la cobertura con un emparejamiento que no es máximo.
    - DFS recursivo con caminos de aumento largos (miles de vértices).

VARIANTES Y RELACIONADOS
    - Conjunto independiente máximo = nl + nr − tam (complemento de la
      cobertura).
    - Cobertura mínima por caminos en un DAG = n − emparejamiento entre
      copias «salida» y «entrada» de los vértices.
    - Con capacidades (cada tarea admite k personas): flujo con dinic.py.
    - Con pesos (costo mínimo de una asignación perfecta): hungaro.py.
    - bipartito.py (verificar que el grafo es bipartito / 2-colorearlo).

DÓNDE PRACTICAR
    - Ningún problema del repo lo usa directamente (Colombia 2023 H es la
      versión con pesos: hungaro.py).
    - CSES «School Dance»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (probar todas las formas de emparejar
      cada izquierdo con un derecho libre o con nadie) en 1500 grafos
      aleatorios con hasta 7×7 vértices: Kuhn == Hopcroft–Karp == bruto,
      los emparejamientos son válidos, y la cobertura de König cubre todas
      las aristas con tam vértices; casos borde y un grafo de 2·10^4
      vértices con emparejamiento perfecto escondido
      (python emparejamiento_bipartito.py)
"""
import random
from collections import deque


def kuhn(nl, nr, ady):
    """Emparejamiento máximo con Kuhn (caminos de aumento por DFS iterativo)."""
    pareja_izq = [-1] * nl
    pareja_der = [-1] * nr
    visto = [-1] * nr                  # visto[v] == s ⇔ v ya se probó al buscar desde s
    tam = 0
    for s in range(nl):
        ptr = {}                       # siguiente vecino por probar de cada izquierdo
        pila_u = [s]                   # izquierdos del camino alternante
        pila_v = []                    # pila_v[k] = derecho elegido por pila_u[k]
        hallado = False
        while pila_u:
            u = pila_u[-1]
            i = ptr.get(u, 0)
            if i < len(ady[u]):
                ptr[u] = i + 1
                v = ady[u][i]
                if visto[v] == s:
                    continue
                visto[v] = s
                pila_v.append(v)
                if pareja_der[v] == -1:
                    hallado = True     # camino de aumento s → … → v
                    break
                pila_u.append(pareja_der[v])   # intentar mover a la pareja de v
            else:
                pila_u.pop()           # u no logra nada: retroceder
                if pila_v:
                    pila_v.pop()
        if hallado:
            # voltear: cada izquierdo del camino toma el derecho que eligió
            for u, v in zip(pila_u, pila_v):
                pareja_izq[u] = v
                pareja_der[v] = u
            tam += 1
    return tam, pareja_izq, pareja_der


def hopcroft_karp(nl, nr, ady):
    """Emparejamiento máximo con Hopcroft–Karp, O(E·√V)."""
    pareja_izq = [-1] * nl
    pareja_der = [-1] * nr
    tam = 0
    while True:
        # BFS por capas desde todos los izquierdos libres
        dist = [-1] * nl
        q = deque()
        for u in range(nl):
            if pareja_izq[u] == -1:
                dist[u] = 0
                q.append(u)
        hay_libre = False
        while q:
            u = q.popleft()
            for v in ady[u]:
                w = pareja_der[v]
                if w == -1:
                    hay_libre = True   # se alcanza un derecho libre
                elif dist[w] == -1:
                    dist[w] = dist[u] + 1
                    q.append(w)
        if not hay_libre:
            return tam, pareja_izq, pareja_der
        # DFS iterativo por las capas desde cada izquierdo libre
        ptr = [0] * nl
        for s in range(nl):
            if pareja_izq[s] != -1:
                continue
            pila_u = [s]
            pila_v = []
            hallado = False
            while pila_u:
                u = pila_u[-1]
                if ptr[u] < len(ady[u]):
                    v = ady[u][ptr[u]]
                    ptr[u] += 1
                    w = pareja_der[v]
                    if w == -1:
                        pila_v.append(v)
                        hallado = True
                        break
                    if dist[w] == dist[u] + 1:
                        pila_v.append(v)
                        pila_u.append(w)
                else:
                    dist[u] = -1       # sin salida: nadie más debe entrar aquí en esta fase
                    pila_u.pop()
                    if pila_v:
                        pila_v.pop()
            if hallado:
                for u, v in zip(pila_u, pila_v):
                    pareja_izq[u] = v
                    pareja_der[v] = u
                tam += 1


def cobertura_minima(nl, nr, ady, pareja_izq, pareja_der):
    """Cobertura mínima de vértices (König) desde un emparejamiento máximo."""
    z_izq = [False] * nl
    z_der = [False] * nr
    pila = [u for u in range(nl) if pareja_izq[u] == -1]
    for u in pila:
        z_izq[u] = True
    while pila:
        u = pila.pop()
        for v in ady[u]:
            if v != pareja_izq[u] and not z_der[v]:   # L → R por arista no usada
                z_der[v] = True
                w = pareja_der[v]                     # R → L por arista usada
                if w != -1 and not z_izq[w]:
                    z_izq[w] = True
                    pila.append(w)
    cub_izq = [u for u in range(nl) if not z_izq[u]]
    cub_der = [v for v in range(nr) if z_der[v]]
    return cub_izq, cub_der


def demo():
    ady = [[0, 1], [0], [1, 2]]
    print("Kuhn:", kuhn(3, 3, ady))                       # (3, [1, 0, 2], [1, 0, 2])
    print("Hopcroft–Karp:", hopcroft_karp(3, 3, ady))
    ady2 = [[0], [0], [0, 1]]
    tam, pi, pd = hopcroft_karp(3, 2, ady2)
    print("Grafo 2: emparejamiento", tam, "cobertura (izq, der):",
          cobertura_minima(3, 2, ady2, pi, pd))           # ([2], [0])


# ---------- pruebas ----------

def _bruto(nl, nr, ady):
    """Máximo emparejamiento probando para cada izquierdo: nadie o un derecho libre."""
    usado = [False] * nr
    mejor = 0

    def ir(u, cuenta):                 # profundidad ≤ nl ≤ 7
        nonlocal mejor
        if u == nl:
            mejor = max(mejor, cuenta)
            return
        ir(u + 1, cuenta)
        for v in set(ady[u]):
            if not usado[v]:
                usado[v] = True
                ir(u + 1, cuenta + 1)
                usado[v] = False

    ir(0, 0)
    return mejor


def _valido(nl, nr, ady, res):
    tam, pi, pd = res
    assert sum(1 for x in pi if x != -1) == tam
    for u in range(nl):
        if pi[u] != -1:
            assert pi[u] in ady[u] and pd[pi[u]] == u
    for v in range(nr):
        if pd[v] != -1:
            assert pi[pd[v]] == v


def pruebas():
    random.seed(1931)

    # Casos borde
    assert kuhn(0, 0, []) == (0, [], []) and hopcroft_karp(0, 3, [])[0] == 0
    assert kuhn(3, 0, [[], [], []])[0] == 0 and hopcroft_karp(3, 0, [[], [], []])[0] == 0
    assert kuhn(2, 1, [[0], [0]])[0] == 1
    assert hopcroft_karp(2, 2, [[0, 0, 1], [0]])[0] == 2     # vecinos repetidos

    for _ in range(1500):
        nl, nr = random.randint(0, 7), random.randint(0, 7)
        p = random.random()
        ady = [[v for v in range(nr) if random.random() < p] for _ in range(nl)]
        for u in range(nl):
            random.shuffle(ady[u])
        esperado = _bruto(nl, nr, ady)
        for f in (kuhn, hopcroft_karp):
            res = f(nl, nr, ady)
            assert res[0] == esperado
            _valido(nl, nr, ady, res)
        # König: la cobertura toca todas las aristas y tiene tam vértices
        tam, pi, pd = hopcroft_karp(nl, nr, ady)
        ci, cd = cobertura_minima(nl, nr, ady, pi, pd)
        assert len(ci) + len(cd) == tam
        si, sd = set(ci), set(cd)
        assert all(u in si or v in sd for u in range(nl) for v in ady[u])

    # Grande: 10^4 + 10^4 con una permutación escondida
    N = 10 ** 4
    perm = list(range(N))
    random.shuffle(perm)
    ady = [list({perm[u]} | {random.randrange(N) for _ in range(4)}) for u in range(N)]
    for u in range(N):
        random.shuffle(ady[u])
    res = hopcroft_karp(N, N, ady)
    assert res[0] == N
    _valido(N, N, ady, res)
    assert kuhn(N, N, ady)[0] == N


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
