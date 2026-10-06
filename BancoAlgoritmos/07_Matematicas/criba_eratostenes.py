"""
Matemáticas — Criba de Eratóstenes, criba lineal (SPF) y criba segmentada («Sieve of Eratosthenes»)
Nivel: Básico (criba lineal y segmentada: Intermedio)
Ejecutar: python criba_eratostenes.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Saber de golpe cuáles números hasta N son primos (N hasta ~10^7 en
    Python), obtener la lista de primos, o el MENOR FACTOR PRIMO de cada
    número (para factorizar muchos números en O(log n) cada uno). La versión
    segmentada lista los primos de un rango [L, R] con R hasta ~10^12 si
    R − L es pequeño (~10^6).
    Señales en el enunciado: MUCHAS consultas «¿es primo x?» con x ≤ 10^7;
    «los primeros k primos»; «cuántos primos hay hasta N»; factorizar todos
    los números de un arreglo con valores ≤ 10^6–10^7; «primos entre L y R»
    con R grande pero R − L chico.

FUNCIÓN
    criba(n) -> bytearray         es_primo[i] = 1 si i es primo (0 ≤ i ≤ n).
    primos_hasta(n) -> list       primos ≤ n en orden creciente.
    criba_lineal(n) -> (spf, primos)
        spf[i] = menor factor primo de i (spf[0] = spf[1] = 0), y la lista
        de primos ≤ n.
    criba_segmentada(lo, hi) -> list   primos en [lo, hi] (lo ≥ 0).

IDEA Y ALGORITMO
    Eratóstenes: recorrer i = 2, 3, …; si i no ha sido tachado es primo, y
    se tachan sus múltiples. Por qué es correcto: un compuesto n = a·b con
    1 < a ≤ b tiene un factor primo p ≤ a ≤ √n, así que queda tachado al
    procesar p; un primo nunca es múltiplo de un primo menor, así que nunca
    se tacha. Basta tachar desde p·p: un múltiplo k·p con k < p tiene un
    factor primo ≤ k < p y ya fue tachado. Por lo mismo basta procesar
    p ≤ √n.
    Costo: Σ_{p ≤ n} n/p = n·(1/2 + 1/3 + 1/5 + …) ≈ n·ln ln n (la suma de
    los inversos de los primos crece como ln ln n): prácticamente lineal.
    En Python el truco es tachar con asignación por rebanadas sobre un
    bytearray (es_primo[p*p::p] = ...), que corre en C.

    Criba lineal (menor factor primo, SPF): todo compuesto x se escribe de
    forma ÚNICA como x = p·i con p = spf(x) el menor primo de x (entonces
    p ≤ spf(i)). El algoritmo, para cada i, recorre los primos p ≤ spf(i) y
    marca spf[p·i] = p; al llegar a p = spf(i) se detiene. Así cada
    compuesto se marca EXACTAMENTE una vez (con su par (p, i) único): O(n).
    Lo valioso no es el O(n) (en Python es más lenta que Eratóstenes con
    rebanadas) sino el arreglo spf, que permite factorizar en O(log n).

    Segmentada: para tachar los compuestos de [lo, hi] solo se necesitan
    los primos ≤ √hi (mismo argumento de arriba). Se cribán esos primos con
    la criba normal y luego, para cada p, se tachan en el segmento sus
    múltiples desde max(p·p, primer múltiplo de p ≥ lo). Memoria
    O(√hi + (hi − lo)) en vez de O(hi).
    El ingenuo (probar primalidad de cada número por división hasta √x) es
    O(N·√N): con N = 10^6 son ~10^9 operaciones.

MACROALGORITMO
    Eratóstenes:
    1. es_primo = [1]·(n+1); es_primo[0] = es_primo[1] = 0.
    2. Para i = 2 … ⌊√n⌋: si es_primo[i], tachar i·i, i·i + i, … ≤ n.
    3. Los i con es_primo[i] = 1 son los primos.
    Lineal:
    4. spf = [0]·(n+1); para i = 2 … n: si spf[i] = 0, i es primo (spf[i] = i).
    5. Para cada primo p ≤ spf[i] con p·i ≤ n: spf[p·i] = p.
    Segmentada:
    6. Primos base = criba hasta ⌊√hi⌋.
    7. Arreglo del segmento de tamaño hi − lo + 1; para cada primo base p,
       tachar desde max(p·p, ⌈lo/p⌉·p) con paso p. Quitar 0 y 1 si caen.

COMPLEJIDAD
    Eratóstenes: O(n log log n) tiempo, O(n) memoria (1 byte por número).
    En Python: n = 10^7 en ~0.5–1 s con bytearray y rebanadas.
    Criba lineal: O(n) tiempo y memoria (lista de enteros: ~8 bytes cada
    uno o más); en Python puro n ≈ 10^6 por segundo (más lenta).
    Segmentada: O(√hi log log hi + (hi − lo) log log hi).

EJEMPLO A MANO
    n = 30. Se tacha desde p·p:
      p = 2: 4 6 8 10 12 14 16 18 20 22 24 26 28 30
      p = 3: 9 15 21 27 (12, 18, 24, 30 ya estaban)
      p = 5: 25 (y 30 ya estaba)          (7·7 = 49 > 30: se para)
    Primos: 2 3 5 7 11 13 17 19 23 29.
    spf[12] = 2, spf[15] = 3, spf[25] = 5, spf[29] = 29.
    criba_segmentada(100, 130) = [101, 103, 107, 109, 113, 127].

ERRORES TÍPICOS
    - Tachar desde 2·p en vez de p·p: correcto pero más lento; tachar desde
      p·p con p·p calculado en int de 32 bits (C++) desborda si p > 46340.
    - Olvidar marcar 0 y 1 como no primos (también en la segmentada cuando
      lo ≤ 1).
    - Criba de 10^8 o más en Python: no cabe en tiempo; buscar otra idea
      (segmentada, Miller–Rabin, fórmula).
    - En la segmentada, empezar a tachar en ⌈lo/p⌉·p cuando ese valor ES p
      (tacharía al propio primo): por eso se usa max(p·p, …).
    - Usar una lista de bool de Python para 10^7 en vez de bytearray: 8×
      más memoria y mucho más lenta.

VARIANTES Y RELACIONADOS
    - Factorizar con spf en O(log n): factorizacion.py.
    - Criba de φ de Euler, de número de divisores, de Möbius: misma idea de
      recorrer múltiplos (phi_euler.py, divisores.py).
    - Prueba individual de primalidad: primalidad.py (√n) y
      miller_rabin_pollard.py (n hasta 10^18).
    - Contar primos ≤ 10^11 (Meissel–Lehmer / Lucy) — fuera del alcance aquí.

DÓNDE PRACTICAR
    - ICPC/OMP 2017 Murcia/E - Prime Darts (criba para los primeros 99 primos)
    - SPOJ PRIME1 «Prime Generator» (criba segmentada)
    - Codeforces 230B «T-primes»; CSES «Counting Divisors» (con spf)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (división de prueba) para todo n ≤ 3000,
      spf contra el menor divisor buscado a mano hasta 3000, 300 segmentos
      aleatorios contra fuerza bruta (incluye lo ≤ 1 y segmentos alrededor
      de 10^10), y π(10^6) = 78498 (python criba_eratostenes.py)
"""
import math
import random


def criba(n):
    """es_primo[i] = 1 si i es primo, para 0 <= i <= n (bytearray)."""
    es_primo = bytearray([1]) * (n + 1)
    es_primo[0:2] = bytearray(min(2, n + 1))    # 0 y 1 no son primos (con cuidado si n < 1)
    for i in range(2, math.isqrt(n) + 1):
        if es_primo[i]:
            # tachar i*i, i*i + i, ... de un solo golpe (la rebanada corre en C)
            es_primo[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
    return es_primo


def primos_hasta(n):
    """Lista de primos <= n."""
    if n < 2:
        return []
    es_primo = criba(n)
    return [i for i in range(2, n + 1) if es_primo[i]]


def criba_lineal(n):
    """(spf, primos): spf[i] = menor factor primo de i (0 para i < 2)."""
    spf = [0] * (n + 1)
    primos = []
    for i in range(2, n + 1):
        if spf[i] == 0:         # nadie lo marcó: i es primo
            spf[i] = i
            primos.append(i)
        si = spf[i]
        # marcar p*i para los primos p <= spf[i]: p es el menor primo de p*i
        for p in primos:
            if p > si or p * i > n:
                break
            spf[p * i] = p
    return spf, primos


def criba_segmentada(lo, hi):
    """Primos en [lo, hi] usando solo los primos <= sqrt(hi)."""
    if hi < 2 or hi < lo:
        return []
    lo = max(lo, 2)
    base = primos_hasta(math.isqrt(hi))
    seg = bytearray([1]) * (hi - lo + 1)        # seg[k] representa al número lo + k
    for p in base:
        inicio = max(p * p, (lo + p - 1) // p * p)   # nunca tachar al propio p
        if inicio > hi:
            continue
        seg[inicio - lo::p] = bytearray(len(range(inicio, hi + 1, p)))
    return [lo + k for k in range(hi - lo + 1) if seg[k]]


def demo():
    print("primos <= 30:", primos_hasta(30))
    spf, _ = criba_lineal(30)
    print("spf[12], spf[15], spf[25], spf[29] =", spf[12], spf[15], spf[25], spf[29])
    print("primos en [100, 130]:", criba_segmentada(100, 130))


def pruebas():
    random.seed(7)

    def es_primo_bruto(x):
        return x >= 2 and all(x % d for d in range(2, x))

    # Casos borde
    assert primos_hasta(0) == [] and primos_hasta(1) == [] and primos_hasta(2) == [2]
    assert list(criba(0)) == [0] and list(criba(1)) == [0, 0]
    assert criba_lineal(1) == ([0, 0], [])
    assert criba_segmentada(0, 1) == [] and criba_segmentada(0, 2) == [2]
    assert criba_segmentada(10, 5) == [] and criba_segmentada(24, 28) == []

    # Criba completa y lineal contra fuerza bruta
    N = 3000
    es_p = criba(N)
    spf, primos = criba_lineal(N)
    bruto = [x for x in range(N + 1) if es_primo_bruto(x)]
    assert [x for x in range(N + 1) if es_p[x]] == bruto == primos == primos_hasta(N)
    for x in range(2, N + 1):
        assert spf[x] == next(d for d in range(2, x + 1) if x % d == 0)
    for n in range(0, 60):
        assert primos_hasta(n) == [x for x in bruto if x <= n]

    # Segmentada contra fuerza bruta
    for _ in range(300):
        lo = random.randint(0, 3000)
        hi = lo + random.randint(0, 200)
        assert criba_segmentada(lo, hi) == [x for x in range(lo, hi + 1) if es_primo_bruto(x)]
    for _ in range(4):
        # segmentos alrededor de 10^10: división de prueba hasta la raíz (independiente)
        lo = random.randint(10**10, 10**10 + 10**6)
        hi = lo + 60
        seg = set(criba_segmentada(lo, hi))
        for x in range(lo, hi + 1):
            assert (x in seg) == all(x % d for d in range(2, math.isqrt(x) + 1))

    # Resultado conocido: hay 78498 primos menores que 10^6
    assert len(primos_hasta(10**6)) == 78498
    assert criba_lineal(10**5)[1] == primos_hasta(10**5)
    assert len(criba_segmentada(999_000, 1_000_000)) == len(
        [p for p in primos_hasta(10**6) if p >= 999_000])


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
