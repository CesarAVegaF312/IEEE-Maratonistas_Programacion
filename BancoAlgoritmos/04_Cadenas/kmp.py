"""
Cadenas — Función prefijo y búsqueda KMP («Knuth–Morris–Pratt, prefix function»)
Nivel: Intermedio
Ejecutar: python kmp.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar TODAS las apariciones de un patrón P en un texto T en
    O(|T| + |P|), y responder preguntas de estructura de una cadena:
    bordes (prefijos que también son sufijos), periodo mínimo, si la cadena
    es una potencia u^k, cuántas veces aparece cada prefijo.
    Señales en el enunciado: «cuántas veces aparece P en T» con |T|, |P|
    hasta 10^6; «prefijo que también es sufijo»; «la cadena se forma
    repitiendo un bloque»; «patrón que se repite / periodo»; secuencias de
    NÚMEROS (no solo letras) donde hay que buscar un bloque.

FUNCIÓN
    funcion_prefijo(s) -> list[int]
        pi[i] = largo del borde propio más largo de s[0..i] (prefijo de
        s[0..i], distinto de él, que también es sufijo). pi[0] = 0.
    kmp_buscar(texto, patron) -> list[int]
        Posiciones de inicio (desde 0) de todas las apariciones, incluyendo
        las que se solapan. Patrón vacío → todas las posiciones 0..|T|.
    bordes(s) -> list[int]       largos de todos los bordes propios, crecientes
    periodos(s) -> list[int]     todos los p en 1..n con s[i] == s[i+p]
    periodo_minimo(s) -> int     n - pi[n-1] (n = 0 → 0)
    Sirven para str, list o tuple (cualquier secuencia comparable con ==).

IDEA Y ALGORITMO
    Si ya sé que s[0..i-1] tiene borde de largo k (s[0..k-1] = s[i-k..i-1])
    y s[k] == s[i], el borde crece a k+1. Si no coincide, NO hay que volver
    a empezar: el siguiente candidato a borde es el borde más largo de
    s[0..k-1], es decir pi[k-1] (un borde de un borde es borde, y todos los
    bordes de s[0..i-1] se recorren así de mayor a menor). Se salta por esa
    cadena de bordes hasta que coincida o k = 0.
    ¿Por qué es lineal? k sube a lo más 1 por carácter y cada salto lo baja
    al menos 1; en total los saltos no superan las subidas: ≤ 2n pasos.
    Búsqueda: se recorre el texto manteniendo k = largo del prefijo de P más
    largo que termina en la posición actual del texto (misma recurrencia,
    usando pi de P). Cuando k == |P| hay aparición; se continúa con
    k = pi[|P|-1] para no perder las solapadas.
    Bordes y periodos: s tiene periodo p ⇔ s tiene borde de largo n-p.
    Los bordes son pi[n-1], pi[pi[n-1]-1], … ; el periodo mínimo es
    n - pi[n-1], y s = u^k con |u| < n ⇔ ese periodo divide a n.
    Ingenuo: comparar P en cada posición, O(|T|·|P|) (10^12 en el peor).

MACROALGORITMO
    1. pi[0] = 0. Para i = 1..n-1: k = pi[i-1].
    2. Mientras k > 0 y s[k] != s[i]: k = pi[k-1].
    3. Si s[k] == s[i]: k += 1. pi[i] = k.
    4. Búsqueda: k = 0; por cada carácter c del texto aplicar 2–3 con c.
    5. Si k == |P|: anotar inicio (i - |P| + 1) y hacer k = pi[|P|-1].
    6. Bordes: recorrer k = pi[n-1], pi[k-1], … hasta 0. Periodos: n - borde.

COMPLEJIDAD
    Tiempo O(|T| + |P|), memoria O(|P|). En Python, ~10^6 caracteres en
    ~0,5 s. (Si solo hay que buscar texto en texto, str.find en ciclo es
    más rápido en Python; KMP sirve cuando hay que razonar con pi o la
    secuencia no es un str.)

EJEMPLO A MANO
    s = "aabaaab"
      i=1 'a': k=0, s[0]='a' = → pi=1
      i=2 'b': k=1, s[1]='a' ≠ 'b' → k=pi[0]=0; s[0]≠'b' → pi=0
      i=3 'a': k=0, s[0]='a' = → pi=1
      i=4 'a': k=1, s[1]='a' = → pi=2
      i=5 'a': k=2, s[2]='b' ≠ → k=pi[1]=1; s[1]='a' = → pi=2
      i=6 'b': k=2, s[2]='b' = → pi=3
    pi = [0,1,0,1,2,2,3]; bordes = [1, 3] ("a", "aab"); periodos = [4, 6, 7].
    kmp_buscar("abababa", "aba") = [0, 2, 4] (solapadas).

ERRORES TÍPICOS
    - Usar un `if` en vez de `while` al retroceder por la cadena de bordes.
    - Tras una aparición, reiniciar k = 0: se pierden las solapadas.
    - Concatenar P + '#' + T con un separador que sí aparece en el texto
      (o con listas de números: el separador debe ser un valor imposible).
      Esta versión recorre el texto aparte y no necesita separador.
    - Confundir «periodo mínimo» con «la cadena es potencia»: "abaab" tiene
      periodo 3 pero 3 no divide a 5, así que no es u^k.

VARIANTES Y RELACIONADOS
    - Autómata KMP (transiciones por letra) para DP «cadenas que no
      contienen P»: aut[k][c] en O(|P|·Σ).
    - Contar apariciones de cada prefijo de s: cnt[pi[i]]++ y propagar por
      la cadena de bordes de mayor a menor.
    - Buscar P en un texto CIRCULAR / «¿B es rotación de A?»: buscar B en A+A.
    - Mismo poder con otra representación: funcion_z.py. Muchos patrones a
      la vez: aho_corasick.py. Rotación mínima: rotacion_minima.py.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/H - Half the Polygon (congruencia = una secuencia
      cíclica es rotación de otra: buscarla en la secuencia duplicada; allí
      se usa la búsqueda de str de Python, KMP es la versión manual)
    - CSES «String Matching», «Finding Borders», «Finding Periods»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (definiciones directas: comparar en
      cada posición, probar cada largo de borde/periodo) en 3000 casos
      aleatorios + casos borde + listas de números (python kmp.py)
"""
import random


def funcion_prefijo(s):
    """pi[i] = largo del borde propio más largo de s[0..i]."""
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        k = pi[i - 1]
        # Retroceder por la cadena de bordes hasta poder extender con s[i].
        while k > 0 and s[k] != s[i]:
            k = pi[k - 1]
        if s[k] == s[i]:
            k += 1
        pi[i] = k
    return pi


def kmp_buscar(texto, patron):
    """Inicios de todas las apariciones (solapadas incluidas) de patron en texto."""
    m = len(patron)
    if m == 0:
        return list(range(len(texto) + 1))
    pi = funcion_prefijo(patron)
    res = []
    k = 0                           # largo del prefijo de patron que termina aquí
    for i, c in enumerate(texto):
        while k > 0 and patron[k] != c:
            k = pi[k - 1]
        if patron[k] == c:
            k += 1
        if k == m:
            res.append(i - m + 1)
            k = pi[m - 1]           # seguir buscando (permite solapes)
    return res


def bordes(s):
    """Largos de todos los bordes propios de s, de menor a mayor."""
    if not s:
        return []
    pi = funcion_prefijo(s)
    res = []
    k = pi[-1]
    while k > 0:                    # un borde de un borde también es borde
        res.append(k)
        k = pi[k - 1]
    return res[::-1]


def periodos(s):
    """Todos los periodos p (1..n): p es periodo ⇔ hay borde de largo n - p."""
    n = len(s)
    if n == 0:
        return []
    return sorted([n - b for b in bordes(s)] + [n])


def periodo_minimo(s):
    """Menor periodo; s es potencia u^k (k ≥ 2) ⇔ periodo_minimo(s) divide a n y es < n."""
    return len(s) - funcion_prefijo(s)[-1] if s else 0


def demo():
    s = "aabaaab"
    print("s =", s)
    print("funcion_prefijo:", funcion_prefijo(s))          # [0, 1, 0, 1, 2, 2, 3]
    print("bordes:", bordes(s))                            # [1, 3]
    print("periodos:", periodos(s))                        # [4, 6, 7]
    print("kmp_buscar('abababa', 'aba'):", kmp_buscar("abababa", "aba"))   # [0, 2, 4]
    t = "abcabcabc"
    p = periodo_minimo(t)
    print("periodo_minimo('abcabcabc') =", p, "→ es potencia:", len(t) % p == 0 and p < len(t))


def pruebas():
    random.seed(4242)

    def pi_bruto(s):
        return [max(k for k in range(i + 1) if s[:k] == s[i + 1 - k:i + 1]) for i in range(len(s))]

    def buscar_bruto(t, p):
        return [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]

    # Casos borde
    assert funcion_prefijo("") == [] and bordes("") == [] and periodos("") == []
    assert funcion_prefijo("a") == [0] and periodo_minimo("a") == 1
    assert kmp_buscar("", "a") == [] and kmp_buscar("", "") == [0]
    assert kmp_buscar("aaaa", "aa") == [0, 1, 2]
    assert bordes("aaaa") == [1, 2, 3] and periodos("aaaa") == [1, 2, 3, 4]
    assert periodo_minimo("abaab") == 3
    # Funciona con listas de números (no hace falta separador)
    assert kmp_buscar([1, 2, 1, 2, 1], [1, 2, 1]) == [0, 2]

    for _ in range(3000):
        alfabeto = random.choice(["a", "ab", "abc"])
        s = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 14)))
        p = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 4)))
        n = len(s)
        assert funcion_prefijo(s) == pi_bruto(s)
        assert kmp_buscar(s, p) == buscar_bruto(s, p)
        assert bordes(s) == [k for k in range(1, n) if s[:k] == s[n - k:]]
        assert periodos(s) == [q for q in range(1, n + 1)
                               if all(s[i] == s[i + q] for i in range(n - q))]
        if n:
            assert periodo_minimo(s) == periodos(s)[0]
        lista = [random.randint(0, 2) for _ in range(random.randint(0, 12))]
        patron = [random.randint(0, 2) for _ in range(random.randint(1, 3))]
        assert kmp_buscar(lista, patron) == buscar_bruto(lista, patron)

    # Grande: 2·10^5 caracteres, peor caso para retrocesos
    t = "a" * 200000
    assert len(kmp_buscar(t, "a" * 1000)) == 200000 - 1000 + 1
    t = ("ab" * 50000) + "c"
    assert kmp_buscar(t, "abc") == [len(t) - 3]


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
