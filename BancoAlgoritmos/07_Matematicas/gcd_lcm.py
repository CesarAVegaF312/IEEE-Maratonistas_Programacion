"""
Matemáticas — Máximo común divisor y mínimo común múltiplo («GCD / LCM», algoritmo de Euclides)
Nivel: Básico
Ejecutar: python gcd_lcm.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular el mayor entero que divide a dos (o más) números (gcd = mcd) y el
    menor entero positivo que es múltiplo de todos ellos (lcm = mcm), en
    O(log) pasos aunque los números sean de 10^18.
    Señales en el enunciado: «simplificar la fracción», «cada cuánto
    coinciden» (eventos periódicos → mcm), «el mayor tamaño de baldosa / grupo
    que divide exacto», «¿se puede formar c con pasos de a y b?» (→ gcd),
    fracciones irreducibles, ciclos que se sincronizan.

FUNCIÓN
    gcd(a, b) -> int        mcd de |a| y |b|; gcd(0, 0) = 0, gcd(a, 0) = |a|.
    lcm(a, b) -> int        mcm de |a| y |b|; 0 si alguno es 0.
    gcd_lista(v) -> int     mcd de toda la lista (0 si está vacía).
    lcm_lista(v) -> int     mcm de toda la lista (1 si está vacía).
    En Python ya existen: math.gcd(*args) y math.lcm(*args) (Python ≥ 3.9).

IDEA Y ALGORITMO
    Euclides: gcd(a, b) = gcd(b, a mod b), y gcd(a, 0) = a.
    Por qué: si a = q·b + r, todo d que divide a «a» y a «b» divide a
    r = a − q·b; y todo d que divide a «b» y a «r» divide a a = q·b + r. Los
    pares (a, b) y (b, r) tienen EXACTAMENTE los mismos divisores comunes,
    así que su máximo es el mismo. Cuando el segundo número llega a 0, el
    mayor divisor de (g, 0) es g.
    Por qué es rápido: tras dos pasos el primer número se reduce al menos a
    la mitad (si b ≤ a/2, entonces r < b ≤ a/2; si b > a/2, r = a − b < a/2).
    Son ≤ 2·log2(min) iteraciones (el peor caso son Fibonacci consecutivos —
    teorema de Lamé). El ingenuo (probar todos los d desde min(a, b) hacia
    abajo) es O(min(a, b)): imposible con 10^18.
    mcm: si g = gcd(a, b), a = g·a', b = g·b' con gcd(a', b') = 1, el menor
    múltiplo común es g·a'·b', es decir lcm(a, b) = a / g · b. (Equivalente:
    gcd·lcm = a·b, porque por cada primo gcd toma el exponente mínimo y lcm
    el máximo, y mín + máx = suma.) Se divide ANTES de multiplicar para no
    desbordar en C++/Java.
    Varios números: gcd y lcm son asociativos, así que se acumulan de
    izquierda a derecha: gcd(a, b, c) = gcd(gcd(a, b), c).

MACROALGORITMO
    1. Tomar valores absolutos (el gcd siempre se define no negativo).
    2. Mientras b ≠ 0: (a, b) = (b, a mod b).
    3. Devolver a.
    4. mcm: si alguno es 0 → 0; si no, a // gcd(a, b) * b.
    5. Para una lista: acumular con gcd (desde 0) o con lcm (desde 1).

COMPLEJIDAD
    gcd: O(log min(a, b)) divisiones; memoria O(1).
    En Python, ~10^6 gcd por segundo con math.gcd (está en C); con la
    versión escrita a mano, unas 3–5 veces menos.
    Ojo: el mcm de muchos números crece muy rápido (mcm(1..100) tiene 41
    cifras); en C++ desborda, en Python solo se vuelve lento.

EJEMPLO A MANO
    gcd(252, 105):
      (252, 105) → 252 mod 105 = 42 → (105, 42)
      (105, 42)  → 105 mod 42  = 21 → (42, 21)
      (42, 21)   → 42 mod 21   = 0  → (21, 0)  → gcd = 21
    lcm(252, 105) = 252 / 21 · 105 = 12 · 105 = 1260.
    gcd_lista([12, 18, 30]) = gcd(gcd(12, 18), 30) = gcd(6, 30) = 6.

ERRORES TÍPICOS
    - Calcular lcm como a * b / g en C++: a·b desborda antes de dividir.
      Escribir a / g * b.
    - Usar / (división real) en Python en vez de //: lcm queda float y pierde
      precisión pasando de 2^53.
    - Olvidar los negativos: en C++ a % b puede ser negativo; tomar abs()
      al inicio. (math.gcd ya devuelve siempre no negativo.)
    - Inicializar mal el acumulado: gcd de una lista empieza en 0
      (gcd(0, x) = x), lcm empieza en 1.
    - Recursión gcd(b, a % b) sin caso base b == 0 → división por cero.

VARIANTES Y RELACIONADOS
    - Euclides extendido (coeficientes x, y con a·x + b·y = gcd):
      euclides_extendido.py. Ecuaciones a·x + b·y = c: diofantica_lineal.py.
    - Simplificar fracción p/q: dividir ambos por gcd(p, q).
    - gcd en rangos de un arreglo: tabla dispersa o árbol de segmentos (es
      idempotente y asociativo).
    - gcd(F_m, F_n) = F_gcd(m, n) para Fibonacci; gcd(2^a − 1, 2^b − 1) =
      2^gcd(a, b) − 1.

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/J - Jawbreaking Candy (reducir fracciones con gcd)
    - ICPC/Colombia 2017/B - Balance Game (existencia de solución: gcd | R)
    - CSES «Common Divisors»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (probar todos los divisores / todos los
      múltiplos) en 3000 pares aleatorios, contra math.gcd/math.lcm en 3000
      pares grandes y listas aleatorias, más casos borde con 0 y negativos
      (python gcd_lcm.py)
"""
import math
import random


def gcd(a, b):
    """Máximo común divisor de |a| y |b| (Euclides iterativo)."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b     # los divisores comunes de (a, b) y (b, a mod b) son los mismos
    return a


def lcm(a, b):
    """Mínimo común múltiplo de |a| y |b| (0 si alguno es 0)."""
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd(a, b) * abs(b)     # dividir ANTES de multiplicar


def gcd_lista(v):
    """mcd de todos los elementos (0 para la lista vacía, neutro del gcd)."""
    g = 0
    for x in v:
        g = gcd(g, x)
        if g == 1:          # ya no puede bajar más: cortar temprano
            break
    return g


def lcm_lista(v):
    """mcm de todos los elementos (1 para la lista vacía, neutro del lcm)."""
    m = 1
    for x in v:
        m = lcm(m, x)
    return m


def demo():
    print("gcd(252, 105) =", gcd(252, 105))                 # 21
    print("lcm(252, 105) =", lcm(252, 105))                 # 1260
    print("gcd_lista([12, 18, 30]) =", gcd_lista([12, 18, 30]))   # 6
    print("lcm_lista([4, 6, 10]) =", lcm_lista([4, 6, 10]))       # 60
    p, q = 84, 126
    g = gcd(p, q)
    print(f"{p}/{q} simplificada = {p // g}/{q // g}")      # 2/3


def pruebas():
    random.seed(2024)

    # Casos borde
    assert gcd(0, 0) == 0 and gcd(0, 7) == 7 and gcd(7, 0) == 7
    assert gcd(-12, 18) == 6 and gcd(12, -18) == 6 and gcd(-12, -18) == 6
    assert lcm(0, 5) == 0 and lcm(-4, 6) == 12 and lcm(1, 1) == 1
    assert gcd_lista([]) == 0 and lcm_lista([]) == 1
    assert gcd_lista([5]) == 5 and lcm_lista([5]) == 5
    assert gcd(10**18, 10**18 - 1) == 1
    # Peor caso de Euclides: Fibonacci consecutivos
    f0, f1 = 1, 1
    for _ in range(85):
        f0, f1 = f1, f0 + f1
    assert gcd(f1, f0) == 1

    # Fuerza bruta: el mayor d que divide a ambos, el menor múltiplo común
    for _ in range(3000):
        a = random.randint(0, 200)
        b = random.randint(0, 200)
        if a == 0 and b == 0:
            continue
        g_bruto = max(d for d in range(1, max(a, b) + 1) if a % d == 0 and b % d == 0)
        assert gcd(a, b) == g_bruto
        assert gcd(-a, b) == g_bruto
        if a > 0 and b > 0:
            # recorrer los múltiplos de a hasta el primero que también lo sea de b
            m_bruto = next(m for m in range(a, a * b + 1, a) if m % b == 0)
            assert lcm(a, b) == m_bruto

    # Contra la biblioteca estándar con números grandes y listas
    for _ in range(3000):
        a = random.randint(-10**18, 10**18)
        b = random.randint(-10**18, 10**18)
        assert gcd(a, b) == math.gcd(a, b)
        assert lcm(a, b) == math.lcm(a, b)
        v = [random.choice([2, 3, 4, 6, 9, 12, 35]) * random.randint(1, 50)
             for _ in range(random.randint(0, 6))]
        assert gcd_lista(v) == math.gcd(*v)
        assert lcm_lista(v) == math.lcm(*v)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
