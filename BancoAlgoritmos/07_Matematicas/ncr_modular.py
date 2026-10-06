"""
Matemáticas — C(n, k) módulo un primo: factoriales precomputados y teorema de Lucas
Nivel: Intermedio
Ejecutar: python ncr_modular.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Responder MUCHAS consultas C(n, k) mód p (p primo, típicamente
    10^9+7 o 998244353) en O(1) cada una tras un precálculo O(N).
    Si p es pequeño (p ≤ ~10^6) y n puede ser enorme (10^18), usar Lucas.
    Cómo reconocerlo: «imprima la respuesta módulo 10^9+7» en un problema de
    conteo con binomiales; n hasta 10^6–10^7; muchas consultas o sumas de
    binomiales; «módulo un primo pequeño p» con n gigante → Lucas.

FUNCIÓN
    preparar(N, p) -> (fact, inv_fact)
        fact[i] = i! mód p, inv_fact[i] = (i!)^(-1) mód p para 0 ≤ i ≤ N.
        Exige N < p (si no, N! ≡ 0 y no hay inverso).
    ncr(n, k, fact, inv_fact, p) -> int     C(n, k) mód p; 0 si k<0 o k>n.
    inversos_1_a_n(N, p) -> list            inv[i] = i^(-1) mód p, en O(N).
    lucas(n, k, p) -> int                   C(n, k) mód p, p primo pequeño,
                                            n y k arbitrarios.

IDEA Y ALGORITMO
    - C(n, k) = n! / (k!(n-k)!). Módulo p no se puede «dividir», pero sí
      multiplicar por el inverso: por el pequeño teorema de Fermat, si p es
      primo y p ∤ a, a^(p-1) ≡ 1 (mód p), luego a·a^(p-2) ≡ 1 y
      a^(-1) ≡ a^(p-2) = pow(a, p-2, p) (en Python 3.8+: pow(a, -1, p)).
    - Precálculo en O(N) con UNA sola exponenciación: se calcula
      inv_fact[N] = pow(fact[N], p-2, p) y se baja con
        inv_fact[i-1] = inv_fact[i] · i,   porque 1/(i-1)! = i / i!.
    - Inversos de 1..N en O(N): escribiendo p = q·i + r (q = p//i, r = p%i),
      0 ≡ q·i + r ⇒ i^(-1) ≡ -q · r^(-1) (mód p), con r < i ya calculado.
    - Teorema de Lucas: si n = Σ n_j p^j y k = Σ k_j p^j en base p,
        C(n, k) ≡ Π_j C(n_j, k_j)  (mód p)   (C(a, b) = 0 si b > a).
      Prueba: para 0 < i < p, p divide a C(p, i) = p!/(i!(p-i)!) (p está en
      el numerador y no en el denominador), así que (1+x)^p ≡ 1 + x^p.
      Con n = n_0 + p·m: (1+x)^n ≡ (1+x)^{n_0}·(1+x^p)^m. El coeficiente de
      x^k con k = k_0 + p·k' solo sale de x^{k_0} en el primer factor (sus
      grados son < p) y de x^{p·k'} en el segundo: C(n_0, k_0)·C(m, k').
      Se repite con m y k' (los siguientes dígitos).
    - El enfoque ingenuo (math.comb(n, k) % p) construye un entero de
      ~n·log n bits: inviable con muchas consultas y n ~ 10^6.

MACROALGORITMO
    1. N = mayor n que se va a consultar (debe ser < p).
    2. fact[0..N] acumulando productos mód p.
    3. inv_fact[N] = fact[N]^(p-2) mód p; bajar inv_fact[i-1] = inv_fact[i]·i.
    4. Consulta: fact[n]·inv_fact[k]·inv_fact[n-k] mód p (0 si k fuera de rango).
    5. Lucas: mientras n o k > 0, multiplicar C(n % p, k % p) (con tabla de
       factoriales de tamaño p) y hacer n //= p, k //= p.

COMPLEJIDAD
    preparar: O(N) tiempo y memoria (N = 10^6 en ~0,3 s en Python).
    ncr: O(1). lucas: O(p) de precálculo + O(log_p n) por consulta.

EJEMPLO A MANO
    p = 7, C(10, 3) = 120 ≡ 1 (mód 7).
    Factoriales: 10! ≡ 0 mód 7 → NO sirve (10 ≥ p); usar Lucas:
    10 = (1,3)_7, 3 = (0,3)_7 → C(1,0)·C(3,3) = 1·1 = 1. ✔
    p = 10^9+7: C(10, 3) = 3628800 · inv(6) · inv(5040) = 120.

ERRORES TÍPICOS
    - Usar factoriales con n ≥ p (todo da 0 o basura): ahí va Lucas.
    - Calcular pow(x, p-2, p) por cada consulta en vez de precomputar
      inv_fact (multiplica el tiempo por ~30).
    - Olvidar el «% p» en algún producto (en Python no desborda, pero los
      números crecen y todo se vuelve lento).
    - No devolver 0 cuando k < 0 o k > n (índice negativo en Python ¡no da
      error!, lee del final de la lista).
    - Usar Fermat con módulo NO primo (p.ej. 10^9): el inverso no existe en
      general; ahí hay que factorizar o usar Lucas generalizado/CRT.

VARIANTES Y RELACIONADOS
    - combinatoria_basica.py (versión exacta), conteo_complemento.py,
      inclusion_exclusion.py, estrellas_barras.py, catalan.py (usan esto).
    - Para un solo C(n, k) con k pequeño y n enorme (< p): producto
      n(n-1)…(n-k+1) · inv(k!) en O(k).
    - Módulo compuesto (p^e o producto de primos): Lucas generalizado
      (Granville) + teorema chino del resto.
    - Inverso modular general (módulo no primo): Euclides extendido.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/K - Sample Median Preservation (suma de productos
      de binomiales mód 10^9+7, factoriales hasta 10^6)
    - ICPC/Guangzhou 2017/F - Finding Paths (factoriales e inversos hasta 3001)
    - ICPC/Guangzhou 2017/J - Journey through Gridland (factoriales hasta 10^6)
    - CSES «Binomial Coefficients», «Creating Strings II», «Distributing Apples»

VERIFICACIÓN
    - Pruebas: OK contra math.comb(n, k) % p para todo n ≤ 200 con
      p = 10^9+7 y 998244353, 1000 pares aleatorios con n ≤ 5000; Lucas
      contra math.comb % p con p ∈ {2,3,5,7,11,13,101} en 3000 casos con
      n ≤ 3000; inversos de 1..N comprobados (python ncr_modular.py)
"""
import math
import random

MOD = 1_000_000_007


def preparar(N, p=MOD):
    """fact[i] = i! mód p, inv_fact[i] = (i!)^(-1) mód p, para i en 0..N (N < p)."""
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % p
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], p - 2, p)        # Fermat: una sola potencia
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % p   # 1/(i-1)! = i · 1/i!
    return fact, inv_fact


def ncr(n, k, fact, inv_fact, p=MOD):
    """C(n, k) mód p en O(1) con las tablas de preparar()."""
    if k < 0 or k > n:
        return 0
    return fact[n] * inv_fact[k] % p * inv_fact[n - k] % p


def inversos_1_a_n(N, p=MOD):
    """inv[i] = i^(-1) mód p para 1 ≤ i ≤ N, en O(N) (p primo, N < p)."""
    inv = [0, 1] + [0] * (N - 1) if N >= 1 else [0]
    for i in range(2, N + 1):
        # p = (p//i)·i + p%i  ⇒  i^(-1) = -(p//i) · (p%i)^(-1)
        inv[i] = (p - p // i) * inv[p % i] % p
    return inv


_tablas_lucas = {}   # p -> (fact, inv_fact) de 0..p-1, se calcula una vez por primo


def lucas(n, k, p):
    """C(n, k) mód p para p primo (pequeño) y n, k arbitrarios (teorema de Lucas)."""
    if k < 0 or k > n:
        return 0
    if p not in _tablas_lucas:
        _tablas_lucas[p] = preparar(p - 1, p)  # tabla para dígitos 0..p-1
    fact, inv_fact = _tablas_lucas[p]
    r = 1
    while n or k:
        a, b = n % p, k % p                     # dígitos actuales en base p
        if b > a:
            return 0                            # C(a, b) = 0 con b > a
        r = r * fact[a] % p * inv_fact[b] % p * inv_fact[a - b] % p
        n //= p
        k //= p
    return r


def demo():
    fact, inv_fact = preparar(20)
    print("C(10, 3) mód 1e9+7 =", ncr(10, 3, fact, inv_fact))       # 120
    print("C(10, 3) mód 7 (Lucas) =", lucas(10, 3, 7))               # 1
    print("C(100, 30) mód 13 (Lucas) =", lucas(100, 30, 13),
          "| math.comb % 13 =", math.comb(100, 30) % 13)
    print("inversos 1..5 mód 7:", inversos_1_a_n(5, 7)[1:])          # [1, 4, 5, 2, 3]


def pruebas():
    random.seed(77)

    # Casos borde
    f, fi = preparar(0)
    assert ncr(0, 0, f, fi) == 1 and ncr(0, 1, f, fi) == 0 and ncr(0, -1, f, fi) == 0
    assert lucas(0, 0, 2) == 1 and lucas(5, 7, 3) == 0

    # Factoriales contra math.comb % p (todo n ≤ 200, dos primos usuales)
    for p in (MOD, 998244353):
        f, fi = preparar(5000, p)
        for n in range(201):
            for k in range(-1, n + 2):
                esperado = math.comb(n, k) % p if 0 <= k <= n else 0
                assert ncr(n, k, f, fi, p) == esperado
        for _ in range(500):
            n = random.randint(0, 5000)
            k = random.randint(0, n)
            assert ncr(n, k, f, fi, p) == math.comb(n, k) % p

    # Inversos 1..N
    for p in (7, 13, MOD):
        N = min(p - 1, 3000)
        inv = inversos_1_a_n(N, p)
        assert all(i * inv[i] % p == 1 for i in range(1, N + 1))

    # Lucas contra math.comb % p con primos pequeños (incluye n ≥ p)
    for _ in range(3000):
        p = random.choice([2, 3, 5, 7, 11, 13, 101])
        n = random.randint(0, 3000)
        k = random.randint(0, n + 3)
        esperado = math.comb(n, k) % p if k <= n else 0
        assert lucas(n, k, p) == esperado
    # Propiedad conocida: C(n, k) es impar ⇔ los bits de k están en n
    for _ in range(300):
        n = random.randint(0, 10**18)
        k = random.randint(0, n)
        assert lucas(n, k, 2) == (1 if n & k == k else 0)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
