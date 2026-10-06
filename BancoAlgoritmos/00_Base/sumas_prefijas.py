"""
Base — Sumas prefijas 1D y 2D («Prefix sums»)
Nivel: Básico
Ejecutar: python sumas_prefijas.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Responder en O(1) «¿cuánto suman los elementos de la posición l a la r?»
    (o de un rectángulo de una matriz), después de un precálculo O(N).
    Señales en el enunciado: arreglo FIJO (no cambia) + muchas consultas de
    suma/conteo sobre rangos; «cuántos ... entre l y r»; sumas de
    subarreglos o submatrices; N y Q hasta 10^5–10^6.

FUNCIÓN
    prefijas(a) -> P             P[i] = a[0] + … + a[i-1], len(P) = len(a) + 1
    suma_rango(P, l, r) -> int   a[l] + … + a[r]  (índices desde 0, inclusive;
                                 0 si l > r)
    prefijas_2d(M) -> P          P[i][j] = suma del rectángulo M[0..i-1][0..j-1]
    suma_rect(P, f1, c1, f2, c2) -> int
                                 suma de M[f1..f2][c1..c2] (inclusive)

IDEA Y ALGORITMO
    1D: la suma de a[l..r] es (suma de los primeros r+1) − (suma de los
    primeros l) = P[r+1] − P[l]. P se arma con P[i+1] = P[i] + a[i].
    Usar P[0] = 0 (un elemento extra al inicio) elimina el caso especial
    l = 0.
    2D: P[i][j] = suma de la submatriz superior izquierda de i filas y j
    columnas. Por inclusión–exclusión:
        P[i+1][j+1] = M[i][j] + P[i][j+1] + P[i+1][j] − P[i][j]
    (el rectángulo de arriba y el de la izquierda se solapan en P[i][j],
    que se contó dos veces). La consulta usa la misma idea al revés:
        suma(f1..f2, c1..c2) = P[f2+1][c2+1] − P[f1][c2+1] − P[f2+1][c1] + P[f1][c1]
    El ingenuo (sumar el rango en cada consulta) es O(N) por consulta:
    con N = Q = 10^5 son 10^10 operaciones; con prefijas son 2·10^5.

MACROALGORITMO
    1. P = [0] * (n + 1).
    2. Para i = 0..n-1: P[i+1] = P[i] + a[i].
    3. Cada consulta [l, r]: responder P[r+1] − P[l].
    4. (2D) P de (n+1)×(m+1) con ceros en la fila 0 y la columna 0.
    5. (2D) Llenar con la fórmula de inclusión–exclusión, fila por fila.
    6. (2D) Cada rectángulo: cuatro términos con signos + − − +.

COMPLEJIDAD
    1D: precálculo O(N), consulta O(1), memoria O(N).
    2D: precálculo O(N·M), consulta O(1), memoria O(N·M).
    En Python, itertools.accumulate arma 10^6 prefijas en ~0,1 s.

EJEMPLO A MANO
    a = [3, 1, 4, 1, 5, 9]
    P = [0, 3, 4, 8, 9, 14, 23]
    suma_rango(P, 2, 4) = P[5] − P[2] = 14 − 4 = 10   (4 + 1 + 5)
    M = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]      P (4×4) = [[0, 0, 0, 0], [0, 1, 3, 6],
                                    [0, 5, 12, 21], [0, 12, 27, 45]]
    suma_rect(P, 1, 1, 2, 2) = P[3][3] − P[1][3] − P[3][1] + P[1][1]
                             = 45 − 6 − 12 + 1 = 28   (5 + 6 + 8 + 9)

ERRORES TÍPICOS
    - Desfase de índices: P[r] − P[l] suma a[l..r-1], no a[l..r]. Fijar UNA
      convención (aquí P tiene n+1 posiciones) y respetarla.
    - Olvidar el + P[f1][c1] en 2D (se restó dos veces).
    - Usar prefijas cuando el arreglo CAMBIA entre consultas: cada cambio
      cuesta O(N). Ahí va un árbol de Fenwick o de segmentos.
    - Enunciado con índices desde 1: convertir al leer (l-1, r-1).
    - En C++ desbordar int; en Python no pasa, pero sí tarda si los números
      crecen muchísimo (no es el caso normal).

VARIANTES Y RELACIONADOS
    - Prefijas de conteo: P[i] = cuántos a[j] cumplen algo, j < i.
    - Prefijas de XOR (xor de rango = P[r+1] ^ P[l]); de productos solo con
      inverso modular.
    - Subarreglo con suma K / más largo con suma 0: prefijas + diccionario
      (conteo_diccionarios.py).
    - Inverso de la operación: arreglo_diferencias.py (sumar en rangos).
    - Ventana de tamaño fijo: ventana_deslizante.py.
    - Con actualizaciones: árbol de Fenwick / árbol de segmentos.

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/A - Account Qualifying (sumas prefijas + primera aparición)
    - ICPC/Colombia 2026/B - Bankey (ventana con sumas prefijas)
    - ICPC/OMP 2017 Murcia/B - Pool Filling (sumas prefijas + búsqueda binaria)
    - CSES «Static Range Sum Queries», «Forest Queries» (2D)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (sumar el rango con sum()) en 600
      arreglos/matrices aleatorios con todas sus consultas + casos borde
      (python sumas_prefijas.py)
"""
import random
from itertools import accumulate


def prefijas(a):
    """P[i] = a[0] + ... + a[i-1]; len(P) = len(a) + 1, P[0] = 0."""
    return [0] + list(accumulate(a))     # igual a: P[i+1] = P[i] + a[i]


def suma_rango(P, l, r):
    """a[l] + ... + a[r] (inclusive, índices desde 0); 0 si l > r."""
    if l > r:
        return 0
    return P[r + 1] - P[l]


def prefijas_2d(M):
    """P[i][j] = suma de M[0..i-1][0..j-1]; tamaño (n+1) x (m+1)."""
    n = len(M)
    m = len(M[0]) if n else 0
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        fila, arriba, abajo = M[i], P[i], P[i + 1]
        for j in range(m):
            # inclusión–exclusión: arriba + izquierda − esquina (contada 2 veces)
            abajo[j + 1] = fila[j] + arriba[j + 1] + abajo[j] - arriba[j]
    return P


def suma_rect(P, f1, c1, f2, c2):
    """Suma de M[f1..f2][c1..c2] (inclusive); 0 si el rectángulo es vacío."""
    if f1 > f2 or c1 > c2:
        return 0
    return P[f2 + 1][c2 + 1] - P[f1][c2 + 1] - P[f2 + 1][c1] + P[f1][c1]


def demo():
    a = [3, 1, 4, 1, 5, 9]
    P = prefijas(a)
    print("a =", a)
    print("P =", P)                                        # [0,3,4,8,9,14,23]
    print("suma_rango(P, 2, 4) =", suma_rango(P, 2, 4))    # 10
    M = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    P2 = prefijas_2d(M)
    print("P2 =", P2)
    print("suma_rect(P2, 1, 1, 2, 2) =", suma_rect(P2, 1, 1, 2, 2))   # 28


def pruebas():
    random.seed(777)

    # Casos borde
    assert prefijas([]) == [0]
    assert suma_rango(prefijas([5]), 0, 0) == 5
    assert suma_rango(prefijas([5, 6]), 1, 0) == 0
    assert prefijas_2d([]) == [[0]]
    assert suma_rect(prefijas_2d([[7]]), 0, 0, 0, 0) == 7

    # 1D: todas las consultas contra sum()
    for _ in range(300):
        n = random.randint(0, 25)
        a = [random.randint(-10**9, 10**9) for _ in range(n)]
        P = prefijas(a)
        for l in range(n):
            for r in range(l, n):
                assert suma_rango(P, l, r) == sum(a[l:r + 1])

    # 2D: todas las consultas contra doble suma
    for _ in range(300):
        n = random.randint(1, 6)
        m = random.randint(1, 6)
        M = [[random.randint(-50, 50) for _ in range(m)] for _ in range(n)]
        P = prefijas_2d(M)
        for f1 in range(n):
            for f2 in range(f1, n):
                for c1 in range(m):
                    for c2 in range(c1, m):
                        bruta = sum(M[i][j] for i in range(f1, f2 + 1) for j in range(c1, c2 + 1))
                        assert suma_rect(P, f1, c1, f2, c2) == bruta


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
