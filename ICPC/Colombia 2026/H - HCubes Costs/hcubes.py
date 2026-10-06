"""
Colombia 2026 — H: HCubes Costs («Costos en hipercubos»)
Ejecutar: python hcubes.py < hcubes.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    La start-up ICPC (InterConnectivity Per Cubes) diseña redes con forma de
    n-hipercubo: los nodos son las cadenas binarias de n bits y dos nodos
    están unidos si difieren en exactamente un bit. Cada arista tiene un costo
    definido recursivamente y quieren el costo mínimo de comunicar dos nodos.

QUÉ HAY QUE HACER
    Entrada: varios casos, uno por línea: n a b (a y b son los nodos escritos
             en decimal). Termina con la línea "0 0 0" (no se procesa).
    Salida:  por caso, una línea con el costo del camino más barato de a a b.
    Restricciones clave: 0 < n <= 20, 0 <= a, b < 2^n. La cantidad de casos
             no está acotada en el enunciado (puede haber cientos de miles).

    Costos (con xu = "el bit x pegado ANTES de la cadena u"):
        c_1(0, 1) = 1
        c_{n+1}(xu, xv) = c_n(u, v)          (aristas dentro de cada copia)
        c_{n+1}(xu, yu) = n + 1, si x != y   (arista que cambia el bit nuevo)

IDEA Y ALGORITMO
    Observación 1 — cada bit tiene un costo fijo. El bit que se agrega al
    pasar de H_n a H_{n+1} es el de MÁS A LA IZQUIERDA (el más significativo)
    y la arista que lo cambia cuesta n+1. Las aristas de las copias conservan
    su costo, así que al seguir creciendo el cubo ese bit sigue costando n+1.
    Desenrollando la recursión: cambiar el bit de la posición i (contando
    desde 0 por la derecha, es decir, el de valor 2^i) cuesta SIEMPRE i + 1,
    sin importar n ni los demás bits.
    Comprobación con el enunciado: en H_3, 000-001 cuesta 1, 000-010 cuesta 2
    y 000-100 cuesta 3.

    Observación 2 — qué bits cambiar. Un camino de a a b es una secuencia de
    cambios de un bit. Cada bit en el que a y b difieren (los bits en 1 de
    a XOR b) debe cambiarse un número IMPAR de veces (≥ 1); cada bit en el
    que coinciden, un número PAR (≥ 0). Como todos los costos son positivos,
    lo óptimo es cambiar cada bit distinto exactamente una vez y no tocar los
    demás; el orden no importa. Por tanto:
        respuesta = suma de (i + 1) sobre los bits i encendidos de a XOR b.

    Truco de rendimiento: puede haber muchísimos casos, así que en vez de
    recorrer los 20 bits en cada uno, se precalcula una tabla para los 10
    bits bajos y otra para los 10 bits altos (2 x 1024 entradas) y cada caso
    se responde con dos consultas a tabla (O(1)).
        alto: bit i+10 cuesta (i + 1) + 10, así que
        COSTO_ALTO[h] = COSTO_BAJO[h] + 10 * popcount(h).

MACROALGORITMO
    1. Precalcular COSTO_BAJO[m] = suma de (i+1) por cada bit i de m, m < 1024.
    2. Precalcular COSTO_ALTO[h] = COSTO_BAJO[h] + 10 * popcount(h).
    3. Leer todos los tokens de la entrada de una vez.
    4. Para cada caso (n, a, b) hasta "0 0 0": x = a XOR b.
    5. Respuesta = COSTO_BAJO[x & 1023] + COSTO_ALTO[x >> 10].
    6. Imprimir todas las respuestas juntas.

COMPLEJIDAD
    Tiempo O(1) por caso (+ O(2^10) de precálculo), memoria O(número de
    casos) para la salida. Con el archivo del usuario de 300 000 casos
    (entrada_hcubes_limite.txt, 5 MB) tarda ~0.3 s.

EJEMPLO A MANO
    3 6 2: 110 XOR 010 = 100 -> bit 2 -> costo 3.
    3 1 6: 001 XOR 110 = 111 -> bits 0,1,2 -> 1 + 2 + 3 = 6.
    2 3 3: XOR = 0 -> 0.      1 0 1: XOR = 1 -> bit 0 -> 1.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/H")
    - Fuerza bruta: OK en 3000 casos aleatorios (n <= 7) contra Dijkstra
      sobre el hipercubo construido LITERALMENTE con la definición recursiva
      de los costos; además coincide con hcubes.py del usuario en los
      300 000 casos de entrada_hcubes_limite.txt.
"""
import sys

# --- Precálculo de los costos por bloques de 10 bits -------------------------
# COSTO_BAJO[m]: costo de cambiar los bits encendidos de m, si m ocupa los
# bits 0..9 (el bit i cuesta i + 1).
COSTO_BAJO = [0] * 1024
for m in range(1, 1024):
    bajo = (m & -m).bit_length() - 1          # índice del bit más bajo de m
    COSTO_BAJO[m] = COSTO_BAJO[m & (m - 1)] + bajo + 1

# COSTO_ALTO[h]: lo mismo, pero si h ocupa los bits 10..19: cada bit cuesta
# 10 más que su homólogo bajo.
COSTO_ALTO = [COSTO_BAJO[h] + 10 * bin(h).count("1") for h in range(1024)]


def costo_minimo(a, b):
    """Costo del camino más barato entre los nodos a y b (n <= 20)."""
    x = a ^ b                                 # bits que hay que cambiar
    return COSTO_BAJO[x & 1023] + COSTO_ALTO[x >> 10]


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    # Cada caso son 3 tokens; se para en "0 0 0" (o si la entrada se acaba).
    for idx in range(0, len(datos) - 2, 3):
        n, a, b = int(datos[idx]), int(datos[idx + 1]), int(datos[idx + 2])
        if n == 0 and a == 0 and b == 0:
            break
        salida.append(costo_minimo(a, b))
    sys.stdout.write("\n".join(map(str, salida)) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
