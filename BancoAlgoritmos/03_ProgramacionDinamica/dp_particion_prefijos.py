"""
Programación dinámica — Partición en piezas sobre prefijos («Word break / partition DP»)
Nivel: Intermedio
Ejecutar: python dp_particion_prefijos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Partir una cadena (o un arreglo) en pedazos CONTIGUOS que cumplan alguna
    condición, y decir si se puede, de cuántas formas, o con el mínimo /
    máximo de algo. Ejemplos:
      - «Word break»: separar un texto sin espacios en palabras de un
        diccionario (mostrar una forma y contar cuántas hay).
      - Partir una cadena en el mínimo número de palíndromos.
    Señales: «dividir / tokenizar / segmentar / cortar en bloques
    consecutivos», «cada pedazo debe ser…», n ≤ ~10^4–10^5 si las piezas
    son cortas (≤ L), n ≤ ~3000 si pueden ser largas (O(n²)).

FUNCIÓN
    segmentar(s, diccionario) -> list | None
        Una partición de s en palabras del diccionario, o None.
    contar_segmentaciones(s, diccionario, mod=None) -> int
    min_palindromos(s) -> (int, list)
        Mínimo número de piezas palíndromas y una partición que lo logra.

IDEA Y ALGORITMO
    Patrón general (todas las variantes):
      ESTADO      dp[i] = respuesta para el PREFIJO s[:i] (los primeros i
                  caracteres ya están partidos).
      TRANSICIÓN  la última pieza es s[j:i] (j < i) y debe ser válida:
                  dp[i] = combinar sobre j válidos de dp[j] (OR para «¿se
                  puede?», + para contar, min/max + costo para optimizar).
      CASO BASE   dp[0] = verdadero / 1 / 0 (el prefijo vacío ya está partido).
      ORDEN       i creciente.
      RESPUESTA   dp[n]; para mostrar la partición se guarda desde[i] = el j
                  usado y se retrocede desde n.
    Por qué: en cualquier partición, quitar la última pieza deja una
    partición del prefijo; y las particiones con distinta última pieza son
    distintas (por eso se suman al contar).
    Hacerlo rápido: no probar todos los j, sino solo las piezas posibles:
      - Diccionario: probar solo los LARGOS que existen en el diccionario
        (o recorrer un trie desde j) -> O(n · #largos · L).
      - Palíndromos: precalcular pal[j][i] («s[j..i] es palíndromo») en
        O(n²) con pal[j][i] = s[j] == s[i] and pal[j+1][i-1]; luego cada
        transición es O(1) y el total O(n²).

MACROALGORITMO
    1. Precalcular cómo saber rápido si s[j:i] es una pieza válida.
    2. dp[0] = caso base.
    3. Para i = 1..n: para cada j con s[j:i] válida, combinar dp[j] en
       dp[i] (guardar desde[i] = j si mejora).
    4. Respuesta dp[n]; retroceder con desde[] para mostrar las piezas.

COMPLEJIDAD
    Diccionario: O(n · #largos · L) (el corte s[j:i] cuesta L). Palíndromos:
    O(n²) tiempo y memoria; n = 2000 en ~1 s en Python.

EJEMPLO A MANO
    s = "catsanddog", dic = {cat, cats, and, sand, dog}
      dp[0]=1; dp[3]=1 (cat); dp[4]=1 (cats); dp[7]: «sand» desde 3 y «and»
      desde 4 -> 2; dp[10]: «dog» desde 7 -> 2.  -> 2 formas:
      cat sand dog / cats and dog.
    s = "aab": min_palindromos = 2 ("aa", "b").

ERRORES TÍPICOS
    - Índices: dp tiene n+1 casillas; la pieza que termina en i es s[j:i].
    - Probar todos los j con un corte s[j:i] cada vez: O(n² · n) sin querer.
    - Contar sin módulo: el número de particiones crece exponencialmente.
    - Olvidar dp[0] = 1 al contar (todo queda en 0).

VARIANTES Y RELACIONADOS
    - Partir un arreglo en exactamente K grupos (agregar el número de
      grupos al estado): dp_divide_venceras.py, optimizacion_knuth.py.
    - Decodificaciones de dígitos a letras (piezas de 1 o 2 dígitos).
    - Tokenizar maximizando puntaje con un trie (Spacebar Tokenizer).
    - reconstruccion_solucion.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/E - Spacebar Tokenizer (DP sobre prefijos + trie).
    - ICPC/Colombia 2026/E - Custom Keypad (DP de partición en B bloques
      contiguos + reconstrucción con desempate).
    - Externos: CSES «Word Combinations» (contar, con trie).

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las 2^(n-1) formas de cortar,
      n ≤ 12) en 600 casos aleatorios + casos borde (python dp_particion_prefijos.py)
"""
import random


def segmentar(s, diccionario):
    """Una partición de s en palabras del diccionario (lista) o None."""
    palabras = set(diccionario)
    largos = sorted({len(w) for w in palabras if w})
    n = len(s)
    desde = [-1] * (n + 1)              # desde[i] = inicio de la última palabra de s[:i]
    puede = [False] * (n + 1)
    puede[0] = True                     # prefijo vacío: ya está partido
    for i in range(1, n + 1):
        for L in largos:
            j = i - L
            if j < 0:
                break
            if puede[j] and s[j:i] in palabras:
                puede[i], desde[i] = True, j
                break
    if not puede[n]:
        return None
    piezas, i = [], n
    while i > 0:
        piezas.append(s[desde[i]:i])
        i = desde[i]
    return piezas[::-1]


def contar_segmentaciones(s, diccionario, mod=None):
    """Número de formas de partir s en palabras del diccionario."""
    palabras = set(diccionario)
    largos = sorted({len(w) for w in palabras if w})
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        total = 0
        for L in largos:
            j = i - L
            if j < 0:
                break
            if dp[j] and s[j:i] in palabras:
                total += dp[j]          # última palabra s[j:i]
        dp[i] = total % mod if mod else total
    return dp[n]


def min_palindromos(s):
    """(mínimo de piezas palíndromas, una partición óptima)."""
    n = len(s)
    # pal[j][i]: s[j..i] (inclusive) es palíndromo. j decreciente para tener pal[j+1][i-1].
    pal = [[False] * n for _ in range(n)]
    for j in range(n - 1, -1, -1):
        for i in range(j, n):
            pal[j][i] = s[j] == s[i] and (i - j < 2 or pal[j + 1][i - 1])
    INF = float("inf")
    dp = [0] + [INF] * n                # dp[i]: mínimo de piezas para s[:i]
    desde = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(i):
            if pal[j][i - 1] and dp[j] + 1 < dp[i]:
                dp[i], desde[i] = dp[j] + 1, j
    piezas, i = [], n
    while i > 0:
        piezas.append(s[desde[i]:i])
        i = desde[i]
    return dp[n], piezas[::-1]


def demo():
    s, dic = "catsanddog", ["cat", "cats", "and", "sand", "dog"]
    print(f"segmentar({s!r}) ->", segmentar(s, dic))
    print("formas ->", contar_segmentaciones(s, dic))                 # 2
    print("min_palindromos('aab') ->", min_palindromos("aab"))         # (2, ['aa', 'b'])
    print("min_palindromos('ababbbabbababa') ->", min_palindromos("ababbbabbababa"))  # 4 piezas


def pruebas():
    random.seed(1527)

    def particiones(s):
        n = len(s)
        if n == 0:
            yield []
            return
        for mask in range(1 << (n - 1)):
            piezas, ini = [], 0
            for b in range(n - 1):
                if mask >> b & 1:
                    piezas.append(s[ini:b + 1])
                    ini = b + 1
            piezas.append(s[ini:])
            yield piezas

    # Casos borde
    assert segmentar("", ["a"]) == [] and contar_segmentaciones("", ["a"]) == 1
    assert segmentar("abc", []) is None and contar_segmentaciones("abc", []) == 0
    assert min_palindromos("") == (0, [])
    assert min_palindromos("x") == (1, ["x"])
    assert min_palindromos("abba") == (1, ["abba"])
    assert contar_segmentaciones("a" * 40, ["a", "aa"]) == 165580141   # Fibonacci(41)

    for _ in range(600):
        alfabeto = random.choice(["ab", "abc"])
        s = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 12)))
        dic = list({"".join(random.choice(alfabeto) for _ in range(random.randint(1, 3)))
                    for _ in range(random.randint(0, 6))})
        validas = [p for p in particiones(s) if all(x in dic for x in p)]
        assert contar_segmentaciones(s, dic) == len(validas)
        assert contar_segmentaciones(s, dic, 5) == len(validas) % 5
        seg = segmentar(s, dic)
        if validas:
            assert seg is not None and "".join(seg) == s and all(x in dic for x in seg)
        else:
            assert seg is None
        mejor = min(len(p) for p in particiones(s) if all(x == x[::-1] for x in p))
        k, piezas = min_palindromos(s)
        assert k == mejor == len(piezas)
        assert "".join(piezas) == s and all(x == x[::-1] and x for x in piezas)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
