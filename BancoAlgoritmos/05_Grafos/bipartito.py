"""
Grafos — Grafo bipartito / 2-coloración («Bipartite check, 2-coloring»)
Nivel: Básico
Ejecutar: python bipartito.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir si los vértices de un grafo se pueden pintar con DOS colores de
    modo que toda arista una vértices de distinto color (equivalente: partir
    los vértices en dos grupos sin aristas dentro de un grupo), y dar la
    coloración.
    Señales en el enunciado: «dos equipos / dos bandos», «enemigos no pueden
    quedar juntos», «colorear con 2 colores», «placebo y droga», «paridad»
    (grillas y caballos de ajedrez son bipartitos por color de casilla),
    «¿hay un ciclo de largo impar?».

FUNCIÓN
    bipartito(adj) -> (es, color)
        es = True si el grafo es bipartito. color[v] ∈ {0, 1} es una
        2-coloración válida (si es True); si es False, color no sirve.
        Funciona con grafos no conexos (colorea cada componente).
    resolver_uva10004(texto) -> str
        UVa 10004 «Bicoloring» completo: casos «n, e, e aristas» hasta n = 0;
        imprime «BICOLORABLE.» o «NOT BICOLORABLE.».

IDEA Y ALGORITMO
    En una componente conexa, fijar el color de un vértice s determina el de
    todos los demás: un vecino de s debe tener el color contrario, el vecino
    de ese otra vez el de s, etc. Es decir, color[v] = paridad de la
    distancia a s POR CUALQUIER CAMINO. El BFS asigna color[v] = 1 − color[u]
    al descubrir v desde u y luego revisa TODAS las aristas: si alguna une
    dos vértices del mismo color, no hay 2-coloración (la coloración era
    forzada, así que ninguna otra elección habría servido).
    Teorema (König): un grafo es bipartito ⇔ no tiene ciclos de largo impar.
    Un ciclo impar obliga a alternar colores un número impar de veces y
    volver al mismo vértice: contradicción. La arista conflictiva que
    encuentra el BFS cierra justamente un ciclo impar.
    Probar las 2^n coloraciones es la fuerza bruta (solo n ≤ ~20).

MACROALGORITMO
    1. color = [-1]*n.
    2. Para cada s sin color: color[s] = 0, BFS desde s.
    3. Al sacar u, para cada vecino v:
         si color[v] == -1: color[v] = 1 − color[u], meterlo a la cola;
         si color[v] == color[u]: devolver «no bipartito».
    4. Si se terminan todas las componentes sin conflicto: bipartito.

COMPLEJIDAD
    O(n + m) tiempo, O(n) memoria. ~10^6 aristas por segundo en Python.

EJEMPLO A MANO
    Triángulo 0-1, 1-2, 2-0: color[0]=0 → color[1]=1, color[2]=1; al
    revisar la arista 1-2 ambos tienen color 1 → NOT BICOLORABLE.
    Camino 0-1, 1-2: colores 0, 1, 0 → BICOLORABLE.
    Estrella 0-1, …, 0-8: centro 0, hojas 1 → BICOLORABLE.
    (Son los tres casos de ejemplo de UVa 10004.)

ERRORES TÍPICOS
    - Colorear solo desde el vértice 0 si el grafo puede ser no conexo.
    - Solo mirar aristas hacia vértices SIN color: el conflicto aparece con
      vecinos YA coloreados; hay que comparar siempre.
    - Lazos (u-u): hacen al grafo no bipartito; el chequeo color[v]==color[u]
      ya lo detecta si el lazo está en la lista de adyacencia.
    - DFS recursivo en grafos grandes (usar cola/pila explícita).

VARIANTES Y RELACIONADOS
    - Minimizar/maximizar un bando: en cada componente hay exactamente dos
      coloraciones (intercambiar colores); elegir por componente (a veces
      con una mochila sobre las componentes).
    - Restricciones «iguales / distintos» entre pares: BFS con paridad en la
      arista o union_find.py con paridad.
    - Emparejamiento en grafos bipartitos: emparejamiento_bipartito.py.
    - Restricciones de dos opciones más generales (x o y): dos_sat.py.

DÓNDE PRACTICAR
    - 2026-1/problemas/10004 - Bicoloring (maratón interna 2026-1;
      UVa 10004 «Bicoloring»)
    - ICPC/Colombia 2024/D - Drug Test (2-coloración del grafo «suma =
      potencia de 2»)
    - ICPC/Colombia 2023/C - Knights (el grafo del caballo es bipartito:
      argumento de paridad)
    - CSES «Building Teams»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (probar las 2^n coloraciones) en 2000
      grafos aleatorios, coloración devuelta validada arista por arista,
      ejemplo de UVa 10004 y casos borde (python bipartito.py)
"""
import itertools
import random
from collections import deque


def bipartito(adj):
    """(True, color) si el grafo admite 2-coloración; (False, color) si no."""
    n = len(adj)
    color = [-1] * n
    for s in range(n):
        if color[s] != -1:
            continue
        color[s] = 0                         # cada componente se fija por separado
        cola = deque([s])
        while cola:
            u = cola.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]  # forzado: vecino = color contrario
                    cola.append(v)
                elif color[v] == color[u]:   # arista dentro de un bando: ciclo impar
                    return False, color
    return True, color


def resolver_uva10004(texto):
    """UVa 10004 Bicoloring: lee todos los casos y devuelve la salida completa."""
    tokens = iter(texto.split())
    salida = []
    for tok in tokens:
        n = int(tok)
        if n == 0:
            break
        e = int(next(tokens))
        adj = [[] for _ in range(n)]
        for _ in range(e):
            u, v = int(next(tokens)), int(next(tokens))
            adj[u].append(v)
            adj[v].append(u)
        es, _ = bipartito(adj)
        salida.append("BICOLORABLE." if es else "NOT BICOLORABLE.")
    return "\n".join(salida)


EJEMPLO_10004 = """3
3
0 1
1 2
2 0
3
2
0 1
1 2
9
8
0 1
0 2
0 3
0 4
0 5
0 6
0 7
0 8
0
"""


def _adyacencia(n, aristas):
    adj = [[] for _ in range(n)]
    for u, v in aristas:
        adj[u].append(v)
        if u != v:
            adj[v].append(u)
    return adj


def demo():
    print("Ejemplo UVa 10004:")
    print(resolver_uva10004(EJEMPLO_10004))
    adj = _adyacencia(6, [(0, 1), (1, 2), (2, 3), (4, 5)])
    print("camino 0-1-2-3 y arista 4-5:", bipartito(adj))   # (True, [0,1,0,1,0,1])


def pruebas():
    random.seed(10004)
    casos = 0

    assert resolver_uva10004(EJEMPLO_10004) == \
        "NOT BICOLORABLE.\nBICOLORABLE.\nBICOLORABLE."
    assert bipartito([]) == (True, [])
    assert bipartito([[]])[0] is True
    assert bipartito([[0]])[0] is False                    # lazo
    assert bipartito(_adyacencia(2, [(0, 1), (0, 1)]))[0]  # arista doble: sí
    # Ciclos: par sí, impar no
    for L in range(3, 30):
        es, _ = bipartito(_adyacencia(L, [(i, (i + 1) % L) for i in range(L)]))
        assert es == (L % 2 == 0)

    for _ in range(2000):
        n = random.randint(1, 9)
        m = random.randint(0, 12)
        aristas = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
        es, color = bipartito(_adyacencia(n, aristas))
        # Fuerza bruta: probar todas las coloraciones
        bruta = any(all(c[u] != c[v] for u, v in aristas)
                    for c in itertools.product((0, 1), repeat=n))
        assert es == bruta
        if es:
            assert all(color[u] != color[v] for u, v in aristas)
            assert all(c in (0, 1) for c in color)
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
