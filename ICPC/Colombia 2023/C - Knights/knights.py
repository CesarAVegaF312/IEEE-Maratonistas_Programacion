"""
Colombia 2023 — C: Knights («Caballos»)
Ejecutar: python knights.py < knights.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Dos caballos, KA y KB, están en un tablero n×n y quieren encontrarse.
    Se mueven por turnos (KA primero), un salto de caballo cada vez, sin
    salir del tablero. Se encuentran en k movimientos si en su k-ésimo
    movimiento KB cae en la casilla donde está KA.

QUÉ HAY QUE HACER
    Entrada: varios casos "n a b c d" (1 < n < 300, 0 ≤ a,b,c,d < n);
             KA está en (a,b) y KB en (c,d). Termina con "0 0 0 0 0".
    Salida:  por caso, el mínimo número de movimientos para encontrarse, o
             '*' si es imposible.

INTERPRETACIÓN USADA (literal, confirmada por el coordinador)
    KA mueve primero y se alternan sin poder pasar turno. Se encuentran
    cuando KB, en su k-ésimo movimiento, cae sobre la casilla de KA; en ese
    momento AMBOS han hecho exactamente k movimientos. Si empiezan en la
    misma casilla, la respuesta es 0. Que KA caiga sobre KB no cuenta.

INCONSISTENCIA DEL EJEMPLO (importante)
    Con esta lectura el ejemplo 1 del enunciado, "8 0 0 5 4 -> 2", es
    imposible: (0,0) y (5,4) son casillas de distinto color y, como se
    explica abajo, entonces nunca pueden encontrarse. Esta solución imprime
    '*' en ese caso, así que probar.py marca FALLA en el ejemplo DE FORMA
    ESPERADA. La misma lectura sí reproduce el ejemplo trabajado del texto
    ((0,0) y (6,2) en 8×8 -> 2) y los ejemplos 2 y 3 ('*' y 1).
    Se probaron otras lecturas (KA también puede caer sobre KB, se puede
    pasar turno, contar rondas o movimientos de uno solo, un error de
    límites en el tablero): ninguna da los tres resultados del ejemplo a la
    vez, porque los ejemplos 1 y 2 son ambos pares de distinto color a
    distancia 3 y toda lectura natural los trata igual. Por eso NO hay
    ningún caso especial para forzar el 2.

IDEA Y ALGORITMO
    BFS en el grafo del caballo + argumento de paridad (grafo bipartito).
    Se encuentran en k movimientos si y solo si existe una casilla s a la que
    KA llega con un camino de exactamente k saltos y KB también. Pegando el
    camino de KA con el de KB al revés se obtiene un camino de 2k saltos de
    A a B; y al revés, si hay un camino de A a B de largo 2k, su casilla del
    medio sirve como s. Por tanto:
        se encuentran en k  <=>  hay un camino de A a B de largo exactamente 2k.
    El grafo del caballo es bipartito (cada salto cambia el color i+j mod 2),
    así que todos los caminos de A a B tienen la misma paridad que la
    distancia d = dist(A, B), y existen caminos de largo d, d+2, d+4, …
    (ir y volver). Conclusión:
        - A = B                       -> 0
        - B inalcanzable desde A      -> '*'
        - d impar (distinto color)    -> '*'
        - d par                       -> d / 2  (el mínimo k con 2k ≥ d)

MACROALGORITMO
    1. Leer n, a, b, c, d; si todo es 0, terminar.
    2. Si (a,b) = (c,d), imprimir 0.
    3. BFS desde (a,b) en el tablero n×n con los 8 saltos de caballo, hasta
       llegar a (c,d) o agotar las casillas.
    4. Si no se llegó o la distancia es impar, imprimir '*'.
    5. Si no, imprimir distancia / 2.

COMPLEJIDAD
    BFS O(n^2) por caso (≤ 89 401 casillas), memoria O(n^2).

EJEMPLO A MANO
    6×6, KA (1,2), KB (5,4): distancia 2 (por (3,3)) -> 1.
    3×3, KA (0,0), KB (0,1): distancia 3, impar -> '*'.
    8×8, KA (0,0), KB (6,2): distancia 4 -> 2 (ejemplo trabajado del texto).

VERIFICACIÓN
    - Ejemplo del enunciado: 2 de 3 líneas iguales; la línea 1 da '*' en vez
      de 2 por la inconsistencia descrita arriba (FALLA esperada en
      python probar.py "Colombia 2023/C").
    - Fuerza bruta: BFS sobre estados (posición KA, posición KB, turno) que
      simula literalmente los turnos; coincide con esta solución en todos
      los pares de casillas de tableros 2..6 y en 300 casos aleatorios con
      n ≤ 12.
"""
import sys
from collections import deque

SALTOS = ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1))


def distancia_caballo(n, origen, destino):
    """Distancia BFS en saltos de caballo en un tablero n×n (None si no se llega)."""
    if origen == destino:
        return 0
    # dist guarda -1 para casillas no visitadas; se indexa por fila*n + columna.
    dist = [-1] * (n * n)
    oi, oj = origen
    dist[oi * n + oj] = 0
    meta = destino[0] * n + destino[1]
    cola = deque([(oi, oj)])
    while cola:
        i, j = cola.popleft()
        siguiente = dist[i * n + j] + 1
        for di, dj in SALTOS:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n:
                idx = ni * n + nj
                if dist[idx] < 0:
                    if idx == meta:
                        return siguiente
                    dist[idx] = siguiente
                    cola.append((ni, nj))
    return None


def resolver(n, a, b, c, d):
    dist = distancia_caballo(n, (a, b), (c, d))
    # Inalcanzable o de distinto color (distancia impar): nunca coinciden
    # justo después de un movimiento de KB.
    if dist is None or dist % 2 == 1:
        return "*"
    return str(dist // 2)


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for p in range(0, len(datos) - 4, 5):
        n, a, b, c, d = (int(v) for v in datos[p:p + 5])
        if n == 0 and a == 0 and b == 0 and c == 0 and d == 0:
            break
        salida.append(resolver(n, a, b, c, d))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
