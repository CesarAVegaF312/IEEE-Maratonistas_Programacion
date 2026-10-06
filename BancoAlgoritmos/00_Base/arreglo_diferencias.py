"""
Base — Arreglo de diferencias 1D y 2D («Difference array»)
Nivel: Básico
Ejecutar: python arreglo_diferencias.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Aplicar muchas actualizaciones «sumar v a todas las posiciones de l a r»
    (o a un rectángulo de una matriz) y al FINAL conocer el arreglo
    resultante. Cada actualización cuesta O(1) y la reconstrucción O(N).
    Señales en el enunciado: «Q operaciones: sumar v en el rango [l, r]» y
    las preguntas vienen DESPUÉS de todas las operaciones (offline);
    «¿cuántos intervalos cubren cada punto?», «¿en qué momento hay más
    personas?», pintar franjas/rectángulos y contar capas.

FUNCIÓN
    aplicar_rangos(n, ops) -> list
        ops: tuplas (l, r, v), índices desde 0 e inclusive. Devuelve el
        arreglo de n ceros tras sumar v en cada [l, r].
    aplicar_rectangulos(n, m, ops) -> list[list]
        ops: tuplas (f1, c1, f2, c2, v) inclusive. Matriz n×m resultante.
    max_solapamiento(intervalos) -> int
        Máximo número de intervalos [s, e] (enteros, inclusive) que
        comparten un punto.

IDEA Y ALGORITMO
    Es la operación INVERSA de las sumas prefijas. Si D es un arreglo y A
    sus sumas prefijas (A[i] = D[0] + … + D[i]), entonces poner D[l] += v
    suma v a TODOS los A[i] con i ≥ l. Para que solo afecte hasta r, se
    compensa con D[r+1] -= v. Así cada rango toca 2 casillas, y al final
    una pasada de sumas prefijas reconstruye el arreglo (las
    actualizaciones se suman porque todo es lineal).
    2D: D[f1][c1] += v suma v a todo el cuadrante inferior derecho desde
    (f1, c1). Para recortarlo al rectángulo se resta en (f1, c2+1) y en
    (f2+1, c1), y se vuelve a sumar en (f2+1, c2+1), que se restó dos
    veces (inclusión–exclusión). Luego sumas prefijas 2D.
    El ingenuo (recorrer el rango en cada operación) es O(N) por operación:
    Q = N = 10^5 → 10^10. Con diferencias: O(N + Q).

MACROALGORITMO
    1. D = [0] * (n + 1)   (una casilla extra para r + 1 = n).
    2. Por cada operación (l, r, v): D[l] += v; D[r+1] -= v.
    3. Recorrer acumulando: A[i] = A[i-1] + D[i].
    4. (2D) D de (n+1)×(m+1); cuatro esquinas con signos + − − +.
    5. (2D) Sumas prefijas por filas y luego por columnas (o la fórmula 2D).
    6. Responder las preguntas sobre el arreglo final.

COMPLEJIDAD
    1D: O(N + Q) tiempo, O(N) memoria.  2D: O(N·M + Q).
    En Python, 10^6 operaciones + reconstrucción en ~0,5 s.
    Si las coordenadas son enormes (hasta 10^9), no se crea el arreglo:
    se ordenan los eventos (barrido) — ver max_solapamiento.

EJEMPLO A MANO
    n = 6, ops = (1, 3, +2), (2, 5, +1), (0, 0, +5)
      D tras (1,3,2):  [0, 2, 0, 0, -2, 0, 0]
      D tras (2,5,1):  [0, 2, 1, 0, -2, 0, -1]
      D tras (0,0,5):  [5, -3, 1, 0, -2, 0, -1]
      prefijas de D[0..5]:  [5, 2, 3, 3, 1, 1]
    Comprobación: pos 0 → 5; pos 1 → 2; pos 2,3 → 2+1; pos 4,5 → 1. ✓

ERRORES TÍPICOS
    - D de tamaño n (no n+1): D[r+1] se sale cuando r = n − 1.
    - Mezclar intervalos inclusivos y semiabiertos: con [l, r) se resta en
      D[r], no en D[r+1].
    - Querer consultar ENTRE actualizaciones: el arreglo solo es válido tras
      reconstruir. Para mezclar consultas y actualizaciones online hace
      falta Fenwick (sobre D) o árbol de segmentos con propagación perezosa.
    - En el barrido por eventos, procesar en el orden incorrecto los
      inicios y fines que caen en la misma coordenada.

VARIANTES Y RELACIONADOS
    - Barrido por eventos (coordenadas grandes): +1 en s, −1 en e+1,
      ordenar y acumular.
    - Diferencias de segundo orden: sumar progresiones aritméticas en rangos.
    - Relacionados: sumas_prefijas.py (la operación inversa).
    - Online: árbol de Fenwick con actualización de rango y consulta de punto.

DÓNDE PRACTICAR
    - Codeforces 295A «Greg and Array» (diferencias aplicadas dos veces)
    - Codeforces 816B «Karen and Coffee» (diferencias + sumas prefijas)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (sumar casilla por casilla) en 1500
      casos aleatorios 1D, 2D y de solapamiento + casos borde
      (python arreglo_diferencias.py)
"""
import random


def aplicar_rangos(n, ops):
    """Arreglo de n ceros tras sumar v en cada [l, r] (inclusive, desde 0)."""
    D = [0] * (n + 1)                # casilla extra: r + 1 puede valer n
    for l, r, v in ops:
        D[l] += v                    # desde l en adelante se suma v ...
        D[r + 1] -= v                # ... y se cancela después de r
    A = [0] * n
    acum = 0
    for i in range(n):
        acum += D[i]                 # suma prefija de D = valor real
        A[i] = acum
    return A


def aplicar_rectangulos(n, m, ops):
    """Matriz n x m de ceros tras sumar v en cada rectángulo (f1, c1)-(f2, c2)."""
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for f1, c1, f2, c2, v in ops:
        D[f1][c1] += v
        D[f1][c2 + 1] -= v
        D[f2 + 1][c1] -= v
        D[f2 + 1][c2 + 1] += v       # esta esquina se restó dos veces
    # Sumas prefijas 2D: primero por filas, luego por columnas.
    for i in range(n):
        fila = D[i]
        for j in range(1, m):
            fila[j] += fila[j - 1]
    for i in range(1, n):
        arriba, fila = D[i - 1], D[i]
        for j in range(m):
            fila[j] += arriba[j]
    return [D[i][:m] for i in range(n)]


def max_solapamiento(intervalos):
    """Máximo de intervalos [s, e] (inclusive) que comparten un punto.

    Barrido por eventos: (s, +1) y (e + 1, -1). Al ordenar, en una misma
    coordenada los -1 van antes que los +1 (el que termina en e ya no cubre
    e + 1), y así no se cuenta un solapamiento falso.
    """
    eventos = []
    for s, e in intervalos:
        eventos.append((s, 1))
        eventos.append((e + 1, -1))
    eventos.sort()                   # (x, -1) < (x, +1): salidas primero
    mejor = act = 0
    for _, d in eventos:
        act += d
        mejor = max(mejor, act)
    return mejor


def demo():
    ops = [(1, 3, 2), (2, 5, 1), (0, 0, 5)]
    print("aplicar_rangos(6, ops) =", aplicar_rangos(6, ops))     # [5,2,3,3,1,1]
    M = aplicar_rectangulos(3, 4, [(0, 0, 1, 1, 1), (1, 1, 2, 3, 10)])
    print("rectángulos:")
    for fila in M:
        print("   ", fila)
    print("max_solapamiento =", max_solapamiento([(1, 5), (2, 3), (3, 8), (6, 7)]))  # 3


def pruebas():
    random.seed(4242)

    # Casos borde
    assert aplicar_rangos(0, []) == []
    assert aplicar_rangos(1, [(0, 0, 7)]) == [7]
    assert aplicar_rangos(3, [(0, 2, 1)] * 4) == [4, 4, 4]
    assert aplicar_rectangulos(1, 1, [(0, 0, 0, 0, -3)]) == [[-3]]
    assert max_solapamiento([]) == 0
    assert max_solapamiento([(1, 2), (3, 4)]) == 1      # se tocan sin solaparse
    assert max_solapamiento([(1, 3), (3, 4)]) == 2      # comparten el 3

    for _ in range(500):
        n = random.randint(1, 30)
        ops = []
        for _ in range(random.randint(0, 20)):
            l = random.randint(0, n - 1)
            r = random.randint(l, n - 1)
            ops.append((l, r, random.randint(-10, 10)))
        bruta = [0] * n
        for l, r, v in ops:
            for i in range(l, r + 1):
                bruta[i] += v
        assert aplicar_rangos(n, ops) == bruta

    for _ in range(500):
        n, m = random.randint(1, 7), random.randint(1, 7)
        ops = []
        for _ in range(random.randint(0, 10)):
            f1 = random.randint(0, n - 1); f2 = random.randint(f1, n - 1)
            c1 = random.randint(0, m - 1); c2 = random.randint(c1, m - 1)
            ops.append((f1, c1, f2, c2, random.randint(-5, 5)))
        bruta = [[0] * m for _ in range(n)]
        for f1, c1, f2, c2, v in ops:
            for i in range(f1, f2 + 1):
                for j in range(c1, c2 + 1):
                    bruta[i][j] += v
        assert aplicar_rectangulos(n, m, ops) == bruta

    for _ in range(500):
        iv = []
        for _ in range(random.randint(0, 10)):
            s = random.randint(-5, 15)
            iv.append((s, s + random.randint(0, 6)))
        bruta = max([sum(1 for s, e in iv if s <= x <= e) for x in range(-6, 23)], default=0)
        assert max_solapamiento(iv) == bruta


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
