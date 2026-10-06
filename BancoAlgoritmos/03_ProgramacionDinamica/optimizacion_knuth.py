"""
Programación dinámica — Optimización de Knuth para DP de intervalos («Knuth–Yao optimization»)
Nivel: Avanzado
Ejecutar: python optimizacion_knuth.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Bajar de O(n³) a O(n²) las DP de intervalos de la forma
        dp[i][j] = min_{i ≤ k < j} (dp[i][k] + dp[k+1][j]) + w(i, j)
    cuando el costo w cumple ciertas desigualdades. El clásico: hay n pilas
    en fila con a[i] objetos; unir dos pilas ADYACENTES cuesta la suma de
    ambas; unir todo en una pila con costo mínimo (visto al revés: partir
    una pila en dos cuesta su tamaño). Con n = 1000–5000, O(n³) no alcanza.
    Señales: DP de intervalos con «costo = suma del tramo» (o cualquier w
    monótono que cumpla el cuadrángulo), n hasta ~5000, árbol binario de
    búsqueda óptimo, cortar un palo en puntos dados.

FUNCIÓN
    unir_pilas_cubico(a) -> int   DP de intervalos directa, O(n³).
    unir_pilas_knuth(a) -> int    misma respuesta en O(n²).
        a: lista de enteros NO negativos (tamaños de las pilas, en orden).

IDEA Y ALGORITMO
    DP base (DP de intervalos):
      ESTADO      dp[i][j] = costo mínimo de unir las pilas i..j en una.
      TRANSICIÓN  la última unión junta [i..k] con [k+1..j]:
                  dp[i][j] = min_k dp[i][k] + dp[k+1][j] + suma(i..j).
      CASO BASE   dp[i][i] = 0.
      ORDEN       por largo creciente del intervalo.
      RESPUESTA   dp[0][n-1].
    Optimización: sea opt[i][j] el k que da el mínimo. Si w cumple
      (1) desigualdad del cuadrángulo: w(a,c) + w(b,d) ≤ w(a,d) + w(b,c)
          para a ≤ b ≤ c ≤ d, y
      (2) monotonía: w(b,c) ≤ w(a,d) para [b,c] ⊆ [a,d],
    entonces (Knuth 1971, Yao 1980) el corte óptimo es monótono:
          opt[i][j-1] ≤ opt[i][j] ≤ opt[i+1][j].
    Basta probar k en ese rango. Para un largo fijo, la suma de los tamaños
    de los rangos es telescópica: Σ_i (opt[i+1][j] - opt[i][j-1] + 1) =
    O(n), así que cada largo cuesta O(n) y el total es O(n²).
    w(i, j) = suma(i..j) con a ≥ 0 cumple ambas (con igualdad en (1)).
    Con números negativos la monotonía (2) puede fallar: no usar Knuth.

MACROALGORITMO
    1. Sumas prefijas para w(i, j) en O(1).
    2. dp[i][i] = 0, opt[i][i] = i.
    3. Para largo = 2..n, para cada i (j = i + largo - 1):
    4.    probar k desde opt[i][j-1] hasta opt[i+1][j] (sin pasar de j-1);
    5.    dp[i][j] = mejor + w(i, j); opt[i][j] = k del mejor (el primero).
    6. Respuesta dp[0][n-1].

COMPLEJIDAD
    Tiempo O(n²), memoria O(n²). En Python n = 1000 en ~1–2 s (n²/2 ≈
    5·10^5 intervalos con rangos cortos); la versión cúbica tardaría minutos.

EJEMPLO A MANO
    a = [4, 1, 3, 2] (prefijos 0 4 5 8 10)
      largo 2: dp[0][1]=5 (opt 0), dp[1][2]=4 (opt 1), dp[2][3]=5 (opt 2)
      largo 3: dp[0][2]: k ∈ [opt[0][1], opt[1][2]] = [0, 1]:
               k=0: 0 + 4 = 4; k=1: 5 + 0 = 5 -> 4 + 8 = 12 (opt 0)
               dp[1][3]: k ∈ [1, 2]: k=1: 0+5 = 5; k=2: 4+0 = 4 -> 4 + 6 = 10 (opt 2)
      largo 4: dp[0][3]: k ∈ [opt[0][2], opt[1][3]] = [0, 2]:
               k=0: 0+10; k=1: 5+5; k=2: 12+0 -> 10 + 10 = 20.

ERRORES TÍPICOS
    - Aplicarla sin verificar las condiciones (con valores negativos, con
      costos que no son del tipo «suma del intervalo»): da respuestas malas
      sin avisar. Probar contra la O(n³) en casos pequeños.
    - Olvidar inicializar opt[i][i] = i.
    - Confundirla con «unir piedras en círculo»: duplicar el arreglo y
      tomar el mínimo de los intervalos de largo n.
    - Usar listas de listas de Python para n = 5000: 2,5·10^7 casillas,
      demasiada memoria; en Python el límite práctico es n ≈ 2000.

VARIANTES Y RELACIONADOS
    - Árbol binario de búsqueda óptimo (frecuencias de acceso).
    - Knuth para partición en K grupos: opt[k-1][i] ≤ opt[k][i] ≤ opt[k][i+1].
    - Algoritmo de Garsia–Wachs para unir pilas en O(n log n).
    - dp_intervalos.py, dp_divide_venceras.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/I - Stack Solitaire (DP de intervalos con
      optimización de Knuth; es exactamente este problema).
    - Externos: UVa 10003 «Cutting Sticks» (Knuth aplica).

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (probar todas las secuencias de
      uniones, n ≤ 7) en 300 casos, contra la O(n³) en 200 casos con n ≤ 40,
      + casos borde (python optimizacion_knuth.py)
"""
import random
import time


def unir_pilas_cubico(a):
    """DP de intervalos directa, O(n³)."""
    n = len(a)
    if n <= 1:
        return 0
    pre = [0]
    for x in a:
        pre.append(pre[-1] + x)
    dp = [[0] * n for _ in range(n)]
    for largo in range(2, n + 1):
        for i in range(n - largo + 1):
            j = i + largo - 1
            dp[i][j] = min(dp[i][k] + dp[k + 1][j] for k in range(i, j)) + pre[j + 1] - pre[i]
    return dp[0][n - 1]


def unir_pilas_knuth(a):
    """Misma DP con la optimización de Knuth: k solo en [opt[i][j-1], opt[i+1][j]]."""
    n = len(a)
    if n <= 1:
        return 0
    pre = [0]
    for x in a:
        pre.append(pre[-1] + x)
    dp = [[0] * n for _ in range(n)]
    opt = [[0] * n for _ in range(n)]
    for i in range(n):
        opt[i][i] = i                                   # caso base del corte óptimo
    for largo in range(2, n + 1):
        for i in range(n - largo + 1):
            j = i + largo - 1
            fila_i = dp[i]
            mejor, mk = None, -1
            for k in range(opt[i][j - 1], min(opt[i + 1][j], j - 1) + 1):
                c = fila_i[k] + dp[k + 1][j]
                if mejor is None or c < mejor:
                    mejor, mk = c, k
            dp[i][j] = mejor + pre[j + 1] - pre[i]
            opt[i][j] = mk
    return dp[0][n - 1]


def demo():
    a = [4, 1, 3, 2]
    print("a =", a, "-> cúbico", unir_pilas_cubico(a), "| Knuth", unir_pilas_knuth(a))   # 20 20
    random.seed(1)
    b = [random.randint(1, 100) for _ in range(250)]
    t0 = time.perf_counter()
    r1 = unir_pilas_cubico(b)
    t1 = time.perf_counter()
    r2 = unir_pilas_knuth(b)
    t2 = time.perf_counter()
    print(f"n = 250: cúbico {r1} en {t1 - t0:.2f} s | Knuth {r2} en {t2 - t1:.2f} s")


def pruebas():
    random.seed(2023)

    def bruta(pilas):
        """Probar TODAS las secuencias de uniones de vecinos."""
        if len(pilas) <= 1:
            return 0
        mejor = None
        for k in range(len(pilas) - 1):
            unida = pilas[k] + pilas[k + 1]
            c = unida + bruta(pilas[:k] + [unida] + pilas[k + 2:])
            if mejor is None or c < mejor:
                mejor = c
        return mejor

    # Casos borde
    assert unir_pilas_knuth([]) == unir_pilas_knuth([7]) == 0
    assert unir_pilas_knuth([3, 4]) == 7
    assert unir_pilas_knuth([0, 0, 0]) == 0
    assert unir_pilas_knuth([5] * 8) == unir_pilas_cubico([5] * 8) == 5 * 8 * 3

    for _ in range(300):
        a = [random.randint(0, 20) for _ in range(random.randint(1, 7))]
        assert unir_pilas_knuth(a) == unir_pilas_cubico(a) == bruta(a)

    for _ in range(200):
        tope = random.choice([1, 5, 1000])
        a = [random.randint(0, tope) for _ in range(random.randint(1, 40))]
        assert unir_pilas_knuth(a) == unir_pilas_cubico(a)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
