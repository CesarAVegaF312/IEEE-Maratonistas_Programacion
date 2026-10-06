"""
Grafos — Flujo máximo con Dinic («Dinic's algorithm»)
Nivel: Avanzado
Ejecutar: python dinic.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Lo mismo que Edmonds–Karp (flujo máximo de s a t con capacidades, y
    por el teorema max-flow min-cut, el corte mínimo), pero mucho más
    rápido: es el algoritmo de flujo que conviene tener en la libreta.
    Señales en el enunciado: capacidades, «cuántos pueden pasar como
    máximo», «mínimo costo para desconectar», caminos disjuntos,
    emparejamiento bipartito grande, asignaciones con cupos. Miles de
    vértices y decenas de miles de aristas.

FUNCIÓN
    d = Dinic(n)
    d.agregar(u, v, cap, cap_rev=0) -> id
        Arista u → v con capacidad cap (cap_rev = cap si es no dirigida).
    d.flujo_maximo(s, t) -> int
    d.flujo(id) -> int        flujo que pasa por la arista id
    d.lado_s() -> list[bool]  tras el flujo: vértices alcanzables desde s
                              en el residual (lado s de un corte mínimo)

IDEA Y ALGORITMO
    Grafo residual igual que en Edmonds–Karp (inversa de e = e ^ 1).
    Dinic trabaja por FASES:
      1) BFS desde s en el residual calcula nivel[v] = distancia a s.
      2) Solo se usan aristas que suben exactamente un nivel
         (nivel[v] = nivel[u] + 1): el «grafo de niveles», un DAG donde
         todos los caminos s → t son caminos MÁS CORTOS.
      3) Se empuja un FLUJO BLOQUEANTE: caminos de aumento en ese DAG hasta
         que todo camino s → t tenga una arista saturada. Con un puntero
         it[v] por vértice, una arista que ya no sirve (saturada o que lleva
         a un callejón sin salida) no se vuelve a mirar en la fase.
    Tras cada fase la distancia de s a t en el residual crece al menos en 1
    (los caminos más cortos quedaron todos bloqueados), así que hay a lo
    sumo V fases. Cada fase cuesta O(V·E): total O(V²·E). Con capacidades
    unitarias (emparejamiento bipartito) baja a O(E·√V).
    La búsqueda de caminos es ITERATIVA: se avanza desde s guardando en una
    pila las aristas del camino; en un callejón sin salida se retrocede y
    se avanza el puntero del vértice anterior; al llegar a t se empuja el
    cuello de botella y se vuelve a s con los punteros intactos.

MACROALGORITMO
    1. Crear cada arista con su inversa (cap 0, o cap_rev).
    2. BFS desde s: nivel[]. Si t no tiene nivel, terminar.
    3. it[v] = 0 para todo v.
    4. Desde s, avanzar por la arista it[v] si tiene cap > 0 y sube un
       nivel; si no, it[v] += 1. Si v se queda sin aristas, retroceder.
    5. Al llegar a t: cuello b, restar b a las aristas del camino y sumarlo
       a sus inversas; flujo += b; volver a s.
    6. Cuando s se queda sin aristas útiles termina la fase: volver a 2.

COMPLEJIDAD
    Tiempo O(V²·E) (O(E·√V) con capacidades unitarias), memoria O(V + E).
    En Python ~10^4 vértices y ~10^5 aristas en 1–2 s en redes típicas.

EJEMPLO A MANO
    s = 0, t = 3; aristas 0→1 (3), 0→2 (2), 1→2 (5), 1→3 (2), 2→3 (3).
    Fase 1: niveles 0:0, 1:1, 2:1, 3:2. Grafo de niveles: 0→1, 0→2, 1→3,
    2→3 (1→2 no sube de nivel). Caminos: 0→1→3 (2) y 0→2→3 (2) → flujo 4.
    Fase 2: residual 0→1 (1), 1→2 (5), 2→3 (1): niveles 0:0, 1:1, 2:2, 3:3.
    Camino 0→1→2→3 con cuello 1 → flujo 5.
    Fase 3: 0→1 y 0→2 están saturadas, t no se alcanza → flujo máximo 5.
    lado_s() = {0}: corte {0} | {1,2,3} de capacidad 3 + 2 = 5.

ERRORES TÍPICOS
    - No usar el puntero it[v] (volver a revisar aristas inútiles): el
      algoritmo sigue correcto pero degenera a algo mucho más lento.
    - Aceptar aristas con nivel[v] > nivel[u] en vez de == nivel[u] + 1.
    - DFS recursivo: con caminos largos (miles de vértices) revienta la
      pila de Python.
    - Olvidar que el objeto queda con el residual modificado: para otra
      consulta (otros s, t) hay que reconstruirlo.

VARIANTES Y RELACIONADOS
    - edmonds_karp.py (más simple, más lento).
    - corte_minimo.py (aristas del corte, corte de vértices partiendo nodos).
    - emparejamiento_bipartito.py (Hopcroft–Karp = Dinic especializado).
    - Súper fuente / súper sumidero, capacidades en vértices (v_in → v_out),
      cotas inferiores, flujo de costo mínimo.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/M - Byte Flu (corte mínimo de vértices con Dinic)
    - CSES «Download Speed», «Police Chase», «School Dance», «Distinct Routes»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (corte mínimo enumerando todos los
      conjuntos S con s ∈ S, t ∉ S) en 1500 redes aleatorias con n ≤ 8;
      capacidad y conservación del flujo por arista; el lado_s() da un corte
      de capacidad igual al flujo; casos borde y una red bipartita de 4000
      vértices con emparejamiento perfecto conocido (python dinic.py)
"""
import random
from collections import deque


class Dinic:
    def __init__(self, n):
        self.n = n
        self.ady = [[] for _ in range(n)]   # ids de aristas que salen de cada vértice
        self.dest = []
        self.cap = []                       # capacidad residual
        self.orig = []
        self.nivel = [-1] * n

    def agregar(self, u, v, cap, cap_rev=0):
        e = len(self.dest)
        self.ady[u].append(e)
        self.dest.append(v)
        self.cap.append(cap)
        self.orig.append(cap)
        self.ady[v].append(e + 1)           # inversa = e ^ 1
        self.dest.append(u)
        self.cap.append(cap_rev)
        self.orig.append(cap_rev)
        return e

    def _bfs(self, s, t):
        """Niveles desde s en el residual. ¿Se alcanza t?"""
        nivel = [-1] * self.n
        nivel[s] = 0
        q = deque([s])
        dest, cap, ady = self.dest, self.cap, self.ady
        while q:
            u = q.popleft()
            for e in ady[u]:
                if cap[e] > 0 and nivel[dest[e]] == -1:
                    nivel[dest[e]] = nivel[u] + 1
                    q.append(dest[e])
        self.nivel = nivel
        return nivel[t] != -1

    def flujo_maximo(self, s, t):
        if s == t:
            return 0
        dest, cap, ady = self.dest, self.cap, self.ady
        total = 0
        while self._bfs(s, t):
            nivel = self.nivel
            it = [0] * self.n               # siguiente arista por probar de cada vértice
            camino = []                     # aristas del camino actual desde s
            v = s
            while True:
                if v == t:
                    # empujar el cuello de botella y volver a s
                    b = min(cap[e] for e in camino)
                    for e in camino:
                        cap[e] -= b
                        cap[e ^ 1] += b
                    total += b
                    camino.clear()
                    v = s
                    continue
                lista = ady[v]
                avanzo = False
                while it[v] < len(lista):
                    e = lista[it[v]]
                    if cap[e] > 0 and nivel[dest[e]] == nivel[v] + 1:
                        camino.append(e)    # avanzar sin mover it[v]: e puede servir otra vez
                        v = dest[e]
                        avanzo = True
                        break
                    it[v] += 1              # arista inútil en esta fase
                if avanzo:
                    continue
                # callejón sin salida en v
                if v == s:
                    break                   # fin de la fase (flujo bloqueante)
                e = camino.pop()
                v = dest[e ^ 1]             # retroceder al vértice anterior
                it[v] += 1                  # y descartar la arista que llevaba aquí
        return total

    def flujo(self, e):
        return self.orig[e] - self.cap[e]

    def lado_s(self):
        """Tras flujo_maximo: alcanzables desde s en el residual (lado S del corte)."""
        return [x != -1 for x in self.nivel]


def demo():
    d = Dinic(4)
    for u, v, c in [(0, 1, 3), (0, 2, 2), (1, 2, 5), (1, 3, 2), (2, 3, 3)]:
        d.agregar(u, v, c)
    print("Flujo máximo 0 → 3:", d.flujo_maximo(0, 3))           # 5
    print("Flujo por arista:", [d.flujo(2 * k) for k in range(5)])
    print("Lado s del corte mínimo:", [v for v, x in enumerate(d.lado_s()) if x])


def _corte_minimo_bruto(n, aristas, s, t):
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
    random.seed(27182)

    # Casos borde
    assert Dinic(2).flujo_maximo(0, 1) == 0
    assert Dinic(1).flujo_maximo(0, 0) == 0
    d = Dinic(2)
    d.agregar(0, 1, 5)
    d.agregar(0, 1, 7)
    assert d.flujo_maximo(0, 1) == 12
    d = Dinic(3)
    d.agregar(0, 1, 10 ** 18)
    d.agregar(1, 2, 10 ** 18)
    assert d.flujo_maximo(0, 2) == 10 ** 18

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
        d = Dinic(n)
        ids = [d.agregar(u, v, c, cr) for u, v, c, cr in aristas]
        f = d.flujo_maximo(s, t)
        assert f == _corte_minimo_bruto(n, aristas, s, t)
        balance = [0] * n
        for (u, v, c, cr), e in zip(aristas, ids):
            x = d.flujo(e)
            assert -cr <= x <= c
            balance[u] -= x
            balance[v] += x
        assert balance[t] == f and balance[s] == -f
        assert all(balance[v] == 0 for v in range(n) if v not in (s, t))
        # el lado s del residual es un corte de capacidad = flujo
        S = d.lado_s()
        assert S[s] and not S[t]
        corte = sum((c if S[u] and not S[v] else 0) + (cr if S[v] and not S[u] else 0)
                    for u, v, c, cr in aristas)
        assert corte == f

    # Grande: bipartito 2000 + 2000 con una permutación escondida → flujo 2000
    N = 2000
    perm = list(range(N))
    random.shuffle(perm)
    d = Dinic(2 * N + 2)
    s, t = 2 * N, 2 * N + 1
    for i in range(N):
        d.agregar(s, i, 1)
        d.agregar(N + i, t, 1)
        vecinos = {perm[i]} | {random.randrange(N) for _ in range(5)}
        for j in vecinos:
            d.agregar(i, N + j, 1)
    assert d.flujo_maximo(s, t) == N


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
