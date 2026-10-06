"""
Grafos — Grafos funcionales: ciclos, liebre y tortuga de Floyd, k-ésimo sucesor
         («Functional graphs», «Floyd's cycle detection», «binary lifting»)
Nivel: Intermedio/Avanzado
Ejecutar: python grafo_funcional.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Un grafo funcional es uno donde cada nodo tiene EXACTAMENTE una arista
    de salida: v → f(v). Toda secuencia x, f(x), f(f(x)), … termina
    entrando a un ciclo (forma de «ρ»: una cola y luego un ciclo). Sirve
    para saber dónde y cuándo se repite un proceso, y para saltar k pasos
    con k enorme (10^9, 10^18) sin simular.
    Señales en el enunciado: «cada X apunta/envía/teletransporta a un único
    Y», permutaciones, «aplicar la operación k veces», «¿termina o se queda
    en un ciclo?», generadores pseudoaleatorios x → (a·x + b) mod m,
    «después de 10^18 pasos, ¿dónde está?».

FUNCIÓN
    analizar(f) -> (en_ciclo, cola, largo)
        f[v] = sucesor de v (0..n-1). en_ciclo[v]: v está en un ciclo;
        cola[v]: pasos hasta llegar a un nodo de ciclo; largo[v]: largo del
        ciclo al que llega v.
    floyd(g, x0) -> (mu, lam)
        g = función (callable), sin tabla: mu = índice del primer elemento
        de la secuencia que está en el ciclo, lam = largo del ciclo.
        Memoria O(1): sirve cuando el espacio de estados es enorme.
    Saltos(f, max_k)            binary lifting
        .sucesor(v, k) -> f aplicado k veces a v (0 ≤ k ≤ max_k).

IDEA Y ALGORITMO
    Ciclos (analizar): recorrer desde cada nodo no visitado marcando los
    nodos del camino actual con su posición. Si se llega a un nodo del
    MISMO camino, desde esa posición hasta el final hay un ciclo nuevo. Si
    se llega a un nodo ya terminado, el camino es solo cola. Luego, de
    atrás hacia adelante, cola[x] = cola[f[x]] + 1. Cada nodo se recorre
    una vez: O(n), sin recursión.
    Floyd (liebre y tortuga): la tortuga avanza 1 y la liebre 2. Una vez
    ambas dentro del ciclo la liebre gana 1 por paso, así que se encuentran
    en < mu + lam pasos, en un punto x_i con i múltiplo de lam. Entonces,
    si una vuelve a x0 y ambas avanzan de a 1, se encuentran exactamente en
    x_mu (desde x_i, mu pasos más dan x_{i+mu} = x_mu porque i ≡ 0 mód lam).
    Con mu conocido, una más da la vuelta al ciclo para medir lam.
    Binary lifting: salto[j][v] = f aplicado 2^j veces a v; se llena con
    salto[j][v] = salto[j−1][salto[j−1][v]]. Para avanzar k se suman los
    saltos de los bits encendidos de k: O(log k) por consulta.
    Alternativa sin tablas para una sola consulta: con analizar(), si
    k ≥ cola[v] se reduce k a cola[v] + (k − cola[v]) mód largo[v].

MACROALGORITMO
    analizar:
    1. estado = 0 (nuevo), 1 (en el camino actual), 2 (terminado).
    2. Desde cada s nuevo, avanzar v = f[v] guardando el camino hasta ver
       un nodo con estado ≠ 0.
    3. Si ese nodo tiene estado 1: el sufijo del camino desde él es un
       ciclo: cola = 0, largo = su tamaño.
    4. El resto del camino, de atrás hacia adelante: cola = cola[f] + 1,
       largo = largo[f]. Marcar todo como terminado.
    floyd:
    1. t = g(x0), l = g(g(x0)); mientras t != l: t = g(t), l = g(g(l)).
    2. t = x0; mu = 0; mientras t != l: t = g(t), l = g(l), mu += 1.
    3. lam = 1, l = g(t); mientras t != l: l = g(l), lam += 1.

COMPLEJIDAD
    analizar: O(n). floyd: O(mu + lam) evaluaciones, memoria O(1).
    Saltos: O(n log K) preproceso y memoria, O(log K) por consulta.
    En Python: n = 2·10^5 con K = 10^9 (30 niveles) en ~1–2 s.

EJEMPLO A MANO
    f = [1, 2, 3, 1, 3, 4, 5]:   6 → 5 → 4 → 3 → 1 → 2 → 3 …
    Ciclo {1, 2, 3} (largo 3). Desde 0: cola 1. Desde 6: cola 3 (6→5→4→3).
    Floyd desde x0 = 6: secuencia x0..x8 = 6 5 4 3 1 2 3 1 2 …
      (tortuga, liebre) = (x1, x2) = (5, 4) → (x2, x4) = (4, 1)
      → (x3, x6) = (3, 3): se encuentran; i = 3 es múltiplo de lam = 3.
      Tortuga a x0, liebre sigue en x6, ambas de a 1:
      (6, 3) → (5, 1) → (4, 2) → (3, 3): mu = 3 (x3 = 3 es el primero
      del ciclo). Una vuelta desde 3: 1, 2, 3 → lam = 3.
    sucesor(6, 10): 6→5→4→3→1→2→3→1→2→3→1 → 1.

ERRORES TÍPICOS
    - Seguir el camino recursivamente (n = 10^5 revienta la pila).
    - Marcar solo «visitado» sin distinguir «en el camino actual»: un nodo
      ya terminado no indica un ciclo nuevo.
    - En Floyd, arrancar con t = l = x0 y comparar antes de mover (se
      «encuentran» de inmediato).
    - Binary lifting con pocos niveles: para K = 10^18 hacen falta 60.
    - Olvidar que la cola NO se repite: reducir k mód largo solo cuando
      k ≥ cola[v].

VARIANTES Y RELACIONADOS
    - Permutaciones (todo nodo en un ciclo): orden = mcm de los largos.
    - Brent: otra detección de ciclos O(1) memoria, algo más rápida.
    - Pollard-Rho usa Floyd/Brent sobre x → x² + c mód n.
    - lca.py (binary lifting sobre el padre en un árbol).
    - deteccion_ciclos.py (ciclos en grafos generales), scc.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/K - kewl Texting (seguir sugerencias desde {start}
      en un grafo funcional: llega a {end} o detecta un ciclo → INFINITE)
    - CSES «Planets Queries I» (k-ésimo sucesor), «Planets Queries II»,
      «Planets Cycles»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (simular paso a paso y guardar la
      primera aparición de cada nodo) en 500 grafos funcionales aleatorios
      con n ≤ 30 (todos los nodos y k ≤ 100), Floyd contra el mismo
      método en 500 secuencias x → (a·x² + b) mod m; casos borde y n = 10^5
      con k = 10^18 (python grafo_funcional.py)
"""
import random


def analizar(f):
    """(en_ciclo, cola, largo) para cada nodo del grafo funcional f."""
    n = len(f)
    estado = [0] * n           # 0 nuevo, 1 en el camino actual, 2 terminado
    pos = [0] * n              # posición en el camino actual
    en_ciclo = [False] * n
    cola = [0] * n
    largo = [0] * n
    for s in range(n):
        if estado[s]:
            continue
        camino = []
        v = s
        while estado[v] == 0:
            estado[v] = 1
            pos[v] = len(camino)
            camino.append(v)
            v = f[v]
        if estado[v] == 1:     # volvimos al camino actual: ciclo nuevo
            ciclo = camino[pos[v]:]
            for x in ciclo:
                en_ciclo[x] = True
                largo[x] = len(ciclo)
                estado[x] = 2
            camino = camino[:pos[v]]
        for x in reversed(camino):              # la cola, de atrás hacia adelante
            cola[x] = cola[f[x]] + 1
            largo[x] = largo[f[x]]
            estado[x] = 2
    return en_ciclo, cola, largo


def floyd(g, x0):
    """(mu, lam) de la secuencia x0, g(x0), g(g(x0)), … con memoria O(1)."""
    # 1) encontrarse dentro del ciclo (la liebre va al doble)
    t, l = g(x0), g(g(x0))
    while t != l:
        t, l = g(t), g(g(l))
    # 2) desde x0 y desde el encuentro, de a un paso: se cruzan en x_mu
    mu = 0
    t = x0
    while t != l:
        t, l = g(t), g(l)
        mu += 1
    # 3) dar una vuelta para medir el ciclo
    lam = 1
    l = g(t)
    while t != l:
        l = g(l)
        lam += 1
    return mu, lam


class Saltos:
    """Binary lifting: f aplicado k veces en O(log k)."""

    def __init__(self, f, max_k):
        self.tabla = [list(f)]                  # tabla[j][v] = f^(2^j)(v)
        for _ in range(1, max(1, max_k.bit_length())):
            ant = self.tabla[-1]
            self.tabla.append([ant[ant[v]] for v in range(len(f))])

    def sucesor(self, v, k):
        j = 0
        while k:
            if k & 1:
                v = self.tabla[j][v]
            k >>= 1
            j += 1
        return v


def demo():
    f = [1, 2, 3, 1, 3, 4, 5]
    en_ciclo, cola, largo = analizar(f)
    print("en ciclo:", [v for v in range(len(f)) if en_ciclo[v]])   # [1, 2, 3]
    print("cola:", cola, "largo:", largo)
    print("Floyd desde 6 (mu, lam):", floyd(lambda x: f[x], 6))     # (3, 3)
    print("sucesor(6, 10):", Saltos(f, 10).sucesor(6, 10))           # 1
    # Estilo kewl Texting: seguir desde 0 hasta llegar a un nodo final o repetir
    g = [2, 0, 4, 3, 1]            # 3 → 3 sería «{end}»; desde 0: 0 2 4 1 0 … ciclo
    visto, v, seq = set(), 0, []
    while v not in visto and v != 3:
        visto.add(v)
        seq.append(v)
        v = g[v]
    print("desde 0:", seq, "→", "termina" if v == 3 else "INFINITE")


def _bruto_secuencia(g, x0, limite):
    """mu y lam simulando con diccionario de primeras apariciones."""
    primera = {}
    x, i = x0, 0
    while x not in primera:
        primera[x] = i
        x = g(x)
        i += 1
        assert i <= limite
    return primera[x], i - primera[x]


def pruebas():
    random.seed(1967)

    # Casos borde
    assert analizar([]) == ([], [], [])
    assert analizar([0]) == ([True], [0], [1])                 # lazo
    assert analizar([1, 0]) == ([True, True], [0, 0], [2, 2])
    assert floyd(lambda x: 0, 0) == (0, 1)
    assert floyd(lambda x: min(x + 1, 5), 0) == (5, 1)
    assert Saltos([0], 1).sucesor(0, 0) == 0

    for _ in range(500):
        n = random.randint(1, 30)
        if random.random() < 0.2:
            f = random.sample(range(n), n)                     # permutación
        else:
            f = [random.randrange(n) for _ in range(n)]
        en_ciclo, cola, largo = analizar(f)
        S = Saltos(f, 100)
        for v in range(n):
            mu, lam = _bruto_secuencia(lambda x: f[x], v, n + 1)
            assert cola[v] == mu and largo[v] == lam and en_ciclo[v] == (mu == 0)
            assert floyd(lambda x: f[x], v) == (mu, lam)
            x = v
            for k in range(101):
                assert S.sucesor(v, k) == x
                x = f[x]

    # Floyd sobre secuencias implícitas (sin tabla)
    for _ in range(500):
        m = random.randint(1, 3000)
        a, b = random.randrange(m), random.randrange(m)
        g = lambda x, a=a, b=b, m=m: (a * x * x + b) % m
        x0 = random.randrange(m)
        assert floyd(g, x0) == _bruto_secuencia(g, x0, m + 1)

    # Grande: n = 10^5, k = 10^18 contra la reducción por ciclo
    N = 10 ** 5
    f = [random.randrange(N) for _ in range(N)]
    K = 10 ** 18
    S = Saltos(f, K)
    _, cola, largo = analizar(f)
    for v in random.sample(range(N), 200):
        k = cola[v] + (K - cola[v]) % largo[v]                  # mismo nodo que K pasos
        x = v
        for _ in range(k):
            x = f[x]
        assert S.sucesor(v, K) == x


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
