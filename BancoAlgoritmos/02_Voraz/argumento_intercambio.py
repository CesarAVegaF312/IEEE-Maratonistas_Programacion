"""
Voraz — Argumento de intercambio y regla de Smith («Exchange argument», «Smith's rule»)
Nivel: Intermedio
Ejecutar: python argumento_intercambio.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Técnica para DESCUBRIR y DEMOSTRAR el orden óptimo cuando la respuesta
    es «poner los elementos en algún orden»: se mira qué pasa al
    intercambiar dos elementos VECINOS y de ahí sale el criterio de
    ordenamiento (un comparador).
    Ejemplo clásico: N trabajos con duración t_i y peso w_i en una sola
    máquina; minimizar Σ w_i · C_i, donde C_i es el instante en que termina
    el trabajo i (regla de Smith).
    Señales en el enunciado: «en qué orden…», «minimizar la suma de
    tiempos de espera / multas por día / costo acumulado», N hasta 10^5
    (descarta probar las N! permutaciones o una DP sobre subconjuntos).

FUNCIÓN
    orden_smith(trabajos) -> list[int]
        trabajos: lista de (duracion, peso) con duracion > 0 y peso >= 0.
        Devuelve los índices en el orden óptimo.
    costo_ponderado(trabajos, orden) -> int    Σ w_i · C_i de ese orden.
    mayor_concatenacion(numeros) -> str
        Segundo ejemplo de la técnica: el mayor número que se forma
        concatenando todos los números dados (como cadenas).

IDEA Y ALGORITMO
    Receta del argumento de intercambio:
      1. Tomar un orden cualquiera y dos elementos VECINOS a y b (a justo
         antes que b), que empiezan en el instante T.
      2. Comparar el costo de «… a b …» con el de «… b a …». Lo que está
         antes y después de la pareja NO cambia (empieza y termina igual).
      3. De esa comparación sale una condición «a debe ir antes que b si…»
         que depende SOLO de a y b: ese es el comparador.
      4. Comprobar que el comparador es un orden total (transitivo). Si lo
         es, cualquier orden que lo viole tiene un par vecino «invertido»;
         intercambiarlo no empeora el costo, y repitiendo (como burbuja) se
         llega al orden ordenado sin haber empeorado nunca: es óptimo.
    Aplicado a Σ w·C con a y b vecinos:
        a antes: w_a·(T + t_a) + w_b·(T + t_a + t_b)
        b antes: w_b·(T + t_b) + w_a·(T + t_a + t_b)
        diferencia (a antes − b antes) = w_b·t_a − w_a·t_b
    Así que a va antes que b si t_a · w_b < t_b · w_a, es decir, si
    t_a / w_a < t_b / w_b: ordenar por duración/peso creciente (regla de
    Smith). Al ser comparar un número real por trabajo, es transitivo.
    Se compara con multiplicación cruzada de enteros (exacto, sin
    flotantes, y funciona con peso 0 = razón infinita).
    Segundo ejemplo: concatenar números para el mayor resultado. Con a y b
    vecinos solo importa si a+b > b+a como cadenas (mismo largo). El
    comparador «a+b > b+a» es transitivo (equivale a comparar a/(10^|a|−1)
    contra b/(10^|b|−1)), así que ordenar con él es óptimo. Ordenar como
    cadenas a secas falla: ["3", "30"] da "303" pero lo mejor es "330".

MACROALGORITMO
    1. Escribir el costo con dos vecinos a, b en ambos órdenes.
    2. Simplificar la diferencia hasta una condición que solo dependa de
       a y b.
    3. Verificar transitividad (si es «comparar f(a) con f(b)», es gratis).
    4. Implementar el comparador con functools.cmp_to_key (o una clave
       f(a) si se puede) y ordenar.
    5. Calcular la respuesta recorriendo el orden.

COMPLEJIDAD
    O(N log N) comparaciones; memoria O(N). Con cmp_to_key, Python ordena
    ~10^5–10^6 elementos por segundo (una clave con key= es más rápida).

EJEMPLO A MANO
    trabajos (t, w): A (3, 1), B (1, 2), C (2, 2)
    razones t/w: A = 3, B = 0.5, C = 1 → orden B, C, A
      B termina en 1: 2·1 = 2;  C en 3: 2·3 = 6;  A en 6: 1·6 = 6 → 14.
    Orden de entrada A, B, C: 1·3 + 2·4 + 2·6 = 23.

ERRORES TÍPICOS
    - Ordenar por un solo atributo (duración o peso) por intuición, sin
      hacer la cuenta del intercambio.
    - Comparar razones con flotantes: empates mal resueltos y errores con
      valores grandes; usar multiplicación cruzada.
    - Usar un comparador NO transitivo: sorted puede devolver cualquier
      cosa. Probar siempre contra fuerza bruta en casos pequeños.
    - En Python 3, sorted no acepta cmp=: hace falta functools.cmp_to_key.

VARIANTES Y RELACIONADOS
    - Pesos iguales: minimizar la suma de tiempos de finalización = el más
      corto primero (SPT).
    - Minimizar el máximo retraso: ordenar por plazo (EDD); maximizar
      tareas a tiempo: 02_Voraz/voraz_con_monticulo.py.
    - Problemas donde el intercambio de vecinos depende de algo acumulado
      (p. ej. el orden de «pelear con monstruos»): a veces el criterio
      divide en dos grupos y ordena cada uno distinto.
    - 02_Voraz/mochila_fraccionaria.py y 02_Voraz/seleccion_actividades.py
      también se demuestran con intercambio; 02_Voraz/bridge_and_torch.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/B - The Bridge at Night (la optimalidad del voraz
      se demuestra con un argumento de intercambio)
    - ICPC/Colombia 2026/G - Math United FC (intercambio que justifica el
      voraz con arrepentimiento)
    - UVa 10026 «Shoemaker's Problem» (exactamente la regla de Smith).
    - CSES «Tasks and Deadlines» (el más corto primero).
    - LeetCode 179 «Largest Number» (mayor_concatenacion).

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las permutaciones, N <= 7) en
      1000 casos aleatorios para cada problema, más casos borde y empates
      (python argumento_intercambio.py)
"""
import random
from functools import cmp_to_key
from itertools import permutations


def orden_smith(trabajos):
    """Orden que minimiza Σ peso·fin: duración/peso creciente (regla de Smith)."""
    def cmp(i, j):
        ti, wi = trabajos[i]
        tj, wj = trabajos[j]
        # i antes que j  ⇔  ti/wi < tj/wj  ⇔  ti·wj < tj·wi  (exacto con enteros)
        return ti * wj - tj * wi
    return sorted(range(len(trabajos)), key=cmp_to_key(cmp))


def costo_ponderado(trabajos, orden):
    """Σ w_i · C_i ejecutando los trabajos en ese orden desde el instante 0."""
    tiempo = costo = 0
    for i in orden:
        t, w = trabajos[i]
        tiempo += t                 # C_i: instante en que termina i
        costo += w * tiempo
    return costo


def mayor_concatenacion(numeros):
    """Mayor número (como cadena) concatenando todos los números dados."""
    s = [str(x) for x in numeros]
    # a antes que b si a+b > b+a (resultado del intercambio de vecinos)
    s.sort(key=cmp_to_key(lambda a, b: (a + b < b + a) - (a + b > b + a)))
    r = "".join(s)
    return r.lstrip("0") or ("0" if r else "")   # "00" -> "0"


def demo():
    trabajos = [(3, 1), (1, 2), (2, 2)]
    orden = orden_smith(trabajos)
    print("trabajos (t, w) =", trabajos)
    print("orden de Smith  =", orden, " costo =", costo_ponderado(trabajos, orden))  # [1,2,0] 14
    print("orden original  costo =", costo_ponderado(trabajos, [0, 1, 2]))           # 23
    print("mayor concatenación de [3, 30, 34, 5, 9] =",
          mayor_concatenacion([3, 30, 34, 5, 9]))                                  # 9534330


def pruebas():
    random.seed(10026)

    # Casos borde
    assert orden_smith([]) == [] and costo_ponderado([], []) == 0
    assert orden_smith([(4, 2)]) == [0]
    t = [(2, 3)] * 4                                       # todos iguales
    assert costo_ponderado(t, orden_smith(t)) == 3 * (2 + 4 + 6 + 8)
    assert orden_smith([(5, 0), (1, 1)]) == [1, 0]         # peso 0 va al final
    assert mayor_concatenacion([3, 30]) == "330"
    assert mayor_concatenacion([0, 0]) == "0"
    assert mayor_concatenacion([]) == ""
    assert mayor_concatenacion([12, 121]) == "12121"

    # Smith contra todas las permutaciones
    for _ in range(1000):
        n = random.randint(1, 7)
        trabajos = [(random.randint(1, 10), random.randint(0, 10)) for _ in range(n)]
        orden = orden_smith(trabajos)
        assert sorted(orden) == list(range(n))
        mejor = min(costo_ponderado(trabajos, p) for p in permutations(range(n)))
        assert costo_ponderado(trabajos, orden) == mejor

    # Concatenación contra todas las permutaciones
    for _ in range(1000):
        n = random.randint(1, 6)
        nums = [random.choice([random.randint(0, 9), random.randint(0, 99),
                               random.randint(0, 999)]) for _ in range(n)]
        mejor = max(int("".join(map(str, p))) for p in permutations(nums))
        assert mayor_concatenacion(nums) == str(mejor)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
