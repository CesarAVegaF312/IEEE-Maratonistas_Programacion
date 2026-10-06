"""
Programación dinámica — Memoización vs tabulación («Top-down / bottom-up»)
Nivel: Básico
Ejecutar: python memoizacion.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Toda DP se puede escribir de dos formas: TOP-DOWN (recursión + memoria:
    la función se llama a sí misma y guarda cada resultado la primera vez
    que lo calcula) o BOTTOM-UP (una tabla que se llena en un orden en el
    que los subproblemas que se necesitan ya están listos). Este archivo
    muestra las dos sobre dos problemas clásicos y explica cuándo usar cada
    una y cómo no morir por el límite de recursión de Python.
    Señales de DP en un enunciado: «¿de cuántas formas…?», «costo mínimo /
    máximo para…», una recursión natural cuyos subproblemas SE REPITEN (la
    versión recursiva ingenua es exponencial) y pocos estados distintos
    (n ≤ 10^5–10^6 en 1D, n·m ≤ ~10^6–10^7 en 2D).

FUNCIÓN
    formas_dado_ingenuo(n) -> int   recursión sin memoria (exponencial, solo
                                    para comparar).
    formas_dado_memo(n) -> int      número de secuencias de lanzamientos de un
    formas_dado_tabla(n) -> int     dado (1..6) que suman n, contando el orden,
                                    módulo 10^9+7 (CSES «Dice Combinations»).
    rana_memo(h) -> int             costo mínimo para ir de la piedra 0 a la
    rana_tabla(h) -> int            n-1 saltando 1 o 2 piedras; saltar de i a
                                    j cuesta |h[i] - h[j]| (AtCoder DP «Frog 1»).
    con_pila_grande(f, *args)       ejecuta f(*args) en un hilo con pila grande
                                    y límite de recursión alto.

IDEA Y ALGORITMO
    Formas del dado:
      ESTADO      f(x) = número de secuencias de lanzamientos que suman x.
      TRANSICIÓN  mirar el ÚLTIMO lanzamiento d ∈ {1..6}:
                  f(x) = Σ_{d=1..6, d ≤ x} f(x - d).
      CASO BASE   f(0) = 1 (la secuencia vacía).
      ORDEN       x creciente (f(x) solo usa valores menores).
      RESPUESTA   f(n).
    Rana:
      ESTADO      c(i) = costo mínimo para llegar de la piedra 0 a la i.
      TRANSICIÓN  se llegó a i desde i-1 o desde i-2:
                  c(i) = min(c(i-1) + |h[i]-h[i-1]|, c(i-2) + |h[i]-h[i-2]|).
      CASO BASE   c(0) = 0.
      ORDEN       i creciente.         RESPUESTA  c(n-1).
    Por qué funciona: la recursión ingenua recalcula el mismo f(x) un número
    exponencial de veces (f(n) llama a f(n-1)…f(n-6), y cada una vuelve a
    llamar a casi los mismos). Pero solo hay n+1 subproblemas DISTINTOS: si
    se guarda cada uno, se calcula una sola vez y el costo total es
    (#estados) × (costo de una transición).
    TOP-DOWN (lru_cache o diccionario): se escribe igual que la recursión y
    solo visita los estados que de verdad se alcanzan. Conviene cuando el
    espacio de estados es enorme pero se alcanzan pocos (máscaras con pocos
    estados alcanzables, juegos, estados con tuplas), o cuando el orden de
    llenado no es obvio. Costos en Python: cada llamada es ~5–10 veces más
    lenta que una iteración de un for, y la profundidad está limitada.
    BOTTOM-UP: se elige un orden donde las dependencias ya están calculadas.
    Más rápida, sin problemas de pila, y permite ahorrar memoria (guardar
    solo las últimas filas). Es la opción por defecto en competencia cuando
    el orden es claro.
    Límite de recursión: Python corta en 1000 niveles. sys.setrecursionlimit
    sube ese número, pero las llamadas también gastan la pila del sistema
    (sobre todo a través de lru_cache, que está escrita en C) y con ~10^4–10^5
    niveles el programa puede morir sin mensaje. Salidas: (a) correr la
    función en un hilo con pila grande (con_pila_grande); (b) «calentar» la
    memo llamando f(0), f(300), f(600)… en orden creciente, para que ninguna
    llamada baje más de ~300 niveles; (c) pasar a bottom-up.

MACROALGORITMO
    Top-down:
    1. Escribir la recursión: casos base y transición.
    2. Antes de calcular, mirar si el estado ya está en la memoria.
    3. Al terminar, guardar el resultado en la memoria y devolverlo.
    4. Si la profundidad puede pasar de ~1000: calentar o pila grande.
    Bottom-up:
    1. Crear la tabla con los casos base.
    2. Recorrer los estados en un orden donde las dependencias estén listas.
    3. Aplicar la transición; la respuesta queda en la casilla final.

COMPLEJIDAD
    Ambas O(#estados × costo de transición): dado O(6n), rana O(n).
    Memoria O(n) (la rana bottom-up podría usar O(1) con dos variables).
    En Python, bottom-up ~10^7 operaciones simples por segundo; top-down
    ~10^6 llamadas por segundo.

EJEMPLO A MANO
    Dado, n = 4: f(0)=1, f(1)=1, f(2)=f(1)+f(0)=2, f(3)=2+1+1=4,
    f(4)=4+2+1+1=8 (1111, 112, 121, 211, 22, 13, 31, 4).
    Rana, h = [10, 30, 40, 20]: c(0)=0, c(1)=20, c(2)=min(20+10, 0+30)=30,
    c(3)=min(30+20, 20+10)=30.

ERRORES TÍPICOS
    - Olvidar la memoria (o guardar después de un return temprano): la
      solución sigue siendo exponencial.
    - lru_cache definido FUERA de la función de cada caso de prueba con
      parámetros globales distintos (h, monedas…): respuestas viejas en
      caché. Definirlo dentro o llamar f.cache_clear() entre casos.
    - Recursión de 10^5 niveles sin pila grande: «RecursionError» o cierre
      silencioso del programa.
    - Argumentos no hashables (listas) con lru_cache: convertirlos a tupla.
    - Bottom-up en un orden en el que la dependencia todavía no se calculó.

VARIANTES Y RELACIONADOS
    - Memo manual con diccionario (rana_memo): útil cuando el estado es una
      tupla o una máscara y se alcanzan pocos estados.
    - Ahorro de memoria: si dp[i] solo usa dp[i-1], dp[i-2], basta un par de
      variables (o dos filas en 2D).
    - cambio_monedas_dp.py, mochila_01.py, dp_digitos.py (top-down natural),
      dp_mascaras.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/B - Forming Better Groups (memo con diccionario sobre
      máscaras: solo se visitan los estados alcanzables).
    - Externos: CSES «Dice Combinations»; AtCoder Educational DP Contest
      A «Frog 1» y B «Frog 2».

VERIFICACIÓN
    - Pruebas: OK; el dado se compara contra la enumeración de todas las
      composiciones (2^(n-1)) para n ≤ 16, la rana contra la enumeración de
      todos los caminos en 400 casos aleatorios, y memo vs tabla para n
      grandes (incluye n = 10^5 con pila grande) (python memoizacion.py).
"""
import random
import sys
import threading
from functools import lru_cache

MOD = 10**9 + 7


def formas_dado_ingenuo(n, contador=None):
    """Recursión directa SIN memoria: exponencial. contador[0] cuenta llamadas."""
    if contador is not None:
        contador[0] += 1
    if n == 0:
        return 1
    return sum(formas_dado_ingenuo(n - d, contador) for d in range(1, 7) if d <= n)


def formas_dado_memo(n):
    """Top-down con lru_cache. La caché vive dentro: cada llamada empieza limpia."""
    @lru_cache(maxsize=None)
    def f(x):
        if x == 0:
            return 1
        total = 0
        for d in range(1, 7):
            if d <= x:
                total += f(x - d)
        return total % MOD

    # «Calentar»: al calcular en orden creciente de a 300, cada llamada
    # encuentra en caché lo que está 300 niveles abajo -> profundidad ≤ ~300.
    for x in range(0, n, 300):
        f(x)
    return f(n)


def formas_dado_tabla(n):
    """Bottom-up: dp[x] se llena en orden creciente de x."""
    dp = [0] * (n + 1)
    dp[0] = 1                                   # caso base: secuencia vacía
    for x in range(1, n + 1):
        total = 0
        for d in range(1, 7):
            if d <= x:
                total += dp[x - d]              # el último lanzamiento fue d
        dp[x] = total % MOD
    return dp[n]


def con_pila_grande(f, *args, pila_mb=128, limite=10**6):
    """Ejecuta f(*args) en un hilo con pila de `pila_mb` MB y devuelve su
    resultado. Úsese para recursiones de 10^4–10^6 niveles. (En Windows el
    máximo permitido es < 256 MB.)"""
    resultado, error = [], []

    def tarea():
        try:
            resultado.append(f(*args))
        except BaseException as e:              # se relanza en el hilo principal
            error.append(e)

    viejo = sys.getrecursionlimit()
    sys.setrecursionlimit(max(viejo, limite))
    threading.stack_size(pila_mb * 2**20)
    hilo = threading.Thread(target=tarea)
    hilo.start()
    hilo.join()
    threading.stack_size(0)                     # volver al tamaño por defecto
    sys.setrecursionlimit(viejo)
    if error:
        raise error[0]
    return resultado[0]


def rana_memo(h):
    """Top-down con memo manual (diccionario). Profundidad n: usa pila grande."""
    memo = {}

    def c(i):
        if i == 0:
            return 0
        if i in memo:
            return memo[i]
        r = c(i - 1) + abs(h[i] - h[i - 1])
        if i >= 2:
            r = min(r, c(i - 2) + abs(h[i] - h[i - 2]))
        memo[i] = r                             # guardar ANTES de devolver
        return r

    if len(h) <= 500:
        return c(len(h) - 1)
    return con_pila_grande(c, len(h) - 1)


def rana_tabla(h):
    """Bottom-up: c[i] solo depende de c[i-1] y c[i-2]."""
    n = len(h)
    c = [0] * n
    for i in range(1, n):
        c[i] = c[i - 1] + abs(h[i] - h[i - 1])
        if i >= 2:
            c[i] = min(c[i], c[i - 2] + abs(h[i] - h[i - 2]))
    return c[n - 1]


def demo():
    print("Dado: f(0..6) =", [formas_dado_tabla(x) for x in range(7)])  # 1 1 2 4 8 16 32
    cont = [0]
    formas_dado_ingenuo(20, cont)
    print("n = 20: llamadas sin memoria =", cont[0], "| estados distintos = 21")
    print("formas_dado_memo(10^5) =", formas_dado_memo(10**5))
    h = [10, 30, 40, 20]
    print("Rana h =", h, "-> memo", rana_memo(h), "tabla", rana_tabla(h))  # 30 30


def pruebas():
    random.seed(2024)

    # Dado: contra todas las composiciones de n (cortes = máscara de n-1 bits)
    for n in range(1, 17):
        cuenta = 0
        for mask in range(1 << (n - 1)):
            ok, largo = True, 1
            for b in range(n - 1):
                if mask >> b & 1:               # corte después de la posición b
                    ok &= largo <= 6
                    largo = 1
                else:
                    largo += 1
            ok &= largo <= 6
            cuenta += ok
        assert formas_dado_tabla(n) == formas_dado_memo(n) == cuenta % MOD
        assert formas_dado_ingenuo(n) == cuenta
    assert formas_dado_tabla(0) == formas_dado_memo(0) == 1
    for n in [999, 1000, 12345, 10**5]:
        assert formas_dado_memo(n) == formas_dado_tabla(n)

    # Rana: contra la enumeración de todos los caminos de saltos 1 / 2
    def rana_bruta(h):
        n, mejor = len(h), [float("inf")]

        def rec(i, costo):
            if i == n - 1:
                mejor[0] = min(mejor[0], costo)
                return
            for s in (1, 2):
                if i + s < n:
                    rec(i + s, costo + abs(h[i + s] - h[i]))
        rec(0, 0)
        return mejor[0]

    for _ in range(400):
        n = random.randint(1, 14)
        h = [random.randint(1, 50) for _ in range(n)]
        assert rana_memo(h) == rana_tabla(h) == rana_bruta(h)
    assert rana_memo([7]) == rana_tabla([7]) == 0
    assert rana_tabla([5, 5, 5, 5]) == 0

    # Rana grande: memo con pila grande (10^5 niveles) vs tabla
    h = [random.randint(1, 10**4) for _ in range(10**5)]
    assert rana_memo(h) == rana_tabla(h)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
