"""
Programación dinámica — Optimización divide y vencerás («Divide and conquer DP optimization»)
Nivel: Avanzado
Ejecutar: python dp_divide_venceras.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Acelerar DP de partición en K grupos de la forma
        dp[g][i] = min_{j < i} dp[g-1][j] + C(j, i)
    (partir los primeros i elementos en g grupos contiguos; el último grupo
    es a[j:i]) de O(K·n²) a O(K·n log n), cuando el corte óptimo es
    MONÓTONO: opt[g][i] ≤ opt[g][i+1].
    Ejemplo clásico (CSES «Subarray Squares»): partir un arreglo de n
    números no negativos en exactamente K subarreglos contiguos minimizando
    la suma de los cuadrados de las sumas de cada subarreglo.
    Señales: «dividir en K grupos/bloques/góndolas consecutivos», costo de
    un grupo que «crece más que lineal» con su tamaño, n ≤ ~10^4–10^5,
    K ≤ ~100 (K·n² demasiado).

FUNCIÓN
    particion_cuadrados(a, K) -> int        con divide y vencerás.
    particion_cuadrados_lenta(a, K) -> int  la DP O(K·n²), para comparar.
        Mínimo de Σ (suma del grupo)² partiendo a en K grupos NO vacíos
        (1 ≤ K ≤ len(a)), con a[i] ≥ 0.

IDEA Y ALGORITMO
    ESTADO      dp[g][i] = costo mínimo de partir a[:i] en g grupos.
    TRANSICIÓN  el último grupo es a[j:i] (j ≤ i-1, no vacío):
                dp[g][i] = min_j dp[g-1][j] + (pre[i] - pre[j])².
    CASOS BASE  dp[0][0] = 0; dp[0][i>0] = infinito.
    ORDEN       g creciente (cada capa solo usa la anterior).
    RESPUESTA   dp[K][n].
    Optimización: dentro de una capa g, sea opt(i) el j óptimo (el menor si
    hay empate). Si C cumple la desigualdad del cuadrángulo
        C(a, c) + C(b, d) ≤ C(a, d) + C(b, c)   para a ≤ b ≤ c ≤ d,
    entonces opt(i) ≤ opt(i+1). Intuición: si el último grupo de a[:i]
    empieza en j, alargar el prefijo nunca hace conveniente que el último
    grupo empiece más a la izquierda (sería un grupo aún más grande y
    cuadrático). Con (suma)² y valores ≥ 0 se cumple.
    Entonces se calcula la capa con «divide y vencerás»: calcular(lo, hi,
    optlo, opthi) halla dp[g][mid] para mid = (lo+hi)/2 probando j solo en
    [optlo, opthi] y luego resuelve [lo, mid-1] con j en [optlo, opt(mid)] y
    [mid+1, hi] con j en [opt(mid), opthi]. En cada nivel de la recursión
    los rangos de j se tocan solo en los extremos -> O(n) por nivel,
    O(log n) niveles.
    En el código, la recursión se reemplaza por una pila explícita.

MACROALGORITMO
    1. Sumas prefijas; capa anterior = [0, inf, inf, …].
    2. Para g = 1..K:
    3.    pila = [(1, n, 0, n-1)]; mientras haya: sacar (lo, hi, olo, ohi).
    4.    mid = (lo+hi)//2; probar j en [olo, min(mid-1, ohi)]; guardar el mejor
          valor en la capa nueva y su j.
    5.    apilar (lo, mid-1, olo, j*) y (mid+1, hi, j*, ohi).
    6. Respuesta: capa K en n.

COMPLEJIDAD
    O(K · n log n) tiempo, O(n) memoria (dos capas). En Python K·n·log n ≈
    3·10^6 en ~1–2 s (p. ej. n = 3000, K = 50).

EJEMPLO A MANO
    a = [2, 3, 1, 2, 2, 3], K = 3 (pre = 0 2 5 6 8 10 13)
      [2, 3] [1, 2] [2, 3]   -> 25 +  9 + 25 = 59   (óptima)
      [2, 3] [1, 2, 2] [3]   -> 25 + 25 +  9 = 59   (empata)
      [2, 3, 1] [2, 2] [3]   -> 36 + 16 +  9 = 61
    Capa g = 3, i = 6: la D&C prueba solo los j entre los opt de sus
    vecinos ya calculados en vez de los 5 posibles. Respuesta 59.

ERRORES TÍPICOS
    - Aplicarla sin que el óptimo sea monótono (verificar contra la lenta).
    - Rango de j mal cortado: el último grupo debe ser no vacío (j ≤ mid-1).
    - Cuando dp[g-1][j] es infinito para todos los j del rango, igual hay
      que propagar un opt razonable (aquí: optlo) para no romper los rangos.
    - Recursión de Python sin límite: la profundidad es log n, pero
      hacerlo con pila evita sorpresas.

VARIANTES Y RELACIONADOS
    - Knuth para partición: opt[g-1][i] ≤ opt[g][i] ≤ opt[g][i+1] da
      O(n²) total sin el log (optimizacion_knuth.py).
    - «Aliens trick» (relajación lagrangiana) para quitar la dimensión K.
    - convex_hull_trick.py cuando C(j, i) se separa en productos.
    - dp_particion_prefijos.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/E - Custom Keypad (misma forma dp[k][i] de partir
      en B bloques contiguos; allí n = 26 y basta la DP directa).
    - Externos: CSES «Subarray Squares»; Codeforces 321E «Ciel and Gondolas».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las formas de elegir K-1 cortes,
      n ≤ 9) en 400 casos y contra la DP O(K·n²) en 150 casos con n ≤ 60,
      + casos borde (python dp_divide_venceras.py)
"""
import itertools
import random


def particion_cuadrados(a, K):
    """Mínimo de Σ (suma del grupo)² en K grupos contiguos no vacíos, O(K n log n)."""
    n = len(a)
    pre = [0]
    for x in a:
        pre.append(pre[-1] + x)
    INF = float("inf")
    prev = [0] + [INF] * n                  # capa g = 0
    for _ in range(K):
        cur = [INF] * (n + 1)               # cur[0] = inf: 0 elementos no hacen g ≥ 1 grupos
        pila = [(1, n, 0, n - 1)]
        while pila:
            lo, hi, olo, ohi = pila.pop()
            if lo > hi:
                continue
            mid = (lo + hi) // 2
            mejor, mj = INF, olo
            for j in range(olo, min(mid - 1, ohi) + 1):   # último grupo a[j:mid], no vacío
                s = pre[mid] - pre[j]
                v = prev[j] + s * s
                if v < mejor:
                    mejor, mj = v, j
            cur[mid] = mejor
            pila.append((lo, mid - 1, olo, mj))           # a la izquierda: opt ≤ mj
            pila.append((mid + 1, hi, mj, ohi))           # a la derecha: opt ≥ mj
        prev = cur
    return prev[n]


def particion_cuadrados_lenta(a, K):
    """La DP directa O(K n²)."""
    n = len(a)
    pre = [0]
    for x in a:
        pre.append(pre[-1] + x)
    INF = float("inf")
    prev = [0] + [INF] * n
    for _ in range(K):
        cur = [INF] * (n + 1)
        for i in range(1, n + 1):
            cur[i] = min(prev[j] + (pre[i] - pre[j]) ** 2 for j in range(i))
        prev = cur
    return prev[n]


def demo():
    a, K = [2, 3, 1, 2, 2, 3], 3
    print("a =", a, "K =", K, "->", particion_cuadrados(a, K),
          "| lenta:", particion_cuadrados_lenta(a, K))                    # 59 59
    random.seed(7)
    b = [random.randint(1, 10**4) for _ in range(3000)]
    print("n = 3000, K = 50 ->", particion_cuadrados(b, 50))


def pruebas():
    random.seed(321)

    def bruta(a, K):
        n, mejor = len(a), None
        for cortes in itertools.combinations(range(1, n), K - 1):
            bordes = (0,) + cortes + (n,)
            v = sum(sum(a[bordes[t]:bordes[t + 1]]) ** 2 for t in range(K))
            if mejor is None or v < mejor:
                mejor = v
        return mejor

    # Casos borde
    assert particion_cuadrados([5], 1) == 25
    assert particion_cuadrados([1, 2, 3], 3) == 1 + 4 + 9
    assert particion_cuadrados([0, 0, 0, 0], 2) == 0
    assert particion_cuadrados([4, 4, 4, 4], 2) == 64 + 64

    for _ in range(400):
        n = random.randint(1, 9)
        a = [random.randint(0, 10) for _ in range(n)]
        K = random.randint(1, n)
        assert particion_cuadrados(a, K) == bruta(a, K) == particion_cuadrados_lenta(a, K)

    for _ in range(150):
        n = random.randint(1, 60)
        a = [random.randint(0, random.choice([1, 10, 1000])) for _ in range(n)]
        K = random.randint(1, n)
        assert particion_cuadrados(a, K) == particion_cuadrados_lenta(a, K)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
