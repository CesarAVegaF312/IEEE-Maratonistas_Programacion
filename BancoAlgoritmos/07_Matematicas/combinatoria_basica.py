"""
Matemáticas — Combinatoria básica: factoriales, variaciones, combinaciones y Pascal
Nivel: Básico
Ejecutar: python combinatoria_basica.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Contar de cuántas formas se pueden ordenar o escoger objetos sin
    enumerarlos: permutaciones (n!), variaciones (ordenar k de n),
    combinaciones (escoger k de n sin orden), con y sin repetición, y
    permutaciones de multiconjuntos (multinomial).
    Cómo reconocerlo: «¿de cuántas formas…?», «cuántos subconjuntos de
    tamaño k», «cuántos caminos en una cuadrícula», «cuántas palabras con
    estas letras»; respuestas enormes (en Python no hay desborde; en C++ se
    pediría módulo, ver ncr_modular.py).

FUNCIÓN
    factorial(n) -> int                      n! (0! = 1)
    variaciones(n, k) -> int                 n·(n-1)···(n-k+1) (0 si k > n)
    combinaciones(n, k) -> int               C(n, k) (0 si k < 0 o k > n)
    triangulo_pascal(n) -> list[list[int]]   filas 0..n, fila i = C(i, 0..i)
    multinomial(ks) -> int                   (k1+…+km)! / (k1!···km!)
    En Python: math.factorial, math.perm(n, k), math.comb(n, k) hacen lo mismo
    en C y son lo que se debe usar en competencia. Aquí se implementan para
    entender de dónde salen.

IDEA Y ALGORITMO
    Principio del producto: si una elección se hace en pasos y el paso i
    tiene a_i opciones (sin importar lo elegido antes), el total es Π a_i.
    - Permutaciones de n: n opciones para el 1.º, n-1 para el 2.º… → n!.
    - Variaciones V(n, k) (ordenar k de n): n·(n-1)···(n-k+1) = n!/(n-k)!.
    - Combinaciones C(n, k): cada subconjunto de k elementos aparece k! veces
      entre las V(n, k) listas ordenadas (una por cada orden), así que
      C(n, k) = V(n, k) / k! = n! / (k!(n-k)!).
    - Pascal C(n, k) = C(n-1, k-1) + C(n-1, k): fijado el elemento n, los
      subconjuntos que lo contienen son C(n-1, k-1) y los que no, C(n-1, k).
    - Fórmula multiplicativa sin números gigantes intermedios:
        r_0 = 1,  r_i = r_{i-1} · (n-k+i) / i,  con r_i = C(n-k+i, i).
      Cada división es EXACTA porque r_i es un entero (es un binomial).
      Por simetría C(n, k) = C(n, n-k): usar k = min(k, n-k).
    - Con repetición: palabras de longitud k sobre n símbolos = n^k;
      multiconjuntos de tamaño k sobre n tipos = C(n+k-1, k) (estrellas y
      barras, ver estrellas_barras.py).
    - Multinomial: ordenar n objetos donde hay k_1 iguales de un tipo, k_2 de
      otro…: n! cuenta todos como distintos y cada palabra se repite
      k_1!·k_2!··· veces (permutar los iguales entre sí no la cambia).
      Equivale a Π C(k_1+…+k_i, k_i) (ir colocando un tipo a la vez).

MACROALGORITMO
    1. Identificar si el orden importa (variación) o no (combinación).
    2. Identificar si se puede repetir (n^k, C(n+k-1, k)) o no.
    3. Si hay objetos idénticos, dividir por el factorial de cada grupo
       (multinomial).
    4. Calcular con math.comb / math.perm, o con la tabla de Pascal si se
       necesitan muchos C(i, j) pequeños.
    5. Si hay módulo primo y n grande, usar factoriales precomputados
       (ncr_modular.py).

COMPLEJIDAD
    combinaciones(n, k): O(min(k, n-k)) multiplicaciones de enteros grandes.
    triangulo_pascal(n): O(n²) tiempo y memoria (n ≈ 3000 en ~1 s).
    math.comb(10^5, 5·10^4) (≈30 000 dígitos) tarda unos milisegundos.

EJEMPLO A MANO
    C(5, 2) multiplicativo con k=2: r1 = 1·4/1 = 4, r2 = 4·5/2 = 10.
    Pascal fila 5: 1 5 10 10 5 1 (10 = 4 + 6 de la fila 4: 1 4 6 4 1).
    V(5, 2) = 5·4 = 20 = C(5,2)·2!.  Palabra «BANANA»: 6!/(1!·3!·2!) = 60.
    Caminos monótonos en cuadrícula 3×2 (3 a la derecha, 2 arriba): C(5,2) = 10.

ERRORES TÍPICOS
    - Calcular n! / (k!(n-k)!) con flotantes (pierde precisión): usar enteros
      y división entera //, o math.comb.
    - Hacer la división de la fórmula multiplicativa al final en vez de en
      cada paso (funciona en Python pero produce números enormes; en C++
      desborda) o en otro orden (r·i/(n-k+i) NO es exacta).
    - Olvidar los casos k < 0 o k > n (deben dar 0, no error).
    - Confundir «con orden» y «sin orden»: si el problema dice «grupos» o
      «subconjuntos» casi siempre es sin orden.

VARIANTES Y RELACIONADOS
    - ncr_modular.py (C(n, k) mód p para n hasta 10^6–10^7 y Lucas).
    - estrellas_barras.py (repartir objetos idénticos en cajas).
    - conteo_complemento.py, inclusion_exclusion.py (contar con restricciones).
    - catalan.py, rango_combinacion.py (ranking/unranking de combinaciones).
    - Identidades útiles: Σ_k C(n,k) = 2^n; Vandermonde
      Σ_j C(a,j)·C(b,k-j) = C(a+b, k); «hockey stick» Σ_{i=r}^{n} C(i,r) = C(n+1,r+1).

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/D - Discrete Catalog (sumas de math.comb para el rango)
    - ICPC/Guangzhou 2017/F - Finding Paths (multinomial + C(s,n)·C(s,m)·C(s,k))
    - CSES «Creating Strings II» (multinomial), «Binomial Coefficients»

VERIFICACIÓN
    - Pruebas: OK contra enumeración con itertools (permutations,
      combinations, product, combinations_with_replacement, permutaciones
      distintas de un multiconjunto) para n ≤ 7, contra math.comb/math.perm
      para n ≤ 60 y la identidad de Pascal (python combinatoria_basica.py)
"""
import itertools
import math
import random


def factorial(n):
    """n! iterativo (0! = 1)."""
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def variaciones(n, k):
    """Listas ordenadas de k elementos distintos tomados de n: n!/(n-k)!."""
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(n - k + 1, n + 1):
        r *= i
    return r


def combinaciones(n, k):
    """C(n, k) con la fórmula multiplicativa (división exacta en cada paso)."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)               # simetría: menos iteraciones
    r = 1
    for i in range(1, k + 1):
        # Invariante: tras este paso r = C(n-k+i, i), que es entero,
        # por eso la división // es exacta (multiplicar ANTES de dividir).
        r = r * (n - k + i) // i
    return r


def triangulo_pascal(n):
    """Filas 0..n del triángulo de Pascal: fila[i][j] = C(i, j)."""
    filas = [[1]]
    for i in range(1, n + 1):
        prev = filas[-1]
        # Cada interior es la suma de los dos de arriba (con o sin el elemento i).
        fila = [1] + [prev[j - 1] + prev[j] for j in range(1, i)] + [1]
        filas.append(fila)
    return filas


def multinomial(ks):
    """(k1+…+km)! / (k1!···km!) como producto de binomiales (sin fracciones)."""
    r, total = 1, 0
    for k in ks:
        total += k
        r *= combinaciones(total, k)   # elegir dónde van los k del tipo nuevo
    return r


def demo():
    print("C(5, 2) =", combinaciones(5, 2))                    # 10
    print("V(5, 2) =", variaciones(5, 2))                      # 20
    print("Pascal fila 5:", triangulo_pascal(5)[5])            # [1, 5, 10, 10, 5, 1]
    print("anagramas de BANANA =", multinomial([1, 3, 2]))     # 60
    print("caminos en cuadrícula 3x2 =", combinaciones(5, 2))  # 10
    print("multiconjuntos de 3 sobre 4 tipos =", combinaciones(4 + 3 - 1, 3))  # 20


def pruebas():
    random.seed(2024)

    # Casos borde
    assert factorial(0) == 1 and factorial(1) == 1
    assert combinaciones(0, 0) == 1 and combinaciones(5, -1) == 0 and combinaciones(3, 4) == 0
    assert variaciones(0, 0) == 1 and variaciones(3, 4) == 0
    assert multinomial([]) == 1 and multinomial([0, 0]) == 1

    # Contra enumeración explícita (n pequeño)
    for n in range(0, 8):
        u = range(n)
        assert factorial(n) == sum(1 for _ in itertools.permutations(u))
        for k in range(0, n + 2):
            assert variaciones(n, k) == sum(1 for _ in itertools.permutations(u, k))
            assert combinaciones(n, k) == sum(1 for _ in itertools.combinations(u, k))
            if k <= 4:
                assert n ** k == sum(1 for _ in itertools.product(u, repeat=k))
                if n > 0:
                    cr = sum(1 for _ in itertools.combinations_with_replacement(u, k))
                    assert cr == combinaciones(n + k - 1, k)

    # Multinomial contra permutaciones distintas de un multiconjunto
    for _ in range(200):
        ks = [random.randint(0, 3) for _ in range(random.randint(1, 3))]
        palabra = [t for t, k in enumerate(ks) for _ in range(k)]
        assert multinomial(ks) == len(set(itertools.permutations(palabra)))

    # Contra math.comb / math.perm y Pascal
    pas = triangulo_pascal(60)
    for n in range(0, 61):
        for k in range(0, n + 1):
            assert combinaciones(n, k) == math.comb(n, k) == pas[n][k]
            assert variaciones(n, k) == math.perm(n, k)
    for _ in range(300):
        n = random.randint(0, 2000)
        k = random.randint(0, n)
        assert combinaciones(n, k) == math.comb(n, k)
    assert sum(pas[20]) == 2 ** 20


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
