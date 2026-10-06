"""
Matemáticas — Eliminación gaussiana: exacta (Fraction), módulo p y en GF(2) («Gaussian elimination»)
Nivel: Intermedio/Avanzado
Ejecutar: python eliminacion_gaussiana.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Resolver un sistema lineal A·x = b de m ecuaciones y n incógnitas y
    decir si no tiene solución, tiene una única o infinitas; calcular el
    rango y el determinante. En GF(2) (todo módulo 2, suma = XOR) resuelve
    problemas de interruptores («Lights Out»), paridades y bases XOR.
    Cómo reconocerlo: «encontrar valores que cumplan estas ecuaciones
    lineales», probabilidades/esperanzas definidas por ecuaciones que se
    refieren unas a otras (cadenas de Markov), «presionar un botón cambia
    estos focos», «subconjunto con XOR dado»; n ≤ ~300 (O(n³)).

FUNCIÓN
    gauss_fraction(A, b) -> (estado, x, rango)
        Exacto con fractions.Fraction. estado: 0 = sin solución,
        1 = única, 2 = infinitas (x es UNA solución, libres = 0); x = None si 0.
    gauss_mod(A, b, p) -> (estado, x, rango)    igual, todo mód p primo.
    determinante_mod(A, p) -> int               det(A) mód p.
    gauss_gf2(filas, n) -> (estado, x)
        filas[i] es un entero: bits 0..n−1 = coeficientes, bit n = lado
        derecho. x es un entero con la solución (bit j = x_j).

IDEA Y ALGORITMO
    Las operaciones elementales de fila (intercambiar dos filas, multiplicar
    una por c ≠ 0, sumar a una fila un múltiplo de otra) son invertibles, así
    que NO cambian el conjunto de soluciones. Se usan para llevar [A | b] a
    forma escalonada reducida:
      para cada columna c, buscar una fila (aún no usada) con entrada ≠ 0
      (el pivote), subirla, normalizar el pivote a 1 y anular la columna c
      en TODAS las demás filas.
    Al terminar, rango = número de pivotes r. Lectura del resultado:
    - Si alguna fila queda 0 = d con d ≠ 0 → sin solución (rango(A) <
      rango([A|b]), teorema de Rouché–Frobenius).
    - Si no y r = n → única (cada variable es pivote de su fila).
    - Si no y r < n → infinitas (las n − r variables sin pivote son libres;
      con libres = 0 cada pivote vale su lado derecho). En GF(2)/mód p
      «infinitas» significa exactamente p^(n−r) soluciones.
    Determinante: los intercambios cambian el signo, normalizar divide por
    el pivote; det = (±1) · Π pivotes (0 si falta algún pivote).
    En GF(2) una fila es un entero y «restar» es XOR: cada eliminación es
    una sola operación sobre enteros (bitset), muy rápido en Python.
    Fraction evita los errores de redondeo pero sus numeradores crecen; con
    flotantes hay que pivotar por el mayor |valor| (pivoteo parcial).

MACROALGORITMO
    1. Armar la matriz aumentada [A | b].
    2. fila = 0; para cada columna c = 0..n−1:
    3.   buscar i ≥ fila con M[i][c] ≠ 0; si no hay, c es variable libre.
    4.   intercambiar filas i y fila; dividir la fila por M[fila][c].
    5.   para toda otra fila j con M[j][c] ≠ 0: M[j] −= M[j][c]·M[fila].
    6.   guardar donde[c] = fila; fila += 1.
    7. Revisar filas ≥ rango: si alguna tiene b ≠ 0 → sin solución.
    8. x[c] = M[donde[c]][n] para columnas con pivote, 0 para las libres;
       estado = única si rango = n, si no infinitas.

COMPLEJIDAD
    O(min(m,n)·m·n) operaciones: n = m = 300 son 2,7·10^7 (≈ 3–5 s en
    Python puro con mód p; Fraction es bastante más lento por el tamaño de
    los números). GF(2) con bitsets: O(n²) operaciones sobre enteros de n
    bits, n = 2000 en ~1 s.

EJEMPLO A MANO
    x + y + z = 6, 2y + 5z = −4, 2x + 5y − z = 27:
    F3 −= 2F1 → (0, 3, −3 | 15); pivote y: F2/2 → (0, 1, 5/2 | −2);
    eliminando y: F3 → (0, 0, −21/2 | 21) → z = −2, y = 3, x = 5.
    GF(2): x0⊕x1 = 1, x1⊕x2 = 0 → rango 2 < 3: infinitas (2 soluciones),
    con x2 = 0: x1 = 0, x0 = 1.

ERRORES TÍPICOS
    - Con flotantes, no pivotar por el máximo y comparar con == 0 en vez de
      |v| < eps.
    - Anular solo las filas de abajo y luego olvidar la sustitución hacia
      atrás (aquí se anula en todas: forma reducida, no hace falta).
    - Declarar «única» solo porque no hay contradicción, sin ver el rango.
    - Usar la columna de b como si fuera una variable al buscar pivotes.
    - Mód p no primo: no todo pivote no nulo es invertible.

VARIANTES Y RELACIONADOS
    - Pivoteo parcial con flotantes (Guangzhou G lo usa con n = 301).
    - Base XOR («xor basis»): Gauss en GF(2) incremental, para máximo XOR
      de un subconjunto (trucos_bits.py).
    - Inversa de una matriz: eliminar [A | I].
    - probabilidad_esperanza.py (esperanzas con ciclos = sistema lineal).
    - Matrix-tree de Kirchhoff: número de árboles generadores = un
      determinante.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/G - Great Coin Game (sistema (n+1)×(n+1) de
      Conway resuelto con Gauss y pivoteo parcial)
    - ICPC/Colombia 2024/F - Turnswitch (Lights Out: la solución del repo
      enumera la primera fila; el modelo general es un sistema en GF(2))

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (probar las p^n asignaciones) en
      sistemas mód 5 y GF(2) con n ≤ 4 (1500 casos), Fraction contra rango
      por menores (determinantes por Leibniz) y comprobación A·x = b en 500
      casos, determinante mód p contra Leibniz (python eliminacion_gaussiana.py)
"""
import itertools
import random
from fractions import Fraction


def gauss_fraction(A, b):
    """Resuelve A x = b exactamente. Devuelve (estado, x, rango)."""
    m, n = len(A), (len(A[0]) if A else 0)
    M = [[Fraction(v) for v in A[i]] + [Fraction(b[i])] for i in range(m)]
    donde = [-1] * n            # donde[c] = fila del pivote de la columna c
    fila = 0
    for c in range(n):
        piv = next((i for i in range(fila, m) if M[i][c] != 0), -1)
        if piv == -1:
            continue                                  # c es variable libre
        M[fila], M[piv] = M[piv], M[fila]
        inv = 1 / M[fila][c]
        M[fila] = [v * inv for v in M[fila]]           # pivote = 1
        for j in range(m):
            if j != fila and M[j][c] != 0:
                f = M[j][c]
                M[j] = [vj - f * vf for vj, vf in zip(M[j], M[fila])]
        donde[c] = fila
        fila += 1
    rango = fila
    if any(M[i][n] != 0 for i in range(rango, m)):    # fila 0 = d ≠ 0
        return 0, None, rango
    x = [M[donde[c]][n] if donde[c] != -1 else Fraction(0) for c in range(n)]
    return (1 if rango == n else 2), x, rango


def gauss_mod(A, b, p):
    """Resuelve A x = b mód p primo. Devuelve (estado, x, rango)."""
    m, n = len(A), (len(A[0]) if A else 0)
    M = [[v % p for v in A[i]] + [b[i] % p] for i in range(m)]
    donde = [-1] * n
    fila = 0
    for c in range(n):
        piv = next((i for i in range(fila, m) if M[i][c]), -1)
        if piv == -1:
            continue
        M[fila], M[piv] = M[piv], M[fila]
        inv = pow(M[fila][c], p - 2, p)                # inverso por Fermat
        M[fila] = [v * inv % p for v in M[fila]]
        for j in range(m):
            if j != fila and M[j][c]:
                f = M[j][c]
                M[j] = [(vj - f * vf) % p for vj, vf in zip(M[j], M[fila])]
        donde[c] = fila
        fila += 1
    rango = fila
    if any(M[i][n] for i in range(rango, m)):
        return 0, None, rango
    x = [M[donde[c]][n] if donde[c] != -1 else 0 for c in range(n)]
    return (1 if rango == n else 2), x, rango


def determinante_mod(A, p):
    """det(A) mód p primo (A cuadrada)."""
    n = len(A)
    M = [[v % p for v in fila] for fila in A]
    det = 1
    for c in range(n):
        piv = next((i for i in range(c, n) if M[i][c]), -1)
        if piv == -1:
            return 0
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            det = -det                                  # un intercambio cambia el signo
        det = det * M[c][c] % p
        inv = pow(M[c][c], p - 2, p)
        for j in range(c + 1, n):
            if M[j][c]:
                f = M[j][c] * inv % p
                M[j] = [(vj - f * vc) % p for vj, vc in zip(M[j], M[c])]
    return det % p


def gauss_gf2(filas, n):
    """Sistema en GF(2): filas[i] = coeficientes en bits 0..n-1, lado derecho en bit n.

    Devuelve (estado, x) con x entero (bit j = x_j); x = None si no hay solución.
    """
    filas = list(filas)
    m = len(filas)
    donde = [-1] * n
    fila = 0
    for c in range(n):
        piv = next((i for i in range(fila, m) if filas[i] >> c & 1), -1)
        if piv == -1:
            continue
        filas[fila], filas[piv] = filas[piv], filas[fila]
        for j in range(m):
            if j != fila and filas[j] >> c & 1:
                filas[j] ^= filas[fila]                # restar = XOR
        donde[c] = fila
        fila += 1
    if any(filas[i] >> n & 1 for i in range(fila, m)):
        return 0, None
    x = 0
    for c in range(n):
        if donde[c] != -1 and filas[donde[c]] >> n & 1:
            x |= 1 << c
    return (1 if fila == n else 2), x


def demo():
    A = [[1, 1, 1], [0, 2, 5], [2, 5, -1]]
    b = [6, -4, 27]
    estado, x, r = gauss_fraction(A, b)
    print("estado", estado, "x =", [str(v) for v in x], "rango", r)   # 1 [5, 3, -2] 3
    print("mód 7:", gauss_mod(A, b, 7))   # det = −21 ≡ 0 (mód 7): rango 2, infinitas
    print("det mód 1e9+7:", determinante_mod(A, 10**9 + 7))          # -21 → 999999986
    # x0⊕x1 = 1, x1⊕x2 = 0  (bits 0..2 coeficientes, bit 3 lado derecho)
    print("GF(2):", gauss_gf2([0b1011, 0b0110], 3))                  # (2, 1)
    print("sin solución:", gauss_fraction([[1, 1], [2, 2]], [1, 3]))


def _det_leibniz(M):
    n = len(M)
    total = 0
    for perm in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        prod = 1
        for i in range(n):
            prod *= M[i][perm[i]]
        total += -prod if inv % 2 else prod
    return total


def _rango_menores(M):
    """Rango = tamaño del mayor menor con determinante ≠ 0 (fuerza bruta)."""
    m, n = len(M), (len(M[0]) if M else 0)
    for k in range(min(m, n), 0, -1):
        for fs in itertools.combinations(range(m), k):
            for cs in itertools.combinations(range(n), k):
                if _det_leibniz([[M[i][j] for j in cs] for i in fs]) != 0:
                    return k
    return 0


def pruebas():
    random.seed(4242)

    # Casos borde
    assert gauss_fraction([[0, 0]], [0]) == (2, [0, 0], 0)
    assert gauss_fraction([[0, 0]], [1])[0] == 0
    assert gauss_mod([[3]], [6], 7) == (1, [2], 1)
    assert gauss_gf2([], 2) == (2, 0)
    assert determinante_mod([[0, 1], [1, 0]], 7) == 6

    # Mód 5 y GF(2) contra probar todas las asignaciones
    for _ in range(1500):
        p = random.choice([2, 5])
        m, n = random.randint(1, 4), random.randint(1, 4)
        A = [[random.randint(0, p - 1) for _ in range(n)] for _ in range(m)]
        b = [random.randint(0, p - 1) for _ in range(m)]
        sols = [x for x in itertools.product(range(p), repeat=n)
                if all(sum(A[i][j] * x[j] for j in range(n)) % p == b[i] for i in range(m))]
        estado, x, r = gauss_mod(A, b, p)
        esperado = 0 if not sols else (1 if len(sols) == 1 else 2)
        assert estado == esperado
        if sols:
            assert tuple(x) in sols and len(sols) == p ** (n - r)
        if p == 2:
            filas = [sum(A[i][j] << j for j in range(n)) | (b[i] << n) for i in range(m)]
            e2, x2 = gauss_gf2(filas, n)
            assert e2 == esperado
            if sols:
                assert tuple((x2 >> j) & 1 for j in range(n)) in sols

    # Fraction: rango contra menores, solución comprobada, consistencia
    for _ in range(500):
        m, n = random.randint(1, 4), random.randint(1, 4)
        A = [[random.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        b = [random.randint(-5, 5) for _ in range(m)]
        estado, x, r = gauss_fraction(A, b)
        assert r == _rango_menores(A)
        aum = [A[i] + [b[i]] for i in range(m)]
        consistente = _rango_menores(aum) == r          # Rouché–Frobenius
        assert (estado != 0) == consistente
        if estado:
            assert all(sum(A[i][j] * x[j] for j in range(n)) == b[i] for i in range(m))
            assert estado == (1 if r == n else 2)

    # Determinante mód p contra Leibniz
    for _ in range(300):
        n = random.randint(1, 5)
        A = [[random.randint(-9, 9) for _ in range(n)] for _ in range(n)]
        for p in (7, 10**9 + 7):
            assert determinante_mod(A, p) == _det_leibniz(A) % p


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
