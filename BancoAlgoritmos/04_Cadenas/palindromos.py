"""
Cadenas — Palíndromos: verificar y expansión desde el centro («Expand around center»)
Nivel: Básico
Ejecutar: python palindromos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir si una cadena se lee igual al derecho y al revés, y encontrar la
    subcadena palíndroma más larga (o contar todas) en O(n²) sin estructuras
    raras: suficiente para n ≤ ~3000 en Python.
    Señales en el enunciado: «se lee igual en ambos sentidos», «capicúa»,
    «simétrica»; «ignorando espacios / mayúsculas / puntuación» (hay que
    normalizar antes); «la subcadena palíndroma más larga» con n pequeño.
    Si n llega a 10^5–10^6, usar manacher.py.

FUNCIÓN
    es_palindromo(s) -> bool            dos punteros, O(n), memoria O(1)
    es_palindromo_reverso(s) -> bool    s == s[::-1] (lo más rápido en Python)
    normalizar(s) -> str                solo letras inglesas a-z en minúscula
    palindromo_mas_largo(s) -> (inicio, largo)
        Subcadena palíndroma más larga s[inicio:inicio+largo]; ante empate,
        la que empieza más a la izquierda. Para s vacía devuelve (0, 0).
    contar_palindromos(s) -> int
        Cantidad de pares (i, j) con s[i:j] palíndromo no vacío (cuenta
        posiciones, no subcadenas distintas).

IDEA Y ALGORITMO
    Verificar: s es palíndromo ⇔ s[i] == s[n-1-i] para todo i < n/2. Con dos
    punteros que se acercan desde los extremos basta la mitad de las
    comparaciones; en Python, s == s[::-1] hace lo mismo pero en C.
    Más largo: todo palíndromo tiene un CENTRO: un carácter (largo impar)
    o el hueco entre dos caracteres (largo par). Hay 2n-1 centros. Desde
    cada centro se expande mientras los extremos coincidan. Esto es correcto
    porque s[l..r] es palíndromo ⇔ s[l] == s[r] y s[l+1..r-1] lo es: si la
    expansión falla en un radio, ningún radio mayor con ese centro sirve.
    Así cada centro aporta TODOS sus palíndromos (uno por radio), lo que
    también sirve para contarlos.
    El ingenuo (probar las n² subcadenas y verificar cada una) es O(n³).

MACROALGORITMO
    1. (Si el enunciado lo pide) normalizar: filtrar letras y pasar a minúscula.
    2. Para cada centro c en 0..2n-2: l = c // 2, r = l + c % 2.
    3. Mientras l >= 0, r < n y s[l] == s[r]: contar un palíndromo, l -= 1, r += 1.
    4. Al parar, el palíndromo de ese centro es s[l+1 .. r-1] (largo r-l-1).
    5. Quedarse con el más largo (el primero en caso de empate).

COMPLEJIDAD
    Verificar: O(n). Más largo y contar: O(n²) peor caso (s = "aaaa…"),
    O(n) memoria. En Python, n ≈ 3000 en ~1 s en el peor caso.

EJEMPLO A MANO
    s = "abacdc": centros impares y pares, se muestra el radio alcanzado:
      centro 'b' (i=1): a|b|a coincide → "aba"; luego i-2 < 0, para. largo 3
      centro 'd' (i=4): c|d|c coincide → "cdc"; luego 'a' vs fin, para. largo 3
      ningún centro par expande (no hay letras iguales vecinas).
    Más largo: (0, 3) = "aba" (empata con "cdc", gana el de la izquierda).
    Contar: 6 de largo 1 + "aba" + "cdc" = 8.

ERRORES TÍPICOS
    - Olvidar los palíndromos de largo PAR (solo expandir desde caracteres).
    - Normalizar con str.isalpha(): acepta letras de otros alfabetos (á, ñ…);
      si el enunciado dice «letras inglesas», filtrar por rango a-z / A-Z.
    - Leer con input().strip() cuando los espacios son parte de la línea.
    - La cadena vacía (o sin letras tras normalizar) SÍ es palíndromo.

VARIANTES Y RELACIONADOS
    - Todos los palíndromos en O(n): manacher.py.
    - Consultas «¿s[i:j] es palíndromo?»: tabla DP pal[i][j] en O(n²) o
      hashing del texto y del reverso (hashing_polinomial.py) en O(1).
    - Mínimo número de cortes en palíndromos: DP O(n²) sobre esta expansión.
    - ¿Se puede reordenar en palíndromo? A lo más una letra con frecuencia
      impar (frecuencias_anagramas.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/J - Just Palindromes! (normalizar + comparar con el
      reverso; mismo problema en ICPC/Colombia 2026 Warmup/D)
    - LeetCode 5 «Longest Palindromic Substring», LeetCode 647
      «Palindromic Substrings»; CSES «Longest Palindrome» (con n = 10^6 ya
      exige Manacher)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las subcadenas) en 3000 casos
      aleatorios + casos borde (python palindromos.py)
"""
import random


def es_palindromo(s):
    """True si s se lee igual al derecho y al revés (dos punteros)."""
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True


def es_palindromo_reverso(s):
    """Misma respuesta comparando con el reverso: en Python es lo más rápido."""
    return s == s[::-1]


def normalizar(s):
    """Solo letras inglesas, en minúscula (no usar isalpha: acepta 'ñ', 'á'...)."""
    return "".join(c.lower() for c in s if "a" <= c <= "z" or "A" <= c <= "Z")


def palindromo_mas_largo(s):
    """(inicio, largo) de la subcadena palíndroma más larga; la más a la izquierda."""
    n = len(s)
    mejor_ini, mejor_largo = 0, 0
    # c recorre los 2n-1 centros: c par → centro en el carácter c//2 (largo
    # impar); c impar → centro en el hueco entre c//2 y c//2 + 1 (largo par).
    for c in range(2 * n - 1):
        l = c // 2
        r = l + c % 2
        while l >= 0 and r < n and s[l] == s[r]:
            l -= 1
            r += 1
        # Al salir, s[l+1 .. r-1] es el palíndromo máximo de este centro.
        largo = r - l - 1
        if largo > mejor_largo or (largo == mejor_largo and l + 1 < mejor_ini):
            mejor_ini, mejor_largo = l + 1, largo
    return mejor_ini, mejor_largo


def contar_palindromos(s):
    """Número de subcadenas palíndromas no vacías (contadas por posición)."""
    n = len(s)
    total = 0
    for c in range(2 * n - 1):
        l = c // 2
        r = l + c % 2
        # Cada paso exitoso de la expansión es un palíndromo distinto.
        while l >= 0 and r < n and s[l] == s[r]:
            total += 1
            l -= 1
            r += 1
    return total


def demo():
    s = "abacdc"
    print("s =", repr(s))
    i, k = palindromo_mas_largo(s)
    print("palindromo_mas_largo:", (i, k), "->", repr(s[i:i + k]))   # (0, 3) 'aba'
    print("contar_palindromos:", contar_palindromos(s))              # 8
    frase = "A man, a plan, a canal: Panama!"
    print(repr(frase), "normalizada:", repr(normalizar(frase)),
          "es palíndromo:", es_palindromo(normalizar(frase)))        # True


def pruebas():
    random.seed(2024)

    def mas_largo_bruto(s):
        n = len(s)
        mejor = (0, 0)
        for i in range(n):
            for j in range(i + 1, n + 1):
                t = s[i:j]
                if t == t[::-1] and (j - i > mejor[1] or (j - i == mejor[1] and i < mejor[0])):
                    mejor = (i, j - i)
        return mejor

    def contar_bruto(s):
        n = len(s)
        return sum(1 for i in range(n) for j in range(i + 1, n + 1) if s[i:j] == s[i:j][::-1])

    # Casos borde
    assert es_palindromo("") and es_palindromo_reverso("")
    assert es_palindromo("x") and es_palindromo("abba") and not es_palindromo("ab")
    assert palindromo_mas_largo("") == (0, 0)
    assert palindromo_mas_largo("z") == (0, 1)
    assert palindromo_mas_largo("aaaa") == (0, 4)
    assert palindromo_mas_largo("abcd") == (0, 1)
    assert contar_palindromos("") == 0 and contar_palindromos("aaa") == 6
    assert normalizar(".---.-") == "" and es_palindromo(normalizar(".---.-"))
    assert normalizar("Ñandú A-b") == "andab"   # ñ y ú no son letras inglesas

    # Aleatorios contra fuerza bruta
    for _ in range(3000):
        n = random.randint(0, 14)
        alfabeto = "ab" if random.random() < 0.6 else "abc"
        s = "".join(random.choice(alfabeto) for _ in range(n))
        assert es_palindromo(s) == es_palindromo_reverso(s) == (list(s) == list(reversed(s)))
        assert palindromo_mas_largo(s) == mas_largo_bruto(s)
        assert contar_palindromos(s) == contar_bruto(s)

    # Peor caso de tamaño moderado (todas iguales): n(n+1)/2 palíndromos
    s = "a" * 1500
    assert palindromo_mas_largo(s) == (0, 1500)
    assert contar_palindromos(s) == 1500 * 1501 // 2


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
