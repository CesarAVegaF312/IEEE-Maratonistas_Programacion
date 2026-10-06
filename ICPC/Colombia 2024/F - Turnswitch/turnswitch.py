"""
Colombia 2024 — F: Turnswitch («El interruptor giratorio»)
Ejecutar: python turnswitch.py < turnswitch.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    La nave Century Hawk debe saltar al hiperespacio, pero su regulador
    Turnswitch (una matriz N×N de interruptores horizontales/verticales)
    quedó desordenado. Girar un interruptor también gira sus vecinos
    ortogonales. La nave salta si todos quedan en la misma posición.

QUÉ HAY QUE HACER
    Entrada: varios casos; N (1 ≤ N ≤ 10) y N líneas de N caracteres
             '|' o '-'. Termina con 0. Siempre existe solución.
    Salida:  por caso, el mínimo número de interruptores a girar para que
             todos queden '-' o todos queden '|'.
    (Nota: en el PDF original las tres figuras del ejemplo son la misma
    imagen; nos guiamos por el texto.)

IDEA Y ALGORITMO
    Es el juego "Lights Out" con dos posibles objetivos. Observaciones:
      • Girar dos veces el mismo interruptor no hace nada y el orden no
        importa (todo es XOR) ⇒ una solución es un CONJUNTO de casillas.
      • Fijado qué se gira en la fila 0, la fila 1 queda FORZADA: la única
        forma de corregir la casilla (0, c) sin tocar la fila 0 otra vez es
        girar (1, c). En general, el estado de la fila i (tras los giros de
        las filas i-1 e i) determina los giros de la fila i+1. Al final solo
        hay que comprobar que la última fila quedó bien.
    Por eso basta enumerar los 2^N patrones de la primera fila (≤ 1024) para
    cada uno de los 2 objetivos y propagar fila por fila: "chasing the
    lights". Cada fila se representa como máscara de bits, y girar el
    patrón p en una fila cambia esa fila por p ^ (p<<1) ^ (p>>1) y a las
    filas vecinas por p.
    Probar los 2^(N²) conjuntos (fuerza bruta) sería imposible para N = 10.

MACROALGORITMO
    1. Leer la matriz y convertir cada fila en máscara (bit c = 1 si '|').
    2. Para cada objetivo (todo 0 o todo 1) y cada patrón p0 de la fila 0:
       a. Copiar las filas; aplicar p0 a la fila 0 (y su efecto en fila 1).
       b. Para i = 1..N-1: p_i = fila[i-1] XOR objetivo (lo que falta
          corregir arriba); aplicarlo a las filas i-1, i, i+1.
       c. Si la última fila coincide con el objetivo, la solución es
          válida; su costo es la suma de bits de todos los p_i.
    3. Imprimir el mínimo costo encontrado.

COMPLEJIDAD
    O(2 · 2^N · N) operaciones de máscara por caso ≈ 2·10⁴ para N = 10.
    Un archivo con 100 casos de N = 10 tarda ~1,3 s.

EJEMPLO A MANO
    Primer caso (-||, ---, |-|), objetivo todo '-' (bits 0). Con p0 = 000:
    fila 0 = -|| ⇒ p1 = 110 (columnas 1 y 2, contando desde la izquierda);
    tras girarlas la fila 1 queda |-- ⇒ p2 = 100 (columna 0); la fila 2
    queda --- ⇒ válido con 3 giros: (1,1), (1,2), (2,0). Ningún otro
    patrón da menos, respuesta 3.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/F")
    - Fuerza bruta: OK en 300 matrices aleatorias con N ≤ 4 contra la
      enumeración de los 2^(N²) conjuntos de giros (incluye casos sin
      solución para un objetivo; para ambos se devuelve el mínimo válido).
"""
import sys


def minimo_giros(filas, n):
    """filas: lista de n máscaras (bit c = 1 si el interruptor es '|')."""
    completo = (1 << n) - 1
    mejor = None
    for objetivo in (0, completo):              # todo '-' o todo '|'
        for p0 in range(1 << n):
            estado = filas[:]                    # copia de trabajo
            costo = 0
            presion = p0
            for i in range(n):
                if i > 0:
                    # La fila i-1 solo puede corregirse girando la fila i.
                    presion = estado[i - 1] ^ objetivo
                if presion:
                    costo += bin(presion).count("1")
                    # Efecto en la propia fila: la casilla y sus vecinas izq./der.
                    estado[i] ^= (presion ^ (presion << 1) ^ (presion >> 1)) & completo
                    if i > 0:
                        estado[i - 1] ^= presion
                    if i + 1 < n:
                        estado[i + 1] ^= presion
            if estado[n - 1] == objetivo and (mejor is None or costo < mejor):
                mejor = costo
    return mejor


def main():
    tokens = sys.stdin.read().split()
    pos = 0
    salida = []
    while pos < len(tokens):
        n = int(tokens[pos]); pos += 1
        if n == 0:
            break
        filas = []
        for _ in range(n):
            linea = tokens[pos]; pos += 1
            mascara = 0
            for c, ch in enumerate(linea):
                if ch == '|':
                    mascara |= 1 << c
            filas.append(mascara)
        salida.append(str(minimo_giros(filas, n)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
