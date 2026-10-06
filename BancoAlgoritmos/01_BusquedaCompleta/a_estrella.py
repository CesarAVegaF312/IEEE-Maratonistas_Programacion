"""
Búsqueda completa — A* e IDA* sobre espacios de estados («A* search, IDA*»)
Nivel: Avanzado
Ejecutar: python a_estrella.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar el camino MÁS CORTO desde un estado inicial a un estado meta
    en un grafo de estados enorme (rompecabezas, configuraciones), usando
    una HEURÍSTICA h(estado) que estima lo que falta. Explora primero lo que
    parece más prometedor y deja sin visitar gran parte del espacio que un
    BFS/Dijkstra recorrería.
    Señales en el enunciado: «mínimo número de movimientos para ordenar /
    resolver», tableros deslizantes (8-puzzle, 15-puzzle), pilas o silos
    que se reacomodan, el espacio de estados es demasiado grande para BFS
    pero hay una cota inferior natural de los movimientos que faltan.

FUNCIÓN
    a_estrella(inicio, es_meta, vecinos, h) -> (costo, camino) | (None, None)
        vecinos(e) produce pares (siguiente, costo ≥ 0). h ADMISIBLE (nunca
        sobreestima) y CONSISTENTE (h(e) ≤ costo(e, e') + h(e')).
        camino = lista de estados de inicio a la meta.
    ida_estrella(inicio, es_meta, vecinos, h) -> costo | None
        Misma respuesta con memoria O(profundidad) (sin diccionarios).
    resolver_8puzzle(estado, con_ida=False) -> (movimientos, texto)
        estado: tupla de 9 con 0 = hueco, meta (1,2,3,4,5,6,7,8,0).
        Devuelve (−1, "") si no tiene solución. texto: letras U/D/L/R que
        indican hacia dónde se mueve el HUECO (vacío si se usa IDA*).

IDEA Y ALGORITMO
    A* es Dijkstra ordenando por f(e) = g(e) + h(e): g = costo real desde
    el inicio, h = estimación de lo que falta. Con h ≡ 0 es Dijkstra.
    Por qué da el óptimo: si h es consistente, f no decrece a lo largo de
    un camino, así que los estados salen del heap en orden de f y, cuando
    sale la meta, ningún camino pendiente puede ser más barato (su f ya es
    ≥ y h(meta) = 0). Cuanto más cerca h del valor real, menos se expande.
    Heurística del 8-puzzle: DISTANCIA MANHATTAN = Σ por ficha (no el hueco)
    de |fila − fila_meta| + |col − col_meta|. Es admisible: cada movimiento
    desliza UNA ficha UNA casilla, así que baja la suma en a lo sumo 1. Y
    consistente por el mismo motivo.
    IDA*: búsqueda en profundidad con límite en f; si no encuentra la meta,
    el nuevo límite es el menor f que se pasó. Repite poco trabajo (el
    árbol crece exponencialmente, el último nivel domina) y no guarda
    visitados: ideal cuando el espacio no cabe en memoria (15-puzzle).
    Resolubilidad (tablero de ancho impar): un movimiento horizontal no
    cambia el orden de las fichas; uno vertical salta 2 fichas, cambiando
    las inversiones en 0 o ±2. La paridad de inversiones es invariante, así
    que el estado tiene solución si y solo si sus inversiones son pares
    (como la meta, que tiene 0). Hay 9!/2 = 181440 estados alcanzables.

MACROALGORITMO
    1. Definir el estado (inmutable, hashable: tupla) y la meta.
    2. Definir vecinos(e) con su costo y una h admisible y consistente.
    3. heap = [(h(inicio), 0, inicio)]; g[inicio] = 0.
    4. Sacar el de menor f; si es una entrada vieja (g mayor que g[e]), saltar.
    5. Si es meta: reconstruir el camino con padre[] y devolver.
    6. Para cada vecino e' con costo c: si g[e] + c < g[e'], actualizar
       g[e'], padre[e'] y meter (g[e'] + h(e'), g[e'], e') al heap.
    (IDA*)
    7. límite = h(inicio); DFS que corta cuando g + h > límite y recuerda
       el menor f cortado; si no halló la meta, límite = ese mínimo.

COMPLEJIDAD
    Exponencial en el peor caso; depende de la calidad de h. 8-puzzle con
    Manhattan: soluciones de hasta 31 movimientos, miles a decenas de miles
    de expansiones (≈ 0,01–0,3 s en Python). A* usa memoria O(estados
    visitados); IDA*, O(profundidad).

EJEMPLO A MANO
    estado = (1, 2, 3,
              4, 0, 6,
              7, 5, 8)    Manhattan: 5 está a 1 de su casilla, 8 a 1 → h = 2
      g=0 f=2: hueco al centro. Vecinos: hueco abajo (5 sube) → h = 1, f = 2
      g=1 f=2: (1,2,3,4,5,6,7,0,8). Hueco a la derecha (8 a la izquierda) → meta
    → 2 movimientos, texto "DR"

ERRORES TÍPICOS
    - Heurística no admisible (p. ej. contar el hueco en Manhattan): A*
      deja de garantizar el óptimo.
    - No descartar entradas viejas del heap (procesar un estado dos veces).
    - Marcar como visitado al METER al heap en vez de al SACAR (con h solo
      admisible puede perder el óptimo).
    - Estados mutables (listas) como claves de diccionario.
    - No verificar la resolubilidad: A* explora los 181440 estados y falla.
    - IDA* sin evitar volver al estado padre: se pierde mucho tiempo en
      idas y vueltas.

VARIANTES Y RELACIONADOS
    - h ≡ 0: Dijkstra; costos 1 y h ≡ 0: BFS.
    - Mejores heurísticas: conflicto lineal, bases de datos de patrones.
    - BFS bidireccional / encuentro en el medio sobre estados.
    - Relacionados: backtracking_poda.py, branch_and_bound.py (IDA* es una
      ramificación y poda con cota g + h).

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/G - Grain Silos (A* sobre configuraciones de silos)
    - UVa 652 «Eight» (8-puzzle con reconstrucción del camino)
    - UVa 10181 «15-Puzzle Problem» (IDA*)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (BFS desde la meta sobre los 181440
      estados alcanzables): A* en 40 estados aleatorios con su camino
      validado paso a paso, IDA* en 40 estados de distancia ≤ 20,
      admisibilidad de Manhattan en 20000 estados, y estados sin solución
      (python a_estrella.py)
"""
import heapq
import random
from collections import deque

META = (1, 2, 3, 4, 5, 6, 7, 8, 0)
# Movimientos del HUECO en el tablero 3x3: letra -> desplazamiento de índice
MOVS = (("U", -3), ("D", 3), ("L", -1), ("R", 1))


def a_estrella(inicio, es_meta, vecinos, h):
    """(costo, camino) del camino más corto, o (None, None) si no hay."""
    g = {inicio: 0}
    padre = {inicio: None}
    heap = [(h(inicio), 0, inicio)]
    while heap:
        f, ge, e = heapq.heappop(heap)
        if ge > g[e]:
            continue                        # entrada vieja: ya se encontró algo mejor
        if es_meta(e):
            camino = []
            while e is not None:
                camino.append(e)
                e = padre[e]
            return ge, camino[::-1]
        for s, c in vecinos(e):
            ng = ge + c
            if ng < g.get(s, float("inf")):
                g[s] = ng
                padre[s] = e
                heapq.heappush(heap, (ng + h(s), ng, s))
    return None, None


def ida_estrella(inicio, es_meta, vecinos, h):
    """Costo del camino más corto con IDA* (memoria O(profundidad)), o None."""
    camino = [inicio]
    en_camino = {inicio}
    costo_meta = [None]

    def dfs(e, ge, limite):
        """Devuelve -1 si llegó a la meta, si no el menor f que superó el límite."""
        f = ge + h(e)
        if f > limite:
            return f
        if es_meta(e):
            costo_meta[0] = ge
            return -1
        minimo = float("inf")
        for s, c in vecinos(e):
            if s in en_camino:
                continue                    # no volver a estados del camino actual
            camino.append(s); en_camino.add(s)
            r = dfs(s, ge + c, limite)
            if r == -1:
                return -1
            camino.pop(); en_camino.remove(s)
            minimo = min(minimo, r)
        return minimo

    limite = h(inicio)
    while True:
        r = dfs(inicio, 0, limite)
        if r == -1:
            return costo_meta[0]            # (con h admisible coincide con el límite)
        if r == float("inf"):
            return None                     # no hay más estados: sin solución
        limite = r


# ---------------- 8-puzzle ----------------

def manhattan(estado):
    """Suma de distancias Manhattan de cada ficha (no el hueco) a su casilla meta."""
    d = 0
    for i, v in enumerate(estado):
        if v:
            m = v - 1                       # casilla meta de la ficha v
            d += abs(i // 3 - m // 3) + abs(i % 3 - m % 3)
    return d


def vecinos_8puzzle(estado):
    z = estado.index(0)
    for _, delta in MOVS:
        j = z + delta
        # no salirse del tablero ni «envolver» de una fila a otra
        if 0 <= j < 9 and (delta in (-3, 3) or j // 3 == z // 3):
            l = list(estado)
            l[z], l[j] = l[j], l[z]
            yield tuple(l), 1


def resoluble(estado):
    """Tablero 3x3: tiene solución si y solo si las inversiones son pares."""
    fichas = [v for v in estado if v]
    inv = sum(1 for i in range(8) for j in range(i + 1, 8) if fichas[i] > fichas[j])
    return inv % 2 == 0


def resolver_8puzzle(estado, con_ida=False):
    """(movimientos, texto U/D/L/R del hueco); (-1, "") si no tiene solución."""
    estado = tuple(estado)
    if not resoluble(estado):
        return -1, ""
    if con_ida:
        return ida_estrella(estado, lambda e: e == META, vecinos_8puzzle, manhattan), ""
    costo, camino = a_estrella(estado, lambda e: e == META, vecinos_8puzzle, manhattan)
    texto = []
    for a, b in zip(camino, camino[1:]):
        delta = b.index(0) - a.index(0)
        texto.append(next(letra for letra, d in MOVS if d == delta))
    return costo, "".join(texto)


def demo():
    e = (1, 2, 3, 4, 0, 6, 7, 5, 8)
    print("estado:", e[0:3], e[3:6], e[6:9], " h =", manhattan(e))
    print("A*  :", resolver_8puzzle(e))                         # (2, 'DR')
    dificil = (8, 6, 7, 2, 5, 4, 3, 0, 1)                         # uno de los más difíciles (31)
    print("A*  en", dificil, "→", resolver_8puzzle(dificil)[0], "movimientos")
    print("IDA* en (4,1,3,7,2,6,0,5,8) →", resolver_8puzzle((4, 1, 3, 7, 2, 6, 0, 5, 8), con_ida=True)[0])
    print("sin solución (1,2,3,4,5,6,8,7,0) →", resolver_8puzzle((1, 2, 3, 4, 5, 6, 8, 7, 0)))


def _bfs_desde_meta():
    """Distancia real de cada estado alcanzable a la meta (los movimientos son reversibles)."""
    dist = {META: 0}
    cola = deque([META])
    while cola:
        e = cola.popleft()
        for s, _ in vecinos_8puzzle(e):
            if s not in dist:
                dist[s] = dist[e] + 1
                cola.append(s)
    return dist


def _aplicar(estado, texto):
    l = list(estado)
    for letra in texto:
        z = l.index(0)
        j = z + dict(MOVS)[letra]
        assert 0 <= j < 9 and (letra in "UD" or j // 3 == z // 3)   # movimiento legal
        l[z], l[j] = l[j], l[z]
    return tuple(l)


def pruebas():
    random.seed(652)
    dist = _bfs_desde_meta()
    assert len(dist) == 181440                       # 9!/2 estados alcanzables
    assert max(dist.values()) == 31

    # Casos borde
    assert resolver_8puzzle(META) == (0, "")
    assert resolver_8puzzle(META, con_ida=True) == (0, "")
    assert resolver_8puzzle((1, 2, 3, 4, 5, 6, 8, 7, 0)) == (-1, "")

    # Resolubilidad = alcanzable desde la meta
    estados = list(dist)
    for _ in range(2000):
        p = list(range(9)); random.shuffle(p)
        assert resoluble(p) == (tuple(p) in dist)

    # Admisibilidad de Manhattan
    for e in random.sample(estados, 20000):
        assert manhattan(e) <= dist[e]

    # A*: costo óptimo y camino válido
    for e in random.sample(estados, 40):
        costo, texto = resolver_8puzzle(e)
        assert costo == dist[e] == len(texto)
        assert _aplicar(e, texto) == META

    # IDA*: estados de distancia <= 20
    cercanos = [e for e in estados if dist[e] <= 20]
    for e in random.sample(cercanos, 40):
        assert resolver_8puzzle(e, con_ida=True)[0] == dist[e]


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
