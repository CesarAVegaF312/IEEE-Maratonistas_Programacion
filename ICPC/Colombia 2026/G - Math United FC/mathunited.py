"""
Colombia 2026 — G: Math United FC («Math United FC»)
Ejecutar: python mathunited.py < mathunited.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    La división de traspasos de un club empieza con un presupuesto B que
    nunca puede volverse negativo. Revisa una lista de jugadores EN ORDEN:
    los "comerciales" (valor > 0) suben el presupuesto; los "prospectos"
    (valor <= 0) lo bajan o lo dejan igual. Se quiere contratar la mayor
    cantidad posible de prospectos.

QUÉ HAY QUE HACER
    Entrada: varios casos; "B P" y una línea con los P valores en orden.
             Termina con "0 0".
    Salida:  por caso, el máximo número de prospectos contratables
             manteniendo el presupuesto >= 0 en todo momento.
    Restricciones clave: P <= 2·10^5, |valor| <= 10^9, 0 <= B <= 10^9.

IDEA Y ALGORITMO
    1) Contratar a TODOS los comerciales: solo suben el presupuesto, y lo que
       se maximiza son los prospectos, así que nunca estorban.
    2) Prospectos: algoritmo voraz con "arrepentimiento" usando un montículo
       (heap) de máximos con los costos de los prospectos ya contratados.
       Se contrata cada prospecto que llega; si el presupuesto queda
       negativo, se "descontrata" el MÁS CARO contratado hasta ahora
       (puede ser el recién llegado). Con eso el presupuesto vuelve a ser
       >= 0 (ese costo es >= al que lo hizo negativo) y la cantidad
       contratada baja en 1.

    ¿Por qué es óptimo? Invariante: tras procesar el prefijo t, el conjunto
    contratado tiene el MÁXIMO tamaño posible para ese prefijo y, entre los
    de ese tamaño, el MAYOR presupuesto restante (la menor suma de costos).
    Al llegar un prospecto nuevo: si cabe, el tamaño sube en 1 (no se puede
    subir más). Si no cabe, no existe ningún conjunto válido de tamaño
    (anterior + 1) en el prefijo t+1 — tendría que tener un conjunto de
    tamaño "anterior" en el prefijo t más este prospecto, y ninguno deja
    presupuesto suficiente —; cambiar el más caro por el nuevo conserva el
    tamaño y deja el presupuesto más alto posible. Además, quitar un
    prospecto anterior solo SUBE el presupuesto en todos los puntos
    intermedios, así que el conjunto sigue siendo válido en todo el prefijo
    (es el clásico argumento de intercambio del problema "Potions" de
    Codeforces 1526C2).
    Los prospectos de valor 0 entran siempre (costo 0, jamás se sacan
    antes que uno con costo > 0).

    "Decidir sobre la marcha" del enunciado es solo ambientación: la
    respuesta es el máximo sobre todas las decisiones posibles en orden.

MACROALGORITMO
    1. presupuesto = B, heap vacío (costos de prospectos contratados).
    2. Para cada valor v de la lista:
         - si v > 0: presupuesto += v.
         - si v <= 0: presupuesto -= |v|; meter |v| al heap;
           si presupuesto < 0: sacar el mayor costo c del heap y
           presupuesto += c.
    3. Respuesta = tamaño del heap.

COMPLEJIDAD
    O(P log P) tiempo, O(P) memoria por caso. Caso grande (5 casos con
    P = 2·10^5, valores aleatorios): ≈ 0.9 s.

EJEMPLO A MANO
    B = 9, valores -4 -7 5 -6 -1 -4:
      -4 → 5 {4};  -7 → -2 < 0, sale 7 → 5 {4};  +5 → 10;
      -6 → 4 {4,6};  -1 → 3 {4,6,1};  -4 → -1 < 0, sale 6 → 5 {4,1,4}.
    Respuesta 3 (A, E, F, como dice el enunciado).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/G")
    - Fuerza bruta (todos los 2^P subconjuntos, simulando el presupuesto
      en orden): idéntica en 2000 casos aleatorios con P <= 12.
"""
import sys
from heapq import heappush, heappushpop


def resolver(presupuesto, valores):
    # heapq es un montículo de MÍNIMOS: se guardan los costos negados para
    # tener a mano el prospecto más caro (el de -costo más pequeño).
    heap = []
    for v in valores:
        if v > 0:
            presupuesto += v                 # comercial: siempre se contrata
            continue
        # Prospecto de costo -v >= 0: se contrata...
        presupuesto += v
        if presupuesto >= 0:
            heappush(heap, v)                # v = -costo
        else:
            # ...y si el presupuesto quedó negativo se descontrata el más
            # caro (incluido el recién llegado). heappushpop mete v y saca el
            # menor elemento (= el de mayor costo) en una sola operación.
            mas_caro = heappushpop(heap, v)
            presupuesto -= mas_caro          # devolver su costo (-mas_caro)
    return len(heap)


def main():
    datos = sys.stdin.buffer.read().split()
    idx, salida = 0, []
    while idx + 1 < len(datos):
        b, p = int(datos[idx]), int(datos[idx + 1])
        idx += 2
        if b == 0 and p == 0:                # fin de la entrada
            break
        valores = list(map(int, datos[idx: idx + p]))
        idx += p
        salida.append(resolver(b, valores))
    sys.stdout.write("\n".join(map(str, salida)) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
