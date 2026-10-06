"""
Grafos — Puentes y puntos de articulación («Bridges and articulation points»)
Nivel: Intermedio
Ejecutar: python puentes_articulacion.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    En un grafo NO dirigido:
      · PUENTE: arista cuya eliminación aumenta el número de componentes
        conexas (desconecta algo).
      · PUNTO DE ARTICULACIÓN (vértice de corte): vértice cuya eliminación
        (con sus aristas) aumenta el número de componentes.
    Se calculan TODOS en un solo DFS, O(n + m).
    Señales en el enunciado: «enlaces críticos», «carreteras / ciudades
    necesarias», «si se cae este servidor, ¿se desconecta la red?», «¿qué
    calles se pueden volver de un solo sentido?» (las que no son puente),
    componentes 2-arista-conexas o biconexas.

FUNCIÓN
    puentes_articulaciones(n, aristas) -> (puentes, articulaciones)
        aristas = [(u, v)] (índices desde 0; admite aristas paralelas y lazos).
        puentes = lista ordenada de ÍNDICES de aristas que son puente.
        articulaciones = lista ordenada de vértices de corte.

IDEA Y ALGORITMO
    DFS con tiempos de entrada tin[v] y el valor low-link:
        low[v] = menor tin alcanzable desde el subárbol de v usando aristas
                 del árbol hacia abajo y UNA arista de retroceso.
    En un grafo no dirigido el DFS solo produce aristas de árbol y de
    retroceso (a un ancestro), nunca de cruce. Entonces, para la arista de
    árbol p–v (p padre de v):
      · p–v es PUENTE ⇔ low[v] > tin[p]: nada del subárbol de v tiene una
        arista que vuelva a p o más arriba, así que quitando p–v el subárbol
        queda aislado. Si low[v] ≤ tin[p], hay un camino alternativo.
      · p (no raíz) es ARTICULACIÓN ⇔ algún hijo v tiene low[v] ≥ tin[p]:
        el subárbol de v solo llega hasta p, así que sin p queda aislado.
      · La raíz es articulación ⇔ tiene ≥ 2 hijos en el árbol DFS (entre
        subárboles de hijos distintos no hay aristas: no hay cruce).
    Cálculo: low[v] = min(tin[v], tin[w] por cada retroceso v–w, low[h] por
    cada hijo h). Para no confundir la arista de vuelta al padre con un
    retroceso se ignora la arista por su ÍNDICE (no por el vértice padre):
    así dos aristas paralelas p–v se ven como ciclo y no son puente.
    Iterativo (pila con índice de vecino, como dfs.py): cuando v termina,
    se actualiza low[padre] y se aplican las dos pruebas.
    Ingenuo: quitar cada arista/vértice y contar componentes: O(m·(n+m)).

MACROALGORITMO
    1. adj[u] = [(v, id)]; tin = [-1]*n; reloj = 0.
    2. Para cada raíz r sin visitar: tin[r] = low[r] = reloj++; pila = [r].
    3. Tope v: si quedan vecinos (w, id): si id es la arista de llegada,
       saltar; si w no visitado: tin[w] = low[w] = reloj++, guardar padre y
       arista, apilar; si ya visitado: low[v] = min(low[v], tin[w]).
    4. Si v no tiene más vecinos: desapilar; con p = padre:
       low[p] = min(low[p], low[v]); si low[v] > tin[p] → arista puente;
       si p no es raíz y low[v] ≥ tin[p] → p articulación; si p es raíz,
       contar un hijo más.
    5. Raíz con ≥ 2 hijos → articulación.

COMPLEJIDAD
    O(n + m) tiempo y memoria. ~10^6 aristas por segundo en Python.

EJEMPLO A MANO
    Aristas: e0 0-1, e1 1-2, e2 2-0, e3 1-3, e4 3-4, e5 4-5, e6 5-3.
    (Dos triángulos 0-1-2 y 3-4-5 unidos por la arista 1-3.)
    DFS desde 0: tin 0→0, 1→1, 2→2 (retroceso 2-0: low[2]=0), 3→3, 4→4,
    5→5 (retroceso 5-3: low[5]=3) → low[4]=3, low[3]=3, low[1]=0.
      Arista 1-3: low[3] = 3 > tin[1] = 1 → PUENTE (e3).
      Vértice 1: hijo 3 con low 3 ≥ tin[1] = 1 → ARTICULACIÓN.
      Vértice 3: hijo 4 con low 3 ≥ tin[3] = 3 → ARTICULACIÓN.
    Resultado: puentes [3], articulaciones [1, 3].

ERRORES TÍPICOS
    - Ignorar al vértice padre en vez de a la ARISTA de llegada: con aristas
      paralelas reporta puentes falsos.
    - Aplicar a la raíz la regla low[v] ≥ tin[p] (siempre se cumple): la
      raíz es articulación solo con ≥ 2 hijos DFS.
    - Usar low[w] en vez de tin[w] en las aristas de retroceso: para
      puentes da igual, para articulaciones da respuestas incorrectas.
    - DFS recursivo con n = 10^5: RecursionError.
    - Un mismo vértice puede cumplir la condición con varios hijos: no
      reportarlo repetido.

VARIANTES Y RELACIONADOS
    - Componentes 2-arista-conexas: quitar los puentes y sacar componentes.
    - Componentes biconexas (por vértices): pila de aristas durante el DFS.
    - Orientar un grafo para que sea fuertemente conexo: posible ⇔ conexo y
      sin puentes (orientar aristas de árbol hacia abajo y retrocesos hacia
      arriba).
    - Dirigido: el mismo low-link da componentes fuertemente conexas (scc.py).
    - DFS iterativo base: dfs.py.

DÓNDE PRACTICAR
    - CSES «Necessary Roads» (puentes), «Necessary Cities» (articulaciones)
    - UVa 796 «Critical Links» (puentes), UVa 315 «Network» (articulaciones)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (quitar cada arista / cada vértice y
      contar componentes) en 2000 grafos aleatorios con aristas paralelas y
      lazos; un camino de 100000 vértices (todo puente) sin recursión
      (python puentes_articulacion.py)
"""
import random


def puentes_articulaciones(n, aristas):
    """(índices de aristas puente, vértices de articulación), ambos ordenados."""
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(aristas):
        adj[u].append((v, i))
        if u != v:
            adj[v].append((u, i))
    tin = [-1] * n
    low = [0] * n
    padre = [-1] * n
    llegada = [-1] * n          # índice de la arista de árbol que llega a v
    it = [0] * n
    es_art = [False] * n
    puentes = []
    reloj = 0
    for r in range(n):
        if tin[r] != -1:
            continue
        tin[r] = low[r] = reloj
        reloj += 1
        hijos_raiz = 0
        pila = [r]
        while pila:
            v = pila[-1]
            if it[v] < len(adj[v]):
                w, i = adj[v][it[v]]
                it[v] += 1
                if i == llegada[v]:            # la misma arista de vuelta al padre
                    continue
                if tin[w] == -1:               # arista de árbol: «llamar» a w
                    padre[w] = v
                    llegada[w] = i
                    tin[w] = low[w] = reloj
                    reloj += 1
                    pila.append(w)
                elif tin[w] < low[v]:          # arista de retroceso (o lazo)
                    low[v] = tin[w]
            else:                              # v terminó: informar al padre
                pila.pop()
                p = padre[v]
                if p == -1:
                    continue
                if low[v] < low[p]:
                    low[p] = low[v]
                if low[v] > tin[p]:
                    puentes.append(llegada[v])
                if p == r:
                    hijos_raiz += 1
                elif low[v] >= tin[p]:
                    es_art[p] = True
        if hijos_raiz >= 2:
            es_art[r] = True
    return sorted(puentes), [v for v in range(n) if es_art[v]]


def _componentes(n, aristas, quitado=-1):
    """Número de componentes (sin contar el vértice `quitado`), etiquetado ingenuo."""
    etiqueta = list(range(n))
    cambio = True
    while cambio:
        cambio = False
        for u, v in aristas:
            if quitado in (u, v):
                continue
            m = min(etiqueta[u], etiqueta[v])
            if etiqueta[u] != m or etiqueta[v] != m:
                etiqueta[u] = etiqueta[v] = m
                cambio = True
    return len({etiqueta[v] for v in range(n) if v != quitado})


def demo():
    aristas = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 5), (5, 3)]
    p, a = puentes_articulaciones(6, aristas)
    print("aristas:", list(enumerate(aristas)))
    print("puentes (índices):", p, "->", [aristas[i] for i in p])   # [3] -> [(1, 3)]
    print("articulaciones:", a)                                      # [1, 3]
    print("con 1-3 duplicada:", puentes_articulaciones(6, aristas + [(3, 1)]))


def pruebas():
    random.seed(796)
    casos = 0

    assert puentes_articulaciones(0, []) == ([], [])
    assert puentes_articulaciones(1, [(0, 0)]) == ([], [])
    assert puentes_articulaciones(2, [(0, 1)]) == ([0], [])
    assert puentes_articulaciones(2, [(0, 1), (1, 0)]) == ([], [])     # paralelas
    assert puentes_articulaciones(3, [(0, 1), (1, 2)]) == ([0, 1], [1])

    # Camino largo: todas las aristas son puente, todos los internos articulación
    n = 100000
    p, a = puentes_articulaciones(n, [(i, i + 1) for i in range(n - 1)])
    assert p == list(range(n - 1)) and a == list(range(1, n - 1))

    for _ in range(2000):
        n = random.randint(1, 8)
        m = random.randint(0, 11)
        aristas = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
        p, a = puentes_articulaciones(n, aristas)
        base = _componentes(n, aristas)
        # Fuerza bruta: quitar cada arista / cada vértice y contar componentes
        bruta_p = [i for i in range(m)
                   if _componentes(n, aristas[:i] + aristas[i + 1:]) > base]
        bruta_a = [v for v in range(n) if _componentes(n, aristas, v) > base]
        assert p == bruta_p and a == bruta_a
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
