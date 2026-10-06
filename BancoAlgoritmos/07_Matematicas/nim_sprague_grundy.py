"""
Matemáticas — Nim y teorema de Sprague–Grundy (números de Grundy, suma de juegos)
Nivel: Intermedio/Avanzado
Ejecutar: python nim_sprague_grundy.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir quién gana un juego IMPARCIAL (las mismas jugadas para ambos
    jugadores, información completa, sin azar, pierde quien no puede
    jugar) cuando el juego es la SUMA de varios juegos independientes: en
    cada turno se elige uno de los subjuegos y se juega en él.
    Cómo reconocerlo: «dos jugadores juegan óptimamente, alternan turnos,
    pierde el que no pueda mover», varias pilas/tableros/fichas que no
    interactúan; «¿quién gana?» o «¿cuál es la primera jugada ganadora?».

FUNCIÓN
    gana_nim(pilas) -> bool              True si gana el primer jugador (XOR ≠ 0)
    jugada_nim(pilas) -> (i, nuevo) | None
        Una jugada ganadora: dejar la pila i con «nuevo» piedras; None si
        la posición es perdedora.
    mex(conjunto) -> int                 menor entero ≥ 0 que no está
    grundy_sustraccion(N, movs) -> list  g[0..N] del juego «quitar m ∈ movs
                                         piedras de una pila»
    grundy_division(N) -> list           juego de Grundy: partir una pila en
                                         dos pilas de tamaños DISTINTOS
    gana_suma(grundys) -> bool           XOR de los Grundy de los subjuegos ≠ 0

IDEA Y ALGORITMO
    Nim (teorema de Bouton): con pilas a_1..a_n, el que mueve PIERDE ⇔
    a_1 ⊕ … ⊕ a_n = 0. Prueba: (1) desde X = 0, cambiar una sola pila
    cambia el XOR, así que toda jugada deja X ≠ 0. (2) Desde X ≠ 0, sea b el
    bit más alto de X; alguna pila a_i tiene ese bit, y a_i ⊕ X < a_i (se
    apaga el bit b y solo cambian bits menores), así que dejar a_i ⊕ X es
    legal y deja XOR 0. (3) La posición final (todo 0) tiene X = 0 y el que
    mueve pierde. Por inducción, las posiciones con X = 0 son perdedoras.
    Sprague–Grundy: toda posición P de un juego imparcial equivale a una
    pila de Nim de tamaño g(P) = mex{ g(Q) : Q sucesor de P }. Por qué: desde
    P se puede ir a posiciones de cualquier valor 0..g(P)−1 (como en una pila
    de Nim) y nunca a una de valor g(P); si el rival sube a un valor mayor,
    se puede volver a g(P) (por definición de mex en esa posición), lo que
    no cambia el resultado. Así, la suma de juegos se comporta como Nim con
    pilas g(P_i): el primero gana ⇔ g(P_1) ⊕ … ⊕ g(P_n) ≠ 0. Además una
    posición es perdedora ⇔ g = 0.
    Cuando una jugada parte un juego en dos (juego de Grundy), el sucesor es
    una SUMA y su valor es el XOR de las partes.

MACROALGORITMO
    1. Separar el juego en subjuegos independientes.
    2. Para cada tipo de subjuego, calcular g por DP en orden de tamaño:
       g(P) = mex de los g de sus sucesores (XOR si un sucesor es una suma).
    3. Si N es grande, imprimir g(0..100) y buscar un patrón/periodo.
    4. Respuesta: XOR de los g de los subjuegos; ≠ 0 → gana el primero.
    5. Jugada ganadora: buscar un subjuego i y un sucesor Q con
       g(Q) = g(P_i) ⊕ X (en Nim: dejar la pila en a_i ⊕ X).

COMPLEJIDAD
    Nim: O(n). Grundy por DP: O(N · jugadas por posición); juego de Grundy
    O(N²) (N ≈ 3000 en ~1 s en Python). Los g son ≤ número de jugadas.

EJEMPLO A MANO
    Pilas (3, 4, 5): 3 ⊕ 4 ⊕ 5 = 011 ⊕ 100 ⊕ 101 = 010 = 2 ≠ 0 → gana el
    primero. Bit más alto de 2 es el 1; la pila 3 (011) lo tiene: 3 ⊕ 2 = 1,
    dejar la pila 0 en 1 → (1, 4, 5), XOR 0.
    Sustracción con movs {1, 3, 4}: g = 0 1 0 1 2 3 2 0 1 0 1 2 3 2 … (periodo 7).

ERRORES TÍPICOS
    - Sumar en vez de hacer XOR de los Grundy.
    - Aplicarlo a juegos PARTISANOS (cada jugador con jugadas propias, como
      el ajedrez) o con empate: Sprague–Grundy no sirve ahí.
    - Nim «misère» (pierde quien toma la última): la regla cambia cuando
      todas las pilas son ≤ 1 (ahí gana el primero ⇔ hay un número PAR de
      pilas de 1); si alguna pila es > 1, la regla es la normal.
    - Calcular el mex con un conjunto que incluye valores de posiciones
      inválidas (p. ej. pila negativa).
    - Olvidar que el sucesor que parte en dos tiene valor XOR, no mex.

VARIANTES Y RELACIONADOS
    - posiciones_ganadoras.py (DP ganar/perder cuando no hay suma de juegos).
    - Nim en escalera («staircase nim»): solo cuentan las pilas en
      escalones impares (XOR de ellas).
    - Nim con a lo sumo k pilas por jugada (Moore): sumar bits mód k+1.
    - trucos_bits.py (propiedades del XOR).

DÓNDE PRACTICAR
    - No hay problemas del repo que lo usen.
    - CSES «Nim Game I», «Nim Game II» (sustracción {1,2,3} → pilas mód 4),
      «Stair Game», «Grundy's Game», «Stick Game»

VERIFICACIÓN
    - Pruebas: OK contra búsqueda exhaustiva del árbol de juego (minimax
      con memo sobre la tupla completa de pilas) en todas las posiciones de
      Nim con ≤ 3 pilas de ≤ 6, sumas de juegos de sustracción y del juego
      de Grundy (400 casos); jugada_nim deja siempre XOR 0
      (python nim_sprague_grundy.py)
"""
import random
from functools import lru_cache
from itertools import product


def gana_nim(pilas):
    """True si el primer jugador gana Nim normal (XOR de las pilas ≠ 0)."""
    x = 0
    for a in pilas:
        x ^= a
    return x != 0


def jugada_nim(pilas):
    """(i, nuevo) que deja XOR 0, o None si la posición es perdedora."""
    x = 0
    for a in pilas:
        x ^= a
    if x == 0:
        return None
    for i, a in enumerate(pilas):
        if a ^ x < a:              # la pila tiene el bit más alto de x
            return i, a ^ x
    return None                    # inalcanzable


def mex(valores):
    """Mínimo entero no negativo que no está en valores."""
    s = set(valores)
    m = 0
    while m in s:
        m += 1
    return m


def grundy_sustraccion(N, movs):
    """g[n] del juego: de una pila de n se pueden quitar m ∈ movs piedras."""
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        g[n] = mex(g[n - m] for m in movs if m <= n)
    return g


def grundy_division(N):
    """Juego de Grundy: partir una pila en dos pilas no vacías de tamaños distintos."""
    g = [0] * (N + 1)
    for n in range(3, N + 1):
        # el sucesor es la SUMA de dos pilas: su valor es el XOR
        g[n] = mex(g[a] ^ g[n - a] for a in range(1, (n + 1) // 2) if a != n - a)
    return g


def gana_suma(grundys):
    """El primero gana la suma de juegos ⇔ XOR de los Grundy ≠ 0."""
    x = 0
    for v in grundys:
        x ^= v
    return x != 0


def demo():
    print("Nim (3,4,5): gana el primero?", gana_nim([3, 4, 5]), "jugada:", jugada_nim([3, 4, 5]))
    print("Grundy sustracción {1,3,4}, n=0..13:", grundy_sustraccion(13, [1, 3, 4]))
    print("Juego de Grundy (dividir), n=0..12:", grundy_division(12))
    g = grundy_sustraccion(20, [1, 3, 4])
    print("pilas 5, 9, 13 con {1,3,4}: gana el primero?", gana_suma([g[5], g[9], g[13]]))


# ---------- fuerza bruta: minimax sobre la tupla completa ----------

def _gana_bruto(estado, sucesores):
    @lru_cache(maxsize=None)
    def gana(e):
        return any(not gana(s) for s in sucesores(e))
    return gana(estado)


def _suc_nim(e):
    for i, a in enumerate(e):
        for nuevo in range(a):
            yield tuple(sorted(e[:i] + (nuevo,) + e[i + 1:]))


def _suc_sustraccion(movs):
    def suc(e):
        for i, a in enumerate(e):
            for m in movs:
                if m <= a:
                    yield tuple(sorted(e[:i] + (a - m,) + e[i + 1:]))
    return suc


def _suc_division(e):
    for i, a in enumerate(e):
        for x in range(1, a):
            if x != a - x:
                yield tuple(sorted(e[:i] + e[i + 1:] + (x, a - x)))


def pruebas():
    random.seed(777)

    # Casos borde
    assert not gana_nim([]) and not gana_nim([0, 0]) and gana_nim([1])
    assert jugada_nim([2, 2]) is None and jugada_nim([0, 5]) == (1, 0)
    assert mex([]) == 0 and mex([0, 1, 3]) == 2
    assert grundy_division(2) == [0, 0, 0]

    # Nim: todas las posiciones con ≤ 3 pilas de ≤ 6
    for k in range(0, 4):
        for e in product(range(7), repeat=k):
            e = tuple(sorted(e))
            assert gana_nim(e) == _gana_bruto(e, _suc_nim)
            j = jugada_nim(list(e))
            if j is not None:
                i, nuevo = j
                assert nuevo < e[i] and not gana_nim(e[:i] + (nuevo,) + e[i + 1:])

    # Sumas de juegos de sustracción con movimientos aleatorios
    for _ in range(200):
        movs = sorted(random.sample(range(1, 6), random.randint(1, 3)))
        e = tuple(sorted(random.randint(0, 12) for _ in range(random.randint(1, 3))))
        g = grundy_sustraccion(12, movs)
        assert gana_suma([g[a] for a in e]) == _gana_bruto(e, _suc_sustraccion(movs))

    # Juego de Grundy (las jugadas crean nuevas pilas)
    g = grundy_division(14)
    for _ in range(200):
        e = tuple(sorted(random.randint(1, 14) for _ in range(random.randint(1, 2))))
        assert gana_suma([g[a] for a in e]) == _gana_bruto(e, _suc_division)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
