"""
Colombia 2023 — G: Grain Silos («Silos de grano»)
Ejecutar: python grain.py < grain.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Sir Lancelot guardó sacos de distintos granos mezclados en N silos
    iguales de capacidad C. Hay que reordenarlos para que cada silo tenga un
    solo tipo de grano y cada tipo quede en un único silo, con el mínimo
    número de movimientos.

QUÉ HAY QUE HACER
    Entrada: varios casos "N C" (1 ≤ N, C ≤ 15) y C filas de N caracteres
             (letra = saco, '.' = vacío); la columna j es el silo j, leído de
             arriba hacia abajo. Termina con "0 0".
             Un movimiento lleva el saco de ARRIBA de un silo a otro silo
             vacío o cuyo saco de arriba sea del mismo tipo, sin pasar la
             capacidad C.
    Salida:  por caso, el mínimo de movimientos, o "Camelot Will Starve!"
             si no se puede.

IDEA Y ALGORITMO
    Búsqueda A* sobre el espacio de configuraciones con una cota inferior
    admisible y consistente.
    - Estado: la tupla ORDENADA de silos (cada silo como cadena de abajo
      hacia arriba). Los silos son idénticos, así que ordenar identifica
      configuraciones que solo difieren en qué silo es cuál.
    - Cota inferior h: un saco que nunca se mueve está en un "tramo de
      fondo" (los sacos del mismo tipo pegados desde el fondo del silo), y
      ese silo tiene que terminar siendo el de su tipo. Cada silo tiene un
      solo tipo en el fondo, así que para cada tipo t basta tomar el tramo
      de fondo de t más largo entre todos los silos (nunca se usa el mismo
      silo para dos tipos). Si "conservados" es la suma de esos tramos,
        h = (número de sacos) − conservados
      es una cota inferior: todos los demás sacos deben moverse al menos
      una vez.
    - Consistencia: un movimiento solo puede alargar en 1 un tramo de fondo
      (el saco cae en un silo vacío o sobre un silo puro de su tipo); quitar
      el saco de arriba nunca alarga ningún tramo. Así h baja a lo sumo 1
      por movimiento y A* con costo unitario devuelve el óptimo.
    - Meta: h = 0 equivale a que cada tipo está completo en un solo silo y
      ese silo es puro.
    - Imposible: si A* agota todos los estados alcanzables sin llegar a la
      meta (p. ej. todos los silos llenos con tapas distintas).
    No hay un algoritmo polinomial conocido sencillo: el problema es un
    rompecabezas de ordenar pilas, y la cota h no siempre es exacta (puede
    hacer falta mover un saco dos veces), por eso se busca.

MACROALGORITMO
    1. Leer N, C y la cuadrícula; armar cada silo de abajo hacia arriba.
    2. Calcular h del estado inicial; si es 0, la respuesta es 0.
    3. A*: cola de prioridad por g + h (g = movimientos hechos).
    4. Al sacar un estado, generar todos los movimientos válidos (origen
       no vacío; destino distinto, con espacio, vacío o con la misma tapa),
       normalizar (ordenar silos) y relajar g.
    5. Si un estado generado tiene h = 0, se cuenta como meta al sacarlo de
       la cola; se imprime su g.
    6. Si la cola se vacía, imprimir "Camelot Will Starve!".

COMPLEJIDAD
    EXPONENCIAL en el peor caso: el número de configuraciones crece muy
    rápido con N y C. Medido en Python con N = C = 15:
      - hasta ~65 sacos (pocos tipos o silos poco llenos): 0,06–2,2 s;
      - casos imposibles muy llenos (casi no hay movimientos): ≈ 0,1–0,4 s;
      - 70 a 170 sacos mezclados al azar: NO termina en 30–60 s.
    O sea, la solución es exacta pero NO alcanza para los casos densos
    que permiten las cotas (N, C ≤ 15); solo sirve si los datos del juez
    son pequeños o poco llenos, como los del ejemplo.
    Se probó una poda "mover siempre un saco al silo puro de su tipo", pero
    no se pudo demostrar que conserve el óptimo (falla si ese silo puro no
    es el silo final de su tipo), así que no se usa.

EJEMPLO A MANO
    Ejemplo 1: silos (fondo->arriba) WBB, BRR, WW, R, vacío. Tramos de
    fondo conservables: W=2 (silo 3), B=1 (silo 2), R=1 (silo 4) -> 4 de 9
    sacos, h = 5, y la búsqueda encuentra 5 movimientos, que es la
    respuesta.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2023/G")
    - Fuerza bruta: BFS simple (sin cota ni normalización de silos) en
      600 casos aleatorios con N ≤ 4, C ≤ 3 (62 de ellos imposibles): OK.
    - Rendimiento: ver COMPLEJIDAD. Estado: correcta pero lenta en casos
      densos grandes (parcial en rendimiento).
"""
import heapq
import sys

SIN_SOLUCION = "Camelot Will Starve!"


def leer_silos(filas, n):
    """Convierte las filas (arriba->abajo) en silos como cadenas fondo->arriba."""
    silos = []
    for j in range(n):
        columna = "".join(fila[j] for fila in reversed(filas))  # fondo -> arriba
        silos.append(columna.replace(".", ""))
    return silos


def cota_inferior(estado, total):
    """h = sacos − suma, por tipo, del tramo de fondo más largo."""
    mejor_tramo = {}
    for silo in estado:
        if not silo:
            continue
        t = silo[0]
        largo = 1
        while largo < len(silo) and silo[largo] == t:
            largo += 1
        if largo > mejor_tramo.get(t, 0):
            mejor_tramo[t] = largo
    return total - sum(mejor_tramo.values())


def vecinos(estado, capacidad):
    """Todos los estados a un movimiento (normalizados: silos ordenados)."""
    n = len(estado)
    resultado = []
    for o in range(n):
        origen = estado[o]
        if not origen:
            continue
        saco = origen[-1]
        destino_vacio_usado = False
        for d in range(n):
            if d == o:
                continue
            destino = estado[d]
            if len(destino) >= capacidad:
                continue
            if destino:
                if destino[-1] != saco:
                    continue
            else:
                # Todos los silos vacíos son equivalentes: probar solo uno.
                if destino_vacio_usado:
                    continue
                destino_vacio_usado = True
            nuevo = list(estado)
            nuevo[o] = origen[:-1]
            nuevo[d] = destino + saco
            resultado.append(tuple(sorted(nuevo)))
    return resultado


def minimo_movimientos(silos, capacidad):
    total = sum(len(s) for s in silos)
    inicio = tuple(sorted(silos))
    h0 = cota_inferior(inicio, total)
    if h0 == 0:
        return 0
    mejor_g = {inicio: 0}
    # Prioridad (f, -g): a igual f se expande primero el estado más profundo.
    # No cambia la optimalidad (A* sigue sacando por f creciente) pero hace
    # que dentro del contorno óptimo la búsqueda baje "en profundidad" hacia
    # la meta en lugar de abrir todo el nivel.
    cola = [(h0, 0, inicio)]
    while cola:
        f, menos_g, estado = heapq.heappop(cola)
        g = -menos_g
        if g > mejor_g.get(estado, g):
            continue  # entrada vieja de la cola
        if f - g == 0:
            return g  # h = 0: meta (h consistente => g óptimo)
        for sig in vecinos(estado, capacidad):
            ng = g + 1
            if ng < mejor_g.get(sig, 1 << 30):
                mejor_g[sig] = ng
                heapq.heappush(cola, (ng + cota_inferior(sig, total), -ng, sig))
    return None


def main():
    lineas = sys.stdin.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(lineas):
        n, c = int(lineas[pos]), int(lineas[pos + 1])
        pos += 2
        if n == 0 and c == 0:
            break
        filas = lineas[pos:pos + c]
        pos += c
        r = minimo_movimientos(leer_silos(filas, n), c)
        salida.append(SIN_SOLUCION if r is None else str(r))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
