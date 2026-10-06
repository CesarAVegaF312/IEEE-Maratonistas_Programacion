"""
Colombia 2023 — H: Match Points («Emparejamiento de puntos»)
Ejecutar: python matchp.py < matchp.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    ICPC fabrica tarjetas de circuitos con m puntos O y m puntos X. Una
    tarjeta está "bien hecha" si cada O se une con un segmento a exactamente
    un X (y viceversa) sin que los segmentos se crucen. Se busca la longitud
    mínima total de un emparejamiento bien hecho.

QUÉ HAY QUE HACER
    Entrada: varios casos; cada uno m (0 < m ≤ 200), luego una línea con las
             m coordenadas de los O y otra con las m de los X. Termina con 0.
             No hay tres puntos colineales; coordenadas en [0, 1000].
    Salida:  por caso, la longitud mínima con exactamente 3 decimales.

IDEA Y ALGORITMO
    Asignación de costo mínimo (algoritmo húngaro) + "descruce".
    Observación clave: el emparejamiento perfecto de longitud mínima (sin
    exigir nada sobre cruces) YA es no cruzado. Si dos segmentos O1–X1 y
    O2–X2 se cruzaran en un punto P, cambiando a O1–X2 y O2–X1 se tiene,
    por la desigualdad triangular,
        |O1X2| + |O2X1| < |O1P| + |PX2| + |O2P| + |PX1| = |O1X1| + |O2X2|
    (estricta porque no hay tres puntos colineales), lo que contradice la
    minimalidad. Así, el óptimo entre los bien hechos es el óptimo entre
    todos, y basta resolver el problema de asignación clásico con costos
    = distancias euclidianas.
    Probar las m! asignaciones es imposible; el húngaro (versión con
    potenciales y caminos más cortos, O(m^3)) lo resuelve exacto.

MACROALGORITMO
    1. Leer m y los 2m puntos.
    2. Matriz de costos: costo[i][j] = distancia entre O_i y X_j.
    3. Húngaro: agregar las filas una por una; para cada fila, buscar con
       un Dijkstra sobre costos reducidos (potenciales u, v) el camino
       aumentante más barato y actualizar potenciales y emparejamiento.
    4. Sumar las distancias de la asignación final.
    5. Imprimir con "%.3f".

COMPLEJIDAD
    Tiempo O(m^3) = 8·10^6 pasos para m = 200, memoria O(m^2).
    En Python un caso con m = 200 tarda entre ≈ 0,13 s (puntos aleatorios)
    y ≈ 0,3 s (configuraciones con caminos aumentantes largos), medido;
    con muchísimos casos grandes podría acercarse al límite del juez.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2023/H")
    - Fuerza bruta: para m ≤ 6, se enumeran las m! asignaciones, se
      descartan las que tienen segmentos cruzados y se toma la mínima; en
      400 casos aleatorios sin tres puntos colineales coincide con el
      húngaro (lo que además comprueba la observación de "descruce").
"""
import sys
from math import hypot

INF = float("inf")


def hungaro(costo):
    """Asignación de costo mínimo (matriz cuadrada m×m). Devuelve asignación
    asign[j] = fila asignada a la columna j (índices desde 0)."""
    m = len(costo)
    # Índices desde 1 internamente; la columna 0 es un "comodín" auxiliar.
    u = [0.0] * (m + 1)       # potencial de filas
    v = [0.0] * (m + 1)       # potencial de columnas
    fila_de = [0] * (m + 1)   # fila_de[j]: fila emparejada con la columna j
    previo = [0] * (m + 1)    # columna anterior en el camino aumentante
    for i in range(1, m + 1):
        fila_de[0] = i
        j0 = 0
        minimo = [INF] * (m + 1)   # menor costo reducido para llegar a cada columna
        usada = [False] * (m + 1)
        while True:
            usada[j0] = True
            i0 = fila_de[j0]
            costo_i0 = costo[i0 - 1]
            ui0 = u[i0]
            delta = INF
            j1 = 0
            for j in range(1, m + 1):
                if not usada[j]:
                    # costo reducido de la arista (i0, j)
                    cur = costo_i0[j - 1] - ui0 - v[j]
                    if cur < minimo[j]:
                        minimo[j] = cur
                        previo[j] = j0
                    if minimo[j] < delta:
                        delta = minimo[j]
                        j1 = j
            # Ajuste de potenciales: mantiene costos reducidos ≥ 0 y hace
            # 0 la arista más barata hacia j1.
            for j in range(m + 1):
                if usada[j]:
                    u[fila_de[j]] += delta
                    v[j] -= delta
                else:
                    minimo[j] -= delta
            j0 = j1
            if fila_de[j0] == 0:
                break  # columna libre: se encontró camino aumentante
        # Aumentar a lo largo del camino.
        while j0:
            j1 = previo[j0]
            fila_de[j0] = fila_de[j1]
            j0 = j1
    return [fila_de[j] - 1 for j in range(1, m + 1)]


def longitud_optima(puntos_o, puntos_x):
    costo = [[hypot(ox - xx, oy - xy) for (xx, xy) in puntos_x] for (ox, oy) in puntos_o]
    asign = hungaro(costo)
    return sum(costo[asign[j]][j] for j in range(len(puntos_x)))


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        m = int(datos[pos])
        pos += 1
        if m == 0:
            break
        coords = [int(t) for t in datos[pos:pos + 4 * m]]
        pos += 4 * m
        puntos_o = [(coords[2 * i], coords[2 * i + 1]) for i in range(m)]
        puntos_x = [(coords[2 * m + 2 * i], coords[2 * m + 2 * i + 1]) for i in range(m)]
        salida.append("%.3f" % longitud_optima(puntos_o, puntos_x))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
