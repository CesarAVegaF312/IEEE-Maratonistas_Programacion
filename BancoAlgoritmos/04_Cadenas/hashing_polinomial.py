"""
Cadenas — Hashing polinomial con doble módulo («Rolling hash / polynomial hashing»)
Nivel: Intermedio
Ejecutar: python hashing_polinomial.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Convierte cada subcadena s[i:j] en un número, calculable en O(1) tras
    un preproceso O(n). Dos subcadenas iguales tienen el mismo hash; dos
    distintas casi seguro no. Así «¿s[i:j] == t[k:l]?» cuesta O(1) en vez
    de O(largo), y con búsqueda binaria se obtiene el prefijo común de dos
    posiciones en O(log n) o la subcadena común más larga en O(n log n).
    Señales en el enunciado: muchas comparaciones de subcadenas; «la
    subcadena más larga que aparece en ambas / en al menos K»; «¿cuántas
    subcadenas distintas de largo L?»; comparar trozos de texto en O(1)
    combinado con búsqueda binaria sobre la respuesta.

FUNCIÓN
    HashCadena(s)               preproceso O(n); s puede ser str o lista de enteros ≥ 0
        .obtener(i, j) -> int   hash de s[i:j] (0 ≤ i ≤ j ≤ n)
    buscar_hash(texto, patron) -> list[int]          inicios de las apariciones
    lcp_hash(ha, i, hb, j) -> int
        Prefijo común de a[i:] y b[j:] (ha, hb de la misma clase) en O(log n).
    subcadena_comun_mas_larga(a, b) -> (largo, inicio)
        Mayor L tal que alguna subcadena de largo L de a aparece en b;
        inicio = menor i con a[i:i+L] en b. (0, 0) si no comparten nada.

IDEA Y ALGORITMO
    Se ve la cadena como un número en base B: H(s) = Σ s[k]·B^(n-1-k) mod M.
    Con los hashes de prefijos h[j] = H(s[0:j]) (h[j+1] = h[j]·B + s[j]),
        H(s[i:j]) = h[j] - h[i]·B^(j-i)   (mod M)
    porque h[j] es h[i] «desplazado» j-i posiciones más el trozo s[i:j].
    Colisiones: para dos cadenas distintas fijas de largo L, con B
    ALEATORIA, la probabilidad de que coincidan módulo un primo M es
    ≤ L/M (un polinomio no nulo de grado < L tiene < L raíces). Con
    M ≈ 10^9 y 10^6 comparaciones la probabilidad de algún error ya es
    apreciable (y hay casos anti-hash con base fija); con DOS módulos
    independientes es ≈ L²/(M1·M2) ≈ 10^-18 por comparación. Se combinan
    en un solo entero (x1·2^30 + x2) para usarlo directo en set/dict.
    Búsqueda binaria: «a[i:] y b[j:] coinciden en los primeros L» es
    monótono en L; «existe subcadena común de largo L» también (si hay de
    largo L, sus prefijos de largo L-1 también son comunes).

MACROALGORITMO
    1. Elegir base B aleatoria y dos primos M1, M2; precalcular potencias.
    2. h1[0] = h2[0] = 0; h[k+1] = (h[k]·B + valor(s[k])) mod M.
    3. obtener(i, j): combinar (h[j] - h[i]·B^(j-i)) mod M de ambos módulos.
    4. Buscar P: comparar hash(P) con cada ventana del texto.
    5. LCP de dos posiciones: buscar el mayor L con hashes iguales (binaria).
    6. Subcadena común: binaria sobre L; para L fijo, conjunto de hashes de
       las ventanas de b y recorrer las de a.

COMPLEJIDAD
    Preproceso O(n), obtener O(1), lcp_hash O(log n), subcadena común
    O((|a|+|b|) log) con conjuntos. En Python, preprocesar 10^6 caracteres
    toma ~1 s (dos módulos); 10^6 llamadas a obtener, ~1 s.

EJEMPLO A MANO (un solo módulo, B = 10, M grande, a=1, b=2, …)
    s = "abab": h = [0, 1, 12, 121, 1212]
    H(s[0:2]) = h[2] - h[0]·10² = 12;  H(s[2:4]) = h[4] - h[2]·10² = 1212 - 1200 = 12
    → s[0:2] == s[2:4] ("ab" = "ab") sin comparar letra por letra.
    subcadena_comun_mas_larga("xabcy", "zabcw") = (3, 1)  ("abc")

ERRORES TÍPICOS
    - Base fija conocida (y módulo 2^64 implícito en C++): hay casos
      anti-hash (Thue–Morse) que colisionan seguro. Base aleatoria.
    - Valor 0 para algún carácter: "a" y "aa" podrían confundirse si se
      comparan largos distintos. Usar valor ≥ 1 (aquí ord(c) o x+1).
    - Restar sin volver a tomar % M (en C++ queda negativo; en Python el %
      ya da no negativo, pero hay que aplicarlo).
    - Comparar hashes de subcadenas de DISTINTO largo: no tiene sentido.
    - Desempatar «lexicográficamente menor» comparando hashes: hay que
      comparar los textos reales (o usar lcp_hash y mirar el carácter).

VARIANTES Y RELACIONADOS
    - Palíndromo s[i:j] en O(1): hash del reverso (palindromos.py, manacher.py).
    - Un solo módulo 2^61 - 1 con base aleatoria (más rápido en C++).
    - Hash 2D para matrices (filas y luego columnas).
    - Hash de multiconjunto (suma de aleatorios) para «mismas letras».
    - Exactos y sin probabilidad: kmp.py, funcion_z.py, suffix_array.py,
      suffix_automaton.py (subcadena común más larga en O(n)).

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/F - Finding Common Passwords (búsqueda binaria +
      hashing: la subcadena más larga presente en ≥ K contraseñas)
    - CSES «String Matching», «Finding Periods» (también salen con hashing)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (comparar subcadenas reales, LCP
      carácter a carácter, todas las subcadenas comunes) en 2000 casos
      aleatorios con miles de comparaciones + casos borde
      (python hashing_polinomial.py)
"""
import random

M1, M2 = 1_000_000_007, 998_244_353     # dos primos < 2^30
# Base aleatoria con un generador propio: no depende de random.seed(...)
B = random.Random().randrange(1000, M2 - 1)
_p1, _p2 = [1], [1]                      # potencias de B, compartidas


def _potencias(n):
    while len(_p1) <= n:
        _p1.append(_p1[-1] * B % M1)
        _p2.append(_p2[-1] * B % M2)


class HashCadena:
    """Hashes de prefijos de s; obtener(i, j) da el hash de s[i:j] en O(1)."""

    def __init__(self, s):
        n = len(s)
        _potencias(n)
        h1 = [0] * (n + 1)
        h2 = [0] * (n + 1)
        for k, c in enumerate(s):
            v = ord(c) if isinstance(c, str) else c + 1     # valor siempre ≥ 1
            h1[k + 1] = (h1[k] * B + v) % M1
            h2[k + 1] = (h2[k] * B + v) % M2
        self.h1, self.h2, self.n = h1, h2, n

    def obtener(self, i, j):
        """Hash de s[i:j], los dos módulos combinados en un entero."""
        x1 = (self.h1[j] - self.h1[i] * _p1[j - i]) % M1
        x2 = (self.h2[j] - self.h2[i] * _p2[j - i]) % M2
        return x1 << 30 | x2


def buscar_hash(texto, patron):
    """Inicios de todas las apariciones de patron en texto (Rabin–Karp)."""
    n, m = len(texto), len(patron)
    ht = HashCadena(texto)
    objetivo = HashCadena(patron).obtener(0, m)
    return [i for i in range(n - m + 1) if ht.obtener(i, i + m) == objetivo]


def lcp_hash(ha, i, hb, j):
    """Prefijo común de a[i:] y b[j:] con búsqueda binaria sobre el largo."""
    lo, hi = 0, min(ha.n - i, hb.n - j)
    # Invariante: largo lo coincide; buscamos el mayor que coincide.
    while lo < hi:
        m = (lo + hi + 1) // 2
        if ha.obtener(i, i + m) == hb.obtener(j, j + m):
            lo = m
        else:
            hi = m - 1
    return lo


def subcadena_comun_mas_larga(a, b):
    """(L, i): mayor L con a[i:i+L] presente en b, y el menor i que lo logra."""
    ha, hb = HashCadena(a), HashCadena(b)

    def primera_comun(L):
        """Menor i con a[i:i+L] en b, o -1 si ninguna ventana de largo L es común."""
        de_b = {hb.obtener(j, j + L) for j in range(len(b) - L + 1)}
        for i in range(len(a) - L + 1):
            if ha.obtener(i, i + L) in de_b:
                return i
        return -1

    # Binaria: L = 0 siempre sirve; buscamos el mayor L que sirve.
    lo, hi = 0, min(len(a), len(b))
    while lo < hi:
        m = (lo + hi + 1) // 2
        if primera_comun(m) >= 0:
            lo = m
        else:
            hi = m - 1
    return (lo, primera_comun(lo)) if lo > 0 else (0, 0)


def demo():
    s = "abab"
    h = HashCadena(s)
    print("s =", s)
    print("hash(s[0:2]) == hash(s[2:4]):", h.obtener(0, 2) == h.obtener(2, 4))   # True
    print("hash(s[0:2]) == hash(s[1:3]):", h.obtener(0, 2) == h.obtener(1, 3))   # False
    print("buscar_hash('abacaba', 'aba'):", buscar_hash("abacaba", "aba"))        # [0, 4]
    ha, hb = HashCadena("abcabd"), HashCadena("xabcabz")
    print("lcp de 'abcabd'[0:] y 'xabcabz'[1:]:", lcp_hash(ha, 0, hb, 1))         # 5
    print("subcadena_comun_mas_larga('xabcy', 'zabcw'):",
          subcadena_comun_mas_larga("xabcy", "zabcw"))                            # (3, 1)


def pruebas():
    random.seed(2023)

    def lcs_bruto(a, b):
        for L in range(min(len(a), len(b)), 0, -1):
            comunes = [i for i in range(len(a) - L + 1) if a[i:i + L] in b]
            if comunes:
                return (L, comunes[0])
        return (0, 0)

    # Casos borde
    assert buscar_hash("", "") == [0] and buscar_hash("abc", "abcd") == []
    assert subcadena_comun_mas_larga("", "abc") == (0, 0)
    assert subcadena_comun_mas_larga("abc", "xyz") == (0, 0)
    assert subcadena_comun_mas_larga("aaaa", "aa") == (2, 0)
    h = HashCadena("a")
    assert h.obtener(0, 0) == HashCadena("").obtener(0, 0) == 0
    # Listas con ceros: [0] y [0, 0] no deben confundirse con la cadena vacía
    hl = HashCadena([0, 0, 1])
    assert hl.obtener(0, 1) == hl.obtener(1, 2) != hl.obtener(2, 3)

    comparaciones = 0
    for _ in range(2000):
        alfabeto = random.choice(["ab", "abc", "a"])
        s = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 16)))
        t = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 16)))
        hs, ht = HashCadena(s), HashCadena(t)
        # Igualdad de subcadenas arbitrarias del mismo largo (entre s y t)
        for _ in range(20):
            L = random.randint(0, min(len(s), len(t)))
            i = random.randint(0, len(s) - L)
            j = random.randint(0, len(t) - L)
            assert (hs.obtener(i, i + L) == ht.obtener(j, j + L)) == (s[i:i + L] == t[j:j + L])
            comparaciones += 1
        # LCP con binaria
        if s and t:
            i, j = random.randrange(len(s)), random.randrange(len(t))
            k = 0
            while i + k < len(s) and j + k < len(t) and s[i + k] == t[j + k]:
                k += 1
            assert lcp_hash(hs, i, ht, j) == k
        p = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 3)))
        assert buscar_hash(s, p) == [i for i in range(len(s) - len(p) + 1) if s[i:i + len(p)] == p]
        assert subcadena_comun_mas_larga(s, t) == lcs_bruto(s, t)
    assert comparaciones == 40000

    # Grande: dos cadenas de 2·10^4 con una subcadena común plantada de 3000
    comun = "".join(random.choice("ab") for _ in range(3000))
    a = "".join(random.choice("cd") for _ in range(10000)) + comun + "e" * 7000
    b = "f" * 5000 + comun + "".join(random.choice("gh") for _ in range(12000))
    assert subcadena_comun_mas_larga(a, b) == (3000, 10000)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
