"""
Búsqueda completa — Fuerza bruta con bucles anidados («Iterative complete search»)
Nivel: Básico
Ejecutar: python fuerza_bruta_bucles.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Probar TODAS las posibilidades con bucles anidados y quedarse con las
    que cumplen. Es la primera idea que hay que considerar: si el número de
    candidatos cabe en el tiempo, es la solución más segura (no hay
    demostración que fallar). La clave es ESTIMAR antes de programar.
    Señales en el enunciado: N pequeño (≤ 20, ≤ 100, ≤ 500), pocas
    variables con rangos chicos, «encuentre todas las…», respuestas que
    caben en pocos dígitos (26^3 placas, 5 dígitos, 10 cifras distintas).

FUNCIÓN
    division_uva725(n) -> list[tuple[int, int]]
        Todos los pares (abcde, fghij) con abcde / fghij = n donde los 10
        dígitos (con ceros a la izquierda) son 0..9 sin repetir. Ordenados
        por el numerador.
    tripletas_suma(a, x) -> int
        Cuántas tripletas i < j < k cumplen a[i] + a[j] + a[k] == x
        (fuerza bruta O(N³)).
    tripletas_suma_rapida(a, x) -> int
        Lo mismo en O(N²) fijando dos índices y contando el tercero.
    alcanza(operaciones, segundos=1.0) -> bool
        Regla práctica: ¿cabe en el tiempo en Python? (~10^7 op/s simples).

IDEA Y ALGORITMO
    1) Contar candidatos. Antes de escribir, multiplicar los tamaños de los
       bucles. En Python, con operaciones simples, ~10^7 por segundo
       (C++ ~10^8–10^9). Tabla orientativa para ~1 s en Python:
            N ≤ 10      O(N!)          10! = 3,6·10^6
            N ≤ 20      O(2^N · N)     2^20 ≈ 10^6
            N ≤ 200     O(N³)          8·10^6
            N ≤ 3000    O(N²)          9·10^6
            N ≤ 10^6    O(N log N) u O(N)
    2) Reducir el espacio con lo que se sabe. UVa 725 (abcde/fghij = N):
       probar las 10! asignaciones de dígitos es 3,6·10^6 (lento en Python);
       pero si se fija fghij, abcde = N·fghij queda DETERMINADO. Basta
       recorrer fghij de 01234 a 98765 // N: ≤ 10^5 candidatos, cada uno
       con una comprobación barata de dígitos distintos.
    3) Romper el orden para no repetir: i < j < k en vez de tres bucles
       completos (divide entre 6 el trabajo y evita contar permutaciones).
    4) Si aun así no alcanza, eliminar el bucle más interno con una
       estructura (diccionario, sumas prefijas, búsqueda binaria): las
       tripletas pasan de O(N³) a O(N²) contando con un Counter cuántos
       valores x − a[i] − a[j] hay después de j.

MACROALGORITMO
    1. Identificar las variables libres de la solución y su rango.
    2. Multiplicar rangos → número de candidatos; comparar con ~10^7·seg.
    3. Si no alcanza: ¿alguna variable queda determinada por las otras?
       ¿se puede imponer un orden (i < j) o una simetría?
    4. Escribir los bucles, del más externo al más interno, con cortes
       tempranos (break/continue) cuando ya no puede servir.
    5. Comprobar cada candidato y guardar/contar los válidos.
    6. Si sigue sin alcanzar: sacar el bucle interno con una estructura.

COMPLEJIDAD
    division_uva725: ≤ 98765/N candidatos × O(10) por comprobación.
    tripletas_suma: O(N³); tripletas_suma_rapida: O(N²) tiempo, O(N) memoria.

EJEMPLO A MANO
    n = 62, se recorre fghij = 01234 … 98765 // 62 = 1592:
      fghij = 01234 → abcde = 76508 → "7650801234": el 0 se repite ✗
      fghij = 01245 → abcde = 77190 → "7719001245": 7, 1 y 0 repetidos ✗
      …
      fghij = 01283 → abcde = 79546 → "7954601283": diez dígitos distintos ✓
      fghij = 01528 → abcde = 94736 → "9473601528": diez dígitos distintos ✓
    Solo ~360 candidatos en vez de 10! = 3,6·10^6.
    tripletas_suma([1, 2, 3, 4, 5], 9) = 2   ({1,3,5}, {2,3,4})

ERRORES TÍPICOS
    - No estimar y programar algo de 10^9 operaciones en Python.
    - Olvidar los ceros a la izquierda (01283 tiene 5 dígitos): formatear
      con f"{x:05d}".
    - Bucles completos (i, j, k en 0..N−1) que cuentan cada tripleta 6 veces
      o usan el mismo índice dos veces.
    - Comprobaciones caras dentro del bucle más interno (crear listas,
      convertir a texto) cuando se pueden subir a un bucle exterior.
    - Rangos con off-by-one: range(a, b) no incluye b.

VARIANTES Y RELACIONADOS
    - Enumerar subconjuntos: subconjuntos_mascaras.py; permutaciones:
      permutaciones.py; con poda: backtracking_poda.py.
    - Si la condición es monótona en una variable: búsqueda binaria
      (busqueda_sobre_respuesta.py).
    - N ≤ 40 con subconjuntos: meet_in_the_middle.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/I - License Plates (enumerar los 26^3 candidatos)
    - ICPC/Colombia 2026/A - Balanced System Reactor (enumeración acotada de divisores)
    - UVa 725 «Division»; CSES «Apple Division» (2^N candidatos)

VERIFICACIÓN
    - Pruebas: OK. UVa 725 contra una enumeración independiente (todas las
      permutaciones de 5 dígitos para el denominador) para todos los N de
      2 a 79; tripletas O(N³) contra O(N²) y contra itertools.combinations
      en 1000 casos aleatorios + casos borde (python fuerza_bruta_bucles.py)
"""
import itertools
import random
from collections import Counter


def division_uva725(n):
    """Pares (abcde, fghij) con abcde / fghij = n y los 10 dígitos distintos."""
    res = []
    # fghij determina abcde = n * fghij; abcde debe tener a lo sumo 5 dígitos
    for den in range(1234, 98765 // n + 1):
        num = den * n
        s = f"{num:05d}{den:05d}"       # ceros a la izquierda incluidos
        if len(set(s)) == 10:           # 10 caracteres y 10 dígitos distintos
            res.append((num, den))
    return res


def tripletas_suma(a, x):
    """Tripletas i < j < k con a[i] + a[j] + a[k] == x; fuerza bruta O(N³)."""
    n = len(a)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            falta = x - a[i] - a[j]     # subir el cálculo fuera del bucle interno
            for k in range(j + 1, n):
                if a[k] == falta:
                    total += 1
    return total


def tripletas_suma_rapida(a, x):
    """Lo mismo en O(N²): se reemplaza el bucle de k por un Counter."""
    n = len(a)
    total = 0
    despues = Counter(a)                # cuenta de valores con índice > j (se ajusta)
    for j in range(n):
        despues[a[j]] -= 1              # ahora 'despues' cubre índices > j
        for i in range(j):
            total += despues[x - a[i] - a[j]]
    return total


def alcanza(operaciones, segundos=1.0):
    """Regla práctica para Python: ~10^7 operaciones simples por segundo."""
    return operaciones <= 10**7 * segundos


def demo():
    for n in (62, 61):
        pares = division_uva725(n)
        if pares:
            for num, den in pares:
                print(f"{num:05d} / {den:05d} = {n}")
        else:
            print(f"There are no solutions for {n}.")
    print("tripletas_suma([1, 2, 3, 4, 5], 9) =", tripletas_suma([1, 2, 3, 4, 5], 9))   # 2
    print("¿10! cabe en 1 s?", alcanza(3628800), " ¿200^3?", alcanza(200**3),
          " ¿10^5 al cuadrado?", alcanza(10**10))


def pruebas():
    random.seed(725)

    # Casos borde y ejemplo del enunciado de UVa 725
    assert division_uva725(62) == [(79546, 1283), (94736, 1528)]
    assert division_uva725(61) == []
    assert tripletas_suma([], 0) == 0 == tripletas_suma_rapida([], 0)
    assert tripletas_suma([1, 1], 3) == 0 == tripletas_suma_rapida([1, 1], 3)
    assert tripletas_suma([0] * 6, 0) == 20 == tripletas_suma_rapida([0] * 6, 0)
    assert alcanza(10**7) and not alcanza(10**8)

    # UVa 725 contra otra enumeración: el denominador recorre las
    # permutaciones de 5 dígitos distintos (30240) en vez de un rango.
    dens = [int("".join(p)) for p in itertools.permutations("0123456789", 5)]
    for n in range(2, 80):
        esperado = []
        for den in dens:
            num = den * n
            if num < 100000 and len(set(f"{num:05d}{den:05d}")) == 10:
                esperado.append((num, den))
        assert division_uva725(n) == sorted(esperado)

    for _ in range(1000):
        a = [random.randint(-5, 5) for _ in range(random.randint(0, 12))]
        x = random.randint(-10, 10)
        bruta = sum(1 for t in itertools.combinations(a, 3) if sum(t) == x)
        assert tripletas_suma(a, x) == bruta == tripletas_suma_rapida(a, x)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
