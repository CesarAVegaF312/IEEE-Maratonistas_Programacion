"""
Colombia 2023 — E: LISP Extravaganza («Extravagancia LISP»)
Ejecutar: python extravaganza.py < extravaganza.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En LISP todo se escribe con paréntesis. Dada una cadena de '(' y ')',
    se pide la longitud de la subsecuencia balanceada más larga (no tiene que
    ser contigua).

QUÉ HAY QUE HACER
    Entrada: primera línea m (número de casos); luego m líneas "n s" con
             1 ≤ n ≤ 50 000 y s formada solo por paréntesis.
    Salida:  por caso, la longitud de la subsecuencia balanceada más larga.

IDEA Y ALGORITMO
    Emparejamiento voraz con contador (equivalente a una pila de '(').
    Se recorre s de izquierda a derecha contando los '(' abiertos aún sin
    pareja. Cada ')' que encuentra un '(' abierto forma una pareja (+2);
    un ')' sin '(' disponible se descarta.
    Por qué es óptimo: una subsecuencia balanceada es un emparejamiento de
    '(' con ')' posteriores sin cruces "inválidos"; el número máximo de
    parejas posibles es exactamente el que logra el voraz, porque emparejar
    un ')' en cuanto se puede nunca impide parejas futuras (cualquier '('
    abierto sirve igual para un ')' posterior). El conjunto de caracteres
    emparejados, en su orden original, siempre es balanceado.

MACROALGORITMO
    1. Leer m y, para cada caso, la cadena s.
    2. abiertos = 0, parejas = 0.
    3. Para cada c en s: si '(' -> abiertos += 1; si ')' y abiertos > 0 ->
       abiertos -= 1, parejas += 1.
    4. Imprimir 2 * parejas.

COMPLEJIDAD
    O(n) por caso, memoria O(n) para la lectura.

EJEMPLO A MANO
    "())()": ( abre; ) pareja 1; ) se descarta; ( abre; ) pareja 2 -> 4.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2023/E")
    - Fuerza bruta: probando todas las subsecuencias (2^n) de cadenas con
      n ≤ 12, 500 casos aleatorios: OK.
    - Rendimiento: 20 casos con n = 50 000: ≈ 0,12 s.
"""
import sys


def mas_larga_balanceada(s):
    abiertos = 0   # '(' leídos que aún no tienen ')' asignado
    parejas = 0    # parejas '(' ')' formadas
    for c in s:
        if c == "(":
            abiertos += 1
        elif abiertos > 0:
            abiertos -= 1
            parejas += 1
    return 2 * parejas


def main():
    datos = sys.stdin.read().split()
    if not datos:
        return
    m = int(datos[0])
    salida = []
    pos = 1
    for _ in range(m):
        # cada caso: n y s (s nunca es vacía porque n ≥ 1)
        s = datos[pos + 1]
        pos += 2
        salida.append(str(mas_larga_balanceada(s)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
