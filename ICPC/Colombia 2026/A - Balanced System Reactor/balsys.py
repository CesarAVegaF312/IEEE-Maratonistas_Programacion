"""
Colombia 2026 — A: Balanced System Reactor («Reactor de sistema balanceado»)
Ejecutar: python balsys.py < balsys.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Una planta tiene n reactores, cada uno con un "factor de potencia" entero
    positivo. El sistema está balanceado si la SUMA de los factores es igual a
    su PRODUCTO. Por seguridad, exactamente n-3 reactores deben tener factor 1,
    así que solo quedan 3 factores "libres" (todos >= 2).

QUÉ HAY QUE HACER
    Entrada: varios casos, un entero n por línea (4 <= n <= 10^7); termina con 0.
    Salida:  por caso, los 3 factores distintos de 1 en orden ascendente
             ("a b c") o "IMPOSSIBLE" si no existen.
    Restricciones clave: n <= 10^7; el número de casos no está acotado.

IDEA Y ALGORITMO
    Sea k = n - 3 (cantidad de unos) y a <= b <= c los tres factores >= 2.
    La condición suma = producto es
            k + a + b + c = a·b·c.
    Truco de factorización (el mismo de "Simon's favorite factoring trick"):
    multiplicando por a y sumando 1 a ambos lados,
            a²bc - ab - ac + 1 = a·k + a² + 1
            (a·b - 1) · (a·c - 1) = a·k + a² + 1  =: M(a)
    Entonces, fijado a, una terna equivale a un DIVISOR d = a·b - 1 de M(a)
    con:
        * d ≡ -1 (mod a)          (para que b = (d+1)/a sea entero; el
                                   cofactor e = M/d cumple automáticamente
                                   e ≡ -1 (mod a) porque M ≡ 1 (mod a)),
        * d >= a² - 1             (⇔ b >= a),
        * d <= e, o sea d² <= M   (⇔ b <= c).
    Por eso basta recorrer d = a²-1, a²-1+a, a²-1+2a, … hasta sqrt(M) y
    quedarse con el primero que divida a M: da el MENOR b para ese a.

    Para a = 2 esto dice: (2b-1)(2c-1) = 2n - 1, es decir, hay solución con
    a = 2 si y solo si 2n - 1 es compuesto (≈ 94 % de los n). Solo cuando
    2n - 1 es primo hay que probar a = 3, 4, …

    Cota de a: f(a,b,c) = abc - a - b - c crece en cada variable (si las
    otras son >= 2), así que el mínimo con c >= b >= a es f(a,a,a) = a³ - 3a;
    si a³ - 3a > k ya no puede haber solución con ese a ni con mayores.
    a <= ~k^(1/3) ≈ 215, y para cada a se prueban ~sqrt(M)/a ≈ sqrt(k/a)
    divisores: en total ≈ 8·10^4 pruebas en el peor caso con n = 10^7.

    AMBIGÜEDAD DEL ENUNCIADO: puede haber VARIAS ternas válidas (p. ej.
    n = 53: "2 2 18", "2 3 11" y "2 4 8") y el enunciado no dice cuál imprimir
    (probablemente el juez usa un verificador que acepta cualquiera). Aquí se
    imprime la lexicográficamente MENOR (a mínimo y, con ese a, b mínimo), que
    es la que sale al recorrer a y b en orden creciente. En los ejemplos del
    enunciado la terna es única, así que no hay conflicto.

MACROALGORITMO
    1. Leer los n hasta encontrar 0.
    2. k = n - 3.
    3. Para a = 2, 3, 4, … mientras a³ - 3a <= k:
         M = a·k + a² + 1;
         buscar el menor d en {a²-1, a²-1+a, …} con d² <= M y M % d == 0;
         si existe → b = (d+1)/a, c = (M/d + 1)/a; responder "a b c".
    4. Si ningún a funcionó → "IMPOSSIBLE".

COMPLEJIDAD
    Por caso: O(Σ_a sqrt(k/a)) ≈ O(n^(2/3)) en el peor caso (cuando no hay
    solución), pero casi siempre termina con a = 2 en O(p) donde p es el menor
    factor de 2n - 1. Memoria O(1).
    Medido (CPython 3.12): 10 000 n aleatorios <= 10^7 en 0.5 s; 2030 casos
    "IMPOSSIBLE" cercanos a 10^7 (el peor caso posible) en 6–10 s (3–5 ms
    c/u). Solo con miles de peores casos Python podría acercarse al límite.

EJEMPLO A MANO
    n = 13 → k = 10, a = 2: M = 2·10 + 4 + 1 = 25; d = 3 no divide, d = 5
    sí (5² <= 25) → b = 3, c = (25/5 + 1)/2 = 3 → "2 3 3"
    (comprobación: 10 + 2 + 3 + 3 = 18 = 2·3·3).
    n = 6 → k = 3, a = 2: M = 11 (primo) → nada; a = 3: 27 - 9 = 18 > 3
    → "IMPOSSIBLE".

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/A")
    - Fuerza bruta (tres bucles a <= b <= c probando suma = producto y
      tomando la primera terna en orden lexicográfico): idéntica para TODO n
      en [4, 3000] y en 300 valores aleatorios de n hasta 10^5.
"""
import sys
from math import isqrt


def resolver(n):
    """Devuelve la terna (a, b, c) lexicográficamente menor, o None."""
    k = n - 3                         # número de reactores con factor 1
    a = 2
    while a * a * a - 3 * a <= k:     # f(a,a,a) <= k: aún puede haber solución
        # (a·b - 1)(a·c - 1) = M: buscar el menor divisor d = a·b - 1 de M
        # con d ≡ -1 (mod a), d >= a² - 1 (b >= a) y d² <= M (b <= c).
        M = a * k + a * a + 1
        d = next((d for d in range(a * a - 1, isqrt(M) + 1, a) if M % d == 0), 0)
        if d:
            return a, (d + 1) // a, (M // d + 1) // a
        a += 1
    return None


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for tok in datos:
        n = int(tok)
        if n == 0:                    # fin de la entrada
            break
        terna = resolver(n)
        salida.append("IMPOSSIBLE" if terna is None else "%d %d %d" % terna)
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
