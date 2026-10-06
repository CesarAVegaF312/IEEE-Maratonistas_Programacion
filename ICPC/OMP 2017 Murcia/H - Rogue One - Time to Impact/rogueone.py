"""
OMP 2017 Murcia — H: Rogue One: Time to Impact («Rogue One: tiempo hasta el impacto»)
Ejecutar: python rogueone.py < rogueone.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En Scarif, la Estrella de la Muerte ha disparado una bola de fuego hacia
    ti. Un robot tomó dos fotos de la bola: una en t = 0 y otra en t = 10 s, y
    midió su diámetro en píxeles en cada una. No se conoce ni el tamaño real,
    ni la velocidad, ni la distancia de la bola.

QUÉ HAY QUE HACER
    Entrada: número de casos; cada caso "A B" (diámetros en píxeles en t=0 y
    t=10), enteros positivos con B > A.
    Salida:  el tiempo hasta el impacto (desde t = 0) en segundos, TRUNCADO
    a entero (92.99 → 92).
    Restricciones clave: solo enteros positivos; hay que evitar errores de
    redondeo al truncar, así que se calcula con aritmética entera exacta.

IDEA Y ALGORITMO
    Modelo de cámara estenopeica (pinhole) + velocidad constante.
    El tamaño aparente de un objeto es inversamente proporcional a su
    distancia: tamaño = f·D / d (f = focal, D = diámetro real). Entonces
        A = f·D / d0,   B = f·D / d1,   con d1 = d0 - 10·v.
    Dividiendo: A / B = d1 / d0 = 1 - 10·v / d0. Como el tiempo hasta el
    impacto es T = d0 / v (la bola recorre d0 a velocidad v),
        A / B = 1 - 10 / T   ⇒   T = 10·B / (B - A).
    Las incógnitas f, D, d0 y v se cancelan: por eso basta con A y B.
    Como B > A, el denominador es positivo y T > 10. Para truncar sin
    errores de coma flotante se usa división entera: T = (10·B) // (B - A)
    (con ambos positivos, // es exactamente el truncamiento).

MACROALGORITMO
    1. Leer el número de casos.
    2. Para cada par (A, B): imprimir (10·B) // (B - A).

COMPLEJIDAD
    Tiempo O(1) por caso, memoria O(número de casos). 200 000 casos: ~0.25 s.

EJEMPLO A MANO
    10 21 → 210 / 11 = 19.09 → 19.   10 19 → 190 / 9 = 21.1 → 21.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "OMP 2017/H")
    - Fuerza bruta: OK en 2000 casos aleatorios contra una simulación física
      exacta (Fraction): se eligen D, f, d0 al azar, se deduce v para que la
      imagen a los 10 s mida B, y se calcula floor(d0 / v).
"""
import sys


def tiempo_impacto(a, b):
    """T = 10·B / (B - A), truncado; aritmética entera exacta."""
    return (10 * b) // (b - a)


def main():
    datos = sys.stdin.buffer.read().split()
    casos = int(datos[0])
    salida = []
    for k in range(casos):
        a = int(datos[1 + 2 * k])
        b = int(datos[2 + 2 * k])
        salida.append(str(tiempo_impacto(a, b)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
