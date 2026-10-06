"""
Base — Búsqueda binaria («Binary search»)
Nivel: Básico
Ejecutar: python busqueda_binaria.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar en O(log N) la primera posición donde una condición pasa de
    falso a verdadero: en un arreglo ordenado («¿cuántos valores son ≤ x?»,
    «¿dónde insertar x?») o sobre un rango de números («búsqueda binaria
    sobre la respuesta»).
    Señales en el enunciado: arreglo ordenado + muchas consultas; «el mínimo
    valor tal que…» / «el máximo valor tal que…» cuando, si X sirve, todo lo
    mayor (o menor) también sirve.

FUNCIÓN
    primer_verdadero(lo, hi, cond) -> int
        Menor x en [lo, hi) con cond(x) verdadero; hi si ninguno lo cumple.
        Exige que cond sea MONÓTONA: F F F … F V V … V.
    cota_inferior(a, x) -> int    primer índice i con a[i] >= x  (= bisect_left)
    cota_superior(a, x) -> int    primer índice i con a[i] >  x  (= bisect_right)

IDEA Y ALGORITMO
    Si la condición es monótona, basta mirar el punto medio m del rango que
    queda: si cond(m) es verdadera, la respuesta está en m o a su izquierda;
    si es falsa, está estrictamente a la derecha. Cada paso descarta la mitad
    del rango, así que en ⌈log2(N)⌉ pasos queda un solo candidato.
    Invariante del código: todo x < lo es FALSO y todo x ≥ hi es VERDADERO
    (o está fuera del rango). Cuando lo == hi, ese es el primer verdadero.
    Escribirla siempre como «primer verdadero» evita los errores de ±1: el
    resto de búsquedas (último falso, cota inferior/superior, búsqueda sobre
    la respuesta) se obtienen eligiendo bien la condición.
    El ingenuo (recorrer de izquierda a derecha) es O(N) por consulta: con
    N = Q = 10^5 son 10^10 operaciones; la binaria baja a ~1,7·10^6.

MACROALGORITMO
    1. Fijar el rango [lo, hi) donde puede estar la respuesta.
    2. Mientras lo < hi: m = (lo + hi) // 2.
    3. Si cond(m) es verdadera: hi = m (m es candidato, seguir a la izquierda).
    4. Si no: lo = m + 1 (m no sirve, ni nada a su izquierda).
    5. Devolver lo.

COMPLEJIDAD
    O(log N) evaluaciones de cond; memoria O(1).
    En Python, 10^5–10^6 consultas por segundo con bisect (está en C).

EJEMPLO A MANO
    a = [1, 3, 3, 5, 8, 13], cota_inferior(a, 4) (cond: a[i] >= 4):
      lo=0 hi=6 → m=3: a[3]=5 >= 4 V → hi=3
      lo=0 hi=3 → m=1: a[1]=3 >= 4 F → lo=2
      lo=2 hi=3 → m=2: a[2]=3 >= 4 F → lo=3     → respuesta 3 (a[3] = 5)

ERRORES TÍPICOS
    - Usar lo = m en vez de lo = m + 1: ciclo infinito cuando hi = lo + 1.
    - Aplicarla con una condición que NO es monótona (o arreglo sin ordenar).
    - En búsqueda sobre la respuesta, olvidar que hi debe ser un valor que
      seguro sirve (o hi + 1 si se quiere detectar «no hay solución»).
    - Búsqueda sobre reales: iterar un número fijo de veces (60–100) en vez
      de comparar con epsilon.

VARIANTES Y RELACIONADOS
    - Último falso = primer_verdadero(...) - 1.
    - Contar valores en [x, y]: cota_superior(a, y) - cota_inferior(a, x).
    - Búsqueda binaria sobre reales: for _ in range(100) con m = (lo+hi)/2.
    - Búsqueda ternaria (funciones unimodales).
    - En Python, para arreglos usar bisect.bisect_left / bisect_right.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/I - License Plates (voraz + búsqueda binaria)
    - ICPC/Colombia 2023/F - Finding Common Passwords (binaria + hashing)
    - ICPC/OMP 2017 Murcia/B - Pool Filling (sumas prefijas + binaria)
    - Codeforces 706B «Interesting Drink»; CSES «Factory Machines»,
      «Array Division» (búsqueda sobre la respuesta)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (recorrido lineal) y contra bisect en
      2000 casos aleatorios + casos borde (python busqueda_binaria.py)
"""
import bisect
import random


def primer_verdadero(lo, hi, cond):
    """Menor x en [lo, hi) con cond(x) verdadero; hi si ninguno.

    Invariante: todo x < lo es falso, todo x >= hi es verdadero (o no existe).
    """
    while lo < hi:
        m = (lo + hi) // 2
        if cond(m):
            hi = m          # m sirve: la respuesta es m o algo a su izquierda
        else:
            lo = m + 1      # m no sirve: por monotonía, nada <= m sirve
    return lo


def cota_inferior(a, x):
    """Primer índice i con a[i] >= x (len(a) si no hay). Igual a bisect_left."""
    return primer_verdadero(0, len(a), lambda i: a[i] >= x)


def cota_superior(a, x):
    """Primer índice i con a[i] > x (len(a) si no hay). Igual a bisect_right."""
    return primer_verdadero(0, len(a), lambda i: a[i] > x)


def raiz_entera(n):
    """Ejemplo de búsqueda sobre la respuesta: mayor r con r*r <= n.

    cond(r) = r*r > n es monótona; el primer r que la cumple, menos 1, es la raíz.
    """
    return primer_verdadero(0, n + 2, lambda r: r * r > n) - 1


def demo():
    a = [1, 3, 3, 5, 8, 13]
    print("a =", a)
    print("cota_inferior(a, 4) =", cota_inferior(a, 4))   # 3
    print("cota_superior(a, 3) =", cota_superior(a, 3))   # 3
    print("cuántos en [3, 8]:", cota_superior(a, 8) - cota_inferior(a, 3))  # 4
    print("raiz_entera(50) =", raiz_entera(50))           # 7


def pruebas():
    random.seed(12345)

    # Casos borde
    assert cota_inferior([], 5) == 0
    assert cota_superior([], 5) == 0
    assert cota_inferior([7], 7) == 0 and cota_superior([7], 7) == 1
    assert cota_inferior([2, 2, 2], 2) == 0 and cota_superior([2, 2, 2], 2) == 3
    assert primer_verdadero(0, 10, lambda x: False) == 10
    assert primer_verdadero(0, 10, lambda x: True) == 0

    # Aleatorios contra fuerza bruta lineal y contra bisect
    for _ in range(2000):
        n = random.randint(0, 30)
        a = sorted(random.randint(-10, 10) for _ in range(n))
        x = random.randint(-12, 12)
        lineal_inf = next((i for i in range(n) if a[i] >= x), n)
        lineal_sup = next((i for i in range(n) if a[i] > x), n)
        assert cota_inferior(a, x) == lineal_inf == bisect.bisect_left(a, x)
        assert cota_superior(a, x) == lineal_sup == bisect.bisect_right(a, x)

    # Búsqueda sobre la respuesta
    for n in list(range(0, 2000)) + [10**18, 10**18 - 1]:
        r = raiz_entera(n)
        assert r * r <= n < (r + 1) * (r + 1)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
