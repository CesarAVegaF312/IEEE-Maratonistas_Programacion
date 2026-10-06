"""
Cadenas — Rotación mínima (Booth / dos punteros) y factorización de Lyndon (Duval)
          («Lexicographically minimal string rotation», «Lyndon factorization»)
Nivel: Avanzado
Ejecutar: python rotacion_minima.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Para una cadena CIRCULAR (collar, huella, polígono descrito por su
    secuencia de lados) da su representante canónico: la rotación
    lexicográficamente menor, en O(n). Dos cadenas circulares son la misma
    ⇔ sus rotaciones mínimas son iguales, así que sirve para deduplicar o
    agrupar con un set/dict.
    La factorización de Lyndon parte s en palabras de Lyndon no crecientes;
    es la base de Duval (otro método de rotación mínima) y de la
    generación de secuencias de De Bruijn.
    Señales en el enunciado: «cadena circular», «collar», «ABCD, BCDA y
    CDAB son la misma», «representante canónico / forma normal», «iguales
    salvo rotación».

FUNCIÓN
    rotacion_minima(s) -> int
        Menor índice i tal que s[i:] + s[:i] es la rotación mínima (dos
        punteros, «algoritmo de la representación mínima»). s vacía → 0.
    booth(s) -> int
        Algoritmo de Booth (1980, función de falla tipo KMP sobre s+s):
        un índice de la rotación mínima.
    factorizacion_lyndon(s) -> list
        Duval: s = w1 w2 … wk con cada wi de Lyndon y w1 ≥ w2 ≥ … ≥ wk.
    rotacion_minima_duval(s) -> int     menor índice, vía Duval sobre s+s
    es_lyndon(s) -> bool                no vacía y estrictamente menor que
                                        todas sus rotaciones propias
    Sirven para str o list.

IDEA Y ALGORITMO
    Dos punteros: i < j son dos candidatos de inicio y k cuántos caracteres
    coinciden ya: s[i..i+k-1] == s[j..j+k-1] (índices módulo n).
      - Si s[i+k] == s[j+k], k += 1.
      - Si s[i+k] > s[j+k], ninguna rotación que empiece en i, i+1, …, i+k
        es la mínima: la que empieza en i+t pierde contra la que empieza en
        j+t (comparten k-t letras y luego la de j+t es menor). Saltar
        i = i + k + 1. Simétrico si s[j+k] > s[i+k]. Si quedan iguales,
        j += 1. Reiniciar k = 0.
      - Termina cuando un puntero pasa n (descartó todo) o k == n (las dos
        rotaciones son iguales: s es periódica). La respuesta es min(i, j).
    Cada paso aumenta i + j + k, que no pasa de 3n: O(n).
    Booth: calcula una función de falla sobre s+s mientras mantiene k = el
    mejor inicio visto; cuando una comparación muestra algo menor, mueve k.
    Duval: s es de Lyndon si es estrictamente menor que todos sus sufijos
    propios. Se recorre manteniendo un prefijo de la forma w^p w' (w de
    Lyndon, w' prefijo de w): con j el carácter nuevo y k su «gemelo»
    en w, si s[k] == s[j] se sigue la periodicidad, si s[k] < s[j] el
    bloque entero pasa a ser un solo Lyndon (k vuelve al inicio), y si
    s[k] > s[j] se emiten las p copias de w como factores. Lineal.
    Rotación mínima vía Duval: el inicio del último factor de Lyndon de s+s
    que empieza en la primera mitad.
    Ingenuo: min(s[i:] + s[:i] for i in range(n)) es O(n²): con n = 5000 y
    100 cadenas ya son 2,5·10^9 operaciones de copia.

MACROALGORITMO
    1. i = 0, j = 1, k = 0.
    2. Mientras i < n, j < n, k < n: a = s[(i+k) % n], b = s[(j+k) % n].
    3. Si a == b: k += 1 y seguir.
    4. Si a > b: i += k + 1; si no: j += k + 1. Si i == j: j += 1. k = 0.
    5. Respuesta: min(i, j). Rotación: s[r:] + s[:r].
    6. Duval: i = 0; mientras i < n: j = i+1, k = i; mientras j < n y
       s[k] ≤ s[j]: k = i si s[k] < s[j], si no k += 1; j += 1. Luego
       emitir bloques de largo j - k mientras i ≤ k.

COMPLEJIDAD
    Todo O(n) en tiempo; O(1) extra (dos punteros, Duval) u O(n) (Booth).
    En Python, n = 10^6 en ~0,5 s con los dos punteros (Duval, ~0,3 s).

EJEMPLO A MANO
    s = "baca" (rotaciones: baca, acab, caba, abac → mínima "abac", i = 3)
      i=0 j=1 k=0: 'b' > 'a' → i = 1 → i == j → j = 2
      i=1 j=2 k=0: 'a' < 'c' → j = 3
      i=1 j=3: k=0 'a' = 'a' → k=1: 'c' > 'b' (s[0]) → i = 1+2 = 3 → j = 4
      j = n → respuesta min(3, 4) = 3 → "abac"
    factorizacion_lyndon("banana") = [b, an, an, a]   (b ≥ an ≥ an ≥ a)

ERRORES TÍPICOS
    - Saltar solo i += 1 en vez de i += k + 1: pasa a O(n²) en "aaa…ab".
    - Olvidar el caso i == j (comparar una rotación consigo misma).
    - No parar cuando k == n: con s periódica ("abab") el ciclo no termina.
    - Comparar huellas por igualdad de la rotación sin normalizar ambas
      (o normalizar una sola).
    - Nombres: mucho material en español llama «Booth» al método de dos
      punteros; el Booth original usa función de falla. Ambos están aquí y
      dan la misma rotación.

VARIANTES Y RELACIONADOS
    - Rotación MÁXIMA: invertir las comparaciones.
    - ¿B es rotación de A?: |A| == |B| y B aparece en A+A (kmp.py), o
      comparar rotaciones mínimas.
    - Contar collares distintos: lema de Burnside / Pólya.
    - Palabras de Lyndon y secuencias de De Bruijn: de_bruijn.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/F - Fingerprints (representante canónico de
      huellas circulares con la rotación mínima de dos punteros)
    - CSES «Minimal Rotation»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (generar todas las rotaciones; Lyndon
      por definición y factorización por «prefijo de Lyndon más largo») en
      3000 casos aleatorios + casos borde (python rotacion_minima.py)
"""
import random


def rotacion_minima(s):
    """Menor índice de inicio de la rotación lexicográficamente mínima (dos punteros)."""
    n = len(s)
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        a, b = s[(i + k) % n], s[(j + k) % n]
        if a == b:
            k += 1
            continue
        # El que tiene la letra mayor pierde, y con él los k siguientes inicios.
        if a > b:
            i += k + 1
        else:
            j += k + 1
        if i == j:
            j += 1
        k = 0
    return min(i, j) if n else 0


def booth(s):
    """Algoritmo de Booth (función de falla sobre s+s): índice de la rotación mínima."""
    n = len(s)
    if n == 0:
        return 0
    f = [-1] * (2 * n)      # función de falla de la rotación candidata que empieza en k
    k = 0                   # mejor inicio encontrado hasta ahora
    for j in range(1, 2 * n):
        c = s[j % n]
        i = f[j - k - 1]
        while i != -1 and c != s[(k + i + 1) % n]:
            if c < s[(k + i + 1) % n]:
                k = j - i - 1       # apareció un inicio menor
            i = f[i]
        if i == -1 and c != s[(k + i + 1) % n]:
            if c < s[(k + i + 1) % n]:
                k = j
            f[j - k] = -1
        else:
            f[j - k] = i + 1
    return k


def factorizacion_lyndon(s):
    """Duval: lista de factores de Lyndon no crecientes cuya concatenación es s."""
    n = len(s)
    res = []
    i = 0
    while i < n:
        # Invariante: s[i:j] = w^p w' con w de Lyndon de largo j - k.
        j, k = i + 1, i
        while j < n and s[k] <= s[j]:
            if s[k] < s[j]:
                k = i               # todo s[i..j] es ahora un único Lyndon
            else:
                k += 1              # sigue la periodicidad
            j += 1
        while i <= k:               # emitir las copias completas de w
            res.append(s[i:i + j - k])
            i += j - k
    return res


def rotacion_minima_duval(s):
    """Inicio del último factor de Lyndon de s+s que empieza en la primera mitad."""
    n = len(s)
    t = s + s
    i = ans = 0
    while i < n:
        ans = i
        j, k = i + 1, i
        while j < 2 * n and t[k] <= t[j]:
            k = i if t[k] < t[j] else k + 1
            j += 1
        while i <= k:
            i += j - k
    return ans


def es_lyndon(s):
    """Estrictamente menor que todas sus rotaciones propias ⇔ un solo factor de Lyndon."""
    return len(s) > 0 and len(factorizacion_lyndon(s)) == 1


def demo():
    s = "baca"
    r = rotacion_minima(s)
    print("s =", s, "→ rotacion_minima =", r, "→", s[r:] + s[:r])   # 3 abac
    print("booth:", booth(s), " duval:", rotacion_minima_duval(s))   # 3 3
    print("factorizacion_lyndon('banana'):", factorizacion_lyndon("banana"))  # ['b', 'an', 'an', 'a']
    print("es_lyndon('aab'):", es_lyndon("aab"), " es_lyndon('abab'):", es_lyndon("abab"))  # True False
    huellas = ["ABCD", "CDAB", "BCDA", "ACBD"]
    canon = []
    for h in huellas:
        r = rotacion_minima(h)
        if h[r:] + h[:r] not in canon:
            canon.append(h[r:] + h[:r])
    print("huellas", huellas, "→ distintas:", canon)                # ['ABCD', 'ACBD']


def pruebas():
    random.seed(2025)

    def lyndon_bruto(w):
        return len(w) > 0 and all(w < w[i:] + w[:i] for i in range(1, len(w)))

    def factorizacion_bruta(s):
        # El primer factor es el prefijo de Lyndon más largo.
        res = []
        while s:
            L = max(L for L in range(1, len(s) + 1) if lyndon_bruto(s[:L]))
            res.append(s[:L])
            s = s[L:]
        return res

    # Casos borde
    assert rotacion_minima("") == booth("") == rotacion_minima_duval("") == 0
    assert factorizacion_lyndon("") == [] and not es_lyndon("")
    assert rotacion_minima("a") == 0 and factorizacion_lyndon("a") == ["a"]
    assert rotacion_minima("aaaa") == 0 and rotacion_minima("abab") == 0
    assert rotacion_minima("ba") == 1
    assert factorizacion_lyndon("aaa") == ["a", "a", "a"]
    assert rotacion_minima([3, 1, 2]) == 1                 # también con listas

    for _ in range(3000):
        alfabeto = random.choice(["a", "ab", "abc", "abcd"])
        s = "".join(random.choice(alfabeto) for _ in range(random.randint(1, 14)))
        n = len(s)
        rots = [s[i:] + s[:i] for i in range(n)]
        minima = min(rots)
        primero = rots.index(minima)
        assert rotacion_minima(s) == primero
        assert rotacion_minima_duval(s) == primero
        b = booth(s)
        assert 0 <= b < n and rots[b] == minima
        f = factorizacion_lyndon(s)
        assert "".join(f) == s
        assert all(lyndon_bruto(w) for w in f)
        assert all(f[t] >= f[t + 1] for t in range(len(f) - 1))
        assert f == factorizacion_bruta(s)
        assert es_lyndon(s) == lyndon_bruto(s)

    # Grande: peor caso para el salto i += 1 ("aaa…ab")
    s = "a" * 200000 + "b" + "a" * 199999
    assert rotacion_minima(s) == 200001
    s = "".join(random.choice("ab") for _ in range(200000))
    r = rotacion_minima(s)
    assert r == rotacion_minima_duval(s)
    b = booth(s)
    assert s[b:] + s[:b] == s[r:] + s[:r]


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
