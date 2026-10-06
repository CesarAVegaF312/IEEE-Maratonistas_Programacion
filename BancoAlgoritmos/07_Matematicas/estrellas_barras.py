"""
Matemáticas — Estrellas y barras, con cotas inferiores y superiores («stars and bars»)
Nivel: Intermedio
Ejecutar: python estrellas_barras.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Contar de cuántas formas se reparten n objetos IDÉNTICOS en k cajas
    DISTINTAS, o equivalentemente cuántas soluciones enteras tiene
    x_1 + x_2 + … + x_k = n con x_i ≥ 0 (o con mínimos y máximos por caja).
    Cómo reconocerlo: «repartir n caramelos (iguales) entre k niños»,
    «cuántas soluciones enteras no negativas», «multiconjuntos de tamaño n
    sobre k tipos», «sucesiones no decrecientes de largo n con valores en
    1..k», cotas «cada uno recibe al menos a_i / a lo sumo c_i».

FUNCIÓN
    repartos(n, k) -> int                 x_1+…+x_k = n, x_i ≥ 0
    repartos_minimos(n, minimos) -> int   x_i ≥ minimos[i]
    repartos_cotas(n, minimos, maximos) -> int
        minimos[i] ≤ x_i ≤ maximos[i] (inclusión–exclusión sobre las cajas
        que se pasan; O(2^k), para k pequeño).
    repartos_tope_comun(n, k, c) -> int   0 ≤ x_i ≤ c para todas, en O(k).
    Todas devuelven 0 si no hay solución; repartos(0, 0) = 1.

IDEA Y ALGORITMO
    Biyección: un reparto (x_1, …, x_k) se escribe como n estrellas y k−1
    barras: x_1 estrellas, una barra, x_2 estrellas, una barra, … Ej. con
    n = 5, k = 3: (2,0,3) ↔ ★★||★★★. Toda fila de n estrellas y k−1 barras
    corresponde a un único reparto y viceversa, así que hay tantos repartos
    como formas de elegir qué k−1 de las n+k−1 posiciones son barras:
        repartos(n, k) = C(n + k − 1, k − 1).
    Mínimos: con y_i = x_i − a_i ≥ 0 queda Σ y_i = n − Σ a_i, es decir
        C(n − Σa_i + k − 1, k − 1)   (0 si n < Σ a_i).
    Máximos: los repartos «malos» son los que tienen alguna caja i con
    x_i ≥ c_i + 1. Para un conjunto S de cajas que se pasan, se resta c_i+1
    en cada una (cambio de variable) y queda un reparto libre. Por
    inclusión–exclusión:
        Σ_{S ⊆ cajas} (−1)^{|S|} · repartos(n − Σ_{i∈S}(c_i+1), k).
    Si todos los topes son iguales a c, el término solo depende de j = |S|:
        Σ_j (−1)^j C(k, j) C(n − j(c+1) + k − 1, k − 1).
    Desigualdad Σ x_i ≤ n: agregar una variable de holgura x_{k+1} ≥ 0
    → repartos(n, k+1) = C(n + k, k).
    El ingenuo (recorrer todas las tuplas) es exponencial en k.

MACROALGORITMO
    1. Traducir el problema a x_1 + … + x_k = n (objetos idénticos, cajas
       distintas). Si es «≤ n», agregar holgura.
    2. Restar los mínimos: n' = n − Σ a_i (si n' < 0, respuesta 0).
    3. Sin máximos: C(n' + k − 1, k − 1).
    4. Con máximos: inclusión–exclusión sobre las cajas que se pasan
       (subconjuntos, o agrupado por tamaño si el tope es común).
    5. Con módulo: binomiales con factoriales mód p (ncr_modular.py).

COMPLEJIDAD
    repartos / repartos_minimos: O(k) (un binomial). repartos_tope_comun:
    O(k) binomiales. repartos_cotas: O(2^k · k), k ≤ ~18 en 1 s.

EJEMPLO A MANO
    5 caramelos entre 3 niños: C(7, 2) = 21.
    Cada niño al menos 1: n' = 2 → C(4, 2) = 6.
    Cada niño a lo sumo 2 (n = 5, k = 3, c = 2): j=0: C(7,2) = 21;
    j=1: −3·C(4,2) = −18; j=2: +3·C(1,2) = 0 → 3 ((1,2,2),(2,1,2),(2,2,1)).

ERRORES TÍPICOS
    - Usarlo con objetos DISTINTOS (eso es k^n) o con cajas IDÉNTICAS (eso
      son particiones de enteros, otra cosa).
    - Confundir C(n+k−1, k−1) con C(n+k−1, k) (son C(n+k−1, n), no k).
    - Olvidar que el binomial con «n» negativo debe dar 0 (math.comb lanza
      error con argumentos negativos).
    - En la versión con máximos, olvidar restar c_i + 1 (no c_i).

VARIANTES Y RELACIONADOS
    - combinatoria_basica.py (multiconjuntos = combinaciones con repetición).
    - inclusion_exclusion.py (la técnica para los topes).
    - funciones_generatrices.py: el número de soluciones con cotas es el
      coeficiente de x^n en Π_i (x^{a_i} + … + x^{c_i}); útil cuando k es
      grande y los topes son distintos (DP/polinomios en O(k·n)).
    - Sucesiones no decrecientes de largo n en [1..k] = C(n + k − 1, n).

DÓNDE PRACTICAR
    - No hay problemas del repo que lo usen directamente.
    - CSES «Distributing Apples» (n manzanas entre k niños, mód 10^9+7)

VERIFICACIÓN
    - Pruebas: OK contra enumeración de todas las tuplas con
      itertools.product en 1200 casos aleatorios pequeños (k ≤ 4, n ≤ 12)
      + casos borde (python estrellas_barras.py)
"""
import itertools
import random
from math import comb


def C(n, r):
    """Binomial que devuelve 0 fuera de rango (math.comb falla con negativos)."""
    return comb(n, r) if 0 <= r <= n else 0


def repartos(n, k):
    """Soluciones de x_1+…+x_k = n con x_i ≥ 0."""
    if k == 0:
        return 1 if n == 0 else 0
    if n < 0:
        return 0
    return C(n + k - 1, k - 1)


def repartos_minimos(n, minimos):
    """Soluciones con x_i ≥ minimos[i]: cambio de variable y_i = x_i − a_i."""
    return repartos(n - sum(minimos), len(minimos))


def repartos_cotas(n, minimos, maximos):
    """Soluciones con minimos[i] ≤ x_i ≤ maximos[i] (inclusión–exclusión, O(2^k))."""
    k = len(minimos)
    n -= sum(minimos)
    topes = [maximos[i] - minimos[i] for i in range(k)]   # ahora 0 ≤ y_i ≤ topes[i]
    if any(t < 0 for t in topes):
        return 0
    total = 0
    for mask in range(1 << k):
        # S = cajas que forzamos a pasarse: y_i ≥ topes[i] + 1
        exceso = 0
        for i in range(k):
            if mask >> i & 1:
                exceso += topes[i] + 1
        signo = -1 if bin(mask).count("1") % 2 else 1
        total += signo * repartos(n - exceso, k)
    return total


def repartos_tope_comun(n, k, c):
    """Soluciones con 0 ≤ x_i ≤ c para todas las k variables, en O(k)."""
    return sum((-1) ** j * C(k, j) * repartos(n - j * (c + 1), k)
               for j in range(k + 1))


def demo():
    print("5 caramelos, 3 niños:", repartos(5, 3))                          # 21
    print("cada uno al menos 1:", repartos_minimos(5, [1, 1, 1]))           # 6
    print("cada uno a lo sumo 2:", repartos_tope_comun(5, 3, 2))            # 3
    print("1 ≤ x1 ≤ 3, 0 ≤ x2 ≤ 2, 2 ≤ x3 ≤ 4, suma 6:",
          repartos_cotas(6, [1, 0, 2], [3, 2, 4]))
    print("x1+x2+x3 ≤ 4 (holgura):", repartos(4, 4))                        # 35


def pruebas():
    random.seed(55)

    # Casos borde
    assert repartos(0, 0) == 1 and repartos(3, 0) == 0
    assert repartos(0, 5) == 1 and repartos(-1, 3) == 0
    assert repartos_minimos(2, [1, 1, 1]) == 0
    assert repartos_cotas(3, [2], [1]) == 0
    assert repartos_tope_comun(0, 0, 3) == 1

    for _ in range(1200):
        k = random.randint(0, 4)
        n = random.randint(0, 12)
        mins = [random.randint(0, 3) for _ in range(k)]
        maxs = [m + random.randint(-1, 5) for m in mins]
        tuplas = list(itertools.product(range(n + 1), repeat=k))
        assert repartos(n, k) == sum(1 for t in tuplas if sum(t) == n)
        assert repartos_minimos(n, mins) == sum(
            1 for t in tuplas if sum(t) == n and all(t[i] >= mins[i] for i in range(k)))
        assert repartos_cotas(n, mins, maxs) == sum(
            1 for t in tuplas if sum(t) == n and all(mins[i] <= t[i] <= maxs[i] for i in range(k)))
        c = random.randint(0, 5)
        assert repartos_tope_comun(n, k, c) == sum(
            1 for t in tuplas if sum(t) == n and max(t, default=0) <= c)
        # desigualdad con holgura
        assert repartos(n, k + 1) == sum(1 for t in tuplas if sum(t) <= n)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
