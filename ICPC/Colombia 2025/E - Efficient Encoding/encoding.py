"""
Colombia 2025 — E: Efficient Encoding («Codificación eficiente»)
Ejecutar: python encoding.py < encoding.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En el año 3057 el ICPC comprime mensajes con un código binario libre de
    prefijos óptimo (Huffman). La frecuencia esperada de cada símbolo varía
    con el tiempo como una función lineal por tramos con tres puntos:
    (0, a_i), (m_i, b_i), (T, c_i). Hay que elegir el instante de codificación.

QUÉ HAY QUE HACER
    Entrada: K casos. Cada caso: "n T" y n líneas "a_i m_i b_i c_i".
    Salida:  por caso, "t C" donde t es el menor tiempo entero en [0, T] que
             minimiza C(t) = costo del código óptimo para las frecuencias
             f_i(t), y C con 3 decimales.
    Restricciones clave: K ≤ 1000, n ≤ 100, T ≤ 10^6, 0 < m_i < T,
             0 ≤ a_i, b_i, c_i ≤ 10^6 (enteros).

IDEA Y ALGORITMO
    1) Costo del código óptimo = costo de HUFFMAN: con un montículo se juntan
       repetidamente los dos pesos menores; el costo total Σ f_i·ℓ_i es la
       suma de los pesos de todos los nodos internos creados.
       Con n = 1 la palabra tiene longitud 1 (lo confirma el ejemplo 2:
       f(1) = 1 y la respuesta es 1.000), así que C = f_1.
    2) Observación clave (CONCAVIDAD POR TRAMOS): ordenemos los "puntos de
       quiebre" B = {0, T} ∪ {m_i}. Entre dos quiebres consecutivos TODAS las
       f_i son lineales en t. Para un árbol de código FIJO (longitudes ℓ_i
       fijas) el costo Σ f_i(t)·ℓ_i es entonces lineal en t, y
           C(t) = mín sobre todos los árboles de (función lineal),
       y el mínimo de funciones lineales es CÓNCAVO. Una función cóncava en
       un intervalo alcanza su mínimo en un extremo; y si un punto interior
       empatara con el mínimo, la concavidad obliga a que el extremo izquierdo
       también lo alcance. Por lo tanto el MENOR t que minimiza C (incluso
       entre todos los reales) es un punto de quiebre, y todos los quiebres
       son enteros (0, T y los m_i lo son). Basta evaluar C en ≤ n+2 puntos
       en lugar de en los 10^6+1 enteros de [0, T].
    3) Empates: se evalúa todo con flotantes; los candidatos cuyo costo queda
       a menos de 1e-9 (relativo) del mínimo se re-evalúan de forma EXACTA
       (frecuencias racionales llevadas a un denominador común entero y
       Huffman con enteros) para elegir sin errores de redondeo el menor t.

MACROALGORITMO
    1. Leer K; para cada caso leer n, T y los n cuartetos.
    2. Candidatos = {0, T} ∪ {m_i}, ordenados.
    3. Para cada candidato t, calcular las f_i(t) (tramo izquierdo si t ≤ m_i,
       derecho si no) y el costo de Huffman en flotante.
    4. Quedarse con los candidatos casi empatados con el mínimo; recalcular
       su costo exacto (fracción) y elegir el de menor costo y menor t.
    5. Imprimir "t C" con C redondeado a 3 decimales.

COMPLEJIDAD
    Tiempo O(n · n log n) por caso (n+2 Huffman de n símbolos), memoria O(n).
    Medido en el peor tamaño (K = 1000, n = 100, todos los m_i distintos,
    valores aleatorios): ~5 s en Python (≈5 ms por caso). Si además casi
    todos los candidatos empatan (p. ej. todas las funciones constantes) el
    desempate exacto sube el total a ~15 s: Python puede ser lento ahí.

EJEMPLO A MANO
    Caso 1, t = 0: frecuencias 2, 4, 3 → Huffman: 2+3 = 5, 5+4 = 9 →
    C = 5 + 9 = 14. En los demás quiebres (5, 6, 8, 10) el costo es mayor
    → "0 14.000".

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/E")
    - Fuerza bruta: C(t) EXACTO (fracciones + Huffman) en TODOS los enteros
      t ∈ [0, T] y además en muchos t fraccionarios, con T ≤ 30 y n ≤ 6
      (comprueba también que ningún real no entero da un costo menor):
      OK en 1500 casos aleatorios (con muchos empates: frecuencias pequeñas
      y funciones constantes).
    - Caso grande (K = 1000, n = 100, m_i distintos): ~5 s (ver COMPLEJIDAD).
    - Nota: el enunciado no fija la longitud de palabra con n = 1; el ejemplo
      2 solo cuadra con longitud 1 (C = f_1), que es lo implementado.
"""
import sys
import heapq
from fractions import Fraction
from math import gcd


def huffman(pesos):
    """Costo Σ f_i·ℓ_i del código prefijo óptimo (sirve con float o int)."""
    if len(pesos) == 1:
        return pesos[0]  # un solo símbolo: palabra de longitud 1
    h = list(pesos)
    heapq.heapify(h)
    total = 0
    for _ in range(len(pesos) - 1):
        x = heapq.heappop(h)
        s = x + h[0]              # dos menores
        heapq.heapreplace(h, s)   # el nuevo nodo interno reemplaza al 2.º
        total += s                # cada nodo interno suma su peso al costo
    return total


def frecuencia_exacta(a, m, b, c, T, t):
    """f_i(t) como (numerador, denominador) enteros."""
    if t <= m:
        return a * m + (b - a) * t, m
    return b * (T - m) + (c - b) * (t - m), T - m


def costo_exacto(simbolos, T, t):
    """C(t) exacto: todas las frecuencias a un denominador común D (enteros)
    y Huffman con enteros; el resultado es la fracción costo/D."""
    fr = []
    for a, m, b, c in simbolos:
        num, den = frecuencia_exacta(a, m, b, c, T, t)
        g = gcd(num, den)
        fr.append((num // g, den // g))
    D = 1
    for _, den in fr:
        D = D * den // gcd(D, den)
    return Fraction(huffman([num * (D // den) for num, den in fr]), D)


def resolver(T, simbolos):
    # Puntos de quiebre: el mínimo (y su menor t) está en uno de ellos.
    candidatos = sorted({0, T} | {m for _, m, _, _ in simbolos})

    # Pendientes de cada tramo, precalculadas para evaluar rápido en float.
    izq = [(a, (b - a) / m, m) for a, m, b, c in simbolos]
    der = [(b, (c - b) / (T - m), m) for a, m, b, c in simbolos]

    costos = []
    for t in candidatos:
        f = [a0 + p * t if t <= m else b0 + q * (t - m)
             for (a0, p, m), (b0, q, _) in zip(izq, der)]
        costos.append(huffman(f))

    minimo = min(costos)
    tolerancia = 1e-9 * max(1.0, minimo)
    casi = [t for t, cst in zip(candidatos, costos) if cst - minimo <= tolerancia]

    if len(casi) == 1:
        mejor_t = casi[0]
        mejor_c = costo_exacto(simbolos, T, mejor_t)
    else:
        # Desempate exacto: menor costo y, a igual costo, menor t.
        mejor_t, mejor_c = None, None
        for t in casi:  # casi está en orden creciente de t
            cst = costo_exacto(simbolos, T, t)
            if mejor_c is None or cst < mejor_c:
                mejor_t, mejor_c = t, cst
    return mejor_t, float(mejor_c)


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    casos = int(datos[pos])
    pos += 1
    salida = []
    for _ in range(casos):
        n, T = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        simbolos = []
        for _ in range(n):
            a, m, b, c = (int(v) for v in datos[pos:pos + 4])
            pos += 4
            simbolos.append((a, m, b, c))
        t, costo = resolver(T, simbolos)
        salida.append(f"{t} {costo:.3f}")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
