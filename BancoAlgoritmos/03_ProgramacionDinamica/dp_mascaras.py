"""
Programación dinámica — DP sobre máscaras de bits: TSP y asignación («Bitmask DP»)
Nivel: Intermedio
Ejecutar: python dp_mascaras.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Cuando el estado natural es «qué SUBCONJUNTO de elementos ya usé» y n es
    pequeño (n ≤ 20 en C++, ≤ ~15–17 en Python), el subconjunto se guarda
    como un entero de n bits (máscara) y se hace DP sobre las 2^n máscaras.
    Dos clásicos:
      - Viajante (TSP): ciclo de costo mínimo que visita todas las ciudades
        exactamente una vez y vuelve al inicio.
      - Asignación: n trabajadores, n tareas, costo[i][j]; asignar a cada
        trabajador una tarea distinta con costo total mínimo.
    Señales: n ≤ 20, «visitar todos», «cada uno exactamente una vez»,
    «emparejar / repartir en grupos», donde probar las n! permutaciones es
    demasiado (12! ≈ 4,8·10^8) pero 2^n · n es poco.

FUNCIÓN
    tsp(dist) -> (int, list)
        Costo del ciclo mínimo que sale y vuelve a 0 y la ruta [0, …, 0].
        dist es una matriz n×n (puede ser asimétrica).
    asignacion(costo) -> (int, list)
        Costo mínimo y tarea[i] asignada a cada trabajador i.

IDEA Y ALGORITMO
    Máscara: el bit v de mask vale 1 si el elemento v está en el conjunto.
    mask >> v & 1 pregunta; mask | 1 << v agrega; bin(mask).count("1") = tamaño.
    TSP (Held–Karp):
      ESTADO      dp[mask][v] = costo mínimo de un camino que sale de 0,
                  visita exactamente las ciudades de mask y termina en v.
      TRANSICIÓN  ir de v a una ciudad u no visitada:
                  dp[mask | 1<<u][u] = min(…, dp[mask][v] + dist[v][u]).
      CASO BASE   dp[1][0] = 0 (solo la ciudad 0, parado en 0).
      ORDEN       máscaras crecientes: agregar un bit siempre da un número
                  mayor, así que los estados de origen ya están terminados.
      RESPUESTA   min_v dp[TODAS][v] + dist[v][0]; la ruta se reconstruye
                  con padre[mask][v].
      Por qué basta (mask, v): para continuar, lo único que importa del
      pasado es qué ciudades faltan y dónde estoy, no el orden en que se
      visitaron (n! órdenes colapsan en 2^n · n estados).
    Asignación:
      ESTADO      dp[mask] = costo mínimo de asignar las tareas de mask a
                  los trabajadores 0..k-1, con k = popcount(mask).
      TRANSICIÓN  el trabajador k toma una tarea j libre:
                  dp[mask | 1<<j] = min(…, dp[mask] + costo[k][j]).
      CASO BASE   dp[0] = 0.   ORDEN  máscaras crecientes.
      RESPUESTA   dp[TODAS]. No hace falta guardar el trabajador: lo da el
                  número de bits.

MACROALGORITMO
    1. dp de tamaño 2^n (× n en TSP) en infinito; caso base.
    2. Para mask = 0..2^n - 1 (creciente):
    3.    si el estado es alcanzable, probar cada elemento que falte y
          relajar el estado con ese bit agregado (guardar el padre).
    4. Leer la respuesta en la máscara llena; reconstruir hacia atrás.

COMPLEJIDAD
    TSP: O(2^n · n²) tiempo, O(2^n · n) memoria. En Python n ≤ ~14–15
    (15: 7·10^6 pasos, unos segundos).
    Asignación: O(2^n · n); n ≤ ~18–20 en Python. (Para n grande: algoritmo
    húngaro, O(n³).)

EJEMPLO A MANO
    dist = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
      dp[0011][1] = 10, dp[0101][2] = 15, dp[1001][3] = 20
      dp[1011][3] = dp[0011][1] + 25 = 35; dp[1111][2] = dp[1011][3] + 30 = 65
      ciclo 0 -> 1 -> 3 -> 2 -> 0 = 10 + 25 + 30 + 15 = 80.

ERRORES TÍPICOS
    - Precedencia: en Python «mask >> v & 1» es (mask >> v) & 1 (bien), pero
      «1 << n - 1» es 1 << (n - 1).
    - Olvidar cerrar el ciclo (+ dist[v][0]) o, si el problema pide camino
      (no ciclo), sumarlo de más.
    - n = 1 en TSP: el ciclo cuesta 0 (dist[0][0] si el enunciado lo pide).
    - Recorrer estados no alcanzables (infinito) gastando tiempo: saltarlos.
    - En Python, listas de listas de 2^n × n con n = 17 ya son ~2·10^6
      enteros: cuidado con la memoria.

VARIANTES Y RELACIONADOS
    - Camino hamiltoniano (sin volver), contar caminos hamiltonianos (CSES
      «Hamiltonian Flights»), repartir en grupos (dp[mask] sobre submáscaras:
      O(3^n)), «elemento libre más bajo» para no contar particiones repetidas.
    - sos_dp.py (sumas sobre subconjuntos), memoizacion.py (top-down sobre
      máscaras alcanzables), dp_perfil.py (máscara de una frontera).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/B - Forming Better Groups (DP sobre máscaras con
      «elemento libre más bajo»).
    - Externos: CSES «Hamiltonian Flights», «Elevator Rides»; AtCoder
      Educational DP Contest O «Matching» (asignación contando).

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las permutaciones, n ≤ 7) en
      300 casos de TSP y 300 de asignación + casos borde; se valida que la
      ruta/asignación reconstruida cueste el óptimo (python dp_mascaras.py)
"""
import itertools
import random


def tsp(dist):
    """(costo del ciclo mínimo desde 0, ruta [0, …, 0]) con Held–Karp."""
    n = len(dist)
    if n == 1:
        return 0, [0, 0]
    INF = float("inf")
    total = 1 << n
    dp = [[INF] * n for _ in range(total)]
    padre = [[-1] * n for _ in range(total)]
    dp[1][0] = 0                                    # solo la ciudad 0, parado en 0
    for mask in range(1, total, 2):                 # máscaras que contienen a 0
        fila = dp[mask]
        for v in range(n):
            d = fila[v]
            if d == INF:
                continue                            # estado no alcanzable
            dv = dist[v]
            for u in range(n):
                if mask >> u & 1:
                    continue                        # u ya visitada
                nm = mask | 1 << u
                if d + dv[u] < dp[nm][u]:
                    dp[nm][u] = d + dv[u]
                    padre[nm][u] = v
    llena = total - 1
    costo, ultimo = min((dp[llena][v] + dist[v][0], v) for v in range(1, n))
    ruta, mask, v = [], llena, ultimo
    while v != -1:                                  # retroceder por los padres
        ruta.append(v)
        mask, v = mask ^ (1 << v), padre[mask][v]
    ruta.reverse()
    ruta.append(0)
    return costo, ruta


def asignacion(costo):
    """(costo mínimo, tarea[i] de cada trabajador i). dp[mask] con k = popcount(mask)."""
    n = len(costo)
    INF = float("inf")
    dp = [INF] * (1 << n)
    eleccion = [-1] * (1 << n)                      # última tarea agregada
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        k = bin(mask).count("1")                    # siguiente trabajador
        if k == n:
            continue
        for j in range(n):
            if not mask >> j & 1:
                nm = mask | 1 << j
                if dp[mask] + costo[k][j] < dp[nm]:
                    dp[nm] = dp[mask] + costo[k][j]
                    eleccion[nm] = j
    tarea, mask = [0] * n, (1 << n) - 1
    for k in range(n - 1, -1, -1):                  # el trabajador k tomó eleccion[mask]
        j = eleccion[mask]
        tarea[k] = j
        mask ^= 1 << j
    return dp[(1 << n) - 1], tarea


def demo():
    dist = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
    print("TSP ->", tsp(dist))       # costo 80 (0-1-3-2-0, puede salir en el otro sentido)
    costo = [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]
    print("asignación ->", asignacion(costo))                    # (13, [1, 0, 2, 3])


def pruebas():
    random.seed(1218)

    # Casos borde
    assert tsp([[0]]) == (0, [0, 0])
    assert tsp([[0, 3], [5, 0]]) == (8, [0, 1, 0])
    assert asignacion([[4]]) == (4, [0])

    for _ in range(300):
        n = random.randint(2, 7)
        dist = [[0 if i == j else random.randint(1, 30) for j in range(n)] for i in range(n)]
        mejor = min(sum(dist[a][b] for a, b in zip((0,) + p, p + (0,)))
                    for p in itertools.permutations(range(1, n)))
        c, ruta = tsp(dist)
        assert c == mejor
        assert ruta[0] == ruta[-1] == 0 and sorted(ruta[:-1]) == list(range(n))
        assert sum(dist[a][b] for a, b in zip(ruta, ruta[1:])) == c

    for _ in range(300):
        n = random.randint(1, 7)
        costo = [[random.randint(0, 20) for _ in range(n)] for _ in range(n)]
        mejor = min(sum(costo[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
        c, tarea = asignacion(costo)
        assert c == mejor
        assert sorted(tarea) == list(range(n)) and sum(costo[i][tarea[i]] for i in range(n)) == c


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
