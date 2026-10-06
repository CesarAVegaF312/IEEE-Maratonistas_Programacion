"""
Grafos — Flujo máximo con Edmonds–Karp («Max flow, Edmonds–Karp»)
Nivel: Avanzado
Ejecutar: python edmonds_karp.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular cuánto «material» (agua, datos, personas) puede pasar como
    máximo de una fuente s a un sumidero t en una red donde cada arista
    tiene una capacidad. Por el teorema flujo máximo = corte mínimo,
    también resuelve «el costo mínimo de cortar aristas para separar s de
    t», emparejamientos, caminos disjuntos, asignaciones con cupos…
    Señales en el enunciado: capacidades, «cuántos como máximo pueden
    llegar», «mínimo de aristas/vértices a eliminar para desconectar»,
    «cuántos caminos disjuntos», asignar personas a tareas con límites.
    N chico-mediano (cientos de vértices, miles de aristas).

FUNCIÓN
    ek = EdmondsKarp(n)
    ek.agregar(u, v, cap, cap_rev=0) -> id
        Arista u → v con capacidad cap. Para una arista NO dirigida usar
        cap_rev = cap. Devuelve el id para consultar su flujo después.
    ek.flujo_maximo(s, t) -> int
    ek.flujo(id) -> int     flujo que pasa por la arista id (u → v)

IDEA Y ALGORITMO
    Grafo RESIDUAL: por cada arista u → v con capacidad c y flujo f quedan
    c − f unidades para empujar hacia adelante y f para «devolver» (la
    arista inversa v → u). Un camino de aumento es un camino s → t con
    capacidad residual positiva en todas sus aristas; empujar por él el
    mínimo residual (el cuello de botella) aumenta el flujo.
    Ford–Fulkerson: repetir mientras haya camino de aumento. Al terminar,
    los vértices alcanzables desde s en el residual forman un lado S de un
    corte cuyas aristas están todas saturadas, así que flujo = capacidad
    de ese corte ≥ corte mínimo ≥ flujo: es máximo (teorema max-flow
    min-cut).
    Edmonds–Karp elige SIEMPRE el camino de aumento más CORTO (BFS). Con
    eso la distancia de s a cada vértice en el residual nunca baja, y cada
    arista es cuello de botella a lo sumo O(V) veces: O(V·E) aumentos de
    O(E) cada uno. Con DFS arbitrario el número de aumentos puede depender
    de las capacidades (y con reales ni siquiera terminar).
    Truco de implementación: las aristas se guardan en arreglos y la
    inversa de la arista e es e ^ 1 (se crean de a pares).

MACROALGORITMO
    1. Por cada arista u → v (cap c) crear e = (u→v, c) y e^1 = (v→u, 0).
    2. BFS desde s en el residual (solo aristas con cap > 0) guardando
       con qué arista se llegó a cada vértice.
    3. Si t no se alcanzó: terminar.
    4. Recorrer el camino desde t hacia atrás y hallar el cuello de botella b.
    5. A cada arista e del camino: cap[e] −= b, cap[e^1] += b. Flujo += b.
    6. Volver a 2.

COMPLEJIDAD
    Tiempo O(V·E²) en el peor caso (mucho menos en la práctica),
    memoria O(V + E). En Python: V ~ 500, E ~ 5000 sin problema; para
    redes más grandes o emparejamientos usar dinic.py.

EJEMPLO A MANO
    s = 0, t = 3; aristas 0→1 (3), 0→2 (2), 1→2 (5), 1→3 (2), 2→3 (3).
    BFS 1: 0→1→3, cuello min(3, 2) = 2 → flujo 2.
    BFS 2: 0→2→3, cuello min(2, 3) = 2 → flujo 4.
    BFS 3: 0→1→2→3, cuello min(1, 5, 1) = 1 → flujo 5.
    BFS 4: 0→1 y 0→2 quedaron saturadas, desde 0 no se llega a nadie → fin.
    Flujo máximo = 5 = capacidad del corte {0} | {1,2,3}: 3 + 2
    (el corte {0,1,2} | {3}: 2 + 3 también es mínimo).

ERRORES TÍPICOS
    - No crear la arista inversa (o crearla con la capacidad de la
      original): sin ella no se puede «deshacer» flujo y la respuesta sale
      menor.
    - Aristas no dirigidas: basta UN par con cap y cap_rev = cap, no dos
      pares.
    - Usar lista de adyacencia de vecinos en vez de ids de aristas: con
      aristas paralelas se mezclan las capacidades.
    - Olvidar capacidad «infinita» suficientemente grande (o usar float
      inf con enteros grandes mezclados).
    - Reutilizar el objeto para otra consulta sin reconstruir: las
      capacidades quedaron modificadas.

VARIANTES Y RELACIONADOS
    - dinic.py (más rápido: O(V²E), O(E√V) en bipartitos).
    - corte_minimo.py (las aristas del corte a partir del residual).
    - emparejamiento_bipartito.py (caso especial con capacidades 1).
    - Varias fuentes / sumideros: súper fuente y súper sumidero.
    - Capacidad en vértices: partir v en v_in → v_out.
    - Flujo de costo mínimo: cambiar BFS por Bellman-Ford/SPFA.

DÓNDE PRACTICAR
    - Ningún problema del repo lo usa directamente; ICPC/Colombia 2026/M -
      Byte Flu necesita flujo máximo (se resolvió con Dinic, ver dinic.py).
    - CSES «Download Speed», «Police Chase», «Distinct Routes»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (corte mínimo enumerando todos los
      conjuntos S con s ∈ S, t ∉ S) en 1500 redes aleatorias dirigidas y no
      dirigidas con n ≤ 8; además se comprueban capacidad y conservación
      del flujo por arista; casos borde (python edmonds_karp.py)
"""
import random
from collections import deque


class EdmondsKarp:
    def __init__(self, n):
        self.n = n
        self.ady = [[] for _ in range(n)]   # ady[u] = ids de aristas que salen de u
        self.dest = []                      # dest[e] = vértice al que llega e
        self.cap = []                       # capacidad RESIDUAL de e
        self.orig = []                      # capacidad original (para flujo(e))

    def agregar(self, u, v, cap, cap_rev=0):
        """Arista u → v (y su inversa v → u con cap_rev). Devuelve su id."""
        e = len(self.dest)
        self.ady[u].append(e)
        self.dest.append(v)
        self.cap.append(cap)
        self.orig.append(cap)
        self.ady[v].append(e + 1)           # la inversa de e es e ^ 1
        self.dest.append(u)
        self.cap.append(cap_rev)
        self.orig.append(cap_rev)
        return e

    def flujo_maximo(self, s, t):
        if s == t:
            return 0
        dest, cap, ady = self.dest, self.cap, self.ady
        total = 0
        while True:
            # BFS: llego[v] = arista con la que se llegó a v (-1 = no visitado)
            llego = [-1] * self.n
            llego[s] = -2
            q = deque([s])
            while q and llego[t] == -1:
                u = q.popleft()
                for e in ady[u]:
                    v = dest[e]
                    if cap[e] > 0 and llego[v] == -1:
                        llego[v] = e
                        q.append(v)
            if llego[t] == -1:
                return total                # no hay camino de aumento
            # cuello de botella recorriendo el camino hacia atrás
            b = None
            v = t
            while v != s:
                e = llego[v]
                if b is None or cap[e] < b:
                    b = cap[e]
                v = dest[e ^ 1]
            # empujar b unidades
            v = t
            while v != s:
                e = llego[v]
                cap[e] -= b
                cap[e ^ 1] += b
                v = dest[e ^ 1]
            total += b

    def flujo(self, e):
        """Flujo neto que pasa por la arista e (negativo si va al revés)."""
        return self.orig[e] - self.cap[e]


def demo():
    ek = EdmondsKarp(4)
    for u, v, c in [(0, 1, 3), (0, 2, 2), (1, 2, 5), (1, 3, 2), (2, 3, 3)]:
        ek.agregar(u, v, c)
    print("Flujo máximo 0 → 3:", ek.flujo_maximo(0, 3))          # 5
    print("Flujo por arista:", [ek.flujo(2 * k) for k in range(5)])  # [3, 2, 1, 2, 3]


def _corte_minimo_bruto(n, aristas, s, t):
    """Mínimo sobre todo S (s ∈ S, t ∉ S) de la capacidad que sale de S."""
    mejor = None
    for mask in range(1 << n):
        if not (mask >> s) & 1 or (mask >> t) & 1:
            continue
        c = 0
        for u, v, cap, cap_rev in aristas:
            if (mask >> u) & 1 and not (mask >> v) & 1:
                c += cap
            if (mask >> v) & 1 and not (mask >> u) & 1:
                c += cap_rev
        if mejor is None or c < mejor:
            mejor = c
    return mejor


def pruebas():
    random.seed(31415)

    # Casos borde
    ek = EdmondsKarp(2)
    assert ek.flujo_maximo(0, 1) == 0                       # sin aristas
    ek = EdmondsKarp(1)
    assert ek.flujo_maximo(0, 0) == 0
    ek = EdmondsKarp(2)
    ek.agregar(0, 1, 5)
    ek.agregar(0, 1, 7)                                     # aristas paralelas
    assert ek.flujo_maximo(0, 1) == 12
    ek = EdmondsKarp(2)
    ek.agregar(1, 0, 9)                                     # va al revés
    assert ek.flujo_maximo(0, 1) == 0
    ek = EdmondsKarp(3)
    ek.agregar(0, 1, 10 ** 18)
    ek.agregar(1, 2, 10 ** 18)
    assert ek.flujo_maximo(0, 2) == 10 ** 18                # capacidades enormes

    # Aleatorios contra corte mínimo por fuerza bruta
    for caso in range(1500):
        n = random.randint(2, 8)
        m = random.randint(0, 3 * n)
        no_dirigido = caso % 3 == 0
        aristas = []
        for _ in range(m):
            u, v = random.randrange(n), random.randrange(n)
            c = random.randint(0, 10)
            aristas.append((u, v, c, c if no_dirigido else 0))
        s, t = random.sample(range(n), 2)
        ek = EdmondsKarp(n)
        ids = [ek.agregar(u, v, c, cr) for u, v, c, cr in aristas]
        f = ek.flujo_maximo(s, t)
        assert f == _corte_minimo_bruto(n, aristas, s, t)
        # capacidades y conservación del flujo
        balance = [0] * n
        for (u, v, c, cr), e in zip(aristas, ids):
            x = ek.flujo(e)
            assert -cr <= x <= c
            balance[u] -= x
            balance[v] += x
        assert balance[t] == f and balance[s] == -f
        assert all(balance[v] == 0 for v in range(n) if v not in (s, t))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
