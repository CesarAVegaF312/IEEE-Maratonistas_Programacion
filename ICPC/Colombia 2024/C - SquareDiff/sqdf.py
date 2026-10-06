"""
Colombia 2024 — C: SquareDiff («Diferencia de cuadrados»)
Ejecutar: python sqdf.py < sqdf.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Alana juega con diferencias de cuadrados (1²−0² = 1, 6²−4² = 20, …) y
    nota que nunca encuentra x, y con x² − y² = 2. Quiere saber qué enteros
    se pueden escribir como diferencia de dos cuadrados de enteros.

QUÉ HAY QUE HACER
    Entrada: varios enteros N (0 < N < 40 000), uno por línea; termina en 0.
    Salida:  por cada N, "Y" si existe (x, y) enteros con x² − y² = N, "N" si no.

IDEA Y ALGORITMO
    Teoría de números (factorización de la diferencia de cuadrados):
        N = x² − y² = (x − y)(x + y) = a · b,   con a = x − y, b = x + y.
    a y b tienen la MISMA paridad (su suma 2x es par). Recíprocamente, si
    N = a·b con a, b de igual paridad, x = (a+b)/2, y = (b−a)/2 son enteros.
      • N impar: a = 1, b = N (ambos impares) ⇒ siempre se puede.
      • N ≡ 0 (mod 4): a = 2, b = N/2 (ambos pares) ⇒ se puede.
      • N ≡ 2 (mod 4): un factor par y otro impar siempre (no pueden ser
        ambos pares porque 4 ∤ N, ni ambos impares porque N es par) ⇒ NO.
    Conclusión: respuesta "N" exactamente cuando N mod 4 == 2.

MACROALGORITMO
    1. Leer enteros hasta encontrar 0.
    2. Para cada N imprimir "N" si N % 4 == 2, si no "Y".

COMPLEJIDAD
    O(1) por caso; O(número de casos) en total (10⁵ casos: ~0,2 s).

EJEMPLO A MANO
    1 → impar → Y;  2 → 2 mod 4 = 2 → N;  3 → Y;  20 → 0 mod 4 → Y (6²−4²).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/C")
    - Fuerza bruta: OK para TODOS los N de 1 a 39 999, comparando con una
      búsqueda directa de divisores a·b = N con a, b de igual paridad.
"""
import sys


def es_diferencia_de_cuadrados(n):
    """True si n = x² − y² para enteros x, y (n > 0)."""
    return n % 4 != 2


def main():
    salida = []
    for tok in sys.stdin.buffer.read().split():
        n = int(tok)
        if n == 0:
            break
        salida.append("Y" if es_diferencia_de_cuadrados(n) else "N")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
