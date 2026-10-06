"""
Base — Ventana deslizante («Sliding window»; deque monótona)
Nivel: Básico/Intermedio
Ejecutar: python ventana_deslizante.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular algo sobre TODOS los subarreglos contiguos de tamaño K (ventana
    fija) o encontrar el mejor subarreglo que cumple una condición (ventana
    variable), actualizando el resultado al entrar un elemento por la
    derecha y salir otro por la izquierda, en vez de recalcular cada ventana.
    Señales en el enunciado: «K días/posiciones consecutivas», «en cada
    bloque de K», «máximo (o mínimo) de cada ventana», «el tramo más largo
    sin repetir», N hasta 10^5–10^6.

FUNCIÓN
    max_suma_ventana(a, k) -> int
        Máxima suma de k elementos consecutivos (1 <= k <= len(a)).
    maximos_ventana(a, k) -> list
        Lista de n − k + 1 valores: el máximo de cada ventana a[i..i+k-1].
    mas_larga_sin_repetidos(a) -> int
        Largo del subarreglo contiguo más largo sin valores repetidos.
    mas_corta_suma_al_menos(a, s) -> int
        a con valores >= 0. Largo mínimo de un subarreglo con suma >= s;
        0 si no existe.

IDEA Y ALGORITMO
    Ventana fija con suma: al mover la ventana un paso, suma += a[i] −
    a[i−k]. O(1) por paso en vez de O(K).
    Máximo en ventana: el máximo no se puede «restar» al salir un elemento.
    Se mantiene una DEQUE de ÍNDICES cuyos valores son DECRECIENTES
    (de adelante hacia atrás):
      - Al entrar a[i], se sacan por detrás todos los índices j con
        a[j] <= a[i]: nunca volverán a ser máximo, porque a[i] es al menos
        igual de grande y además sale DESPUÉS que ellos.
      - Si el índice del frente ya salió de la ventana (j <= i − k), se saca.
      - El frente es el máximo de la ventana actual.
    Cada índice entra y sale de la deque una sola vez: O(N) en total
    (aunque haya un while dentro del for).
    Ventana variable: dos punteros l ≤ r; se agranda por la derecha y se
    encoge por la izquierda mientras la ventana sea inválida. Funciona si
    la condición es MONÓTONA: si [l, r] es válida, todo subintervalo
    también (sin repetidos; suma ≤ S con valores ≥ 0).

MACROALGORITMO
    (Máximo en ventana de tamaño k)
    1. dq = deque vacía de índices.
    2. Para i = 0..n−1:
    3.    Mientras dq no vacía y a[dq[-1]] <= a[i]: dq.pop().
    4.    dq.append(i).
    5.    Si dq[0] <= i − k: dq.popleft()   (salió de la ventana).
    6.    Si i >= k − 1: anotar a[dq[0]].
    (Ventana variable, más larga sin repetidos)
    7. Para cada r: mientras a[r] ya esté en la ventana, sacar a[l], l += 1.
    8. Agregar a[r] y actualizar el máximo con r − l + 1.

COMPLEJIDAD
    Todas O(N) tiempo; memoria O(K) (deque) u O(N) (conjunto de valores).
    En Python, ~10^6 elementos en ~0,5–1 s.

EJEMPLO A MANO
    a = [1, 3, -1, -3, 5, 3, 6, 7], k = 3 (dq guarda índices; valor entre [])
      i=0: dq=[0[1]]
      i=1: saca 0 (1 <= 3) → dq=[1[3]]
      i=2: dq=[1[3], 2[-1]]                 → max 3
      i=3: dq=[1[3], 2[-1], 3[-3]]          → max 3
      i=4: saca 3, 2, 1 → dq=[4[5]]         → max 5
      i=5: dq=[4[5], 5[3]]                  → max 5
      i=6: saca 5, 4 → dq=[6[6]]            → max 6
      i=7: saca 6 → dq=[7[7]]               → max 7
    maximos_ventana = [3, 3, 5, 5, 6, 7]

ERRORES TÍPICOS
    - Guardar VALORES en la deque en vez de índices: no se sabe cuándo
      expiran.
    - Usar < en vez de <= al sacar (funciona, pero deja duplicados inútiles)
      o comparar al revés y obtener el mínimo.
    - Usar list.pop(0) como cola: es O(N) por operación; usar deque.
    - Ventana variable con valores negativos: la condición deja de ser
      monótona y la técnica falla.
    - Olvidar el caso k > n (no hay ventanas) o la ventana inicial.

VARIANTES Y RELACIONADOS
    - Mínimo en ventana: misma deque con >= (o negar los valores).
    - DP con ventana: dp[i] = a[i] + max(dp[i−k..i−1]) en O(N).
    - Ventana sobre sumas prefijas: suma de la ventana = P[i+k] − P[i]
      (sumas_prefijas.py).
    - Relacionados: dos_punteros.py, pila_cola_deque.py (pila monótona).

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/B - Bankey (ventana fija de M sobre cada paridad)
    - CSES «Playlist» (más larga sin repetidos)
    - Codeforces 279B «Books» (ventana variable con suma ≤ t)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (recalcular cada ventana / probar
      todos los subarreglos) en 2000 casos aleatorios + casos borde
      (python ventana_deslizante.py)
"""
import random
from collections import deque


def max_suma_ventana(a, k):
    """Máxima suma de k consecutivos (1 <= k <= len(a))."""
    suma = sum(a[:k])
    mejor = suma
    for i in range(k, len(a)):
        suma += a[i] - a[i - k]     # entra a[i], sale a[i-k]
        if suma > mejor:
            mejor = suma
    return mejor


def maximos_ventana(a, k):
    """Máximo de cada ventana a[i..i+k-1]; lista de len(a) - k + 1 valores."""
    dq = deque()                    # índices con valores estrictamente decrecientes
    res = []
    for i, v in enumerate(a):
        while dq and a[dq[-1]] <= v:
            dq.pop()                # dominados por v: nunca más serán máximo
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()            # el frente salió de la ventana
        if i >= k - 1:
            res.append(a[dq[0]])
    return res


def mas_larga_sin_repetidos(a):
    """Largo del subarreglo contiguo más largo sin valores repetidos."""
    dentro = set()                  # valores de a[l..r-1]
    l = 0
    mejor = 0
    for r, v in enumerate(a):
        while v in dentro:          # encoger hasta sacar la copia anterior de v
            dentro.remove(a[l])
            l += 1
        dentro.add(v)
        mejor = max(mejor, r - l + 1)
    return mejor


def mas_corta_suma_al_menos(a, s):
    """Largo mínimo de subarreglo con suma >= s (a >= 0); 0 si no existe."""
    mejor = 0
    l = 0
    suma = 0
    for r, v in enumerate(a):
        suma += v
        # mientras siga cumpliendo, intentar acortarla por la izquierda
        while l <= r and suma >= s:
            if mejor == 0 or r - l + 1 < mejor:
                mejor = r - l + 1
            suma -= a[l]
            l += 1
    return mejor


def demo():
    a = [1, 3, -1, -3, 5, 3, 6, 7]
    print("a =", a)
    print("max_suma_ventana(a, 3) =", max_suma_ventana(a, 3))     # 16
    print("maximos_ventana(a, 3) =", maximos_ventana(a, 3))       # [3,3,5,5,6,7]
    b = [5, 1, 3, 5, 2, 3, 4, 1]
    print("mas_larga_sin_repetidos(", b, ") =", mas_larga_sin_repetidos(b))   # 5
    c = [2, 3, 1, 2, 4, 3]
    print("mas_corta_suma_al_menos(", c, ", 7) =", mas_corta_suma_al_menos(c, 7))  # 2


def pruebas():
    random.seed(31337)

    # Casos borde
    assert max_suma_ventana([4], 1) == 4
    assert maximos_ventana([4], 1) == [4]
    assert maximos_ventana([1, 2], 3) == []
    assert maximos_ventana([2, 2, 2], 2) == [2, 2]
    assert mas_larga_sin_repetidos([]) == 0
    assert mas_larga_sin_repetidos([7, 7, 7]) == 1
    assert mas_corta_suma_al_menos([], 1) == 0
    assert mas_corta_suma_al_menos([1, 1], 5) == 0
    assert mas_corta_suma_al_menos([1, 2], 0) == 1

    for _ in range(2000):
        n = random.randint(1, 20)
        a = [random.randint(-8, 8) for _ in range(n)]
        k = random.randint(1, n)
        assert max_suma_ventana(a, k) == max(sum(a[i:i + k]) for i in range(n - k + 1))
        assert maximos_ventana(a, k) == [max(a[i:i + k]) for i in range(n - k + 1)]

        b = [random.randint(0, 6) for _ in range(n)]
        assert mas_larga_sin_repetidos(b) == max(
            r - l + 1 for l in range(n) for r in range(l, n) if len(set(b[l:r + 1])) == r - l + 1)
        s = random.randint(1, 30)
        largos = [r - l + 1 for l in range(n) for r in range(l, n) if sum(b[l:r + 1]) >= s]
        assert mas_corta_suma_al_menos(b, s) == min(largos, default=0)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
