"""
Cadenas — Distancia de edición bit-paralela de Myers («Myers' bit-vector algorithm»)
Nivel: Avanzado
Ejecutar: python myers_bit_paralelo.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcula la distancia de Levenshtein (mínimo de inserciones, borrados y
    sustituciones para convertir a en b) guardando una COLUMNA ENTERA de la
    tabla de programación dinámica en dos enteros de bits, y procesando
    cada letra de b con ~15 operaciones de bits. En Python los enteros no
    tienen límite de 64 bits, así que sirve para cualquier |a| y las
    operaciones corren en C: es decenas de veces más rápido que la DP
    clásica de dos ciclos. También hace búsqueda aproximada: dónde aparece
    un patrón con a lo más k errores dentro de un texto.
    Señales en el enunciado: «distancia de edición ≤ K» entre MUCHOS pares
    (~10^5 pares de cadenas cortas) o pares largos; «aparece con a lo
    más k errores»; la DP O(|a|·|b|) en Python no alcanza por constante.

FUNCIÓN
    levenshtein_dp(a, b) -> int          DP clásica O(|a|·|b|), referencia
    levenshtein_myers(a, b) -> int       bit-paralelo, O(|b|·⌈|a|/64⌉)
    a_lo_sumo_k(a, b, k) -> bool         lev(a, b) ≤ k, con corte temprano
    busqueda_aproximada(texto, patron, k) -> list[int]
        Posiciones j (desde 0) donde termina alguna subcadena de texto a
        distancia ≤ k de patron (patron no vacío).
    Sirven para str, bytes o listas (cualquier secuencia de elementos hashables).

IDEA Y ALGORITMO
    Tabla clásica: D[i][j] = lev(a[:i], b[:j]); columnas j = 0..|b|, filas
    i = 0..m. Observación (Ukkonen, Myers): dos celdas vecinas difieren en
    -1, 0 o +1. Entonces una columna se describe con las DIFERENCIAS
    VERTICALES Δv[i] = D[i][j] - D[i-1][j] ∈ {-1, 0, +1}, guardadas como
    dos máscaras: Pv (bits donde Δv = +1) y Mv (donde Δv = -1). Bit i-1 ↔
    fila i. La columna 0 es 0,1,2,…,m → Pv = todos unos, Mv = 0.
    Pasar a la columna siguiente con la letra c: Eq = bits de las
    posiciones de a donde está c (precalculado por letra). Las
    recurrencias de la DP, escritas sobre diferencias, se vuelven fórmulas
    de bits; la única parte «no local» (una coincidencia que se propaga
    hacia abajo por una racha de +1) se resuelve con una SUMA de enteros,
    cuyo acarreo recorre la racha en una sola operación:
        Xv = Eq | Mv
        Xh = (((Eq & Pv) + Pv) ^ Pv) | Eq
        Ph = Mv | ~(Xh | Pv)          (Δh = +1 en cada fila)
        Mh = Pv & Xh                  (Δh = -1)
        dist += 1 si el bit alto de Ph, -= 1 si el de Mh   (última fila)
        Ph = (Ph << 1) | 1   ;  Mh = Mh << 1   (fila 0: D[0][j] = j sube 1)
        Pv = Mh | ~(Xv | Ph) ;  Mv = Ph & Xv
    (todo enmascarado a m bits, porque ~ en Python da negativos).
    Búsqueda aproximada: la fila 0 vale 0 en todas las columnas (el patrón
    puede empezar donde sea), así que se desplaza Ph SIN meter el 1.
    Corte temprano: cada letra que falta de b cambia la última fila en a
    lo más 1; si dist - (letras restantes) > k ya no puede bajar a k.

MACROALGORITMO
    1. Peq[c] = OR de 1 << i para cada i con a[i] == c.
    2. Pv = (1 << m) - 1, Mv = 0, dist = m (columna 0).
    3. Para cada letra c de b: Eq = Peq.get(c, 0); calcular Xv, Xh, Ph, Mh.
    4. Actualizar dist con el bit m-1 de Ph / Mh.
    5. Desplazar Ph (con | 1 para distancia global, sin él para búsqueda)
       y Mh; calcular el nuevo Pv, Mv; enmascarar a m bits.
    6. Distancia: dist al final. Búsqueda: anotar j cuando dist ≤ k.
       Acotada: cortar si dist - restantes > k.

COMPLEJIDAD
    O(|b|·⌈m/64⌉) operaciones de máquina (cada operación de bits sobre un
    entero de m bits cuesta m/64 palabras, en C). Memoria O(σ + m/64).
    Medido en Python: dos cadenas de 10^4 en ~0,1 s (la DP clásica tarda
    ~30 s); pares de cadenas de 10–20 letras, ~25 µs por par (≈ 2·10^5
    pares en 5 s), por eso con muchos pares conviene filtrar antes por
    diferencia de largos y usar el corte temprano de a_lo_sumo_k.

EJEMPLO A MANO
    a = "ab" (m = 2), b = "ba". Columnas de la DP (filas i = 0, 1, 2):
      j=0: [0, 1, 2]  Δv = (+1, +1)  → Pv = 11, Mv = 00, dist = 2
      j=1 ('b'): [1, 1, 1]  Δv = (0, 0) → Pv = 00, Mv = 00, dist = 1
      j=2 ('a'): [2, 1, 2]  Δv = (-1, +1) → Pv = 10, Mv = 01, dist = 2
    (bits escritos fila 2 | fila 1). lev("ab", "ba") = 2.
    busqueda_aproximada("xxabcxx", "abd", 1) = [3, 4]: "ab" termina en 3
    (falta la d) y "abc" termina en 4 (c por d).

ERRORES TÍPICOS
    - No enmascarar: en Python ~x es negativo y los desplazamientos hacen
      crecer el entero sin fin (resultados basura y lentitud).
    - Olvidar el «| 1» al desplazar Ph en la distancia global (o ponerlo
      en la búsqueda aproximada, donde la fila 0 es toda ceros).
    - Leer la distancia del bit equivocado: es el bit m-1 (fila m).
    - a vacía: no hay bits; la distancia es |b| (caso aparte).
    - En C++ con m > 64 hay que encadenar palabras con acarreo; en Python
      no hace falta, pero cada operación cuesta proporcional a m.

VARIANTES Y RELACIONADOS
    - Ukkonen: DP solo en la banda |i - j| ≤ k, O(k·n), para k pequeño.
    - Distancia de Hamming (solo sustituciones): popcount de máscaras.
    - LCS bit-paralela (Allison–Dix / Hyyrö): misma idea con otra recurrencia.
    - Para k = 0 la búsqueda exacta es kmp.py / funcion_z.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/M - Byte Flu (grafo con arista si lev ≤ K, hasta
      ~5·10^5 pares, + corte mínimo con Dinic)

VERIFICACIÓN
    - Pruebas: OK contra la DP clásica y contra una recursión con memo
      (definición directa) en 3000 pares aleatorios, búsqueda aproximada
      contra la DP probando todos los inicios en 1500 casos, cadenas de
      1000 letras (m > 64, varias palabras) + casos borde
      (python myers_bit_paralelo.py)
"""
import random
from functools import lru_cache


def levenshtein_dp(a, b):
    """DP clásica por filas: O(|a|·|b|) tiempo, O(|b|) memoria."""
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, y in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y))
        prev = cur
    return prev[-1]


def _mascaras(a):
    """peq[c] = bits de las posiciones de a donde aparece c."""
    peq = {}
    for i, c in enumerate(a):
        peq[c] = peq.get(c, 0) | (1 << i)
    return peq


def _myers(a, b, k=None, global_=True):
    """Núcleo: recorre b columna por columna. Devuelve la distancia final
    (global), o la lista de columnas con dist ≤ k (búsqueda), o None si el
    corte temprano (k dado, global) descarta lev ≤ k."""
    m = len(a)
    peq = _mascaras(a)
    mascara = (1 << m) - 1
    alto = 1 << (m - 1)
    pv, mv, dist = mascara, 0, m        # columna 0: diferencias verticales todas +1
    entrada = 1 if global_ else 0       # fila 0: D[0][j] = j (global) o 0 (búsqueda)
    finales = []
    restantes = len(b)
    for j, c in enumerate(b):
        eq = peq.get(c, 0)
        xv = eq | mv
        # La suma propaga una coincidencia hacia abajo por la racha de +1 (acarreo).
        xh = ((((eq & pv) + pv) & mascara) ^ pv) | eq
        ph = mv | (~(xh | pv) & mascara)
        mh = pv & xh
        if ph & alto:
            dist += 1
        elif mh & alto:
            dist -= 1
        ph = ((ph << 1) | entrada) & mascara
        mh = (mh << 1) & mascara
        pv = mh | (~(xv | ph) & mascara)
        mv = ph & xv
        if global_:
            restantes -= 1
            # Cada letra que falta cambia la última fila en a lo más 1.
            if k is not None and dist - restantes > k:
                return None
        elif dist <= k:
            finales.append(j)
    return dist if global_ else finales


def levenshtein_myers(a, b):
    """Distancia de Levenshtein entre a y b, bit-paralela."""
    if not a:
        return len(b)
    return _myers(a, b)


def a_lo_sumo_k(a, b, k):
    """True si lev(a, b) <= k (con filtros baratos y corte temprano)."""
    if abs(len(a) - len(b)) > k:
        return False                    # hace falta al menos esa cantidad de inserciones
    if not a:
        return len(b) <= k
    d = _myers(a, b, k)
    return d is not None and d <= k


def busqueda_aproximada(texto, patron, k):
    """Columnas j donde termina una subcadena de texto con lev(patron, ·) <= k."""
    assert patron, "el patrón debe ser no vacío"
    return _myers(patron, texto, k, global_=False)


def demo():
    a, b = "ab", "ba"
    print(f"levenshtein_myers({a!r}, {b!r}) =", levenshtein_myers(a, b))           # 2
    # Traza de las máscaras columna por columna (como en EJEMPLO A MANO)
    m, peq = len(a), _mascaras(a)
    mascara, pv, mv, dist = (1 << m) - 1, (1 << m) - 1, 0, m
    print(f"  j=0: Pv={pv:0{m}b} Mv={mv:0{m}b} dist={dist}")
    for j, c in enumerate(b, 1):
        eq = peq.get(c, 0)
        xv = eq | mv
        xh = ((((eq & pv) + pv) & mascara) ^ pv) | eq
        ph = mv | (~(xh | pv) & mascara)
        mh = pv & xh
        dist += 1 if ph >> (m - 1) & 1 else -1 if mh >> (m - 1) & 1 else 0
        ph = ((ph << 1) | 1) & mascara
        mh = (mh << 1) & mascara
        pv = mh | (~(xv | ph) & mascara)
        mv = ph & xv
        print(f"  j={j} ({c!r}): Pv={pv:0{m}b} Mv={mv:0{m}b} dist={dist}")
    print("levenshtein_myers('kitten', 'sitting') =", levenshtein_myers("kitten", "sitting"))  # 3
    print("a_lo_sumo_k('kitten', 'sitting', 2) =", a_lo_sumo_k("kitten", "sitting", 2))       # False
    print("busqueda_aproximada('xxabcxx', 'abd', 1) =",
          busqueda_aproximada("xxabcxx", "abd", 1))                                           # [3, 4]


def pruebas():
    random.seed(2026)

    def lev_memo(a, b):
        # Definición recursiva directa (solo para cadenas cortas).
        @lru_cache(maxsize=None)
        def d(i, j):
            if i == 0:
                return j
            if j == 0:
                return i
            return min(d(i - 1, j) + 1, d(i, j - 1) + 1, d(i - 1, j - 1) + (a[i - 1] != b[j - 1]))
        return d(len(a), len(b))

    # Casos borde
    assert levenshtein_myers("", "") == 0 and levenshtein_myers("", "abc") == 3
    assert levenshtein_myers("abc", "") == 3 and levenshtein_myers("abc", "abc") == 0
    assert a_lo_sumo_k("", "", 0) and not a_lo_sumo_k("a", "", 0)
    assert levenshtein_myers([1, 2, 3], [1, 3]) == 1
    assert busqueda_aproximada("", "a", 1) == [] and busqueda_aproximada("b", "a", 1) == [0]

    for _ in range(3000):
        alfabeto = random.choice(["ab", "abc", "abcdefghij"])
        a = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 12)))
        b = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 12)))
        d = levenshtein_dp(a, b)
        assert d == lev_memo(a, b)
        assert levenshtein_myers(a, b) == d
        k = random.randint(0, 6)
        assert a_lo_sumo_k(a, b, k) == (d <= k)

    for _ in range(1500):
        alfabeto = random.choice(["ab", "abc"])
        t = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 12)))
        p = "".join(random.choice(alfabeto) for _ in range(random.randint(1, 5)))
        k = random.randint(0, 3)
        # Mejor subcadena que termina en j: probar todos los inicios (incluida la vacía).
        esperado = [j for j in range(len(t))
                    if min(levenshtein_dp(p, t[i:j + 1]) for i in range(j + 2)) <= k]
        assert busqueda_aproximada(t, p, k) == esperado

    # Cadenas largas (m > 64: el entero usa varias palabras)
    for _ in range(3):
        a = "".join(random.choice("acgt") for _ in range(700))
        b = list(a)
        for _ in range(60):
            b[random.randrange(len(b))] = random.choice("acgt")
        b = "".join(b) + "".join(random.choice("acgt") for _ in range(300))
        d = levenshtein_dp(a, b)
        assert levenshtein_myers(a, b) == d
        assert a_lo_sumo_k(a, b, d) and not a_lo_sumo_k(a, b, d - 1)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
