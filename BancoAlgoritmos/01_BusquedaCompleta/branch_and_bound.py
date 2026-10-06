r"""
Búsqueda completa — Ramificación y poda: clique máxima («Branch and bound, Bron–Kerbosch»)
Nivel: Avanzado
Ejecutar: python branch_and_bound.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Resolver EXACTAMENTE problemas de optimización NP-difíciles con N
    moderado (≈ 40–60) explorando un árbol de decisiones y cortando cada
    rama cuya COTA (lo mejor que podría lograr) no supera la mejor solución
    ya encontrada. Ejemplo clásico: la clique máxima (el mayor conjunto de
    vértices adyacentes dos a dos).
    Señales en el enunciado: «el mayor grupo en que todos son compatibles
    / amigos / comparten algo», «el mayor conjunto sin conflictos»
    (conjunto independiente = clique en el grafo complemento), N ≤ 50,
    sin estructura especial (no es árbol ni bipartito).

FUNCIÓN
    clique_maxima(n, ady) -> list[int]
        ady[v] = máscara de bits de los vecinos de v (sin v). Devuelve los
        vértices de una clique máxima, ordenados (lista vacía si n = 0).
    cliques_maximales(n, ady) -> int
        Cuántas cliques MAXIMALES hay (no se pueden agrandar). Es el
        Bron–Kerbosch con pivote «puro», sin cota.

IDEA Y ALGORITMO
    Bron–Kerbosch mantiene tres conjuntos (máscaras de bits):
      R = clique que se está construyendo,
      P = candidatos: vértices adyacentes a TODO R que aún se pueden agregar,
      X = vértices adyacentes a todo R que ya se exploraron (para no repetir).
    Al agregar v: R ∪ {v}, P ∩ N(v), X ∩ N(v). Si P y X quedan vacíos, R es
    maximal. Después de explorar v, se pasa de P a X.
    Pivote (Tomita): se elige u en P ∪ X con más vecinos en P y solo se
    ramifica sobre P \ N(u). Por qué basta: toda clique maximal contiene a
    u o a algún NO vecino de u (si solo tuviera vecinos de u, se podría
    agregar u y no sería maximal). Las ramas por vecinos de u se cubren
    cuando se ramifica por u mismo o por un no vecino. Con pivote, el
    número de llamadas es O(3^(n/3)) en el peor caso.
    Cota (branch and bound): R solo puede crecer con vértices de P, así que
    |R| + |P| es una cota superior. Si |R| + |P| ≤ mejor, se poda la rama.
    Ordenar los vértices de mayor a menor grado ayuda a encontrar pronto
    una clique grande (mejor cota desde el inicio).
    Máscaras: intersecar es un AND, |P| es P.bit_count(): muy rápido en Python.

MACROALGORITMO
    1. Construir ady[v] como máscara de vecinos.
    2. mejor = []; llamar expandir(R = ∅, P = todos, X = ∅).
    3. En expandir: si P y X vacíos → R es maximal; actualizar mejor.
    4. Si |R| + |P| ≤ |mejor| → podar (volver).
    5. Elegir pivote u en P ∪ X que maximice |P ∩ N(u)|.
    6. Para cada v en P \ N(u):
    7.    expandir(R ∪ {v}, P ∩ N(v), X ∩ N(v)); P −= {v}; X += {v}.
    8. Devolver mejor.

COMPLEJIDAD
    Peor caso O(3^(n/3)) llamadas (≈ 10^8 para n = 50, pero la cota y el
    pivote lo bajan muchísimo en grafos típicos). Memoria O(n) por nivel;
    la profundidad es ≤ tamaño de la clique ≤ n (recursión segura).
    En Python, grafos aleatorios de n = 50 con densidad 0,5 en < 0,1 s.

EJEMPLO A MANO
    Vértices 0..5, aristas: 0-1, 0-2, 1-2, 1-3, 2-3, 3-4, 4-5, 3-5
      R = {}, P = {0..5}. Pivote: u = 3 (vecinos en P: 1, 2, 4, 5)
      → solo se ramifica en P \ N(3) = {0, 3}
      v = 0: R = {0}, P = {1, 2} → v = 1: R = {0, 1}, P = {2} → {0, 1, 2} maximal (3)
      v = 3: R = {3}, P = {1, 2, 4, 5}, X = {} (0 no es vecino de 3)
        cota 1 + 4 > 3, sigue; pivote 1 → ramas v = 1 y v = 4:
        R = {3, 1}, P = {2}: cota 2 + 1 = 3 ≤ 3 → se poda ({1, 2, 3} no mejora)
        R = {3, 4}, P = {5}: cota 2 + 1 = 3 ≤ 3 → se poda ({3, 4, 5} tampoco)
    → clique máxima de tamaño 3: [0, 1, 2]

ERRORES TÍPICOS
    - Incluir v en ady[v] (lazos): rompe P ∩ N(v).
    - Olvidar pasar v de P a X tras explorarlo: se repiten cliques.
    - Elegir el pivote solo en P (también vale, pero en P ∪ X poda más).
    - Podar con ≤ cuando se quieren TODAS las soluciones óptimas (usar <).
    - Para conjunto independiente máximo, olvidar complementar el grafo.

VARIANTES Y RELACIONADOS
    - Cota por coloreo voraz (algoritmo MCQ/MCS de Tomita): una clique usa a
      lo sumo un vértice de cada color; mucho más fuerte que |P|.
    - Conjunto independiente máximo = clique máxima del complemento;
      cobertura de vértices mínima = n − independiente máximo.
    - Coloreo de grafos con N pequeño: backtracking + cotas.
    - Relacionados: backtracking_poda.py, subconjuntos_mascaras.py,
      meet_in_the_middle.py (clique máxima en N ≤ 40 también sale con MITM).

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/H - Holy Network (clique máxima, branch & bound con
      coloreo de Tomita)
    - Codeforces 1105E «Helping Hiasat» (conjunto independiente máximo, N ≤ 40)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (las 2^n máscaras, revisando si cada
      una es clique y si es maximal) en 600 grafos aleatorios de n ≤ 11 con
      densidades variadas + casos borde + un caso n = 50 validado como
      clique (python branch_and_bound.py)
"""
import random


def clique_maxima(n, ady):
    """Vértices (ordenados) de una clique máxima; ady[v] = máscara de vecinos."""
    mejor = [0]                 # máscara de la mejor clique (lista para modificarla dentro)

    def expandir(R, P, X):
        if not P and not X:
            if R.bit_count() > mejor[0].bit_count():
                mejor[0] = R    # R es maximal y mejor que lo conocido
            return
        if R.bit_count() + P.bit_count() <= mejor[0].bit_count():
            return              # COTA: ni tomando todo P se supera lo mejor
        # pivote: vértice de P ∪ X con más vecinos en P
        PX = P | X
        u, mejor_grado = -1, -1
        while PX:
            b = PX & -PX
            PX ^= b
            w = b.bit_length() - 1
            g = (P & ady[w]).bit_count()
            if g > mejor_grado:
                u, mejor_grado = w, g
        candidatos = P & ~ady[u]  # solo no vecinos del pivote (u incluido si está en P)
        while candidatos:
            b = candidatos & -candidatos
            candidatos ^= b
            v = b.bit_length() - 1
            expandir(R | b, P & ady[v], X & ady[v])
            P &= ~b             # v ya explorado: de P a X
            X |= b
            if R.bit_count() + P.bit_count() <= mejor[0].bit_count():
                return          # la cota también se re-evalúa al achicarse P

    if n > 0:
        expandir(0, (1 << n) - 1, 0)
    return [v for v in range(n) if mejor[0] >> v & 1]


def cliques_maximales(n, ady):
    """Número de cliques maximales (Bron–Kerbosch con pivote, sin cota)."""
    total = 0
    pila = [(0, (1 << n) - 1, 0)]   # pila explícita de (R, P, X)
    while pila:
        R, P, X = pila.pop()
        if not P and not X:
            total += 1
            continue
        PX = P | X
        u = max((w for w in range(n) if PX >> w & 1), key=lambda w: (P & ady[w]).bit_count())
        candidatos = P & ~ady[u]
        while candidatos:
            b = candidatos & -candidatos
            candidatos ^= b
            v = b.bit_length() - 1
            pila.append((R | b, P & ady[v], X & ady[v]))
            P &= ~b
            X |= b
    return total


def grafo(n, aristas):
    """Lista de adyacencia como máscaras a partir de una lista de aristas."""
    ady = [0] * n
    for a, b in aristas:
        ady[a] |= 1 << b
        ady[b] |= 1 << a
    return ady


def demo():
    aristas = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (3, 5)]
    ady = grafo(6, aristas)
    print("aristas:", aristas)
    print("clique_maxima =", clique_maxima(6, ady))           # [0, 1, 2]
    print("cliques maximales:", cliques_maximales(6, ady))    # 3


def _es_clique(m, n, ady):
    return all(ady[i] >> j & 1 for i in range(n) if m >> i & 1 for j in range(n) if m >> j & 1 and j != i)


def pruebas():
    random.seed(1105)

    # Casos borde
    assert clique_maxima(0, []) == []
    assert cliques_maximales(0, []) == 1                  # el vacío es la única maximal
    assert clique_maxima(1, [0]) == [0]
    assert clique_maxima(3, [0, 0, 0]) == [0]             # sin aristas: un vértice
    assert cliques_maximales(3, [0, 0, 0]) == 3
    completo = grafo(6, [(i, j) for i in range(6) for j in range(i + 1, 6)])
    assert clique_maxima(6, completo) == list(range(6))
    assert cliques_maximales(6, completo) == 1

    for _ in range(600):
        n = random.randint(1, 11)
        p = random.choice([0.1, 0.3, 0.5, 0.7, 0.9])
        ady = grafo(n, [(i, j) for i in range(n) for j in range(i + 1, n) if random.random() < p])
        cliques = [m for m in range(1 << n) if _es_clique(m, n, ady)]
        tam = max(m.bit_count() for m in cliques)
        r = clique_maxima(n, ady)
        mr = sum(1 << v for v in r)
        assert len(r) == tam and _es_clique(mr, n, ady)
        # maximal: ningún vértice de fuera es adyacente a todos los de la clique
        maximales = sum(1 for m in cliques
                        if not any(not m >> v & 1 and ady[v] & m == m for v in range(n)))
        assert cliques_maximales(n, ady) == maximales

    # Caso grande: n = 50, debe terminar rápido y ser clique
    n = 50
    ady = grafo(n, [(i, j) for i in range(n) for j in range(i + 1, n) if random.random() < 0.5])
    r = clique_maxima(n, ady)
    assert _es_clique(sum(1 << v for v in r), n, ady) and len(r) >= 2


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
