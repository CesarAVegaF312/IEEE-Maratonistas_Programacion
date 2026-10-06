"""
Matemáticas — Función φ de Euler y teorema de Euler («Euler's totient function»)
Nivel: Intermedio
Ejecutar: python phi_euler.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    φ(n) = cuántos k en 1..n son coprimos con n. Aparece al contar
    fracciones irreducibles, pares con gcd dado, y sobre todo para REDUCIR
    EXPONENTES: si gcd(a, m) = 1, a^b ≡ a^(b mod φ(m)) (mód m).
    Señales en el enunciado: «cuántos números ≤ n son coprimos con n»,
    «fracciones irreducibles con denominador n», «cuántos pares (i, j) con
    gcd(i, j) = 1», «gcd(a, n) = d» (= φ(n/d) de ellos), torres de
    potencias a^(b^c) mod m, «el período de a^k mod m divide a…».

FUNCIÓN
    phi(n) -> int                   φ(n) por división de prueba, n ≥ 1.
    criba_phi(N) -> list            φ(i) para 0 ≤ i ≤ N (φ(0) = 0).
    potencia_exp_grande(a, b, m)    a^b mod m reduciendo b con φ(m), válido
                                    para CUALQUIER a (teorema de Euler
                                    generalizado); b ≥ 0 puede ser enorme.

IDEA Y ALGORITMO
    Fórmula: si n = Π p^e, entonces φ(n) = n · Π_{p | n} (1 − 1/p).
    Justificación: un k en 1..n NO es coprimo con n si y solo si lo divide
    algún primo p de n. Para p^e: los no coprimos son los múltiplos de p
    (p^(e−1) de ellos), así que φ(p^e) = p^e − p^(e−1) = p^e(1 − 1/p).
    φ es multiplicativa (φ(a·b) = φ(a)·φ(b) si gcd(a, b) = 1) por el teorema
    chino del resto: k mod a·b ↔ (k mod a, k mod b) es una biyección, y k es
    coprimo con a·b si y solo si sus dos restos lo son con a y con b.
    Multiplicando sobre las potencias de primo sale la fórmula. En código,
    «res *= (1 − 1/p)» se hace exacto como res −= res // p.
    Criba: arrancar con φ[i] = i y, para cada primo p (detectado porque
    φ[p] sigue valiendo p), aplicar φ[k] −= φ[k] // p a todos sus múltiplos.
    Teorema de Euler: si gcd(a, m) = 1, a^φ(m) ≡ 1 (mód m). Prueba: sean
    r1, …, r_φ los residuos coprimos con m. Los a·r_i también son coprimos,
    y son distintos (a es invertible), así que son los mismos r_i en otro
    orden. Multiplicando todos: a^φ · Π r_i ≡ Π r_i y Π r_i es invertible:
    a^φ ≡ 1. (Fermat es el caso m primo, φ(p) = p − 1.)
    Consecuencia: a^b ≡ a^(b mod φ(m)) si gcd(a, m) = 1.
    Versión generalizada (sin pedir coprimalidad): si b ≥ φ(m), entonces
    a^b ≡ a^((b mod φ(m)) + φ(m)) (mód m). Idea: para cada potencia de primo
    p^e de m, si p | a, ambos lados son ≡ 0 mód p^e porque los dos
    exponentes son ≥ φ(m) ≥ φ(p^e) ≥ e; si p ∤ a, aplica Euler con
    φ(p^e) | φ(m). Por el TCR vale módulo m. Si b < φ(m) se calcula directo.

MACROALGORITMO
    φ(n):
    1. res = n; para p = 2, 3, … con p·p ≤ n:
    2.     si p | n: quitar p de n por completo; res −= res // p.
    3. Si queda n > 1 (un primo grande): res −= res // n.
    Criba:
    4. φ = [0, 1, 2, …, N]; para p = 2..N: si φ[p] == p (primo), para cada
       múltiplo k de p: φ[k] −= φ[k] // p.
    Exponente gigante:
    5. f = φ(m); si b ≥ f, b' = b mod f + f; si no, b' = b.
    6. Devolver pow(a, b', m).

COMPLEJIDAD
    φ(n): O(√n). Criba: O(N log log N) (en Python N ≈ 10^6 en ~1 s).
    Exponente gigante: O(√m + log b) (más el costo de calcular b si viene de
    otra potencia; para torres se aplica recursivamente con φ(φ(m)) …,
    que llega a 1 en O(log m) niveles).

EJEMPLO A MANO
    φ(36): 36 = 2²·3² → 36 · (1/2) · (2/3) = 12.
      En código: res = 36 → p = 2: res = 36 − 18 = 18 → p = 3: res = 18 − 6 = 12.
      Coprimos con 36 en 1..36: 1 5 7 11 13 17 19 23 25 29 31 35 (12) ✓.
    Euler: φ(10) = 4, 3^4 = 81 ≡ 1 (mód 10) ✓.
    3^(10^18) mod 10 = 3^(10^18 mod 4) = 3^0 = 1.
    Generalizado: 2^100 mod 12, φ(12) = 4: 2^(100 mod 4 + 4) = 2^4 = 16 ≡ 4,
      y en efecto 2^100 ≡ 4 (mód 12) (gcd(2, 12) ≠ 1, la versión simple daría
      2^0 = 1, que es INCORRECTO).

ERRORES TÍPICOS
    - Reducir el exponente con φ(m) cuando gcd(a, m) ≠ 1 usando la versión
      simple: falla (ver ejemplo). Usar la generalizada (+ φ(m)).
    - Reducir el exponente módulo m en vez de módulo φ(m).
    - Usar res * (p − 1) // p en vez de res // p * (p − 1): ambos son
      exactos en Python; en C++ el primero puede desbordar.
    - Olvidar el factor primo grande que queda al final de la división de
      prueba.
    - φ(1) = 1 (el 1 es coprimo consigo mismo).

VARIANTES Y RELACIONADOS
    - Σ_{d | n} φ(d) = n (agrupar k ≤ n por gcd(k, n)).
    - Número de fracciones irreducibles en (0, 1] con denominador ≤ N
      (sucesión de Farey): Σ_{k ≤ N} φ(k).
    - Pares 1 ≤ i ≤ n con gcd(i, n) = d: φ(n/d).
    - Criba lineal (calcula φ junto con el spf): criba_eratostenes.py.
    - Exponenciación: exponenciacion_rapida.py; Fermat: aritmetica_modular.py.
    - Orden multiplicativo de a (divide a φ(m)) y logaritmo discreto:
      logaritmo_discreto.py.

DÓNDE PRACTICAR
    - En los problemas del repo no aparece directamente.
    - CSES «Exponentiation II» (a^(b^c) mod p: el exponente se reduce
      módulo p − 1 = φ(p))
    - Codeforces 1295D «Same GCDs» (la respuesta es φ(m / gcd(a, m)))

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (contar k con gcd(k, n) = 1) para todo
      n ≤ 2000 (individual y criba), 200 n aleatorios hasta 10^10 contra la
      fórmula con la factorización, teorema de Euler en 2000 pares
      aleatorios, y potencia_exp_grande contra pow(a, b, m) con b hasta
      10^50 para todo tipo de a y m (python phi_euler.py)
"""
import math
import random


def phi(n):
    """φ(n) = n · prod (1 - 1/p) sobre los primos p | n, en O(√n)."""
    res = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            res -= res // p         # res *= (1 - 1/p), exacto
        p += 1
    if n > 1:                       # queda un primo grande
        res -= res // n
    return res


def criba_phi(N):
    """φ(i) para todo 0 <= i <= N, en O(N log log N)."""
    f = list(range(N + 1))
    for p in range(2, N + 1):
        if f[p] == p:               # nadie lo tocó: p es primo
            for k in range(p, N + 1, p):
                f[k] -= f[k] // p
    return f


def potencia_exp_grande(a, b, m):
    """a^b mod m para cualquier a (Euler generalizado): reduce b módulo φ(m)."""
    f = phi(m)
    if b >= f:
        b = b % f + f               # el "+ f" hace que valga aunque gcd(a, m) != 1
    return pow(a, b, m)


def demo():
    print("phi(36) =", phi(36))                           # 12
    print("phi(i), i=1..12:", criba_phi(12)[1:])
    print("3^phi(10) mod 10 =", pow(3, phi(10), 10))      # 1 (teorema de Euler)
    print("3^(10^18) mod 10 =", potencia_exp_grande(3, 10**18, 10))   # 1
    print("2^100 mod 12 =", potencia_exp_grande(2, 100, 12), "(pow:", pow(2, 100, 12), ")")


def pruebas():
    random.seed(1295)

    # Casos borde
    assert phi(1) == 1 and phi(2) == 1 and phi(1000000007) == 1000000006
    assert criba_phi(1) == [0, 1] and criba_phi(0) == [0]
    assert potencia_exp_grande(5, 0, 1) == 0 and potencia_exp_grande(0, 0, 7) == 1

    # Fuerza bruta: contar los k con gcd(k, n) = 1
    N = 2000
    cr = criba_phi(N)
    for n in range(1, N + 1):
        bruto = sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
        assert phi(n) == bruto == cr[n]
        # identidad: suma de φ(d) sobre los divisores de n es n
        if n <= 300:
            assert sum(cr[d] for d in range(1, n + 1) if n % d == 0) == n

    # Números grandes contra la fórmula con la factorización (independiente)
    for _ in range(200):
        n = random.randint(1, 10**10) if random.random() < 0.5 else random.randint(1, 10**5) ** 2
        x, primos, p = n, [], 2
        while p * p <= x:
            if x % p == 0:
                primos.append(p)
                while x % p == 0:
                    x //= p
            p += 1
        if x > 1:
            primos.append(x)
        esperado = n
        for q in primos:
            esperado = esperado // q * (q - 1)
        assert phi(n) == esperado

    # Teorema de Euler
    for _ in range(2000):
        m = random.randint(1, 10**6)
        a = random.randint(0, 10**9)
        if math.gcd(a, m) == 1:
            assert pow(a, phi(m), m) == 1 % m

    # Euler generalizado contra pow con exponentes enormes, cualquier a
    for i in range(2000):
        m = random.randint(1, 3000) if i % 20 else random.randint(1, 10**9)
        a = random.choice([random.randint(0, 10**9), 2 ** random.randint(0, 20), 6, 0, m])
        b = random.choice([random.randint(0, 50), random.randint(0, 10**50)])
        assert potencia_exp_grande(a, b, m) == pow(a, b, m)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
