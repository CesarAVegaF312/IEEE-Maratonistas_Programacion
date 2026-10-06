"""
Matemáticas — Rango y des-rango de combinaciones y permutaciones («ranking / unranking»)
Nivel: Intermedio
Ejecutar: python rango_combinacion.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Pasar de un objeto combinatorio (un k-subconjunto, una permutación) a su
    POSICIÓN en orden lexicográfico (rango) y al revés (des-rango), sin
    generar la lista completa, que puede tener 10^17 elementos.
    Cómo reconocerlo: «todos los … se numeran en orden lexicográfico; dado
    uno, imprima su número» o «imprima el k-ésimo»; «la siguiente
    permutación tras saltar r»; codificar un estado (permutación) como un
    entero compacto para usarlo en un arreglo/BFS.

FUNCIÓN
    rango_comb(n, a) -> int        a = k-subconjunto de {0..n-1} en orden
                                   creciente; posición 0-indexada entre los
                                   C(n, k) en orden lexicográfico.
    desrango_comb(n, k, r) -> list el k-subconjunto con rango r (0 ≤ r < C(n,k)).
    rango_perm(p) -> int           p = permutación de 0..n-1; rango 0-indexado
                                   entre las n! en orden lexicográfico.
    desrango_perm(n, r) -> list    la permutación con rango r (0 ≤ r < n!).

IDEA Y ALGORITMO
    El rango de x es el número de objetos lexicográficamente MENORES que x.
    Se cuentan agrupándolos por la primera posición i donde difieren de x:
    coinciden en 0..i-1 y en la posición i tienen algo menor.
    - Combinaciones: si en la posición i se pone v con a[i-1] < v < a[i], las
      k−1−i posiciones restantes se eligen entre los n−1−v valores mayores
      que v: C(n−1−v, k−1−i) formas. Sumando sobre i y v:
        rango = Σ_i Σ_{v=a[i-1]+1}^{a[i]-1} C(n−1−v, k−1−i),  a[-1] = −1.
      Cada objeto menor se cuenta una sola vez (por su primera diferencia).
    - Permutaciones (código de Lehmer): en la posición i, los valores
      posibles menores que p[i] son los NO usados antes y menores que p[i]
      (c_i de ellos); cada uno deja (n−1−i)! formas de completar:
        rango = Σ_i c_i · (n−1−i)!   (sistema factorial de numeración).
    - Des-rango: es el mismo conteo leído como «búsqueda»: en cada posición
      se prueban los candidatos en orden creciente; si el bloque de objetos
      que empieza con el candidato tiene tamaño ≤ r, se salta (r −= tamaño);
      si no, ese candidato es el correcto y se baja a la siguiente posición.
    El ingenuo (generar todos y buscar) cuesta C(n, k) o n!: inviable.

MACROALGORITMO
    1. Rango: recorrer las posiciones i de izquierda a derecha.
    2. Para cada valor candidato menor que x[i] (y válido), sumar cuántos
       objetos completan ese prefijo (binomial o factorial).
    3. Marcar x[i] como usado y seguir.
    4. Des-rango: en cada posición, recorrer candidatos crecientes restando
       el tamaño de su bloque mientras r ≥ tamaño; fijar el primero que no.
    5. Repetir hasta llenar las k (o n) posiciones.

COMPLEJIDAD
    Combinaciones: O(n) binomiales (math.comb), memoria O(k).
    Permutaciones: O(n²) con lista de no usados; O(n log n) con un árbol de
    Fenwick para contar «no usados menores» (n ~ 10^5).
    Los rangos pueden ser enormes (n!), Python los maneja sin problema.

EJEMPLO A MANO
    n=5, a=[0,2,4] (en 1-indexado {1,3,5}): i=0: nada menor que 0.
    i=1: v=1 → C(5−1−1, 1) = 3. i=2: v=3 → C(0, 0) = 1. Rango 4.
    p=[2,0,1]: c = [2, 0, 0] → 2·2! + 0·1! + 0·0! = 4 (orden: 012, 021, 102,
    120, 201, 210 → 201 es la posición 4 ✔).

ERRORES TÍPICOS
    - Mezclar 0-indexado y 1-indexado en valores y rangos (el enunciado
      puede numerar desde 1).
    - En permutaciones, contar todos los menores que p[i] en vez de solo
      los NO usados.
    - En el des-rango, usar < en vez de ≤ al decidir si se salta un bloque
      (r es 0-indexado: si r == tamaño, el objeto está en el siguiente bloque).
    - Factoriales/binomiales que desbordan en C++ (en Python no).

VARIANTES Y RELACIONADOS
    - Rango de permutaciones de un MULTICONJUNTO: el bloque de cada
      candidato es un multinomial (combinatoria_basica.py).
    - Rango de cadenas con restricciones (p. ej. paréntesis balanceados):
      igual idea con el conteo hecho por DP (catalan.py).
    - Sistema numérico combinatorio («combinadic»): otra forma del mismo
      rango, ordenando por el elemento mayor.
    - Contar inversiones con Fenwick (mismo truco para el código de Lehmer).

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/D - Discrete Catalog (rango de una combinación en
      orden lexicográfico, n ≤ 60)

VERIFICACIÓN
    - Pruebas: OK contra la lista completa generada con itertools.combinations
      / itertools.permutations (que salen en orden lexicográfico) para todos
      los n ≤ 7, y ida y vuelta rango ↔ des-rango en 500 casos aleatorios
      con n ≤ 60 (python rango_combinacion.py)
"""
import itertools
import random
from math import comb, factorial


def rango_comb(n, a):
    """Posición lexicográfica (desde 0) del k-subconjunto creciente a de {0..n-1}."""
    k = len(a)
    r = 0
    previo = -1
    for i, ai in enumerate(a):
        # valores menores que a[i] que podrían ir en la posición i
        for v in range(previo + 1, ai):
            r += comb(n - 1 - v, k - 1 - i)   # completar con valores > v
        previo = ai
    return r


def desrango_comb(n, k, r):
    """k-subconjunto de {0..n-1} con rango lexicográfico r (0 ≤ r < C(n,k))."""
    res = []
    v = 0
    for i in range(k):
        while True:
            bloque = comb(n - 1 - v, k - 1 - i)   # subconjuntos que siguen con v
            if r < bloque:
                break
            r -= bloque                            # saltar todo el bloque de v
            v += 1
        res.append(v)
        v += 1
    return res


def rango_perm(p):
    """Rango lexicográfico (desde 0) de la permutación p de 0..n-1 (Lehmer)."""
    n = len(p)
    usado = [False] * n
    r = 0
    for i, x in enumerate(p):
        c = sum(1 for y in range(x) if not usado[y])   # menores aún libres
        r += c * factorial(n - 1 - i)
        usado[x] = True
    return r


def desrango_perm(n, r):
    """Permutación de 0..n-1 con rango lexicográfico r (0 ≤ r < n!)."""
    libres = list(range(n))
    res = []
    for i in range(n):
        f = factorial(n - 1 - i)          # tamaño del bloque de cada candidato
        q, r = divmod(r, f)               # saltar q bloques completos
        res.append(libres.pop(q))
    return res


def demo():
    print("rango_comb(5, [0,2,4]) =", rango_comb(5, [0, 2, 4]))       # 4
    print("desrango_comb(5, 3, 4) =", desrango_comb(5, 3, 4))         # [0, 2, 4]
    print("rango_perm([2,0,1]) =", rango_perm([2, 0, 1]))             # 4
    print("desrango_perm(3, 4) =", desrango_perm(3, 4))               # [2, 0, 1]
    print("rango de {29..59} entre C(60,31):", rango_comb(60, list(range(29, 60))))


def pruebas():
    random.seed(2025)

    # Casos borde
    assert rango_comb(0, []) == 0 and desrango_comb(0, 0, 0) == []
    assert rango_comb(4, []) == 0 and desrango_comb(4, 0, 0) == []
    assert rango_perm([]) == 0 and desrango_perm(0, 0) == []
    assert rango_perm([0]) == 0

    # Contra la lista completa en orden lexicográfico
    for n in range(0, 8):
        for k in range(0, n + 1):
            for idx, c in enumerate(itertools.combinations(range(n), k)):
                assert rango_comb(n, list(c)) == idx
                assert desrango_comb(n, k, idx) == list(c)
        for idx, p in enumerate(itertools.permutations(range(n))):
            assert rango_perm(list(p)) == idx
            assert desrango_perm(n, idx) == list(p)

    # Ida y vuelta con n grande
    for _ in range(500):
        n = random.randint(1, 60)
        k = random.randint(0, n)
        r = random.randrange(comb(n, k))
        a = desrango_comb(n, k, r)
        assert len(a) == k and a == sorted(set(a)) and rango_comb(n, a) == r
        m = random.randint(1, 30)
        r = random.randrange(factorial(m))
        p = desrango_perm(m, r)
        assert sorted(p) == list(range(m)) and rango_perm(p) == r


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
