"""
Colombia 2025 — B: Binary Dozens («Docenas binarias»)
Ejecutar: python bindozens.py < bindozens.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Egan vende nano-huevos solo en nano-cajas completas de 12. Dado el número
    de huevos producidos H (escrito en binario), los que no completan una caja
    se descartan.

QUÉ HAY QUE HACER
    Entrada: varias líneas, cada una una cadena binaria B (1 ≤ |B| ≤ 500).
             Una línea con "*" termina la entrada.
    Salida:  por cada B, el número de huevos sobrantes D = H mod 12, en decimal.
    Restricciones clave: |B| ≤ 500 bits (H puede tener ~150 dígitos decimales).

IDEA Y ALGORITMO
    D = H mod 12. Hay dos formas igual de válidas:
      a) Python tiene enteros de precisión arbitraria: int(B, 2) % 12.
      b) Esquema de Horner con aritmética modular (lo que se haría en C/Java):
         recorriendo los bits de izquierda a derecha, H = 2·H + bit, y como
         (2·H + bit) mod 12 = (2·(H mod 12) + bit) mod 12, basta guardar el
         resto en cada paso. Nunca se manejan números grandes.
    Se implementa (b) por ser la idea "de verdad" del problema; (a) se usa
    como verificación.

MACROALGORITMO
    1. Leer líneas hasta encontrar "*".
    2. Para cada cadena: resto = 0; por cada bit, resto = (2·resto + bit) % 12.
    3. Imprimir el resto.

COMPLEJIDAD
    Tiempo O(|B|) por caso, memoria O(1) adicional.

EJEMPLO A MANO
    B = 100001 (= 33): restos 1, 2, 4, 8, 16%12=4, 9 → D = 9.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/B")
    - Fuerza bruta int(B, 2) % 12: OK en 2000 cadenas aleatorias de hasta 500 bits.
    - Caso grande (20 000 cadenas de 500 bits): ~0.6 s.
"""
import sys


def sobrantes(binario):
    """H mod 12 calculado con Horner modular, sin números grandes."""
    resto = 0
    for bit in binario:
        resto = (2 * resto + (bit == "1")) % 12
    return resto


def main():
    salida = []
    for linea in sys.stdin:
        b = linea.strip()
        if b == "*":  # fin de la entrada
            break
        if not b:     # tolerar líneas en blanco
            continue
        salida.append(str(sobrantes(b)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
