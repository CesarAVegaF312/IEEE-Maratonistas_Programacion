"""
ACM ICPC Guangzhou Summer Series 2017 — G: Great Coin Game («El gran juego de la moneda»)
Ejecutar: python greatcoingame.py < greatcoingame.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Cada uno de n estudiantes escribe una cadena distinta de longitud m de
    'H' (cara) y 'T' (cruz). Se lanza una moneda justa hasta que los
    últimos m lanzamientos coinciden con alguna cadena; su dueño gana.
    (Es el "juego de Penney" generalizado a n jugadores.)

QUÉ HAY QUE HACER
    Entrada: hasta fin de archivo, casos (≤ 100) con "n m" y n cadenas.
    Salida:  la probabilidad de ganar de cada estudiante, una por línea,
             con 6 decimales.
    Restricciones clave: 1 ≤ n, m ≤ 300.

IDEA Y ALGORITMO
    Método de Conway / martingala del "apostador" + eliminación gaussiana.
    * Correlación: para cadenas a, b de longitud m definimos
          a:b = Σ_{k=1..m} [sufijo de a de largo k == prefijo de b de largo k]·2^k.
    * Argumento de martingala (Li 1980, Guibas–Odlyzko): antes de cada
      lanzamiento llega un apostador nuevo que apuesta 1 a que salen, en
      orden, las letras de la cadena b (doblando lo ganado mientras acierta).
      El juego es justo, así que la ganancia esperada al parar es 0. Al
      parar (en el tiempo T, cuando aparece la cadena a ganadora), los
      apostadores vivos son exactamente los que empezaron en un sufijo de a
      que es prefijo de b, y su dinero suma a:b. Por el teorema de parada
      opcional:  E[T] = Σ_a P(gana a) · (a:b)   para TODA cadena b.
    * Esto da n ecuaciones lineales con incógnitas p_1..p_n y E = E[T],
      más Σ p_a = 1: un sistema (n+1)×(n+1) con solución única.
      Dividimos todo por 2^m (pesos 2^(k-m) ∈ (0,1]) para trabajar con
      números moderados en punto flotante.
    * Cálculo rápido de las correlaciones (n^2 pares × m largos sería
      2,7·10^7 comparaciones de cadenas): ordenamos las cadenas; las que
      comparten un prefijo de largo k forman un BLOQUE CONTIGUO en el orden.
      Para cada a y cada k buscamos (diccionario) el bloque cuyo prefijo es
      el sufijo de a de largo k y le sumamos 2^(k-m) a todo el bloque con un
      arreglo de diferencias. Costo O(n·m) búsquedas + O(n^2).
    * Sistema lineal: eliminación de Gauss con pivoteo parcial; las filas
      se actualizan con comprensiones de listas (mucho más rápido que
      bucles índice a índice).

MACROALGORITMO
    1. Leer n, m y las cadenas de cada caso.
    2. Ordenar las cadenas; para cada largo k, diccionario prefijo → bloque
       [lo, hi] de posiciones en el orden.
    3. Para cada cadena a: recorrer k = 1..m, acumular 2^(k-m) en el
       bloque del sufijo de largo k (arreglo de diferencias) → fila de
       correlaciones a:b para todas las b.
    4. Armar el sistema: para cada b, Σ_a corr(a,b)·p_a - E' = 0; y Σ p_a = 1.
    5. Resolver con Gauss + pivoteo parcial.
    6. Imprimir p_a con 6 decimales en el orden de entrada.

COMPLEJIDAD
    Tiempo O(n·m + n^3) por caso, memoria O(n^2). Un caso n = m = 300 tarda
    ≈ 0,85 s en Python (3 casos máximos ≈ 2,3 s); el peor caso teórico (100
    casos máximos) serían ~75 s, por encima del límite de 5 s del juez.

EJEMPLO A MANO
    THT, TTH, HTT (m=3, pesos 2^(k-3) = 1/4, 1/2, 1 para k = 1, 2, 3):
    corr(THT,THT) = 1 + 1/4 (sufijo "T" = prefijo "T") = 5/4, etc. El
    sistema da p = (1/3, 1/4, 5/12) = 0.333333 0.250000 0.416667.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/G")
    - Fuerza bruta (cadena de Markov sobre los últimos m-1 lanzamientos,
      iterando la distribución hasta que la masa no absorbida < 1e-13, sin
      usar correlaciones): OK en 500 casos aleatorios con m ≤ 7 (diferencia
      máxima 5e-7 = solo el redondeo a 6 decimales de la salida).
    - Estabilidad numérica: el sistema en flotantes contra el mismo sistema
      resuelto con fracciones exactas (n = 30, m = 40, incluidas cadenas con
      largos bloques de H compartidos): error máximo 2e-17.
"""
import sys


def correlaciones(cadenas, m):
    """corr[a][b] = Σ_k [suf_k(a) == pre_k(b)]·2^(k-m)."""
    n = len(cadenas)
    orden = sorted(range(n), key=lambda i: cadenas[i])
    ordenadas = [cadenas[i] for i in orden]

    # bloques[k][prefijo] = (lo, hi): posiciones (en el orden) con ese prefijo.
    bloques = [None] * (m + 1)
    for k in range(1, m + 1):
        d = {}
        for pos, s in enumerate(ordenadas):
            p = s[:k]
            if p in d:
                d[p][1] = pos          # los iguales son contiguos al estar ordenados
            else:
                d[p] = [pos, pos]
        bloques[k] = d

    pesos = [2.0 ** (k - m) for k in range(m + 1)]
    corr = [None] * n
    for a in range(n):
        s = cadenas[a]
        dif = [0.0] * (n + 1)
        for k in range(1, m + 1):
            bloque = bloques[k].get(s[m - k:])
            if bloque is not None:
                dif[bloque[0]] += pesos[k]
                dif[bloque[1] + 1] -= pesos[k]
        # Suma prefija → valor por posición en el orden; devolver al índice original.
        fila = [0.0] * n
        acum = 0.0
        for pos in range(n):
            acum += dif[pos]
            fila[orden[pos]] = acum
        corr[a] = fila
    return corr


def resolver_sistema(M):
    """Gauss con pivoteo parcial sobre la matriz aumentada M (lista de filas)."""
    N = len(M)
    for c in range(N):
        piv = max(range(c, N), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        fila_p = M[c]
        inv = 1.0 / fila_p[c]
        fila_p = [x * inv for x in fila_p]
        M[c] = fila_p
        cola_p = fila_p[c:]
        for r in range(c + 1, N):
            f = M[r][c]
            if f != 0.0:
                fila = M[r]
                fila[c:] = [x - f * y for x, y in zip(fila[c:], cola_p)]
    # Sustitución hacia atrás (la diagonal ya es 1).
    x = [0.0] * N
    for r in range(N - 1, -1, -1):
        fila = M[r]
        x[r] = fila[N] - sum(fila[k] * x[k] for k in range(r + 1, N))
    return x


def resolver(cadenas, m):
    n = len(cadenas)
    corr = correlaciones(cadenas, m)
    # Incógnitas: p_0..p_{n-1}, E' (= E[T]/2^m). Columna n+1: término independiente.
    M = []
    for b in range(n):
        # Σ_a corr[a][b]·p_a - E' = 0
        M.append([corr[a][b] for a in range(n)] + [-1.0, 0.0])
    M.append([1.0] * n + [0.0, 1.0])       # Σ p_a = 1
    sol = resolver_sistema(M)
    return sol[:n]


def main():
    datos = sys.stdin.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        n, m = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        cadenas = datos[pos:pos + n]
        pos += n
        for p in resolver(cadenas, m):
            # max(…, 0.0) evita imprimir "-0.000000" por error de redondeo.
            salida.append("%.6f" % max(p, 0.0))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
