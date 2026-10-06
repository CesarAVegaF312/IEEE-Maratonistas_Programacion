"""
Cadenas — Algoritmo de Manacher («Manacher's algorithm»)
Nivel: Intermedio
Ejecutar: python manacher.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcula en O(n), para cada centro de la cadena, el radio del palíndromo
    más largo centrado allí. Con eso salen en tiempo lineal: la subcadena
    palíndroma más larga, el número total de subcadenas palíndromas y
    consultas «¿s[i:j] es palíndromo?» en O(1).
    Señales en el enunciado: palíndromos con n hasta 10^5–10^6 (la
    expansión desde el centro, O(n²), ya no alcanza); «contar subcadenas
    palíndromas»; «el palíndromo más largo que empieza / termina en i».

FUNCIÓN
    manacher(s) -> (d1, d2)
        d1[i] = número de palíndromos de largo IMPAR centrados en i
                (el más largo es s[i-d1[i]+1 : i+d1[i]], largo 2·d1[i]-1).
        d2[i] = número de palíndromos de largo PAR centrados entre i-1 e i
                (el más largo es s[i-d2[i] : i+d2[i]], largo 2·d2[i]).
    palindromo_mas_largo(s) -> (inicio, largo)   el más a la izquierda en empate
    contar_palindromos(s) -> int                 Σ d1 + Σ d2
    es_palindromo_rango(d1, d2, i, j) -> bool    ¿s[i:j] es palíndromo? en O(1)

IDEA Y ALGORITMO
    Se mantiene el palíndromo [l, r] que llega más a la derecha de todos los
    encontrados. Si i está dentro (i ≤ r), su espejo j = l + r - i también
    lo está, y como s[l..r] es palíndromo, alrededor de i se ve lo mismo
    que alrededor de j (reflejado) MIENTRAS no se salga de [l, r]. Por eso
    d1[i] ≥ min(d1[j], r - i + 1): se arranca desde ahí y solo se expande
    comparando caracteres más allá de r.
    ¿Por qué O(n)? Cada comparación exitosa de la expansión empuja r una
    posición a la derecha, y r nunca retrocede: a lo más n éxitos en total
    (más un fracaso por i). Igual que la caja de la función Z.
    Los palíndromos pares se tratan con d2 y el espejo l + r - i + 1 (o con
    el truco de intercalar '#': "aba" → "#a#b#a#", donde todos son impares).
    Consulta s[i:j]: el centro de [i, j) es fijo; es palíndromo ⇔ el
    palíndromo máximo de ese centro alcanza la mitad del largo.

MACROALGORITMO
    1. d1: l = 0, r = -1. Para i = 0..n-1:
    2.   k = 1 si i > r; si no, k = min(d1[l + r - i], r - i + 1).
    3.   Mientras s[i-k] == s[i+k] (dentro de rango): k += 1.
    4.   d1[i] = k; si i + k - 1 > r: l, r = i - k + 1, i + k - 1.
    5. d2: igual con k = 0 / min(d2[l + r - i + 1], r - i + 1), comparando
       s[i-k-1] con s[i+k] y actualizando l, r = i - k, i + k - 1.
    6. Más largo = máximo de 2·d1[i]-1 y 2·d2[i]; total = Σd1 + Σd2.

COMPLEJIDAD
    Tiempo O(n), memoria O(n). En Python, n = 10^6 en ~1,5 s (dos pasadas);
    n = 2·10^5 holgado.

EJEMPLO A MANO
    s = "abaaba" (posiciones 0..5)
      d1: i=0:1  i=1:2 ("aba")  i=2:1  i=3:1  i=4:2 ("aba")  i=5:1
      d2: i=3: s[2..3]="aa", s[1..4]="baab", s[0..5]="abaaba" → 3; los demás 0
          (en i=3, l=0, r=5: todo el texto es el palíndromo más a la derecha)
    Más largo: 2·d2[3] = 6 → (0, 6) "abaaba".
    Total: Σd1 = 8, Σd2 = 3 → 11 palíndromos.

ERRORES TÍPICOS
    - Mezclar convenciones: radio con o sin el centro, d2 centrado a la
      izquierda o a la derecha de i. Elegir una y respetarla en las fórmulas.
    - Olvidar el min con r - i + 1: el valor del espejo puede salirse del
      palíndromo [l, r] y ser falso para i.
    - Con el truco de '#', usar un separador que aparece en el texto (o
      olvidar dividir entre 2 al volver a la cadena original).
    - Escribir la expansión con recursión o sin chequear los bordes.

VARIANTES Y RELACIONADOS
    - Versión unificada intercalando separadores: un solo arreglo p.
    - Palíndromo más largo que es prefijo: mayor centro con d que toca 0
      (o KMP de s + '#' + rev(s)).
    - Contar palíndromos DISTINTOS: árbol de palíndromos (eertree).
    - Versión O(n²) sencilla: palindromos.py; consultas con hashing del
      reverso: hashing_polinomial.py.

DÓNDE PRACTICAR
    - CSES «Longest Palindrome» (n = 10^6); LeetCode 5 «Longest Palindromic
      Substring», 647 «Palindromic Substrings»
    - (No hay problema del repo ICPC que lo necesite: Colombia 2025/J solo
      verifica la cadena completa.)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (verificar cada subcadena) en 2000
      cadenas aleatorias, incluidas todas sus consultas s[i:j], + casos
      borde (python manacher.py)
"""
import random


def manacher(s):
    """d1[i]: palíndromos impares centrados en i; d2[i]: pares centrados entre i-1 e i."""
    n = len(s)
    d1 = [0] * n
    l, r = 0, -1                    # palíndromo impar que llega más a la derecha
    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)   # espejo, recortado a [l, r]
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        if i + k - 1 > r:
            l, r = i - k + 1, i + k - 1
    d2 = [0] * n
    l, r = 0, -1                    # palíndromo par que llega más a la derecha
    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        if i + k - 1 > r:
            l, r = i - k, i + k - 1
    return d1, d2


def palindromo_mas_largo(s):
    """(inicio, largo) del palíndromo más largo; ante empate, el de menor inicio."""
    if not s:
        return (0, 0)
    d1, d2 = manacher(s)
    candidatos = [(-(2 * d1[i] - 1), i - d1[i] + 1) for i in range(len(s))]
    candidatos += [(-2 * d2[i], i - d2[i]) for i in range(len(s)) if d2[i]]
    largo_neg, inicio = min(candidatos)
    return (inicio, -largo_neg)


def contar_palindromos(s):
    """Número de subcadenas palíndromas no vacías (por posición)."""
    d1, d2 = manacher(s)
    return sum(d1) + sum(d2)


def es_palindromo_rango(d1, d2, i, j):
    """¿s[i:j] es palíndromo? (vacía cuenta como palíndromo)."""
    L = j - i
    if L <= 0:
        return True
    if L % 2:
        return d1[(i + j - 1) // 2] >= (L + 1) // 2     # centro en el carácter del medio
    return d2[(i + j) // 2] >= L // 2                   # centro entre (i+j)/2 - 1 y (i+j)/2


def demo():
    s = "abaaba"
    d1, d2 = manacher(s)
    print("s =", s)
    print("d1 =", d1)                                       # [1, 2, 1, 1, 2, 1]
    print("d2 =", d2)                                       # [0, 0, 0, 3, 0, 0]
    print("palindromo_mas_largo:", palindromo_mas_largo(s))  # (0, 6)
    print("contar_palindromos:", contar_palindromos(s))      # 11
    print("¿s[1:5] = 'baab' es palíndromo?", es_palindromo_rango(d1, d2, 1, 5))  # True
    print("¿s[0:4] = 'abaa' es palíndromo?", es_palindromo_rango(d1, d2, 0, 4))  # False


def pruebas():
    random.seed(1975)

    def mas_largo_bruto(s):
        mejor = (0, 0)
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                if s[i:j] == s[i:j][::-1] and (j - i > mejor[1]):
                    mejor = (i, j - i)
        return mejor

    # Casos borde
    assert manacher("") == ([], []) and palindromo_mas_largo("") == (0, 0)
    assert manacher("a") == ([1], [0]) and contar_palindromos("a") == 1
    assert palindromo_mas_largo("ab") == (0, 1)
    assert contar_palindromos("aaaa") == 10

    for _ in range(2000):
        alfabeto = random.choice(["a", "ab", "abc"])
        s = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 16)))
        n = len(s)
        d1, d2 = manacher(s)
        # Definición directa de d1 y d2
        for i in range(n):
            assert d1[i] == max(k for k in range(1, n + 1)
                                if i - k + 1 >= 0 and i + k <= n
                                and s[i - k + 1:i + k] == s[i - k + 1:i + k][::-1])
            assert d2[i] == max(k for k in range(0, n + 1)
                                if i - k >= 0 and i + k <= n
                                and s[i - k:i + k] == s[i - k:i + k][::-1])
        assert palindromo_mas_largo(s) == mas_largo_bruto(s)
        total = 0
        for i in range(n + 1):
            for j in range(i, n + 1):
                es = s[i:j] == s[i:j][::-1]
                assert es_palindromo_rango(d1, d2, i, j) == es
                total += es and j > i
        assert contar_palindromos(s) == total

    # Grande: 2·10^5, peor caso para la expansión ingenua
    s = "a" * 200000
    assert palindromo_mas_largo(s) == (0, 200000)
    assert contar_palindromos(s) == 200000 * 200001 // 2
    s = "".join(random.choice("ab") for _ in range(100000))
    s = s + s[::-1]
    assert palindromo_mas_largo(s)[1] == 200000


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
