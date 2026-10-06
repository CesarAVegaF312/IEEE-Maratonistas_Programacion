"""
ACM ICPC Guangzhou Summer Series 2017 — K: Kid's Spiral Problem («El problema de la espiral del niño»)
Ejecutar: python kidspiral.py < kidspiral.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En una cuadrícula (2n+1)×(2n+1) se escriben los enteros positivos en
    espiral: el 1 en el centro (0,0), el 2 a su derecha (1,0) y se sigue en
    sentido antihorario (3 en (1,1), 4 en (0,1), 5 en (-1,1), …). Se pregunta
    la suma de los números dentro de un rectángulo.

QUÉ HAY QUE HACER
    Entrada: varios casos (≤ 100) hasta fin de archivo. Cada uno: "n q" y luego
             q líneas "x1 y1 x2 y2" (dos esquinas opuestas del rectángulo).
             [El enunciado dice "there are lines" sin decir cuántas; por el
             ejemplo son q.] El eje y crece hacia arriba (ver la figura).
    Salida:  por consulta, la suma de las casillas con x entre x1..x2 e y
             entre y1..y2 (ambos extremos incluidos), módulo 1000000007.
    Restricciones clave: n ≤ 10^9 (no se puede recorrer el rectángulo),
             q ≤ 100, -n ≤ coordenadas ≤ n.

IDEA Y ALGORITMO
    1) Fórmula cerrada del valor de una casilla. La casilla (x,y) está en el
       "anillo" k = max(|x|,|y|). El anillo k (k ≥ 1) contiene los números
       (2k-1)^2+1 … (2k+1)^2 y empieza en (k, -k+1). Partimos el anillo en
       cuatro lados de 2k casillas cada uno (las esquinas quedan en un solo
       lado):
         derecha  x = k,  y ∈ [-k+1, k]  → valor (2k-1)^2 +  k + y
         arriba   y = k,  x ∈ [-k, k-1]  → valor (2k-1)^2 + 3k - x
         izquierda x = -k, y ∈ [-k, k-1] → valor (2k-1)^2 + 5k - y
         abajo    y = -k, x ∈ [-k+1, k]  → valor (2k-1)^2 + 7k + x
       (p. ej. (1,1): 1+1+1 = 3; (-1,-2): k=2 abajo, 9+14-1 = 22.)
    2) Suma por regiones. Cada una de las 4 regiones ("todas las casillas
       que son lado derecho de algún anillo", etc.) es un triángulo infinito.
       Recorremos la región con una variable EXTERNA t = k (el anillo) y una
       INTERNA s (la otra coordenada). Para un t fijo, s recorre un intervalo
       [L(t), U(t)] = intersección del rango del lado con el del rectángulo;
       L es un máximo de funciones lineales de t y U un mínimo.
       La suma interna Σ_{s=L}^{U} (P(t) + c·s) tiene fórmula cerrada:
       cnt·P(t) + c·(L+U)·cnt/2, con cnt = U-L+1.
    3) Suma sobre t sin recorrer 10^9 valores: partimos el rango de t en
       trozos donde L(t) y U(t) son UNA SOLA función lineal y cnt no cambia
       de signo (los cortes están donde se cruzan dos de esas rectas). En
       cada trozo, la suma interna f(t) es un polinomio de grado ≤ 3 en t,
       así que Σ_{t=a}^{b} f(t) se obtiene exactamente con diferencias
       finitas de Newton:  Σ_{t=a}^{b} f(t) = Σ_{r=0}^{3} Δ^r f(a)·C(N, r+1),
       N = b-a+1 (basta evaluar f en a, a+1, a+2, a+3).
       Python trabaja con enteros exactos; el módulo se aplica al final.
    4) El centro (0,0) vale 1 y se suma aparte si cae en el rectángulo.

MACROALGORITMO
    1. Leer todos los números; por caso leer n, q y las q consultas.
    2. Normalizar la consulta (x1 ≤ x2, y1 ≤ y2).
    3. Para cada una de las 4 regiones: calcular el rango de anillos t que
       tocan el rectángulo, las cotas inferiores/superiores (rectas en t)
       de la variable interna y la fórmula P(t), c del valor.
    4. Cortar el rango de t en los cruces de esas rectas.
    5. En cada trozo sumar f(t) con diferencias de Newton (o directo si es
       corto).
    6. Sumar las 4 regiones + el centro, imprimir módulo 10^9+7.

COMPLEJIDAD
    O(1) por consulta (unas decenas de evaluaciones de polinomios); total
    O(número de consultas). 10 000 consultas aleatorias con n = 10^9 tardan
    ≈ 0,9 s en Python (incluido el arranque).

EJEMPLO A MANO
    "0 -2 1 1": columnas x=0,1 y filas y=-2..1 → 23+24+8+9+1+2+4+3 = 74.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/K")
    - Fuerza bruta (espiral construida casilla a casilla, n ≤ 7, sumando el
      rectángulo directamente): OK en 3000 consultas aleatorias.
"""
import sys

MOD = 1_000_000_007


def comb_small(N, r):
    """C(N, r) para r pequeño (r ≤ 4) con enteros exactos."""
    num = 1
    den = 1
    for k in range(r):
        num *= N - k
        den *= k + 1
    return num // den


def suma_polinomio(f, a, b):
    """Σ_{t=a}^{b} f(t) para f polinomio de grado ≤ 3 en [a, b].

    Si el tramo es corto se suma directamente; si no, se usa la fórmula de
    Newton con las diferencias hacia adelante en t = a.
    """
    N = b - a + 1
    if N <= 0:
        return 0
    if N <= 4:
        return sum(f(t) for t in range(a, b + 1))
    valores = [f(a + k) for k in range(4)]
    total = 0
    # Δ^r f(a) para r = 0..3, calculadas en sitio sobre la lista
    for r in range(4):
        total += valores[0] * comb_small(N, r + 1)
        valores = [valores[k + 1] - valores[k] for k in range(len(valores) - 1)]
    return total


def suma_region(t_lo, t_hi, inferiores, superiores, P, c):
    """Suma de la región parametrizada por el anillo t ∈ [t_lo, t_hi].

    inferiores / superiores: listas de rectas (p, q) que representan p*t + q;
    la variable interna s va de L(t) = max(inferiores) a U(t) = min(superiores).
    El valor de la casilla (t, s) es P(t) + c*s.
    """
    if t_lo > t_hi:
        return 0
    rectas = inferiores + superiores

    # Puntos de corte: donde dos rectas se cruzan, y donde U - L + 1 = 0.
    # Para cada cruce real r agregamos floor(r) y floor(r)+1 como inicios de
    # trozo; así dentro de cada trozo ninguna diferencia cambia de signo.
    cortes = {t_lo, t_hi + 1}
    pares = []
    for i in range(len(rectas)):
        for j in range(i + 1, len(rectas)):
            pares.append((rectas[i], rectas[j], 0))
    for (p1, q1) in inferiores:
        for (p2, q2) in superiores:
            pares.append(((p1, q1), (p2, q2), 1))  # U - L + 1 = 0
    for (p1, q1), (p2, q2), extra in pares:
        dp = p1 - p2
        if dp == 0:
            continue
        # p1 t + q1 = p2 t + q2 + extra  →  t = (q2 + extra - q1) / dp
        num = q2 + extra - q1
        r = num // dp if dp > 0 else (-num) // (-dp)  # floor exacto
        for cand in (r, r + 1):
            if t_lo < cand <= t_hi:
                cortes.add(cand)
    cortes = sorted(cortes)

    def f(t):
        # Suma de la fila/columna del anillo t dentro del rectángulo.
        L = max(p * t + q for p, q in inferiores)
        U = min(p * t + q for p, q in superiores)
        cnt = U - L + 1
        # Dentro de un trozo cnt tiene signo fijo; si es ≤ 0 el trozo es
        # vacío completo (devolvemos 0, que también es polinomio).
        if cnt <= 0:
            return 0
        return cnt * P(t) + c * (L + U) * cnt // 2

    total = 0
    for k in range(len(cortes) - 1):
        a, b = cortes[k], cortes[k + 1] - 1
        total += suma_polinomio(f, a, b)
    return total


def suma_rectangulo(x1, y1, x2, y2):
    """Suma exacta (sin módulo) de la espiral en [x1,x2]×[y1,y2]."""
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    total = 0
    # Centro
    if x1 <= 0 <= x2 and y1 <= 0 <= y2:
        total += 1
    # Lado derecho: t = x = k ≥ 1, s = y ∈ [-t+1, t], valor (2t-1)^2 + t + y
    total += suma_region(max(x1, 1), x2,
                         [(0, y1), (-1, 1)], [(0, y2), (1, 0)],
                         lambda t: (2 * t - 1) ** 2 + t, 1)
    # Lado de arriba: t = y = k, s = x ∈ [-t, t-1], valor (2t-1)^2 + 3t - x
    total += suma_region(max(y1, 1), y2,
                         [(0, x1), (-1, 0)], [(0, x2), (1, -1)],
                         lambda t: (2 * t - 1) ** 2 + 3 * t, -1)
    # Lado izquierdo: t = -x = k, s = y ∈ [-t, t-1], valor (2t-1)^2 + 5t - y
    total += suma_region(max(-x2, 1), -x1,
                         [(0, y1), (-1, 0)], [(0, y2), (1, -1)],
                         lambda t: (2 * t - 1) ** 2 + 5 * t, -1)
    # Lado de abajo: t = -y = k, s = x ∈ [-t+1, t], valor (2t-1)^2 + 7t + x
    total += suma_region(max(-y2, 1), -y1,
                         [(0, x1), (-1, 1)], [(0, x2), (1, 0)],
                         lambda t: (2 * t - 1) ** 2 + 7 * t, 1)
    return total


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        n, q = int(datos[pos]), int(datos[pos + 1])  # n no hace falta: las consultas ya están dentro
        pos += 2
        for _ in range(q):
            x1, y1, x2, y2 = (int(v) for v in datos[pos:pos + 4])
            pos += 4
            salida.append(str(suma_rectangulo(x1, y1, x2, y2) % MOD))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
