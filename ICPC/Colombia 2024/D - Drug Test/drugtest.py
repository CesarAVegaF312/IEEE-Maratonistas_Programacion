"""
Colombia 2024 — D: Drug Test («Prueba de un medicamento»)
Ejecutar: python drugtest.py < drugtest.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    La empresa ACIS prueba un medicamento X con paquetes de k píldoras
    (k-paquetes), cada uno "activo" (con X) o "placebo" (sin X); el paquete
    vacío (k = 0) es placebo. Cada individuo recibe un activo y un placebo.

QUÉ HAY QUE HACER
    Hay que etiquetar cada tamaño k ∈ [0, N] como A (activo) o P (placebo)
    de modo que:
      c1: cada individuo recibe un activo de tamaño a y un placebo de tamaño p
          con a + p potencia de 2;
      c2: todo tamaño 0..N aparece en algún par.
    Se garantiza que el diseño es único. Responder Q consultas q_k.
    Entrada: varios casos "N Q" (0 < N < 10 000, 0 < Q ≤ 100) seguidos de
             Q enteros; termina con "0 0".
    Salida:  por caso, una cadena de Q letras A/P sin espacios.

IDEA Y ALGORITMO
    Modelo de grafos: vértices 0..N, arista k — j si k ≠ j y k + j es
    potencia de 2. El diseño es una 2-coloración (bipartición) en la que
    todo vértice tiene al menos un vecino: cada par (a, p) es una arista
    con extremos de colores distintos. Si el grafo es conexo, la
    2-coloración es única fijando 0 = placebo; esa es la unicidad que
    menciona el enunciado.

    Observación clave (recurrencia): para k ≥ 1 sea P la menor potencia de
    2 con P ≥ k. Entonces j = P − k cumple 0 ≤ j < k (si k es potencia de 2,
    j = 0; si no, P/2 < k < P ⇒ 0 < P − k < k). Así cada k tiene un vecino
    menor que él ⇒ por inducción el grafo sobre [0, N] es conexo para todo
    N, y el color de k queda determinado:
            color(0) = P,   color(k) = opuesto de color(P − k).
    Como el grafo de [0, N] es un subgrafo inducido conexo del grafo de
    [0, 9999], la coloración NO depende de N: se precalcula una sola vez
    para 0..9999 y cada consulta es O(1). (Que el grafo sea bipartito, es
    decir, que esta coloración respete TODAS las aristas, lo garantiza el
    enunciado; además se comprobó explícitamente para 0..9999.)

MACROALGORITMO
    1. color[0] = 'P'.
    2. Para k = 1..9999: P = menor potencia de 2 ≥ k; color[k] = opuesto
       de color[P − k].
    3. Para cada caso, leer las Q consultas y concatenar color[q].

COMPLEJIDAD
    Precálculo O(MAX), cada consulta O(1). 1000 casos × 100 consultas: ~0,15 s.

EJEMPLO A MANO
    N = 12: 1 → P=1, vecino 0 (P) ⇒ A. 3 → P=4, vecino 1 (A) ⇒ P.
    5 → P=8, vecino 3 (P) ⇒ A. 7 → vecino 1 ⇒ P. 9 → P=16, vecino 7 ⇒ A.
    Consultas 1 3 5 7 9 ⇒ "APAPA". ✔

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/D")
    - Fuerza bruta: OK. Para cada N ≤ 14 se enumeraron las 2^(N+1)
      etiquetas con 0 = P, exigiendo c2 y que TODO par k + j = 2^m una un
      activo con un placebo; hay exactamente una y coincide con la nuestra.
      Además se comprobó que para 0..9999 toda arista k + j = 2^m une
      colores distintos (grafo bipartito).
    - Nota de interpretación: si c1 se leyera solo como "los pares que se
      usan deben sumar potencia de 2" (pudiendo existir k, j del mismo tipo
      con k + j = 2^m), el diseño NO sería único (p. ej. N = 3 admite PAAP y
      PPAA). La unicidad que afirma el enunciado y la lista de pares del
      ejemplo N = 12 (que es exactamente el conjunto de TODAS las aristas)
      confirman la lectura usada: cada par que suma potencia de 2 es
      (activo, placebo), es decir, una 2-coloración propia.
"""
import sys

MAX = 10000   # N < 10 000


def precalcular_colores(limite):
    """color[k] = 'A' o 'P' para k en [0, limite)."""
    color = ['P'] * limite          # el paquete vacío (0) es placebo
    potencia = 1                    # menor potencia de 2 que sea ≥ k
    for k in range(1, limite):
        while potencia < k:
            potencia *= 2
        vecino = potencia - k       # 0 ≤ vecino < k, ya coloreado
        color[k] = 'A' if color[vecino] == 'P' else 'P'
    return color


def main():
    color = precalcular_colores(MAX)
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        n, q = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        if n == 0 and q == 0:
            break
        consultas = datos[pos:pos + q]
        pos += q
        salida.append("".join(color[int(c)] for c in consultas))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
