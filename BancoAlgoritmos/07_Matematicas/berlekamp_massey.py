"""
Matemáticas — Berlekamp–Massey: la recurrencia lineal mínima de una sucesión mód p
Nivel: Avanzado
Ejecutar: python berlekamp_massey.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Dados los primeros N términos s_0..s_{N−1} de una sucesión (mód p
    primo), encontrar la recurrencia lineal MÁS CORTA
        s_i = c_1·s_{i−1} + … + c_L·s_{i−L}    (para todo L ≤ i < N)
    en O(N²). Si se sabe que la sucesión cumple alguna recurrencia de orden
    ≤ k, con N ≥ 2k términos BM la encuentra exactamente; después Kitamasa
    da el término 10^18.
    Cómo reconocerlo: la respuesta es una DP con transición lineal fija
    (matriz de transferencia, caminos en un grafo, conteo de embaldosados)
    con MUCHOS estados pero se pide n gigante: se generan los primeros
    ~2·(número de estados) términos con la DP lenta y BM encuentra la
    recurrencia, normalmente mucho más corta que la matriz. También para
    «adivinar» la fórmula de una sucesión.

FUNCIÓN
    berlekamp_massey(s, p) -> list
        Devuelve coefs = [c_1, …, c_L] (L mínimo) mód p. L = 0 ([]) si la
        sucesión es toda cero.
    termino_n(coefs, s, n, p) -> int
        f(n) con esa recurrencia y los primeros términos de s (Kitamasa
        copiado en versión corta, O(L² log n)).

IDEA Y ALGORITMO
    Se procesa un término a la vez manteniendo la recurrencia más corta C
    (como polinomio C(x) = 1 − c_1 x − … − c_L x^L) que genera lo visto.
    Al llegar s_n se calcula la DISCREPANCIA
        d = s_n − Σ_{i=1}^{L} c_i s_{n−i}.
    Si d = 0, C sigue sirviendo. Si no, se corrige con la última recurrencia
    B que falló (la que había antes del último cambio de largo, con su
    discrepancia b, ocurrida m pasos atrás):
        C(x) ← C(x) − (d / b) · x^m · B(x).
    Por qué funciona: x^m·B(x) aplicado a la sucesión da 0 en las
    posiciones anteriores (B generaba hasta donde falló) y da exactamente b
    en la posición n; restando d/b veces se anula la discrepancia sin
    estropear los términos anteriores (todo es lineal).
    Minimalidad (teorema de Massey): si una recurrencia de largo L genera
    s_0..s_{n−1} pero no s_n, toda recurrencia que genere s_0..s_n tiene
    largo ≥ n + 1 − L. Por eso, cuando 2L ≤ n el largo nuevo es n + 1 − L
    (no se puede menos) y en otro caso se conserva L.
    Garantía: si la sucesión real cumple una recurrencia de orden k y N ≥ 2k,
    la recurrencia hallada es la verdadera (dos recurrencias de orden ≤ k
    que coinciden en 2k términos generan la misma sucesión).

MACROALGORITMO
    1. C = [1], B = [1], L = 0, m = 1, b = 1.
    2. Para cada n: d = s_n + Σ_{i=1}^{L} C[i]·s_{n−i} (C guarda −c_i).
    3. Si d = 0: m += 1.
    4. Si d ≠ 0 y 2L ≤ n: guardar T = C; C −= (d/b)·x^m·B; L = n + 1 − L;
       B = T; b = d; m = 1.
    5. Si d ≠ 0 y 2L > n: C −= (d/b)·x^m·B; m += 1.
    6. Devolver c_i = −C[i] para i = 1..L.
    7. (Uso típico) generar 2k + 10 términos con una DP, BM, y Kitamasa
       para el término pedido.

COMPLEJIDAD
    O(N²) tiempo, O(N) memoria (N = 2000 términos ≈ 1 s en Python).
    La recurrencia hallada puede ser mucho más corta que el número de
    estados de la DP (en Guangzhou E: 187 estados → orden 76).

EJEMPLO A MANO
    s = 0, 1, 1, 2, 3, 5 (mód p grande); C = 1, B = 1, L = 0, m = 1, b = 1.
    n=0: d = 0 → m = 2.
    n=1: d = 1; 2L ≤ 1 → C = 1 − 1·x²·B = 1 − x², L = 2, B = 1, b = 1, m = 1.
    n=2: d = s2 − s0 = 1; 2L > 2 → C = (1 − x²) − x·B = 1 − x − x², m = 2.
    n=3,4,5: d = 2−1−1 = 0, 3−2−1 = 0, 5−3−2 = 0.
    Resultado C = 1 − x − x²: s_i = s_{i−1} + s_{i−2}, L = 2.
    Para s_i = i² (0, 1, 4, 9, 16, 25, 36): L = 3, coefs = [3, −3, 1]
    (s_i = 3s_{i−1} − 3s_{i−2} + s_{i−3}, la tercera diferencia es 0).

ERRORES TÍPICOS
    - Dar menos de 2k términos: la recurrencia sale corta y equivocada.
    - Usarlo con flotantes o con módulo NO primo (hace falta dividir por b).
    - Confundir el signo: el polinomio C guarda −c_i.
    - Generar los términos iniciales con una DP que ya está mal indexada
      (BM «encuentra» una recurrencia para cualquier cosa).
    - Si la respuesta mód p no es una recurrencia lineal (p.ej. depende de
      n de forma no lineal, como n!), BM devuelve un L ≈ N/2: señal de alerta.

VARIANTES Y RELACIONADOS
    - kitamasa.py (siguiente paso: el término n), exponenciacion_matrices.py.
    - Sucesiones que cumplen recurrencias: Σ de polinomios en n, número de
      caminos en grafos, coeficientes de P(x)/Q(x) (funciones_generatrices.py),
      determinantes/potencias de matrices (Cayley–Hamilton).
    - Polinomio mínimo de una matriz dispersa (algoritmo de Wiedemann).

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/E - Easy Tiling Problem (matriz de transferencia
      de 187 estados → BM → recurrencia de orden 76 → Kitamasa)

VERIFICACIÓN
    - Pruebas: OK con 400 recurrencias aleatorias (orden ≤ 8) recuperadas
      con 2k términos y comprobadas en 3k términos; minimalidad contra
      fuerza bruta (probar todas las recurrencias de cada largo) en 300
      sucesiones aleatorias mód 2 y mód 3 de largo ≤ 7; termino_n contra
      iteración (python berlekamp_massey.py)
"""
import itertools
import random

MOD = 1_000_000_007


def berlekamp_massey(s, p=MOD):
    """Recurrencia lineal mínima [c_1..c_L] de s (mód p primo)."""
    C = [1]          # recurrencia actual como polinomio: 1 + C[1]x + … (C[i] = −c_i)
    B = [1]          # recurrencia anterior al último cambio de largo
    L, m, b = 0, 1, 1
    for n in range(len(s)):
        # discrepancia entre s_n y lo que predice C
        d = s[n] % p
        for i in range(1, L + 1):
            d = (d + C[i] * s[n - i]) % p
        if d == 0:
            m += 1
            continue
        coef = d * pow(b, p - 2, p) % p
        T = C[:]
        if len(C) < len(B) + m:
            C += [0] * (len(B) + m - len(C))
        for i, bi in enumerate(B):                    # C −= coef · x^m · B
            C[i + m] = (C[i + m] - coef * bi) % p
        if 2 * L <= n:
            L = n + 1 - L                             # el largo debe crecer
            B, b, m = T, d, 1
        else:
            m += 1
    C += [0] * (L + 1 - len(C))
    return [(-C[i]) % p for i in range(1, L + 1)]


def termino_n(coefs, s, n, p=MOD):
    """f(n) para la recurrencia coefs y valores iniciales s[0..L-1] (Kitamasa corto)."""
    k = len(coefs)
    if n < len(s) or k == 0:
        return s[n] % p if n < len(s) else 0

    def mul(a, b):
        prod = [0] * (2 * k - 1)
        for i, ai in enumerate(a):
            for j, bj in enumerate(b):
                prod[i + j] += ai * bj
        for i in range(2 * k - 2, k - 1, -1):         # x^k ≡ Σ c_j x^(k-j)
            t = prod[i] % p
            for j in range(1, k + 1):
                prod[i - j] += t * coefs[j - 1]
            prod[i] = 0
        return [v % p for v in prod[:k]]

    r = [1] + [0] * (k - 1)
    base = [coefs[0] % p] if k == 1 else [0, 1] + [0] * (k - 2)
    e = n
    while e:
        if e & 1:
            r = mul(r, base)
        base = mul(base, base)
        e >>= 1
    return sum(r[j] * s[j] for j in range(k)) % p


def _genera(coefs, ini, N, p):
    f = list(ini)
    k = len(coefs)
    while len(f) < N:
        i = len(f)
        f.append(sum(coefs[j] * f[i - 1 - j] for j in range(k)) % p)
    return f[:N]


def _largo_minimo_bruto(s, p):
    """Menor L tal que existe c ∈ Z_p^L con s_i = Σ c_j s_{i-j} para L ≤ i < N."""
    N = len(s)
    for L in range(0, N + 1):
        for c in itertools.product(range(p), repeat=L):
            if all(s[i] == sum(c[j] * s[i - 1 - j] for j in range(L)) % p for i in range(L, N)):
                return L
    return N


def demo():
    fib = [0, 1, 1, 2, 3, 5, 8, 13]
    print("Fibonacci:", berlekamp_massey(fib))                          # [1, 1]
    cuadrados = [i * i for i in range(10)]
    c = berlekamp_massey(cuadrados)
    print("i^2:", [x if x < MOD // 2 else x - MOD for x in c])          # [3, -3, 1]
    print("(10^6)^2 mód p por la recurrencia:", termino_n(c, cuadrados, 10**6),
          "| directo:", (10**6) ** 2 % MOD)
    # Embaldosados de 3×n con dominós (solo n par): 1, 0, 3, 0, 11, 0, 41, 0, 153 …
    dom = [1, 0, 3, 0, 11, 0, 41, 0, 153, 0, 571]
    c = berlekamp_massey(dom)
    print("dominós 3×n:", [x if x < MOD // 2 else x - MOD for x in c])   # [0, 4, 0, -1]


def pruebas():
    random.seed(1703)

    # Casos borde
    assert berlekamp_massey([]) == []
    assert berlekamp_massey([0, 0, 0]) == []
    assert len(berlekamp_massey([5])) == 1                 # s_0 ≠ 0 exige L ≥ 1
    assert berlekamp_massey([2, 4, 8, 16]) == [2]

    # Recurrencias aleatorias: con 2k términos se recupera una que genera todo
    for _ in range(400):
        p = random.choice([MOD, 998244353, 7])
        k = random.randint(1, 8)
        coefs = [random.randint(0, p - 1) for _ in range(k)]
        ini = [random.randint(0, p - 1) for _ in range(k)]
        s = _genera(coefs, ini, 3 * k + 5, p)
        c = berlekamp_massey(s[:2 * k], p)
        assert len(c) <= k
        assert _genera(c, s[:len(c)], len(s), p) == s       # genera los 3k+5 términos
        n = random.randint(0, 3 * k + 4)
        assert termino_n(c, s[:len(c)], n, p) == s[n]

    # Minimalidad contra fuerza bruta (mód 2 y mód 3, sucesiones cortas)
    for _ in range(300):
        p = random.choice([2, 3])
        N = random.randint(1, 7)
        s = [random.randint(0, p - 1) for _ in range(N)]
        c = berlekamp_massey(s, p)
        assert len(c) == _largo_minimo_bruto(s, p)
        assert all(s[i] == sum(c[j] * s[i - 1 - j] for j in range(len(c))) % p
                   for i in range(len(c), N))

    # termino_n con n grande contra fórmula directa (i^3)
    cub = [i ** 3 % MOD for i in range(12)]
    c = berlekamp_massey(cub)
    assert len(c) == 4
    for n in (10**5, 123456789, 10**12):
        assert termino_n(c, cub, n) == pow(n, 3, MOD)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
