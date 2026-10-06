"""
Grafos — Camino y circuito euleriano con Hierholzer («Eulerian path / circuit»)
Nivel: Avanzado
Ejecutar: python euler_hierholzer.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Recorrer TODAS las aristas de un grafo exactamente una vez (camino
    euleriano), volviendo al inicio si se pide un circuito. Se decide con
    una condición sobre los grados y se construye en O(N + M).
    Señales en el enunciado: «usar cada ficha/palabra/calle una sola vez»,
    «encadenar palabras donde la última letra de una es la primera de la
    siguiente», «dibujar sin levantar el lápiz», «la cadena más corta que
    contiene todas las subcadenas de largo k» (De Bruijn). OJO: si piden
    pasar por cada VÉRTICE una vez es camino hamiltoniano (NP-difícil),
    otra cosa muy distinta.

FUNCIÓN
    euler_dirigido(n, aristas)    -> (vertices, ids) | None
    euler_no_dirigido(n, aristas) -> (vertices, ids) | None
        aristas[k] = (u, v), vértices 0..n-1; se permiten lazos y aristas
        repetidas (multigrafo).
        vertices = recorrido v0, v1, …, vm (m + 1 vértices);
        ids      = índices de las aristas en el orden en que se usan (m).
        Si existe CIRCUITO lo devuelve (vertices[0] == vertices[-1]); si
        solo hay camino, arranca en el vértice obligado. None si no existe.
        Con m = 0 devuelve ([0], []) (o ([], []) si n = 0).

IDEA Y ALGORITMO
    Condiciones de existencia (todas las aristas deben estar en una misma
    componente conexa; los vértices aislados no importan):
      - Dirigido, circuito: grado_entrada == grado_salida en todo vértice.
      - Dirigido, camino: además se permite UN vértice con sal − ent = 1
        (el inicio) y UNO con ent − sal = 1 (el final).
      - No dirigido, circuito: todos los grados pares.
      - No dirigido, camino: exactamente 0 o 2 vértices de grado impar
        (si son 2, el camino va de uno al otro).
    Por qué: cada vez que el recorrido pasa por un vértice intermedio entra
    y sale, gastando una arista de entrada y una de salida (o 2 del grado);
    solo el inicio y el final pueden quedar desbalanceados.
    Hierholzer: caminar desde el inicio gastando aristas sin repetir hasta
    trabarse. Con los grados balanceados uno solo se traba en el vértice
    final, pero puede dejar ciclos sin recorrer colgando de vértices del
    camino. La versión con pila lo arregla sola: se avanza mientras el
    vértice del tope tenga aristas sin usar; cuando no tiene, se saca y se
    agrega a la respuesta. Así los ciclos pendientes se «empalman» en el
    punto donde cuelgan. La respuesta sale al revés y se invierte.
    La conexidad se verifica al final: si el recorrido no usó las M
    aristas, había aristas en otra componente y no hay solución.
    Cada arista se mira O(1) veces gracias a un puntero por vértice
    (no se borra de listas: se avanza el puntero). En no dirigido cada
    arista aparece en las listas de sus dos extremos y se marca «usada».

MACROALGORITMO
    1. Calcular grados (ent/sal en dirigido; grado en no dirigido).
    2. Revisar la condición y elegir el inicio: el vértice con sal − ent = 1
       (o uno de grado impar); si todo está balanceado, cualquiera con aristas.
    3. pila = [inicio]. Mientras haya pila: v = tope.
    4. Si v tiene una arista sin usar (puntero), marcarla y apilar su otro
       extremo (con el id de la arista).
    5. Si no, sacar v de la pila y agregarlo a la respuesta.
    6. Invertir la respuesta; si tiene menos de M + 1 vértices → None.

COMPLEJIDAD
    Tiempo O(N + M), memoria O(N + M). En Python ~10^6 aristas en 1–2 s.

EJEMPLO A MANO
    Dirigido, n = 4: aristas 0:(0→1) 1:(1→2) 2:(2→0) 3:(0→3) 4:(3→0).
    Todo balanceado → circuito desde 0. Pila: 0 →(a0) 1 →(a1) 2 →(a2) 0
    →(a3) 3 →(a4) 0. El 0 ya no tiene aristas: se van sacando 0,3,0,2,1,0.
    Invertido: 0 1 2 0 3 0 con aristas 0,1,2,3,4.
    Si se hubiera ido primero por 0→3→0, el ciclo 0→1→2→0 quedaría colgando
    y la pila lo empalma igual.

ERRORES TÍPICOS
    - Olvidar revisar la conexidad (grados perfectos pero dos componentes).
    - Arrancar en un vértice cualquiera cuando hay desbalance: el inicio
      debe ser el de sal − ent = 1 (o un vértice de grado impar).
    - En no dirigido, usar la misma arista dos veces (una desde cada
      extremo) por no marcarla como usada por id.
    - Borrar aristas de listas con list.remove (O(grado) cada vez): usar un
      puntero por vértice.
    - Versión recursiva: con 10^5 aristas revienta la pila de Python.

VARIANTES Y RELACIONADOS
    - Recorrido lexicográficamente menor: ordenar las aristas de cada
      vértice y tomar siempre la menor disponible (OMP 2017 F).
    - Secuencias de De Bruijn: circuito euleriano en el grafo cuyos nodos
      son las palabras de largo k − 1.
    - Mínimas aristas a repetir para recorrer todo («cartero chino»).
    - dfs.py, componentes_conexas.py, scc.py.

DÓNDE PRACTICAR
    - ICPC/OMP 2017 Murcia/F - Chained Words (circuito euleriano dirigido,
      lexicográficamente menor)
    - ICPC/Colombia 2023/A - ASP (circuito euleriano en el dirigido
      completo: longitud N(N−1)+1)
    - CSES «Mail Delivery», «Teleporters Path», «De Bruijn Sequence»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (backtracking sobre todas las formas
      de recorrer las aristas) en 1200 multigrafos aleatorios dirigidos y
      no dirigidos con m ≤ 7; se valida que el recorrido use cada arista
      una vez y que sea circuito cuando existe uno; casos borde, el
      dirigido completo de ASP y multigrafos de 2·10^5 aristas
      (python euler_hierholzer.py)
"""
import random


def euler_dirigido(n, aristas):
    """Camino/circuito euleriano dirigido: (vertices, ids) o None."""
    m = len(aristas)
    if m == 0:
        return ([0], []) if n else ([], [])
    ady = [[] for _ in range(n)]          # ady[u] = ids de aristas que salen de u
    ent = [0] * n
    sal = [0] * n
    for k, (u, v) in enumerate(aristas):
        ady[u].append(k)
        sal[u] += 1
        ent[v] += 1
    # Condición de grados y elección del inicio
    inicio = aristas[0][0]               # si todo está balanceado: cualquiera con aristas
    extra_ini = extra_fin = 0
    for v in range(n):
        d = sal[v] - ent[v]
        if d == 1:
            extra_ini += 1
            inicio = v
        elif d == -1:
            extra_fin += 1
        elif d != 0:
            return None
    if (extra_ini, extra_fin) not in ((0, 0), (1, 1)):
        return None
    # Hierholzer iterativo
    ptr = [0] * n                        # siguiente arista sin usar de cada vértice
    pila = [(inicio, -1)]                # (vértice, arista con la que se llegó)
    vertices, ids = [], []
    while pila:
        v, e = pila[-1]
        if ptr[v] < len(ady[v]):
            k = ady[v][ptr[v]]
            ptr[v] += 1
            pila.append((aristas[k][1], k))
        else:                            # v sin aristas: entra a la respuesta
            pila.pop()
            vertices.append(v)
            if e != -1:
                ids.append(e)
    if len(ids) != m:                    # quedaron aristas en otra componente
        return None
    vertices.reverse()
    ids.reverse()
    return vertices, ids


def euler_no_dirigido(n, aristas):
    """Camino/circuito euleriano no dirigido: (vertices, ids) o None."""
    m = len(aristas)
    if m == 0:
        return ([0], []) if n else ([], [])
    ady = [[] for _ in range(n)]          # ady[u] = (vecino, id)
    grado = [0] * n
    for k, (u, v) in enumerate(aristas):
        ady[u].append((v, k))
        ady[v].append((u, k))             # un lazo queda dos veces en ady[u]
        grado[u] += 1
        grado[v] += 1
    impares = [v for v in range(n) if grado[v] % 2]
    if len(impares) not in (0, 2):
        return None
    inicio = impares[0] if impares else aristas[0][0]
    usada = [False] * m
    ptr = [0] * n
    pila = [(inicio, -1)]
    vertices, ids = [], []
    while pila:
        v, e = pila[-1]
        # saltar aristas ya usadas desde el otro extremo
        while ptr[v] < len(ady[v]) and usada[ady[v][ptr[v]][1]]:
            ptr[v] += 1
        if ptr[v] < len(ady[v]):
            w, k = ady[v][ptr[v]]
            ptr[v] += 1
            usada[k] = True
            pila.append((w, k))
        else:
            pila.pop()
            vertices.append(v)
            if e != -1:
                ids.append(e)
    if len(ids) != m:
        return None
    vertices.reverse()
    ids.reverse()
    return vertices, ids


def demo():
    aristas = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 0)]
    print("Dirigido:", euler_dirigido(4, aristas))     # ([0,1,2,0,3,0], [0,1,2,3,4])
    print("Solo camino (3→0 quitada):", euler_dirigido(4, aristas[:4]))
    # Casa con techo (5 vértices, 8 aristas): dos impares → camino de 3 a 4
    casa = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3), (2, 4), (3, 4)]
    print("Casa sin levantar el lápiz:", euler_no_dirigido(5, casa)[0])
    # ASP (Colombia 2023 A): dirigido completo sin lazos con N = 3
    N = 3
    completo = [(x, y) for x in range(N) for y in range(N) if x != y]
    vs, _ = euler_dirigido(N, completo)
    print("ASP N=3, palabra de largo", len(vs), ":", "".join("abc"[v] for v in vs))


# ---------- pruebas ----------

def _valida(n, aristas, res, dirigido):
    """El recorrido usa cada arista una vez y es consecutivo."""
    vs, ids = res
    m = len(aristas)
    assert len(ids) == m and sorted(ids) == list(range(m)) and len(vs) == m + 1
    for t, k in enumerate(ids):
        u, v = aristas[k]
        a, b = vs[t], vs[t + 1]
        assert (a, b) == (u, v) or (not dirigido and (a, b) == (v, u))


def _fuerza_bruta(n, aristas, dirigido):
    """(existe camino, existe circuito) por backtracking sobre las aristas."""
    m = len(aristas)
    usada = [False] * m
    hallado = [False, False]

    def ir(v, ini, cuantas):            # recursión de profundidad ≤ m ≤ 7
        if hallado[1]:                  # ya hay circuito (y por tanto camino)
            return
        if cuantas == m:
            hallado[0] = True
            if v == ini:
                hallado[1] = True
            return
        for k in range(m):
            if usada[k]:
                continue
            u, w = aristas[k]
            for a, b in ((u, w), (w, u)) if not dirigido else ((u, w),):
                if a == v:
                    usada[k] = True
                    ir(b, ini, cuantas + 1)
                    usada[k] = False

    for s in range(n):
        ir(s, s, 0)
    return hallado


def pruebas():
    random.seed(4242)

    # Casos borde
    assert euler_dirigido(0, []) == ([], []) and euler_no_dirigido(3, []) == ([0], [])
    assert euler_dirigido(1, [(0, 0)]) == ([0, 0], [0])               # lazo
    assert euler_no_dirigido(1, [(0, 0), (0, 0)])[0] == [0, 0, 0]
    assert euler_dirigido(2, [(0, 1), (0, 1)]) is None                 # sal(0) − ent(0) = 2
    assert euler_no_dirigido(2, [(0, 1), (0, 1)])[0] in ([0, 1, 0], [1, 0, 1])
    assert euler_dirigido(4, [(0, 1), (2, 3)]) is None                 # grados bien, desconexo
    assert euler_no_dirigido(4, [(0, 1), (1, 0), (2, 3), (3, 2)]) is None
    assert euler_dirigido(3, [(0, 1), (1, 2)]) == ([0, 1, 2], [0, 1])

    # Aleatorios contra backtracking (multigrafos con lazos)
    for dirigido in (True, False):
        f = euler_dirigido if dirigido else euler_no_dirigido
        for _ in range(600):
            n = random.randint(1, 5)
            m = random.randint(1, 7)
            aristas = [(random.randrange(n), random.randrange(n)) for _ in range(m)]
            camino, circuito = _fuerza_bruta(n, aristas, dirigido)
            res = f(n, aristas)
            assert (res is not None) == camino
            if res is not None:
                _valida(n, aristas, res, dirigido)
                # si existe circuito, debe devolver un circuito
                assert (res[0][0] == res[0][-1]) == circuito

    # ASP: dirigido completo sin lazos → circuito de N(N−1) aristas
    for N in range(2, 12):
        completo = [(x, y) for x in range(N) for y in range(N) if x != y]
        vs, ids = euler_dirigido(N, completo)
        assert len(vs) == N * (N - 1) + 1 and vs[0] == vs[-1]
        _valida(N, completo, (vs, ids), True)

    # Grandes: un paseo cerrado aleatorio de 2·10^5 pasos define un multigrafo
    # euleriano; se desordenan las aristas y se reconstruye
    n, M = 1000, 2 * 10 ** 5
    paseo = [0]
    for _ in range(M - 1):
        paseo.append(random.randrange(n))
    paseo.append(0)
    aristas = [(paseo[i], paseo[i + 1]) for i in range(M)]
    random.shuffle(aristas)
    for dirigido, f in ((True, euler_dirigido), (False, euler_no_dirigido)):
        res = f(n, aristas)
        assert res is not None and res[0][0] == res[0][-1]
        _valida(n, aristas, res, dirigido)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
