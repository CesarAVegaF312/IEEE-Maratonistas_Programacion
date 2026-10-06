"""
Matemáticas — Aritmética modular («Modular arithmetic»)
Nivel: Básico
Ejecutar: python aritmetica_modular.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Hacer cuentas con números que serían gigantes guardando solo su resto
    módulo m. Casi todo problema de conteo pide «la respuesta módulo
    10^9 + 7» porque el resultado real tiene miles de cifras.
    Señales en el enunciado: «imprima la respuesta módulo 10^9 + 7 / 998244353»;
    «el resto de dividir este número de 10^5 dígitos entre m»; «P/Q como
    P·Q^(−1) mod p»; restos que se repiten (palomar sobre los m restos).

FUNCIÓN
    suma_mod(a, b, m), resta_mod(a, b, m), mul_mod(a, b, m) -> int en [0, m)
    inverso_fermat(a, p) -> int     a^(−1) mod p, p PRIMO y a ≢ 0 (mód p).
    div_mod(a, b, p) -> int         a · b^(−1) mod p (p primo, b ≢ 0).
    resto_c(a, m) -> int            el resto como lo da C++/Java (signo de a).
    horner_mod(digitos, base, m)    valor del número escrito en «digitos»
                                    (cadena o lista) módulo m.

IDEA Y ALGORITMO
    Por qué se puede reducir en cada paso: si a = q1·m + r1 y b = q2·m + r2,
        a + b = (q1 + q2)·m + (r1 + r2)           → (a+b) ≡ r1 + r2
        a − b = (q1 − q2)·m + (r1 − r2)           → (a−b) ≡ r1 − r2
        a · b = (q1·q2·m + q1·r2 + q2·r1)·m + r1·r2 → (a·b) ≡ r1 · r2
    Los términos múltiplos de m no cambian el resto, así que se puede
    reemplazar cada número por su resto ANTES de operar. Por inducción,
    cualquier expresión con +, −, · da lo mismo reduciendo al final o en
    cada paso (y en cada paso los números quedan < m²).
    La DIVISIÓN no se reduce así: 6 ≡ 2 (mód 4) pero 6/2 = 3 y 2/2 = 1.
    Dividir por b es multiplicar por un b' con b·b' ≡ 1 (el inverso), que
    existe si y solo si gcd(b, m) = 1.
    Pequeño teorema de Fermat: si p es primo y p ∤ a, a^(p−1) ≡ 1 (mód p).
    Prueba: los números a·1, a·2, …, a·(p−1) son distintos módulo p (si
    a·i ≡ a·j entonces p | a·(i − j), y como p ∤ a, p | i − j, imposible si
    i ≠ j) y ninguno es 0, así que son 1, 2, …, p−1 en otro orden.
    Multiplicándolos todos: a^(p−1)·(p−1)! ≡ (p−1)! y, como (p−1)! no es
    múltiplo de p, se cancela: a^(p−1) ≡ 1. Por tanto a·a^(p−2) ≡ 1, es
    decir a^(−1) ≡ a^(p−2) (mód p), que se calcula con exponenciación
    rápida en O(log p).
    Negativos: Python define a % m con el signo de m (siempre en [0, m) si
    m > 0): (−7) % 3 = 2. C++/Java truncan hacia cero: −7 % 3 = −1. En
    C++ hay que normalizar: ((a % m) + m) % m.

MACROALGORITMO
    1. Normalizar las entradas a [0, m) con % m.
    2. Sumar/restar/multiplicar y aplicar % m después de CADA operación.
    3. Para dividir por b (m primo): multiplicar por pow(b, m − 2, m).
    4. Para un número dado como cadena: Horner, r = (r·base + dígito) % m.
    5. Al imprimir, asegurarse de que el resultado está en [0, m).

COMPLEJIDAD
    +, −, · : O(1). Inverso por Fermat: O(log p). Horner: O(número de
    dígitos). En Python los enteros nunca desbordan, pero reducir en cada
    paso mantiene los números chicos (si no, cada operación se vuelve lenta).

EJEMPLO A MANO
    m = 7:  (5 + 4) mod 7 = 2;  (3 − 5) mod 7 = −2 → 5;  (6 · 5) mod 7 = 30 mod 7 = 2.
    Inverso de 3 módulo 7: 3^(7−2) = 3^5 = 243 = 34·7 + 5 → 5; 3·5 = 15 ≡ 1 ✓.
    12 / 3 mod 7 = 12·5 mod 7 = 60 mod 7 = 4 = 12/3 ✓.
    "1234" mod 7 por Horner: 1 → (1·10+2)=12≡5 → (5·10+3)=53≡4 → (4·10+4)=44≡2.
    1234 = 176·7 + 2 ✓.

ERRORES TÍPICOS
    - En C++/Java, a − b puede dar negativo: escribir (a − b + m) % m o
      ((a − b) % m + m) % m.
    - En C++, a·b con a, b < 10^9+7 en int desborda: usar long long (cabe
      porque (10^9+7)^2 < 9,2·10^18).
    - Dividir con / después de haber reducido: el resultado es basura. Usar
      el inverso modular.
    - Fermat con m NO primo (p. ej. 10^9 o 2^32): no vale. Usar Euclides
      extendido (euclides_extendido.py) y verificar gcd(b, m) = 1.
    - Restar dos resultados ya reducidos y comparar con 0 sin normalizar.
    - Escribir 1e9+7 en Python: es float. Usar 10**9 + 7.

VARIANTES Y RELACIONADOS
    - Exponenciación rápida: exponenciacion_rapida.py.
    - Inverso con módulo no primo e inversos 1..n en O(n): euclides_extendido.py.
    - Reducir exponentes módulo φ(m) (teorema de Euler): phi_euler.py.
    - Combinar restos de varios módulos: teorema_chino_resto.py.
    - Factoriales e inversos modulares para combinatoria: ver los archivos
      de combinatoria de esta carpeta.

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/B - Binary Dozens (Horner modular, H mod 12)
    - ICPC/Colombia 2026/K - Sample Median Preservation (P·Q^(−1) mod p con
      Fermat)
    - ICPC/Guangzhou 2017/F - Finding Paths (inverso modular de 2)
    - ICPC/Colombia 2024/H - Only1s0s (restos (10·r + d) mod N)
    - CSES «Exponentiation II»

VERIFICACIÓN
    - Pruebas: OK contra la cuenta exacta con enteros grandes de Python en
      3000 expresiones aleatorias, inverso contra búsqueda exhaustiva para
      todos los primos < 200, división exacta contra a // b, resto estilo C
      contra la definición por truncamiento, y Horner contra int(cadena)
      (python aritmetica_modular.py)
"""
import random

MOD = 10**9 + 7


def suma_mod(a, b, m=MOD):
    return (a + b) % m


def resta_mod(a, b, m=MOD):
    return (a - b) % m          # en Python % ya devuelve un valor en [0, m)


def mul_mod(a, b, m=MOD):
    return (a % m) * (b % m) % m


def inverso_fermat(a, p=MOD):
    """a^(-1) mod p con p primo y a no múltiplo de p: a^(p-2) (Fermat)."""
    a %= p
    if a == 0:
        raise ZeroDivisionError("0 no tiene inverso módulo p")
    return pow(a, p - 2, p)


def div_mod(a, b, p=MOD):
    """a / b módulo p (primo): a por el inverso de b."""
    return a % p * inverso_fermat(b, p) % p


def resto_c(a, m):
    """Resto como en C++/Java (truncamiento hacia cero): tiene el signo de a."""
    r = abs(a) % abs(m)
    return -r if a < 0 else r


def horner_mod(digitos, base, m):
    """Valor de la secuencia de dígitos (más significativo primero) módulo m."""
    r = 0
    for d in digitos:
        r = (r * base + int(d)) % m     # el número crece como r·base + d
    return r


def demo():
    m = 7
    print("(5 + 4) mod 7 =", suma_mod(5, 4, m))           # 2
    print("(3 - 5) mod 7 =", resta_mod(3, 5, m))          # 5
    print("(6 * 5) mod 7 =", mul_mod(6, 5, m))            # 2
    print("inverso de 3 mod 7 =", inverso_fermat(3, m))   # 5
    print("12 / 3 mod 7 =", div_mod(12, 3, m))            # 4
    print("Python: -7 % 3 =", -7 % 3, "| estilo C++: ", resto_c(-7, 3))   # 2 | -1
    print('"1234" mod 7 =', horner_mod("1234", 10, 7))     # 2
    print('binario "1101" mod 12 =', horner_mod("1101", 2, 12))   # 13 mod 12 = 1


def pruebas():
    random.seed(17)

    # Casos borde
    assert resta_mod(0, 1, 5) == 4 and suma_mod(4, 1, 5) == 0
    assert mul_mod(-1, -1, 5) == 1 and mul_mod(10**30, 10**30, MOD) == pow(10, 60, MOD)
    assert inverso_fermat(1, 2) == 1
    assert horner_mod("", 10, 7) == 0 and horner_mod("0", 10, 1) == 0
    try:
        inverso_fermat(14, 7)
        assert False, "debió fallar: 14 ≡ 0 (mód 7)"
    except ZeroDivisionError:
        pass

    # Reducir en cada paso == reducir al final (cuenta exacta con enteros grandes)
    for _ in range(3000):
        m = random.choice([2, 3, 7, 12, 1000, MOD, 998244353, random.randint(1, 10**12)])
        exacto = 0
        reducido = 0
        for _ in range(random.randint(1, 15)):
            x = random.randint(-10**15, 10**15)
            op = random.randint(0, 2)
            if op == 0:
                exacto, reducido = exacto + x, suma_mod(reducido, x, m)
            elif op == 1:
                exacto, reducido = exacto - x, resta_mod(reducido, x, m)
            else:
                exacto, reducido = exacto * x, mul_mod(reducido, x, m)
        assert reducido == exacto % m and 0 <= reducido < m

    # Inverso de Fermat contra búsqueda exhaustiva, para todos los primos < 200
    primos = [p for p in range(2, 200) if all(p % d for d in range(2, p))]
    for p in primos:
        for a in range(1, p):
            inv = inverso_fermat(a, p)
            assert inv == next(x for x in range(1, p) if a * x % p == 1)

    # División modular: si b divide a a, coincide con la división exacta
    for _ in range(2000):
        b = random.randint(1, 10**6)
        q = random.randint(-10**12, 10**12)
        a = b * q
        p = random.choice([MOD, 998244353])
        assert div_mod(a, b, p) == q % p
        assert div_mod(a, b, p) * b % p == a % p

    # Resto estilo C contra la definición a - m * trunc(a / m)
    for _ in range(2000):
        a = random.randint(-10**6, 10**6)
        m = random.randint(1, 1000)
        q_trunc = abs(a) // m * (1 if a >= 0 else -1)
        assert resto_c(a, m) == a - m * q_trunc
        assert (resto_c(a, m) + m) % m == a % m      # la normalización de C++

    # Horner contra int(cadena, base)
    for _ in range(1000):
        base = random.choice([2, 8, 10, 16])
        n = random.randint(0, 10**40)
        digitos = [int(c, 16) for c in (format(n, "b") if base == 2 else format(n, "o")
                   if base == 8 else str(n) if base == 10 else format(n, "x"))]
        m = random.randint(1, 10**9)
        assert horner_mod(digitos, base, m) == n % m


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
