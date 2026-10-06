"""
Matemáticas — Contar por complemento: buenos = total − malos («complementary counting»)
Nivel: Básico
Ejecutar: python conteo_complemento.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Cuando contar directamente los objetos «buenos» es difícil (muchos
    casos, condiciones de «al menos uno») pero contar el TOTAL y los «malos»
    es fácil. Se responde total − malos.
    Cómo reconocerlo: «al menos uno», «no todos», «distintos», «que no
    cumpla…», «por lo menos una vez»; la condición buena es una unión de
    muchos casos y la mala es una intersección simple («ninguno»).

FUNCIÓN
    cadenas_con_alguna(n, a, b) -> int
        Cadenas de longitud n sobre a letras que usan al menos una de b
        letras especiales: a^n − (a−b)^n.
    pares_distintos(arr) -> int
        Pares i < j con arr[i] != arr[j]: C(n,2) − Σ_v C(cnt_v, 2).
    muestras_mediana(arr, k) -> int
        Subconjuntos de k índices (k impar, len(arr) impar) cuya mediana es
        igual a la mediana de arr (Colombia 2026 K).

IDEA Y ALGORITMO
    Si U es el conjunto de todos los objetos y M ⊆ U los malos, entonces los
    buenos son U \\ M y |U \\ M| = |U| − |M|. Es solo eso, pero cambia el
    problema: «al menos una letra especial» es la unión de n eventos («la
    posición i es especial»), mientras que su complemento «ninguna» es una
    intersección: cada posición elige entre a−b letras → (a−b)^n.
    - pares_distintos: los pares iguales se agrupan por valor; dentro de un
      valor con c apariciones hay C(c, 2) pares iguales.
    - muestras_mediana: sea v la mediana, L = #{< v}, G = #{> v}, h = (k−1)/2.
      La mediana de la muestra es v ⇔ la muestra tiene ≤ h menores y ≤ h
      mayores (si tuviera ≥ h+1 menores, la posición h+1 sería un menor; si
      no, la posición h+1 no puede ser menor ni mayor). Los malos son
        A = «≥ h+1 menores»: Σ_{t≥h+1} C(L, t)·C(n−L, k−t), y B igual con G.
      A y B son DISJUNTOS (tener ambos exige 2h+2 = k+1 > k elementos), así
      que |A ∪ B| = |A| + |B| y buenos = C(n, k) − |A| − |B|.
      Si los malos NO fueran disjuntos habría que sumar |A ∩ B| de vuelta:
      eso es inclusión–exclusión (inclusion_exclusion.py).

MACROALGORITMO
    1. Definir bien el universo U (qué se cuenta, ¿con orden o sin orden?).
    2. Contar |U| (suele ser una potencia o un binomial).
    3. Describir los malos; partirlos en casos DISJUNTOS fáciles de contar.
    4. Si los casos se solapan, usar inclusión–exclusión.
    5. Responder |U| − |malos| (con módulo: (total − malos) % p, sumando p).
    6. Para probabilidades: buenos / total (o buenos · total^(-1) mód p).

COMPLEJIDAD
    Depende de lo que se cuenta; en los ejemplos: cadenas O(log n),
    pares O(n), muestras_mediana O(n log n) (ordenar) + O(n) binomiales.

EJEMPLO A MANO
    Cadenas de 3 letras sobre {a,b,c} con al menos una 'a': 27 − 8 = 19.
    arr = [1, 2, 2, 3, 3, 3]: C(6,2) = 15; iguales C(2,2)+C(3,2) = 1+3 = 4
    → 11 pares distintos.
    arr = [1,2,3,4,5], k = 3: v = 3, L = G = 2, h = 1;
    A = C(2,2)·C(3,1) = 3, B = 3, total C(5,3) = 10 → 10 − 3 − 3 = 4.

ERRORES TÍPICOS
    - Restar malos que se solapan (contarlos dos veces) sin corregir.
    - Universo mal definido (con orden vs. sin orden) entre total y malos:
      ambos deben contarse en el MISMO universo.
    - Con módulo: (total − malos) puede quedar negativo en C++; en Python
      % p ya lo deja en [0, p).
    - Olvidar que el objeto «vacío» o los casos triviales pertenecen al
      total (p. ej. subconjunto vacío).

VARIANTES Y RELACIONADOS
    - inclusion_exclusion.py (cuando los malos se solapan).
    - probabilidad_esperanza.py (P(bueno) = 1 − P(malo)).
    - Contar caminos que NO pasan por casillas prohibidas = total − los que
      pasan (combinado con DP sobre las casillas prohibidas ordenadas).
    - ncr_modular.py (la versión mód p de los binomiales).

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/K - Sample Median Preservation (exactamente
      muestras_mediana, con factoriales mód 10^9+7)
    - ICPC/Guangzhou 2017/F - Finding Paths (total − caminos solo unitarios)
    - CSES «Christmas Party» (desarreglos, complemento + inclusión–exclusión)

VERIFICACIÓN
    - Pruebas: OK contra enumeración directa de los objetos buenos
      (itertools.product / combinations) en 900 casos aleatorios pequeños
      + casos borde (python conteo_complemento.py)
"""
import itertools
import random
from bisect import bisect_left, bisect_right
from collections import Counter
from math import comb


def cadenas_con_alguna(n, a, b):
    """Cadenas de largo n sobre a letras con al menos una de las b especiales."""
    return a ** n - (a - b) ** n          # total − (ninguna especial)


def pares_distintos(arr):
    """Pares i < j con arr[i] != arr[j]."""
    n = len(arr)
    iguales = sum(comb(c, 2) for c in Counter(arr).values())
    return comb(n, 2) - iguales


def muestras_mediana(arr, k):
    """k-subconjuntos (de índices) cuya mediana es la de arr; n y k impares."""
    a = sorted(arr)
    n = len(a)
    v = a[n // 2]
    menores = bisect_left(a, v)
    mayores = n - bisect_right(a, v)
    h = (k - 1) // 2

    def malos(grupo):
        # muestras con >= h+1 elementos del grupo (todos < v, o todos > v)
        return sum(comb(grupo, t) * comb(n - grupo, k - t)
                   for t in range(h + 1, min(grupo, k) + 1))

    # Los dos tipos de malos son disjuntos: basta restarlos.
    return comb(n, k) - malos(menores) - malos(mayores)


def demo():
    print("cadenas de 3 sobre {a,b,c} con alguna 'a':", cadenas_con_alguna(3, 3, 1))  # 19
    print("pares distintos en [1,2,2,3,3,3]:", pares_distintos([1, 2, 2, 3, 3, 3]))   # 11
    print("muestras de 3 de [1..5] con mediana 3:", muestras_mediana([1, 2, 3, 4, 5], 3))  # 4


def pruebas():
    random.seed(2026)

    # Casos borde
    assert cadenas_con_alguna(0, 5, 2) == 0          # cadena vacía no tiene especiales
    assert cadenas_con_alguna(4, 3, 3) == 81
    assert pares_distintos([]) == 0 and pares_distintos([7]) == 0
    assert pares_distintos([4, 4, 4]) == 0
    assert muestras_mediana([5], 1) == 1
    assert muestras_mediana([2, 2, 2, 2, 2], 3) == 10

    for _ in range(300):
        n = random.randint(0, 5)
        a = random.randint(1, 4)
        b = random.randint(0, a)
        bruto = sum(1 for w in itertools.product(range(a), repeat=n)
                    if any(x < b for x in w))      # letras 0..b-1 son especiales
        assert cadenas_con_alguna(n, a, b) == bruto

    for _ in range(300):
        arr = [random.randint(0, 4) for _ in range(random.randint(0, 12))]
        bruto = sum(1 for i, j in itertools.combinations(range(len(arr)), 2)
                    if arr[i] != arr[j])
        assert pares_distintos(arr) == bruto

    for _ in range(300):
        n = random.choice([1, 3, 5, 7, 9, 11])
        k = random.choice([x for x in range(1, n + 1, 2)])
        arr = [random.randint(0, 4) for _ in range(n)]
        v = sorted(arr)[n // 2]
        bruto = sum(1 for idx in itertools.combinations(range(n), k)
                    if sorted(arr[i] for i in idx)[k // 2] == v)
        assert muestras_mediana(arr, k) == bruto


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
