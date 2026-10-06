"""
Programación dinámica — Distancia de edición («Levenshtein distance / edit distance»)
Nivel: Básico
Ejecutar: python distancia_edicion.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Mínimo número de operaciones para convertir la cadena a en la cadena b,
    donde cada operación es INSERTAR un carácter, BORRAR uno o CAMBIAR uno
    por otro (cada una cuesta 1). Además, mostrar qué operaciones hacer.
    Señales: «mínimo de cambios / correcciones / mutaciones», «qué tan
    parecidas son dos palabras», corrector ortográfico, ADN con
    inserciones y borrados. |a|·|b| ≤ ~10^7 en Python.

FUNCIÓN
    distancia_edicion(a, b) -> int
    operaciones_edicion(a, b) -> (int, list)
        Distancia y lista de operaciones, en orden, para aplicar sobre a:
          ("insertar", pos, c)        insertar c en la posición pos
          ("borrar", pos, c)          borrar el carácter c de la posición pos
          ("cambiar", pos, c, d)      cambiar c por d en la posición pos
        pos se refiere a la cadena tal como va quedando (índices desde 0).
    aplicar(a, ops) -> str            aplica la lista (sirve para comprobar).

IDEA Y ALGORITMO
    ESTADO      dp[i][j] = distancia entre los prefijos a[:i] y b[:j].
    TRANSICIÓN  mirar qué pasa con el ÚLTIMO carácter:
                dp[i][j] = min( dp[i-1][j] + 1,                (borrar a[i-1])
                                dp[i][j-1] + 1,                (insertar b[j-1])
                                dp[i-1][j-1] + [a[i-1] ≠ b[j-1]] ) (cambiar o
                                                                  dejar igual)
    CASOS BASE  dp[i][0] = i (borrar todo), dp[0][j] = j (insertar todo).
    ORDEN       i creciente, j creciente.
    RESPUESTA   dp[n][m].
    Por qué: en una edición óptima, el último carácter de b o viene de
    a[i-1] (igual o cambiado) o fue insertado, o a[i-1] fue borrado; los
    tres casos dejan un subproblema de prefijos más cortos.
    Reconstrucción: retroceder desde (n, m) eligiendo una transición que
    explique el valor de dp[i][j]; eso da las operaciones de derecha a
    izquierda. Se invierten y se recorren de izquierda a derecha con un
    contador pos de la cadena actual: igual/cambiar -> pos += 1;
    insertar -> pos += 1; borrar -> pos no avanza.

MACROALGORITMO
    1. Tabla (n+1) × (m+1) con los casos base en la fila y columna 0.
    2. Llenar con el mínimo de las tres transiciones.
    3. Retroceder desde (n, m) anotando la operación usada en cada paso.
    4. Invertir y calcular las posiciones sobre la cadena que va cambiando.

COMPLEJIDAD
    Tiempo O(n · m); memoria O(n · m) con reconstrucción, O(m) sin ella.
    En Python ~3–5·10^6 casillas por segundo.

EJEMPLO A MANO
    a = "kitten", b = "sitting":
      cambiar k->s (pos 0): "sitten"; cambiar e->i (pos 4): "sittin";
      insertar g (pos 6): "sitting".   Distancia 3.
    Tabla de "sol" -> "sal": dp[3][3] = dp[2][2] + 0 = (dp[1][1] + 1) = 1.

ERRORES TÍPICOS
    - Casos base en 0 en vez de i y j.
    - Sumar 1 en la diagonal aunque los caracteres sean iguales.
    - Reconstruir con posiciones de la cadena ORIGINAL cuando las
      operaciones se aplican en orden (las inserciones/borrados corren los
      índices).
    - Costos distintos por operación: generalizar los +1, no cambia la idea.

VARIANTES Y RELACIONADOS
    - Damerau (agrega transposición de vecinos), costos ponderados,
      alineamiento de secuencias (Needleman–Wunsch).
    - Solo inserciones y borrados: |a| + |b| - 2·LCS (lcs.py).
    - Versión bit-paralela de Myers para cadenas largas.
    - reconstruccion_solucion.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/M - Byte Flu (distancia de edición, versión
      bit-paralela de Myers, + corte mínimo).
    - Externos: CSES «Edit Distance»; UVa 526 «String Distance and Transform
      Process» (pide la lista de operaciones).

VERIFICACIÓN
    - Pruebas: OK contra BFS sobre cadenas (fuerza bruta: búsqueda en
      anchura aplicando todas las operaciones posibles) en 400 casos
      aleatorios + casos borde; se aplica la lista de operaciones y se
      comprueba que da b (python distancia_edicion.py)
"""
import random
from collections import deque


def _tabla(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i                        # borrar los i caracteres
    for j in range(m + 1):
        dp[0][j] = j                        # insertar los j caracteres
    for i in range(1, n + 1):
        ai, fila, ant = a[i - 1], dp[i], dp[i - 1]
        for j in range(1, m + 1):
            fila[j] = min(ant[j] + 1,                       # borrar a[i-1]
                          fila[j - 1] + 1,                  # insertar b[j-1]
                          ant[j - 1] + (ai != b[j - 1]))    # cambiar / igual
    return dp


def distancia_edicion(a, b):
    """Mínimo de inserciones, borrados y cambios para pasar de a a b."""
    return _tabla(a, b)[len(a)][len(b)]


def operaciones_edicion(a, b):
    """(distancia, operaciones en orden) para transformar a en b."""
    dp = _tabla(a, b)
    i, j = len(a), len(b)
    pasos = []                              # de derecha a izquierda
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            pasos.append(("igual",) if a[i - 1] == b[j - 1] else ("cambiar", a[i - 1], b[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            pasos.append(("borrar", a[i - 1]))
            i -= 1
        else:                               # necesariamente dp[i][j] == dp[i][j-1] + 1
            pasos.append(("insertar", b[j - 1]))
            j -= 1
    pasos.reverse()
    ops, pos = [], 0                        # pos: índice en la cadena que va cambiando
    for p in pasos:
        if p[0] == "igual":
            pos += 1
        elif p[0] == "cambiar":
            ops.append(("cambiar", pos, p[1], p[2]))
            pos += 1
        elif p[0] == "insertar":
            ops.append(("insertar", pos, p[1]))
            pos += 1
        else:
            ops.append(("borrar", pos, p[1]))   # pos no avanza: el resto se corre
    return dp[len(a)][len(b)], ops


def aplicar(a, ops):
    """Aplica en orden las operaciones devueltas por operaciones_edicion."""
    s = list(a)
    for op in ops:
        if op[0] == "insertar":
            s.insert(op[1], op[2])
        elif op[0] == "borrar":
            assert s[op[1]] == op[2]
            del s[op[1]]
        else:
            assert s[op[1]] == op[2]
            s[op[1]] = op[3]
    return "".join(s)


def demo():
    a, b = "kitten", "sitting"
    d, ops = operaciones_edicion(a, b)
    print(f"{a} -> {b}: distancia {d}")                      # 3
    s = a
    for op in ops:
        s = aplicar(s, [op])
        print("  ", op, "->", s)


def pruebas():
    random.seed(526)

    def bfs(a, b):
        """Fuerza bruta: BFS sobre cadenas de largo ≤ max(|a|, |b|)."""
        alfabeto = sorted(set(a) | set(b))
        tope = max(len(a), len(b))
        dist = {a: 0}
        cola = deque([a])
        while cola:
            s = cola.popleft()
            if s == b:
                return dist[s]
            vecinos = []
            for p in range(len(s)):
                vecinos.append(s[:p] + s[p + 1:])
                for c in alfabeto:
                    vecinos.append(s[:p] + c + s[p + 1:])
            if len(s) < tope:
                for p in range(len(s) + 1):
                    for c in alfabeto:
                        vecinos.append(s[:p] + c + s[p:])
            for t in vecinos:
                if t not in dist:
                    dist[t] = dist[s] + 1
                    cola.append(t)

    # Casos borde
    assert distancia_edicion("", "") == 0
    assert distancia_edicion("abc", "") == 3 and distancia_edicion("", "ab") == 2
    assert distancia_edicion("same", "same") == 0
    assert distancia_edicion("kitten", "sitting") == 3
    assert distancia_edicion("sunday", "saturday") == 3

    for _ in range(400):
        alfabeto, tope = random.choice([("ab", 5), ("abc", 4)])
        a = "".join(random.choice(alfabeto) for _ in range(random.randint(0, tope)))
        b = "".join(random.choice(alfabeto) for _ in range(random.randint(0, tope)))
        d, ops = operaciones_edicion(a, b)
        assert d == bfs(a, b) == distancia_edicion(a, b)
        assert len(ops) == d and aplicar(a, ops) == b

    # Más largas: la lista de operaciones siempre reconstruye b
    for _ in range(100):
        a = "".join(random.choice("abcd") for _ in range(random.randint(0, 25)))
        b = "".join(random.choice("abcd") for _ in range(random.randint(0, 25)))
        d, ops = operaciones_edicion(a, b)
        assert len(ops) == d and aplicar(a, ops) == b
        assert d >= abs(len(a) - len(b)) and d <= max(len(a), len(b))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
