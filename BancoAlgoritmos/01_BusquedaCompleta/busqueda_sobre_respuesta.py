"""
Búsqueda completa — Búsqueda binaria sobre la respuesta («Binary search the answer»)
Nivel: Intermedio
Ejecutar: python busqueda_sobre_respuesta.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Convertir un problema de OPTIMIZACIÓN («el mínimo T tal que…») en
    muchas preguntas de DECISIÓN («¿se puede con T?»), cuando la decisión es
    fácil de responder y MONÓTONA: si se puede con T, también con T + 1.
    Entonces se busca binariamente el menor T que funciona.
    Señales en el enunciado: «minimizar el máximo», «maximizar el mínimo»,
    «el menor tiempo / la menor capacidad para que…», respuesta numérica en
    un rango enorme (hasta 10^18) y una comprobación voraz en O(N).

FUNCIÓN
    primer_verdadero(lo, hi, cond) -> int
        Menor x en [lo, hi) con cond(x) verdadero; hi si ninguno (cond monótona).
    min_max_particion(a, k) -> int
        a de enteros ≥ 0, 1 ≤ k. Partir a en a lo sumo k tramos CONTIGUOS
        (no vacíos) minimizando la mayor suma de un tramo. (UVa 11413,
        CSES «Array Division»; usar ≤ k tramos o exactamente k da lo mismo
        si k ≤ n, porque partir un tramo nunca sube el máximo.)
    tiempo_maquinas(t, productos) -> int
        t[i] = tiempo que tarda la máquina i en hacer un producto; todas
        trabajan en paralelo. Menor tiempo para fabricar 'productos'
        unidades (CSES «Factory Machines»).

IDEA Y ALGORITMO
    Partición: «¿se puede con capacidad C?» (cada tramo suma ≤ C) se
    responde con un VORAZ: llenar cada tramo lo más posible y abrir uno
    nuevo cuando el siguiente número no cabe. Llenar al máximo nunca
    perjudica: cualquier partición válida puede «correr» sus cortes hacia
    la derecha hasta coincidir con los del voraz sin pasarse de C, así que
    si alguna usa ≤ k tramos, el voraz también. Monotonía: con C mayor,
    los mismos cortes siguen sirviendo. Rango: C ∈ [max(a), sum(a)].
    Máquinas: en tiempo T la máquina i hace T // t[i] productos; el total
    Σ T // t[i] crece con T. Rango: T ∈ [0, min(t) · productos] (la
    máquina más rápida sola ya alcanza en ese tiempo).
    En los dos casos: búsqueda binaria del primer T con cond(T) verdadero.
    Probar todos los T uno por uno sería O(rango · N) (rango hasta 10^18).

MACROALGORITMO
    1. Identificar la respuesta T y escribir cond(T): «¿se puede con T?».
    2. Comprobar que cond es monótona (F F … F V V … V).
    3. Elegir lo (seguro falso o el mínimo posible) y hi (seguro verdadero).
    4. Implementar cond en O(N) (normalmente un voraz o un conteo).
    5. Búsqueda binaria: m = (lo + hi) // 2; si cond(m): hi = m; si no: lo = m + 1.
    6. La respuesta es lo.

COMPLEJIDAD
    O(N · log(rango)): con N = 2·10^5 y rango 10^18 son ~60 pasadas de
    O(N) → ~10^7 operaciones, ~1–2 s en Python (usar bucles simples o
    sum(map(...)) en C).

EJEMPLO A MANO
    a = [2, 4, 7, 3, 5], k = 3. Rango [7, 21].
      C = 14: [2,4,7] [3,5]         → 2 tramos ✓  hi = 14
      C = 10: [2,4] [7,3] [5]       → 3 ✓         hi = 10
      C = 8:  [2,4] [7] [3,5]       → 3 ✓         hi = 8
      C = 7:  [2,4] [7] [3] [5]     → 4 ✗         lo = 8
    → 8
    t = [3, 2, 5], productos = 7:  T = 8: 2 + 4 + 1 = 7 ✓;  T = 7: 2 + 3 + 1 = 6 ✗  → 8

ERRORES TÍPICOS
    - Elegir hi demasiado pequeño (no siempre verdadero) o lo demasiado grande.
    - En la partición, olvidar que un solo elemento mayor que C hace
      imposible cualquier partición (por eso lo = max(a)).
    - cond no monótona: la binaria da cualquier cosa. Pensar el argumento.
    - Bucle infinito por lo = m en vez de lo = m + 1.
    - Sobre reales: iterar un número fijo de veces (60–100) en vez de epsilon.
    - Hacer cond en O(N log N) o peor sin necesidad cuando el límite es justo.

VARIANTES Y RELACIONADOS
    - «Maximizar el mínimo» (vacas agresivas, distancia mínima máxima):
      buscar el ÚLTIMO verdadero = primer_verdadero(cond negada) − 1.
    - Respuesta real (tiempo, distancia): binaria con 100 iteraciones.
    - Binaria sobre la respuesta + otro algoritmo como cond (BFS, flujo,
      2-SAT) es muy frecuente en maratón.
    - Relacionados: 00_Base/busqueda_binaria.py, 00_Base/busqueda_ternaria.py.

DÓNDE PRACTICAR
    - 2025-2/maraton_problemas/p11413_fill_containers.py (UVa 11413 «Fill the Containers»)
    - CSES «Array Division», «Factory Machines»
    - Codeforces 760B «Frodo and pillows»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (partición: todas las formas de poner
      cortes con itertools.combinations; máquinas: avanzar T de uno en uno)
      en 2000 casos aleatorios + casos borde + un caso grande de 10^18
      (python busqueda_sobre_respuesta.py)
"""
import itertools
import random


def primer_verdadero(lo, hi, cond):
    """Menor x en [lo, hi) con cond(x) verdadero; hi si ninguno (cond monótona)."""
    while lo < hi:
        m = (lo + hi) // 2
        if cond(m):
            hi = m
        else:
            lo = m + 1
    return lo


def min_max_particion(a, k):
    """Menor C tal que a se parte en <= k tramos contiguos con suma <= C cada uno."""
    if not a:
        return 0

    def se_puede(c):
        # voraz: llenar cada tramo al máximo antes de abrir el siguiente
        tramos, actual = 1, 0
        for x in a:
            if actual + x <= c:
                actual += x
            else:
                tramos += 1
                actual = x
                if tramos > k:
                    return False
        return True

    # lo = max(a): con menos ni un elemento cabe; hi = sum(a): siempre se puede
    return primer_verdadero(max(a), sum(a), se_puede)


def tiempo_maquinas(t, productos):
    """Menor tiempo T con sum(T // ti) >= productos."""
    def alcanza(T):
        return sum(T // ti for ti in t) >= productos
    # hi = min(t) * productos siempre alcanza; el rango es [0, hi] -> buscar en [0, hi)
    hi = min(t) * productos
    return primer_verdadero(0, hi, alcanza)


def demo():
    a = [2, 4, 7, 3, 5]
    print("min_max_particion(", a, ", 3) =", min_max_particion(a, 3))     # 8
    print("tiempo_maquinas([3, 2, 5], 7) =", tiempo_maquinas([3, 2, 5], 7))  # 8
    print("UVa 11413 ejemplo: [1..5] en 3 contenedores →", min_max_particion([1, 2, 3, 4, 5], 3))  # 6


def _particion_bruta(a, k):
    n = len(a)
    mejor = None
    for partes in range(1, min(k, n) + 1):
        for cortes in itertools.combinations(range(1, n), partes - 1):
            bordes = (0,) + cortes + (n,)
            mx = max(sum(a[bordes[i]:bordes[i + 1]]) for i in range(partes))
            if mejor is None or mx < mejor:
                mejor = mx
    return mejor


def pruebas():
    random.seed(11413)

    # Casos borde y ejemplos
    assert min_max_particion([], 3) == 0
    assert min_max_particion([5], 1) == 5
    assert min_max_particion([0, 0, 0], 2) == 0
    assert min_max_particion([1, 2, 3, 4, 5], 3) == 6        # ejemplo de UVa 11413
    assert min_max_particion([4, 78, 9], 2) == 82            # (pequeño caso a mano)
    assert tiempo_maquinas([3, 2, 5], 7) == 8               # ejemplo de CSES
    assert tiempo_maquinas([1], 1) == 1
    assert tiempo_maquinas([10**9], 10**9) == 10**18         # rango enorme sin problema

    for _ in range(2000):
        n = random.randint(1, 9)
        a = [random.randint(0, 20) for _ in range(n)]
        k = random.randint(1, n + 2)
        assert min_max_particion(a, k) == _particion_bruta(a, k)

        t = [random.randint(1, 8) for _ in range(random.randint(1, 4))]
        p = random.randint(1, 15)
        T = 0
        while sum(T // ti for ti in t) < p:
            T += 1                                           # fuerza bruta: avanzar de a uno
        assert tiempo_maquinas(t, p) == T


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
