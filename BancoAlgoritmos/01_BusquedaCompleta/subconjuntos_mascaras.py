"""
Búsqueda completa — Subconjuntos con máscaras de bits («Bitmask subset enumeration»)
Nivel: Básico
Ejecutar: python subconjuntos_mascaras.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Recorrer los 2^N subconjuntos de N elementos representando cada uno con
    un entero: el bit i encendido significa «el elemento i está». También
    recorrer las submáscaras de una máscara (para DP sobre subconjuntos).
    Señales en el enunciado: N ≤ 20 (2^20 ≈ 10^6), «elegir algunos de…»,
    «cada uno se toma o no se toma», «repartir en dos grupos», interruptores
    encendido/apagado, «¿existe una combinación que…?».

FUNCIÓN
    subconjuntos(a) -> list[list]
        Los 2^n subconjuntos de a, en orden de máscara 0..2^n − 1.
    sumas_subconjuntos(a) -> list[int]
        s[mask] = suma de los a[i] con bit i en mask, en O(2^n) total.
    submascaras(m) -> list[int]
        Todas las submáscaras de m, de mayor a menor, terminando en 0.
    preparando_olimpiada(c, l, r, x) -> int
        Codeforces 550B: cuántos subconjuntos de ≥ 2 problemas tienen
        dificultad total en [l, r] y (máx − mín) ≥ x.

IDEA Y ALGORITMO
    Un subconjunto de {0..n−1} ↔ un entero mask en [0, 2^n). Operaciones:
        ¿está i?       mask >> i & 1      (o mask & (1 << i))
        agregar i      mask | (1 << i)
        quitar i       mask & ~(1 << i)
        tamaño         mask.bit_count()   (Python ≥ 3.10; antes bin(m).count("1"))
        bit más bajo   mask & -mask
    for mask in range(1 << n) recorre TODOS los subconjuntos.
    Sumas en O(2^n) en vez de O(2^n · n): la suma de mask es la suma de
    mask sin su bit más bajo, más ese elemento:
        s[mask] = s[mask & (mask − 1)] + a[índice del bit más bajo].
    Submáscaras de m: sub = (sub − 1) & m recorre todas, de mayor a menor.
    Restar 1 apaga el bit más bajo encendido y enciende los de abajo; el &m
    se queda solo con los bits de m. Es como «contar hacia atrás» usando
    solo las posiciones de m. Recorrer las submáscaras de TODAS las
    máscaras cuesta 3^n en total (cada elemento está: fuera de m, en m pero
    no en sub, o en sub), no 4^n.

MACROALGORITMO
    1. Verificar que 2^n (× el costo de evaluar) cabe en el tiempo.
    2. Para mask en 0..2^n − 1:
    3.    Construir lo necesario del subconjunto (suma, máx, mín, tamaño),
          o tomarlo de una tabla calculada en O(1) desde una máscara menor.
    4.    Comprobar la condición y contar/actualizar la mejor respuesta.
    (Submáscaras)
    5. sub = m; repetir: procesar sub; si sub == 0 parar; sub = (sub − 1) & m.

COMPLEJIDAD
    Enumerar: O(2^n · n) si se recorre cada subconjunto bit a bit; O(2^n)
    con la tabla de sumas. Submáscaras de todas las máscaras: O(3^n).
    En Python: 2^20 iteraciones simples ~0,3–0,5 s; 3^13 ≈ 1,6·10^6 bien,
    3^16 ≈ 4,3·10^7 ya es mucho.

EJEMPLO A MANO
    a = [5, 2, 7]:
      mask 0 = 000 → {}        suma 0
      mask 1 = 001 → {5}       suma 5
      mask 2 = 010 → {2}       suma 2
      mask 3 = 011 → {5, 2}    suma s[2] + 5 = 7   (bit más bajo: 0)
      mask 5 = 101 → {5, 7}    suma s[4] + 5 = 12
      mask 7 = 111 → {5, 2, 7} suma s[6] + 5 = 14
    submascaras(0b1011) = 1011, 1010, 1001, 1000, 0011, 0010, 0001, 0000

ERRORES TÍPICOS
    - Precedencia: + y − van antes que << y >>, que van antes que &:
      1 << i - 1 es 1 << (i − 1), y mask & 1 << i es mask & (1 << i).
      En Python == va DESPUÉS de & (mask & 1 == 1 está bien), al revés que
      en C++; ante la duda, paréntesis.
    - Bucle de submáscaras que no procesa el 0 o que no termina (con
      while sub: se salta el 0).
    - n hasta 30 o 40: 2^30 no alcanza en Python → meet_in_the_middle.py.
    - Confundir el bit i con el elemento i+1 cuando el enunciado numera desde 1.

VARIANTES Y RELACIONADOS
    - Subconjuntos de tamaño k: itertools.combinations(range(n), k).
    - DP sobre máscaras (asignaciones, viajante): dp[mask] desde dp[mask sin i].
    - Suma sobre submáscaras (SOS DP) en O(2^n · n).
    - Relacionados: meet_in_the_middle.py, backtracking_poda.py,
      branch_and_bound.py (conjuntos de vértices como máscaras).

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/F - Turnswitch (enumerar los 2^N patrones de la primera fila)
    - ICPC/Colombia 2026/L - Don't Ask Why 2D (enumerar subconjuntos de aristas)
    - ICPC/Colombia 2018/B - Forming Better Groups (DP sobre máscaras de bits)
    - Codeforces 550B «Preparing Olympiad»; CSES «Apple Division»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (itertools.combinations de todos los
      tamaños; submáscaras como todos los x ≤ m con x & m == x) en 1500
      casos aleatorios + conteo total 3^n + casos borde
      (python subconjuntos_mascaras.py)
"""
import itertools
import random


def subconjuntos(a):
    """Los 2^n subconjuntos de a, en orden de máscara."""
    n = len(a)
    return [[a[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]


def sumas_subconjuntos(a):
    """s[mask] = suma de los a[i] con el bit i encendido; O(2^n)."""
    n = len(a)
    s = [0] * (1 << n)
    for mask in range(1, 1 << n):
        bajo = mask & -mask                 # bit más bajo encendido
        i = bajo.bit_length() - 1           # su índice
        s[mask] = s[mask ^ bajo] + a[i]     # mask ^ bajo == mask & (mask - 1)
    return s


def submascaras(m):
    """Submáscaras de m de mayor a menor, incluyendo m y 0."""
    res = []
    sub = m
    while True:
        res.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & m                 # siguiente submáscara menor
    return res


def preparando_olimpiada(c, l, r, x):
    """CF 550B: subconjuntos con >= 2 elementos, suma en [l, r] y máx - mín >= x."""
    n = len(c)
    total = 0
    for mask in range(1 << n):
        if mask.bit_count() < 2:
            continue
        elegidos = [c[i] for i in range(n) if mask >> i & 1]
        if l <= sum(elegidos) <= r and max(elegidos) - min(elegidos) >= x:
            total += 1
    return total


def demo():
    a = [5, 2, 7]
    print("a =", a)
    for mask, (sub, s) in enumerate(zip(subconjuntos(a), sumas_subconjuntos(a))):
        print(f"  mask {mask:03b} → {sub} suma {s}")
    print("submascaras(0b1011) =", [f"{x:04b}" for x in submascaras(0b1011)])
    print("CF 550B ejemplo: c=[1,2,3], l=5, r=6, x=1 →", preparando_olimpiada([1, 2, 3], 5, 6, 1))  # 2


def pruebas():
    random.seed(550)

    # Casos borde
    assert subconjuntos([]) == [[]]
    assert sumas_subconjuntos([]) == [0]
    assert submascaras(0) == [0]
    assert submascaras(1) == [1, 0]
    assert preparando_olimpiada([1, 2, 3], 5, 6, 1) == 2           # ejemplo de CF 550B
    assert preparando_olimpiada([10, 20, 30, 25], 40, 50, 10) == 2
    assert preparando_olimpiada([7], 0, 100, 0) == 0

    # 3^n: suma de submáscaras de todas las máscaras
    for n in range(0, 9):
        assert sum(len(submascaras(m)) for m in range(1 << n)) == 3 ** n

    for _ in range(1500):
        n = random.randint(0, 9)
        a = [random.randint(-10, 10) for _ in range(n)]
        # mismos subconjuntos (como multiconjuntos de índices) que combinations
        por_indices = sorted(tuple(i for i in range(n) if m >> i & 1) for m in range(1 << n))
        bruta = sorted(t for k in range(n + 1) for t in itertools.combinations(range(n), k))
        assert por_indices == bruta
        s = sumas_subconjuntos(a)
        assert all(s[m] == sum(a[i] for i in range(n) if m >> i & 1) for m in range(1 << n))

        m = random.randrange(1 << 10)
        assert submascaras(m) == [x for x in range(m, -1, -1) if x & m == x]

        c = [random.randint(1, 20) for _ in range(n)]
        l = random.randint(0, 60)
        r = l + random.randint(0, 40)
        x = random.randint(0, 15)
        esperado = sum(1 for k in range(2, n + 1) for t in itertools.combinations(c, k)
                       if l <= sum(t) <= r and max(t) - min(t) >= x)
        assert preparando_olimpiada(c, l, r, x) == esperado


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
