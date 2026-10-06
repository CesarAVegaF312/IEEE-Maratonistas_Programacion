"""
Cadenas — Autómata de sufijos («Suffix automaton, SAM»)
Nivel: Avanzado
Ejecutar: python suffix_automaton.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Es el autómata determinista más pequeño que acepta exactamente las
    subcadenas de s (tiene ≤ 2n-1 estados). Se construye EN LÍNEA (letra
    por letra) en O(n) y responde: ¿t es subcadena de s? en O(|t|), cuántas
    veces aparece t, dónde aparece por primera vez, cuántas subcadenas
    distintas hay, la subcadena común más larga con otro texto en O(|t|).
    Señales en el enunciado: «subcadenas distintas», «cuántas veces aparece
    cada consulta» con muchas consultas sobre un texto fijo, «subcadena
    común más larga» de dos textos de 10^5, texto que crece por la derecha.

FUNCIÓN
    AutomataSufijos(s)                     s: str o lista
        .contiene(t) -> bool
        .ocurrencias(t) -> int             apariciones (solapadas); t vacía → n+1
        .primera_aparicion(t) -> int       menor inicio, -1 si no aparece
        .subcadenas_distintas() -> int     sin contar la vacía
    subcadena_comun_mas_larga(a, b) -> (largo, inicio_en_b)
        Mayor L con alguna subcadena de largo L común a a y b, y el menor
        inicio en b de una de ellas; (0, 0) si no comparten nada.

IDEA Y ALGORITMO
    endpos(t) = conjunto de posiciones donde TERMINAN las apariciones de t.
    Las subcadenas con el mismo endpos forman un estado; dentro de un estado
    son sufijos unas de otras con largos consecutivos (minlen..largo[v]).
    El enlace link[v] apunta al estado del sufijo más largo de v que tiene
    un endpos DISTINTO (más grande); los enlaces forman un árbol.
    Agregar la letra c (s crece a sc): se crea el estado cur (largo n+1).
    Desde el último estado se sube por los enlaces poniendo transición c →
    cur mientras no exista. Si se llega a un p con transición c → q:
      - si largo[q] == largo[p] + 1, q representa justo «sufijo de p + c»:
        link[cur] = q;
      - si no, q mezcla subcadenas que ahora tienen endpos distintos: se
        CLONA q con largo[p] + 1 (mismas transiciones y enlace), y se
        redirigen a la copia las transiciones c → q de p y sus ancestros.
    Cuentas: cada estado no clonado aporta una posición final; |endpos(v)|
    = suma en su subárbol del árbol de enlaces → se acumula de los estados
    más largos a los más cortos (orden por largo, conteo en O(n)).
    Distintas: cada estado aporta largo[v] - largo[link[v]] subcadenas.
    Subcadena común: se recorre b sobre el autómata de a manteniendo el
    sufijo más largo de b[:i+1] que es subcadena de a; si falta la
    transición se sube por enlaces (acortando) como en Aho–Corasick.

MACROALGORITMO
    1. Estado 0 = raíz (cadena vacía), link -1, largo 0. ult = 0.
    2. Por cada letra c: crear cur (largo[ult]+1, cnt 1); p = ult.
    3. Mientras p ≠ -1 y c no está en sig[p]: sig[p][c] = cur; p = link[p].
    4. Si p == -1: link[cur] = 0. Si no, q = sig[p][c]: si largo[q] ==
       largo[p]+1, link[cur] = q; si no, clonar q (cnt 0), redirigir
       transiciones c → q en la cadena de p, link[q] = link[cur] = clon.
    5. ult = cur.
    6. Al final: ordenar estados por largo decreciente y sumar cnt al padre.
    7. Consultas: caminar t desde la raíz; si se cae, no aparece.

COMPLEJIDAD
    Construcción O(n·log σ) con dict (amortizado lineal), ≤ 2n-1 estados y
    ≤ 3n-4 transiciones. Consultas O(|t|). En Python, n = 10^5 en ~0,4 s
    (con mucha memoria por los dicts: preferir n ≤ 2·10^5).

EJEMPLO A MANO
    s = "abb":
      'a': estado 1 (largo 1), link 0.
      'b': estado 2 (largo 2), sig[1][b] = sig[0][b] = 2, link 0.
      'b': estado 3 (largo 3), sig[2][b] = 3; en la raíz ya hay b → q = 2,
           pero largo[2] = 2 ≠ 0+1: clonar 2 en 4 (largo 1, sig {b: 3}),
           sig[0][b] = 4, link[2] = link[3] = 4.
    Distintas: (1-0) + (2-1) + (3-1) + (1-0) = 5 → a, b, ab, bb, abb.
    ocurrencias("b"): cnt[4] = cnt[2] + cnt[3] = 2.

ERRORES TÍPICOS
    - Olvidar copiar las transiciones (sig[q].copy()) al clonar: el clon
      y q quedan compartiendo el mismo dict.
    - Dar cnt = 1 a los clones (no son posiciones finales nuevas).
    - Acumular cnt en orden de creación en lugar de por largo decreciente.
    - Creer que hay a lo más n estados: hay hasta 2n-1 (reservar memoria).

VARIANTES Y RELACIONADOS
    - K-ésima subcadena distinta en orden: DP de cuántos caminos salen de
      cada estado y descenso voraz.
    - Subcadena común de K textos: autómata de uno y recorrer los demás
      guardando el mínimo por estado.
    - Alternativas: suffix_array.py (arreglo de sufijos + LCP),
      hashing_polinomial.py (búsqueda binaria + hashing), aho_corasick.py
      (muchos patrones fijos sobre un texto que se recorre una vez).

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/F - Finding Common Passwords: la solución usa
      hashing; su docstring menciona el autómata de sufijos como
      alternativa exacta.
    - CSES «Distinct Substrings», «Counting Patterns», «Pattern Positions»
    - SPOJ «LCS» («Longest Common Substring», 2·10^5 con autómata)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (conjunto de subcadenas, contar con
      startswith, str.find, probar todos los largos) en 2000 casos
      aleatorios con varias consultas cada uno + casos borde
      (python suffix_automaton.py)
"""
import random


class AutomataSufijos:
    def __init__(self, s):
        self.n = len(s)
        sig = [{}]          # transiciones
        link = [-1]         # enlace de sufijo
        largo = [0]         # subcadena más larga del estado
        cnt = [0]           # 1 si el estado es una posición final real (no clon)
        prim = [-1]         # fin de la primera aparición (firstpos)
        ult = 0
        for idx, c in enumerate(s):
            cur = len(sig)
            sig.append({})
            largo.append(largo[ult] + 1)
            link.append(0)
            cnt.append(1)
            prim.append(idx)
            p = ult
            # Los sufijos de lo leído que aún no sabían continuar con c ahora van a cur.
            while p != -1 and c not in sig[p]:
                sig[p][c] = cur
                p = link[p]
            if p != -1:
                q = sig[p][c]
                if largo[p] + 1 == largo[q]:
                    link[cur] = q
                else:
                    # q mezcla subcadenas con endpos distintos: separar con un clon.
                    clon = len(sig)
                    sig.append(sig[q].copy())
                    largo.append(largo[p] + 1)
                    link.append(link[q])
                    cnt.append(0)
                    prim.append(prim[q])
                    while p != -1 and sig[p].get(c) == q:
                        sig[p][c] = clon
                        p = link[p]
                    link[q] = link[cur] = clon
            ult = cur
        # |endpos| = suma de cnt en el subárbol del árbol de enlaces:
        # recorrer por largo decreciente (orden por conteo) y pasar al padre.
        cubetas = [[] for _ in range(self.n + 1)]
        for v in range(1, len(sig)):
            cubetas[largo[v]].append(v)
        for L in range(self.n, 0, -1):
            for v in cubetas[L]:
                cnt[link[v]] += cnt[v]
        self.sig, self.link, self.largo, self.cnt, self.prim = sig, link, largo, cnt, prim

    def _estado(self, t):
        """Estado al que lleva t desde la raíz, o -1 si t no es subcadena."""
        v = 0
        for c in t:
            v = self.sig[v].get(c, -1)
            if v == -1:
                return -1
        return v

    def contiene(self, t):
        return self._estado(t) != -1

    def ocurrencias(self, t):
        if not t:
            return self.n + 1           # la vacía «aparece» en cada hueco
        v = self._estado(t)
        return self.cnt[v] if v != -1 else 0

    def primera_aparicion(self, t):
        v = self._estado(t)
        if v == -1:
            return -1
        return self.prim[v] - len(t) + 1 if t else 0

    def subcadenas_distintas(self):
        return sum(self.largo[v] - self.largo[self.link[v]] for v in range(1, len(self.sig)))


def subcadena_comun_mas_larga(a, b):
    """(L, inicio en b) de la subcadena común más larga, recorriendo b sobre el SAM de a."""
    sam = AutomataSufijos(a)
    sig, link, largo = sam.sig, sam.link, sam.largo
    v = actual = 0                      # actual = largo del sufijo de b[:i+1] presente en a
    mejor, inicio = 0, 0
    for i, c in enumerate(b):
        while v and c not in sig[v]:    # acortar hasta poder extender con c
            v = link[v]
            actual = largo[v]
        if c in sig[v]:
            v = sig[v][c]
            actual += 1
        else:
            v = actual = 0
        if actual > mejor:
            mejor, inicio = actual, i - actual + 1
    return mejor, inicio


def demo():
    s = "abb"
    sam = AutomataSufijos(s)
    print("s =", s)
    print("estados:", len(sam.sig), " largo =", sam.largo, " link =", sam.link)
    print("subcadenas_distintas:", sam.subcadenas_distintas())     # 5
    print("ocurrencias('b'):", sam.ocurrencias("b"))                # 2
    print("primera_aparicion('bb'):", sam.primera_aparicion("bb"))  # 1
    print("contiene('ba'):", sam.contiene("ba"))                    # False
    print("subcadena_comun_mas_larga('xabcy', 'zzabcw'):",
          subcadena_comun_mas_larga("xabcy", "zzabcw"))             # (3, 2)


def pruebas():
    random.seed(271828)

    def lcs_bruto(a, b):
        for L in range(min(len(a), len(b)), 0, -1):
            for j in range(len(b) - L + 1):
                if b[j:j + L] in a:
                    return (L, j)
        return (0, 0)

    # Casos borde
    sam = AutomataSufijos("")
    assert sam.subcadenas_distintas() == 0 and sam.ocurrencias("") == 1
    assert sam.ocurrencias("a") == 0 and sam.primera_aparicion("a") == -1
    sam = AutomataSufijos("aaaa")
    assert sam.subcadenas_distintas() == 4 and sam.ocurrencias("aa") == 3
    assert subcadena_comun_mas_larga("", "abc") == (0, 0)
    assert AutomataSufijos([1, 2, 1, 2]).ocurrencias([1, 2]) == 2

    for _ in range(2000):
        alfabeto = random.choice(["a", "ab", "abc", "abcdef"])
        s = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 18)))
        n = len(s)
        sam = AutomataSufijos(s)
        assert len(sam.sig) <= max(1, 2 * n - 1) + (n == 1)
        assert sam.subcadenas_distintas() == len({s[i:j] for i in range(n) for j in range(i + 1, n + 1)})
        for _ in range(5):
            t = "".join(random.choice(alfabeto) for _ in range(random.randint(1, 4)))
            if random.random() < 0.5 and n:
                i = random.randrange(n)
                t = s[i:random.randint(i + 1, n)]      # una subcadena que sí está
            assert sam.contiene(t) == (t in s)
            assert sam.ocurrencias(t) == sum(1 for i in range(n) if s.startswith(t, i))
            assert sam.primera_aparicion(t) == s.find(t)
        b = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 18)))
        assert subcadena_comun_mas_larga(s, b) == lcs_bruto(s, b)

    # Grande: 10^5 letras
    s = "".join(random.choice("ab") for _ in range(100000))
    sam = AutomataSufijos(s)
    t = s[40000:40020]
    assert sam.ocurrencias(t) == sum(1 for i in range(len(s)) if s.startswith(t, i))
    assert subcadena_comun_mas_larga(s, "c" + s[123:5123] + "c") == (5000, 1)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
