"""
Cadenas — Secuencia de De Bruijn con palabras de Lyndon («De Bruijn sequence, FKM algorithm»)
Nivel: Avanzado
Ejecutar: python de_bruijn.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Una secuencia de De Bruijn B(k, n) es una cadena CIRCULAR de largo k^n
    sobre un alfabeto de k símbolos en la que cada palabra de largo n
    aparece exactamente una vez como ventana. Es la forma más corta de
    «recorrer todas las combinaciones»: cerraduras de teclado sin Enter,
    tambores/discos codificados, pruebas exhaustivas. El algoritmo FKM da,
    además, la secuencia LEXICOGRÁFICAMENTE MENOR.
    Señales en el enunciado: «toda secuencia de n colores / dígitos debe
    aparecer exactamente una vez» en algo circular; «la cadena más corta
    que contiene todas las combinaciones de n dígitos»; m = k^n.

FUNCIÓN
    palabras_lyndon(k, n) -> generador de listas
        Todas las palabras de Lyndon de largo 1..n sobre {0..k-1}, en orden
        lexicográfico (generador; cada lista es una copia).
    de_bruijn(k, n) -> list[int]
        La secuencia circular B(k, n) lexicográficamente menor (largo k^n).
        k = 1 da [0] (largo 1^n = 1).
    de_bruijn_lineal(k, n) -> list[int]
        Versión no circular: B(k, n) + sus primeros n-1 símbolos (largo
        k^n + n - 1), donde cada palabra aparece una vez como subcadena.
    contar_lyndon(k, L) -> int      palabras de Lyndon de largo exactamente L

IDEA Y ALGORITMO
    Palabra de Lyndon: no vacía y estrictamente menor que todas sus
    rotaciones propias (ver rotacion_minima.py). Teorema de Fredricksen,
    Kessler y Maiorana (FKM): si se concatenan EN ORDEN LEXICOGRÁFICO todas
    las palabras de Lyndon sobre k símbolos cuyo largo DIVIDE a n, se
    obtiene una secuencia de De Bruijn B(k, n), y es la menor de todas.
    Intuición del conteo: cada collar (clase de rotación) de largo n tiene
    un periodo primitivo d | n y un único representante de Lyndon de largo
    d; un collar de periodo d aporta d palabras distintas (sus rotaciones).
    Σ_{d|n} d·(Lyndon de largo d) = k^n: las piezas tienen el largo justo.
    Generación en orden (Duval / FKM), iterativa: a partir de la palabra
    de Lyndon w (de largo m ≤ n), la siguiente se obtiene
        1. repetir w cíclicamente hasta largo n,
        2. quitar del final todos los símbolos k-1,
        3. sumar 1 al último símbolo.
    Esto recorre todas las de largo ≤ n en orden y sin repetir.
    Ingenuo: probar todas las cadenas de largo k^n (k^(k^n)) o buscar un
    ciclo euleriano en el grafo de De Bruijn (válido, pero no da la menor
    sin cuidado extra).

MACROALGORITMO
    1. w = [-1].
    2. Mientras w no esté vacía: w[-1] += 1; ahora w es de Lyndon.
    3. Si n % len(w) == 0, agregar w a la secuencia.
    4. Extender w repitiéndola hasta largo n (w[i] = w[i - m]).
    5. Quitar del final los símbolos iguales a k-1 y volver a 2.
    6. (Lineal) agregar al final los primeros n-1 símbolos.

COMPLEJIDAD
    El generador hace O(n) por palabra de Lyndon con largo ≤ n; en total
    O(k^n) amortizado para la secuencia (largo k^n). Memoria O(k^n) de
    salida. Medido en Python: k^n ≈ 10^6 (k=2, n=20 o k=10, n=6) en ~0,1 s.

EJEMPLO A MANO
    k = 2, n = 3. Generación (w → extender → quitar 1s finales → +1):
      [0] → 000 → 000 → [0,0,1]   ; [0] tiene largo 1 | 3 → sí
      [0,0,1] → 001 → 00 → [0,1]  ; largo 3 | 3 → sí
      [0,1] → 010 → 010 → [0,1,1] ; largo 2 ∤ 3 → no
      [0,1,1] → 011 → 0 → [1]     ; sí
      [1] → 111 → [] fin          ; sí
    Lyndon ≤ 3: 0, 001, 01, 011, 1 → B(2,3) = 0 001 011 1 = 00010111
    (con letras: AAABABBB). Ventanas circulares: 000 001 010 101 011 111
    110 100: las 8, cada una una vez.

ERRORES TÍPICOS
    - Concatenar TODAS las palabras de Lyndon de largo ≤ n, no solo las de
      largo que divide a n (para n = 3 se colaría "01").
    - Olvidar que la secuencia es circular: si se pide una cadena lineal
      hay que añadir los primeros n-1 símbolos.
    - k = 1: el teorema da "0" (largo 1); algunos enunciados piden otra
      convención (p. ej. Colombia 2017 D pide n veces 'A'). Leer con cuidado.
    - Generarlas con recursión de profundidad n·algo: usar la versión iterativa.

VARIANTES Y RELACIONADOS
    - Ciclo euleriano (Hierholzer) en el grafo de De Bruijn de nodos de
      largo n-1: otra construcción, útil cuando hay palabras prohibidas.
    - Contar palabras de Lyndon/collares: Möbius y Burnside.
    - Factorización de Lyndon y rotación mínima: rotacion_minima.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/D - Rotating Drum (B(k, n) lexicográficamente
      menor con palabras de Lyndon, FKM)
    - CSES «De Bruijn Sequence» (versión lineal, k = 2)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta: palabras de Lyndon por definición
      (todas las cadenas de largo ≤ n), De Bruijn mínima buscando en orden
      lexicográfico entre TODAS las cadenas de largo k^n (k^n ≤ 16), y
      propiedad «cada ventana una vez» hasta k^n = 65536; 20 pares (k, n)
      + casos borde (python de_bruijn.py)
"""
import itertools


def palabras_lyndon(k, n):
    """Genera las palabras de Lyndon de largo 1..n sobre {0..k-1}, en orden."""
    w = [-1]
    while w:
        w[-1] += 1                  # w es ahora la siguiente palabra de Lyndon
        yield list(w)
        m = len(w)
        while len(w) < n:           # repetir w cíclicamente hasta largo n
            w.append(w[-m])
        while w and w[-1] == k - 1:  # quitar los símbolos máximos del final
            w.pop()


def de_bruijn(k, n):
    """B(k, n) lexicográficamente menor: Lyndon de largo que divide a n, en orden."""
    res = []
    for w in palabras_lyndon(k, n):
        if n % len(w) == 0:
            res.extend(w)
    return res


def de_bruijn_lineal(k, n):
    """Cadena de largo k^n + n - 1 que contiene cada palabra de largo n una vez."""
    s = de_bruijn(k, n)
    return s + s[:n - 1]


def contar_lyndon(k, L):
    """Palabras de Lyndon de largo exactamente L: (1/L)·Σ_{d|L} μ(d)·k^(L/d)."""
    def mobius(d):
        r, p = 1, 2
        while p * p <= d:
            if d % p == 0:
                d //= p
                if d % p == 0:
                    return 0        # p² divide a d
                r = -r
            p += 1
        return -r if d > 1 else r
    return sum(mobius(d) * k ** (L // d) for d in range(1, L + 1) if L % d == 0) // L


def demo():
    k, n = 2, 3
    print("palabras de Lyndon (k=2, n<=3):", list(palabras_lyndon(k, n)))
    # [[0], [0, 0, 1], [0, 1], [0, 1, 1], [1]]
    b = de_bruijn(k, n)
    print("de_bruijn(2, 3):", b, "→", "".join(chr(65 + x) for x in b))   # AAABABBB
    print("de_bruijn_lineal(2, 3):", "".join(map(str, de_bruijn_lineal(k, n))))  # 0001011100
    print("de_bruijn(3, 2):", "".join(map(str, de_bruijn(3, 2))))         # 001021122
    print("contar_lyndon(2, 4):", contar_lyndon(2, 4))                    # 3 (0001 0011 0111)


def pruebas():
    def lyndon(w):
        return len(w) > 0 and all(w < w[i:] + w[:i] for i in range(1, len(w)))

    def es_de_bruijn(s, k, n):
        m = len(s)
        if m != k ** n:
            return False
        ventanas = {tuple(s[(i + t) % m] for t in range(n)) for i in range(m)}
        return len(ventanas) == m and all(0 <= x < k for x in s)

    # Casos borde
    assert de_bruijn(1, 5) == [0] and list(palabras_lyndon(1, 3)) == [[0]]
    assert de_bruijn(5, 1) == [0, 1, 2, 3, 4]
    assert "".join(chr(65 + x) for x in de_bruijn(2, 3)) == "AAABABBB"   # ejemplo de Rotating Drum

    pares = 0
    # Lyndon y De Bruijn mínima contra búsqueda exhaustiva
    for k, n in [(2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (4, 1), (5, 1)]:
        todas = sorted(list(w) for L in range(1, n + 1)
                       for w in itertools.product(range(k), repeat=L) if lyndon(w))
        assert list(palabras_lyndon(k, n)) == todas
        for L in range(1, n + 1):
            assert contar_lyndon(k, L) == sum(1 for w in todas if len(w) == L)
        # product recorre en orden lexicográfico: la primera válida es la menor.
        menor = next(list(s) for s in itertools.product(range(k), repeat=k ** n)
                     if es_de_bruijn(s, k, n))
        assert de_bruijn(k, n) == menor
        pares += 1

    # Propiedad «cada ventana exactamente una vez» en tamaños mayores
    for k, n in [(2, 8), (2, 12), (2, 16), (3, 5), (3, 7), (4, 5), (5, 4),
                 (6, 3), (10, 4), (26, 2), (26, 3), (7, 5)]:
        s = de_bruijn(k, n)
        assert es_de_bruijn(s, k, n)
        lin = de_bruijn_lineal(k, n)
        assert len({tuple(lin[i:i + n]) for i in range(len(lin) - n + 1)}) == k ** n
        assert sum(contar_lyndon(k, d) * d for d in range(1, n + 1) if n % d == 0) == k ** n
        pares += 1
    assert pares == 20


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
