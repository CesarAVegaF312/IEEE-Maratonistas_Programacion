"""
Colombia 2023 — F: Finding Common Passwords («Encontrando contraseñas comunes»)
Ejecutar: python find.py < find.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un ingeniero de seguridad audita N contraseñas y quiere encontrar la
    cadena más larga que aparece como subcadena (contigua) en al menos K de
    ellas, para detectar "palabras comunes" que la gente mete en sus claves.

QUÉ HAY QUE HACER
    Entrada: varios casos "N K" (1 ≤ K ≤ N ≤ 100 000) y N contraseñas de
             letras a-z, con suma de longitudes ≤ 100 000. Termina con "0 0".
    Salida:  por caso, la subcadena más larga presente en ≥ K contraseñas;
             si hay empate, la lexicográficamente menor; '*' si es la vacía.

IDEA Y ALGORITMO
    Búsqueda binaria sobre la respuesta (la longitud) + hashing polinomial
    (rolling hash) módulo el primo de Mersenne 2^61 − 1 con base aleatoria.
    Monotonía: si una cadena de largo L aparece en ≥ K contraseñas, su
    prefijo de largo L−1 también aparece en (al menos) esas mismas K. Por
    eso "existe una subcadena de largo L en ≥ K contraseñas" es verdadero
    hasta cierto L* y falso después: se busca L* en binario.
    Prueba para un L fijo: para cada contraseña se calcula el CONJUNTO de
    hashes de sus ventanas de largo L (el conjunto hace que una contraseña
    cuente una sola vez aunque contenga la subcadena varias veces) y se
    suma 1 al contador de cada hash. Los hashes con contador ≥ K son
    subcadenas válidas. Cada prueba es O(suma de longitudes).
    Desempate: con L* ya conocido, se toma un representante de cada hash
    válido y se elige el menor texto real con min() (se comparan cadenas de
    verdad, no hashes).
    Fuerza bruta de todas las subcadenas sería O(S^2) cadenas (S = 10^5),
    inviable. Alternativas exactas con la misma complejidad asintótica
    serían arreglo de sufijos + ventana deslizante, o autómata de sufijos.
    Riesgo de colisión: con 2^61 − 1 y ~10^5 hashes por prueba, la
    probabilidad es del orden de 10^-8; se considera despreciable.

MACROALGORITMO
    1. Leer N, K y las contraseñas; precalcular hashes prefijo de cada una
       y las potencias de la base.
    2. Búsqueda binaria de L entre 0 y la longitud máxima: L es factible si
       algún hash de ventana de largo L aparece en ≥ K contraseñas distintas.
    3. Si L* = 0, imprimir '*'.
    4. Si no, recolectar los hashes válidos de largo L*, guardar un texto
       representante de cada uno e imprimir el menor.

COMPLEJIDAD
    Tiempo O(S log S) con S = suma de longitudes, memoria O(S).
    Medido en Python con S = 100 000: entre 0,13 s y 0,54 s por caso
    (1000 claves aleatorias; 2 claves de 50 000 casi iguales; 100 000
    claves de 1 letra; una clave de 100 000 'a').

EJEMPLO A MANO
    {monkey, monk, money, motorcycle, recycle}, K = 3: "mon" aparece en 3
    contraseñas; ninguna cadena de largo 4 aparece en 3 -> "mon".

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2023/F")
    - Fuerza bruta: enumerar todas las subcadenas de todas las contraseñas,
      contar en cuántas aparece cada una y elegir la más larga y menor;
      coincide en 500 casos aleatorios (alfabeto {a, b, c}, para forzar
      muchas repeticiones y empates).
"""
import random
import sys

MOD = (1 << 61) - 1
BASE = random.randrange(10 ** 5, MOD - 1)


def hashes_prefijo(s):
    """h[i] = hash de s[:i]."""
    h = [0] * (len(s) + 1)
    acc = 0
    for i, c in enumerate(s):
        acc = (acc * BASE + ord(c)) % MOD
        h[i + 1] = acc
    return h


def conteo_por_hash(prefijos, potencias, largo):
    """Para ventanas de 'largo' dado, cuántas contraseñas distintas contienen
    cada hash."""
    p = potencias[largo]
    conteo = {}
    for h in prefijos:
        n = len(h) - 1
        if n < largo:
            continue
        # Conjunto: cada contraseña aporta como máximo 1 a cada hash.
        vistos = {(h[i + largo] - h[i] * p) % MOD for i in range(n - largo + 1)}
        for x in vistos:
            conteo[x] = conteo.get(x, 0) + 1
    return conteo


def factible(prefijos, potencias, largo, k):
    if largo == 0:
        return True
    return any(c >= k for c in conteo_por_hash(prefijos, potencias, largo).values())


def resolver(claves, k):
    prefijos = [hashes_prefijo(s) for s in claves]
    max_len = max(len(s) for s in claves)
    potencias = [1] * (max_len + 1)
    for i in range(1, max_len + 1):
        potencias[i] = potencias[i - 1] * BASE % MOD

    # Búsqueda binaria del mayor largo factible (0 siempre lo es).
    lo, hi = 0, max_len
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if factible(prefijos, potencias, mid, k):
            lo = mid
        else:
            hi = mid - 1
    if lo == 0:
        return "*"

    largo = lo
    conteo = conteo_por_hash(prefijos, potencias, largo)
    validos = {x for x, c in conteo.items() if c >= k}
    # Un texto representante por hash válido; luego el menor lexicográfico.
    representante = {}
    p = potencias[largo]
    for s, h in zip(claves, prefijos):
        for i in range(len(s) - largo + 1):
            x = (h[i + largo] - h[i] * p) % MOD
            if x in validos and x not in representante:
                representante[x] = s[i:i + largo]
    return min(representante.values())


def main():
    lineas = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(lineas):
        n, k = int(lineas[pos]), int(lineas[pos + 1])
        pos += 2
        if n == 0 and k == 0:
            break
        claves = [w.decode() for w in lineas[pos:pos + n]]
        pos += n
        salida.append(resolver(claves, k))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
