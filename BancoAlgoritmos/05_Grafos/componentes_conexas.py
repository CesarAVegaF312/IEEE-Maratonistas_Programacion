"""
Grafos — Componentes conexas («Connected components»)
Nivel: Básico
Ejecutar: python componentes_conexas.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Partir un grafo NO dirigido en sus «pedazos»: dos vértices están en la
    misma componente si hay un camino entre ellos. Responde «¿cuántos grupos
    hay?», «¿u y v están conectados?», «¿cuántas aristas faltan para
    conectar todo?» (= componentes − 1), «tamaño del grupo más grande».
    Señales en el enunciado: «grupos de amigos», «redes», «islas», «activar
    uno activa a todos los cercanos», «mínimo de X para alcanzar a todos».
    Si el grafo es DIRIGIDO y se pide «se alcanzan mutuamente», eso son
    componentes FUERTEMENTE conexas (scc.py), no estas.

FUNCIÓN
    componentes(adj) -> (comp, k)
        comp[v] = número de componente de v (0..k-1, numeradas en el orden en
        que aparece su vértice más pequeño); k = cantidad de componentes.
    componentes_dsu(n, aristas) -> (comp, k)
        Lo mismo con union-find, cuando solo se tiene la lista de aristas.
    tamanos(comp, k) -> list    tamaño de cada componente.

IDEA Y ALGORITMO
    «Estar conectado» es una relación de equivalencia (reflexiva, simétrica
    en no dirigido, transitiva pegando caminos) y sus clases son las
    componentes. Un BFS desde s visita EXACTAMENTE la componente de s: todo
    lo que visita es alcanzable, y si v es alcanzable por un camino
    s = x0, x1, …, v, por inducción cada xi es descubierto.
    Entonces: recorrer los vértices en orden; cada vértice aún sin
    componente inicia una nueva (no es alcanzable desde ninguna anterior,
    porque si lo fuera ya estaría marcado), y un BFS desde él marca toda su
    componente. Cada vértice y arista se procesa una vez.
    Con union-find (union_find.py) se procesan las aristas una por una
    uniendo extremos; útil si las aristas llegan de a poco (en línea) o si
    el grafo se forma por «cubetas»/relaciones sin construir adyacencia.

MACROALGORITMO
    1. comp = [-1]*n; k = 0.
    2. Para s = 0..n-1 con comp[s] == -1:
    3.   comp[s] = k; BFS desde s marcando comp[v] = k al descubrir v.
    4.   k += 1.
    5. Respuesta: k componentes; u, v conectados ⇔ comp[u] == comp[v].

COMPLEJIDAD
    O(n + m) tiempo, O(n) memoria extra. (DSU: O(m·α(n)) ≈ O(m).)
    En Python ~10^6 aristas por segundo.

EJEMPLO A MANO
    n = 7, aristas 0-1, 1-2, 3-4, 6-6 (lazo).
      s=0: BFS marca 0, 1, 2 → componente 0
      s=3: marca 3, 4         → componente 1
      s=5: solo 5             → componente 2
      s=6: solo 6             → componente 3
    comp = [0, 0, 0, 1, 1, 2, 3], k = 4, tamaños [3, 2, 1, 1].
    Para conectar todo hacen falta k − 1 = 3 aristas.

ERRORES TÍPICOS
    - Olvidar los vértices aislados (sin aristas): también son componentes.
    - Usar DFS recursivo: con un camino de 10^5 vértices revienta.
    - Aplicarlo a un grafo dirigido guardando solo u→v: un BFS desde s no ve
      lo que llega a s; para «débilmente conexo» agregar ambas direcciones.
    - Relación no simétrica en el enunciado («i activa a j si j está en el
      radio de i»): decidir si el grafo es dirigido ANTES de programar.

VARIANTES Y RELACIONADOS
    - Grillas: flood_fill.py. Uniones en línea / Kruskal: union_find.py, mst.py.
    - Dirigido: scc.py. Bipartición por componente: bipartito.py.
    - Contar aristas por componente: m_c = n_c − 1 ⇔ la componente es árbol
      (sin ciclos); m_c ≥ n_c ⇔ tiene ciclo (deteccion_ciclos.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/J - Lumina (respuesta = número de componentes)
    - ICPC/Colombia 2025/C - Celestial Veins (BFS por componente y
      clasificar cada una por vértices, aristas y grados)
    - ICPC/Colombia 2018/C - Carrol's Scrabble (componentes con union-find
      sobre cubetas)
    - CSES «Building Roads» (componentes − 1)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (clausura transitiva con Floyd–Warshall
      booleano) en 1500 grafos aleatorios; BFS y DSU dan la misma partición;
      un camino de 200000 vértices (python componentes_conexas.py)
"""
import random
from collections import deque


def componentes(adj):
    """comp[v] = componente de v (0..k-1) y k, con un BFS por componente."""
    n = len(adj)
    comp = [-1] * n
    k = 0
    for s in range(n):
        if comp[s] != -1:
            continue
        comp[s] = k               # s no es alcanzable desde componentes previas
        cola = deque([s])
        while cola:
            u = cola.popleft()
            for v in adj[u]:
                if comp[v] == -1:
                    comp[v] = k
                    cola.append(v)
        k += 1
    return comp, k


def componentes_dsu(n, aristas):
    """Mismo resultado que componentes() pero con union-find sobre las aristas."""
    padre = list(range(n))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]     # compresión por mitades
            x = padre[x]
        return x

    for u, v in aristas:
        ru, rv = raiz(u), raiz(v)
        if ru != rv:
            padre[ru] = rv
    # Renumerar raíces 0..k-1 en orden del vértice más pequeño de cada una
    numero = {}
    comp = []
    for v in range(n):
        r = raiz(v)
        if r not in numero:
            numero[r] = len(numero)
        comp.append(numero[r])
    return comp, len(numero)


def tamanos(comp, k):
    t = [0] * k
    for c in comp:
        t[c] += 1
    return t


def _adyacencia(n, aristas):
    adj = [[] for _ in range(n)]
    for u, v in aristas:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def demo():
    n, aristas = 7, [(0, 1), (1, 2), (3, 4), (6, 6)]
    comp, k = componentes(_adyacencia(n, aristas))
    print("aristas:", aristas)
    print("comp =", comp, " k =", k)                   # [0,0,0,1,1,2,3] 4
    print("tamaños:", tamanos(comp, k))                # [3, 2, 1, 1]
    print("aristas para conectar todo:", k - 1)        # 3
    print("¿0 y 2 conectados?", comp[0] == comp[2])    # True
    print("con DSU:", componentes_dsu(n, aristas))


def pruebas():
    random.seed(2017)
    casos = 0

    # Casos borde
    assert componentes([]) == ([], 0)
    assert componentes([[]]) == ([0], 1)
    assert componentes_dsu(3, []) == ([0, 1, 2], 3)

    # Camino largo (sin recursión)
    n = 200000
    ar = [(i, i + 1) for i in range(n - 1)]
    assert componentes(_adyacencia(n, ar))[1] == 1
    assert componentes_dsu(n, ar)[1] == 1

    for _ in range(1500):
        n = random.randint(1, 10)
        m = random.randint(0, 12)
        aristas = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
        comp, k = componentes(_adyacencia(n, aristas))
        # Fuerza bruta: clausura transitiva (Floyd–Warshall booleano)
        R = [[i == j for j in range(n)] for i in range(n)]
        for u, v in aristas:
            R[u][v] = R[v][u] = True
        for x in range(n):
            for i in range(n):
                for j in range(n):
                    if R[i][x] and R[x][j]:
                        R[i][j] = True
        for u in range(n):
            for v in range(n):
                assert (comp[u] == comp[v]) == R[u][v]
        # k = número de clases distintas; numeración por primer vértice
        clases = {frozenset(j for j in range(n) if R[i][j]) for i in range(n)}
        assert k == len(clases)
        vistos = []
        for c in comp:
            if c not in vistos:
                vistos.append(c)
        assert vistos == list(range(k))
        # DSU produce exactamente la misma numeración
        assert componentes_dsu(n, aristas) == (comp, k)
        assert sum(tamanos(comp, k)) == n
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
