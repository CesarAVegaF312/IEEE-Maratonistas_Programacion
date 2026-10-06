"""
Colombia 2024 — K: Skyline («Perfil urbano»)
Ejecutar: python skyline.py < skyline.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Lucy Diamond, arquitecta, compara perfiles urbanos. Mide qué tan
    "desordenadas" están las alturas de los edificios de una ciudad como la
    fracción de pares (i < j) con h_i > h_j.

QUÉ HAY QUE HACER
    Entrada: varios casos; N (0 < N < 10⁵) y una línea con N alturas
             enteras. Termina con 0.
    Salida:  por caso, HD / PHD con 3 decimales, donde HD = número de pares
             i < j con h_i > h_j (inversiones) y PHD = N(N−1)/2; si N = 1,
             se imprime 0.000.
    Nota: el enunciado dice −20 < h < 300 pero el ejemplo usa −29; por eso
    NO se asume ninguna cota: se comprimen las alturas a rangos.

IDEA Y ALGORITMO
    Conteo de inversiones con un árbol de Fenwick (BIT).
    Recorriendo de izquierda a derecha, al llegar a h_j las inversiones que
    terminan en j son los i < j ya vistos con h_i > h_j = (vistos) −
    (vistos con altura ≤ h_j). El BIT indexado por el rango de la altura
    responde "cuántos vistos con rango ≤ r" en O(log N) y se actualiza en
    O(log N). Las alturas se comprimen (valores distintos ordenados) para
    que el BIT tenga tamaño ≤ N sin importar el rango real de h.
    PHD = N(N−1)/2 es el número de pares (todos podrían estar invertidos).
    El ingenuo O(N²) (5·10⁹ pares) no alcanza.

MACROALGORITMO
    1. Leer N y las alturas.
    2. Si N == 1: imprimir 0.000.
    3. Comprimir alturas a rangos 1..K.
    4. Para cada altura en orden: HD += vistos − consulta(rango);
       actualizar(rango, +1); vistos += 1.
    5. Imprimir HD / (N(N−1)/2) con 3 decimales ("%.3f", como printf).

COMPLEJIDAD
    O(N log N) tiempo, O(N) memoria. N = 99 999 tarda ~0,3 s en Python.

EJEMPLO A MANO
    28 30 −29 28: inversiones (28,−29), (30,−29), (30,28) = 3; PHD = 6 ⇒
    0.500.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/K")
    - Fuerza bruta: OK en 500 casos aleatorios (N ≤ 30, alturas con muchas
      repeticiones y negativas) contra el conteo O(N²) de pares.
"""
import sys


def contar_inversiones(alturas):
    """Número de pares i < j con alturas[i] > alturas[j]."""
    rango = {v: i + 1 for i, v in enumerate(sorted(set(alturas)))}
    k = len(rango)
    arbol = [0] * (k + 1)              # Fenwick: frecuencias por rango
    inversiones = 0
    vistos = 0
    for h in alturas:
        r = rango[h]
        # Cuántos vistos tienen rango ≤ r (prefijo del Fenwick).
        menores_o_iguales = 0
        i = r
        while i > 0:
            menores_o_iguales += arbol[i]
            i -= i & -i
        inversiones += vistos - menores_o_iguales
        # Registrar esta altura.
        i = r
        while i <= k:
            arbol[i] += 1
            i += i & -i
        vistos += 1
    return inversiones


def medida(alturas):
    n = len(alturas)
    if n < 2:
        return 0.0
    return contar_inversiones(alturas) / (n * (n - 1) // 2)


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos]); pos += 1
        if n == 0:
            break
        alturas = list(map(int, datos[pos:pos + n]))
        pos += n
        salida.append("%.3f" % medida(alturas))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
