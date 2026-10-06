"""
Programación dinámica — DP de dígitos («Digit DP»)
Nivel: Intermedio
Ejecutar: python dp_digitos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Contar cuántos enteros x en [0, N] (o en [a, b]) cumplen una propiedad
    que depende de sus DÍGITOS: suma de dígitos igual a S, sin dos dígitos
    vecinos iguales, sin el dígito 4, divisible por K, cantidad de unos en
    binario… con N hasta 10^18 (imposible recorrerlos uno por uno).
    Señales: «¿cuántos números entre a y b…?» con a, b ≤ 10^18 y una
    condición sobre los dígitos.

FUNCIÓN
    contar_suma_digitos(N, S) -> int
        Cuántos x en [0, N] tienen suma de dígitos exactamente S.
    contar_sin_vecinos_iguales(N) -> int
        Cuántos x en [0, N] no tienen dos dígitos consecutivos iguales
        (CSES «Counting Numbers»; 0 cuenta).
    contar_rango(f, a, b) -> int
        f(b) - f(a - 1): cuántos en [a, b] (f(-1) = 0).

IDEA Y ALGORITMO
    Se construye x dígito a dígito de izquierda a derecha, igual de largo
    que N (rellenando con ceros a la izquierda). x ≤ N exactamente cuando,
    en la primera posición donde x y N difieren, x tiene el dígito menor.
    Por eso basta un bit:
      ajustado = «hasta ahora x copió exactamente los dígitos de N».
    Si está ajustado, el siguiente dígito puede ir de 0 a d[pos]; si no, de
    0 a 9 (x ya es menor y nada lo puede hacer pasar de N).
    Suma de dígitos:
      ESTADO      f(pos, suma, ajustado) = cuántas formas de completar los
                  dígitos pos.. si ya se lleva `suma` y el bit `ajustado`.
      TRANSICIÓN  probar cada dígito c permitido:
                  f(pos+1, suma + c, ajustado and c == d[pos]).
      CASO BASE   pos == largo: 1 si suma == S, si no 0 (poda: suma > S -> 0).
      ORDEN       top-down con memoria (la profundidad es solo el número de
                  dígitos, ≤ 19: la recursión es segura aquí).
      RESPUESTA   f(0, 0, True).
    Sin vecinos iguales: el estado agrega el dígito anterior; los CEROS A LA
    IZQUIERDA no son dígitos reales (007 es 7), así que mientras no haya
    empezado el número el «anterior» es un valor especial (10) y poner otro
    0 no cuenta como repetición.
    Por qué es eficiente: el número de estados es (#dígitos) × (valores de
    la información extra) × 2, y cada uno prueba 10 dígitos.

MACROALGORITMO
    1. d = lista de dígitos de N.
    2. Definir f(pos, info, ajustado) con memoria.
    3. tope = d[pos] si ajustado, si no 9.
    4. Para c en 0..tope (si c es válido según info): sumar
       f(pos+1, nueva info, ajustado and c == tope).
    5. Respuesta f(0, info inicial, True). Rango [a, b]: f(b) - f(a-1).

COMPLEJIDAD
    O(#dígitos × #info × 2 × 10). Suma de dígitos con N = 10^18:
    19 · 163 · 2 · 10 ≈ 6·10^4 pasos. Instantáneo.

EJEMPLO A MANO
    N = 25, S = 4: d = [2, 5].
      primer dígito 0 (ya no ajustado): segundo = 4 -> «04» = 4       (1)
      primer dígito 1 (no ajustado):    segundo = 3 -> 13             (1)
      primer dígito 2 (ajustado):       segundo ≤ 5, = 2 -> 22        (1)
      Total 3: {4, 13, 22}.

ERRORES TÍPICOS
    - Olvidar actualizar ajustado (o compararlo con 9 en vez de d[pos]).
    - Tratar los ceros a la izquierda como dígitos reales cuando la
      propiedad depende de ellos (vecinos, «contiene un 0», cantidad de dígitos).
    - Rango [a, b]: usar f(b) - f(a) (pierde a) en vez de f(b) - f(a - 1).
    - Memoizar ajustado = True no ayuda (es un solo camino), pero no hace
      daño; olvidar lru_cache sí es fatal.
    - Reutilizar la caché entre llamadas con N distinto (la función interna
      debe definirse dentro, o limpiarse).

VARIANTES Y RELACIONADOS
    - Divisible por K: info = resto módulo K. Dígitos en base 2: popcount.
    - Sumar en vez de contar (p. ej. suma de dígitos de todos los números ≤ N):
      devolver (cantidad, suma) por estado.
    - Versión iterativa: diccionario de estados avanzando posición a posición.
    - memoizacion.py.

DÓNDE PRACTICAR
    - Externos: CSES «Counting Numbers».

VERIFICACIÓN
    - Pruebas: OK contra recorrido directo de todos los x ≤ 30 000 (con
      sumas prefijas) en 1500 consultas aleatorias + rangos + casos borde, y
      propiedad Σ_S contar_suma_digitos(N, S) = N + 1 para N hasta 10^18
      (python dp_digitos.py)
"""
import random
from functools import lru_cache


def contar_suma_digitos(N, S):
    """Cuántos x en [0, N] tienen suma de dígitos S."""
    if N < 0:
        return 0
    d = [int(c) for c in str(N)]
    largo = len(d)

    @lru_cache(maxsize=None)
    def f(pos, suma, ajustado):
        if suma > S:
            return 0                            # poda: ya no se puede bajar
        if pos == largo:
            return 1 if suma == S else 0
        tope = d[pos] if ajustado else 9
        return sum(f(pos + 1, suma + c, ajustado and c == tope) for c in range(tope + 1))

    return f(0, 0, True)


def contar_sin_vecinos_iguales(N):
    """Cuántos x en [0, N] no tienen dos dígitos consecutivos iguales."""
    if N < 0:
        return 0
    d = [int(c) for c in str(N)]
    largo = len(d)
    NADA = 10                                   # «todavía no empezó el número»

    @lru_cache(maxsize=None)
    def f(pos, previo, ajustado):
        if pos == largo:
            return 1
        tope = d[pos] if ajustado else 9
        total = 0
        for c in range(tope + 1):
            if c == previo:
                continue                        # dos vecinos iguales
            nuevo = NADA if (previo == NADA and c == 0) else c   # cero a la izquierda
            total += f(pos + 1, nuevo, ajustado and c == tope)
        return total

    return f(0, NADA, True)


def contar_rango(f, a, b):
    """Cuántos x en [a, b] cumplen la propiedad que cuenta f (f(N) = cuántos en [0, N])."""
    return f(b) - f(a - 1)


def demo():
    print("x ≤ 25 con suma de dígitos 4:", contar_suma_digitos(25, 4))          # 3
    print("x ≤ 100 sin vecinos iguales:", contar_sin_vecinos_iguales(100))      # 91
    print("en [123, 321] sin vecinos iguales:",
          contar_rango(contar_sin_vecinos_iguales, 123, 321))                   # CSES: 171
    print("x ≤ 10^18 con suma de dígitos 100:", contar_suma_digitos(10**18, 100))


def pruebas():
    random.seed(2220)
    TOPE = 30000

    def sin_vecinos(x):
        s = str(x)
        return all(s[i] != s[i + 1] for i in range(len(s) - 1))

    # Sumas prefijas de la fuerza bruta
    acum_vec = []
    acum_suma = {}
    c = 0
    for x in range(TOPE + 1):
        c += sin_vecinos(x)
        acum_vec.append(c)
    sumas = [sum(map(int, str(x))) for x in range(TOPE + 1)]

    def bruta_suma(N, S):
        if S not in acum_suma:
            a, t = [], 0
            for x in range(TOPE + 1):
                t += sumas[x] == S
                a.append(t)
            acum_suma[S] = a
        return acum_suma[S][N] if N >= 0 else 0

    # Casos borde
    assert contar_suma_digitos(0, 0) == 1 and contar_suma_digitos(0, 1) == 0
    assert contar_suma_digitos(-1, 0) == 0 and contar_sin_vecinos_iguales(-1) == 0
    assert contar_sin_vecinos_iguales(0) == 1 and contar_sin_vecinos_iguales(11) == 11
    assert contar_rango(contar_sin_vecinos_iguales, 123, 321) == 171

    for _ in range(1500):
        N = random.randint(0, TOPE)
        S = random.randint(0, 30)
        assert contar_suma_digitos(N, S) == bruta_suma(N, S)
        assert contar_sin_vecinos_iguales(N) == acum_vec[N]
    for _ in range(300):
        a = random.randint(0, TOPE)
        b = random.randint(a, TOPE)
        assert contar_rango(contar_sin_vecinos_iguales, a, b) == acum_vec[b] - (acum_vec[a - 1] if a else 0)

    # Propiedad: cada x ≤ N tiene exactamente una suma de dígitos
    for N in [10**18, 10**18 - 1, 987654321987654321, 99999, 10**9 + 7]:
        assert sum(contar_suma_digitos(N, S) for S in range(9 * 19 + 1)) == N + 1


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
