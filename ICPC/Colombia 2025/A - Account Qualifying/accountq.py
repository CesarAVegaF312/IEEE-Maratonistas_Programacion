"""
Colombia 2025 — A: Account Qualifying («Calificación de cuentas»)
Ejecutar: python accountq.py < accountq.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    El Bank of Linearonia califica las cuentas de sus clientes. Cada cuenta es
    una secuencia de transacciones enteras: positiva = depósito, cero =
    consulta de saldo, negativa = retiro. Hay que calcular tres índices.

QUÉ HAY QUE HACER
    Entrada: varios casos; cada uno es una línea con N y otra con N enteros
             X[0..N-1]. Una línea con un único 0 termina la entrada.
    Salida:  por caso, "d w r" en una línea:
               d = máximo depósito (0 si no hay depósitos),
               w = retiro más negativo (0 si no hay retiros),
               r = longitud del subarreglo CONTIGUO más largo con tantos
                   depósitos como retiros (los ceros no cuentan; r puede ser 0).
    Restricciones clave: N ≤ 10 000, |X[i]| ≤ 10 000.

IDEA Y ALGORITMO
    d y w son un simple máximo/mínimo filtrado.
    Para r se usa la técnica estándar de "sumas prefijas + primera aparición"
    (la misma que para "subarreglo más largo con suma 0"):
      - Se transforma cada transacción en su signo: +1, 0 ó -1.
      - Sea S[i] = suma de los signos de X[0..i-1] (S[0] = 0). El subarreglo
        X[l..r-1] tiene igual número de depósitos que de retiros  <=>  la
        suma de sus signos es 0  <=>  S[r] == S[l].
      - Para maximizar r - l con S[r] == S[l], basta recordar para cada valor
        de la suma prefija el PRIMER índice donde apareció: al llegar a r, el
        mejor l es esa primera aparición (es el l más pequeño posible).
    La fuerza bruta O(N²) (probar todos los subarreglos) son 5·10^7
    operaciones por caso en Python: demasiado; esto es O(N).

MACROALGORITMO
    1. Leer N; si es 0, terminar.
    2. Leer los N enteros.
    3. d = máximo de los positivos (o 0); w = mínimo de los negativos (o 0).
    4. Recorrer la secuencia acumulando la suma de signos; guardar en un
       diccionario la primera posición de cada suma (con suma 0 en posición 0).
    5. En cada posición, si la suma ya se vio, candidato = posición actual −
       primera posición; quedarse con el máximo.
    6. Imprimir "d w r".

COMPLEJIDAD
    Tiempo O(N) por caso, memoria O(N).

EJEMPLO A MANO
    X = 23 -12 0 15 0 5 → signos + - 0 + 0 +
    S = 0, 1, 0, 0, 1, 1, 2 (posiciones 0..6).
    S=1 aparece primero en 1 y de nuevo en 5 → longitud 4 (X[1..4]).
    S=0 aparece en 0 y en 3 → longitud 3. Máximo r = 4.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/A")
    - Fuerza bruta O(N²) sobre todos los subarreglos: OK en 500 casos
      aleatorios pequeños.
    - Caso grande (N = 10 000, 100 casos): ~0.5 s.
"""
import sys


def resolver(x):
    """Devuelve (d, w, r) para la lista de transacciones x."""
    depositos = [v for v in x if v > 0]
    retiros = [v for v in x if v < 0]
    d = max(depositos) if depositos else 0
    w = min(retiros) if retiros else 0  # "el más negativo"

    # primera[s] = primer índice de prefijo donde la suma de signos valió s.
    primera = {0: 0}
    suma = 0
    r = 0
    for i, v in enumerate(x, start=1):
        if v > 0:
            suma += 1
        elif v < 0:
            suma -= 1
        # (v == 0 no cambia la suma: una consulta no afecta los conteos)
        if suma in primera:
            # X[primera[suma] .. i-1] tiene suma de signos 0.
            r = max(r, i - primera[suma])
        else:
            primera[suma] = i
    return d, w, r


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos])
        pos += 1
        if n == 0:  # línea con un único 0: fin de la entrada
            break
        x = [int(t) for t in datos[pos:pos + n]]
        pos += n
        d, w, r = resolver(x)
        salida.append(f"{d} {w} {r}")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
