"""
Matemáticas — Juegos: DP de posiciones ganadoras/perdedoras y minimax («winning/losing positions»)
Nivel: Intermedio
Ejecutar: python posiciones_ganadoras.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir quién gana un juego de dos jugadores con información completa
    y sin azar, jugando ambos óptimamente, calculando para CADA posición si
    es ganadora (G) o perdedora (P) para quien mueve; o, si hay puntaje,
    la mejor diferencia de puntos que puede asegurar (minimax).
    Cómo reconocerlo: «juegan óptimamente», «¿quién gana?», «¿cuántos
    puntos más obtiene el primero?»; el número de posiciones distintas es
    manejable (≤ 10^6–10^7) aunque el árbol de partidas sea enorme.

FUNCIÓN
    tabla_sustraccion(N, movs) -> list[bool]
        gana[n] para una pila de n piedras de la que se quitan m ∈ movs;
        pierde quien no puede mover.
    juego_en_grafo(n, aristas) -> list[str]
        Ficha en un grafo dirigido (puede tener CICLOS): mover la ficha por
        una arista; pierde quien no puede mover. Resultado por nodo:
        'G' (gana quien mueve), 'P' (pierde) o 'E' (empate: juego infinito).
    extremos(a) -> int
        Juego de quitar del extremo izquierdo o derecho de un arreglo y
        sumarse ese valor: diferencia (primero − segundo) con juego óptimo.

IDEA Y ALGORITMO
    Definición recursiva (la que se demuestra por inducción en el número
    de jugadas restantes, en un juego que siempre termina):
      - una posición sin jugadas es perdedora (P);
      - es GANADORA ⇔ existe una jugada a una posición perdedora (el rival
        quedará perdiendo);
      - es PERDEDORA ⇔ todas las jugadas llevan a posiciones ganadoras.
    Si el grafo de posiciones es acíclico, se calcula en orden topológico
    (por tamaño: pilas más pequeñas primero).
    Con ciclos (análisis retrógrado): se parte de las posiciones sin
    jugadas (P) y se propaga hacia atrás con una cola: un predecesor de una
    P es G; un predecesor queda P cuando TODAS sus jugadas resultaron G
    (contador de sucesores sin resolver que llega a 0). Lo que nunca se
    resuelve es empate: ningún jugador puede forzar el final (el que
    perdería siempre tiene una jugada que no pierde y evita las P).
    Minimax con puntaje: dif[i][j] = mejor (mío − rival) con el subarreglo
    a[i..j]; si tomo a[i], el rival queda con dif[i+1][j] a su favor:
        dif[i][j] = max(a[i] − dif[i+1][j], a[j] − dif[i][j−1]).
    El ingenuo (explorar todas las partidas) es exponencial; la DP visita
    cada posición una vez.

MACROALGORITMO
    1. Definir la posición (estado) con lo mínimo que determina el futuro
       (incluye de quién es el turno si el juego no es simétrico).
    2. Identificar las posiciones terminales y su valor.
    3. Sin ciclos: recorrer en orden (tamaño creciente) aplicando
       «G si algún sucesor es P».
    4. Con ciclos: análisis retrógrado con cola y contador de sucesores.
    5. Con puntaje: dif = max sobre jugadas de (ganancia − dif del rival).
    6. Si N es enorme, imprimir la tabla para N pequeño y buscar el patrón.

COMPLEJIDAD
    O(posiciones × jugadas): sustracción O(N·|movs|); grafo O(n + m);
    extremos O(n²) (n ≈ 3000 en ~2 s en Python).

EJEMPLO A MANO
    movs = {1, 3, 4}: n=0 P; 1 G (→0); 2 P (solo →1 G); 3 G (→0); 4 G (→0);
    5 G (→2); 6 G (→2); 7 P (→6,4,3 todas G); 8 G (→7) … periodo 7: P en
    n ≡ 0, 2 (mód 7).
    a = [4, 5, 1, 3]: largo 2: [5,1]→4, [4,5]→1, [1,3]→2; largo 3:
    [4,5,1] → max(4−4, 1−1) = 0, [5,1,3] → max(5−2, 3−4) = 3;
    largo 4: max(4 − 3, 3 − 0) = 3. El primero debe tomar el 3 (¡no el 4,
    que es mayor!): 3, 4, 5, 1 → 8 − 5 = 3.

ERRORES TÍPICOS
    - Marcar «perdedora» una posición solo porque UNA jugada lleva a G
      (debe ser TODAS).
    - Con ciclos, usar recursión con memo directamente: entra en ciclo
      infinito o marca mal los empates.
    - En minimax con puntaje, sumar en vez de restar el valor del rival.
    - Recursión profunda en Python (usar DP iterativa).
    - Confundir juego normal (pierde quien no puede mover) con misère.

VARIANTES Y RELACIONADOS
    - nim_sprague_grundy.py (cuando el juego es suma de juegos independientes).
    - Juegos en DAG con «quién mueve» en el estado (juegos partisanos).
    - Poda alfa–beta para minimax en árboles grandes.
    - DP sobre intervalos (dif[i][j] es un caso típico).

DÓNDE PRACTICAR
    - No hay problemas del repo que lo usen.
    - CSES «Stick Game» (tabla_sustraccion), «Removal Game» (extremos)

VERIFICACIÓN
    - Pruebas: OK contra búsqueda exhaustiva: minimax recursivo del árbol
      completo (sustracción N ≤ 25 y extremos n ≤ 10, 600 casos) y, para
      grafos con ciclos, minimax limitado a 2n+2 jugadas (gana/pierde
      forzado dentro del límite, si no empate) en 400 grafos aleatorios
      (python posiciones_ganadoras.py)
"""
import random
from collections import deque


def tabla_sustraccion(N, movs):
    """gana[n]: True si quien mueve gana con una pila de n (quitar m ∈ movs)."""
    gana = [False] * (N + 1)
    for n in range(1, N + 1):
        # G si existe una jugada a una posición perdedora
        gana[n] = any(m <= n and not gana[n - m] for m in movs)
    return gana


def juego_en_grafo(n, aristas):
    """'G'/'P'/'E' por nodo para el juego de mover una ficha en un grafo dirigido."""
    suc_pendientes = [0] * n                    # sucesores aún no resueltos como G
    pred = [[] for _ in range(n)]
    for u, v in aristas:
        suc_pendientes[u] += 1
        pred[v].append(u)
    res = ['E'] * n
    cola = deque()
    for v in range(n):
        if suc_pendientes[v] == 0:              # sin jugadas: pierde quien mueve
            res[v] = 'P'
            cola.append(v)
    while cola:
        v = cola.popleft()
        for u in pred[v]:
            if res[u] != 'E':
                continue
            if res[v] == 'P':
                res[u] = 'G'                    # puede mover a una perdedora
                cola.append(u)
            else:
                suc_pendientes[u] -= 1
                if suc_pendientes[u] == 0:      # todas sus jugadas llevan a G
                    res[u] = 'P'
                    cola.append(u)
    return res


def extremos(a):
    """Diferencia óptima (primero − segundo) tomando de los extremos del arreglo."""
    n = len(a)
    if n == 0:
        return 0
    dif = a[:]                                  # intervalos de largo 1: dif[i] = a[i]
    for largo in range(2, n + 1):
        # dif[i] pasa a representar el intervalo a[i .. i+largo-1]
        dif = [max(a[i] - dif[i + 1], a[i + largo - 1] - dif[i])
               for i in range(n - largo + 1)]
    return dif[0]


def demo():
    g = tabla_sustraccion(14, [1, 3, 4])
    print("{1,3,4}, n=0..14:", "".join("G" if x else "P" for x in g))  # PGPGGGGPGPGGGGP
    print("grafo 0->1, 1->2, 2->0, 3->4, 2->3:",
          juego_en_grafo(5, [(0, 1), (1, 2), (2, 0), (3, 4), (2, 3)]))  # E E E G P
    print("extremos [4, 5, 1, 3]:", extremos([4, 5, 1, 3]))                 # 3


def _sustraccion_bruta(n, movs):
    return any(not _sustraccion_bruta(n - m, movs) for m in movs if m <= n)


def _extremos_bruto(a):
    if not a:
        return 0
    return max(a[0] - _extremos_bruto(a[1:]), a[-1] - _extremos_bruto(a[:-1]))


def _grafo_bruto(n, aristas):
    suc = [[] for _ in range(n)]
    for u, v in aristas:
        suc[u].append(v)
    memo = {}

    def val(v, d):                              # resultado forzable en ≤ d jugadas
        if (v, d) in memo:
            return memo[(v, d)]
        if not suc[v]:
            r = 'P'
        elif d == 0:
            r = 'E'
        else:
            hijos = [val(w, d - 1) for w in suc[v]]
            r = 'G' if 'P' in hijos else ('P' if all(h == 'G' for h in hijos) else 'E')
        memo[(v, d)] = r
        return r
    return [val(v, 2 * n + 2) for v in range(n)]


def pruebas():
    random.seed(4040)

    # Casos borde
    assert tabla_sustraccion(0, [1]) == [False]
    assert juego_en_grafo(1, []) == ['P'] and juego_en_grafo(1, [(0, 0)]) == ['E']
    assert juego_en_grafo(2, [(0, 1), (1, 0)]) == ['E', 'E']
    assert extremos([]) == 0 and extremos([7]) == 7 and extremos([2, 2]) == 0

    for _ in range(300):
        movs = random.sample(range(1, 7), random.randint(1, 3))
        N = random.randint(0, 25)
        assert tabla_sustraccion(N, movs) == [_sustraccion_bruta(n, movs) for n in range(N + 1)]

    for _ in range(300):
        a = [random.randint(-5, 10) for _ in range(random.randint(0, 10))]
        assert extremos(a) == _extremos_bruto(a)

    for _ in range(400):
        n = random.randint(1, 8)
        aristas = list({(random.randrange(n), random.randrange(n))
                        for _ in range(random.randint(0, 2 * n))})
        assert juego_en_grafo(n, aristas) == _grafo_bruto(n, aristas)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
