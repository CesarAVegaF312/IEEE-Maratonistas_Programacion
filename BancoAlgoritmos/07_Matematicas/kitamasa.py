"""
Matemáticas — Kitamasa: n-ésimo término de una recurrencia lineal en O(k² log n) («Kitamasa method»)
Nivel: Avanzado
Ejecutar: python kitamasa.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular f(n) mód p para una recurrencia lineal homogénea de orden k
        f(i) = c_1·f(i−1) + c_2·f(i−2) + … + c_k·f(i−k)
    con n hasta 10^18, en O(k² log n) en vez del O(k³ log n) de la
    exponenciación de matrices. Con k = 100 es la diferencia entre ~10^8 y
    ~10^6 operaciones por consulta.
    Cómo reconocerlo: recurrencia lineal de orden k «grande» (50–1000) y n
    gigante; muchas consultas de la misma recurrencia; después de
    Berlekamp–Massey (que entrega la recurrencia pero no el término).

FUNCIÓN
    kitamasa(coefs, iniciales, n, p) -> int
        coefs = [c_1, …, c_k], iniciales = [f(0), …, f(k−1)]; devuelve f(n) mód p.
    x_a_la_n_mod(coefs, n, p) -> list
        R(x) = x^n mód P(x) como lista de k coeficientes (r_0 … r_{k−1}),
        con P(x) = x^k − c_1 x^{k−1} − … − c_k (polinomio característico).

IDEA Y ALGORITMO
    Sea φ el funcional lineal sobre polinomios definido por φ(x^m) = f(m).
    La recurrencia dice exactamente que φ(x^m · P(x)) = f(m+k) − Σ_j c_j
    f(m+k−j) = 0 para todo m ≥ 0, y por linealidad φ(Q·P) = 0 para todo
    polinomio Q. Si x^n = Q(x)·P(x) + R(x) (división de polinomios), entonces
        f(n) = φ(x^n) = φ(Q·P) + φ(R) = φ(R) = Σ_{j<k} r_j · f(j).
    Así que basta calcular R = x^n mód P, un polinomio de grado < k, y para
    eso se usa exponenciación binaria sobre polinomios: el producto de dos
    restos tiene grado ≤ 2k−2 y se reduce con la regla
        x^k ≡ c_1 x^{k−1} + … + c_k   (mód P),
    bajando desde el coeficiente más alto (cada x^i con i ≥ k se reemplaza
    por Σ_j c_j x^{i−j}). Producto O(k²) + reducción O(k²) por paso, y hay
    O(log n) pasos. Comparado con matrices: el estado es un polinomio de k
    coeficientes en vez de una matriz de k² entradas.

MACROALGORITMO
    1. Si n < k, responder iniciales[n].
    2. R = 1 (polinomio constante), B = x (o x mód P si k = 1).
    3. Recorrer los bits de n: si el bit está, R = R·B mód P; B = B·B mód P.
    4. Para reducir un producto de grado ≤ 2k−2: para i desde el grado más
       alto hasta k, t = coef[i]; coef[i−j] += t·c_j (j = 1..k); coef[i] = 0.
    5. Responder Σ_j r_j · f(j) mód p.

COMPLEJIDAD
    O(k² log n) tiempo, O(k) memoria. En Python puro, k = 100 y n = 10^18
    son ~90 productos de 10^4 multiplicaciones (~0,2 s medido); con sustitución de
    Kronecker (empaquetar coeficientes en un entero grande) el producto
    corre en C y baja a milisegundos (ver Colombia 2018 F).

EJEMPLO A MANO
    Fibonacci: P(x) = x² − x − 1, así x² ≡ x + 1. x⁴ = (x²)² ≡ (x+1)² =
    x² + 2x + 1 ≡ 3x + 2. Entonces F(4) = 3·F(1) + 2·F(0) = 3·1 + 2·0 = 3. ✔
    x⁵ = x·x⁴ ≡ 3x² + 2x ≡ 5x + 3 → F(5) = 5.

ERRORES TÍPICOS
    - Orden de los coeficientes: coefs[0] multiplica a f(i−1), no a f(i−k).
    - Reducir de abajo hacia arriba (hay que ir del grado mayor al menor,
      porque reducir x^i crea términos de grado i−1 que también se reducen).
    - Olvidar el caso k = 1 (x ya tiene grado k y hay que reducirlo).
    - Recurrencias NO homogéneas (con +constante): agregar la constante como
      término extra aumentando k en 1 (multiplicar P por (x − 1)).

VARIANTES Y RELACIONADOS
    - exponenciacion_matrices.py (O(k³ log n), más general: varios estados).
    - berlekamp_massey.py (encuentra coefs a partir de 2k términos).
    - Truco del repo (Colombia 2018 F): reducir módulo Q = (x−1)·P, que
      tiene solo 3 términos, para que la reducción sea O(k).
    - Con FFT el producto es O(k log k) y todo O(k log k log n).
    - Algoritmo de Bostan–Mori: [x^n] P(x)/Q(x) con la misma complejidad.

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/F - A Fibonacci Family Formula (orden k ≤ 100,
      n ≤ 10^15; también es el C del warmup 2026)
    - ICPC/Guangzhou 2017/E - Easy Tiling Problem (Kitamasa sobre la
      recurrencia que entrega Berlekamp–Massey)

VERIFICACIÓN
    - Pruebas: OK contra iteración directa en 600 recurrencias aleatorias
      (k ≤ 8, n ≤ 200), Fibonacci con n hasta 10^18 contra «fast doubling»,
      y la k-bonacci de Colombia 2018 F (python kitamasa.py)
"""
import random

MOD = 1_000_000_007


def _mul_mod(a, b, coefs, p):
    """(a·b) mód P(x) con a, b de grado < k; resultado con k coeficientes."""
    k = len(coefs)
    prod = [0] * (2 * k - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                prod[i + j] += ai * bj
    # Reducir desde el grado más alto: x^i = x^(i-k)·x^k ≡ Σ_j c_j x^(i-j)
    for i in range(2 * k - 2, k - 1, -1):
        t = prod[i] % p
        if t:
            for j in range(1, k + 1):
                prod[i - j] += t * coefs[j - 1]
        prod[i] = 0
    return [v % p for v in prod[:k]]


def x_a_la_n_mod(coefs, n, p=MOD):
    """Coeficientes r_0..r_{k-1} de x^n mód P(x), P(x) = x^k − Σ c_j x^(k-j)."""
    k = len(coefs)
    resultado = [1] + [0] * (k - 1)            # polinomio 1
    if k == 1:
        base = [coefs[0] % p]                  # x ≡ c_1 (mód x − c_1)
    else:
        base = [0, 1] + [0] * (k - 2)          # polinomio x
    while n:
        if n & 1:
            resultado = _mul_mod(resultado, base, coefs, p)
        base = _mul_mod(base, base, coefs, p)
        n >>= 1
    return resultado


def kitamasa(coefs, iniciales, n, p=MOD):
    """f(n) mód p con f(i) = Σ_j coefs[j]·f(i-1-j), f(0..k-1) = iniciales."""
    k = len(coefs)
    if n < k:
        return iniciales[n] % p
    r = x_a_la_n_mod(coefs, n, p)
    return sum(r[j] * iniciales[j] for j in range(k)) % p   # f(n) = φ(R)


def _fib_doubling(n, p):
    """(F(n), F(n+1)) por duplicación: F(2m) = F(m)(2F(m+1) − F(m)), F(2m+1) = F(m)² + F(m+1)²."""
    if n == 0:
        return 0, 1
    a, b = _fib_doubling(n >> 1, p)
    c = a * (2 * b - a) % p
    d = (a * a + b * b) % p
    return (d, (c + d) % p) if n & 1 else (c, d)


def demo():
    print("x^4 mód (x^2 - x - 1):", x_a_la_n_mod([1, 1], 4))        # [2, 3] = 3x + 2
    print("F(10) =", kitamasa([1, 1], [0, 1], 10))                   # 55
    print("F(10^18) mód 1e9+7 =", kitamasa([1, 1], [0, 1], 10**18))
    k = 3   # Colombia 2018 F: f_0 = 1, f_j = 2^(j-1), suma de los k anteriores
    print("familia k=3, n=4:", kitamasa([1] * k, [1] + [2 ** (j - 1) for j in range(1, k)], 4))  # 7


def pruebas():
    random.seed(1810)

    # Casos borde
    assert kitamasa([5], [3], 0) == 3 and kitamasa([5], [3], 3) == 375
    assert kitamasa([0, 0], [4, 7], 5) == 0
    assert kitamasa([1, 1], [0, 1], 1) == 1

    for _ in range(600):
        k = random.randint(1, 8)
        p = random.choice([MOD, 998244353, 101, 2])
        coefs = [random.randint(0, 20) for _ in range(k)]
        ini = [random.randint(0, 20) for _ in range(k)]
        f = ini[:]
        for i in range(k, 201):
            f.append(sum(coefs[j] * f[i - 1 - j] for j in range(k)) % p)
        n = random.randint(0, 200)
        assert kitamasa(coefs, ini, n, p) == f[n] % p

    for _ in range(200):
        n = random.randint(0, 10**18)
        assert kitamasa([1, 1], [0, 1], n) == _fib_doubling(n, MOD)[0]

    # k-bonacci de Colombia 2018 F (mód 10^9+9) contra iteración
    P9 = 1_000_000_009
    for k in range(1, 12):
        ini = [1] + [2 ** (j - 1) for j in range(1, k)]
        f = [1]
        for n in range(1, 120):
            f.append(sum(f[max(0, n - k):n]) % P9)
        for n in range(120):
            assert kitamasa([1] * k, ini, n, P9) == f[n]


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
