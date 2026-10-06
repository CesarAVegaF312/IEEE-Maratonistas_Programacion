"""
Cadenas — Frecuencias de letras y anagramas («Anagrams»)
Nivel: Básico
Ejecutar: python frecuencias_anagramas.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Contar cuántas veces aparece cada letra resuelve todo lo que «no depende
    del orden»: decidir si dos palabras son anagramas, agrupar palabras con
    las mismas letras, encontrar ventanas de un texto que son permutación de
    un patrón, o saber si se puede formar una palabra con otras letras.
    Señales en el enunciado: «reordenando las letras», «anagrama»,
    «permutación de la cadena», «con las mismas letras», «¿se puede formar…
    usando las fichas?», «sin importar el orden».

FUNCIÓN
    frecuencias(s) -> list[int]          26 contadores (a..z); s en minúsculas
    son_anagramas(a, b) -> bool           mismas letras con las mismas veces
    agrupar_anagramas(palabras) -> list[list[str]]
        Grupos en orden de primera aparición; dentro de cada grupo, las
        palabras en el orden de entrada.
    ventanas_anagrama(texto, patron) -> list[int]
        Índices i tales que texto[i:i+|patron|] es anagrama de patron.
    se_puede_formar(palabra, fichas) -> bool
        ¿Alcanzan las letras de fichas (cada una se usa una vez)?

IDEA Y ALGORITMO
    Dos cadenas son anagramas ⇔ tienen el mismo MULTICONJUNTO de letras
    ⇔ el mismo vector de frecuencias ⇔ la misma versión ordenada. Esa
    "forma canónica" (tupla de 26 contadores, o sorted(s)) es idéntica para
    todas las palabras del grupo y distinta entre grupos, así que sirve
    como clave de diccionario para agrupar en una pasada.
    Ventanas: al deslizar la ventana un paso, solo cambian dos contadores
    (entra una letra, sale otra). Se mantiene «cuántas de las 26 letras
    tienen la frecuencia correcta»; la ventana es anagrama cuando son 26.
    Así cada paso es O(1) y no O(26) ni O(m).
    El ingenuo (probar permutaciones) es O(m!) y ni siquiera es necesario.

MACROALGORITMO
    1. Anagramas: comparar frecuencias(a) == frecuencias(b) (o Counter).
    2. Agrupar: clave = tuple(frecuencias(p)) (o "".join(sorted(p))); un
       diccionario clave → lista de palabras.
    3. Ventanas: contar el patrón y la primera ventana; iguales = letras con
       la misma cuenta en ambos.
    4. Deslizar: quitar texto[i-m], agregar texto[i]; antes y después de
       cada cambio ajustar «iguales» para esa letra.
    5. Si iguales == 26, la ventana actual es anagrama.

COMPLEJIDAD
    frecuencias / son_anagramas: O(n). Agrupar: O(Σ|p|) con la tupla de
    frecuencias (O(Σ|p| log|p|) con sorted). Ventanas: O(|texto| + 26).
    En Python, 10^6 caracteres por segundo sin problema.

EJEMPLO A MANO
    palabras = ["eat", "tea", "tan", "ate", "nat", "bat"]
    claves (sorted): aet, aet, ant, aet, ant, abt
    grupos: [eat, tea, ate], [tan, nat], [bat]
    ventanas_anagrama("cbaebabacd", "abc"): ventanas "cba" (i=0) y "bac"
    (i=6) → [0, 6]

ERRORES TÍPICOS
    - Usar la lista de frecuencias como clave de dict: las listas no son
      hashables; convertir a tupla.
    - Restar ord('a') a letras mayúsculas o dígitos: índice fuera de rango.
      Normalizar antes o usar collections.Counter.
    - En la ventana deslizante, recalcular las 26 letras en cada paso: pasa
      a O(26·n), que en Python sí se nota con n = 10^6.
    - Olvidar que las cadenas de distinto largo nunca son anagramas.

VARIANTES Y RELACIONADOS
    - ¿Se puede reordenar en palíndromo? ⇔ a lo más una letra con
      frecuencia impar (palindromos.py).
    - Firma por bits (máscara de paridades) cuando solo importa par/impar.
    - Hash de multiconjunto (suma de valores aleatorios por letra) para
      comparar ventanas sin contar: ver hashing_polinomial.py.
    - Contar permutaciones distintas: n! / Π(frecuencia_c!).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/C - Carrol's Scrabble (cubetas de anagramas con la
      palabra ordenada como clave + BFS)
    - LeetCode 242 «Valid Anagram», 49 «Group Anagrams», 438 «Find All
      Anagrams in a String»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (sorted / Counter / probar cada
      ventana) en 3000 casos aleatorios + casos borde
      (python frecuencias_anagramas.py)
"""
import random
from collections import Counter


def frecuencias(s):
    """26 contadores: cuántas veces aparece cada letra 'a'..'z' en s."""
    f = [0] * 26
    for c in s:
        f[ord(c) - 97] += 1
    return f


def son_anagramas(a, b):
    """True si a y b tienen exactamente las mismas letras (con repetición)."""
    return len(a) == len(b) and frecuencias(a) == frecuencias(b)


def agrupar_anagramas(palabras):
    """Agrupa palabras con la misma clave canónica (tupla de frecuencias)."""
    grupos = {}                 # clave -> lista de palabras (dict conserva el orden)
    for p in palabras:
        grupos.setdefault(tuple(frecuencias(p)), []).append(p)
    return list(grupos.values())


def ventanas_anagrama(texto, patron):
    """Inicios i con texto[i:i+m] anagrama de patron (m = |patron|), en O(n)."""
    n, m = len(texto), len(patron)
    if m > n:
        return []
    objetivo = frecuencias(patron)
    actual = frecuencias(texto[:m])
    # iguales = cuántas letras tienen ya la misma cuenta en ventana y patrón.
    iguales = sum(1 for k in range(26) if actual[k] == objetivo[k])
    res = [0] if iguales == 26 else []
    for i in range(m, n):
        # Sale texto[i-m] y entra texto[i]; cada cambio toca una sola letra.
        for c, delta in ((ord(texto[i - m]) - 97, -1), (ord(texto[i]) - 97, +1)):
            if actual[c] == objetivo[c]:
                iguales -= 1        # deja de estar bien...
            actual[c] += delta
            if actual[c] == objetivo[c]:
                iguales += 1        # ...o vuelve a estarlo
        if iguales == 26:
            res.append(i - m + 1)
    return res


def se_puede_formar(palabra, fichas):
    """¿Cada letra de palabra aparece en fichas al menos esas veces?"""
    disp = Counter(fichas)
    return all(disp[c] >= k for c, k in Counter(palabra).items())


def demo():
    palabras = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print("palabras =", palabras)
    print("agrupar_anagramas:", agrupar_anagramas(palabras))
    # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    print("son_anagramas('listen', 'silent'):", son_anagramas("listen", "silent"))  # True
    print("ventanas_anagrama('cbaebabacd', 'abc'):",
          ventanas_anagrama("cbaebabacd", "abc"))                                  # [0, 6]
    print("se_puede_formar('hola', 'aloha'):", se_puede_formar("hola", "aloha"))   # True


def pruebas():
    random.seed(77)

    def agrupar_bruto(palabras):
        # O(n²): cada palabra se compara con el representante de cada grupo.
        grupos = []
        for p in palabras:
            for g in grupos:
                if sorted(g[0]) == sorted(p):
                    g.append(p)
                    break
            else:
                grupos.append([p])
        return grupos

    # Casos borde
    assert son_anagramas("", "") and not son_anagramas("a", "")
    assert not son_anagramas("ab", "abb")
    assert agrupar_anagramas([]) == []
    assert agrupar_anagramas(["", ""]) == [["", ""]]
    assert ventanas_anagrama("", "") == [0]
    assert ventanas_anagrama("ab", "abc") == []
    assert ventanas_anagrama("aaaa", "aa") == [0, 1, 2]
    assert se_puede_formar("", "") and not se_puede_formar("aa", "a")

    for _ in range(3000):
        alfabeto = random.choice(["ab", "abc", "abcz"])
        a = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 6)))
        b = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 6)))
        assert son_anagramas(a, b) == (sorted(a) == sorted(b))
        assert se_puede_formar(a, b) == all(a.count(c) <= b.count(c) for c in a)

        palabras = ["".join(random.choice(alfabeto) for _ in range(random.randint(0, 4)))
                    for _ in range(random.randint(0, 10))]
        assert agrupar_anagramas(palabras) == agrupar_bruto(palabras)

        texto = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 15)))
        patron = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 4)))
        m = len(patron)
        esperado = [i for i in range(len(texto) - m + 1) if sorted(texto[i:i + m]) == sorted(patron)]
        assert ventanas_anagrama(texto, patron) == esperado

    # Texto grande: la ventana deslizante debe ir en tiempo lineal
    texto = "".join(random.choice("ab") for _ in range(200000))
    assert len(ventanas_anagrama(texto, "aabb")) == sum(
        1 for i in range(len(texto) - 3) if texto[i:i + 4].count("a") == 2)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
