"""
Matemáticas — Números de Catalan: fórmula, recurrencia y qué cuentan («Catalan numbers»)
Nivel: Intermedio
Ejecutar: python catalan.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    La sucesión 1, 1, 2, 5, 14, 42, 132, 429, 1430, … (C_0, C_1, …) aparece
    en muchísimos conteos de estructuras «anidadas» o «que no se cruzan».
    Cómo reconocerlo: calcular a mano los primeros casos y obtener
    1, 2, 5, 14 es la señal más fuerte. Enunciados típicos: secuencias de
    paréntesis balanceados con n pares, árboles binarios con n nodos,
    triangulaciones de un polígono convexo de n+2 lados, caminos en
    cuadrícula de (0,0) a (n,n) que no cruzan la diagonal, formas de poner
    paréntesis a un producto de n+1 factores, permutaciones ordenables con
    una pila, n cuerdas que no se cruzan entre 2n puntos de un círculo.

FUNCIÓN
    catalan(n) -> int                  C_n = C(2n, n) / (n + 1) exacto
    catalan_tabla(N) -> list[int]      C_0..C_N con la recurrencia O(N²)
    catalan_mod(N, p) -> list[int]     C_0..C_N mód p primo en O(N)
    boleta(a, b) -> int                cadenas con a '(' y b ')' (a ≥ b) en
                                       las que ningún prefijo tiene más ')'
                                       que '('; boleta(n, n) = C_n

IDEA Y ALGORITMO
    Recurrencia (descomposición por el primer bloque): toda secuencia
    balanceada no vacía se escribe de forma única como ( A ) B, con A y B
    balanceadas; si A tiene i pares, B tiene n−1−i. Por eso
        C_0 = 1,  C_n = Σ_{i=0}^{n−1} C_i · C_{n−1−i}.
    Lo mismo para árboles binarios (raíz, subárbol izquierdo, derecho) y
    triangulaciones (el triángulo apoyado en un lado fijo parte el polígono
    en dos). Por eso todas esas familias tienen el mismo conteo.
    Fórmula cerrada por el principio de reflexión: piense '(' = paso +1 y
    ')' = paso −1. Hay C(2n, n) caminos de 0 a 0 con 2n pasos. Uno es MALO
    si en algún momento baja a −1. Reflejando (cambiando +1 ↔ −1) todo lo
    que viene DESPUÉS de la primera visita a −1, un camino malo se vuelve
    un camino de 0 a −2, y la operación es reversible; los caminos de 0 a
    −2 tienen n−1 subidas y n+1 bajadas: C(2n, n+1). Entonces
        C_n = C(2n, n) − C(2n, n+1) = C(2n, n) / (n+1).
    Igual con a subidas y b bajadas (a ≥ b): buenos = C(a+b, b) − C(a+b, b−1)
    (problema de la boleta). Para la tabla mód p en O(N):
        C_{n} = C_{n−1} · 2(2n−1) / (n+1)   (sale del cociente de las fórmulas).

MACROALGORITMO
    1. Reconocer la estructura (paréntesis, árbol, triangulación, camino
       que no cruza la diagonal) o calcular los primeros casos a mano.
    2. Si piden un solo C_n exacto: math.comb(2n, n) // (n + 1).
    3. Si piden muchos C_n mód p: factoriales mód p, C(2n,n)·inv(n+1).
    4. Si la estructura tiene variantes (restricciones extra), volver a la
       recurrencia de descomposición en primer bloque como DP.
    5. Si hay distinto número de aperturas y cierres: fórmula de la boleta.

COMPLEJIDAD
    catalan(n): un binomial exacto. catalan_tabla: O(N²) (N ≈ 2000 en 1 s,
    con enteros grandes). catalan_mod: O(N) con inversos 1..N+1.
    C_n crece como 4^n / (n^{3/2} √π): C_30 ≈ 3,8·10^15.

EJEMPLO A MANO
    C_3 = C(6,3)/4 = 20/4 = 5: ((())), (()()), (())(), ()(()), ()()().
    Recurrencia: C_3 = C_0C_2 + C_1C_1 + C_2C_0 = 2 + 1 + 2 = 5.
    Reflexión: C(6,3) − C(6,4) = 20 − 15 = 5.

ERRORES TÍPICOS
    - Desfase de índice: árboles binarios con n nodos = C_n, pero árboles
      binarios llenos con n hojas = C_{n−1}; polígono de n lados = C_{n−2}.
    - Calcular C(2n, n)/(n+1) con / (flotante) en vez de //.
    - Con módulo, dividir por (n+1) sin usar el inverso modular.
    - Usar la recurrencia O(N²) cuando N = 10^6 (usar la fórmula).

VARIANTES Y RELACIONADOS
    - Fórmula de la boleta / números de Catalan generalizados (aperturas ≠
      cierres, caminos que no tocan otra recta).
    - Números de Motzkin, Schröder (otras descomposiciones en primer bloque).
    - funciones_generatrices.py: G(x) = 1 + x·G(x)² ⇒ G = (1 − √(1−4x))/(2x).
    - ncr_modular.py (C_n mód p), combinatoria_basica.py.

DÓNDE PRACTICAR
    - No hay problemas del repo que lo usen directamente.
    - CSES «Bracket Sequences I» (C_{n/2} mód 10^9+7), «Bracket Sequences
      II» (prefijo dado: fórmula de la boleta)

VERIFICACIÓN
    - Pruebas: OK contra enumeración de cadenas de paréntesis (n ≤ 10),
      permutaciones evitables por 231 / ordenables con pila (n ≤ 7),
      triangulaciones contadas por fuerza bruta recursiva sobre polígonos
      (n ≤ 9), boleta contra enumeración (a, b ≤ 8), recurrencia y versión
      mód p hasta N = 300 (python catalan.py)
"""
import itertools
from functools import lru_cache
from math import comb

MOD = 1_000_000_007


def catalan(n):
    """C_n exacto = C(2n, n) / (n + 1)."""
    return comb(2 * n, n) // (n + 1)


def catalan_tabla(N):
    """C_0..C_N con la recurrencia de primer bloque C_n = Σ C_i·C_{n-1-i}."""
    c = [1] + [0] * N
    for n in range(1, N + 1):
        c[n] = sum(c[i] * c[n - 1 - i] for i in range(n))
    return c


def catalan_mod(N, p=MOD):
    """C_0..C_N mód p (p primo > N+1) con C_n = C_{n-1}·2(2n-1)/(n+1)."""
    inv = [0, 1] + [0] * N                      # inversos de 1..N+1 en O(N)
    for i in range(2, N + 2):
        inv[i] = (p - p // i) * inv[p % i] % p
    c = [1] * (N + 1)
    for n in range(1, N + 1):
        c[n] = c[n - 1] * 2 * (2 * n - 1) % p * inv[n + 1] % p
    return c


def boleta(a, b):
    """Cadenas con a '(' y b ')' sin prefijo con más ')' que '(' (reflexión)."""
    if b > a:
        return 0
    if b == 0:
        return 1
    return comb(a + b, b) - comb(a + b, b - 1)


def demo():
    print("C_0..C_10:", catalan_tabla(10))
    print("C_3 por fórmula =", catalan(3), "| reflexión:", comb(6, 3) - comb(6, 4))
    print("paréntesis de 3 pares:",
          ["".join(s) for s in itertools.product("()", repeat=6) if _balanceada(s)])
    print("boleta(3, 2) =", boleta(3, 2))   # C(5,2) - C(5,1) = 5
    print("C_1000 mód 1e9+7 =", catalan_mod(1000)[1000])


def _balanceada(s):
    nivel = 0
    for ch in s:
        nivel += 1 if ch == "(" else -1
        if nivel < 0:
            return False
    return nivel == 0


def _prefijos_ok(s):
    nivel = 0
    for ch in s:
        nivel += 1 if ch == "(" else -1
        if nivel < 0:
            return False
    return True


def _evita_231(p):
    # existe i<j<k con p[k] < p[i] < p[j]  →  contiene 231
    n = len(p)
    return not any(p[k] < p[i] < p[j]
                   for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n))


@lru_cache(maxsize=None)
def _triangulaciones(vertices):
    """Fuerza bruta: elegir el tercer vértice del triángulo sobre la arista (v0, vlast)."""
    if len(vertices) < 3:
        return 1
    total = 0
    for idx in range(1, len(vertices) - 1):
        total += _triangulaciones(vertices[:idx + 1]) * _triangulaciones(vertices[idx:])
    return total


def pruebas():
    # Casos borde
    assert catalan(0) == 1 and catalan(1) == 1 and boleta(0, 0) == 1 and boleta(2, 3) == 0

    tabla = catalan_tabla(300)
    tmod = catalan_mod(300)
    for n in range(301):
        assert tabla[n] == catalan(n)
        assert tmod[n] == catalan(n) % MOD
        assert boleta(n, n) == catalan(n)

    # Paréntesis balanceados (enumeración de las 4^n cadenas, n ≤ 10)
    for n in range(0, 11):
        cuenta = sum(1 for s in itertools.product("()", repeat=2 * n) if _balanceada(s))
        assert cuenta == catalan(n)

    # Permutaciones que evitan 231 (= ordenables con una pila)
    for n in range(0, 8):
        cuenta = sum(1 for p in itertools.permutations(range(n)) if _evita_231(p))
        assert cuenta == catalan(n)

    # Triangulaciones de un polígono de n+2 lados
    for n in range(0, 10):
        assert _triangulaciones(tuple(range(n + 2))) == catalan(n)

    # Boleta contra enumeración
    for a in range(0, 9):
        for b in range(0, 9):
            cuenta = sum(1 for pos in itertools.combinations(range(a + b), b)
                         if _prefijos_ok(["(" if i not in pos else ")" for i in range(a + b)]))
            assert boleta(a, b) == cuenta


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
