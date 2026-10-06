"""
Colombia 2023 — D: Robot Arm («Brazo robótico»)
Ejecutar: python arm.py < arm.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    RD2 es un brazo robótico plano: una cadena de N secciones rígidas de
    longitudes l1..lN, con el hombro fijo en (0,0) y articulaciones que giran
    libremente (cualquier ángulo, incluso plegándose sobre sí mismas). Hay
    que decidir qué puntos puede tocar la punta.

QUÉ HAY QUE HACER
    Entrada: varios casos. Cada uno: "N m", luego N longitudes, luego m
             puntos (x, y). Termina con "0 0".
    Salida:  por cada punto, 'Y' si la punta lo alcanza y 'N' si no.
    Restricciones clave: N, m ≤ 10^3, li ≤ 10^4, |x|, |y| ≤ 10^7 + 1.

IDEA Y ALGORITMO
    Geometría: el conjunto alcanzable es un ANILLO (corona circular)
    centrado en el hombro, con radio exterior S = l1 + … + lN y radio
    interior r = max(0, 2·max(li) − S).
    Por qué: el alcance solo depende de la distancia al origen (el brazo
    puede rotar entero). La distancia máxima es S (todo estirado). La mínima
    es 0 si la sección más larga L cabe "plegada" contra las demás
    (L ≤ S − L); si no, lo mejor es apuntar todas las demás contra L y
    queda L − (S − L) = 2L − S. Como la distancia alcanzable varía de forma
    continua al mover las articulaciones, se alcanza todo valor intermedio.
    Un punto (x, y) se alcanza si r ≤ √(x²+y²) ≤ S. Se compara con
    cuadrados, todo en enteros: r² ≤ x²+y² ≤ S², sin errores de redondeo.

MACROALGORITMO
    1. Leer N y m; si ambos son 0, terminar.
    2. Leer las longitudes; S = suma, L = máximo, r = max(0, 2L − S).
    3. Para cada punto, d2 = x² + y².
    4. Imprimir 'Y' si r² ≤ d2 ≤ S², si no 'N'.

COMPLEJIDAD
    O(N + m) por caso, memoria O(N + m).

EJEMPLO A MANO
    Longitudes 2, 5, 2: S = 9, L = 5, r = 1. (4,5): d2 = 41 ∈ [1, 81] -> Y.
    (0,0): d2 = 0 < 1 -> N. (9,−1): d2 = 82 > 81 -> N.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2023/D")
    - Fuerza bruta: el intervalo de distancias se recalcula sección por
      sección (si las distancias alcanzables son [lo, hi], al agregar una
      sección de longitud l pasan a ser la unión de [|ρ − l|, ρ + l] para
      ρ ∈ [lo, hi]); coincide con la fórmula en 500 casos aleatorios.
"""
import sys


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        n, m = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        if n == 0 and m == 0:
            break
        longitudes = [int(v) for v in datos[pos:pos + n]]
        pos += n
        total = sum(longitudes)
        # radio interior del anillo: 0 si la sección más larga se puede plegar
        interior = max(0, 2 * max(longitudes) - total)
        r2_min, r2_max = interior * interior, total * total
        for _ in range(m):
            x, y = int(datos[pos]), int(datos[pos + 1])
            pos += 2
            d2 = x * x + y * y
            salida.append("Y" if r2_min <= d2 <= r2_max else "N")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
