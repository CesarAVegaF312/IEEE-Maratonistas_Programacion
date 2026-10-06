"""
Colombia 2024 — H: Only1s0s («Solo unos y ceros»)
Ejecutar: python only1s0s.py < only1s0s.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Alana, investigadora de teoría de números, observa que todo entero
    positivo N tiene un múltiplo M escrito solo con los dígitos 0 y 1
    (un número "only1s0s"). Le interesa el MENOR de ellos.

QUÉ HAY QUE HACER
    Entrada: varios N (0 < N < 10⁵), uno por línea; termina con 0.
    Salida:  por cada N, el entero D tal que N·D es el menor múltiplo
             positivo de N formado solo por dígitos 0 y 1.
    Ojo: D puede tener muchos dígitos (M puede tener decenas de cifras),
    por eso se trabaja con restos y al final con enteros grandes de Python.

IDEA Y ALGORITMO
    BFS (búsqueda en anchura) sobre los RESTOS módulo N.
    Todo número de 0s y 1s se construye dígito a dígito desde la izquierda:
    si el prefijo tiene resto r, agregar el dígito d da resto (10·r + d) % N.
    Dos prefijos con el mismo resto son intercambiables para el futuro
    (lo que se agregue después produce los mismos restos), así que basta
    visitar cada resto UNA vez, quedándose con el prefijo más pequeño.
    Recorrer en anchura empezando por "1" y generando primero el hijo con
    dígito 0 y luego el de dígito 1 visita los números en orden creciente
    (primero por cantidad de dígitos, luego lexicográfico = numérico). Por
    lo tanto el primer prefijo con resto 0 es el mínimo M.
    Como hay a lo sumo N restos, el BFS termina en ≤ N pasos (esto también
    prueba que M existe: palomar sobre los restos).
    Para reconstruir M se guarda, por cada resto, el resto padre y el
    dígito agregado; luego D = M // N con enteros de precisión arbitraria.

    Nota: el texto del enunciado dice "si N = 4, M = 10000 y M/N = 2500",
    pero el menor múltiplo es 100 (D = 25), que es lo que muestra la salida
    de ejemplo. El ejemplo del texto es inconsistente; seguimos la salida.

MACROALGORITMO
    1. Para cada N (con memo por si se repite):
    2. Cola con el resto de "1" (= 1 % N); marcar padre[1 % N] = raíz.
    3. Sacar r de la cola; si r == 0, parar. Si no, para d = 0, 1:
       r' = (10r + d) % N; si r' no visitado, guardar padre y dígito, encolar.
    4. Reconstruir los dígitos de M siguiendo padres desde el resto 0.
    5. Imprimir M // N.

COMPLEJIDAD
    O(N) por caso en tiempo y memoria. Con 202 casos aleatorios
    N < 10⁵ tarda ~2,2 s en Python (≈ 10 ms por caso); los N repetidos de
    un mismo archivo se resuelven una sola vez (memo).

EJEMPLO A MANO
    N = 4: 1→r1; 10→r2, 11→r3; 100→r0 ⇒ M = 100, D = 25.
    N = 13: M = 1001 = 13·77 ⇒ D = 77.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/H")
    - Fuerza bruta: OK para todos los N de 1 a 3000, comparando con la
      enumeración en orden de los números 1, 10, 11, 100, … (binario de
      b = 1, 2, 3, … leído en decimal) hasta encontrar un múltiplo. En 2956
      de ellos coincide exactamente; en los 44 restantes (p. ej. N = 999,
      cuyo M tiene 27 cifras) la fuerza bruta no termina en tiempo
      razonable, y se comprobó que nuestro M es múltiplo, solo tiene 0/1 y
      es mayor que los primeros 65 535 candidatos (todos no múltiplos).
"""
import sys


def menor_multiplo_01(n):
    """Menor M > 0 formado por dígitos 0/1 con M % n == 0."""
    inicio = 1 % n
    padre = [-1] * n          # resto anterior (-2 marca la raíz "1")
    digito = [0] * n          # dígito que se agregó para llegar a este resto
    visitado = [False] * n
    visitado[inicio] = True
    padre[inicio] = -2
    digito[inicio] = 1
    cola = [inicio]
    i = 0
    while i < len(cola):
        r = cola[i]; i += 1
        if r == 0:
            break
        base = (r * 10) % n
        for d in (0, 1):                     # 0 antes que 1: orden numérico
            nr = base + d
            if nr >= n:
                nr -= n
            if not visitado[nr]:
                visitado[nr] = True
                padre[nr] = r
                digito[nr] = d
                cola.append(nr)
    # Reconstrucción de M desde el resto 0 hacia la raíz.
    cifras = []
    r = 0
    while r != -2:
        cifras.append('1' if digito[r] else '0')
        r = padre[r]
    return int("".join(reversed(cifras)))


def main():
    memo = {}
    salida = []
    for tok in sys.stdin.buffer.read().split():
        n = int(tok)
        if n == 0:
            break
        if n not in memo:
            memo[n] = menor_multiplo_01(n) // n
        salida.append(str(memo[n]))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
