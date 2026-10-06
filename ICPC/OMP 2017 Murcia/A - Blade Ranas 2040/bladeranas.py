"""
OMP 2017 Murcia — A: Blade Ranas 2040 («Blade Ranas 2040»)
Ejecutar: python bladeranas.py < bladeranas.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En un planeta dominado por ranas inteligentes, el cuerpo de policía
    "Blade Ranas" se come a las ranas replicantes. Una Blade Rana lanza su
    lengua en horizontal, vertical o diagonal y se come a todos los
    replicantes en esas líneas, pero la lengua no atraviesa muros.

QUÉ HAY QUE HACER
    Entrada: número de casos; cada caso "R C" y R filas de C caracteres:
    '.' vacío, 'R' replicante, '#' muro.
    Salida:  "fila columna" (1-indexadas) de la casilla desde la que se come
    el máximo de replicantes; en empate, la primera de arriba abajo y luego
    de izquierda a derecha.
    Restricciones clave: R, C ≤ 100 (hasta 10^4 casillas por caso).
    Detalles: si la rana está sobre un replicante, también se lo come (cuenta
    una vez). Sobre un muro se come 0 replicantes (el enunciado lo dice para
    (1,10)), pero la casilla sigue siendo candidata: si todo da 0, la
    respuesta es "1 1".

IDEA Y ALGORITMO
    Precálculo por segmentos (conteo por tramos entre muros).
    Desde una casilla, la rana alcanza, en cada una de las 4 RECTAS que pasan
    por ella (horizontal, vertical, diagonal \\ y antidiagonal /), justo el
    tramo maximal sin muros que contiene a la casilla: hacia ambos lados
    avanza hasta el primer muro. Entonces
        comidos(casilla) = Σ_{4 rectas} replicantes_del_tramo  -  3·[casilla es R]
    (la propia casilla está en los 4 tramos y debe contarse una sola vez).
    Cada recta se recorre una vez partiéndola en tramos en los muros; todas
    las casillas de un tramo reciben el mismo conteo. Así cada casilla se
    visita O(1) veces por familia de rectas.
    El ingenuo (lanzar 8 rayos desde cada casilla) cuesta O(R·C·(R+C)) ≈
    2·10^6·8 operaciones por caso: lento en Python con varios casos.

MACROALGORITMO
    1. Leer el mapa.
    2. Para cada dirección (0,1), (1,0), (1,1), (1,-1):
       a. Recorrer cada recta de esa dirección desde su casilla inicial.
       b. Acumular las casillas no-muro del tramo actual y sus 'R'.
       c. Al encontrar un muro o el borde, sumar el conteo del tramo a todas
          sus casillas y empezar un tramo nuevo.
    3. Restar 3 en cada casilla con 'R' (contada 4 veces, debe ser 1).
    4. Barrer filas y columnas en orden y quedarse con el primer máximo
       (comparación estricta).
    5. Imprimir la posición 1-indexada.

COMPLEJIDAD
    Tiempo O(R·C) por caso, memoria O(R·C).
    Caso grande (20 mapas de 100×100 aleatorios): ~0.4 s.

EJEMPLO A MANO
    Tercer caso: "R.. / ### / .R.". En (1,1): fila "R.." → 1, columna y
    diagonal cortadas por el muro de la fila 2 → tramos {(1,1)} con 1 R cada
    uno, antidiagonal {(1,1)} → 1. Total 4 - 3 = 1. El máximo es 1 y la
    primera casilla con 1 es (1,1).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "OMP 2017/A")
    - Fuerza bruta: OK en 500 mapas aleatorios (hasta 8×8, densidades de
      muros y replicantes variadas) contra el lanzamiento literal de los 8
      rayos desde cada casilla.
"""
import sys

# Una dirección por cada familia de rectas (la opuesta queda incluida al
# recorrer la recta completa).
DIRECCIONES = ((0, 1), (1, 0), (1, 1), (1, -1))


def resolver(filas, columnas, mapa):
    total = [[0] * columnas for _ in range(filas)]

    for df, dc in DIRECCIONES:
        # Casillas iniciales de las rectas: aquellas cuyo predecesor
        # (f - df, c - dc) cae fuera del mapa.
        for f0 in range(filas):
            for c0 in range(columnas):
                fp, cp = f0 - df, c0 - dc
                if 0 <= fp < filas and 0 <= cp < columnas:
                    continue
                # Recorrer la recta partiéndola en tramos sin muros.
                tramo = []          # casillas del tramo actual
                replicantes = 0     # cuántas 'R' tiene el tramo actual
                f, c = f0, c0
                while True:
                    dentro = 0 <= f < filas and 0 <= c < columnas
                    if not dentro or mapa[f][c] == "#":
                        # Cierra el tramo: todas sus casillas ven sus 'R'.
                        for (tf, tc) in tramo:
                            total[tf][tc] += replicantes
                        tramo = []
                        replicantes = 0
                        if not dentro:
                            break
                    else:
                        tramo.append((f, c))
                        if mapa[f][c] == "R":
                            replicantes += 1
                    f += df
                    c += dc

    # La casilla propia, si es 'R', se contó en las 4 rectas: dejar solo 1.
    mejor, mejor_pos = -1, (1, 1)
    for f in range(filas):
        fila_mapa, fila_total = mapa[f], total[f]
        for c in range(columnas):
            valor = fila_total[c] - (3 if fila_mapa[c] == "R" else 0)
            if valor > mejor:   # estricto: en empate gana la primera
                mejor, mejor_pos = valor, (f + 1, c + 1)
    return mejor_pos


def main():
    datos = sys.stdin.read().split()
    casos = int(datos[0])
    idx = 1
    salida = []
    for _ in range(casos):
        filas, columnas = int(datos[idx]), int(datos[idx + 1])
        idx += 2
        mapa = datos[idx:idx + filas]
        idx += filas
        f, c = resolver(filas, columnas, mapa)
        salida.append(f"{f} {c}")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
