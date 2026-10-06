"""
Programación dinámica — Subsecuencia común más larga («Longest Common Subsequence», LCS)
Nivel: Básico
Ejecutar: python lcs.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Dadas dos secuencias a y b, encontrar la secuencia más larga que es
    subsecuencia de ambas (se pueden saltar elementos pero no reordenar), y
    mostrarla.
    Señales: «comparar dos textos / ADN / órdenes», «mínimo de borrados para
    que dos cadenas queden iguales» (= |a| + |b| - 2·LCS), «diff», «la
    secuencia más corta que contiene a ambas» (= |a| + |b| - LCS).
    Tamaños: |a|·|b| ≤ ~10^7 en Python.

FUNCIÓN
    lcs(a, b) -> str | list
        Una LCS de a y b (cadena si a es cadena; lista si no).
    lcs_longitud(a, b) -> int
        Solo el largo, con memoria O(|b|) (dos filas).

IDEA Y ALGORITMO
    ESTADO      dp[i][j] = largo de la LCS de los prefijos a[:i] y b[:j].
    TRANSICIÓN  si a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] + 1
                si no:              dp[i][j] = max(dp[i-1][j], dp[i][j-1]).
    CASOS BASE  dp[0][j] = dp[i][0] = 0 (un prefijo vacío no comparte nada).
    ORDEN       i creciente y, dentro, j creciente (cada casilla usa la de
                arriba, la de la izquierda y la diagonal).
    RESPUESTA   dp[n][m].
    Por qué: si los últimos caracteres coinciden, hay una LCS óptima que
    los empareja (si una LCS no usa a[i-1], se puede cambiar su último
    elemento emparejado por este). Si no coinciden, al menos uno de los dos
    no participa: se descarta a[i-1] o b[j-1] y se toma lo mejor.
    Reconstrucción (retroceder sobre la tabla): desde (n, m): si
    a[i-1] == b[j-1] ese carácter va en la LCS y se pasa a (i-1, j-1); si
    no, se va hacia el vecino (arriba o izquierda) que tenga el valor dp[i][j].
    Se recogen los caracteres al revés y se invierte.

MACROALGORITMO
    1. Tabla (n+1) × (m+1) en ceros.
    2. Llenar fila por fila con la transición.
    3. i, j = n, m; mientras i > 0 y j > 0: si coinciden, guardar y bajar en
       diagonal; si no, moverse hacia el vecino con mayor dp.
    4. Invertir lo guardado.

COMPLEJIDAD
    Tiempo O(n · m). Memoria O(n · m) para reconstruir, O(m) si solo se
    necesita el largo. n = m = 3000 (9·10^6 casillas) es ~2–4 s en Python
    puro: cuidado. (Hirschberg reconstruye con memoria O(m).)

EJEMPLO A MANO
    a = "ABCBDAB", b = "BDCABA"
          ""  B  D  C  A  B  A
      ""   0  0  0  0  0  0  0
      A    0  0  0  0  1  1  1
      B    0  1  1  1  1  2  2
      C    0  1  1  2  2  2  2
      B    0  1  1  2  2  3  3
      D    0  1  2  2  2  3  3
      A    0  1  2  2  3  3  4
      B    0  1  2  2  3  4  4      -> largo 4, por ejemplo "BCBA".

ERRORES TÍPICOS
    - Confundir subsecuencia (salteada) con subcadena (contigua): la
      subcadena común más larga usa dp[i][j] = dp[i-1][j-1] + 1 o 0.
    - Índices corridos: dp tiene un tamaño (n+1)×(m+1) y el carácter de la
      fila i es a[i-1].
    - Reconstruir con un desempate que no respeta la tabla (ir a un vecino
      con valor menor a dp[i][j] cuando no coinciden).
    - Recursión top-down con n = m = 1000: un millón de estados y
      profundidad 2000; mejor bottom-up.

VARIANTES Y RELACIONADOS
    - distancia_edicion.py (misma tabla con costos), lis.py (LCS de una
      permutación con 1..n = LIS), reconstruccion_solucion.py.
    - LCS lexicográficamente menor, contar LCS distintas, LCS de 3 cadenas
      (tabla 3D).

DÓNDE PRACTICAR
    - Externos: UVa 10405 «Longest Common Subsequence»; UVa 531 «Compromise»
      (reconstrucción con palabras); AtCoder Educational DP Contest F «LCS».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las subsecuencias de a,
      |a| ≤ 10) en 800 casos aleatorios + casos borde; se valida que la
      respuesta sea subsecuencia de ambas (python lcs.py)
"""
import random


def lcs(a, b):
    """Una subsecuencia común más larga de a y b (str si a es str; si no, lista)."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]      # fila y columna 0: casos base
    for i in range(1, n + 1):
        ai, fila, ant = a[i - 1], dp[i], dp[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                fila[j] = ant[j - 1] + 1               # emparejar los últimos
            else:
                fila[j] = ant[j] if ant[j] >= fila[j - 1] else fila[j - 1]
    res, i, j = [], n, m
    while i > 0 and j > 0:                           # retroceder sobre la tabla
        if a[i - 1] == b[j - 1]:
            res.append(a[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1                                   # a[i-1] no participa
        else:
            j -= 1                                   # b[j-1] no participa
    res.reverse()
    return "".join(res) if isinstance(a, str) else res


def lcs_longitud(a, b):
    """Largo de la LCS con dos filas (memoria O(|b|))."""
    m = len(b)
    ant = [0] * (m + 1)
    for x in a:
        fila = [0] * (m + 1)
        for j in range(1, m + 1):
            if x == b[j - 1]:
                fila[j] = ant[j - 1] + 1
            else:
                fila[j] = max(ant[j], fila[j - 1])
        ant = fila
    return ant[m]


def demo():
    a, b = "ABCBDAB", "BDCABA"
    print(f"lcs({a!r}, {b!r}) = {lcs(a, b)!r}, largo {lcs_longitud(a, b)}")   # largo 4
    print("con listas:", lcs([1, 2, 3, 4, 1], [3, 4, 1, 2, 1, 3]))           # largo 3 ([1, 2, 3])


def pruebas():
    random.seed(10405)

    def es_subsecuencia(s, t):
        it = iter(t)
        return all(c in it for c in s)

    def bruta(a, b):
        n, mejor = len(a), 0
        for mask in range(1 << n):
            s = [a[i] for i in range(n) if mask >> i & 1]
            if len(s) > mejor and es_subsecuencia(s, b):
                mejor = len(s)
        return mejor

    # Casos borde
    assert lcs("", "abc") == "" and lcs("abc", "") == ""
    assert lcs("abc", "abc") == "abc"
    assert lcs("abc", "xyz") == ""
    assert lcs("aaaa", "aa") == "aa"
    assert lcs([], [1]) == []

    for _ in range(800):
        alfabeto = random.choice(["ab", "abc", "abcd"])
        a = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 10)))
        b = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 10)))
        s = lcs(a, b)
        assert len(s) == bruta(a, b) == lcs_longitud(a, b)
        assert es_subsecuencia(s, a) and es_subsecuencia(s, b)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
