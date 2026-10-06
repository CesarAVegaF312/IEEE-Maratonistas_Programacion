"""
Grafos — Búsqueda en profundidad iterativa («Depth-First Search, DFS»)
Nivel: Básico
Ejecutar: python dfs.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Recorrer un grafo yendo «lo más hondo posible» antes de retroceder. No
    da distancias mínimas (eso es bfs.py), pero sí ESTRUCTURA: el árbol DFS,
    los tiempos de entrada/salida de cada vértice y la relación
    ancestro–descendiente. Es la base de: detección de ciclos, orden
    topológico, puentes y articulaciones, componentes fuertemente conexas,
    recorridos de árboles (subárboles = intervalos [entrada, salida]).
    Señales en el enunciado: «¿u está en el subárbol de v?», «visitar todo lo
    alcanzable», «ciclo», «dependencias», cualquier problema de árboles.

FUNCIÓN
    dfs(adj) -> (orden, entrada, salida, padre)
        Recorre TODO el grafo (bosque DFS), arrancando por 0, 1, 2… y
        visitando los vecinos en el orden en que aparecen en adj[u]
        (el mismo orden que la versión recursiva).
        orden   = vértices en preorden (en el orden en que se descubren).
        entrada[v], salida[v] = tiempos con un único reloj 0..2n-1.
        padre[v] = padre en el árbol DFS (-1 para las raíces).
    es_ancestro(entrada, salida, u, v) -> bool
        True si u es ancestro de v en el árbol DFS (u es ancestro de sí mismo).

IDEA Y ALGORITMO
    La versión recursiva es: entrar a v, para cada vecino no visitado
    recursar, salir de v. En Python la recursión revienta hacia ~1000
    niveles (y subir el límite puede tumbar el intérprete con 10^5), así que
    se simula la pila de llamadas: cada vértice en la pila recuerda POR QUÉ
    vecino iba (it[v]). En cada paso se mira el tope v:
      · si le quedan vecinos, se toma el siguiente u; si u no está visitado
        se «llama» (se marca entrada y se apila); si ya lo estaba, se sigue;
      · si no le quedan vecinos, la «llamada» termina: se marca salida y se
        desapila.
    Así entrada/salida coinciden EXACTAMENTE con las del DFS recursivo.
    Por qué funcionan los tiempos: v está en la pila durante el intervalo
    [entrada[v], salida[v]], y todo lo que se descubre mientras v está en la
    pila es descendiente de v. Por eso los intervalos de dos vértices o son
    disjuntos o uno contiene al otro («paréntesis»), y
        u ancestro de v  ⇔  entrada[u] ≤ entrada[v] y salida[v] ≤ salida[u].
    OJO: la variante «sacar v, apilar todos sus vecinos» también visita todo
    lo alcanzable, pero NO produce un árbol DFS válido ni tiempos de salida;
    sirve solo para alcanzabilidad/componentes.

MACROALGORITMO
    1. entrada = [-1]*n, it = [0]*n, reloj = 0.
    2. Para cada raíz r no visitada: entrada[r] = reloj++, pila = [r].
    3. Mientras la pila no esté vacía, v = tope:
    4.   si it[v] < grado(v): u = adj[v][it[v]], it[v] += 1;
         si u no visitado: padre[u] = v, entrada[u] = reloj++, apilar u.
    5.   si no: salida[v] = reloj++, desapilar.
    6. Ancestro: comparar intervalos [entrada, salida].

COMPLEJIDAD
    O(n + m) tiempo, O(n) memoria extra. ~10^6 aristas por segundo en Python.

EJEMPLO A MANO
    Dirigido: 0→1, 0→2, 1→3, 2→3, 4→2.
      entra 0 (t0) → entra 1 (t1) → entra 3 (t2) → sale 3 (t3) → sale 1 (t4)
      → entra 2 (t5) [3 ya visto] → sale 2 (t6) → sale 0 (t7)
      → nueva raíz 4: entra (t8) [2 ya visto] → sale (t9)
    entrada = [0, 1, 5, 2, 8], salida = [7, 4, 6, 3, 9]; 0 es ancestro de 3
    ([0,7] ⊇ [2,3]); 2 no lo es ([5,6] y [2,3] disjuntos).

ERRORES TÍPICOS
    - DFS recursivo con 10^5 vértices en línea: RecursionError o caída
      silenciosa del intérprete. Usar la pila explícita.
    - Usar la pila «apilar todos los vecinos» y creer que da tiempos DFS.
    - Grafo no conexo: arrancar solo desde 0 y olvidar las demás raíces.
    - Comparar ancestros con < estricto cuando u == v debe contar.

VARIANTES Y RELACIONADOS
    - Clasificación de aristas dirigidas u→v con los tiempos: árbol
      (padre[v] = u), retroceso (v ancestro de u: ¡ciclo!), avance (u
      ancestro de v, no de árbol), cruce (intervalos disjuntos).
    - Ciclos: deteccion_ciclos.py. Orden topológico: orden_topologico.py
      (también = vértices por salida decreciente).
    - Low-link: puentes_articulacion.py, scc.py. Árboles: lca.py, diametro_arbol.py.
    - Euler tour de árbol: subárbol de v = vértices con entrada en
      [entrada[v], salida[v]] → consultas de subárbol con Fenwick/segment tree.

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/G - Signal Coverage (Tarjan iterativo: DFS con pila
      explícita y low-link)
    - CSES «Building Roads», «Counting Rooms» (recorrido por componentes)
    - CSES «Subordinates» (tamaños de subárbol en un árbol)

VERIFICACIÓN
    - Pruebas: OK contra un DFS recursivo (fuerza bruta) en 2000 grafos
      aleatorios dirigidos y no dirigidos (mismos orden/entrada/salida/padre),
      propiedad de ancestros contra la cadena de padres, y un camino de
      200000 vértices sin desbordar la pila (python dfs.py)
"""
import random
import sys


def dfs(adj):
    """DFS iterativo sobre todo el grafo: (orden, entrada, salida, padre)."""
    n = len(adj)
    entrada = [-1] * n
    salida = [-1] * n
    padre = [-1] * n
    it = [0] * n               # it[v] = índice del próximo vecino de v a mirar
    orden = []
    reloj = 0
    for r in range(n):
        if entrada[r] != -1:
            continue
        entrada[r] = reloj
        reloj += 1
        orden.append(r)
        pila = [r]
        while pila:
            v = pila[-1]
            if it[v] < len(adj[v]):
                u = adj[v][it[v]]
                it[v] += 1
                if entrada[u] == -1:           # «llamada recursiva» a u
                    padre[u] = v
                    entrada[u] = reloj
                    reloj += 1
                    orden.append(u)
                    pila.append(u)
            else:                              # v terminó todos sus vecinos
                salida[v] = reloj
                reloj += 1
                pila.pop()
    return orden, entrada, salida, padre


def es_ancestro(entrada, salida, u, v):
    """¿u es ancestro de v en el bosque DFS? (u es ancestro de sí mismo)."""
    return entrada[u] <= entrada[v] and salida[v] <= salida[u]


def _adyacencia(n, aristas, dirigido):
    adj = [[] for _ in range(n)]
    for u, v in aristas:
        adj[u].append(v)
        if not dirigido:
            adj[v].append(u)
    return adj


def _dfs_recursivo(adj):
    """Fuerza bruta: la definición recursiva, tal cual (solo para n pequeño)."""
    n = len(adj)
    entrada, salida, padre, orden = [-1] * n, [-1] * n, [-1] * n, []
    reloj = [0]

    def visitar(v):
        entrada[v] = reloj[0]
        reloj[0] += 1
        orden.append(v)
        for u in adj[v]:
            if entrada[u] == -1:
                padre[u] = v
                visitar(u)
        salida[v] = reloj[0]
        reloj[0] += 1

    for r in range(n):
        if entrada[r] == -1:
            visitar(r)
    return orden, entrada, salida, padre


def demo():
    aristas = [(0, 1), (0, 2), (1, 3), (2, 3), (4, 2)]
    adj = _adyacencia(5, aristas, dirigido=True)
    orden, entrada, salida, padre = dfs(adj)
    print("aristas dirigidas:", aristas)
    print("preorden:", orden)              # [0, 1, 3, 2, 4]
    print("entrada:", entrada)             # [0, 1, 5, 2, 8]
    print("salida: ", salida)              # [7, 4, 6, 3, 9]
    print("padre:  ", padre)               # [-1, 0, 0, 1, -1]
    print("¿0 ancestro de 3?", es_ancestro(entrada, salida, 0, 3))   # True
    print("¿2 ancestro de 3?", es_ancestro(entrada, salida, 2, 3))   # False


def pruebas():
    random.seed(99)
    casos = 0

    # Casos borde
    assert dfs([]) == ([], [], [], [])
    assert dfs([[]]) == ([0], [0], [1], [-1])
    assert dfs([[0]]) == ([0], [0], [1], [-1])            # lazo

    # Camino de 200000 vértices: la versión recursiva reventaría
    n = 200000
    adj = _adyacencia(n, [(i, i + 1) for i in range(n - 1)], dirigido=True)
    orden, entrada, salida, padre = dfs(adj)
    assert orden == list(range(n)) and salida[0] == 2 * n - 1 and entrada[n - 1] == n - 1

    sys.setrecursionlimit(10000)
    for _ in range(2000):
        n = random.randint(1, 10)
        m = random.randint(0, 18)
        dirigido = random.random() < 0.5
        aristas = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
        adj = _adyacencia(n, aristas, dirigido)
        res = dfs(adj)
        assert res == _dfs_recursivo(adj)
        orden, entrada, salida, padre = res
        # Los tiempos son una permutación de 0..2n-1
        assert sorted(entrada + salida) == list(range(2 * n))
        # Ancestro por intervalos == ancestro por cadena de padres
        for u in range(n):
            for v in range(n):
                x, es = v, False
                while x != -1:
                    if x == u:
                        es = True
                        break
                    x = padre[x]
                assert es_ancestro(entrada, salida, u, v) == es
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
