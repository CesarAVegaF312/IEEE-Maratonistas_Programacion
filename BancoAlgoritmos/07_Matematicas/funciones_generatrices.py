"""
Matemáticas — Funciones generatrices con polinomios truncados («generating functions»)
Nivel: Avanzado
Ejecutar: python funciones_generatrices.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Codificar un problema de conteo como una serie A(x) = Σ a_n x^n donde
    a_n es la respuesta para el tamaño n. Las operaciones de conteo se
    vuelven álgebra: «elegir una cosa de aquí Y otra de allá» = producto;
    «secuencias de bloques» = 1/(1 − B(x)). En competencia se trabaja con
    polinomios TRUNCADOS a grado N (solo interesan los coeficientes 0..N).
    Cómo reconocerlo: «¿de cuántas formas se obtiene suma n?» con varias
    fuentes independientes (monedas, dados, objetos con cotas), caminos con
    pesos por tipo de paso, recurrencias lineales («coeficientes de una
    fracción»), o cuando la respuesta pedida es «el coeficiente de x^n en…».

FUNCIÓN
    multiplicar(a, b, N, p) -> list     (A·B) mód x^(N+1), coeficientes mód p
    inversa(a, N, p) -> list            1/A mód x^(N+1) (exige a[0] invertible)
    formas_monedas(monedas, N, p) -> list   [x^n] Π_c 1/(1 − x^c), n = 0..N
    formas_acotadas(topes, N, p) -> list    [x^n] Π_i (1 + x + … + x^{c_i})
    caminos_ponderados(n, m, a, b, c, p) -> int
        Suma sobre caminos de (0,0) a (n,m) con pasos (1,0) de peso a, (0,1)
        de peso b y (1,1) de peso c del PRODUCTO de pesos =
        [x^n y^m] 1/(1 − a·x − b·y − c·x·y) = Σ_k C(n,k)C(m,k)(ab+c)^k a^{n−k} b^{m−k}.

IDEA Y ALGORITMO
    - Producto = elecciones independientes: [x^n] A(x)B(x) = Σ_i a_i b_{n−i}
      cuenta los pares (objeto de A de tamaño i, objeto de B de tamaño n−i).
    - Secuencias: si B(x) cuenta los «bloques» (sin bloque vacío, b_0 = 0),
      las secuencias de bloques son Σ_j B^j = 1/(1 − B). Una moneda c
      usada cualquier número de veces: 1 + x^c + x^{2c} + … = 1/(1 − x^c).
    - Multiplicar por 1/(1 − x^c) en O(N): si R = A/(1 − x^c), entonces
      R·(1 − x^c) = A ⇒ r_n = a_n + r_{n−c} (suma prefija con paso c).
      Multiplicar por (1 + … + x^c) = (1 − x^{c+1})/(1 − x): restar a_{n−c−1}
      y luego prefijar con paso 1.
    - Inversa de una serie: si A·B = 1, igualando coeficientes:
      a_0 b_0 = 1 y Σ_{i=0}^{n} a_i b_{n−i} = 0 (n ≥ 1) ⇒
      b_n = −a_0^{-1} Σ_{i=1}^{n} a_i b_{n−i}. Así 1/(1 − x − x²) da Fibonacci.
    - Caminos ponderados (Guangzhou J): cada camino es una palabra en los
      tres pasos; la serie 1/(1 − (ax + by + cxy)) enumera todas las
      palabras con el producto de sus pesos. Escribiendo
      1 − ax − by − cxy = (1−ax)(1−by) − (ab+c)xy y desarrollando en
      potencias de (ab+c)xy/((1−ax)(1−by)), y usando
      [x^j] (1−ax)^{−(k+1)} = C(j+k, k) a^j, sale la suma cerrada en k.
    El enfoque ingenuo (enumerar combinaciones) es exponencial; la DP
    equivalente es justamente multiplicar polinomios.

MACROALGORITMO
    1. Escribir la función generatriz de cada «ingrediente» (un objeto,
       una moneda, un tipo de paso) como serie en x (marca el tamaño).
    2. Combinar: producto si son independientes; 1/(1 − B) si son
       secuencias; composición si hay estructura anidada.
    3. Truncar todo a grado N (no se necesitan coeficientes mayores).
    4. Calcular con productos O(N²) o con los atajos O(N) por factor
       (1/(1−x^c), (1−x^{c+1})/(1−x)).
    5. Leer el coeficiente pedido (mód p).
    6. Si sale una fracción P/Q con Q de grado pequeño: es una recurrencia
       lineal (kitamasa.py para n enorme).

COMPLEJIDAD
    multiplicar: O(N²) (FFT/NTT bajaría a O(N log N), no incluido).
    inversa: O(N²). formas_monedas / formas_acotadas: O(N) por factor.
    caminos_ponderados: O(min(n,m)) con factoriales precomputados.

EJEMPLO A MANO
    Monedas {1, 2, 5}, N = 5: 1/(1−x) → 1 1 1 1 1 1; ·1/(1−x²) → r_n = a_n +
    r_{n−2}: 1 1 2 2 3 3; ·1/(1−x^5) → 1 1 2 2 3 4. Hay 4 formas de pagar 5:
    5, 2+2+1, 2+1+1+1, 1·5.
    1/(1 − x − x²) = 1 + x + 2x² + 3x³ + 5x⁴ + … (Fibonacci).
    Caminos (2,3) con a=b=c=1: Σ_k C(2,k)C(3,k)2^k = 1 + 12 + 12 = 25
    (números de Delannoy D(2,3) = 25).

ERRORES TÍPICOS
    - No truncar: los polinomios crecen y todo se vuelve O(N²) por factor.
    - Al multiplicar por 1/(1−x^c) «en el lugar», recorrer n de MAYOR a
      menor (eso es la versión 0/1); para uso ilimitado va de menor a mayor.
    - Invertir una serie con a_0 = 0 (no existe la inversa).
    - Confundir conteo ordenado (secuencias: 1/(1−B)) con no ordenado
      (multiconjuntos: Π 1/(1−x^c)).

VARIANTES Y RELACIONADOS
    - Exponenciales (EGF) Σ a_n x^n/n! para objetos etiquetados: el
      producto de EGF combina conjuntos etiquetados (multinomiales).
    - FFT/NTT para productos en O(N log N) (no incluidos aquí).
    - kitamasa.py, berlekamp_massey.py: P(x)/Q(x) ↔ recurrencias lineales.
    - estrellas_barras.py, catalan.py (G = 1 + x G²), DP de mochila.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/J - Journey through Gridland (función generatriz
      de caminos de Delannoy ponderados: caminos_ponderados)
    - CSES «Coin Combinations I» (secuencias = ordenado) y «Coin
      Combinations II» (multiconjunto = Π 1/(1−x^c)), «Dice Combinations»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta: producto contra suma doble, inversa
      comprobando A·B = 1, monedas y cotas contra enumeración de tuplas,
      Fibonacci, caminos ponderados contra DP de cuadrícula (300 casos
      aleatorios por función) (python funciones_generatrices.py)
"""
import itertools
import random
from math import comb

MOD = 1_000_000_007


def multiplicar(a, b, N, p=MOD):
    """Coeficientes 0..N de A·B (mód p)."""
    r = [0] * (N + 1)
    for i, ai in enumerate(a[:N + 1]):
        if ai:
            for j, bj in enumerate(b[:N + 1 - i]):
                r[i + j] += ai * bj
    return [x % p for x in r]


def inversa(a, N, p=MOD):
    """Coeficientes 0..N de 1/A; exige a[0] invertible mód p."""
    a = list(a[:N + 1]) + [0] * max(0, N + 1 - len(a))
    inv0 = pow(a[0], p - 2, p)
    b = [0] * (N + 1)
    b[0] = inv0
    for n in range(1, N + 1):
        # Σ_{i=0}^{n} a_i b_{n-i} = 0  ⇒  b_n = −a_0^{-1} Σ_{i=1}^{n} a_i b_{n-i}
        s = sum(a[i] * b[n - i] for i in range(1, n + 1))
        b[n] = (-s * inv0) % p
    return b


def formas_monedas(monedas, N, p=MOD):
    """[x^n] Π_c 1/(1 − x^c): formas de pagar n con monedas ilimitadas (sin orden)."""
    r = [1] + [0] * N
    for c in monedas:
        for n in range(c, N + 1):      # de menor a mayor: uso ilimitado
            r[n] = (r[n] + r[n - c]) % p
    return r


def formas_acotadas(topes, N, p=MOD):
    """[x^n] Π_i (1 + x + … + x^{c_i}): elegir 0..c_i de cada tipo i."""
    r = [1] + [0] * N
    for c in topes:
        # multiplicar por (1 − x^{c+1}) (de mayor a menor) y luego por 1/(1 − x)
        for n in range(N, c, -1):
            r[n] = (r[n] - r[n - c - 1]) % p
        for n in range(1, N + 1):
            r[n] = (r[n] + r[n - 1]) % p
    return r


def caminos_ponderados(n, m, a, b, c, p=MOD):
    """[x^n y^m] 1/(1 − a x − b y − c x y) mód p (fórmula cerrada en k)."""
    s = (a * b + c) % p
    total = 0
    for k in range(min(n, m) + 1):
        total += comb(n, k) * comb(m, k) * pow(s, k, p) * pow(a, n - k, p) * pow(b, m - k, p)
    return total % p


def demo():
    print("formas de pagar 0..5 con {1,2,5}:", formas_monedas([1, 2, 5], 5))   # 1 1 2 2 3 4
    print("1/(1-x-x^2):", inversa([1, -1, -1], 9))                              # Fibonacci
    print("sumas de dos dados (caras 0..5):", formas_acotadas([5, 5], 10))
    print("Delannoy D(2,3) =", caminos_ponderados(2, 3, 1, 1, 1))              # 25
    print("Guangzhou J ejemplo '3 2 1 2 3' =", caminos_ponderados(3, 2, 2, 1, 3))  # 278


def pruebas():
    random.seed(17)
    p = MOD

    # Casos borde
    assert multiplicar([], [1, 2], 3) == [0, 0, 0, 0]
    assert inversa([5], 0) == [pow(5, p - 2, p)]
    assert formas_monedas([], 3) == [1, 0, 0, 0]
    assert formas_acotadas([0, 0], 2) == [1, 0, 0]
    assert caminos_ponderados(0, 0, 3, 4, 5) == 1

    for _ in range(300):
        N = random.randint(0, 12)
        A = [random.randint(-5, 5) for _ in range(random.randint(0, 8))]
        B = [random.randint(-5, 5) for _ in range(random.randint(0, 8))]
        bruto = [sum(A[i] * B[n - i] for i in range(len(A)) if 0 <= n - i < len(B)) % p
                 for n in range(N + 1)]
        assert multiplicar(A, B, N) == bruto
        A[0:1] = [random.randint(1, 9)] if A else [3]
        assert multiplicar(A, inversa(A, N), N) == [1] + [0] * N

    fib = inversa([1, -1, -1], 40)
    x, y = 1, 1
    for n in range(41):
        assert fib[n] == x % p
        x, y = y, x + y

    for _ in range(300):
        N = random.randint(0, 10)
        monedas = random.sample(range(1, 7), random.randint(0, 3))
        topes = [random.randint(0, 4) for _ in range(random.randint(0, 3))]
        for n in range(N + 1):
            # monedas: cantidades t_c con Σ t_c·c = n
            bruto = sum(1 for t in itertools.product(range(n + 1), repeat=len(monedas))
                        if sum(ti * c for ti, c in zip(t, monedas)) == n)
            assert formas_monedas(monedas, N)[n] == bruto
            bruto = sum(1 for t in itertools.product(*[range(c + 1) for c in topes])
                        if sum(t) == n)
            assert formas_acotadas(topes, N)[n] == bruto

    for _ in range(300):
        n, m = random.randint(0, 8), random.randint(0, 8)
        a, b, c = (random.randint(0, 10**9) for _ in range(3))
        # DP directa: suma de productos de pesos sobre todos los caminos
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for i in range(n + 1):
            for j in range(m + 1):
                if i:
                    dp[i][j] += dp[i - 1][j] * a
                if j:
                    dp[i][j] += dp[i][j - 1] * b
                if i and j:
                    dp[i][j] += dp[i - 1][j - 1] * c
                dp[i][j] %= p
        assert caminos_ponderados(n, m, a, b, c) == dp[n][m]


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
