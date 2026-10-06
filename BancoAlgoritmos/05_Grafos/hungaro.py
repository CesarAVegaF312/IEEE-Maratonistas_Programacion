"""
Grafos — Asignación de costo mínimo: algoritmo húngaro O(n³) («Hungarian algorithm»)
Nivel: Avanzado
Ejecutar: python hungaro.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Dada una matriz de costos a[i][j] (trabajador i hace la tarea j),
    asignar a cada fila una columna DISTINTA minimizando la suma de costos
    (o maximizando la ganancia, cambiando signos). Es el emparejamiento
    perfecto de peso mínimo en un grafo bipartito completo.
    Señales en el enunciado: «asignar cada uno a exactamente uno»,
    «emparejar n puntos con n puntos minimizando la distancia total»,
    «permutación que minimiza Σ a[i][p(i)]», n hasta ~300–500 (n! es
    imposible y la DP por máscaras solo llega a n ≈ 20).

FUNCIÓN
    hungaro(a) -> (costo, asignacion)
        a = matriz n × m (enteros o flotantes). Si n ≤ m, asignacion[i] es
        la columna de la fila i (todas distintas). Si n > m, se asignan solo
        m filas y las demás quedan con −1.
        costo = suma de a[i][asignacion[i]] de las filas asignadas.
    hungaro_max(a) -> (ganancia, asignacion)    versión de máximo

IDEA Y ALGORITMO
    Potenciales (dualidad): si u[i] + v[j] ≤ a[i][j] para todo i, j,
    entonces CUALQUIER asignación cuesta al menos Σu + Σv (sumar la
    desigualdad sobre las parejas elegidas). Si además se logra una
    asignación que usa solo casillas «apretadas» (u[i] + v[j] = a[i][j]),
    su costo es exactamente Σu + Σv: es óptima.
    El algoritmo agrega las filas una por una manteniendo esa invariante.
    Para meter la fila i busca un camino de aumento alternante hacia una
    columna libre, como un Dijkstra sobre costos reducidos
    a[i][j] − u[i] − v[j] ≥ 0: minv[j] = menor costo reducido para llegar
    a la columna j. En cada paso toma la columna j1 no usada con minv
    mínimo (delta) y ajusta potenciales: filas del árbol + delta, columnas
    del árbol − delta. Así las casillas del árbol siguen apretadas, j1 se
    vuelve apretada y ninguna desigualdad se rompe. Si j1 está libre, se
    voltea el camino (arreglo way) y la fila i quedó asignada.
    Cada fila cuesta O(n·m) → O(n²·m), es decir O(n³).
    Es lo mismo que el método «a mano» de restar mínimos de filas y
    columnas y cubrir ceros con líneas, pero sin reconstruir coberturas.
    Ingenuo: probar las n! permutaciones.

MACROALGORITMO
    1. u = v = 0; p[j] = fila asignada a la columna j (0 = libre; índices
       desde 1 y la columna 0 como «raíz» ficticia).
    2. Para cada fila i: p[0] = i, j0 = 0, minv = ∞, usada = falso.
    3. Repetir: marcar j0 usada; i0 = p[j0]; para cada columna j no usada
       actualizar minv[j] con a[i0][j] − u[i0] − v[j] (recordar way[j] = j0)
       y tomar la de minv mínimo (j1, delta).
    4. Ajustar: columnas usadas → u[p[j]] += delta, v[j] −= delta; no
       usadas → minv[j] −= delta. j0 = j1. Si p[j0] == 0 (libre), salir.
    5. Voltear el camino: mientras j0 ≠ 0, p[j0] = p[way[j0]], j0 = way[j0].
    6. asignacion[p[j] − 1] = j − 1 para cada columna j ocupada.

COMPLEJIDAD
    Tiempo O(n²·m) (O(n³) si es cuadrada), memoria O(n·m).
    En Python, n ≈ 200–300 en ~1 s (n = 500 ya tarda varios segundos).

EJEMPLO A MANO
    a = [[4, 1, 3],
         [2, 0, 5],
         [3, 2, 2]]
    Restar el mínimo de cada fila (1, 0, 2) y luego de cada columna (1, 0, 0):
         [[2, 0, 2], [1, 0, 5], [0, 0, 0]]  → potenciales u = (1,0,2),
    v = (1,0,0), cota inferior Σu + Σv = 4. Los ceros no alcanzan para una
    asignación (filas 0 y 1 solo tienen cero en la columna 1). Mínimo no
    cubierto por las líneas {columna 1, fila 2} = 1: se resta a lo no
    cubierto y se suma a la intersección → [[1,0,1],[0,0,4],[0,1,0]].
    Ceros independientes (0,1), (1,0), (2,2): costo 1 + 2 + 2 = 5 = cota.

ERRORES TÍPICOS
    - Mezclar índices: la implementación usa filas y columnas desde 1 (la
      columna 0 es la raíz ficticia); la entrada y la salida van desde 0.
    - Matriz con más filas que columnas: el algoritmo base exige n ≤ m
      (aquí se transpone).
    - Maximizar sin negar los costos (o negar y olvidar devolver −costo).
    - Usar un INF entero pequeño con costos grandes; con flotantes, el
      costo puede acumular error: comparar con tolerancia.
    - Querer usarlo con «aristas prohibidas»: ponerles un costo enorme y
      revisar al final si se usó alguna.

VARIANTES Y RELACIONADOS
    - Maximizar: hungaro_max (niega la matriz).
    - Flujo de costo mínimo: generaliza a capacidades y cupos (más lento).
    - DP sobre máscaras de bits para n ≤ 20 (O(2^n·n)).
    - emparejamiento_bipartito.py (sin pesos: solo cantidad máxima).

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/H - Match Points (asignación húngara con
      distancias euclidianas; el óptimo resulta sin cruces)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las asignaciones con
      itertools.permutations) en 1500 matrices aleatorias de hasta 6×6,
      cuadradas y rectangulares (n < m y n > m), enteras con negativos y
      flotantes (distancias euclidianas, tolerancia 1e-9), máximo y mínimo;
      casos borde y una matriz 150 × 150 (validez y cotas) (python hungaro.py)
"""
import itertools
import math
import random


def hungaro(a):
    """Asignación de costo mínimo. Devuelve (costo, asignacion) con asignacion[i] = columna o −1."""
    n = len(a)
    m = len(a[0]) if n else 0
    if n == 0 or m == 0:
        return 0, [-1] * n
    if n > m:
        # más filas que columnas: resolver la transpuesta y traducir
        costo, por_col = hungaro([list(col) for col in zip(*a)])
        asig = [-1] * n
        for j, i in enumerate(por_col):
            asig[i] = j
        return costo, asig
    INF = float("inf")
    u = [0] * (n + 1)          # potencial de cada fila (1..n)
    v = [0] * (m + 1)          # potencial de cada columna (1..m)
    p = [0] * (m + 1)          # p[j] = fila asignada a la columna j (0 = libre)
    way = [0] * (m + 1)        # columna anterior en el camino alternante
    for i in range(1, n + 1):
        p[0] = i               # la fila nueva cuelga de la columna ficticia 0
        j0 = 0
        minv = [INF] * (m + 1)
        usada = [False] * (m + 1)
        while True:
            usada[j0] = True
            i0 = p[j0]
            fila = a[i0 - 1]
            ui0 = u[i0]
            delta = INF
            j1 = 0
            for j in range(1, m + 1):
                if not usada[j]:
                    cur = fila[j - 1] - ui0 - v[j]      # costo reducido ≥ 0
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            # ajustar potenciales: el árbol sigue apretado y j1 se vuelve apretada
            for j in range(m + 1):
                if usada[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break          # columna libre: hay camino de aumento
        # voltear el camino alternante hasta la raíz
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    asig = [-1] * n
    for j in range(1, m + 1):
        if p[j]:
            asig[p[j] - 1] = j - 1
    costo = sum(a[i][asig[i]] for i in range(n))
    return costo, asig


def hungaro_max(a):
    """Asignación de ganancia máxima."""
    costo, asig = hungaro([[-x for x in fila] for fila in a])
    return -costo, asig


def demo():
    a = [[4, 1, 3],
         [2, 0, 5],
         [3, 2, 2]]
    print("Mínimo:", hungaro(a))        # (5, [1, 0, 2])
    print("Máximo:", hungaro_max(a))    # (11, [0, 2, 1]): 4 + 5 + 2
    puntos_o = [(0, 0), (4, 0)]
    puntos_x = [(4, 1), (0, 1)]
    dist = [[math.dist(o, x) for x in puntos_x] for o in puntos_o]
    print("Emparejar puntos (Colombia 2023 H):", hungaro(dist))   # (2.0, [1, 0])


def _bruto(a):
    n = len(a)
    m = len(a[0]) if n else 0
    if n == 0 or m == 0:
        return 0
    if n <= m:
        return min(sum(a[i][c[i]] for i in range(n))
                   for c in itertools.permutations(range(m), n))
    return min(sum(a[f[j]][j] for j in range(m))
               for f in itertools.permutations(range(n), m))


def _valida(a, costo, asig):
    n = len(a)
    m = len(a[0]) if n else 0
    usadas = [j for j in asig if j != -1]
    assert len(usadas) == len(set(usadas)) == min(n, m)
    assert all(0 <= j < m for j in usadas)
    assert abs(sum(a[i][asig[i]] for i in range(n) if asig[i] != -1) - costo) < 1e-9


def pruebas():
    random.seed(1955)

    # Casos borde
    assert hungaro([]) == (0, [])
    assert hungaro([[7]]) == (7, [0])
    assert hungaro([[5, 5], [5, 5]])[0] == 10
    assert hungaro([[1, 2, 3]]) == (1, [0])                 # una fila
    assert hungaro([[3], [1], [2]]) == (1, [-1, 0, -1])     # una columna
    assert hungaro([[10 ** 15, 1], [1, 10 ** 15]]) == (2, [1, 0])
    assert hungaro([[4, 1, 3], [2, 0, 5], [3, 2, 2]]) == (5, [1, 0, 2])

    # Aleatorios contra todas las permutaciones
    for caso in range(1500):
        n, m = random.randint(1, 6), random.randint(1, 6)
        if caso % 3 == 0:                                   # flotantes: distancias
            P = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(n)]
            Q = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(m)]
            a = [[math.dist(p, q) for q in Q] for p in P]
        else:
            a = [[random.randint(-20, 20) for _ in range(m)] for _ in range(n)]
        costo, asig = hungaro(a)
        _valida(a, costo, asig)
        assert abs(costo - _bruto(a)) < 1e-9
        g, asig = hungaro_max(a)
        _valida(a, g, asig)
        assert abs(g + _bruto([[-x for x in f] for f in a])) < 1e-9

    # Grande: 150 × 150 (fuerza bruta imposible): asignación válida, costo
    # ≥ Σ mínimos por fila y ≤ el de permutaciones aleatorias; mide el tiempo
    N = 150
    a = [[random.randint(0, 10 ** 6) for _ in range(N)] for _ in range(N)]
    costo, asig = hungaro(a)
    _valida(a, costo, asig)
    assert costo >= sum(min(f) for f in a)
    for _ in range(20):
        perm = random.sample(range(N), N)
        assert costo <= sum(a[i][perm[i]] for i in range(N))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
