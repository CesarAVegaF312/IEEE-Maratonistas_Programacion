"""
Cadenas — Prefijo común más largo de varias cadenas («Longest common prefix»)
Nivel: Básico
Ejecutar: python prefijo_comun.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar el prefijo más largo que comparten TODAS las cadenas de una
    lista (o el mayor que comparte algún par). Aparece al agrupar palabras,
    rutas de archivos, autocompletado o como paso de algoritmos más grandes
    (LCP de un arreglo de sufijos).
    Señales en el enunciado: «empiezan igual», «prefijo común», «raíz
    común», «el comienzo más largo compartido por todas las palabras».

FUNCIÓN
    lcp_dos(a, b) -> int                 largo del prefijo común de a y b
    prefijo_comun(palabras) -> str       carácter a carácter (columna por columna)
    prefijo_comun_ordenando(palabras) -> str
        Mismo resultado comparando solo la menor y la mayor en orden
        lexicográfico. Lista vacía → "".
    max_lcp_par(palabras) -> int
        Mayor prefijo común entre DOS palabras distintas de posición
        (0 si hay menos de dos).

IDEA Y ALGORITMO
    Carácter a carácter: el prefijo común de todas tiene largo k si las
    columnas 0..k-1 coinciden en todas las palabras y la columna k falla en
    alguna (o alguna palabra se acaba). Se revisa columna por columna y se
    para en la primera que falla: se miran a lo más n·k + n caracteres.
    Ordenando: si las palabras están ordenadas, cualquier palabra w queda
    entre la menor (mín) y la mayor (máx). Si mín y máx empiezan con P,
    todo lo que está entre ellas en orden lexicográfico también empieza con
    P (no se puede «salir» de P y volver). Así LCP(todas) = LCP(mín, máx).
    No hace falta ordenar todo: basta min() y max(), O(Σ|w|).
    Mejor par: tras ordenar, el par con mayor LCP es de vecinas, porque
    LCP(w_i, w_j) = mín de los LCP de las vecinas entre i y j.
    Ingenuo para un par: probar todos los pares, O(n²·L).

MACROALGORITMO
    1. Si no hay palabras, la respuesta es "".
    2. Carácter a carácter: para k = 0, 1, …: si alguna palabra tiene largo
       k o su carácter k difiere del de la primera, parar.
    3. Responder palabras[0][:k].
    4. (Alternativa) lo = min(palabras), hi = max(palabras); responder
       lo[:lcp_dos(lo, hi)].
    5. (Mejor par) ordenar y tomar el máximo de lcp_dos entre vecinas.

COMPLEJIDAD
    prefijo_comun: O(n·k) con k = respuesta (+ n). prefijo_comun_ordenando:
    O(Σ|w|) por min/max. max_lcp_par: O(Σ|w| log n) por el ordenamiento.
    En Python, 10^6 caracteres en total sin problema.

EJEMPLO A MANO
    palabras = ["flower", "flow", "flight"]
      columna 0: f f f ✓ | columna 1: l l l ✓ | columna 2: o o i ✗ → "fl"
    ordenando: mín = "flight", máx = "flower" → LCP("flight","flower") = "fl"
    max_lcp_par: ordenadas flight, flow, flower → vecinas 2, 4 → 4 ("flow")

ERRORES TÍPICOS
    - No contemplar palabras más cortas que el prefijo actual: índice fuera
      de rango.
    - Lista vacía: min()/max() lanzan error.
    - Mayúsculas: si el enunciado no las distingue, pasar todo a minúscula
      ANTES de comparar (y antes de ordenar).
    - En «mejor par», comparar solo la primera con las demás en lugar de
      vecinas tras ordenar.

VARIANTES Y RELACIONADOS
    - Contar cuántas palabras tienen cierto prefijo: trie.py.
    - LCP de dos subcadenas cualesquiera en O(log n): hashing_polinomial.py;
      de todos los sufijos: suffix_array.py (Kasai); con un patrón fijo:
      funcion_z.py.
    - os.path.commonprefix(lista) hace lo mismo (carácter a carácter).

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/B - Be Strong (LCP sin distinguir mayúsculas)
    - LeetCode 14 «Longest Common Prefix»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (probar cada prefijo de la primera,
      todos los pares) y contra os.path.commonprefix en 3000 casos
      aleatorios + casos borde (python prefijo_comun.py)
"""
import os
import random


def lcp_dos(a, b):
    """Largo del prefijo común de a y b."""
    k, m = 0, min(len(a), len(b))
    while k < m and a[k] == b[k]:
        k += 1
    return k


def prefijo_comun(palabras):
    """Prefijo común de todas, revisando columna por columna."""
    if not palabras:
        return ""
    primera = palabras[0]
    k = 0
    while True:
        # La columna k sirve si existe en todas y coincide con la primera.
        if k == len(primera) or any(k == len(w) or w[k] != primera[k] for w in palabras):
            return primera[:k]
        k += 1


def prefijo_comun_ordenando(palabras):
    """LCP(todas) = LCP(menor, mayor): las demás quedan «entre» ellas."""
    if not palabras:
        return ""
    lo, hi = min(palabras), max(palabras)
    return lo[:lcp_dos(lo, hi)]


def max_lcp_par(palabras):
    """Mayor LCP entre dos palabras de la lista: basta mirar vecinas ordenadas."""
    p = sorted(palabras)
    return max((lcp_dos(p[i], p[i + 1]) for i in range(len(p) - 1)), default=0)


def demo():
    palabras = ["flower", "flow", "flight"]
    print("palabras =", palabras)
    print("prefijo_comun:", repr(prefijo_comun(palabras)))                         # 'fl'
    print("prefijo_comun_ordenando:", repr(prefijo_comun_ordenando(palabras)))     # 'fl'
    print("max_lcp_par:", max_lcp_par(palabras))                                   # 4
    # Como en Be Strong: sin distinguir mayúsculas
    print("Be Strong:", repr(prefijo_comun([w.lower() for w in ["Arbol", "ARBUSTO", "arbitro"]])))  # 'arb'


def pruebas():
    random.seed(99)

    def prefijo_bruto(palabras):
        if not palabras:
            return ""
        # El prefijo más largo de la primera que es prefijo de todas.
        for k in range(len(palabras[0]), -1, -1):
            if all(w.startswith(palabras[0][:k]) for w in palabras):
                return palabras[0][:k]

    def par_bruto(palabras):
        n = len(palabras)
        return max((lcp_dos(palabras[i], palabras[j]) for i in range(n) for j in range(i + 1, n)),
                   default=0)

    # Casos borde
    assert prefijo_comun([]) == prefijo_comun_ordenando([]) == ""
    assert prefijo_comun(["solo"]) == "solo" and max_lcp_par(["solo"]) == 0
    assert prefijo_comun(["", "abc"]) == "" and prefijo_comun(["abc", "abc"]) == "abc"
    assert prefijo_comun(["ab", "abc", "a"]) == "a"
    assert max_lcp_par(["xyz", "xyz"]) == 3

    for _ in range(3000):
        alfabeto = random.choice(["a", "ab", "abc"])
        palabras = ["".join(random.choice(alfabeto) for _ in range(random.randint(0, 7)))
                    for _ in range(random.randint(0, 8))]
        esperado = prefijo_bruto(palabras)
        assert prefijo_comun(palabras) == esperado
        assert prefijo_comun_ordenando(palabras) == esperado
        assert esperado == (os.path.commonprefix(palabras) if palabras else "")
        assert max_lcp_par(palabras) == par_bruto(palabras)

    # Tamaño grande: 5000 palabras de 200 letras casi iguales
    base = "x" * 199
    palabras = [base + random.choice("ab") for _ in range(5000)] + [base + "a"]
    assert prefijo_comun(palabras) == prefijo_comun_ordenando(palabras) == base


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
