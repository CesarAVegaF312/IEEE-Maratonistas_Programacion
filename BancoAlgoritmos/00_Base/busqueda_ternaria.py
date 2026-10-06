"""
Base — Búsqueda ternaria («Ternary search»)
Nivel: Intermedio
Ejecutar: python busqueda_ternaria.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar el máximo (o mínimo) de una función UNIMODAL: sube hasta un
    pico y luego baja (o baja hasta un valle y luego sube), sin conocer
    una fórmula para el pico. Sirve sobre enteros y sobre reales.
    Señales en el enunciado: «minimizar la distancia/costo/tiempo» donde
    el costo es convexo en un parámetro (suma de |x − a_i|, distancia de un
    punto que se mueve, máximo de funciones convexas); «elegir el momento
    / la posición óptima»; la intuición «al principio mejora y después
    empeora».

FUNCIÓN
    ternaria_reales(lo, hi, f, iteraciones=100) -> float
        x en [lo, hi] que MAXIMIZA f (unimodal: estrictamente creciente y
        luego estrictamente decreciente). Para minimizar, pasar -f.
    maximo_entero(lo, hi, f) -> int
        x entero en [lo, hi] que maximiza f; si hay varios máximos
        empatados, devuelve el primero. Exige f estrictamente creciente
        hasta el máximo y no creciente después (sin mesetas antes del pico).
    minimo_entero(lo, hi, f) -> int     igual, minimizando.

IDEA Y ALGORITMO
    Reales: se toman dos puntos interiores m1 < m2 (a 1/3 y 2/3 del
    intervalo). Si f(m1) < f(m2), el máximo NO puede estar en [lo, m1]:
    si estuviera ahí, f ya estaría bajando entre m1 y m2 y sería
    f(m1) > f(m2). Así que lo = m1. Si no, simétricamente hi = m2. Cada
    paso conserva 2/3 del intervalo: 100 pasos lo reducen por (2/3)^100 ≈
    2·10^-18, suficiente para cualquier rango razonable con flotantes.
    Enteros: es más simple y seguro hacer BÚSQUEDA BINARIA sobre la
    «derivada»: cond(x) = f(x) >= f(x+1) («ya no sube») es falsa antes del
    pico y verdadera desde el pico en adelante, es decir, MONÓTONA. El
    primer x donde es verdadera es el máximo. Esto evita los casos borde de
    la ternaria entera (intervalos de 2–3 elementos).
    Por qué no alcanza recorrer todo: el rango puede ser 10^9 o real; la
    ternaria hace O(log) evaluaciones de f.

MACROALGORITMO
    (Reales)
    1. Repetir un número fijo de veces (60–100):
    2.    m1 = lo + (hi − lo)/3,  m2 = hi − (hi − lo)/3.
    3.    Si f(m1) < f(m2): lo = m1; si no: hi = m2.
    4. Devolver (lo + hi)/2.
    (Enteros)
    5. Búsqueda binaria del primer x en [lo, hi) con f(x) >= f(x+1);
       si ninguno, el máximo es hi.

COMPLEJIDAD
    Reales: 2·iteraciones evaluaciones de f (200 con 100 iteraciones).
    Enteros: O(log(hi − lo)) pares de evaluaciones.
    En Python, aun con f de O(N) y N = 10^5, 200 evaluaciones ~0,5 s.

EJEMPLO A MANO
    f(x) = −(x − 7)² + 3 sobre enteros en [0, 20] (pico en 7):
      cond(x) = f(x) >= f(x+1):  x=0..6 F,  x=7.. V
      binaria: lo=0 hi=20 → m=10 V → hi=10; m=5 F → lo=6; m=8 V → hi=8;
               m=7 V → hi=7; m=6 F → lo=7   → 7
    Reales, minimizar g(x) = |x − 1| + |x − 4| + |x − 9| en [0, 10]:
      es convexa con mínimo en la mediana: x = 4, g = 8.

ERRORES TÍPICOS
    - Usarla con funciones que NO son unimodales (varios picos): da un
      máximo local. Comprobar o argumentar la convexidad.
    - Mesetas: si f tiene tramos planos que no son el máximo, la ternaria
      (y la binaria sobre la derivada) puede descartar el lado bueno.
    - Comparar con epsilon (while hi − lo > eps) y quedarse en bucle
      infinito por precisión: iterar un número fijo de veces.
    - Ternaria entera con m1 = m2 o intervalos pequeños: ciclos infinitos;
      mejor la binaria sobre f(x) >= f(x+1).
    - Minimizar con la versión de maximizar sin cambiar el signo.

VARIANTES Y RELACIONADOS
    - Búsqueda por sección áurea: reutiliza una evaluación por paso.
    - Ternaria anidada (función convexa de dos variables).
    - El máximo de funciones convexas es convexo (útil para minimizarlo).
    - Relacionados: busqueda_binaria.py, 01_BusquedaCompleta/busqueda_sobre_respuesta.py.

DÓNDE PRACTICAR
    - Codeforces 578C «Weakness and Poorness» (ternaria sobre reales)
    - Codeforces 439D «Devu and his Brother» (ternaria sobre enteros)
    - UVa 1476 «Error Curves» (mínimo del máximo de parábolas)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (argmax recorriendo todo el rango) en
      2000 funciones unimodales enteras aleatorias; reales contra el
      óptimo conocido (vértice de parábolas, mediana de |x − a_i|) y contra
      un muestreo fino en 500 casos + casos borde (python busqueda_ternaria.py)
"""
import random


def ternaria_reales(lo, hi, f, iteraciones=100):
    """x en [lo, hi] que maximiza f unimodal (para minimizar, usar -f)."""
    for _ in range(iteraciones):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2):
            lo = m1         # el máximo no está en [lo, m1]
        else:
            hi = m2         # el máximo no está en [m2, hi]
    return (lo + hi) / 2


def maximo_entero(lo, hi, f):
    """Primer x en [lo, hi] que maximiza f (sube estrictamente y luego no sube)."""
    # Binaria sobre la «derivada»: cond(x) = f(x) >= f(x+1) es F...F V...V
    a, b = lo, hi           # buscar el primer verdadero en [lo, hi); hi si ninguno
    while a < b:
        m = (a + b) // 2
        if f(m) >= f(m + 1):
            b = m           # ya no sube: el pico es m o está a la izquierda
        else:
            a = m + 1       # todavía sube: el pico está a la derecha
    return a


def minimo_entero(lo, hi, f):
    """Primer x en [lo, hi] que minimiza f (baja estrictamente y luego no baja)."""
    return maximo_entero(lo, hi, lambda x: -f(x))


def demo():
    f = lambda x: -(x - 7) ** 2 + 3
    print("maximo_entero(0, 20, -(x-7)^2+3) =", maximo_entero(0, 20, f))       # 7
    pts = [1, 4, 9]
    g = lambda x: sum(abs(x - p) for p in pts)
    x = ternaria_reales(0, 10, lambda x: -g(x))
    print(f"mínimo de |x-1|+|x-4|+|x-9| en x = {x:.6f}, valor {g(x):.6f}")       # 4, 8
    print("minimo_entero(-100, 100, g) =", minimo_entero(-100, 100, g))         # 4


def pruebas():
    random.seed(1476)

    # Casos borde
    assert maximo_entero(5, 5, lambda x: x) == 5
    assert maximo_entero(0, 10, lambda x: x) == 10              # solo sube
    assert maximo_entero(0, 10, lambda x: -x) == 0              # solo baja
    assert maximo_entero(0, 10, lambda x: 7) == 0               # constante: el primero
    assert minimo_entero(-10**9, 10**9, lambda x: abs(x - 123456789)) == 123456789

    # Enteros: sucesiones aleatorias «sube estricto, luego no sube»
    for _ in range(2000):
        n = random.randint(1, 30)
        pico = random.randint(0, n - 1)
        v = [0] * n
        v[pico] = random.randint(50, 60)
        for i in range(pico - 1, -1, -1):
            v[i] = v[i + 1] - random.randint(1, 4)          # estrictamente menor a la izquierda
        for i in range(pico + 1, n):
            v[i] = v[i - 1] - random.randint(0, 4)          # no crece a la derecha (con mesetas)
        lo = random.randint(-5, 5)
        f = lambda x: v[x - lo]
        esperado = lo + v.index(max(v))
        assert maximo_entero(lo, lo + n - 1, f) == esperado
        assert minimo_entero(lo, lo + n - 1, lambda x: -f(x)) == esperado

    # Reales: vértice de una parábola y mediana de |x - a_i|
    for _ in range(500):
        c = random.uniform(-100, 100)
        a = random.uniform(0.1, 5)
        x = ternaria_reales(-1000, 1000, lambda t: -a * (t - c) ** 2)
        assert abs(x - c) < 1e-6
        pts = [random.randint(-50, 50) for _ in range(random.choice([1, 3, 5, 7]))]
        g = lambda t: sum(abs(t - p) for p in pts)
        x = ternaria_reales(-100, 100, lambda t: -g(t))
        assert abs(x - sorted(pts)[len(pts) // 2]) < 1e-6
        # máximo de dos rectas (convexo): el mínimo está en el cruce, recortado a [-10, 10]
        m1, b1, m2, b2 = random.uniform(-3, -0.1), random.uniform(-5, 5), random.uniform(0.1, 3), random.uniform(-5, 5)
        h = lambda t: max(m1 * t + b1, m2 * t + b2)
        x = ternaria_reales(-10, 10, lambda t: -h(t))
        cruce = min(10.0, max(-10.0, (b2 - b1) / (m1 - m2)))
        assert abs(h(x) - h(cruce)) < 1e-6


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
