"""
Matemáticas — Principio de inclusión–exclusión («inclusion–exclusion principle»)
Nivel: Intermedio
Ejecutar: python inclusion_exclusion.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Contar elementos de una UNIÓN de conjuntos que se solapan, sabiendo
    contar fácilmente las INTERSECCIONES: |A1 ∪ … ∪ Am|. Por complemento,
    también los que no están en ninguno.
    Cómo reconocerlo: «divisible por al menos uno de…», «que no sea múltiplo
    de ninguno de…», «ningún elemento en su posición original»
    (desarreglos), «que use todos los colores / cada caja con al menos uno»
    (sobreyecciones), «al menos uno de cada tipo»; m pequeño (≤ 20) para
    recorrer los 2^m subconjuntos, o simetría que agrupe por tamaño.

FUNCIÓN
    multiplos_de_alguno(n, nums) -> int
        Cantidad de x en [1, n] divisibles por al menos uno de nums.
    desarreglos(n) -> int
        Permutaciones de n sin puntos fijos: D(n) = Σ_i (−1)^i C(n,i) (n−i)!.
    sobreyecciones(n, k) -> int
        Funciones de un conjunto de n a uno de k que cubren todo el destino:
        Σ_i (−1)^i C(k,i) (k−i)^n.   (S(n,k) de Stirling = esto / k!.)

IDEA Y ALGORITMO
    Fórmula: |A1 ∪ … ∪ Am| = Σ_{∅≠S⊆[m]} (−1)^{|S|+1} |∩_{i∈S} Ai|.
    Prueba: tome un elemento x que está en exactamente t ≥ 1 de los
    conjuntos. Aparece en la intersección de S solo si S ⊆ (esos t), así que
    la fórmula lo cuenta Σ_{j=1}^{t} (−1)^{j+1} C(t, j) = 1 − (1 − 1)^t = 1
    vez (binomio de Newton). Un elemento en ningún conjunto se cuenta 0
    veces. Así que la suma cuenta exactamente la unión.
    Versión «ninguno»: |U| − |unión| = Σ_{S⊆[m]} (−1)^{|S|} |∩_S Ai| (S = ∅
    da |U|).
    Simetría: si |∩_S Ai| solo depende de |S| = j, la suma colapsa a
    Σ_j (−1)^j C(m, j) f(j), en O(m) en vez de O(2^m):
    - desarreglos: Ai = «i queda fijo»; fijar j puntos deja (n−j)!.
    - sobreyecciones: Ai = «el valor i no se usa»; prohibir j valores deja
      (k−j)^n funciones.
    - múltiplos: ∩_S Ai = múltiplos de lcm(S): ⌊n / lcm(S)⌋. Si lcm(S) > n
      la intersección es vacía y todo superconjunto también → se poda.

MACROALGORITMO
    1. Definir los conjuntos «malos» Ai (o «buenos» cuya unión se pide).
    2. Encontrar cómo contar |∩_{i∈S} Ai| para un S cualquiera.
    3. Recorrer los subconjuntos S (máscaras 1..2^m − 1, o DFS con poda),
       sumando con signo (−1)^{|S|+1}.
    4. Si la intersección solo depende de |S|, agrupar por tamaño con C(m, j).
    5. Para «ninguno» restar del total (o incluir S = ∅ con signo +).

COMPLEJIDAD
    General O(2^m · costo(intersección)); con m = 20 son 10^6 términos
    (~1 s en Python). Con simetría O(m). Desarreglos/sobreyecciones: O(n)
    o O(k log n) operaciones con enteros grandes.

EJEMPLO A MANO
    Múltiplos de 2 o 3 en [1, 10]: ⌊10/2⌋ + ⌊10/3⌋ − ⌊10/6⌋ = 5 + 3 − 1 = 7
    (2,3,4,6,8,9,10).
    D(4) = 4! − C(4,1)3! + C(4,2)2! − C(4,3)1! + C(4,4)0! = 24−24+12−4+1 = 9.
    Sobreyecciones 3 → 2: 2^3 − 2·1^3 + 0 = 6.

ERRORES TÍPICOS
    - Signo invertido (los conjuntos de tamaño impar suman en la unión).
    - Usar el producto de los números en vez del lcm cuando no son coprimos
      (múltiplos de 4 y 6 → lcm 12, no 24).
    - Desbordar el lcm (en C++): podar en cuanto pase de n.
    - Olvidar el término S = ∅ en la versión «ninguno».
    - Con módulo, (−1)^j se suma como p − x (en Python % lo arregla).

VARIANTES Y RELACIONADOS
    - conteo_complemento.py (caso con un único tipo de malo).
    - Función de Möbius: contar pares coprimos = Σ_d μ(d)·⌊n/d⌋² es
      inclusión–exclusión sobre los primos.
    - Recurrencia de desarreglos: D(n) = (n−1)(D(n−1) + D(n−2)).
    - Números de Stirling de 2.ª especie S(n,k) = sobreyecciones(n,k) / k!.
    - IE sobre caminos en cuadrícula con obstáculos, y «transformada de
      Möbius sobre subconjuntos» (SOS DP) para muchas intersecciones.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/F - Finding Paths (prohibir el vector nulo con
      inclusión–exclusión + multinomiales)
    - CSES «Prime Multiples» (múltiplos de alguno, k ≤ 20),
      «Christmas Party» (desarreglos), «Counting Coprime Pairs» (Möbius)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta: recorrer [1, n] (500 casos),
      itertools.permutations para desarreglos (n ≤ 8) y itertools.product
      para sobreyecciones (n, k ≤ 6); recurrencia de D(n) hasta 60
      (python inclusion_exclusion.py)
"""
import itertools
import random
from math import comb, factorial, gcd


def multiplos_de_alguno(n, nums):
    """x en [1, n] divisibles por al menos uno de nums (DFS con poda por lcm)."""
    nums = sorted(set(nums))
    m = len(nums)
    total = 0
    # pila de (índice desde el que se puede agregar, lcm actual, tamaño de S)
    pila = [(0, 1, 0)]
    while pila:
        i0, l, tam = pila.pop()
        if tam > 0:
            total += (n // l) if tam % 2 == 1 else -(n // l)
        for i in range(i0, m):
            nl = l // gcd(l, nums[i]) * nums[i]
            if nl <= n:              # si lcm > n, ningún superconjunto aporta
                pila.append((i + 1, nl, tam + 1))
    return total


def desarreglos(n):
    """Permutaciones de n elementos sin puntos fijos."""
    return sum((-1) ** i * comb(n, i) * factorial(n - i) for i in range(n + 1))


def sobreyecciones(n, k):
    """Funciones de [n] a [k] que usan todos los k valores."""
    return sum((-1) ** i * comb(k, i) * (k - i) ** n for i in range(k + 1))


def demo():
    print("múltiplos de 2 o 3 en [1,10]:", multiplos_de_alguno(10, [2, 3]))   # 7
    print("D(4) =", desarreglos(4))                                         # 9
    print("sobreyecciones 3 -> 2:", sobreyecciones(3, 2))                   # 6
    print("múltiplos de 4 o 6 en [1,100]:", multiplos_de_alguno(100, [4, 6]))  # 25+16-8 = 33


def pruebas():
    random.seed(31)

    # Casos borde
    assert multiplos_de_alguno(0, [2]) == 0 and multiplos_de_alguno(10, []) == 0
    assert multiplos_de_alguno(10, [1]) == 10
    assert desarreglos(0) == 1 and desarreglos(1) == 0 and desarreglos(2) == 1
    assert sobreyecciones(0, 0) == 1 and sobreyecciones(3, 0) == 0
    assert sobreyecciones(2, 3) == 0

    for _ in range(500):
        n = random.randint(0, 300)
        nums = [random.randint(1, 30) for _ in range(random.randint(0, 6))]
        bruto = sum(1 for x in range(1, n + 1) if any(x % d == 0 for d in nums))
        assert multiplos_de_alguno(n, nums) == bruto

    for n in range(0, 9):
        bruto = sum(1 for p in itertools.permutations(range(n))
                    if all(p[i] != i for i in range(n)))
        assert desarreglos(n) == bruto
    for n in range(2, 61):
        assert desarreglos(n) == (n - 1) * (desarreglos(n - 1) + desarreglos(n - 2))

    for n in range(0, 7):
        for k in range(0, 7):
            bruto = sum(1 for f in itertools.product(range(k), repeat=n)
                        if len(set(f)) == k)
            assert sobreyecciones(n, k) == bruto


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
