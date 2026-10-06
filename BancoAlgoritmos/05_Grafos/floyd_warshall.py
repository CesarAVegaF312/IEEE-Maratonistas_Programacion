"""
Grafos — Floyd–Warshall y clausura transitiva («Floyd–Warshall algorithm»)
Nivel: Intermedio
Ejecutar: python floyd_warshall.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Distancias mínimas entre TODOS los pares de vértices (admite pesos
    negativos y detecta ciclos negativos) con un código de 4 líneas. Su
    versión booleana es la clausura transitiva: «¿u alcanza a v?» para todo
    par.
    Señales en el enunciado: n pequeño (≤ ~150 en Python, ≤ 400–500 en C++),
    muchas consultas «distancia entre a y b», «el peor caso entre cualquier
    par» (diámetro), «elegir el punto de encuentro que minimiza…»,
    relaciones transitivas («si A le gana a B y B a C, A le gana a C»).

FUNCIÓN
    floyd_warshall(n, aristas, dirigido=True) -> (dist, sig)
        aristas = [(u, v, w)]. dist[i][j] = costo mínimo de i a j (INF si no
        hay camino). Si algún dist[i][i] < 0, i está en un ciclo negativo y
        las distancias que pasan por él no son confiables (son −∞).
        sig[i][j] = siguiente vértice después de i en un camino mínimo a j.
    camino(sig, i, j) -> list    vértices de i a j; [] si no hay camino.
    clausura_transitiva(n, aristas) -> list[int]
        alc[i] = máscara de bits: el bit j está prendido ⇔ i alcanza a j por
        un camino de largo ≥ 0 (cada vértice se alcanza a sí mismo).

IDEA Y ALGORITMO
    Programación dinámica sobre los vértices intermedios permitidos:
    D_k[i][j] = mejor camino de i a j cuyos vértices INTERNOS están en
    {0, …, k−1}. Al permitir también el vértice k, el mejor camino o no lo
    usa (D_k[i][j]) o pasa por k una sola vez (D_k[i][k] + D_k[k][j]):
        D_{k+1}[i][j] = min(D_k[i][j], D_k[i][k] + D_k[k][j]).
    Se puede usar UNA sola matriz porque en la ronda k la fila k y la
    columna k no cambian (D[i][k] + D[k][k] ≥ D[i][k] si no hay ciclos
    negativos). Por eso el bucle de k va AFUERA: es la etapa de la DP.
    Reconstrucción: sig[i][j] se inicia en j para cada arista y, cuando el
    camino mejora pasando por k, sig[i][j] = sig[i][k].
    Clausura: lo mismo con «o/y» en vez de «min/+». Con máscaras de bits de
    Python cada fila se actualiza de un golpe: si i alcanza a k, entonces
    alc[i] |= alc[k]. Son n² operaciones sobre enteros de n bits: rapidísimo.
    Comparación: n veces Dijkstra cuesta O(n·m log m); con grafos densos
    (m ≈ n²) Floyd es más simple y del mismo orden.

MACROALGORITMO
    1. D = INF en todo, D[i][i] = 0; por cada arista D[u][v] = min(D[u][v], w)
       y sig[u][v] = v.
    2. Para k = 0..n−1 (AFUERA), para i, para j:
       si D[i][k] + D[k][j] < D[i][j]: actualizar D[i][j] y sig[i][j] = sig[i][k].
    3. Ciclo negativo ⇔ algún D[i][i] < 0.
    4. Camino i→j: i, sig[i][j], sig[sig[i][j]][j], … hasta j.

COMPLEJIDAD
    O(n³) tiempo, O(n²) memoria. En Python, con el truco de sacar la fila
    D[i] y D[i][k] a variables locales, n ≈ 150–200 en ~1 s. La clausura con
    bits es O(n²) operaciones de enteros: n ≈ 2000 sin problema.

EJEMPLO A MANO
    No dirigido: 0-1 (3), 1-2 (1), 0-2 (7), 2-3 (2).
      Inicial D[0] = [0, 3, 7, ∞]
      k = 1: D[0][2] = min(7, 3 + 1) = 4
      k = 2: D[0][3] = min(∞, 4 + 2) = 6, D[1][3] = 1 + 2 = 3
    D[0] = [0, 3, 4, 6]; camino 0 → 3: 0, 1, 2, 3. Diámetro = 6.

ERRORES TÍPICOS
    - Poner el bucle de k adentro (i, j, k): NO es correcto en general.
    - Con INF entero: INF + INF desborda en C++; en Python usar float('inf')
      o revisar D[i][k] < INF antes de sumar.
    - Aristas repetidas: quedarse con la MENOR (no sobrescribir).
    - Ciclos negativos: dist[i][j] queda con un valor finito engañoso; un par
      i, j es −∞ si existe k con D[k][k] < 0, D[i][k] < INF y D[k][j] < INF.

VARIANTES Y RELACIONADOS
    - Diámetro del grafo = máx D[i][j] finito; centro = argmin_i máx_j D[i][j].
    - Minimax / maximin (cuello de botella): cambiar (min, +) por (min, max).
    - Ciclo mínimo dirigido: min_i D[i][i] inicializando D[i][i] = INF.
    - Un origen: dijkstra.py / bellman_ford.py. Alcanzabilidad desde uno: bfs.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/A - A Contest to Meet (Floyd–Warshall + diámetro /
      velocidad mínima)
    - CSES «Shortest Routes II»
    - UVa 821 «Page Hopping» (promedio de distancias entre todos los pares)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta en 1500 grafos aleatorios: distancias
      contra enumeración de todos los caminos simples (pesos −3..9 sin ciclos
      negativos) y Bellman-Ford desde cada vértice; detección de ciclos
      negativos; caminos reconstruidos validados; clausura contra un BFS por
      vértice (python floyd_warshall.py)
"""
import random
from collections import deque

INF = float("inf")


def floyd_warshall(n, aristas, dirigido=True):
    """Distancias entre todos los pares y tabla `sig` para reconstruir caminos."""
    D = [[INF] * n for _ in range(n)]
    sig = [[-1] * n for _ in range(n)]
    for i in range(n):
        D[i][i] = 0
        sig[i][i] = i
    for u, v, w in aristas:
        if w < D[u][v]:                      # aristas repetidas: la más barata
            D[u][v] = w
            sig[u][v] = v
        if not dirigido and w < D[v][u]:
            D[v][u] = w
            sig[v][u] = u
    for k in range(n):                       # k = nuevo intermedio permitido (AFUERA)
        Dk = D[k]
        for i in range(n):
            dik = D[i][k]
            if dik == INF:                   # i no llega a k: nada que mejorar
                continue
            Di, Si = D[i], sig[i]
            sik = Si[k]
            for j in range(n):
                nd = dik + Dk[j]
                if nd < Di[j]:
                    Di[j] = nd
                    Si[j] = sik              # para ir a j por k, primero ir hacia k
    return D, sig


def camino(sig, i, j):
    """Vértices de i a j por un camino mínimo ([] si no hay camino)."""
    if sig[i][j] == -1:
        return []
    ruta = [i]
    while i != j:
        i = sig[i][j]
        ruta.append(i)
    return ruta


def clausura_transitiva(n, aristas):
    """alc[i] = máscara de los vértices alcanzables desde i (incluye a i)."""
    alc = [1 << i for i in range(n)]
    for u, v in aristas:
        alc[u] |= 1 << v
    for k in range(n):
        bit, ak = 1 << k, alc[k]
        for i in range(n):
            if alc[i] & bit:                 # i alcanza a k ⇒ alcanza todo lo de k
                alc[i] |= ak
    return alc


def demo():
    aristas = [(0, 1, 3), (1, 2, 1), (0, 2, 7), (2, 3, 2)]
    D, sig = floyd_warshall(4, aristas, dirigido=False)
    print("aristas no dirigidas:", aristas)
    for fila in D:
        print("   ", fila)
    print("camino 0 → 3:", camino(sig, 0, 3))                # [0, 1, 2, 3]
    print("diámetro:", max(max(f) for f in D))               # 6
    alc = clausura_transitiva(4, [(0, 1), (1, 2), (3, 0)])
    # Cada máscara se muestra con el bit 0 a la IZQUIERDA (carácter j = ¿alcanza a j?)
    print("clausura de 0→1→2, 3→0:", [format(a, "04b")[::-1] for a in alc])


def pruebas():
    random.seed(2017)
    casos = 0

    assert floyd_warshall(0, []) == ([], [])
    assert floyd_warshall(1, [(0, 0, 5)])[0] == [[0]]
    assert floyd_warshall(1, [(0, 0, -1)])[0][0][0] < 0      # lazo negativo
    assert clausura_transitiva(2, []) == [1, 2]

    for _ in range(1500):
        n = random.randint(1, 6)
        m = random.randint(0, 10)
        dirigido = random.random() < 0.7
        bajo = -3 if dirigido else 0          # no dirigido con w<0 = ciclo negativo
        aristas = [(random.randrange(n), random.randrange(n), random.randint(bajo, 9))
                   for _ in range(m)]
        D, sig = floyd_warshall(n, aristas, dirigido)
        lista = aristas + ([] if dirigido else [(v, u, w) for u, v, w in aristas])

        # Ciclo negativo (fuerza bruta): Bellman-Ford desde todos con dist 0
        bf = [0] * n
        for _ in range(n):
            for u, v, w in lista:
                bf[v] = min(bf[v], bf[u] + w)
        hay_neg = any(bf[u] + w < bf[v] for u, v, w in lista)
        assert hay_neg == any(D[i][i] < 0 for i in range(n))

        if not hay_neg:
            # Distancias: mínimo sobre TODOS los caminos simples
            for s in range(n):
                mejor = [INF] * n
                mejor[s] = 0
                pila = [(s, 0, 1 << s)]
                while pila:
                    u, c, us = pila.pop()
                    for a, b, w in lista:
                        if a == u and not us >> b & 1:
                            mejor[b] = min(mejor[b], c + w)
                            pila.append((b, c + w, us | 1 << b))
                assert D[s] == mejor
                # Caminos reconstruidos: existen y suman D[s][t]
                peso = {}
                for a, b, w in lista:
                    peso[(a, b)] = min(w, peso.get((a, b), INF))
                for t in range(n):
                    ruta = camino(sig, s, t)
                    if D[s][t] == INF:
                        assert ruta == []
                    else:
                        assert ruta[0] == s and ruta[-1] == t
                        assert sum(peso[(ruta[i], ruta[i + 1])]
                                   for i in range(len(ruta) - 1)) == D[s][t]

        # Clausura transitiva contra un BFS desde cada vértice
        alc = clausura_transitiva(n, [(u, v) for u, v, _ in lista])
        for s in range(n):
            visto = {s}
            cola = deque([s])
            while cola:
                u = cola.popleft()
                for a, b, _ in lista:
                    if a == u and b not in visto:
                        visto.add(b)
                        cola.append(b)
            assert alc[s] == sum(1 << v for v in visto)
            if not hay_neg:
                assert all((D[s][t] < INF) == (t in visto) for t in range(n))
        casos += 1

    # Tamaño mediano para medir que el bucle optimizado no es lento
    n = 120
    ar = [(random.randrange(n), random.randrange(n), random.randint(1, 100))
          for _ in range(2000)]
    D, _ = floyd_warshall(n, ar)
    assert all(D[i][i] == 0 for i in range(n))
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
