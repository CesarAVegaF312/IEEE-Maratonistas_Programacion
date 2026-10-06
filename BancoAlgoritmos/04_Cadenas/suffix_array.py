"""
Cadenas — Arreglo de sufijos + LCP de Kasai («Suffix array, prefix doubling + Kasai»)
Nivel: Avanzado
Ejecutar: python suffix_array.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    El arreglo de sufijos es la lista de posiciones de inicio de todos los
    sufijos de s, ordenados lexicográficamente. Junto con el arreglo LCP
    (prefijo común entre sufijos vecinos en ese orden) responde casi todo
    sobre subcadenas: cuántas subcadenas distintas hay, la subcadena
    repetida más larga, cuántas veces aparece un patrón (búsqueda binaria),
    la k-ésima subcadena en orden, subcadena común más larga de dos textos.
    Señales en el enunciado: «subcadenas distintas», «aparece al menos dos
    / k veces», «la k-ésima subcadena en orden lexicográfico», n hasta 10^5.

FUNCIÓN
    arreglo_sufijos(s) -> list[int]
        sa[r] = inicio del r-ésimo sufijo en orden (sa es permutación de 0..n-1).
    lcp_kasai(s, sa) -> list[int]
        lcp[r] = prefijo común de los sufijos sa[r-1] y sa[r]; lcp[0] = 0.
    subcadenas_distintas(s) -> int          n(n+1)/2 - Σ lcp (sin contar la vacía)
    contar_apariciones(s, sa, patron) -> int   O(|patron|·log n); patrón vacío → n
    repetida_mas_larga(s) -> str
        La subcadena más larga que aparece ≥ 2 veces (solapadas valen);
        en empate, la menor lexicográficamente; "" si no hay.

IDEA Y ALGORITMO
    Doblado de prefijos (prefix doubling): rango_k[i] = posición de s[i:i+k]
    entre todas las subcadenas de largo k (iguales → mismo rango). Si se
    conocen los rangos para largo k, el orden para largo 2k sale ordenando
    por el PAR (rango_k[i], rango_k[i+k]): comparar s[i:i+2k] es comparar
    primero la mitad izquierda y, si empata, la derecha. Un sufijo que no
    tiene mitad derecha (i+k ≥ n) es más corto y va primero (rango -1).
    Tras ⌈log2 n⌉ dobladas (o antes, cuando todos los rangos son distintos)
    el orden es el de los sufijos completos.
    Kasai: recorrer los sufijos en orden de POSICIÓN (i = 0, 1, …). Si el
    sufijo i tiene prefijo común h con su vecino anterior en sa, el sufijo
    i+1 (quitarle la primera letra) tiene prefijo común ≥ h-1 con el suyo:
    el vecino de i, sin su primera letra, sigue quedando antes que i+1 y
    comparte h-1 letras. Así h baja a lo más 1 por paso y en total sube
    ≤ 2n: O(n).
    Distintas: cada subcadena es prefijo de exactamente un sufijo; el
    sufijo sa[r] aporta n - sa[r] prefijos, de los cuales lcp[r] ya
    aparecieron en el sufijo anterior (y por el orden, en ningún otro nuevo).
    Patrón: los sufijos que empiezan con P forman un bloque CONTIGUO de sa
    → dos búsquedas binarias.
    Ingenuo: sorted(range(n), key=lambda i: s[i:]) es O(n² log n) en el
    peor caso (y O(n²) memoria) — sirve para n ≤ ~5000.

MACROALGORITMO
    1. rango[i] = rango del carácter s[i] (comprimido); sa = 0..n-1; k = 1.
    2. Ordenar sa por la clave (rango[i], rango[i+k] o -1).
    3. Reasignar rangos: igual que el anterior en sa si la clave coincide,
       si no, uno más.
    4. Si el último rango es n-1 (todos distintos), terminar; si no, k *= 2
       y volver a 2.
    5. Kasai: pos[sa[r]] = r; h = 0; para i = 0..n-1 con pos[i] > 0:
       j = sa[pos[i]-1]; extender h mientras s[i+h] == s[j+h];
       lcp[pos[i]] = h; h = max(h-1, 0).

COMPLEJIDAD
    Esta versión ordena con sort en cada doblada: O(n log² n) en el peor
    caso (cadenas tipo "aaaa…", ~log n rondas) y O(n log n) con orden por
    conteo (radix) en lugar de sort; en Python el sort (en C) suele ganar
    igual. Kasai O(n). Memoria O(n).
    Medido en Python con n = 10^5: aleatoria 0,2–0,4 s; "aaa…" ~0,7 s;
    Kasai < 0,1 s.

EJEMPLO A MANO
    s = "banana" (sufijos: 0 banana, 1 anana, 2 nana, 3 ana, 4 na, 5 a)
      k=1 rangos por letra:   a=0 b=1 n=2 → [1,0,2,0,2,0]
      k=1 clave (r[i], r[i+1]): 0:(1,0) 1:(0,2) 2:(2,0) 3:(0,2) 4:(2,0) 5:(0,-1)
        orden: 5(0,-1) 1,3(0,2) 0(1,0) 2,4(2,0) → rangos [2,1,3,1,3,0]
      k=2 clave (r[i], r[i+2]): 1:(1,1) 3:(1,0) 2:(3,3) 4:(3,-1) …
        orden final sa = [5, 3, 1, 0, 4, 2] (a, ana, anana, banana, na, nana)
      lcp = [0, 1, 3, 0, 0, 2]
    distintas = 21 - 6 = 15; repetida más larga = "ana" (lcp 3).

ERRORES TÍPICOS
    - Olvidar que un sufijo sin segunda mitad va ANTES (rango -1 o 0 con
      los rangos reales desplazados en +1).
    - Parar el doblado en un número fijo de rondas en vez de cuando todos
      los rangos son distintos (o k ≥ n).
    - Mezclar la convención de lcp (con el anterior o con el siguiente).
    - En Kasai, reiniciar h = 0 en cada paso (pasa a O(n²)).
    - Comparar sufijos con slicing s[i:] dentro del sort: O(n²) memoria.

VARIANTES Y RELACIONADOS
    - LCP de dos sufijos cualesquiera = mínimo de lcp en el rango
      (sparse table): comparar subcadenas en O(1).
    - Subcadena común más larga de A y B: arreglo de A + '#' + B y mirar
      vecinos de distinto origen. En ≥ K cadenas: ventana deslizante sobre sa.
    - K-ésima subcadena distinta: recorrer sa acumulando n - sa[r] - lcp[r].
    - Alternativas: suffix_automaton.py (O(n), en línea),
      hashing_polinomial.py (más simple, probabilístico).

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/F - Finding Common Passwords: la solución usa
      hashing; su docstring menciona arreglo de sufijos + ventana
      deslizante como alternativa exacta con la misma complejidad.
    - CSES «Distinct Substrings», «Repeating Substring», «Substring Order I»
    - SPOJ «SUBST1» / «DISUBSTR» (subcadenas distintas)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (ordenar los sufijos como cadenas,
      LCP carácter a carácter, conjunto de todas las subcadenas, contar
      con startswith) en 2000 casos aleatorios + casos borde
      (python suffix_array.py)
"""
import bisect
import random


def arreglo_sufijos(s):
    """Inicios de los sufijos de s en orden lexicográfico (doblado de prefijos)."""
    n = len(s)
    if n == 0:
        return []
    # Rangos iniciales: letra comprimida a 0..σ-1 (sirve para str o listas).
    letras = {c: r for r, c in enumerate(sorted(set(s)))}
    rango = [letras[c] for c in s]
    sa = list(range(n))
    k = 1
    while True:
        # Clave de s[i:i+2k] = (rango de la mitad izquierda, de la derecha);
        # se codifica en un entero; sin mitad derecha vale 0 (va primero).
        clave = [rango[i] * (n + 1) + (rango[i + k] + 1 if i + k < n else 0) for i in range(n)]
        sa.sort(key=clave.__getitem__)
        nuevo = [0] * n
        for r in range(1, n):
            nuevo[sa[r]] = nuevo[sa[r - 1]] + (clave[sa[r]] != clave[sa[r - 1]])
        rango = nuevo
        if rango[sa[-1]] == n - 1 or k >= n:    # todos distintos: orden definitivo
            return sa
        k *= 2


def lcp_kasai(s, sa):
    """lcp[r] = prefijo común de los sufijos sa[r-1] y sa[r] (lcp[0] = 0)."""
    n = len(s)
    pos = [0] * n                   # pos[i] = lugar del sufijo i dentro de sa
    for r, i in enumerate(sa):
        pos[i] = r
    lcp = [0] * n
    h = 0
    for i in range(n):              # en orden de posición, no de sa
        if pos[i] == 0:
            h = 0
            continue
        j = sa[pos[i] - 1]          # vecino anterior en el orden
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[pos[i]] = h
        if h:
            h -= 1                  # el sufijo i+1 comparte al menos h-1
    return lcp


def subcadenas_distintas(s):
    """Número de subcadenas distintas no vacías."""
    n = len(s)
    return n * (n + 1) // 2 - sum(lcp_kasai(s, arreglo_sufijos(s)))


def contar_apariciones(s, sa, patron):
    """Cuántos sufijos empiezan con patron: bloque contiguo de sa."""
    m = len(patron)
    clave = lambda i: s[i:i + m]    # se compara solo el prefijo de largo m
    return (bisect.bisect_right(sa, patron, key=clave)
            - bisect.bisect_left(sa, patron, key=clave))


def repetida_mas_larga(s):
    """Subcadena más larga con ≥ 2 apariciones (la menor en empate)."""
    sa = arreglo_sufijos(s)
    lcp = lcp_kasai(s, sa)
    if not lcp or max(lcp) == 0:
        return ""
    r = lcp.index(max(lcp))         # el primero en el orden = menor lexicográficamente
    return s[sa[r]:sa[r] + lcp[r]]


def demo():
    s = "banana"
    sa = arreglo_sufijos(s)
    print("s =", s)
    print("sa =", sa)                                       # [5, 3, 1, 0, 4, 2]
    print("sufijos:", [s[i:] for i in sa])
    print("lcp =", lcp_kasai(s, sa))                        # [0, 1, 3, 0, 0, 2]
    print("subcadenas_distintas:", subcadenas_distintas(s))  # 15
    print("contar_apariciones('ana'):", contar_apariciones(s, sa, "ana"))   # 2
    print("repetida_mas_larga:", repr(repetida_mas_larga(s)))               # 'ana'


def pruebas():
    random.seed(31415)

    def lcp2(a, b):
        k = 0
        while k < len(a) and k < len(b) and a[k] == b[k]:
            k += 1
        return k

    def repetida_bruto(s):
        n = len(s)
        mejor = ""
        for i in range(n):
            for j in range(i + 1, n + 1):
                t = s[i:j]
                if s.find(t, i + 1) != -1 and (len(t) > len(mejor) or (len(t) == len(mejor) and t < mejor)):
                    mejor = t
        return mejor

    # Casos borde
    assert arreglo_sufijos("") == [] and lcp_kasai("", []) == [] and subcadenas_distintas("") == 0
    assert arreglo_sufijos("a") == [0] and subcadenas_distintas("a") == 1
    assert arreglo_sufijos("aaaa") == [3, 2, 1, 0] and lcp_kasai("aaaa", [3, 2, 1, 0]) == [0, 1, 2, 3]
    assert subcadenas_distintas("aaaa") == 4 and repetida_mas_larga("aaaa") == "aaa"
    assert repetida_mas_larga("abc") == ""
    assert contar_apariciones("abc", arreglo_sufijos("abc"), "") == 3
    assert arreglo_sufijos([3, 1, 3, 1]) == [3, 1, 2, 0]     # también con listas

    for _ in range(2000):
        alfabeto = random.choice(["a", "ab", "abc", "abcdefgh"])
        s = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 20)))
        n = len(s)
        sa = arreglo_sufijos(s)
        assert sa == sorted(range(n), key=lambda i: s[i:])
        lcp = lcp_kasai(s, sa)
        assert lcp == [0] * (n > 0) + [lcp2(s[sa[r - 1]:], s[sa[r]:]) for r in range(1, n)]
        assert subcadenas_distintas(s) == len({s[i:j] for i in range(n) for j in range(i + 1, n + 1)})
        p = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 3)))
        assert contar_apariciones(s, sa, p) == sum(1 for i in range(n) if s.startswith(p, i))
        assert repetida_mas_larga(s) == repetida_bruto(s)

    # Grande: aleatoria y peor caso de rondas (todas iguales)
    s = "".join(random.choice("ab") for _ in range(50000))
    sa = arreglo_sufijos(s)
    assert all(s[sa[r - 1]:sa[r - 1] + 60] <= s[sa[r]:sa[r] + 60] for r in range(1, len(s)))
    s = "a" * 50000
    assert arreglo_sufijos(s) == list(range(49999, -1, -1))
    assert subcadenas_distintas(s) == 50000


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
