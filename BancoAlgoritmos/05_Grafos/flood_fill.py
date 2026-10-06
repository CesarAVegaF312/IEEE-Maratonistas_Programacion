"""
Grafos — Relleno por inundación en grillas («Flood fill»)
Nivel: Básico
Ejecutar: python flood_fill.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Pintar / marcar toda la región conectada de una grilla que contiene una
    celda dada (el «balde de pintura» de un editor de imágenes), y con eso
    contar regiones: islas, lagos, cuartos, manchas de petróleo, y medir su
    tamaño.
    Señales en el enunciado: mapa de caracteres ('.', '#', 'W', '@'…),
    «cuántas islas / cuartos / lagos», «tamaño de la región más grande»,
    «celdas adyacentes» (aclara si son 4 u 8 vecinos: ¡léelo!).

FUNCIÓN
    flood_fill(grilla, f, c, nuevo, ocho=False) -> int
        grilla: lista de listas de caracteres (se MODIFICA). Cambia a `nuevo`
        toda la región conectada de celdas con el mismo valor que (f, c).
        Devuelve cuántas celdas pintó (0 si ya era `nuevo`).
    etiquetar_regiones(grilla, terreno, ocho=False) -> (etiqueta, tamanos)
        etiqueta[f][c] = número de región (0, 1, 2…) de cada celda cuyo
        valor está en `terreno`; -1 para las demás. tamanos[k] = celdas de la
        región k. El número de regiones es len(tamanos).
    contar_lagos(grilla, agua='.') -> int
        Regiones de agua (4 vecinos) que NO tocan el borde de la grilla.

IDEA Y ALGORITMO
    Una grilla es un grafo implícito: cada celda es un vértice y está unida a
    sus 4 (u 8) vecinas del mismo tipo. Una «región» es una componente
    conexa de ese grafo. Flood fill = BFS (o DFS) desde una celda, sin
    construir el grafo: los vecinos se generan con la tabla de direcciones.
    Contar regiones: recorrer todas las celdas; cada vez que se encuentra
    una de terreno aún sin etiqueta, empieza una región NUEVA (nadie la
    alcanzó antes, así que no pertenece a ninguna región ya contada) y se
    inunda entera. Cada celda se etiqueta una sola vez → O(F·C) total.
    Lagos: el agua que toca el borde «se escapa» al exterior; un lago es una
    región de agua completamente rodeada. Truco: inundar primero desde las
    celdas de agua del borde y contar después las regiones que queden.
    Por qué iterativo: una grilla 1000×1000 con forma de serpiente tiene una
    región de 10^6 celdas → un DFS recursivo de profundidad 10^6 tumba a
    Python. Con cola (BFS) o pila explícita no hay límite.

MACROALGORITMO
    1. etiqueta = -1 en todas las celdas; k = 0.
    2. Para cada celda (f, c) de terreno con etiqueta -1:
    3.   etiqueta[f][c] = k; cola = [(f, c)].
    4.   Mientras haya celdas en la cola: sacar una; para cada vecina dentro
         de la grilla, de terreno y sin etiqueta: etiquetarla k y meterla.
    5.   Guardar el tamaño de la región; k += 1.
    6. Respuesta: k regiones (o máx(tamanos), etc.).

COMPLEJIDAD
    O(F·C) tiempo y memoria (cada celda entra a la cola una vez y mira 4 u 8
    vecinas). En Python ~10^6 celdas en 1–2 s; para grillas enormes conviene
    aplanar la grilla a una lista 1D con id = f*C + c.

EJEMPLO A MANO
    Grilla (# = tierra):    ##..#     4 vecinos: regiones de tierra
                            #...#       A = {(0,0),(0,1),(1,0)}
                            ..#..       B = {(0,4),(1,4)}
                            ...##       C = {(2,2)}   D = {(3,3),(3,4)}
    → 4 islas con 4 vecinos. Con 8 vecinos (2,2) toca a (3,3) en diagonal:
      C y D se unen → 3 islas. Agua: una sola región y toca el borde → 0 lagos.

ERRORES TÍPICOS
    - Usar 4 vecinos cuando el problema dice 8 (o al revés).
    - Marcar la celda al SACARLA de la cola: se repite muchas veces.
    - DFS recursivo en grillas grandes: RecursionError.
    - Strings de Python son inmutables: para pintar, convertir cada fila en
      lista (list(fila)).
    - flood_fill con nuevo == color original: ciclo infinito si no se revisa.

VARIANTES Y RELACIONADOS
    - Grafos generales: componentes_conexas.py. Con uniones dinámicas
      (celdas que se van activando): union_find.py.
    - Distancia mínima en la grilla: bfs.py; con costos 0/1: bfs_01.py.
    - Vecinos y grilla como grafo: representacion_grafos.py.

DÓNDE PRACTICAR
    - CSES «Counting Rooms»
    - UVa 572 «Oil Deposits» (8 vecinos), UVa 469 «Wetlands of Florida»
      (tamaño de la región que contiene una celda)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (propagar la etiqueta mínima entre
      vecinas hasta que nada cambie) en 1500 grillas aleatorias con 4 y 8
      vecinos, flood_fill contra la región etiquetada, lagos contra su
      definición, y una espiral de 250000 celdas (python flood_fill.py)
"""
import random
from collections import deque

DIR4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIR8 = DIR4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def flood_fill(grilla, f, c, nuevo, ocho=False):
    """Pinta con `nuevo` la región de (f, c) (mismo valor, 4 u 8 vecinos)."""
    F, C = len(grilla), len(grilla[0])
    viejo = grilla[f][c]
    if viejo == nuevo:          # sin esto, nunca se distinguiría lo ya pintado
        return 0
    dirs = DIR8 if ocho else DIR4
    grilla[f][c] = nuevo        # pintar = marcar como visitada
    cola = deque([(f, c)])
    pintadas = 1
    while cola:
        f, c = cola.popleft()
        for df, dc in dirs:
            nf, nc = f + df, c + dc
            if 0 <= nf < F and 0 <= nc < C and grilla[nf][nc] == viejo:
                grilla[nf][nc] = nuevo
                pintadas += 1
                cola.append((nf, nc))
    return pintadas


def etiquetar_regiones(grilla, terreno, ocho=False):
    """Etiqueta cada región conectada de celdas con valor en `terreno`."""
    F, C = len(grilla), len(grilla[0]) if grilla else 0
    dirs = DIR8 if ocho else DIR4
    etiqueta = [[-1] * C for _ in range(F)]
    tamanos = []
    for f0 in range(F):
        for c0 in range(C):
            if grilla[f0][c0] not in terreno or etiqueta[f0][c0] != -1:
                continue
            k = len(tamanos)               # región nueva: nadie la alcanzó antes
            etiqueta[f0][c0] = k
            cola = deque([(f0, c0)])
            tam = 1
            while cola:
                f, c = cola.popleft()
                for df, dc in dirs:
                    nf, nc = f + df, c + dc
                    if (0 <= nf < F and 0 <= nc < C and etiqueta[nf][nc] == -1
                            and grilla[nf][nc] in terreno):
                        etiqueta[nf][nc] = k
                        tam += 1
                        cola.append((nf, nc))
            tamanos.append(tam)
    return etiqueta, tamanos


def contar_lagos(grilla, agua='.'):
    """Regiones de agua (4 vecinos) que no tocan el borde de la grilla."""
    g = [list(fila) for fila in grilla]    # copia: no dañar la entrada
    F, C = len(g), len(g[0])
    # 1) El agua conectada al borde no es lago: se borra inundándola.
    for f in range(F):
        for c in range(C):
            if (f in (0, F - 1) or c in (0, C - 1)) and g[f][c] == agua:
                flood_fill(g, f, c, '\0')
    # 2) Lo que queda de agua son lagos; cada inundación es uno.
    lagos = 0
    for f in range(F):
        for c in range(C):
            if g[f][c] == agua:
                flood_fill(g, f, c, '\0')
                lagos += 1
    return lagos


def _fuerza_bruta(grilla, terreno, ocho):
    """Cada celda empieza con su propio número y toma el mínimo de sus vecinas
    del mismo terreno hasta que nada cambie; regiones = valores distintos."""
    F, C = len(grilla), len(grilla[0])
    lab = [[f * C + c if grilla[f][c] in terreno else -1 for c in range(C)]
           for f in range(F)]
    cambio = True
    while cambio:
        cambio = False
        for f in range(F):
            for c in range(C):
                if lab[f][c] == -1:
                    continue
                for g in range(F):
                    for d in range(C):
                        df, dc = abs(f - g), abs(c - d)
                        vecina = df + dc == 1 or (ocho and df == 1 and dc == 1)
                        if vecina and lab[g][d] != -1 and lab[g][d] < lab[f][c]:
                            lab[f][c] = lab[g][d]
                            cambio = True
    return lab


def demo():
    grilla = ["##..#",
              "#...#",
              "..#..",
              "...##"]
    for fila in grilla:
        print("   ", fila)
    _, t4 = etiquetar_regiones(grilla, "#")
    _, t8 = etiquetar_regiones(grilla, "#", ocho=True)
    print("islas (4 vecinos):", len(t4), "tamaños", t4)   # 4 [3, 2, 1, 2]
    print("islas (8 vecinos):", len(t8), "tamaños", t8)   # 3 [3, 2, 3]
    print("lagos:", contar_lagos(grilla))                  # 0
    g = [list(fila) for fila in grilla]
    print("flood_fill desde (0,2) con '~' pintó", flood_fill(g, 0, 2, "~"), "celdas")
    for fila in g:
        print("   ", "".join(fila))
    anillo = ["#####", "#..##", "#####", "#.#..", "#####"]
    print("lagos en", anillo, "=", contar_lagos(anillo))   # 2


def pruebas():
    random.seed(31)
    casos = 0

    # Casos borde
    assert etiquetar_regiones(["."], "#") == ([[-1]], [])
    assert etiquetar_regiones(["#"], "#") == ([[0]], [1])
    assert flood_fill([["a"]], 0, 0, "a") == 0
    assert contar_lagos(["..."]) == 0
    assert contar_lagos(["###", "#.#", "###"]) == 1

    # Espiral grande (región de ~125000 celdas en un solo camino): sin recursión
    N = 500
    g = [["#"] * N for _ in range(N)]
    for f in range(0, N, 2):
        for c in range(N):
            g[f][c] = "."
        if f + 1 < N:
            g[f + 1][N - 1 if (f // 2) % 2 == 0 else 0] = "."
    _, tam = etiquetar_regiones(g, ".")
    assert len(tam) == 1 and tam[0] == sum(fila.count(".") for fila in g)

    for _ in range(1500):
        F, C = random.randint(1, 6), random.randint(1, 6)
        p = random.random()
        grilla = ["".join("#" if random.random() < p else "." for _ in range(C))
                  for _ in range(F)]
        for ocho in (False, True):
            etiqueta, tamanos = etiquetar_regiones(grilla, "#", ocho)
            bruta = _fuerza_bruta(grilla, "#", ocho)
            # Misma partición: dos celdas comparten etiqueta ⇔ comparten valor bruto
            celdas = [(f, c) for f in range(F) for c in range(C) if grilla[f][c] == "#"]
            assert len(tamanos) == len({bruta[f][c] for f, c in celdas})
            for a in celdas:
                for b in celdas:
                    assert ((etiqueta[a[0]][a[1]] == etiqueta[b[0]][b[1]]) ==
                            (bruta[a[0]][a[1]] == bruta[b[0]][b[1]]))
            assert sum(tamanos) == len(celdas)
            # flood_fill desde una celda pinta exactamente su región
            if celdas:
                f, c = random.choice(celdas)
                g = [list(fila) for fila in grilla]
                k = etiqueta[f][c]
                assert flood_fill(g, f, c, "X", ocho) == tamanos[k]
                for x, y in celdas:
                    assert (g[x][y] == "X") == (etiqueta[x][y] == k)
        # Lagos: regiones de agua (4 vecinos) sin ninguna celda en el borde
        etq, tam = etiquetar_regiones(grilla, ".")
        con_borde = {etq[f][c] for f in range(F) for c in range(C)
                     if etq[f][c] != -1 and (f in (0, F - 1) or c in (0, C - 1))}
        assert contar_lagos(grilla) == len(tam) - len(con_borde)
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
