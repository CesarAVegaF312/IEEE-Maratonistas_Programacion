"""
Colombia 2023 — J: TNumbers («Números T»)
Ejecutar: python tnumbers.py < tnumbers.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    1 + 2 = 3: los números 1..3 se parten en dos bloques consecutivos de igual
    suma. Un TNumber es un n para el que existe k (1 ≤ k < n) con
    1 + … + k = (k+1) + … + n.

QUÉ HAY QUE HACER
    Entrada: varios casos "a b" (1 ≤ a ≤ b ≤ 10^8); termina con "0 0".
    Salida:  por caso, cuántos TNumbers hay en [a, b].

IDEA Y ALGORITMO
    Ecuación de Pell negativa.
    La condición es T(k) = T(n) - T(k), con T(x) = x(x+1)/2, o sea
    n(n+1)/2 = k(k+1). Multiplicando por 8 y completando cuadrados:
        (2n+1)^2 - 1 = 2((2k+1)^2 - 1)  =>  (2n+1)^2 - 2(2k+1)^2 = -1.
    Con x = 2n+1, y = 2k+1 queda x^2 - 2y^2 = -1, la Pell negativa, cuyas
    soluciones positivas son (1,1), (7,5), (41,29), (239,169), … y se
    generan con (x, y) -> (3x + 4y, 2x + 3y) (multiplicar por la unidad
    fundamental 3 + 2√2 de x^2 - 2y^2 = 1). Todas tienen x, y impares, así
    que dan n, k enteros. (1,1) da n = 0, que no cuenta.
    Los TNumbers crecen ~5,8 veces cada uno: hasta 10^8 hay solo un puñado
    (3, 20, 119, 696, 4059, 23660, 137903, 803760, 4684659, 27304196), así que
    se generan una vez y cada consulta solo los cuenta.
    El enfoque ingenuo (probar cada n y cada k) sería O(b) por consulta como
    mínimo; aquí cada consulta es O(#TNumbers) = O(log b).

MACROALGORITMO
    1. Generar los pares (x, y) de x^2 - 2y^2 = -1 con la recurrencia.
    2. Convertir cada uno en n = (x - 1) / 2, quedándose con 1 ≤ n ≤ 10^8.
    3. Para cada consulta (a, b), contar los n de la lista con a ≤ n ≤ b.

COMPLEJIDAD
    Precálculo O(log 10^8), cada consulta O(log 10^8). Memoria O(1).

EJEMPLO A MANO
    (7,5): n = 3, k = 2 -> 1+2 = 3. (41,29): n = 20, k = 14 -> 105 = 105.
    Consulta 1..5 -> solo 3 -> 1. Consulta 4..8 -> 0.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2023/J")
    - Fuerza bruta: lista de TNumbers hasta 200 000 calculada probando
      cada n con isqrt (¿n(n+1)/2 = k(k+1) para algún k?) coincide con la
      generada; además 500 consultas aleatorias en ese rango: OK.
"""
import sys

LIMITE = 10 ** 8


def generar_tnumbers(limite=LIMITE):
    """Lista ordenada de TNumbers n ≤ limite (soluciones de la Pell negativa)."""
    resultado = []
    x, y = 1, 1  # solución fundamental de x^2 - 2y^2 = -1
    while True:
        n = (x - 1) // 2
        if n > limite:
            break
        if n >= 1:  # (1,1) da n = 0, que no es positivo
            resultado.append(n)
        x, y = 3 * x + 4 * y, 2 * x + 3 * y
    return resultado


def main():
    tnumbers = generar_tnumbers()
    datos = sys.stdin.buffer.read().split()
    salida = []
    for i in range(0, len(datos) - 1, 2):
        a, b = int(datos[i]), int(datos[i + 1])
        if a == 0 and b == 0:
            break
        salida.append(str(sum(1 for n in tnumbers if a <= n <= b)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
