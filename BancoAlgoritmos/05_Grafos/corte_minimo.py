"""
Grafos — Corte mínimo s-t a partir del flujo máximo («Min s-t cut»)
Nivel: Avanzado
Ejecutar: python corte_minimo.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar el conjunto de aristas (o de vértices) de costo total mínimo
    cuya eliminación deja a t inalcanzable desde s, y decir CUÁLES son.
    Su valor es igual al flujo máximo (teorema max-flow min-cut).
    Señales en el enunciado: «mínimo costo para desconectar / aislar /
    bloquear», «cuántas calles cerrar para que el ladrón no llegue»,
    «quitar dispositivos para frenar el contagio», «separar dos grupos
    pagando lo menos posible».

FUNCIÓN
    corte_minimo(n, aristas, s, t, dirigido=True) -> (valor, lado_s, ids)
        aristas[k] = (u, v, costo). Si dirigido es False, cada arista es
        no dirigida (costo en ambos sentidos).
        valor  = costo mínimo de un corte s-t (= flujo máximo).
        lado_s = lista de booleanos: lado de s en el corte.
        ids    = índices k de las aristas cortadas (van de lado_s al otro).
    corte_minimo_vertices(n, aristas, costo, s, t) -> (valor, vertices) | None
        Grafo no dirigido; quitar el vértice v cuesta costo[v] (s y t no se
        pueden quitar). None si s y t son vecinos (imposible separarlos).

IDEA Y ALGORITMO
    Tras un flujo máximo, sea S el conjunto de vértices alcanzables desde s
    en el grafo RESIDUAL (aristas con capacidad sobrante > 0).
    - t ∉ S (si no, habría camino de aumento y el flujo no sería máximo).
    - Toda arista original u → v con u ∈ S, v ∉ S está SATURADA (si le
      sobrara capacidad, v sería alcanzable), y toda arista v → u que entra
      a S lleva flujo 0 (si llevara, su inversa permitiría llegar a v).
    - Entonces el flujo neto que cruza de S a T es exactamente la suma de
      capacidades de las aristas S → T: ese corte vale lo mismo que el
      flujo. Como ningún corte puede valer menos que un flujo (todo el
      flujo tiene que cruzarlo), es un corte MÍNIMO.
    Las aristas del corte son las originales con u ∈ S y v ∉ S.
    Corte de VÉRTICES: se parte cada vértice v en v_ent → v_sal con
    capacidad costo[v]; cada arista u—v se vuelve u_sal → v_ent y
    v_sal → u_ent con capacidad «infinita» (nunca conviene cortarlas).
    Un corte finito solo puede cortar aristas internas v_ent → v_sal, es
    decir, vértices. Si el flujo da «infinito», s y t son vecinos.
    Ingenuo: probar todos los subconjuntos S (2^(n−2)).

MACROALGORITMO
    1. Construir la red (inversas con e ^ 1) y correr Dinic de s a t.
    2. BFS desde s solo por aristas con capacidad residual > 0 → S.
    3. Cortadas = aristas originales k con u ∈ S, v ∉ S (en no dirigido,
       también v ∈ S, u ∉ S).
    4. Para vértices: partir cada v en (v, v + n), arista interna con su
       costo (infinito para s y t) y aristas «infinitas» entre partes.
    5. Correr el flujo de s_ent a t_sal; si ≥ INF → None.
    6. Vértices cortados = los v con v_ent ∈ S y v_sal ∉ S.

COMPLEJIDAD
    La del flujo máximo: O(V²·E) con Dinic, + O(V + E) para el BFS final.
    Corte de vértices: el grafo se duplica (2V vértices, 2E + V aristas).

EJEMPLO A MANO
    s = 0, t = 3; aristas 0:(0→1, 3) 1:(0→2, 2) 2:(1→2, 5) 3:(1→3, 2)
    4:(2→3, 3). Flujo máximo = 5. En el residual las dos aristas que salen
    de 0 quedaron saturadas → S = {0}. Corte: aristas 0 y 1 (3 + 2 = 5).
    (El corte {0,1,2} | {3}, aristas 3 y 4, también vale 5: puede haber
    varios cortes mínimos; este método da el de S más pequeño.)

ERRORES TÍPICOS
    - Buscar S recorriendo el grafo ORIGINAL en vez del residual.
    - Tomar como corte «las aristas saturadas»: puede haber aristas
      saturadas que no cruzan el corte (y sobran).
    - Corte de vértices sin partir nodos: el flujo cortaría aristas.
    - Olvidar que s y t no se pueden partir con costo finito (capacidad
      infinita en su arista interna).
    - Usar un INF menor que la suma de todos los costos reales.

VARIANTES Y RELACIONADOS
    - Varias fuentes / sumideros: súper fuente y súper sumidero con
      aristas infinitas (Colombia 2026 M fusiona los infectados en s).
    - Mínimo número de aristas a quitar: todos los costos = 1.
    - Corte global mínimo (sin s, t fijos): Stoer–Wagner.
    - Proyectos y requisitos («project selection»): corte mínimo con
      ganancias en s y costos en t.
    - dinic.py, edmonds_karp.py, emparejamiento_bipartito.py (König).

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/M - Byte Flu (corte mínimo de VÉRTICES con nodos
      partidos y Dinic)
    - CSES «Police Chase» (aristas del corte mínimo)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta en 1000 grafos aleatorios por tipo
      (n ≤ 8): corte de aristas contra los 2^(n−2) conjuntos S (dirigido y
      no dirigido), y corte de vértices contra todos los subconjuntos de
      vértices quitables; se valida que lo devuelto desconecte s de t y que
      su costo sea el valor (python corte_minimo.py)
"""
import random
from collections import deque


class Dinic:
    """Dinic iterativo (ver dinic.py)."""

    def __init__(self, n):
        self.n = n
        self.ady = [[] for _ in range(n)]
        self.dest = []
        self.cap = []
        self.nivel = [-1] * n

    def agregar(self, u, v, cap, cap_rev=0):
        e = len(self.dest)
        self.ady[u].append(e)
        self.dest.append(v)
        self.cap.append(cap)
        self.ady[v].append(e + 1)
        self.dest.append(u)
        self.cap.append(cap_rev)
        return e

    def _bfs(self, s, t):
        nivel = [-1] * self.n
        nivel[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for e in self.ady[u]:
                if self.cap[e] > 0 and nivel[self.dest[e]] == -1:
                    nivel[self.dest[e]] = nivel[u] + 1
                    q.append(self.dest[e])
        self.nivel = nivel
        return nivel[t] != -1

    def flujo_maximo(self, s, t):
        dest, cap, ady = self.dest, self.cap, self.ady
        total = 0
        while self._bfs(s, t):
            nivel = self.nivel
            it = [0] * self.n
            camino = []
            v = s
            while True:
                if v == t:
                    b = min(cap[e] for e in camino)
                    for e in camino:
                        cap[e] -= b
                        cap[e ^ 1] += b
                    total += b
                    camino.clear()
                    v = s
                    continue
                lista = ady[v]
                while it[v] < len(lista):
                    e = lista[it[v]]
                    if cap[e] > 0 and nivel[dest[e]] == nivel[v] + 1:
                        break
                    it[v] += 1
                if it[v] < len(lista):
                    e = lista[it[v]]
                    camino.append(e)
                    v = dest[e]
                    continue
                if v == s:
                    break
                e = camino.pop()
                v = dest[e ^ 1]
                it[v] += 1
        # self.nivel quedó con el último BFS (el que no llegó a t):
        # nivel != -1  ⇔  alcanzable desde s en el residual
        return total


def corte_minimo(n, aristas, s, t, dirigido=True):
    """(valor, lado_s, ids de aristas cortadas) del corte mínimo s-t."""
    d = Dinic(n)
    for u, v, c in aristas:
        d.agregar(u, v, c, 0 if dirigido else c)
    valor = d.flujo_maximo(s, t) if s != t else 0
    d._bfs(s, t)                       # alcanzables desde s en el residual final
    lado_s = [x != -1 for x in d.nivel]
    ids = [k for k, (u, v, c) in enumerate(aristas)
           if (lado_s[u] and not lado_s[v]) or (not dirigido and lado_s[v] and not lado_s[u])]
    return valor, lado_s, ids


def corte_minimo_vertices(n, aristas, costo, s, t):
    """Mínimo costo de vértices (≠ s, t) a quitar para separar s de t (no dirigido)."""
    INF = sum(costo) + 1               # "infinito": más que quitar todos los vértices
    # v_ent = v, v_sal = v + n
    d = Dinic(2 * n)
    for v in range(n):
        d.agregar(v, v + n, INF if v in (s, t) else costo[v])
    for u, v in aristas:
        d.agregar(u + n, v, INF)       # u_sal → v_ent
        d.agregar(v + n, u, INF)       # v_sal → u_ent
    valor = d.flujo_maximo(s, t + n)
    if valor >= INF:
        return None                    # s y t son vecinos (o s == t)
    d._bfs(s, t + n)
    S = d.nivel
    vertices = [v for v in range(n) if S[v] != -1 and S[v + n] == -1]
    return valor, vertices


def demo():
    aristas = [(0, 1, 3), (0, 2, 2), (1, 2, 5), (1, 3, 2), (2, 3, 3)]
    valor, lado, ids = corte_minimo(4, aristas, 0, 3)
    print("Corte mínimo:", valor, "lado s:", [v for v in range(4) if lado[v]],
          "aristas cortadas:", [aristas[k] for k in ids])
    # Corte de vértices: s=0 y t=5 conectados por dos rutas (1-3 y 2-4)
    ar = [(0, 1), (1, 3), (3, 5), (0, 2), (2, 4), (4, 5), (1, 4)]
    costo = [0, 4, 1, 2, 7, 0]
    print("Corte de vértices:", corte_minimo_vertices(6, ar, costo, 0, 5))  # (5, [1, 2])


# ---------- pruebas ----------

def _alcanza(n, ady, s, t, quitado):
    vis = [False] * n
    vis[s] = True
    q = [s]
    while q:
        u = q.pop()
        for w in ady[u]:
            if not vis[w] and not quitado[w]:
                vis[w] = True
                q.append(w)
    return vis[t]


def _bruto_aristas(n, aristas, s, t, dirigido):
    mejor = None
    for mask in range(1 << n):
        if not (mask >> s) & 1 or (mask >> t) & 1:
            continue
        c = 0
        for u, v, cap in aristas:
            a, b = (mask >> u) & 1, (mask >> v) & 1
            if (a and not b) or (not dirigido and b and not a):
                c += cap
        mejor = c if mejor is None else min(mejor, c)
    return mejor


def _bruto_vertices(n, aristas, costo, s, t):
    ady = [[] for _ in range(n)]
    for u, v in aristas:
        ady[u].append(v)
        ady[v].append(u)
    mejor = None
    for mask in range(1 << n):
        if (mask >> s) & 1 or (mask >> t) & 1:
            continue
        quitado = [(mask >> v) & 1 == 1 for v in range(n)]
        if not _alcanza(n, ady, s, t, quitado):
            c = sum(costo[v] for v in range(n) if quitado[v])
            mejor = c if mejor is None else min(mejor, c)
    return mejor


def pruebas():
    random.seed(1618)

    # Casos borde
    assert corte_minimo(2, [], 0, 1) == (0, [True, False], [])
    assert corte_minimo(2, [(0, 1, 4), (0, 1, 6)], 0, 1)[2] == [0, 1]
    assert corte_minimo_vertices(2, [(0, 1)], [1, 1], 0, 1) is None     # vecinos
    assert corte_minimo_vertices(3, [], [5, 5, 5], 0, 2) == (0, [])
    assert corte_minimo_vertices(3, [(0, 1), (1, 2)], [5, 9, 5], 0, 2) == (9, [1])

    # Corte de aristas, dirigido y no dirigido
    for caso in range(1000):
        dirigido = caso % 2 == 0
        n = random.randint(2, 8)
        aristas = [(random.randrange(n), random.randrange(n), random.randint(0, 9))
                   for _ in range(random.randint(0, 3 * n))]
        s, t = random.sample(range(n), 2)
        valor, lado, ids = corte_minimo(n, aristas, s, t, dirigido)
        assert valor == _bruto_aristas(n, aristas, s, t, dirigido)
        assert lado[s] and not lado[t]
        assert sum(aristas[k][2] for k in ids) == valor
        # quitar las aristas cortadas desconecta s de t
        ady = [[] for _ in range(n)]
        for k, (u, v, c) in enumerate(aristas):
            if k not in ids:
                ady[u].append(v)
                if not dirigido:
                    ady[v].append(u)
        assert not _alcanza(n, ady, s, t, [False] * n)

    # Corte de vértices
    for _ in range(1000):
        n = random.randint(2, 8)
        aristas = [tuple(random.sample(range(n), 2)) for _ in range(random.randint(0, 2 * n))]
        costo = [random.randint(0, 9) for _ in range(n)]
        s, t = random.sample(range(n), 2)
        r = corte_minimo_vertices(n, aristas, costo, s, t)
        vecinos = any({u, v} == {s, t} for u, v in aristas)
        if vecinos:
            assert r is None
            continue
        valor, vs = r
        assert valor == _bruto_vertices(n, aristas, costo, s, t)
        assert s not in vs and t not in vs and sum(costo[v] for v in vs) == valor
        ady = [[] for _ in range(n)]
        for u, v in aristas:
            ady[u].append(v)
            ady[v].append(u)
        assert not _alcanza(n, ady, s, t, [v in vs for v in range(n)])


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
