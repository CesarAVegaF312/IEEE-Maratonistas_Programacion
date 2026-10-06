"""
Base — Conteo con diccionarios («Hash maps: frequency, first occurrence, grouping»)
Nivel: Básico
Ejecutar: python conteo_diccionarios.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Contar cuántas veces aparece cada valor, recordar DÓNDE apareció por
    primera vez algo, o agrupar elementos por una clave, todo en O(1) por
    operación (en promedio). Convierte muchas búsquedas O(N²) en O(N).
    Señales en el enunciado: «cuántas veces…», «el más frecuente»,
    «¿apareció antes?», «agrupar los que tienen la misma…», valores
    grandes (hasta 10^9) que no sirven como índice de un arreglo, «el
    subarreglo más largo con suma 0 / igual cantidad de A y B».

FUNCIÓN
    mas_frecuente(a) -> (valor, veces)
        Valor más frecuente; en empate, el MENOR valor. a no vacío.
    mas_largo_suma_cero(a) -> int
        Largo del subarreglo contiguo más largo con suma 0 (0 si no hay).
    contar_subarreglos_suma(a, k) -> int
        Cantidad de subarreglos contiguos con suma exactamente k.
    agrupar_anagramas(palabras) -> list[list[str]]
        Grupos de palabras con las mismas letras, en orden de primera
        aparición del grupo y de las palabras dentro del grupo.

IDEA Y ALGORITMO
    Frecuencias: d[x] = d.get(x, 0) + 1, o collections.Counter(a), que
    hace lo mismo en C. Para el desempate, una clave compuesta
    (-veces, valor) y min.
    Primera aparición + sumas prefijas: con S[i] = a[0] + … + a[i-1], el
    subarreglo a[l..r-1] suma 0  <=>  S[r] == S[l]. Para cada r, el l más
    pequeño con S[l] == S[r] es la PRIMERA aparición de ese valor de S, así
    que basta un diccionario valor → primer índice (con S[0] = 0 en 0).
    Contar subarreglos con suma k: a[l..r-1] suma k  <=>  S[l] == S[r] − k.
    Al llegar a r, se suman cuántas veces se vio S[r] − k antes (un Counter
    de sumas prefijas ya vistas). Funciona con NEGATIVOS, a diferencia de
    dos punteros.
    Agrupar: la clave canónica de una palabra es su lista de letras
    ordenada; dos palabras son anagramas  <=>  tienen la misma clave.
    defaultdict(list) agrupa sin preguntar «¿ya existe?». Desde Python 3.7
    los dict conservan el orden de inserción.

MACROALGORITMO
    1. Elegir la CLAVE (el valor, una suma prefija, una forma canónica).
    2. Elegir lo que se guarda por clave (cuenta, primer índice, lista).
    3. Recorrer una vez: consultar el diccionario ANTES o DESPUÉS de
       insertar el elemento actual, según el problema.
    4. Actualizar la respuesta con lo consultado.
    5. Insertar/actualizar la clave actual.

COMPLEJIDAD
    O(N) en promedio (cada operación de dict es O(1) esperado); memoria
    O(#claves distintas). Counter sobre 10^6 enteros en ~0,1 s.

EJEMPLO A MANO
    a = [1, -1, 3, 2, -2, -3, 4]
    S = [0, 1, 0, 3, 5, 3, 0, 4]   primera[0]=0, primera[1]=1, primera[3]=3, …
      r=2: S=0, primera[0]=0 → largo 2   ([1, -1])
      r=6: S=0, primera[0]=0 → largo 6   ([1, -1, 3, 2, -2, -3])
    → mas_largo_suma_cero = 6

ERRORES TÍPICOS
    - Olvidar la suma prefija 0 en la posición 0 (pierde subarreglos que
      empiezan en el índice 0).
    - En «primera aparición», sobrescribir el índice cada vez (queda la
      ÚLTIMA aparición y el subarreglo sale más corto).
    - Contar el elemento actual consigo mismo por insertar antes de consultar.
    - Usar una lista como clave (no es hashable): convertir a tupla o str.
    - Iterar un Counter esperando orden por frecuencia: usar most_common().

VARIANTES Y RELACIONADOS
    - Más largo con igual número de A y B: convertir a +1/−1 y suma 0.
    - Pares con a[i] + a[j] = X: para cada j, sumar cuenta[X − a[j]].
    - Comprimir coordenadas: {v: i for i, v in enumerate(sorted(set(a)))}.
    - set para «¿ya lo vi?»; defaultdict(int) / Counter para contar.
    - Relacionados: sumas_prefijas.py, 01_BusquedaCompleta/meet_in_the_middle.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/A - Account Qualifying (sumas prefijas + primera aparición)
    - ICPC/Colombia 2026/D - Bingwhenever (diccionario valor → turno)
    - ICPC/Colombia 2017/C - Compact Terms (diccionario (nombre, hijos) → id)
    - CSES «Distinct Numbers», «Subarray Sums II»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (count() por valor, todos los
      subarreglos, comparación de pares con sorted) en 3000 casos aleatorios
      + casos borde (python conteo_diccionarios.py)
"""
import random
from collections import Counter, defaultdict


def mas_frecuente(a):
    """(valor, veces) del más frecuente; en empate, el menor valor."""
    c = Counter(a)
    valor = min(c, key=lambda v: (-c[v], v))   # más veces primero, luego menor valor
    return valor, c[valor]


def mas_largo_suma_cero(a):
    """Largo del subarreglo contiguo más largo con suma 0."""
    primera = {0: 0}            # suma prefija -> primer índice donde apareció
    s = 0
    mejor = 0
    for r, v in enumerate(a, 1):
        s += v                  # s = S[r]
        if s in primera:
            mejor = max(mejor, r - primera[s])
        else:
            primera[s] = r      # solo la PRIMERA vez: da el subarreglo más largo
    return mejor


def contar_subarreglos_suma(a, k):
    """Cantidad de subarreglos contiguos con suma exactamente k."""
    vistas = Counter({0: 1})    # sumas prefijas S[0..r-1] ya vistas
    s = 0
    total = 0
    for v in a:
        s += v
        total += vistas[s - k]  # cada S[l] == S[r] - k da un subarreglo
        vistas[s] += 1          # insertar DESPUÉS de consultar
    return total


def agrupar_anagramas(palabras):
    """Grupos de anagramas en orden de primera aparición."""
    grupos = defaultdict(list)  # clave canónica -> palabras
    for w in palabras:
        grupos["".join(sorted(w))].append(w)
    return list(grupos.values())


def demo():
    a = [1, -1, 3, 2, -2, -3, 4]
    print("a =", a)
    print("mas_frecuente([4, 1, 4, 1, 7]) =", mas_frecuente([4, 1, 4, 1, 7]))   # (1, 2)
    print("mas_largo_suma_cero(a) =", mas_largo_suma_cero(a))                  # 6
    print("contar_subarreglos_suma(a, 3) =", contar_subarreglos_suma(a, 3))
    print("anagramas:", agrupar_anagramas(["amor", "roma", "sol", "mora", "los", "a"]))


def pruebas():
    random.seed(5)

    # Casos borde
    assert mas_frecuente([7]) == (7, 1)
    assert mas_frecuente([2, 2, 1, 1]) == (1, 2)
    assert mas_largo_suma_cero([]) == 0
    assert mas_largo_suma_cero([0]) == 1
    assert mas_largo_suma_cero([5]) == 0
    assert contar_subarreglos_suma([], 0) == 0
    assert contar_subarreglos_suma([0, 0, 0], 0) == 6
    assert agrupar_anagramas([]) == []

    for _ in range(3000):
        n = random.randint(1, 15)
        a = [random.randint(-4, 4) for _ in range(n)]
        mejor = max(a.count(v) for v in a)
        assert mas_frecuente(a) == (min(v for v in a if a.count(v) == mejor), mejor)

        bruta = 0
        for l in range(n):
            for r in range(l, n):
                if sum(a[l:r + 1]) == 0:
                    bruta = max(bruta, r - l + 1)
        assert mas_largo_suma_cero(a) == bruta

        k = random.randint(-6, 6)
        assert contar_subarreglos_suma(a, k) == sum(
            1 for l in range(n) for r in range(l, n) if sum(a[l:r + 1]) == k)

        ws = ["".join(random.choice("abc") for _ in range(random.randint(1, 3)))
              for _ in range(random.randint(0, 8))]
        g = agrupar_anagramas(ws)
        assert sorted(w for grupo in g for w in grupo) == sorted(ws)
        for grupo in g:                       # dentro: todos anagramas, en orden de entrada
            assert all(sorted(w) == sorted(grupo[0]) for w in grupo)
            assert grupo == [w for w in ws if sorted(w) == sorted(grupo[0])]
        for g1 in range(len(g)):              # entre grupos: ninguno es anagrama de otro
            for g2 in range(g1 + 1, len(g)):
                assert sorted(g[g1][0]) != sorted(g[g2][0])


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
