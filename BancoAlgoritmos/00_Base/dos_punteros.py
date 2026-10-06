"""
Base — Dos punteros («Two pointers»)
Nivel: Básico
Ejecutar: python dos_punteros.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Recorrer un arreglo con dos índices que SOLO AVANZAN, para resolver en
    O(N) problemas que a lo ingenuo serían O(N²) (probar todos los pares
    o todos los subarreglos).
    Señales en el enunciado: arreglo ordenado (o que se puede ordenar) y
    «dos elementos con suma X»; «el subarreglo más largo / más corto tal
    que…» con valores NO negativos; «cuántos pares cumplen…»; N hasta
    10^5–10^6 (O(N²) no alcanza).

FUNCIÓN
    par_con_suma(a, x) -> (i, j) | None
        a ORDENADO ascendente. Índices i < j con a[i] + a[j] == x, o None.
    contar_pares_suma_menor_igual(a, x) -> int
        a ordenado. Cantidad de pares i < j con a[i] + a[j] <= x.
    subarreglo_mas_largo(a, s) -> (largo, inicio)
        a con valores >= 0. Subarreglo contiguo más largo con suma <= s
        (largo 0, inicio 0 si ninguno; el de menor inicio en empate).

IDEA Y ALGORITMO
    Par con suma X (ordenado): i al inicio, j al final.
      - Si a[i] + a[j] < x: con este i, TODO j' ≤ j da suma aún menor, así
        que i no sirve con nadie que quede → i += 1.
      - Si a[i] + a[j] > x: con este j, todo i' ≥ i da suma mayor → j -= 1.
      - Si es igual, encontrado.
      Cada paso descarta un índice para siempre: a lo sumo N pasos.
    Subarreglo más largo con suma ≤ S (valores ≥ 0): para cada fin r, el
    mejor inicio l es el menor con suma(a[l..r]) ≤ S. Al crecer r ese l
    nunca retrocede (si a[l..r] ya se pasaba, a[l..r+1] también, porque se
    agrega un valor ≥ 0). Por eso l y r solo avanzan: O(N) en total.
    Esa MONOTONÍA es lo que hay que comprobar antes de usar la técnica: con
    valores negativos falla (agregar puede bajar la suma) y hace falta
    sumas prefijas + otra estructura.

MACROALGORITMO
    (Par con suma X)
    1. Ordenar si no lo está (guardando índices originales si se piden).
    2. i = 0, j = n − 1.
    3. Mientras i < j: comparar a[i] + a[j] con x; avanzar i o retroceder j.
    (Ventana variable)
    4. l = 0, suma = 0. Para cada r: suma += a[r].
    5. Mientras suma > S: suma -= a[l]; l += 1.
    6. Actualizar la mejor respuesta con r − l + 1.

COMPLEJIDAD
    O(N) después de ordenar (O(N log N) si hay que ordenar); memoria O(1).
    En Python, ~10^6 pasos por segundo con bucles while simples.

EJEMPLO A MANO
    a = [1, 2, 4, 7, 11, 15], x = 15
      i=0 j=5: 1+15=16 > 15 → j=4
      i=0 j=4: 1+11=12 < 15 → i=1
      i=1 j=4: 2+11=13 < 15 → i=2
      i=2 j=4: 4+11=15 ✓   → (2, 4)
    a = [2, 1, 3, 4, 1, 1], S = 6:
      r=0..2: suma 6 (l=0) → largo 3;  r=3: suma 10 → saca 2, 1 → l=2, suma 7
      → saca 3 → l=3, suma 4; r=4,5: suma 6 → [4,1,1], largo 3 (empata, se
      queda el primero: inicio 0).

ERRORES TÍPICOS
    - Usarlo con valores negativos en la ventana variable (la monotonía falla).
    - Olvidar ordenar antes del par con suma (y perder los índices originales).
    - Usar while i <= j: permite usar el mismo elemento dos veces.
    - Contar pares: cuando a[i] + a[j] ≤ x, son j − i pares de golpe
      (i con i+1..j), no uno solo.

VARIANTES Y RELACIONADOS
    - Tres elementos con suma X: fijar uno y dos punteros sobre el resto, O(N²).
    - Fusionar dos listas ordenadas; intersección de listas ordenadas.
    - Subarreglo más corto con suma ≥ S, más largo con ≤ K distintos:
      ventana_deslizante.py.
    - Con valores negativos: sumas_prefijas.py + diccionario
      (conteo_diccionarios.py).
    - Meet in the middle usa dos punteros sobre las dos mitades ordenadas
      (01_BusquedaCompleta/meet_in_the_middle.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/H - Ghost Hunting (envolvente convexa + dos punteros)
    - CSES «Sum of Two Values», «Apartments», «Ferris Wheel»
    - Codeforces 279B «Books» (subarreglo más largo con suma ≤ t)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todos los pares / todos los
      subarreglos) en 3000 casos aleatorios + casos borde
      (python dos_punteros.py)
"""
import random


def par_con_suma(a, x):
    """(i, j), i < j, con a[i] + a[j] == x en a ordenado; None si no hay."""
    i, j = 0, len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == x:
            return i, j
        if s < x:
            i += 1          # a[i] es muy pequeño incluso con el mayor que queda
        else:
            j -= 1          # a[j] es muy grande incluso con el menor que queda
    return None


def contar_pares_suma_menor_igual(a, x):
    """Cantidad de pares i < j con a[i] + a[j] <= x, con a ordenado."""
    i, j = 0, len(a) - 1
    total = 0
    while i < j:
        if a[i] + a[j] <= x:
            total += j - i  # a[i] sirve con todos los de i+1..j
            i += 1
        else:
            j -= 1          # a[j] no sirve ni con el menor que queda
    return total


def subarreglo_mas_largo(a, s):
    """(largo, inicio) del subarreglo más largo con suma <= s; a con valores >= 0."""
    mejor, inicio = 0, 0
    l = 0
    suma = 0                # invariante: suma == a[l] + ... + a[r]
    for r, v in enumerate(a):
        suma += v
        while suma > s and l <= r:
            suma -= a[l]    # el inicio l ya no sirve para este r ni los siguientes
            l += 1
        if r - l + 1 > mejor:
            mejor, inicio = r - l + 1, l
    return mejor, inicio


def demo():
    a = [1, 2, 4, 7, 11, 15]
    print("a =", a)
    print("par_con_suma(a, 15) =", par_con_suma(a, 15))                     # (2, 4)
    print("pares con suma <= 9:", contar_pares_suma_menor_igual(a, 9))      # 5
    b = [2, 1, 3, 4, 1, 1]
    print("subarreglo_mas_largo(", b, ", 6) =", subarreglo_mas_largo(b, 6))  # (3, 0)


def pruebas():
    random.seed(99)

    # Casos borde
    assert par_con_suma([], 3) is None
    assert par_con_suma([3], 6) is None             # no se puede usar dos veces
    assert par_con_suma([3, 3], 6) == (0, 1)
    assert contar_pares_suma_menor_igual([], 0) == 0
    assert contar_pares_suma_menor_igual([1, 1, 1, 1], 2) == 6
    assert subarreglo_mas_largo([], 5) == (0, 0)
    assert subarreglo_mas_largo([7, 8], 5) == (0, 0)
    assert subarreglo_mas_largo([0, 0, 0], 0) == (3, 0)

    for _ in range(3000):
        n = random.randint(0, 15)
        a = sorted(random.randint(-10, 10) for _ in range(n))
        x = random.randint(-22, 22)
        pares = [(i, j) for i in range(n) for j in range(i + 1, n) if a[i] + a[j] == x]
        r = par_con_suma(a, x)
        if pares:
            assert r is not None and a[r[0]] + a[r[1]] == x and r[0] < r[1]
        else:
            assert r is None
        bruta = sum(1 for i in range(n) for j in range(i + 1, n) if a[i] + a[j] <= x)
        assert contar_pares_suma_menor_igual(a, x) == bruta

        b = [random.randint(0, 6) for _ in range(n)]
        s = random.randint(0, 15)
        mejor, inicio = 0, 0
        for l in range(n):
            for rr in range(l, n):
                if sum(b[l:rr + 1]) <= s and rr - l + 1 > mejor:
                    mejor, inicio = rr - l + 1, l
        assert subarreglo_mas_largo(b, s) == (mejor, inicio)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
