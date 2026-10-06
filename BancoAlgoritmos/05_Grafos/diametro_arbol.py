"""
Grafos — Diámetro de un árbol con dos BFS y centro del árbol («Tree diameter», «tree center»)
Nivel: Intermedio
Ejecutar: python diametro_arbol.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Diámetro: el camino más largo entre dos nodos de un árbol (en número
    de aristas o en suma de pesos no negativos). Centro: el nodo (o los
    dos nodos vecinos) que minimiza la distancia al nodo más lejano; esa
    distancia es el radio.
    Señales en el enunciado: árbol (N − 1 aristas, conexo) y «la distancia
    máxima entre dos ciudades», «el peor caso de un mensaje», «dónde poner
    la central para que el más lejano quede lo más cerca posible», «tiempo
    en que el fuego/rumor cubre todo el árbol», N hasta 2·10^5.

FUNCIÓN
    diametro(n, aristas) -> (largo, u, v, camino)
        aristas = (u, v) o (u, v, peso) con peso ≥ 0. largo = suma de pesos
        del camino más largo; u, v sus extremos; camino = lista de nodos de
        u a v. Para n = 1: (0, 0, 0, [0]).
    centro(n, aristas) -> (centros, radio)
        Árbol SIN pesos. centros = lista con 1 o 2 nodos; radio = mínima
        excentricidad (= ⌈diámetro / 2⌉).

IDEA Y ALGORITMO
    Dos BFS: desde cualquier nodo s, el nodo a más lejano es SIEMPRE un
    extremo de algún diámetro. Luego el más lejano desde a, b, da el
    diámetro d(a, b).
    Por qué (esbozo): sea x–y un diámetro. El camino de s a a se cruza (o
    se conecta) con el camino x–y en algún nodo c. Si a no fuera extremo
    de un diámetro, reemplazar a por el extremo de x–y más lejano de c
    daría un camino desde s todavía más largo (o un diámetro más largo),
    contradicción. Esto necesita pesos NO negativos.
    Para el camino se guarda el padre de cada nodo en el segundo recorrido.
    En un árbol el camino entre dos nodos es único, así que cualquier
    recorrido (BFS o DFS con pila) da las distancias correctas, también
    con pesos: no hace falta Dijkstra.
    Centro: «pelar hojas». Quitar a la vez todas las hojas, repetir; los
    últimos 1 o 2 nodos que quedan son el centro. Cada ronda baja en 1 la
    excentricidad de todos los nodos que quedan, y el centro es lo último
    en desaparecer. Equivalente: el o los nodos del medio del diámetro.
    Ingenuo: BFS desde cada nodo, O(N²).

MACROALGORITMO
    Diámetro:
    1. Recorrer desde el nodo 0 calculando distancias; a = el más lejano.
    2. Recorrer desde a guardando distancias y padres; b = el más lejano.
    3. largo = dist[b]; reconstruir el camino subiendo por padres de b a a.
    Centro:
    4. grado de cada nodo; hojas = nodos de grado ≤ 1.
    5. Mientras queden más de 2 nodos: quitar todas las hojas actuales,
       bajar el grado de sus vecinos y los que quedan con grado 1 son las
       hojas de la ronda siguiente; radio += 1.
    6. Lo que queda es el centro; si son 2, radio += 1.

COMPLEJIDAD
    Tiempo O(N), memoria O(N). En Python N = 2·10^5 en < 1 s.

EJEMPLO A MANO
    n = 8, aristas 0–1, 1–2, 2–3, 1–4, 4–5, 5–6, 2–7.
    Desde 0: distancias 0:0 1:1 2:2 4:2 3:3 5:3 7:3 6:4 → a = 6.
    Desde 6: 5:1 4:2 1:3 0:4 2:4 3:5 7:5 → b = 3, diámetro 5:
    camino 6–5–4–1–2–3.
    Centro: hojas {0, 3, 6, 7} → quedan {1, 2, 4, 5}; hojas {2, 5} → quedan
    {1, 4}: dos nodos → centro {1, 4}, radio 3 (= ⌈5 / 2⌉).

ERRORES TÍPICOS
    - Usar pesos negativos: el truco de los dos recorridos deja de valer
      (usar DP en árbol).
    - DFS recursivo en un árbol-camino de 10^5 nodos: revienta la pila.
    - Confundir número de nodos con número de aristas del diámetro.
    - En el centro, pelar las hojas de a una (no por rondas) o parar en
      «queda 1 nodo» olvidando el caso de 2 centros.
    - Aplicarlo a un grafo con ciclos: el diámetro de un grafo general es
      otra historia (BFS desde cada nodo o Floyd–Warshall).

VARIANTES Y RELACIONADOS
    - DP en árbol: para cada nodo, las dos ramas más profundas
      (sirve con pesos negativos y para «diámetro pasando por v»).
    - Excentricidad de todos los nodos: max(d(v, a), d(v, b)) con a, b los
      extremos del diámetro (tres recorridos en total).
    - Centroide (otra noción: minimiza el subárbol más grande al quitarlo).
    - bfs.py, lca.py, floyd_warshall.py (diámetro en grafos generales).

DÓNDE PRACTICAR
    - Ningún problema del repo usa el diámetro de un ÁRBOL (Colombia 2017 A
      usa el diámetro de un grafo general con Floyd–Warshall).
    - CSES «Tree Diameter», «Tree Distances I»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las distancias con un recorrido
      desde cada nodo; diámetro = máximo, centro = nodos de excentricidad
      mínima) en 1000 árboles aleatorios con y sin pesos (n ≤ 40), validando
      el camino devuelto; casos borde y un camino de 2·10^5 nodos
      (python diametro_arbol.py)
"""
import random


def _ady(n, aristas):
    ady = [[] for _ in range(n)]
    for a in aristas:
        u, v = a[0], a[1]
        w = a[2] if len(a) > 2 else 1
        ady[u].append((v, w))
        ady[v].append((u, w))
    return ady


def _recorrer(ady, s):
    """Distancias y padres desde s (en un árbol el camino es único: sirve una pila)."""
    n = len(ady)
    dist = [-1] * n
    padre = [-1] * n
    dist[s] = 0
    pila = [s]
    while pila:
        u = pila.pop()
        for v, w in ady[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                padre[v] = u
                pila.append(v)
    return dist, padre


def diametro(n, aristas):
    """(largo, u, v, camino) del camino más largo del árbol (pesos ≥ 0)."""
    ady = _ady(n, aristas)
    d0, _ = _recorrer(ady, 0)
    a = max(range(n), key=lambda x: d0[x])       # extremo de algún diámetro
    da, padre = _recorrer(ady, a)
    b = max(range(n), key=lambda x: da[x])
    camino = [b]
    while camino[-1] != a:                       # subir por padres de b hasta a
        camino.append(padre[camino[-1]])
    camino.reverse()
    return da[b], a, b, camino


def centro(n, aristas):
    """(centros, radio) de un árbol sin pesos, pelando hojas por rondas."""
    ady = [[] for _ in range(n)]
    for a in aristas:
        ady[a[0]].append(a[1])
        ady[a[1]].append(a[0])
    grado = [len(ady[v]) for v in range(n)]
    hojas = [v for v in range(n) if grado[v] <= 1]
    quedan = n
    radio = 0
    while quedan > 2:
        quedan -= len(hojas)
        nuevas = []
        for h in hojas:
            for v in ady[h]:
                grado[v] -= 1
                if grado[v] == 1:                # v se vuelve hoja en la ronda siguiente
                    nuevas.append(v)
        hojas = nuevas
        radio += 1
    if quedan == 2:
        radio += 1
    return sorted(hojas), radio


def demo():
    aristas = [(0, 1), (1, 2), (2, 3), (1, 4), (4, 5), (5, 6), (2, 7)]
    print("Diámetro:", diametro(8, aristas))     # (5, 6, 3, [6, 5, 4, 1, 2, 3])
    print("Centro:", centro(8, aristas))         # ([1, 4], 3)
    pesadas = [(0, 1, 4), (1, 2, 1), (1, 3, 10), (3, 4, 2)]
    print("Diámetro con pesos:", diametro(5, pesadas))   # (16, 4, 0, [4, 3, 1, 0])


def _todas_distancias(n, aristas):
    """Fuerza bruta: distancia entre todo par con un recorrido desde cada nodo."""
    ady = _ady(n, aristas)
    D = []
    for s in range(n):
        dist = {s: 0}
        pend = [s]
        while pend:
            u = pend.pop()
            for v, w in ady[u]:
                if v not in dist:
                    dist[v] = dist[u] + w
                    pend.append(v)
        D.append([dist[v] for v in range(n)])
    return D


def pruebas():
    random.seed(1859)

    # Casos borde
    assert diametro(1, []) == (0, 0, 0, [0]) and centro(1, []) == ([0], 0)
    assert diametro(2, [(0, 1)])[0] == 1 and centro(2, [(0, 1)]) == ([0, 1], 1)
    assert diametro(2, [(0, 1, 0)])[0] == 0                   # peso cero
    assert centro(5, [(0, i) for i in range(1, 5)]) == ([0], 1)   # estrella

    for caso in range(1000):
        n = random.randint(1, 40)
        con_peso = caso % 2 == 1
        aristas = []
        for v in range(1, n):
            u = random.randrange(v)
            aristas.append((u, v, random.randint(0, 20)) if con_peso else (u, v))
        etiqueta = list(range(n))
        random.shuffle(etiqueta)
        aristas = [(etiqueta[a[0]], etiqueta[a[1]]) + tuple(a[2:]) for a in aristas]
        D = _todas_distancias(n, aristas)
        largo, u, v, camino = diametro(n, aristas)
        assert largo == max(max(f) for f in D) == D[u][v]
        # el camino va de u a v, por aristas del árbol, y suma largo
        pesos = {}
        for a in aristas:
            w = a[2] if len(a) > 2 else 1
            pesos[(a[0], a[1])] = pesos[(a[1], a[0])] = w
        assert camino[0] == u and camino[-1] == v and len(set(camino)) == len(camino)
        assert sum(pesos[(camino[i], camino[i + 1])] for i in range(len(camino) - 1)) == largo
        if not con_peso:
            exc = [max(f) for f in D]
            r = min(exc)
            assert centro(n, aristas) == ([x for x in range(n) if exc[x] == r], r)
            assert r == (largo + 1) // 2

    # Grande: camino de 2·10^5 nodos (con DFS recursivo reventaría)
    N = 2 * 10 ** 5
    aristas = [(i, i + 1) for i in range(N - 1)]
    largo, u, v, camino = diametro(N, aristas)
    assert largo == N - 1 and {u, v} == {0, N - 1} and len(camino) == N
    assert centro(N, aristas) == ([N // 2 - 1, N // 2], N // 2)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
