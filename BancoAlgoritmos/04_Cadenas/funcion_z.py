"""
Cadenas — Función Z y búsqueda de patrones («Z-function / Z-algorithm»)
Nivel: Intermedio
Ejecutar: python funcion_z.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcula, para CADA posición i de una cadena, cuánto coincide s[i:] con
    el comienzo de s. Con eso se buscan patrones en O(|T| + |P|) y, sobre
    todo, se obtiene el prefijo común entre el patrón y CADA sufijo del
    texto (lo que KMP no da directamente): «¿cuántos caracteres de P
    coinciden empezando en i?». Aplicada al reverso da sufijos comunes.
    Señales en el enunciado: buscar un patrón con |T| hasta 10^6;
    «coincide salvo un bloque / salvo k posiciones contiguas»; «el prefijo
    más largo de P que aparece en la posición i»; bordes y periodos.

FUNCIÓN
    funcion_z(s) -> list[int]
        z[i] = largo del prefijo común más largo entre s y s[i:]; por
        convención z[0] = n (otras fuentes ponen 0). s vacía → [].
    lcp_con_patron(texto, patron) -> list[int]
        l[i] = largo del prefijo común de texto[i:] y patron (≤ |patron|).
    z_buscar(texto, patron) -> list[int]
        Inicios de todas las apariciones (solapadas incluidas); patrón vacío
        → 0..|T|.
    periodo_minimo_z(s) -> int    menor p con i + z[i] == n (n si no hay)
    Funcionan con str, list o tuple.

IDEA Y ALGORITMO
    Se mantiene la «caja Z» [l, r): el segmento s[l:r] más a la derecha
    encontrado que coincide con un prefijo de s (s[l:r] == s[0:r-l]).
    Para una nueva i < r, s[i:r] es copia de s[i-l : r-l], así que ya se
    sabe que z[i] ≥ min(z[i-l], r-i): se arranca desde ese valor sin
    comparar. Solo se compara más allá de r, y cada comparación exitosa
    mueve r hacia la derecha; como r nunca retrocede y llega a lo más a n,
    el total es O(n).
    Búsqueda: z de patron + [separador] + texto; en la posición m+1+i del
    texto, z vale el prefijo común de texto[i:] y patron (el separador,
    que no está en ninguno, corta la comparación en |patron|). Hay
    aparición en i ⇔ ese valor es |patron|.
    Periodo: s tiene periodo p ⇔ s[p:] == s[:n-p] ⇔ z[p] == n - p.
    El ingenuo compara desde cada i: O(n²) en "aaaa…a".

MACROALGORITMO
    1. z = [0]*n, z[0] = n, l = r = 0.
    2. Para i = 1..n-1: si i < r, z[i] = min(r - i, z[i - l]).
    3. Mientras i + z[i] < n y s[z[i]] == s[i + z[i]]: z[i] += 1.
    4. Si i + z[i] > r: l, r = i, i + z[i] (nueva caja más a la derecha).
    5. Búsqueda: s = P + [sep] + T; apariciones donde z[m+1+i] == m.

COMPLEJIDAD
    Tiempo O(n), memoria O(n). En Python, ~10^6 caracteres en ~0,5–1 s.

EJEMPLO A MANO
    s = "aabxaab" (n = 7)
      i=1: fuera de caja; s[0]=s[1]='a', s[1]='a'≠s[2]='b' → z=1, caja [1,2)
      i=2: fuera; 'a'≠'b' → z=0
      i=3: 'a'≠'x' → z=0
      i=4: 'aab' = 'aab', luego fin → z=3, caja [4,7)
      i=5: dentro: min(r-i=2, z[1]=1) = 1; s[1]='a' vs s[6]='b' ≠ → z=1
      i=6: dentro: min(1, z[2]=0) = 0; 'a' vs 'b' → z=0
    z = [7, 1, 0, 0, 3, 1, 0]
    z_buscar("abacaba", "aba") = [0, 4]

ERRORES TÍPICOS
    - Usar como separador un carácter que sí aparece en el texto: valores
      de z mayores que |P| y apariciones falsas o perdidas. Aquí se usa
      None en una lista, que nunca es igual a un carácter ni a un número.
    - Olvidar la convención de z[0] (n o 0) y usarlo en una fórmula.
    - Al estar dentro de la caja, no tomar el mínimo con r - i: el valor
      copiado puede «salirse» de la caja y ser falso.
    - Recalcular z para cada consulta en vez de una vez para todo el texto.

VARIANTES Y RELACIONADOS
    - Sufijo común de P con T[..j]: z de rev(P) + sep + rev(T).
    - «T[i:i+m] coincide con P salvo un bloque de largo K»: prefijo común
      (z directa) + sufijo común (z del reverso) ≥ m - K.
    - Subcadenas distintas en O(n²): agregar letra por letra y usar z del
      reverso para saber cuántas son nuevas.
    - Equivalente a la función prefijo: kmp.py. Para comparar subcadenas
      arbitrarias: hashing_polinomial.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/J - Romeo and Juliet Secrets (Z directa y del
      reverso para prefijo y sufijo común con cada ventana)
    - CSES «String Matching», «Finding Borders», «Finding Periods»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (comparar carácter a carácter desde
      cada posición) en 3000 casos aleatorios + casos borde + listas de
      números (python funcion_z.py)
"""
import random


def funcion_z(s):
    """z[i] = prefijo común más largo de s y s[i:] (z[0] = n)."""
    n = len(s)
    if n == 0:
        return []
    z = [0] * n
    z[0] = n
    l = r = 0                       # caja Z: s[l:r] == s[0:r-l], r máximo visto
    for i in range(1, n):
        if i < r:
            # Dentro de la caja: s[i:r] es copia de s[i-l:r-l].
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def lcp_con_patron(texto, patron):
    """l[i] = prefijo común de texto[i:] y patron, para cada i."""
    m = len(patron)
    # None como separador: no es igual a ningún carácter ni número.
    z = funcion_z(list(patron) + [None] + list(texto))
    return z[m + 1:]


def z_buscar(texto, patron):
    """Inicios de todas las apariciones de patron en texto."""
    m = len(patron)
    return [i for i, v in enumerate(lcp_con_patron(texto, patron)) if v == m] + \
        ([len(texto)] if m == 0 else [])


def periodo_minimo_z(s):
    """Menor p ≥ 1 con s[p:] == s[:n-p] (es decir, i + z[i] == n)."""
    n = len(s)
    z = funcion_z(s)
    for p in range(1, n):
        if p + z[p] == n:
            return p
    return n


def demo():
    s = "aabxaab"
    print("s =", s)
    print("funcion_z:", funcion_z(s))                                   # [7, 1, 0, 0, 3, 1, 0]
    print("z_buscar('abacaba', 'aba'):", z_buscar("abacaba", "aba"))    # [0, 4]
    print("lcp_con_patron('abacaba', 'abd'):", lcp_con_patron("abacaba", "abd"))
    # [2, 0, 1, 0, 2, 0, 1]
    print("periodo_minimo_z('abcabca') =", periodo_minimo_z("abcabca"))  # 3


def pruebas():
    random.seed(555)

    def lcp(a, b):
        k = 0
        while k < len(a) and k < len(b) and a[k] == b[k]:
            k += 1
        return k

    # Casos borde
    assert funcion_z("") == [] and funcion_z("a") == [1]
    assert funcion_z("aaaa") == [4, 3, 2, 1]
    assert z_buscar("", "") == [0] and z_buscar("abc", "") == [0, 1, 2, 3]
    assert z_buscar("", "a") == [] and z_buscar("ab", "abc") == []
    assert periodo_minimo_z("") == 0 and periodo_minimo_z("ab") == 2
    # Texto con '#': el separador None no se confunde
    assert z_buscar("a#a#a", "a#a") == [0, 2]
    assert z_buscar([3, 1, 3, 1, 3], [3, 1, 3]) == [0, 2]

    for _ in range(3000):
        alfabeto = random.choice(["a", "ab", "abc", "a#"])
        s = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 14)))
        p = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 4)))
        n, m = len(s), len(p)
        assert funcion_z(s) == [lcp(s, s[i:]) for i in range(n)]
        assert lcp_con_patron(s, p) == [lcp(s[i:], p) for i in range(n)]
        assert z_buscar(s, p) == [i for i in range(n - m + 1) if s[i:i + m] == p]
        assert periodo_minimo_z(s) == min([q for q in range(1, n + 1)
                                           if all(s[i] == s[i + q] for i in range(n - q))],
                                          default=0)

    # Grande y peor caso para el ingenuo
    s = "a" * 300000
    z = funcion_z(s)
    assert z[1] == 299999 and z[-1] == 1
    assert len(z_buscar(s, "a" * 500)) == 300000 - 500 + 1


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
