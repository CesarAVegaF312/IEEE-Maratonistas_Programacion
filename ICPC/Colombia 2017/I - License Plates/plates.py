"""
Colombia 2017 — I: License Plates («Placas de carro»)
Ejecutar: python plates.py < plates.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Antonia y su mamá jugaban con las tres letras de las placas de los carros.
    En la versión nueva, la mamá escribe una palabra S y Antonia debe decir
    cuántas cadenas DISTINTAS de tres letras son subsecuencia de S.

QUÉ HAY QUE HACER
    Entrada: T y luego T líneas, cada una con una palabra S de mayúsculas.
    Salida:  por caso, el número de cadenas distintas xyz (3 letras) que son
             subsecuencia de S.
    Restricciones clave: |S| <= 10^5, alfabeto de 26 letras.

IDEA Y ALGORITMO
    Hay sólo 26^3 = 17576 candidatos xyz; basta decidir rápido si cada uno es
    subsecuencia. Observación (elección VORAZ): xyz es subsecuencia de S si y
    sólo si existe una 'y' estrictamente entre la PRIMERA aparición de x y la
    ÚLTIMA aparición de z. Si hay algún i < j < k con S[i]=x, S[j]=y, S[k]=z,
    se puede mover i a la primera x y k a la última z sin romper el orden.
    Así, con  pri[x] = primera posición de x,  ult[z] = última posición de z
    y  sig = primera 'y' después de pri[x]  (26*26 búsquedas), xyz sirve sii
    sig < ult[z]. Para cada (x, y) se cuentan las z con ult[z] > sig usando
    las 26 últimas posiciones ORDENADAS y búsqueda binaria (bisect).

MACROALGORITMO
    1. Leer T y las palabras.
    2. Para cada palabra: pri[x] con find, ult[z] con rfind (letras presentes).
    3. ultimas = lista ordenada de ult[z].
    4. Para cada x presente y cada letra y: sig = S.find(y, pri[x] + 1);
       si existe, sumar cuántas ult[z] > sig (bisect_right).
    5. Imprimir el total.

COMPLEJIDAD
    Tiempo O(26*26*|S|) en el peor caso por las búsquedas find (hechas en C,
    muy rápidas) + O(26^2 log 26). Medido: 12 palabras de |S| = 10^5
    (aleatorias y adversarias para find) en 0.15 s en total.
    Memoria O(|S|).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/I")
    - Fuerza bruta: OK en 1000 palabras aleatorias (|S| <= 12, alfabetos de
      1 a 5 letras): conjunto de todas las ternas S[i]S[j]S[k] con i<j<k.
"""
import sys
from bisect import bisect_right


def contar(s):
    letras = sorted(set(s))
    primera = {x: s.find(x) for x in letras}
    ultimas = sorted(s.rfind(z) for z in letras)
    total = 0
    for x in letras:
        inicio = primera[x] + 1
        for y in letras:
            sig = s.find(y, inicio)          # primera 'y' después de la primera 'x'
            if sig == -1:
                continue
            # z válidas: las que aparecen por última vez después de 'sig'.
            total += len(ultimas) - bisect_right(ultimas, sig)
    return total


def main():
    datos = sys.stdin.read().split()
    if not datos:
        return
    t = int(datos[0])
    salida = [str(contar(s)) for s in datos[1:1 + t]]
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
