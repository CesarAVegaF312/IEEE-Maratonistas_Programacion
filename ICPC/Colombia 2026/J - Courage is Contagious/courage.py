"""
Colombia 2026 — J: Courage is Contagious («El valor es contagioso»)
Ejecutar: python courage.py < courage.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    El general Wei Zhan tiene N soldados. El soldado i tiene un umbral de
    valentía k_i: en la siguiente ronda pelea si y solo si en la ronda actual
    pelean al menos k_i soldados en total. Al amanecer pelean c0 soldados y
    el conteo se actualiza ronda tras ronda hasta que deja de cambiar.

QUÉ HAY QUE HACER
    Entrada: varios casos: "N Q", luego los N umbrales k_i y luego Q valores
             c0. Termina con "0 0".
    Salida:  por cada consulta c0, el número de soldados peleando cuando el
             conteo se estabiliza (una línea por consulta).
    Restricciones clave: N, Q <= 10^5 por caso, suma de N y suma de Q
             <= 10^6; 0 <= k_i <= N, 0 <= c0 <= N.

IDEA Y ALGORITMO
    Sea f(c) = #{ i : k_i <= c } (cuántos pelean en la ronda siguiente si
    ahora pelean c). El proceso es iterar c0, f(c0), f(f(c0)), ... hasta un
    PUNTO FIJO f(c) = c. Simular puede costar O(N) rondas por consulta
    (p. ej. umbrales 0,1,2,...,N-1 suben de uno en uno), y con 10^5
    consultas eso es 10^10: demasiado.

    Observación clave: f es MONÓTONA no decreciente (más peleando nunca hace
    que menos se animen). Por eso la sucesión de conteos también es monótona:
      - Si f(c0) >= c0 la sucesión solo SUBE, y se detiene en
            sube[c0] = el menor c >= c0 con f(c) <= c.
        Por qué: sea c* ese valor. Para c0 <= c < c* se cumple f(c) > c (si
        no, c* no sería el menor), así que el conteo sigue subiendo; y nunca
        se pasa de c*, porque si c <= c* entonces f(c) <= f(c*) <= c*. Además
        f(c*) = c* (si c* > c0: f(c*) >= f(c*-1) > c*-1). Es decir, llega a
        c* y ahí se queda.
      - Si f(c0) < c0 la sucesión solo BAJA y, por el argumento espejo, se
        detiene en  baja[c0] = el mayor c <= c0 con f(c) >= c.
    Como c0 solo toma N+1 valores, se precalculan sube[] y baja[] con dos
    barridos lineales y cada consulta se contesta en O(1).
    (sube siempre existe porque f(N) = N; baja siempre existe porque f(0) >= 0.)

MACROALGORITMO
    1. Contar cuántos soldados tienen cada umbral: cnt[v].
    2. f[c] = suma acumulada de cnt (soldados con umbral <= c), c = 0..N.
    3. Barrido de derecha a izquierda: sube[c] = último c' >= c visto con
       f[c'] <= c'.
    4. Barrido de izquierda a derecha: baja[c] = último c' <= c visto con
       f[c'] >= c'.
    5. Respuesta de cada c0: sube[c0] si f[c0] >= c0, si no baja[c0].

COMPLEJIDAD
    Tiempo O(N + Q) por caso, memoria O(N). Caso grande (10 casos con
    N = Q = 10^5, sumas 10^6): ~1.9 s, igual que la versión del usuario.

EJEMPLO A MANO
    N=4, k=[1,2,2,3]: f = [0,1,3,4,4] para c = 0..4.
    c0=2: f(2)=3 >= 2 -> sube[2]: c=2 (3>2 no), c=3 (4>3 no), c=4 (4<=4 sí) -> 4.
    c0=0: f(0)=0 >= 0 -> sube[0] = 0 (f(0) <= 0) -> 0.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/J")
    - Fuerza bruta: OK en 500 entradas aleatorias (16 215 consultas,
      N <= 12) contra la simulación literal ronda por ronda.
    - Coincide con courage.py del usuario en el caso grande.
"""
import sys


def precalcular(n, umbrales):
    """Devuelve (f, sube, baja) para c = 0..n."""
    # cnt[v] = cuántos soldados tienen umbral exactamente v.
    cnt = [0] * (n + 1)
    for k in umbrales:
        cnt[k] += 1

    # f[c] = soldados con umbral <= c (suma acumulada de cnt).
    f = [0] * (n + 1)
    acum = 0
    for c in range(n + 1):
        acum += cnt[c]
        f[c] = acum

    # sube[c] = menor c' >= c con f[c'] <= c'. Se barre de derecha a
    # izquierda recordando el candidato más cercano por la derecha.
    sube = [0] * (n + 1)
    candidato = n                      # f(n) = n siempre cumple
    for c in range(n, -1, -1):
        if f[c] <= c:
            candidato = c
        sube[c] = candidato

    # baja[c] = mayor c' <= c con f[c'] >= c'. Barrido espejo.
    baja = [0] * (n + 1)
    candidato = 0                      # f(0) >= 0 siempre cumple
    for c in range(n + 1):
        if f[c] >= c:
            candidato = c
        baja[c] = candidato
    return f, sube, baja


def main():
    datos = sys.stdin.buffer.read().split()
    idx, salida = 0, []
    while idx + 1 < len(datos):
        n, q = int(datos[idx]), int(datos[idx + 1])
        idx += 2
        if n == 0 and q == 0:                     # fin de la entrada
            break
        umbrales = map(int, datos[idx: idx + n])
        idx += n
        f, sube, baja = precalcular(n, umbrales)
        # Cada consulta en O(1): si el primer paso no baja, la cuenta sube
        # hasta sube[c0]; si baja, baja hasta baja[c0].
        for c0 in map(int, datos[idx: idx + q]):
            salida.append(sube[c0] if f[c0] >= c0 else baja[c0])
        idx += q
    sys.stdout.write("\n".join(map(str, salida)) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
