"""
Matemáticas — Exponenciación rápida («Binary exponentiation», «exponentiation by squaring»)
Nivel: Básico
Ejecutar: python exponenciacion_rapida.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular a^b (normalmente módulo m) con b hasta 10^18 o más en
    O(log b) multiplicaciones, en vez de b multiplicaciones.
    Señales en el enunciado: «imprima la respuesta módulo 10^9 + 7» con
    potencias enormes; inverso modular por Fermat (a^(p−2) mod p); aplicar
    la MISMA operación b veces (matrices para recurrencias, permutaciones,
    composición de funciones): cualquier operación asociativa se puede
    «elevar» igual.

FUNCIÓN
    potencia_mod(a, b, m) -> int    a^b mod m, en [0, m); b ≥ 0, m ≥ 1.
                                    potencia_mod(x, 0, 1) = 0.
    potencia(x, b, mul, identidad) -> x^b con una operación asociativa
                                    cualquiera (enteros, matrices, …).
    En Python ya existe: pow(a, b, m) (en C, más rápido; con b = −1 da el
    inverso modular desde Python 3.8).

IDEA Y ALGORITMO
    Escribir b en binario: b = Σ b_i·2^i. Entonces
        a^b = Π_{i : b_i = 1} a^(2^i),
    y las potencias a^1, a^2, a^4, a^8, … se obtienen elevando al cuadrado
    la anterior (a^(2^(i+1)) = (a^(2^i))^2). Recorriendo los bits de b de
    menor a mayor: se mantiene base = a^(2^i), y si el bit i vale 1 se
    multiplica el resultado por base. b tiene ⌊log2 b⌋ + 1 bits: O(log b).
    Invariante: resultado · base^(b restante) = a^(b original).
    Equivalente recursivo: a^b = (a^(b/2))^2 si b es par, a·a^(b−1) si es
    impar.
    Módulo m: como (x·y) mod m = ((x mod m)·(y mod m)) mod m, se puede
    reducir después de CADA multiplicación y los números nunca pasan de m²
    (cabe en 64 bits si m ≤ ~3·10^9; en C++ con m ≤ 10^9+7 basta long long).
    Solo usa asociatividad (no conmutatividad), así que sirve igual para
    matrices: x^b con multiplicación de matrices en O(k^3 log b).
    El ingenuo (multiplicar b veces) es O(b): con b = 10^18 nunca termina.

MACROALGORITMO
    1. resultado = 1 mod m; base = a mod m.
    2. Mientras b > 0:
    3.     si b es impar: resultado = resultado · base mod m.
    4.     base = base · base mod m;  b = b // 2.
    5. Devolver resultado.

COMPLEJIDAD
    O(log b) multiplicaciones; memoria O(1).
    pow(a, b, m) nativo: ~10^6 llamadas con b ≈ 10^9 por segundo;
    la versión escrita a mano es unas 10 veces más lenta.

EJEMPLO A MANO
    3^13 mod 7, 13 = 1101₂:
      bit 1: res = 1·3 = 3         base = 3² = 9 ≡ 2
      bit 0: (no multiplica)       base = 2² = 4
      bit 1: res = 3·4 = 12 ≡ 5    base = 4² = 16 ≡ 2
      bit 1: res = 5·2 = 10 ≡ 3    base = 4
    3^13 = 1594323 = 7·227760 + 3  → 3. ✓

ERRORES TÍPICOS
    - Devolver 1 para b = 0 y m = 1: la respuesta es 0 (todo ≡ 0 mód 1).
      Inicializar resultado = 1 % m.
    - No reducir la base al inicio (a puede ser 10^18 o negativo): en C++
      desborda; en Python un a negativo da bien con %, pero conviene
      normalizar.
    - En C++, base·base con int de 32 bits: desborda. Usar long long (y
      __int128 si m > 3·10^9).
    - Reducir el EXPONENTE módulo m: a^b mod m ≠ a^(b mod m) mod m. Lo que
      vale (si gcd(a, m) = 1) es reducirlo módulo φ(m) (ver phi_euler.py);
      con m primo, módulo m − 1.
    - En Python, usar a**b % m: calcula el número gigante completo primero.

VARIANTES Y RELACIONADOS
    - Exponenciación de matrices para recurrencias lineales
      (exponenciacion_matrices.py).
    - Inverso modular por Fermat: aritmetica_modular.py; por Euclides
      extendido: euclides_extendido.py.
    - Teorema de Euler y exponentes gigantes (torres a^b^c): phi_euler.py.
    - Multiplicación binaria (a·b mod m con sumas) para m ~10^18 en C++ sin
      __int128: misma idea con + en lugar de ·.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/K - Sample Median Preservation (inverso por Fermat
      con pow(x, MOD − 2, MOD))
    - ICPC/Guangzhou 2017/F - Finding Paths (factoriales inversos con pow)
    - ICPC/Colombia 2018/F - A Fibonacci Family Formula (x^n módulo un
      polinomio por cuadrados sucesivos, Kitamasa)
    - CSES «Exponentiation», «Exponentiation II»

VERIFICACIÓN
    - Pruebas: OK contra multiplicación repetida (fuerza bruta) en 2000
      casos pequeños, contra pow nativo en 2000 casos con b hasta 10^30, y
      Fibonacci por potencia de matrices contra la iteración simple
      (python exponenciacion_rapida.py)
"""
import random


def potencia_mod(a, b, m):
    """a^b mod m con b >= 0 y m >= 1, en O(log b)."""
    resultado = 1 % m           # si m == 1 todo es 0
    base = a % m                # normaliza negativos y valores grandes
    while b > 0:
        if b & 1:               # el bit actual de b está prendido
            resultado = resultado * base % m
        base = base * base % m  # base pasa de a^(2^i) a a^(2^(i+1))
        b >>= 1
    return resultado


def potencia(x, b, mul, identidad):
    """x^b para cualquier operación asociativa mul con neutro identidad."""
    resultado = identidad
    while b > 0:
        if b & 1:
            resultado = mul(resultado, x)
        x = mul(x, x)
        b >>= 1
    return resultado


def mul_matriz(A, B, m=10**9 + 7):
    """Producto de matrices cuadradas módulo m (para el ejemplo de Fibonacci)."""
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) % m for j in range(n)] for i in range(n)]


def fibonacci_mod(n, m=10**9 + 7):
    """F(n) mod m con [[1,1],[1,0]]^n = [[F(n+1),F(n)],[F(n),F(n-1)]]."""
    M = potencia([[1, 1], [1, 0]], n, lambda A, B: mul_matriz(A, B, m), [[1, 0], [0, 1]])
    return M[0][1] % m


def demo():
    print("3^13 mod 7 =", potencia_mod(3, 13, 7))                       # 3
    print("2^(10^18) mod 1e9+7 =", potencia_mod(2, 10**18, 10**9 + 7))
    print("pow nativo           =", pow(2, 10**18, 10**9 + 7))
    print("F(90) mod 1e9+7 =", fibonacci_mod(90))


def pruebas():
    random.seed(99)

    # Casos borde
    assert potencia_mod(5, 0, 1) == 0 and potencia_mod(5, 0, 7) == 1
    assert potencia_mod(0, 0, 7) == 1 and potencia_mod(0, 5, 7) == 0
    assert potencia_mod(-2, 3, 7) == (-8) % 7
    assert potencia_mod(10**18, 10**18, 1) == 0
    assert potencia(3, 0, lambda x, y: x * y, 1) == 1

    # Fuerza bruta: multiplicar b veces
    for _ in range(2000):
        a = random.randint(-50, 50)
        b = random.randint(0, 40)
        m = random.randint(1, 100)
        bruto = 1 % m
        for _ in range(b):
            bruto = bruto * a % m
        assert potencia_mod(a, b, m) == bruto
        assert potencia(a, b, lambda x, y: x * y, 1) == a ** b

    # Contra pow nativo con exponentes enormes
    for _ in range(2000):
        a = random.randint(0, 10**18)
        b = random.randint(0, 10**30)
        m = random.randint(1, 10**18)
        assert potencia_mod(a, b, m) == pow(a, b, m)

    # Potencia genérica con matrices: Fibonacci contra la iteración simple
    f0, f1 = 0, 1
    for n in range(200):
        assert fibonacci_mod(n) == f0 % (10**9 + 7)
        f0, f1 = f1, f0 + f1


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
