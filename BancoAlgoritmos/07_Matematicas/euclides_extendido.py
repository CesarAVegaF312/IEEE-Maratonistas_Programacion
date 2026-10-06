"""
Matemáticas — Euclides extendido e inverso modular («Extended Euclidean algorithm», «modular inverse»)
Nivel: Intermedio
Ejecutar: python euclides_extendido.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Además de g = gcd(a, b), encontrar enteros x, y con a·x + b·y = g
    (identidad de Bézout). Con eso se calcula el inverso de a módulo m
    aunque m NO sea primo, y se resuelven ecuaciones a·x + b·y = c y
    congruencias a·x ≡ c (mód m).
    Señales en el enunciado: «dividir» módulo un m que no es primo; «s tal
    que p·s ≡ 1 (mód q)»; combinar dos tipos de pasos/pesas/monedas para
    llegar exactamente a un valor; sistemas de congruencias (TCR).

FUNCIÓN
    euclides_extendido(a, b) -> (g, x, y)   a·x + b·y = g = gcd(a, b), a, b ≥ 0.
    inverso_mod(a, m) -> int                x en [0, m) con a·x ≡ 1 (mód m);
                                            −1 si no existe (gcd(a, m) ≠ 1).
    inversos_hasta(n, p) -> list            inv[i] = i^(−1) mod p, 1 ≤ i ≤ n < p,
                                            p primo, en O(n).
    En Python ≥ 3.8: pow(a, -1, m) da el inverso (lanza ValueError si no existe).

IDEA Y ALGORITMO
    Euclides calcula la sucesión de restos r0 = a, r1 = b, r_{k+1} =
    r_{k−1} − q_k·r_k (con q_k = r_{k−1} // r_k) hasta llegar a 0; el último
    resto no nulo es g. La versión extendida guarda, para cada resto, una
    combinación r_k = a·x_k + b·y_k:
        r0 = a = a·1 + b·0,   r1 = b = a·0 + b·1,
    y como r_{k+1} = r_{k−1} − q_k·r_k, los coeficientes cumplen la MISMA
    recurrencia: x_{k+1} = x_{k−1} − q_k·x_k (igual con y). Invariante:
    r = a·x + b·y para los dos restos activos. Al terminar, g = a·x + b·y.
    Cotas: |x| ≤ b/g y |y| ≤ a/g (los coeficientes no crecen
    descontroladamente), así que caben en 64 bits si a, b lo hacen.
    Inverso: a·x ≡ 1 (mód m) ⇔ a·x + m·y = 1 para algún y. Si gcd(a, m) = 1,
    Euclides extendido da ese x. Si g = gcd(a, m) > 1, el lado izquierdo es
    múltiplo de g y no puede valer 1: no hay inverso.
    Inversos de 1..n con p primo en O(n): escribir p = q·i + r (q = p // i,
    r = p mod i < i). Módulo p: 0 ≡ q·i + r ⇒ multiplicando por
    i^(−1)·r^(−1): i^(−1) ≡ −q·r^(−1). Como r < i, inv[r] ya se calculó.
    Comparado con Fermat (a^(p−2)), Euclides extendido no necesita que el
    módulo sea primo y cuesta igual O(log m).

MACROALGORITMO
    1. (r0, x0, y0) = (a, 1, 0);  (r1, x1, y1) = (b, 0, 1).
    2. Mientras r1 ≠ 0:
    3.     q = r0 // r1.
    4.     (r0, r1) = (r1, r0 − q·r1); igual con (x0, x1) y (y0, y1).
    5. Devolver (r0, x0, y0).
    Inverso de a mód m:
    6. (g, x, _) = euclides_extendido(a mod m, m); si g ≠ 1 → no existe.
    7. Si no, devolver x mod m.

COMPLEJIDAD
    O(log min(a, b)) iteraciones, igual que Euclides; memoria O(1).
    inversos_hasta: O(n). pow(a, -1, m) nativo es lo más rápido en Python.

EJEMPLO A MANO
    euclides_extendido(240, 46):
      r      q    x     y
      240         1     0
      46     5    0     1
      10     4    1    -5      (240 − 5·46)
      6      1   -4    21      (46 − 4·10)
      4      1    5   -26
      2      2   -9    47
      0
    g = 2 y 240·(−9) + 46·47 = −2160 + 2162 = 2 ✓.
    inverso_mod(3, 7): 3·5 = 15 ≡ 1 → 5.  inverso_mod(4, 6): gcd = 2 → −1.

ERRORES TÍPICOS
    - Devolver x sin normalizar: puede ser negativo. Usar x % m.
    - Pedir el inverso sin verificar gcd(a, m) = 1 (pow(a, -1, m) lanza
      ValueError; en C++ se obtiene basura silenciosa).
    - Usar Fermat (a^(m−2)) con m no primo: da un valor incorrecto.
    - Versión recursiva intercambiando mal x e y al regresar
      (x = y', y = x' − (a // b)·y'). La iterativa evita ese error.
    - inversos_hasta con n ≥ p: el inverso de p (≡ 0) no existe.

VARIANTES Y RELACIONADOS
    - Ecuación a·x + b·y = c y conteo de soluciones: diofantica_lineal.py.
    - Congruencia lineal a·x ≡ c (mód m): solución si g | c, única módulo m/g.
    - Combinar congruencias: teorema_chino_resto.py.
    - Inverso por Fermat (m primo): aritmetica_modular.py.
    - gcd simple: gcd_lcm.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/E - Rational Coins (s ≡ ±p^(−1) mód q, inverso modular)
    - ICPC/Colombia 2017/B - Balance Game (Euclides extendido para la
      solución particular)
    - ICPC/Colombia 2025/I - Impossible Primebox (residuo −β·α^(−1) mód P)
    - Codeforces 7C «Line»

VERIFICACIÓN
    - Pruebas: OK en 3000 pares aleatorios (identidad a·x + b·y = g, g igual
      a math.gcd, cotas |x| ≤ b/g, |y| ≤ a/g), inverso contra búsqueda
      exhaustiva para todo m ≤ 150 y contra pow(a, -1, m) con m grandes no
      primos, e inversos_hasta contra pow (python euclides_extendido.py)
"""
import math
import random


def euclides_extendido(a, b):
    """(g, x, y) con a*x + b*y = g = gcd(a, b), para a, b >= 0."""
    r0, x0, y0 = a, 1, 0        # invariante: r0 = a*x0 + b*y0
    r1, x1, y1 = b, 0, 1        #             r1 = a*x1 + b*y1
    while r1:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1        # el paso de Euclides...
        x0, x1 = x1, x0 - q * x1        # ...aplicado igual a los coeficientes
        y0, y1 = y1, y0 - q * y1
    return r0, x0, y0


def inverso_mod(a, m):
    """x en [0, m) con a*x ≡ 1 (mod m); -1 si gcd(a, m) != 1."""
    g, x, _ = euclides_extendido(a % m, m)
    if g != 1:
        return -1
    return x % m


def inversos_hasta(n, p):
    """inv[i] = i^(-1) mod p para 1 <= i <= n (p primo, n < p), en O(n)."""
    inv = [0] * (n + 1)
    if n >= 1:
        inv[1] = 1
    for i in range(2, n + 1):
        # p = (p // i)*i + (p % i)  =>  i^(-1) ≡ -(p // i) * (p % i)^(-1)
        inv[i] = (p - p // i) * inv[p % i] % p
    return inv


def demo():
    g, x, y = euclides_extendido(240, 46)
    print(f"euclides_extendido(240, 46) = ({g}, {x}, {y}) -> 240*{x} + 46*{y} = {240 * x + 46 * y}")
    print("inverso_mod(3, 7) =", inverso_mod(3, 7))        # 5
    print("inverso_mod(4, 6) =", inverso_mod(4, 6))        # -1
    print("inverso_mod(7, 10**9) =", inverso_mod(7, 10**9), "(módulo NO primo)")
    print("inversos 1..6 mod 7:", inversos_hasta(6, 7)[1:])   # [1, 4, 5, 2, 3, 6]


def pruebas():
    random.seed(77)

    # Casos borde
    assert euclides_extendido(0, 0) == (0, 1, 0)
    g, x, y = euclides_extendido(0, 5)
    assert g == 5 and 0 * x + 5 * y == 5
    g, x, y = euclides_extendido(5, 0)
    assert g == 5 and 5 * x == 5
    assert inverso_mod(1, 1) == 0          # módulo 1: todo es 0 ≡ 1
    assert inverso_mod(0, 7) == -1 and inverso_mod(-3, 7) == 2   # -3 ≡ 4, 4·2 = 8 ≡ 1

    # Identidad de Bézout y cotas de los coeficientes
    for _ in range(3000):
        a = random.randint(0, 10**18) if random.random() < 0.5 else random.randint(0, 100)
        b = random.randint(0, 10**18) if random.random() < 0.5 else random.randint(0, 100)
        g, x, y = euclides_extendido(a, b)
        assert g == math.gcd(a, b) and a * x + b * y == g
        if a > 0 and b > 0:
            assert abs(x) <= b // g and abs(y) <= a // g

    # Inverso contra búsqueda exhaustiva
    for m in range(1, 151):
        for a in range(-m, 2 * m):
            bruto = next((x for x in range(m) if a * x % m == 1 % m), -1)
            assert inverso_mod(a, m) == bruto

    # Contra pow(a, -1, m) con módulos grandes (primos o no)
    for _ in range(2000):
        m = random.randint(2, 10**18)
        a = random.randint(0, 10**18)
        try:
            esperado = pow(a, -1, m)
        except ValueError:
            esperado = -1
        assert inverso_mod(a, m) == esperado

    # Inversos de 1..n en O(n)
    for p in (2, 3, 7, 101, 998244353, 10**9 + 7):
        n = min(p - 1, 3000)
        inv = inversos_hasta(n, p)
        assert all(inv[i] == pow(i, -1, p) for i in range(1, n + 1))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
