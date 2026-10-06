"""
Grafos — 2-SAT con componentes fuertemente conexas («2-satisfiability»)
Nivel: Avanzado
Ejecutar: python dos_sat.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir si n variables booleanas pueden tomar valores que cumplan un
    conjunto de cláusulas de la forma (a ∨ b), donde a y b son literales
    (x_i o ¬x_i), y construir una asignación válida si existe. En tiempo
    lineal, mientras que SAT general (3 o más literales) es NP-completo.
    Señales en el enunciado: cada elemento tiene DOS opciones (encender o
    no, arriba/abajo, equipo A o B) y las restricciones hablan de PARES:
    «no ambos», «al menos uno de los dos», «si i entonces j», «iguales»,
    «distintos». n hasta 10^5.

FUNCIÓN
    dos_sat(n, clausulas) -> list[bool] | None
        Variables 0..n-1. Cada cláusula es un par de literales ((i, vi), (j, vj))
        que significa (x_i == vi) ∨ (x_j == vj).
        Devuelve una asignación (lista de n booleanos) o None si no hay.
    Restricciones típicas como cláusulas:
        «x_i obligatorio = v»:   ((i, v), (i, v))
        «no ambos»:              ((i, False), (j, False))
        «al menos uno»:          ((i, True), (j, True))
        «si x_i entonces x_j»:   ((i, False), (j, True))
        «x_i == x_j»:            ((i, False), (j, True)) y ((i, True), (j, False))
        «x_i != x_j» (XOR):      ((i, True), (j, True)) y ((i, False), (j, False))

IDEA Y ALGORITMO
    Grafo de implicaciones con 2n nodos: nodo 2i = «x_i», nodo 2i+1 = «¬x_i»
    (negar un literal es cambiar el último bit: l ^ 1). La cláusula (a ∨ b)
    equivale a dos implicaciones: ¬a → b y ¬b → a (si a falla, b debe valer).
    Las implicaciones son transitivas, así que si hay camino de p a q,
    «p verdadero» obliga «q verdadero».
    - Insatisfacible ⇔ para algún i, x_i y ¬x_i están en la misma SCC:
      x_i ⇒ ¬x_i y ¬x_i ⇒ x_i, contradicción. (El recíproco es la parte
      constructiva de abajo.)
    - Construcción: con las SCC numeradas en orden topológico del
      condensado, poner x_i = verdadero si comp[x_i] > comp[¬x_i] (el
      literal que va DESPUÉS en el orden topológico se hace verdadero).
      Por qué funciona: si se pusiera verdadero un literal p y existiera
      p →* q con q falso, entonces comp[p] ≤ comp[q] y, por la simetría del
      grafo (p → q implica ¬q → ¬p), comp[¬q] ≤ comp[¬p]. Como p es
      verdadero, comp[p] > comp[¬p]; como q es falso, comp[¬q] > comp[q].
      Encadenando: comp[p] ≤ comp[q] < comp[¬q] ≤ comp[¬p] < comp[p],
      imposible. Así ninguna implicación lleva de verdadero a falso, y toda
      cláusula se cumple.
    Las SCC se calculan con Tarjan iterativo (copiado de scc.py).
    Ingenuo: probar las 2^n asignaciones.

MACROALGORITMO
    1. Crear 2n nodos (x_i y ¬x_i).
    2. Por cada cláusula (a ∨ b): aristas ¬a → b y ¬b → a.
    3. Calcular las SCC numeradas en orden topológico.
    4. Si comp[2i] == comp[2i+1] para algún i: no hay solución.
    5. Si no, x_i = (comp[2i] > comp[2i+1]).

COMPLEJIDAD
    Tiempo O(n + m), memoria O(n + m), con m cláusulas.
    En Python, ~10^5 cláusulas en alrededor de 1 s.

EJEMPLO A MANO
    3 variables, cláusulas (x0 ∨ x1), (¬x0 ∨ x2), (¬x1 ∨ ¬x2), (¬x2 ∨ ¬x0).
    Aristas: ¬x0→x1, ¬x1→x0, x0→x2, ¬x2→¬x0, x1→¬x2, x2→¬x1, x2→¬x0, x0→¬x2.
    x0 → x2 → ¬x0: poner x0 obliga ¬x0, así que x0 = falso. Luego la
    primera cláusula exige x1 = verdadero, la tercera x2 = falso, y todas se
    cumplen: x = [F, V, F]. El código llega a lo mismo con las SCC.

ERRORES TÍPICOS
    - Agregar solo una de las dos implicaciones de la cláusula (el grafo
      pierde la simetría y la asignación puede salir mal).
    - Invertir la regla de asignación: depende de si las SCC vienen en
      orden topológico (aquí, comp[x] > comp[¬x]) o inverso (Tarjan crudo:
      comp[x] < comp[¬x]).
    - Codificar «x obligatorio» con una sola arista x → x (no hace nada);
      lo correcto es la cláusula (x ∨ x), que da la arista ¬x → x.
    - Generar Θ(n²) cláusulas cuando n es grande: en Python no cabe;
      hay que buscar estructura (ver Colombia 2024 G).

VARIANTES Y RELACIONADOS
    - «A lo sumo uno de un grupo» con variables prefijo (O(k) cláusulas en
      vez de O(k²)).
    - Asignación lexicográficamente menor / con preferencias: requiere
      otra técnica (probar literales con propagación), no solo SCC.
    - scc.py (Tarjan y Kosaraju), bipartito.py (2-coloración = 2-SAT con
      solo cláusulas XOR).

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/G - Signal Coverage (2-SAT con Tarjan y generación
      perezosa de restricciones)
    - CSES «Giant Pizza»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (las 2^n asignaciones) en 1500
      instancias aleatorias con n ≤ 8: coincide la satisfacibilidad y la
      asignación devuelta cumple todas las cláusulas; casos borde y una
      cadena de 10^5 implicaciones (python dos_sat.py)
"""
import itertools
import random


def _tarjan_scc(n, ady):
    """Tarjan iterativo (ver scc.py). comp en ORDEN TOPOLÓGICO del condensado."""
    indice = [-1] * n
    bajo = [0] * n
    en_pila = [False] * n
    sig = [0] * n
    pila = []
    comp = [-1] * n
    c = t = 0
    for r in range(n):
        if indice[r] != -1:
            continue
        indice[r] = bajo[r] = t
        t += 1
        pila.append(r)
        en_pila[r] = True
        llamadas = [r]
        while llamadas:
            v = llamadas[-1]
            if sig[v] < len(ady[v]):
                w = ady[v][sig[v]]
                sig[v] += 1
                if indice[w] == -1:
                    indice[w] = bajo[w] = t
                    t += 1
                    pila.append(w)
                    en_pila[w] = True
                    llamadas.append(w)
                elif en_pila[w] and indice[w] < bajo[v]:
                    bajo[v] = indice[w]
            else:
                llamadas.pop()
                if llamadas and bajo[v] < bajo[llamadas[-1]]:
                    bajo[llamadas[-1]] = bajo[v]
                if bajo[v] == indice[v]:
                    while True:
                        w = pila.pop()
                        en_pila[w] = False
                        comp[w] = c
                        if w == v:
                            break
                    c += 1
    return [c - 1 - x for x in comp]


def dos_sat(n, clausulas):
    """Asignación que cumple todas las cláusulas ((i, vi), (j, vj)), o None."""
    # nodo del literal "x_i == v": 2i si v es verdadero, 2i+1 si es falso
    def nodo(i, v):
        return 2 * i + (0 if v else 1)

    ady = [[] for _ in range(2 * n)]
    for (i, vi), (j, vj) in clausulas:
        a, b = nodo(i, vi), nodo(j, vj)
        ady[a ^ 1].append(b)        # ¬a → b
        ady[b ^ 1].append(a)        # ¬b → a
    comp = _tarjan_scc(2 * n, ady)
    asignacion = []
    for i in range(n):
        if comp[2 * i] == comp[2 * i + 1]:
            return None             # x_i ⇔ ¬x_i: contradicción
        # el literal que va después en orden topológico es el verdadero
        asignacion.append(comp[2 * i] > comp[2 * i + 1])
    return asignacion


def cumple(asignacion, clausulas):
    return all(asignacion[i] == vi or asignacion[j] == vj
               for (i, vi), (j, vj) in clausulas)


def demo():
    clausulas = [((0, True), (1, True)),      # x0 ∨ x1
                 ((0, False), (2, True)),     # ¬x0 ∨ x2
                 ((1, False), (2, False)),    # ¬x1 ∨ ¬x2
                 ((2, False), (0, False))]    # ¬x2 ∨ ¬x0
    x = dos_sat(3, clausulas)
    print("Asignación:", x)                   # [False, True, False]
    # Con x0 obligatorio se vuelve imposible (x0 → x2 → ¬x0)
    print("Con x0 obligatorio:", dos_sat(3, clausulas + [((0, True), (0, True))]))
    # XOR en cadena con número impar de variables en ciclo: imposible
    ciclo = []
    for i in range(3):
        j = (i + 1) % 3
        ciclo += [((i, True), (j, True)), ((i, False), (j, False))]
    print("x0≠x1≠x2≠x0:", dos_sat(3, ciclo))   # None


def _fuerza_bruta(n, clausulas):
    for asig in itertools.product([False, True], repeat=n):
        if cumple(asig, clausulas):
            return True
    return False


def pruebas():
    random.seed(77)

    # Casos borde
    assert dos_sat(0, []) == []
    assert dos_sat(1, []) is not None
    assert dos_sat(1, [((0, True), (0, True))]) == [True]
    assert dos_sat(1, [((0, False), (0, False))]) == [False]
    assert dos_sat(1, [((0, True), (0, True)), ((0, False), (0, False))]) is None
    assert dos_sat(2, [((0, True), (1, False))]) is not None
    # x == y y x != y a la vez: imposible
    assert dos_sat(2, [((0, False), (1, True)), ((0, True), (1, False)),
                       ((0, True), (1, True)), ((0, False), (1, False))]) is None

    # Aleatorios contra las 2^n asignaciones
    for _ in range(1500):
        n = random.randint(1, 8)
        m = random.randint(0, 3 * n)
        cl = [((random.randrange(n), random.random() < 0.5),
               (random.randrange(n), random.random() < 0.5)) for _ in range(m)]
        x = dos_sat(n, cl)
        assert (x is not None) == _fuerza_bruta(n, cl)
        if x is not None:
            assert len(x) == n and cumple(x, cl)

    # Grande: x0 obligatorio y x_i → x_{i+1}; todo debe quedar verdadero
    N = 10 ** 5
    cl = [((0, True), (0, True))] + [((i, False), (i + 1, True)) for i in range(N - 1)]
    assert dos_sat(N, cl) == [True] * N
    # ...y con ¬x_{N-1} obligatorio se vuelve imposible
    assert dos_sat(N, cl + [((N - 1, False), (N - 1, False))]) is None


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
