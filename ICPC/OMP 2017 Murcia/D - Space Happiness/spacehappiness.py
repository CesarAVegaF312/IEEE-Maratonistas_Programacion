"""
OMP 2017 Murcia — D: Space Happiness («Felicidad espacial»)
Ejecutar: python spacehappiness.py < spacehappiness.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Bután quiere mandar un cohete a Marte. El cohete acelera de 0 hasta una
    velocidad máxima s y luego frena hasta 0, pero su velocímetro barato solo
    registra velocidades impares: 0, 1, 3, …, s, …, 3, 1, 0. Pasar de la
    velocidad i a la j cuesta j millones de ngultrums.

QUÉ HAY QUE HACER
    Entrada: t casos; cada uno es un impar s (velocidad máxima).
    Salida:  una línea por caso con el costo total del viaje.
    Restricciones clave: s ≤ 10^9 + 1 (el enunciado omite la cota inferior;
    se asume s ≥ 1). El resultado llega a ~5·10^17: no cabe en 32 bits, pero
    en Python los enteros no tienen límite.

IDEA Y ALGORITMO
    Fórmula cerrada (suma de impares consecutivos).
    La secuencia es 0, 1, 3, …, s-2, s, s-2, …, 3, 1, 0. Cada transición
    cuesta la velocidad de LLEGADA, así que el costo total es la suma de
    todos los términos salvo el 0 inicial:
        (1 + 3 + … + (s-2))  +  s  +  (s-2 + … + 3 + 1)  +  0
    La suma de los primeros m impares es m² (identidad clásica: cada impar
    2k-1 = k² - (k-1)², suma telescópica). Aquí hay m = (s-1)/2 impares
    menores que s, así que
        costo = s + 2·m² = s + (s-1)²/2.
    Simular la secuencia costaría O(s) = 10^9 pasos por caso: imposible; la
    fórmula es O(1).

MACROALGORITMO
    1. Leer t y los t valores de s.
    2. Para cada s: m = (s-1)//2; costo = s + 2*m*m.
    3. Imprimir cada costo en su línea.

COMPLEJIDAD
    Tiempo O(t), memoria O(t). Caso grande (200 000 casos con s ≈ 10^9):
    ~0.2 s.

EJEMPLO A MANO
    s = 7 → secuencia 0,1,3,5,7,5,3,1,0 → 1+3+5+7+5+3+1+0 = 25;
    fórmula: m = 3 → 7 + 2·9 = 25.  s = 11 → m = 5 → 11 + 50 = 61.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "OMP 2017/D")
    - Fuerza bruta: OK contra la simulación literal de la secuencia para todos
      los impares s de 1 a 2001.
"""
import sys


def costo_total(s):
    """Costo de 0 → 1 → 3 → … → s → … → 3 → 1 → 0 (se paga la velocidad de llegada)."""
    m = (s - 1) // 2          # cantidad de impares estrictamente menores que s
    return s + 2 * m * m      # subida (m²) + pico (s) + bajada (m²) + llegada a 0 (0)


def main():
    datos = sys.stdin.buffer.read().split()
    t = int(datos[0])
    salida = [str(costo_total(int(x))) for x in datos[1:1 + t]]
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
