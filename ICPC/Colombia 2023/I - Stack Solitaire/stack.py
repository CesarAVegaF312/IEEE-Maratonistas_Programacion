"""
Colombia 2023 — I: Stack Solitaire («Solitario de pilas»)
Ejecutar: python stack.py < stack.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En el casino ICPC se empieza con una pila de N monedas. En cada jugada se
    parte una pila de 2 o más monedas en dos pilas (sin cambiar el orden) y
    se gana la suma de los valores de la pila partida. Se juega hasta tener
    N pilas de una moneda. Se pide el MÍNIMO puntaje total posible.

QUÉ HAY QUE HACER
    Entrada: varios casos; cada uno N (2 ≤ N ≤ 1000) y N valores
             (1 ≤ v ≤ 100). Termina con una línea "0".
    Salida:  por caso, el puntaje final mínimo.

IDEA Y ALGORITMO
    DP sobre intervalos + optimización de Knuth (es el problema clásico de
    "unir piedras adyacentes" visto al revés).
    Cada pila que aparece en el juego es un intervalo contiguo [i, j] de la
    pila original, y cada intervalo de longitud ≥ 2 se parte exactamente una
    vez, aportando suma(i..j). Así que
        costo(i, j) = suma(i..j) + min_{i ≤ k < j} costo(i, k) + costo(k+1, j)
    con costo(i, i) = 0. El orden en que se parten pilas distintas no
    cambia el total, solo importa el árbol de cortes.
    El DP directo es O(N^3) = 10^9 para N = 1000: inviable. Como el peso
    w(i, j) = suma(i..j) cumple la desigualdad del cuadrángulo y es monótono
    en la inclusión de intervalos, el corte óptimo es monótono:
        opt(i, j−1) ≤ opt(i, j) ≤ opt(i+1, j)    (Knuth–Yao)
    y basta probar k en ese rango. Sumando por cada longitud, los rangos se
    telescopian a O(N), así que el total es O(N^2).

MACROALGORITMO
    1. Leer N y los valores; armar sumas prefijas.
    2. costo[i][i] = 0 y opt[i][i] = i.
    3. Para cada longitud de 2 a N y cada inicio i (j = i + longitud − 1):
       probar k entre opt[i][j−1] y opt[i+1][j] y quedarse con el mejor
       costo[i][k] + costo[k+1][j]; guardar costo y opt.
    4. Imprimir costo[0][N−1].

COMPLEJIDAD
    Tiempo O(N^2) ≈ 10^6 pasos para N = 1000, memoria O(N^2).
    En Python un caso con N = 1000 tarda ≈ 0,4 s (medido).

EJEMPLO A MANO
    7 2 10 5: lo mejor es partir {7,2 | 10,5} (24), luego {7|2} (9) y
    {10|5} (15): total 48.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2023/I")
    - Fuerza bruta: DP O(N^3) sin optimización en 500 casos aleatorios
      (N ≤ 9): OK.
    - Rendimiento: N = 1000 con valores aleatorios o todos iguales: ≈ 0,4 s.
"""
import sys


def costo_minimo(valores):
    n = len(valores)
    pref = [0] * (n + 1)
    for i, v in enumerate(valores):
        pref[i + 1] = pref[i] + v

    # costo[i][j]: mínimo puntaje para deshacer por completo la pila i..j.
    # opt[i][j]: corte k óptimo (la pila se parte en i..k y k+1..j).
    costo = [[0] * n for _ in range(n)]
    opt = [[0] * n for _ in range(n)]
    for i in range(n):
        opt[i][i] = i

    for largo in range(2, n + 1):
        for i in range(0, n - largo + 1):
            j = i + largo - 1
            fila_i = costo[i]
            mejor = None
            mejor_k = i
            # Rango de Knuth para el corte (si largo = 2 es solo k = i).
            k_ini = opt[i][j - 1]
            k_fin = min(opt[i + 1][j], j - 1)
            for k in range(k_ini, k_fin + 1):
                c = fila_i[k] + costo[k + 1][j]
                if mejor is None or c < mejor:
                    mejor = c
                    mejor_k = k
            fila_i[j] = mejor + pref[j + 1] - pref[i]
            opt[i][j] = mejor_k
    return costo[0][n - 1]


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos])
        pos += 1
        if n == 0:
            break
        valores = [int(v) for v in datos[pos:pos + n]]
        pos += n
        salida.append(str(costo_minimo(valores)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
