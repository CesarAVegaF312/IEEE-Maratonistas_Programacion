"""
Colombia 2024 — B: The Bridge at Night («El puente de noche»)
Ejecutar: python bridge.py < bridge.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un grupo quiere cruzar de noche un puente colgante: pasan como máximo dos
    personas a la vez, hay una sola lámpara (alguien debe devolverla) y una
    pareja camina al ritmo del más lento. Es el clásico "bridge and torch".

QUÉ HAY QUE HACER
    Entrada: varios casos; cada uno con N (1 ≤ N ≤ 30) y luego N tiempos
             t (1 ≤ t ≤ 20), uno por línea. Termina con N = 0.
    Salida:  por caso, el tiempo mínimo para que todos crucen.

IDEA Y ALGORITMO
    Algoritmo voraz clásico (demostrado óptimo, Rote 2002) sobre los
    tiempos ordenados t1 ≤ t2 ≤ … ≤ tn. Mientras queden más de 3 personas
    en el lado inicial, hay que llevar a las DOS más lentas (t_{n-1}, t_n)
    al otro lado y dejar la lámpara de vuelta; hay dos estrategias:
      (a) Los dos más rápidos como "escoltas":
          1 y 2 cruzan (t2), 1 vuelve (t1), n-1 y n cruzan (tn), 2 vuelve (t2)
          costo = t1 + 2·t2 + tn
      (b) El más rápido escolta a cada uno:
          1 y n cruzan (tn), 1 vuelve (t1), 1 y n-1 cruzan (t_{n-1}), 1 vuelve
          costo = 2·t1 + t_{n-1} + tn
    Se toma el mínimo y el problema se reduce a n-2 personas (las dos más
    rápidas siguen en el lado inicial con la lámpara). Casos base:
      n = 1 → t1;  n = 2 → t2;  n = 3 → t1 + t2 + t3.
    Por qué funciona: en una solución óptima los dos más lentos o bien
    cruzan juntos (mejor acompañados por los escoltas rápidos, estrategia
    a) o cada uno con el más rápido (estrategia b); un argumento de
    intercambio muestra que ninguna otra combinación es mejor.

MACROALGORITMO
    1. Leer N y los N tiempos; ordenarlos.
    2. Mientras n > 3: sumar min(estrategia a, estrategia b) y quitar los
       dos más lentos (n -= 2).
    3. Sumar el caso base según n ∈ {1, 2, 3}.
    4. Imprimir el total.

COMPLEJIDAD
    O(N log N) por caso (el orden); memoria O(N). Instantáneo.

EJEMPLO A MANO
    Tiempos 1, 2, 5: n = 3 → 1 + 2 + 5 = 8 (coincide con el enunciado).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/B")
    - Fuerza bruta: OK en 600 casos aleatorios (N ≤ 7, t ≤ 20) contra un
      Dijkstra sobre todos los estados (subconjunto en la orilla final,
      lado de la lámpara) con todos los movimientos de 1 o 2 personas.
"""
import sys


def tiempo_minimo(tiempos):
    """Tiempo mínimo para que todos crucen (algoritmo voraz clásico)."""
    t = sorted(tiempos)
    n = len(t)
    total = 0
    # Invariante: las personas t[0..n-1] siguen en la orilla inicial con la lámpara.
    while n > 3:
        escoltas = t[0] + 2 * t[1] + t[n - 1]          # estrategia (a)
        uno_a_uno = 2 * t[0] + t[n - 2] + t[n - 1]     # estrategia (b)
        total += min(escoltas, uno_a_uno)
        n -= 2
    if n == 3:
        total += t[0] + t[1] + t[2]
    elif n == 2:
        total += t[1]
    else:
        total += t[0]
    return total


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos]); pos += 1
        if n == 0:
            break
        tiempos = [int(x) for x in datos[pos:pos + n]]
        pos += n
        salida.append(str(tiempo_minimo(tiempos)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
