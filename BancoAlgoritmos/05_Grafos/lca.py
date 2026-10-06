"""
Grafos — Ancestro común más bajo con binary lifting («Lowest Common Ancestor»)
Nivel: Avanzado
Ejecutar: python lca.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    En un árbol con raíz, el LCA de u y v es el ancestro común más
    profundo. Con él se responden en O(log N) consultas sobre el camino
    único u–v: distancia (suma de pesos), máximo/mínimo de una arista en
    el camino, k-ésimo ancestro, «¿está x en el camino de u a v?».
    Señales en el enunciado: árbol (N − 1 aristas, conexo) con MUCHAS
    consultas sobre pares de nodos (Q hasta 10^5): «distancia entre»,
    «arista más pesada/liviana en la ruta», «jefe común», «ancestro a k
    niveles».

FUNCIÓN
    t = LCA(n, aristas, raiz=0)
        aristas = lista de (u, v, peso) del árbol (peso opcional: (u, v)
        vale como peso 1). Vértices 0..n-1, el árbol debe ser conexo.
    t.lca(u, v)            -> int
    t.distancia(u, v)      -> suma de pesos del camino u–v
    t.max_camino(u, v)     -> mayor peso de arista en el camino (−inf si u == v)
    t.ancestro(v, k)       -> k-ésimo ancestro de v (−1 si no existe)
    t.prof[v], t.dist_raiz[v]   profundidad (aristas) y distancia ponderada a la raíz

IDEA Y ALGORITMO
    sube[j][v] = ancestro 2^j de v (o la raíz si se pasa). Se llena con
    sube[j][v] = sube[j−1][ sube[j−1][v] ]: saltar 2^j es saltar 2^(j−1)
    dos veces. Con eso se sube cualquier k descomponiendo k en binario.
    LCA(u, v):
      1) Igualar profundidades: subir el más profundo prof[u] − prof[v]
         niveles (un salto por cada bit encendido).
      2) Si ya son iguales, ese es el LCA.
      3) Para j de mayor a menor: si sube[j][u] != sube[j][v], subir ambos.
         Se mantiene la invariante «u y v son distintos y a la misma
         altura»: se salta solo cuando el destino todavía está por debajo
         del LCA. Al final u y v son hijos distintos del LCA → LCA = padre.
    Distancia: d(u, v) = dist_raiz[u] + dist_raiz[v] − 2·dist_raiz[lca].
    Máximo en el camino: mx[j][v] = mayor peso entre v y sube[j][v];
    se combina igual que los saltos: mx[j][v] = max(mx[j−1][v],
    mx[j−1][sube[j−1][v]]), y al subir u y v se va acumulando.
    Sirve para cualquier operación asociativa (min, suma, gcd…).
    El árbol se recorre con BFS (no DFS recursivo): con un camino de 10^5
    nodos la recursión revienta la pila de Python.
    Ingenuo: subir de a un padre, O(N) por consulta → O(N·Q).

MACROALGORITMO
    1. BFS desde la raíz: padre, prof, dist_raiz, peso de la arista al padre.
    2. sube[0] = padre (la raíz es su propio padre); mx[0] = peso al padre.
    3. Para j = 1..LOG−1: sube[j][v] = sube[j−1][sube[j−1][v]] y lo mismo con mx.
    4. Consulta: igualar alturas subiendo por bits de la diferencia.
    5. Si coinciden, listo; si no, saltar desde el j más grande mientras
       los ancestros 2^j sean distintos.
    6. Devolver el padre común (y combinar los máximos de los saltos).

COMPLEJIDAD
    Preproceso O(N log N) tiempo y memoria; cada consulta O(log N).
    En Python: N = 10^5 se preprocesa en ~1 s; 10^5 consultas en ~1 s.

EJEMPLO A MANO
    Árbol (raíz 0): 0–1 (3), 0–2 (1), 1–3 (4), 1–4 (2), 4–5 (7), 2–6 (5).
    prof: 0:0, 1:1, 2:1, 3:2, 4:2, 6:2, 5:3.
    lca(5, 3): prof 3 vs 2 → subir 5 un nivel: 4. Ahora 4 y 3 a altura 2;
    j=1: sube[1][4] = 0 = sube[1][3] → no saltar; j=0: sube[0][4] = 1 =
    sube[0][3] → no saltar. LCA = padre(4) = 1.
    distancia(5, 3) = dist_raiz 12 + 7 − 2·3 = 13 (= 7 + 2 + 4).
    max_camino(5, 6): camino 5–4–1–0–2–6, pesos 7, 2, 3, 1, 5 → 7.

ERRORES TÍPICOS
    - LOG demasiado pequeño: con N = 10^5 hace falta LOG ≥ 17.
    - Hacer la raíz su propio «padre −1»: sube[j][−1] indexa el último
      elemento en Python sin error. Aquí la raíz apunta a sí misma.
    - Igualar alturas mal (subir el menos profundo).
    - Saltar cuando sube[j][u] == sube[j][v] (se pasa por encima del LCA).
    - Para máximo en camino, olvidar el último tramo (las dos aristas de u
      y v a su padre común).

VARIANTES Y RELACIONADOS
    - LCA con Euler tour + sparse table: consultas O(1).
    - Consultas offline: Tarjan offline con union-find.
    - Varios árboles (bosque): una raíz por componente o raíz virtual.
    - Heavy-light decomposition: caminos con actualizaciones.
    - grafo_funcional.py (binary lifting para k-ésimo sucesor),
      diametro_arbol.py, bfs.py.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/A - Alice's Travels II (máximos en caminos del
      árbol con LCA por binary lifting + mochila)
    - CSES «Company Queries I» (k-ésimo ancestro), «Company Queries II»,
      «Distance Queries»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (subir de a un padre desde los dos
      nodos, guardando pesos) en 300 árboles aleatorios de hasta 40 nodos
      con todas las parejas de nodos y raíces aleatorias; casos borde y una
      cadena de 10^5 nodos (python lca.py)
"""
import random
from collections import deque


class LCA:
    def __init__(self, n, aristas, raiz=0):
        ady = [[] for _ in range(n)]
        for a in aristas:
            u, v = a[0], a[1]
            w = a[2] if len(a) > 2 else 1
            ady[u].append((v, w))
            ady[v].append((u, w))
        # 1) BFS desde la raíz (iterativo): padre, profundidad, distancias
        padre = [-1] * n
        peso_padre = [float("-inf")] * n
        prof = [0] * n
        dist_raiz = [0] * n
        padre[raiz] = raiz
        q = deque([raiz])
        while q:
            u = q.popleft()
            for v, w in ady[u]:
                if padre[v] == -1:
                    padre[v] = u
                    peso_padre[v] = w
                    prof[v] = prof[u] + 1
                    dist_raiz[v] = dist_raiz[u] + w
                    q.append(v)
        self.prof, self.dist_raiz = prof, dist_raiz
        # 2-3) tablas de saltos: sube[j][v] = ancestro 2^j; mx[j][v] = máximo en ese tramo
        self.LOG = max(1, (n - 1).bit_length())
        self.sube = [padre]
        self.mx = [peso_padre]
        for j in range(1, self.LOG):
            ant, mant = self.sube[-1], self.mx[-1]
            self.sube.append([ant[ant[v]] for v in range(n)])
            self.mx.append([max(mant[v], mant[ant[v]]) for v in range(n)])

    def ancestro(self, v, k):
        """k-ésimo ancestro de v; −1 si sube por encima de la raíz."""
        if k > self.prof[v]:
            return -1
        j = 0
        while k:
            if k & 1:
                v = self.sube[j][v]
            k >>= 1
            j += 1
        return v

    def _subir(self, u, v):
        """LCA y máximo de aristas en el camino u–v."""
        sube, mx = self.sube, self.mx
        mejor = float("-inf")
        if self.prof[u] < self.prof[v]:
            u, v = v, u
        # 1) igualar alturas
        d = self.prof[u] - self.prof[v]
        j = 0
        while d:
            if d & 1:
                mejor = max(mejor, mx[j][u])
                u = sube[j][u]
            d >>= 1
            j += 1
        if u == v:
            return u, mejor
        # 2) subir ambos mientras no coincidan (invariante: u != v, misma altura)
        for j in range(self.LOG - 1, -1, -1):
            if sube[j][u] != sube[j][v]:
                mejor = max(mejor, mx[j][u], mx[j][v])
                u = sube[j][u]
                v = sube[j][v]
        # 3) el último tramo: u y v son hijos distintos del LCA
        mejor = max(mejor, mx[0][u], mx[0][v])
        return sube[0][u], mejor

    def lca(self, u, v):
        return self._subir(u, v)[0]

    def distancia(self, u, v):
        w = self.lca(u, v)
        return self.dist_raiz[u] + self.dist_raiz[v] - 2 * self.dist_raiz[w]

    def max_camino(self, u, v):
        return self._subir(u, v)[1]


def demo():
    aristas = [(0, 1, 3), (0, 2, 1), (1, 3, 4), (1, 4, 2), (4, 5, 7), (2, 6, 5)]
    t = LCA(7, aristas)
    print("lca(5, 3) =", t.lca(5, 3))                  # 1
    print("distancia(5, 3) =", t.distancia(5, 3))      # 13
    print("max_camino(5, 6) =", t.max_camino(5, 6))    # 7
    print("ancestro(5, 2) =", t.ancestro(5, 2))        # 1


def _bruto(n, aristas, raiz):
    """Padre y peso al padre con un recorrido simple; consultas subiendo de a uno."""
    ady = [[] for _ in range(n)]
    for u, v, w in aristas:
        ady[u].append((v, w))
        ady[v].append((u, w))
    padre = {raiz: None}
    peso = {}
    pila = [raiz]
    while pila:
        u = pila.pop()
        for v, w in ady[u]:
            if v not in padre:
                padre[v] = u
                peso[v] = w
                pila.append(v)

    def camino_raiz(x):                 # lista de nodos de x hasta la raíz
        c = [x]
        while padre[c[-1]] is not None:
            c.append(padre[c[-1]])
        return c

    def consulta(u, v):
        cu, cv = camino_raiz(u), camino_raiz(v)
        sv = set(cv)
        w = next(x for x in cu if x in sv)          # primer ancestro común
        pesos = [peso[x] for x in cu[:cu.index(w)]] + [peso[x] for x in cv[:cv.index(w)]]
        return w, sum(pesos), max(pesos, default=float("-inf")), cu
    return consulta


def pruebas():
    random.seed(1736)

    # Casos borde
    t = LCA(1, [])
    assert t.lca(0, 0) == 0 and t.distancia(0, 0) == 0 and t.ancestro(0, 1) == -1
    t = LCA(2, [(0, 1)])                                # sin peso = 1
    assert t.lca(0, 1) == 0 and t.distancia(1, 0) == 1 and t.max_camino(0, 1) == 1

    # Aleatorios contra subir de a un padre
    for _ in range(300):
        n = random.randint(1, 40)
        aristas = [(random.randrange(v), v, random.randint(-5, 20)) for v in range(1, n)]
        etiqueta = list(range(n))
        random.shuffle(etiqueta)                        # renombrar para no tener padre < hijo
        aristas = [(etiqueta[u], etiqueta[v], w) for u, v, w in aristas]
        raiz = random.randrange(n)
        t = LCA(n, aristas, raiz)
        consulta = _bruto(n, aristas, raiz)
        for u in range(n):
            for v in range(n):
                w, d, mx, cu = consulta(u, v)
                assert t.lca(u, v) == w
                assert t.distancia(u, v) == d
                assert t.max_camino(u, v) == mx
            for k in range(n + 1):
                assert t.ancestro(u, k) == (cu[k] if k < len(cu) else -1)

    # Grande: cadena de 10^5 nodos (profundidad 10^5)
    N = 10 ** 5
    t = LCA(N, [(i, i + 1, i % 1000) for i in range(N - 1)])
    assert t.lca(N - 1, 50000) == 50000 and t.lca(0, N - 1) == 0
    assert t.distancia(10, 20) == sum(range(10, 20))
    assert t.max_camino(N - 1, 0) == 999 and t.max_camino(3, 7) == 6
    assert t.ancestro(N - 1, N - 1) == 0


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
