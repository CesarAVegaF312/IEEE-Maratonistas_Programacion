"""
Matemáticas — Invariantes y paridad: paridad de permutaciones y resolubilidad del 15-puzzle
Nivel: Intermedio
Ejecutar: python invariantes_paridad.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Probar que una configuración NO se puede alcanzar (o que sí) sin
    explorar el espacio de estados: se busca una cantidad que ninguna
    jugada cambia (INVARIANTE), típicamente una paridad o un resto módulo
    algo. Si el inicio y el objetivo difieren en el invariante, es imposible.
    Cómo reconocerlo: «¿es posible llegar a…?» con operaciones repetibles
    (intercambios, deslizar fichas, cambiar signos, sumar a pares), espacio
    de estados gigantesco (n! configuraciones), respuesta Sí/No.

FUNCIÓN
    inversiones(p) -> int           pares i<j con p[i] > p[j] (merge sort, O(n log n))
    paridad_ciclos(p) -> int        paridad de la permutación de 0..n−1 por ciclos:
                                    (n − #ciclos) mód 2 (0 = par), O(n)
    resoluble_puzzle(m, n, a) -> bool
        a = lista de m·n valores (fila por fila), permutación de 1..m·n; el
        valor m·n es el hueco. ¿Se puede llegar a 1, 2, …, m·n (hueco al
        final) deslizando fichas vecinas al hueco?
    es_dif_cuadrados(N) -> bool     ¿N = x² − y² con x, y enteros? (invariante mód 4)

IDEA Y ALGORITMO
    Paridad de una permutación: toda permutación se escribe como producto de
    transposiciones y la paridad de esa cantidad es fija (= paridad del
    número de inversiones). Un intercambio de dos elementos cambia el
    número de inversiones en una cantidad IMPAR (los pares con elementos
    intermedios cambian de a dos, más el par intercambiado).
    Por ciclos: un ciclo de largo ℓ es producto de ℓ−1 transposiciones, así
    que paridad = Σ (ℓ−1) = n − #ciclos (mód 2): O(n) sin contar inversiones.
    15-puzzle (m × n): contando el hueco como la ficha m·n, cada jugada
    intercambia el hueco con una vecina (una transposición: la paridad de
    la permutación cambia) y mueve el hueco una casilla (la paridad de su
    distancia Manhattan a la esquina inferior derecha cambia). Por eso
        I = paridad(permutación) + paridad(distancia del hueco)  (mód 2)
    NO cambia con ninguna jugada, y en el objetivo vale 0. Si I = 1 →
    imposible. Para m, n ≥ 2 vale el recíproco (Johnson–Story 1879; Wilson
    1974 para grafos 2-conexos bipartitos): I = 0 → resoluble.
    Caso 1 × n o m × 1: las fichas solo se corren y nunca cambian de orden
    relativo: resoluble ⇔ sin el hueco ya están ordenadas.
    Invariante módulo 4: x² ≡ 0 o 1 (mód 4), así que x² − y² ≢ 2 (mód 4).
    Y todo lo demás sí se alcanza: impar N = (k+1)² − k² con N = 2k+1;
    N ≡ 0 (mód 4): N = (k+1)² − (k−1)² con N = 4k.

MACROALGORITMO
    1. Identificar las operaciones permitidas y escribir el estado.
    2. Buscar una cantidad que cada operación conserve (o cambie de forma
       controlada: siempre ±1, siempre de paridad, siempre ×(−1)).
       Candidatas: paridad de permutación, suma mód k, coloreo de tablero.
    3. Comparar el invariante en el estado inicial y el objetivo.
    4. Si difieren → imposible. Si coinciden, argumentar (o citar) que el
       invariante es la ÚNICA obstrucción (eso es lo difícil).
    5. Verificar casos borde donde el recíproco falla (tableros 1×n).

COMPLEJIDAD
    inversiones O(n log n); paridad_ciclos O(n); resoluble_puzzle O(m·n);
    es_dif_cuadrados O(1).

EJEMPLO A MANO
    2×3, a = 4 1 3 / 6 2 5: inversiones 4>1, 4>3, 4>2, 3>2, 6>2, 6>5 = 6
    (par); el hueco (6) está en la fila 1, columna 0 → distancia 0 + 2 = 2
    (par) → I = 0 → resoluble.
    2×3, a = 4 1 3 / 6 5 2: 7 inversiones → I = 1 → imposible.
    Permutación (1 2 0 4 3): ciclos (0 1 2)(3 4) → 5 − 2 = 3 → impar.

ERRORES TÍPICOS
    - Olvidar contar el hueco en la permutación, o contarlo pero no sumar
      la paridad de su distancia (hay varias formulaciones equivalentes; no
      mezclar piezas de dos).
    - Aplicar la regla de paridad a tableros 1×n (ahí no basta).
    - Contar inversiones en O(n²) con n = 10^5 (usar ciclos o merge sort).
    - Suponer sin prueba que el invariante es suficiente: solo garantiza
      la imposibilidad.

VARIANTES Y RELACIONADOS
    - Regla clásica del 15-puzzle sin contar el hueco: ancho impar →
      inversiones pares; ancho par → inversiones + fila del hueco (desde
      abajo) con cierta paridad. Es la misma invariante reescrita.
    - Coloreo de tablero: dominós en un tablero sin dos esquinas opuestas
      (cada dominó cubre una blanca y una negra).
    - Grafos bipartitos: paridad de la longitud de los caminos.
    - Monovariantes (cantidad que solo crece) para probar terminación.
    - Contar inversiones con Fenwick (estructuras de datos).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/E - Extended Puzzle (exactamente resoluble_puzzle,
      m·n ≤ 10^5, paridad por ciclos)
    - ICPC/Colombia 2023/C - Knights (paridad del color: el grafo del
      caballo es bipartito)
    - ICPC/Colombia 2024/C - SquareDiff (invariante mód 4 de x² − y²)
    - ICPC/Colombia 2024/K - Skyline (conteo de inversiones con Fenwick)

VERIFICACIÓN
    - Pruebas: OK contra BFS sobre TODAS las configuraciones de los
      tableros 2×2, 2×3, 3×2, 2×4, 4×2 y 1×n (n ≤ 5); inversiones y
      paridad por ciclos contra el doble bucle en 2000 permutaciones;
      es_dif_cuadrados contra búsqueda directa para N ≤ 400
      (python invariantes_paridad.py)
"""
import itertools
import random
from collections import deque


def inversiones(p):
    """Pares i<j con p[i] > p[j], por merge sort (iterativo, O(n log n))."""
    a = list(p)
    n = len(a)
    inv = 0
    ancho = 1
    while ancho < n:
        for lo in range(0, n, 2 * ancho):
            mid, hi = min(lo + ancho, n), min(lo + 2 * ancho, n)
            izq, der = a[lo:mid], a[mid:hi]
            i = j = 0
            k = lo
            while i < len(izq) and j < len(der):
                if der[j] < izq[i]:
                    inv += len(izq) - i      # der[j] es menor que todo lo que queda a la izquierda
                    a[k] = der[j]
                    j += 1
                else:
                    a[k] = izq[i]
                    i += 1
                k += 1
            a[k:hi] = izq[i:] + der[j:]
        ancho *= 2
    return inv


def paridad_ciclos(p):
    """Paridad (0 par, 1 impar) de la permutación p de 0..n-1: (n − ciclos) mód 2."""
    n = len(p)
    visto = [False] * n
    ciclos = 0
    for i in range(n):
        if not visto[i]:
            ciclos += 1
            j = i
            while not visto[j]:
                visto[j] = True
                j = p[j]
    return (n - ciclos) % 2


def resoluble_puzzle(m, n, a):
    """¿Se ordena el puzzle m×n (valor m·n = hueco) deslizando fichas?"""
    N = m * n
    if m == 1 or n == 1:
        # En una línea las fichas nunca cambian su orden relativo.
        fichas = [x for x in a if x != N]
        return all(fichas[i] < fichas[i + 1] for i in range(len(fichas) - 1))
    perm = [x - 1 for x in a]                  # permutación de 0..N-1
    pos = a.index(N)
    f, c = divmod(pos, n)
    dist = (m - 1 - f) + (n - 1 - c)           # Manhattan del hueco a su meta
    return (paridad_ciclos(perm) + dist) % 2 == 0


def es_dif_cuadrados(N):
    """N = x² − y² con enteros x, y ⇔ N ≢ 2 (mód 4)."""
    return N % 4 != 2


def demo():
    print("2x3 [4 1 3 / 6 2 5]:", resoluble_puzzle(2, 3, [4, 1, 3, 6, 2, 5]))   # True
    print("2x3 [4 1 3 / 6 5 2]:", resoluble_puzzle(2, 3, [4, 1, 3, 6, 5, 2]))   # False
    p = [1, 2, 0, 4, 3]
    print("permutación", p, "inversiones:", inversiones(p), "paridad:", paridad_ciclos(p))  # 3, 1
    print("¿6 = x²−y²?", es_dif_cuadrados(6), " ¿12?", es_dif_cuadrados(12))    # False True


def _alcanzables(m, n):
    """BFS desde la configuración resuelta (las jugadas son reversibles)."""
    N = m * n
    inicio = tuple(range(1, N + 1))
    vistos = {inicio}
    cola = deque([inicio])
    while cola:
        e = cola.popleft()
        h = e.index(N)
        f, c = divmod(h, n)
        for df, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nf, nc = f + df, c + dc
            if 0 <= nf < m and 0 <= nc < n:
                v = nf * n + nc
                l = list(e)
                l[h], l[v] = l[v], l[h]
                t = tuple(l)
                if t not in vistos:
                    vistos.add(t)
                    cola.append(t)
    return vistos


def pruebas():
    random.seed(2018)

    # Casos borde
    assert inversiones([]) == 0 and paridad_ciclos([]) == 0
    assert inversiones([0]) == 0 and paridad_ciclos([0]) == 0
    assert resoluble_puzzle(1, 2, [2, 1]) and resoluble_puzzle(1, 2, [1, 2])
    assert not resoluble_puzzle(1, 3, [2, 1, 3])

    # Inversiones y paridad por ciclos contra el doble bucle
    for _ in range(2000):
        n = random.randint(0, 30)
        p = list(range(n))
        random.shuffle(p)
        bruto = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        assert inversiones(p) == bruto
        assert paridad_ciclos(p) == bruto % 2
        if n >= 2:                             # una transposición cambia la paridad
            i, j = random.sample(range(n), 2)
            q = p[:]
            q[i], q[j] = q[j], q[i]
            assert paridad_ciclos(q) != paridad_ciclos(p)
    # inversiones con repetidos (no permutación) también
    for _ in range(300):
        a = [random.randint(0, 5) for _ in range(random.randint(0, 20))]
        assert inversiones(a) == sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])

    # Puzzle: todas las configuraciones contra BFS
    for m, n in [(2, 2), (2, 3), (3, 2), (2, 4), (4, 2), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (3, 1), (5, 1)]:
        alcanz = _alcanzables(m, n)
        for e in itertools.permutations(range(1, m * n + 1)):
            assert resoluble_puzzle(m, n, list(e)) == (e in alcanz)

    # Diferencia de cuadrados contra búsqueda directa
    for N in range(1, 401):
        bruto = any(x * x - y * y == N for x in range(0, N + 1) for y in range(0, x + 1))
        assert es_dif_cuadrados(N) == bruto


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
