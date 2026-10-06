"""
Matemáticas — Factorización en primos: división de prueba y menor factor primo («Prime factorization», «trial division», «SPF»)
Nivel: Intermedio
Ejecutar: python factorizacion.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Escribir n = p1^e1 · p2^e2 · … · pk^ek. Casi toda pregunta sobre
    divisores, gcd/lcm de muchos números, φ de Euler o «¿es un cuadrado
    perfecto / cubo?» se responde mirando los exponentes.
    Señales en el enunciado: «número de divisores», «suma de divisores»,
    «exponente del primo p en n!», «producto de los números es un cuadrado»,
    «primos distintos de n»; un solo n ≤ 10^12 (división de prueba) o
    MUCHOS n ≤ 10^7 (menor factor primo precalculado).
    Si n llega a 10^18 → miller_rabin_pollard.py.

FUNCIÓN
    factorizar(n) -> list[(p, e)]        primos en orden creciente con su
                                         exponente; n = 1 → [].  (n ≥ 1)
    construir_spf(limite) -> list        spf[i] = menor factor primo de i.
    factorizar_spf(n, spf) -> list[(p, e)]   igual que factorizar, n ≤ limite.
    exponente_en_factorial(n, p) -> int  exponente de p (primo) en n!.

IDEA Y ALGORITMO
    Teorema fundamental de la aritmética: la factorización en primos existe
    y es única (salvo el orden).
    División de prueba: probar d = 2, 3, 4, … y, cada vez que d divide a n,
    dividir n por d TODAS las veces posibles (contando el exponente).
    - Cada d que divide al n restante es primo: si d = a·b con 1 < a < d,
      el factor a ya se habría quitado por completo al probar a, así que a
      no divide al n restante y d tampoco.
    - Basta probar d·d ≤ n (n el restante): si el n restante no tiene
      divisores ≤ √n, es 1 o es primo (un compuesto tiene un factor ≤ su
      raíz). Ese primo «grande» (a lo sumo uno) se agrega al final.
    Menor factor primo (SPF): con una criba se guarda spf[i]; entonces
    n = spf[n] · (n / spf[n]) y se repite con n / spf[n]. Cada división al
    menos parte n a la mitad: O(log n) pasos por número tras precalcular.
    Exponente de p en n! (Legendre): entre 1..n hay ⌊n/p⌋ múltiplos de p,
    ⌊n/p²⌋ múltiplos de p², …; cada múltiplo de p^k aporta 1 en el término
    k, así que v_p(n!) = Σ_k ⌊n/p^k⌋. Sin factorizar n!.

MACROALGORITMO
    División de prueba:
    1. d = 2; mientras d·d ≤ n:
    2.     si d | n: contar e = cuántas veces se divide n por d; anotar (d, e).
    3.     d += 1 (o probar 2 y luego solo impares).
    4. Si queda n > 1, es primo: anotar (n, 1).
    SPF:
    5. Precalcular spf con criba hasta el máximo valor.
    6. Mientras n > 1: p = spf[n]; dividir n por p mientras se pueda; anotar.

COMPLEJIDAD
    División de prueba: O(√n) por número (peor caso: n primo o p·q con p, q
    cercanos). En Python, n ≈ 10^12 en ~0,1 s; para muchos n así no alcanza.
    SPF: precálculo O(N log log N) (N ≤ ~10^7 en Python, con bastante
    memoria), y O(log n) por consulta.

EJEMPLO A MANO
    n = 360:
      d = 2: 360 → 180 → 90 → 45  (e = 3)
      d = 3: 45 → 15 → 5           (e = 2)
      d = 4: 4·4 = 16 > 5: se para. Queda 5 > 1 → (5, 1).
    360 = 2^3 · 3^2 · 5.
    Con SPF: spf[360] = 2, spf[45] = 3, spf[5] = 5 → mismo resultado.
    v_2(10!) = ⌊10/2⌋ + ⌊10/4⌋ + ⌊10/8⌋ = 5 + 2 + 1 = 8.

ERRORES TÍPICOS
    - Olvidar el primo grande que queda al final (n > 1 tras el bucle):
      p. ej. 2·10^9+14 = 2 · 1000000007 perdería el 1000000007.
    - Comparar d·d ≤ n con el n ORIGINAL en vez del que va quedando: correcto
      pero mucho más lento.
    - Factorizar 10^5 números de hasta 10^7 con división de prueba: TLE.
      Precalcular spf.
    - spf como lista de Python de 10^7 enteros: ~80 MB o más; con límites
      así considerar array('i') o solo factorizar con los primos ≤ √max.
    - Calcular n! y luego factorizarlo (gigante): usar Legendre.

VARIANTES Y RELACIONADOS
    - Criba y criba lineal (spf): criba_eratostenes.py.
    - Contar / sumar / listar divisores desde la factorización: divisores.py.
    - φ de Euler desde la factorización: phi_euler.py.
    - n hasta 10^18: Miller–Rabin + Pollard-Rho (miller_rabin_pollard.py).
    - gcd/lcm de muchos números: mínimo/máximo de exponentes por primo.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/B - Between Ceiling and Floor (primero se quitan
      los primos < 1000 por división, luego Pollard-Rho)
    - Codeforces 26A «Almost Prime»
    - CSES «Counting Divisors» (con spf)

VERIFICACIÓN
    - Pruebas: OK para todo n ≤ 5000 contra una factorización bruta
      (quitar el menor divisor, buscado a mano), con 300 n aleatorios hasta
      10^10 (producto = n, factores primos, orden creciente), SPF contra
      división de prueba hasta 10^5, y Legendre contra contar el exponente
      en n! calculado (python factorizacion.py)
"""
import math
import random


def factorizar(n):
    """Lista [(p, e)] con n = prod p^e, p crecientes. División de prueba hasta √n."""
    res = []
    d = 2
    while d * d <= n:               # n es lo que QUEDA por factorizar
        if n % d == 0:
            e = 0
            while n % d == 0:       # quitar d por completo (así cada d hallado es primo)
                n //= d
                e += 1
            res.append((d, e))
        d += 1 if d == 2 else 2     # después del 2 solo impares
    if n > 1:                       # sin divisores <= su raíz: es primo
        res.append((n, 1))
    return res


def construir_spf(limite):
    """spf[i] = menor factor primo de i (spf[0] = spf[1] = 0)."""
    spf = list(range(limite + 1))
    spf[0] = 0
    if limite >= 1:
        spf[1] = 0
    for i in range(2, math.isqrt(limite) + 1):
        if spf[i] == i:                         # i es primo
            for j in range(i * i, limite + 1, i):
                if spf[j] == j:                 # aún no tiene un primo menor
                    spf[j] = i
    return spf


def factorizar_spf(n, spf):
    """Igual que factorizar(n) pero en O(log n) usando spf (n <= len(spf) - 1)."""
    res = []
    while n > 1:
        p = spf[n]
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        res.append((p, e))
    return res


def exponente_en_factorial(n, p):
    """Fórmula de Legendre: exponente del primo p en n! = sum n // p^k."""
    e = 0
    while n:
        n //= p
        e += n
    return e


def demo():
    print("factorizar(360) =", factorizar(360))                 # [(2, 3), (3, 2), (5, 1)]
    print("factorizar(2 * 1000000007) =", factorizar(2 * 1000000007))
    spf = construir_spf(1000)
    print("spf[360], spf[45], spf[5] =", spf[360], spf[45], spf[5])
    print("factorizar_spf(360) =", factorizar_spf(360, spf))
    print("exponente de 2 en 10! =", exponente_en_factorial(10, 2))   # 8


def pruebas():
    random.seed(4)

    def es_primo(x):
        return x >= 2 and all(x % d for d in range(2, math.isqrt(x) + 1))

    def bruto(n):
        # quitar repetidamente el menor divisor > 1 (buscado uno por uno)
        res = {}
        while n > 1:
            d = next(d for d in range(2, n + 1) if n % d == 0)
            res[d] = res.get(d, 0) + 1
            n //= d
        return sorted(res.items())

    # Casos borde
    assert factorizar(1) == [] and factorizar(2) == [(2, 1)] and factorizar(4) == [(2, 2)]
    assert factorizar(2 * 1000000007) == [(2, 1), (1000000007, 1)]
    assert factorizar(2**40) == [(2, 40)]
    assert factorizar(999983 * 999983) == [(999983, 2)]
    assert exponente_en_factorial(0, 2) == 0 and exponente_en_factorial(1, 5) == 0

    spf = construir_spf(100_000)
    for n in range(1, 5001):
        b = bruto(n)
        assert factorizar(n) == b == factorizar_spf(n, spf)

    # Aleatorios grandes: producto, primalidad y orden
    for _ in range(300):
        n = random.randint(1, 10**10) if random.random() < 0.7 else \
            random.choice([2, 3, 5, 7, 11, 13]) ** random.randint(1, 10) * random.randint(1, 10**6)
        f = factorizar(n)
        assert math.prod(p**e for p, e in f) == n
        assert all(es_primo(p) and e >= 1 for p, e in f)
        assert [p for p, _ in f] == sorted(set(p for p, _ in f))

    # SPF contra división de prueba en todo el rango
    for n in range(1, 100_001, 7):
        assert factorizar_spf(n, spf) == factorizar(n)

    # Legendre contra contar el exponente de p en n! calculado
    for n in range(0, 120):
        f = math.factorial(n)
        for p in (2, 3, 5, 7, 11, 13):
            e, x = 0, f
            while x % p == 0:
                x //= p
                e += 1
            assert exponente_en_factorial(n, p) == e


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
