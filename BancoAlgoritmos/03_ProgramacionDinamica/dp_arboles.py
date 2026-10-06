"""
Programación dinámica — DP en árboles, iterativa («Tree DP / rerooting»)
Nivel: Intermedio
Ejecutar: python dp_arboles.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular algo para cada subárbol de un árbol combinando lo de sus hijos:
    tamaños, el conjunto independiente de peso máximo (elegir nodos sin
    elegir dos vecinos), emparejamientos, mochila en árbol… Y con
    «rerooting», calcular una respuesta para CADA posible raíz en O(n) en
    vez de O(n²) (p. ej. suma de distancias de cada nodo a todos los demás).
    Señales: «árbol / jerarquía / jefes y subordinados», «n - 1 aristas,
    conexo», «no elegir un nodo y su padre», «para cada nodo, …», n ≤ 2·10^5.

FUNCIÓN
    orden_dfs(n, ady, raiz=0) -> (orden, padre)
        Orden en que un DFS descubre los nodos (padres antes que hijos).
    tamanos_subarbol(n, aristas, raiz=0) -> list
    conjunto_independiente_maximo(n, aristas, peso=None) -> (int, list)
        Peso máximo y los nodos elegidos (peso por defecto 1 por nodo).
    suma_distancias(n, aristas) -> list
        res[v] = Σ_u dist(v, u) en aristas (rerooting, CSES «Tree Distances II»).
    Nodos 0..n-1; aristas = lista de pares (u, v).

IDEA Y ALGORITMO
    Iterativo: un DFS con pila da un orden donde cada padre aparece antes
    que sus hijos. Recorriendo ese orden AL REVÉS, cada hijo se procesa
    antes que su padre (orden «postorden»): ahí se hace la DP de abajo hacia
    arriba sin recursión (la recursión fallaría con un camino de 10^5 nodos).
    Tamaños:  sz[v] = 1 + Σ sz[hijos]  (caso base: hoja -> 1).
    Conjunto independiente máximo:
      ESTADO      dp0[v] / dp1[v] = mejor peso en el subárbol de v si v NO
                  está / SÍ está elegido.
      TRANSICIÓN  dp0[v] = Σ_hijos max(dp0[h], dp1[h]);
                  dp1[v] = peso[v] + Σ_hijos dp0[h] (un hijo de un elegido
                  no puede elegirse).
      CASO BASE   hoja: dp0 = 0, dp1 = peso.
      ORDEN       postorden (hijos antes que el padre).
      RESPUESTA   max(dp0[raiz], dp1[raiz]). Reconstrucción de arriba hacia
                  abajo: la raíz se elige si dp1 ≥ dp0; un hijo de elegido no
                  se elige; un hijo de no elegido se elige si dp1 ≥ dp0.
    Rerooting (suma de distancias):
      1. Hacia arriba (raíz 0): sz[v] y abajo[v] = Σ dist(v, u) con u en el
         subárbol de v: abajo[v] = Σ_hijos (abajo[h] + sz[h]) (cada nodo del
         subárbol de h queda 1 más lejos).
      2. Hacia abajo: res[0] = abajo[0]; al mover la raíz de v a un hijo h,
         los sz[h] nodos del subárbol de h quedan 1 más cerca y los n - sz[h]
         restantes 1 más lejos: res[h] = res[v] - sz[h] + (n - sz[h]).
      Orden: preorden (el padre antes que el hijo).

MACROALGORITMO
    1. Lista de adyacencia.
    2. DFS iterativo desde la raíz: orden y padre.
    3. Para v en orden invertido: combinar los valores de los hijos en v
       (o «empujar» v hacia su padre).
    4. (Rerooting) Para v en orden: calcular cada hijo a partir de v.
    5. (Reconstrucción) Para v en orden: decidir v según la decisión del padre.

COMPLEJIDAD
    O(n) tiempo y memoria en todas. n = 2·10^5 en ~0,5 s.

EJEMPLO A MANO
    Aristas 0-1, 0-2, 1-3, 1-4 (raíz 0), pesos 1:
      hojas 2, 3, 4: dp0 = 0, dp1 = 1
      nodo 1: dp0 = 1 + 1 = 2, dp1 = 1 + 0 + 0 = 1
      nodo 0: dp0 = max(2,1) + max(0,1) = 3, dp1 = 1 + 2 + 0 = 3 -> 3
      ({0, 3, 4} o {2, 3, 4}).
    Suma de distancias: abajo[0] = 6 (1+1+2+2); res[1] = 6 - 3 + 2 = 5.

ERRORES TÍPICOS
    - DFS recursivo en un árbol-camino de 10^5 nodos: RecursionError.
    - Olvidar no volver al padre al recorrer los vecinos.
    - En rerooting, actualizar res[h] antes de tener res[v] (usar preorden).
    - Mezclar «v elegido» con «v disponible» en la reconstrucción.

VARIANTES Y RELACIONADOS
    - Emparejamiento máximo en árbol (CSES «Tree Matching»), diámetro,
      mochila en árbol (dp[v][k] fusionando hijos: O(n²) total).
    - Rerooting general: guardar prefijos/sufijos de los hijos para excluir
      uno (cuando la combinación no es invertible, p. ej. máximo).
    - dp_dag.py (un árbol enraizado es un DAG).

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/G - FujikoMine (DP en árbol tipo mochila).
    - Externos: CSES «Subordinates», «Tree Matching», «Tree Distances I»,
      «Tree Distances II»; AtCoder Educational DP Contest P «Independent Set».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todos los subconjuntos para el
      conjunto independiente; BFS desde cada nodo para distancias; contar
      descendientes) en 400 árboles aleatorios + casos borde, y un camino
      de 10^5 nodos para probar que no hay recursión (python dp_arboles.py)
"""
import random
from collections import deque


def _adyacencia(n, aristas):
    ady = [[] for _ in range(n)]
    for u, v in aristas:
        ady[u].append(v)
        ady[v].append(u)
    return ady


def orden_dfs(n, ady, raiz=0):
    """Orden de descubrimiento (padres antes que hijos) y arreglo de padres."""
    padre = [-1] * n
    orden = []
    visto = [False] * n
    visto[raiz] = True
    pila = [raiz]
    while pila:
        v = pila.pop()
        orden.append(v)
        for u in ady[v]:
            if not visto[u]:
                visto[u] = True
                padre[u] = v
                pila.append(u)
    return orden, padre


def tamanos_subarbol(n, aristas, raiz=0):
    orden, padre = orden_dfs(n, _adyacencia(n, aristas), raiz)
    sz = [1] * n
    for v in reversed(orden):            # postorden: los hijos ya sumaron
        if padre[v] != -1:
            sz[padre[v]] += sz[v]
    return sz


def conjunto_independiente_maximo(n, aristas, peso=None):
    """(peso máximo de un conjunto sin vecinos elegidos, nodos elegidos)."""
    if peso is None:
        peso = [1] * n
    orden, padre = orden_dfs(n, _adyacencia(n, aristas))
    dp0 = [0] * n                        # v no elegido
    dp1 = list(peso)                     # v elegido (empieza con su peso)
    for v in reversed(orden):
        p = padre[v]
        if p != -1:                      # empujar el subárbol de v hacia el padre
            dp0[p] += max(dp0[v], dp1[v])
            dp1[p] += dp0[v]
    elegido = [False] * n
    for v in orden:                      # reconstrucción de arriba hacia abajo
        p = padre[v]
        if p != -1 and elegido[p]:
            elegido[v] = False           # su padre está: v no puede
        else:
            elegido[v] = dp1[v] >= dp0[v]
    raiz = orden[0]
    return max(dp0[raiz], dp1[raiz]), [v for v in range(n) if elegido[v]]


def suma_distancias(n, aristas):
    """res[v] = suma de distancias de v a todos los nodos (rerooting en O(n))."""
    orden, padre = orden_dfs(n, _adyacencia(n, aristas))
    sz = [1] * n
    abajo = [0] * n                      # suma de distancias dentro del subárbol
    for v in reversed(orden):
        p = padre[v]
        if p != -1:
            sz[p] += sz[v]
            abajo[p] += abajo[v] + sz[v]
    res = [0] * n
    res[orden[0]] = abajo[orden[0]]
    for v in orden[1:]:                  # preorden: el padre ya tiene su respuesta
        res[v] = res[padre[v]] - sz[v] + (n - sz[v])
    return res


def demo():
    n, aristas = 5, [(0, 1), (0, 2), (1, 3), (1, 4)]
    print("aristas", aristas)
    print("tamaños de subárbol (raíz 0):", tamanos_subarbol(n, aristas))     # [5, 3, 1, 1, 1]
    print("conjunto independiente máximo:", conjunto_independiente_maximo(n, aristas))  # 3
    print("suma de distancias:", suma_distancias(n, aristas))                # [6, 5, 9, 8, 8]


def pruebas():
    random.seed(1132)

    def arbol_aleatorio(n):
        etiqueta = list(range(n))
        random.shuffle(etiqueta)
        return [(etiqueta[i], etiqueta[random.randrange(i)]) for i in range(1, n)]

    def distancias_bfs(n, ady, s):
        d = [-1] * n
        d[s] = 0
        cola = deque([s])
        while cola:
            v = cola.popleft()
            for u in ady[v]:
                if d[u] < 0:
                    d[u] = d[v] + 1
                    cola.append(u)
        return d

    # Casos borde
    assert tamanos_subarbol(1, []) == [1]
    assert conjunto_independiente_maximo(1, [], [7]) == (7, [0])
    assert suma_distancias(1, []) == [0]
    assert suma_distancias(2, [(0, 1)]) == [1, 1]

    for _ in range(400):
        n = random.randint(1, 11)
        aristas = arbol_aleatorio(n)
        ady = _adyacencia(n, aristas)
        peso = [random.randint(0, 9) for _ in range(n)]
        # Conjunto independiente: todos los subconjuntos
        mejor = 0
        for mask in range(1 << n):
            if all(not (mask >> u & 1 and mask >> v & 1) for u, v in aristas):
                mejor = max(mejor, sum(peso[v] for v in range(n) if mask >> v & 1))
        valor, nodos = conjunto_independiente_maximo(n, aristas, peso)
        assert valor == mejor == sum(peso[v] for v in nodos)
        s = set(nodos)
        assert all(not (u in s and v in s) for u, v in aristas)
        # Distancias: BFS desde cada nodo
        dist = [distancias_bfs(n, ady, s) for s in range(n)]
        assert suma_distancias(n, aristas) == [sum(d) for d in dist]
        # Tamaños: u está en el subárbol de v (raíz r) si v está en el camino r..u
        r = random.randrange(n)
        sz = tamanos_subarbol(n, aristas, r)
        for v in range(n):
            assert sz[v] == sum(1 for u in range(n) if dist[r][v] + dist[v][u] == dist[r][u])

    # Camino largo: sin recursión
    n = 10**5
    camino = [(i, i + 1) for i in range(n - 1)]
    assert conjunto_independiente_maximo(n, camino)[0] == (n + 1) // 2
    assert suma_distancias(n, camino)[0] == n * (n - 1) // 2
    assert tamanos_subarbol(n, camino)[0] == n


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
