"""
Matemáticas — Miller–Rabin determinista y Pollard-Rho («Miller–Rabin primality test», «Pollard's rho»)
Nivel: Avanzado
Ejecutar: python miller_rabin_pollard.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir si n ≤ 2^64 (y bastante más) es primo en O(log n) multiplicaciones
    modulares, y factorizar n ≈ 10^18 en ~O(n^(1/4)) pasos, cuando la
    división de prueba (O(√n) = 10^9) es imposible.
    Señales en el enunciado: «n ≤ 10^18» y hay que saber si es primo, o
    calcular su número/suma de divisores o su φ; «el mayor factor primo de
    n» con n enorme; muchas consultas de primalidad con números grandes.

FUNCIÓN
    es_primo(n) -> bool        determinista para n < 3,18·10^23 (cubre 64 bits).
    pollard_rho(n) -> int      un divisor no trivial de n (n compuesto, impar
                               o par).
    factorizar(n) -> list      factores primos de n ≥ 1 con repetición, en
                               orden creciente (n = 1 → []).

IDEA Y ALGORITMO
    Miller–Rabin. Si p es primo, en Z_p las únicas raíces cuadradas de 1 son
    ±1 (x² ≡ 1 ⇒ p | (x − 1)(x + 1) ⇒ p divide a uno de los dos). Escribimos
    n − 1 = d·2^s con d impar. Por Fermat a^(n−1) ≡ 1, y la sucesión
        a^d, a^(2d), a^(4d), …, a^(2^s·d) = a^(n−1) ≡ 1
    se obtiene elevando al cuadrado. Si n es primo, o bien a^d ≡ 1, o bien
    algún término es −1 (el primero que vale 1 tiene como raíz al anterior,
    que debe ser −1). Si para una base a eso NO pasa, n es compuesto con
    certeza («a es testigo»). Para n compuesto impar, a lo sumo 1/4 de las
    bases fallan en detectarlo; y se ha verificado computacionalmente que
    con las bases = los 12 primeros primos (2..37) no hay ningún compuesto
    que las pase todas por debajo de 3,18·10^23 > 2^64. Así el test es
    DETERMINISTA en ese rango (con los 13 primeros, hasta 3,3·10^24).
    Pollard-Rho. Sea p el menor primo de n (desconocido). La sucesión
    x_{i+1} = x_i² + c (mód n), mirada módulo p, toma valores en un
    conjunto de tamaño p, así que por la paradoja del cumpleaños se repite
    tras ~√p pasos y entra en un ciclo (forma de «ρ»). Cuando x_i ≡ x_j
    (mód p) pero no (mód n), gcd(|x_i − x_j|, n) es un divisor propio.
    Para detectar el ciclo sin guardar la sucesión se usa la variante de
    Brent (comparar con un «ancla» que se actualiza en potencias de 2) y se
    acumula el producto de varias diferencias antes de un solo gcd (lotes).
    Como p ≤ √n, son ~n^(1/4) pasos esperados: ~3·10^4 para n ≈ 10^18.
    Si el gcd da n (mala suerte), se reintenta con otro c.
    Factorizar: quitar primos pequeños por división; con el resto,
    recursivamente: si es primo se agrega; si no, partirlo con Pollard-Rho
    (pila explícita, sin recursión).

MACROALGORITMO
    Miller–Rabin:
    1. Descartar n < 2 y los múltiplos de los primos de las bases.
    2. Escribir n − 1 = d·2^s.
    3. Para cada base a: x = a^d mod n; si x ∈ {1, n−1} seguir con la siguiente.
    4.     Repetir s − 1 veces: x = x² mod n; si x = n − 1 → la base pasa.
    5.     Si nunca se llegó a n − 1 → compuesto.
    6. Si todas las bases pasan → primo.
    Pollard-Rho (Brent):
    7. Elegir c y x0 al azar; y = x0; r = 1.
    8. Repetir: ancla = y; avanzar y r veces acumulando q = q·|ancla − y| mod n
       en lotes y calcular g = gcd(q, n); duplicar r hasta que g > 1.
    9. Si g == n, retroceder paso a paso desde el último lote; si sigue
       siendo n, reintentar con otro c.
    Factorizar:
    10. Pila = [n]; sacar m: si es primo agregarlo; si no, d = pollard_rho(m)
        y apilar d y m/d. Ordenar al final.

COMPLEJIDAD
    Miller–Rabin: O(k·log n) multiplicaciones modulares (k = 12 bases).
    Pollard-Rho: O(n^(1/4)) iteraciones esperadas (heurístico).
    En Python: es_primo(~10^18) toma ~0,05 ms; factorizar un semiprimo
    p·q con p, q ≈ 10^9 toma ~0,05–0,3 s (en C++ unas 100 veces menos).

EJEMPLO A MANO
    n = 221 = 13·17, base a = 174: n − 1 = 220 = 55·2² (d = 55, s = 2).
      174^55 mod 221 = 47 (ni 1 ni 220); 47² mod 221 = 220 = −1 → la base 174
      PASA (221 es «pseudoprimo fuerte» en base 174: miente).
    Base a = 2: 2^55 mod 221 = 128; 128² mod 221 = 30 ≠ −1 → 2 es testigo:
      221 es compuesto. (Por eso se usan varias bases.)
    Pollard-Rho con n = 8051, c = 1, x0 = 2 (versión de Floyd):
      x avanza 1 paso, y avanza 2:  (x, y) = (5, 26), (26, 7474), (677, 871)
      gcd(21, 8051) = 1;  gcd(7448, 8051) = 1;  gcd(194, 8051) = 97
      → 8051 = 97 · 83. (Módulo 97 la sucesión ya se había repetido.)

ERRORES TÍPICOS
    - En C++, x·x mod n con n ~10^18 desborda: usar __int128 (en Python no
      hay problema).
    - Usar pocas bases (p. ej. solo 2, 3, 5, 7): hay compuestos que las pasan
      todas (3215031751 pasa 2, 3, 5 y 7). Con las 12 bases de aquí, el primer
      compuesto que engaña es 318665857834031151167461 ≈ 3,2·10^23: para
      números mayores agregar la base 41 (13 bases, hasta 3,3·10^24).
    - Llamar pollard_rho con n primo o con n = 4 (con x² + c y n par puede
      ciclar sin encontrar factor): primero quitar los factores pequeños y
      verificar con Miller–Rabin.
    - Implementación recursiva profunda para factorizar: usar pila.
    - No reintentar cuando el gcd devuelve n.

VARIANTES Y RELACIONADOS
    - n ≤ 10^12 o pocas consultas pequeñas: primalidad.py (√n basta).
    - Muchos n ≤ 10^7: criba con spf (criba_eratostenes.py, factorizacion.py).
    - Con la factorización: divisores.py (d(n), σ(n)), phi_euler.py.
    - Exponenciación modular rápida: exponenciacion_rapida.py.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/B - Between Ceiling and Floor (σ(m) con m ≤ 10^18:
      Miller–Rabin + Pollard-Brent)
    - SPOJ PON «Prime or Not»; Library Checker «Factorize»

VERIFICACIÓN
    - Pruebas: OK contra una criba para todo n ≤ 2·10^5, contra división de
      prueba en 300 n aleatorios hasta 10^12, pseudoprimos fuertes conocidos
      (2047, 1373653, 3215031751, 3825123056546413051…), primos conocidos
      (2^61 − 1, 10^9 + 7…), el primer falso positivo con 12 bases
      (≈ 3,2·10^23, confirma el límite documentado), y factorizaciones verificadas (producto = n,
      todos primos, iguales a división de prueba si n ≤ 10^10) en 400 casos,
      incluidos semiprimos p·q con p, q ≈ 10^9 y potencias de primos
      (python miller_rabin_pollard.py)
"""
import math
import random

PRIMOS_PEQUENOS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]   # bases deterministas (n < 3,18·10^23)


def es_primo(n):
    """Miller–Rabin determinista para n < 3,18·10^23 (incluye todo 64 bits)."""
    if n < 2:
        return False
    for p in PRIMOS_PEQUENOS:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:               # n - 1 = d * 2^s con d impar
        d //= 2
        s += 1
    for a in PRIMOS_PEQUENOS:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue                # la base pasa
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break               # apareció -1: la base pasa
        else:
            return False            # a es testigo: n compuesto seguro
    return True


def pollard_rho(n):
    """Un divisor no trivial de n compuesto (variante de Brent con gcd por lotes)."""
    if n % 2 == 0:
        return 2
    while True:
        c = random.randrange(1, n)
        y = random.randrange(0, n)
        m = 128                     # tamaño del lote: un gcd cada m pasos
        g = r = q = 1
        while g == 1:
            x = y                   # ancla
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y              # para poder retroceder si el lote da g == n
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = math.gcd(q, n)
                k += m
            r *= 2
        if g == n:                  # el lote mezcló el factor con todo n: ir paso a paso
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
        if g != n:
            return g                # si aun así es n, otro c


def factorizar(n):
    """Factores primos de n >= 1 con repetición, en orden creciente."""
    factores = []
    for p in PRIMOS_PEQUENOS:      # los primos chicos, por división (más rápido)
        while n % p == 0:
            factores.append(p)
            n //= p
    pila = [n] if n > 1 else []
    while pila:
        m = pila.pop()
        if es_primo(m):
            factores.append(m)
        else:
            d = pollard_rho(m)
            pila.append(d)
            pila.append(m // d)
    factores.sort()
    return factores


def demo():
    for n in (221, 1_000_000_007, 2**61 - 1, 3215031751):
        print(f"es_primo({n}) = {es_primo(n)}")
    print("factorizar(8051) =", factorizar(8051))                      # [83, 97]
    print("factorizar(10**18) =", factorizar(10**18))
    n = 999999937 * 1000000007
    print(f"factorizar({n}) =", factorizar(n))


def pruebas():
    random.seed(2017)

    def primo_lento(x):
        return x >= 2 and all(x % d for d in range(2, math.isqrt(x) + 1))

    # Casos borde y conocidos
    assert [x for x in range(-3, 20) if es_primo(x)] == [2, 3, 5, 7, 11, 13, 17, 19]
    for x in (2047, 1373653, 25326001, 3215031751, 2152302898747, 3474749660383,
              341550071728321, 3825123056546413051):
        assert not es_primo(x), x                       # pseudoprimos fuertes conocidos
    # El límite documentado es real: el menor compuesto que engaña a las 12 bases
    limite = 399165290221 * 798330580441                # = 318665857834031151167461
    assert es_primo(limite)                             # falso positivo (fuera de rango)
    for x in (10**9 + 7, 998244353, 2**31 - 1, 2**61 - 1, 999999999989):
        assert es_primo(x), x
    assert not es_primo((2**31 - 1) * (2**61 - 1))
    assert factorizar(1) == [] and factorizar(2) == [2] and factorizar(4) == [2, 2]
    assert factorizar(10**18) == [2] * 18 + [5] * 18

    # Contra una criba
    N = 200_000
    criba = bytearray([1]) * (N + 1)
    criba[0] = criba[1] = 0
    for i in range(2, math.isqrt(N) + 1):
        if criba[i]:
            criba[i * i::i] = bytearray(len(range(i * i, N + 1, i)))
    assert all(es_primo(x) == bool(criba[x]) for x in range(N + 1))
    primos = [p for p in range(N + 1) if criba[p]]

    # Contra división de prueba (por primos hasta 10^6 = √10^12)
    primos_raiz = [p for p in range(2, 10**6) if p <= N and criba[p]]
    primos_raiz += [p for p in range(N + 1, 10**6, 2) if es_primo(p)]   # completa con MR (ya validado en ≤ N)
    for _ in range(300):
        n = random.randint(2, 10**12)
        esperado = all(n % p for p in primos_raiz if p * p <= n)
        assert es_primo(n) == (esperado or n in primos_raiz)

    # Factorizaciones
    def verificar(n):
        f = factorizar(n)
        assert math.prod(f) == n and f == sorted(f) and all(es_primo(p) for p in f)
        return f

    for _ in range(300):
        n = random.randint(1, 10**10)
        f = verificar(n)
        # contra división de prueba simple
        g, x, d = [], n, 2
        while d * d <= x:
            while x % d == 0:
                g.append(d)
                x //= d
            d += 1
        if x > 1:
            g.append(x)
        assert f == g
    for _ in range(80):
        n = math.prod(random.choice(primos) for _ in range(random.randint(1, 6))) * \
            random.randint(1, 10**6)
        verificar(n)
    # semiprimos difíciles p·q con p, q ≈ 10^9, y potencias
    grandes = []
    while len(grandes) < 8:
        p = random.randint(10**9, 2 * 10**9)
        if es_primo(p):
            grandes.append(p)
    for i in range(0, 8, 2):
        p, q = grandes[i], grandes[i + 1]
        assert factorizar(p * q) == sorted([p, q])
    assert factorizar(grandes[0] ** 2) == [grandes[0]] * 2
    assert factorizar(1000003 ** 3) == [1000003] * 3


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
