"""
ACM ICPC Guangzhou Summer Series 2017 — J: Journey through Gridland («Viaje por Gridland»)
Ejecutar: python gridland.py < gridland.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Alice va de (0,0) a (n,m) con pasos este, norte o diagonal noreste, cada
    uno con un costo (u, v, w). Hay que "sumar el costo de todos los caminos
    posibles".

QUÉ HAY QUE HACER
    Entrada: hasta fin de archivo, líneas "n m u v w" (≤ 1000 casos).
    Salida:  por caso, la suma sobre todos los caminos, módulo 10^9+7.
    Restricciones clave: 1 ≤ n, m, u, v, w ≤ 10^6.

    ¡OJO, INCONSISTENCIA DEL ENUNCIADO! El texto dice que el costo de un
    camino es la SUMA de sus pasos, pero con esa lectura el ejemplo daría
    107 (no 25) para "2 3 1 1 1". El ejemplo solo cuadra si el costo de un
    camino es el PRODUCTO de los costos de sus pasos y el paso que se da
    (n - d) veces cuesta v, el que se da (m - d) veces cuesta u (d = número
    de diagonales):
        "2 3 1 1 1": todos los pasos cuestan 1 → respuesta = nº de caminos
                     = D(2,3) = 25  ✓
        "3 2 1 2 3": Σ_d (5-d)!/((3-d)!(2-d)!d!) · 2^(3-d) · 1^(2-d) · 3^d
                     = 10·8 + 12·4·3 + 3·2·9 = 80 + 144 + 54 = 278  ✓
    (Con u en el paso de n − d el segundo daría 139.) Implementamos esa
    lectura, que es la única que reproduce ambos ejemplos de las probadas
    (suma/producto × las dos asignaciones de u, v).

IDEA Y ALGORITMO
    Función generatriz de caminos de Delannoy ponderados.
    * Sea a = costo del paso que avanza en la coordenada de n (a = v),
      b = el de la coordenada de m (b = u) y c = w. La suma de productos
      sobre todos los caminos es el coeficiente
          [x^n y^m]  1 / (1 - a x - b y - c x y),
      porque cada camino es una palabra en los pasos y la serie geométrica
      enumera todas las palabras multiplicando sus pesos.
    * Escribiendo 1 - ax - by - cxy = (1-ax)(1-by) - (ab + c)xy y
      desarrollando en potencias de (ab+c)xy:
          coef = Σ_k C(n,k)·C(m,k)·(ab+c)^k·a^(n-k)·b^(m-k)
               = a^n·b^m·n!·m!·Σ_k s^k · [1/k!^2] · [1/(n-k)!] · [1/(m-k)!]
      con s = (ab + c)/(ab) (mód p; a, b < p así que ab es invertible).
      (Es la generalización de D(n,m) = Σ C(n,k)C(m,k)2^k.)
      Esta suma de k = 0..min(n,m) no tiene forma cerrada conocida, así que
      el costo es O(min(n,m)) por caso (también es lo esperado en C++).
    * Para que Python lo aguante: todos los productos término a término se
      hacen con map(operator.mul) sobre rebanadas de listas precalculadas
      (el bucle corre en C). Las potencias s^k, que cambian en cada caso,
      se parten en bloques: s^k = (s^B)^q · s^r con k = qB + r, de modo que
      cada bloque es un producto punto con la tabla fija s^0..s^(B-1) y
      solo hay un bucle Python por bloque (no por término).

MACROALGORITMO
    1. Leer todos los casos; precalcular hasta max(n,m): factoriales,
       inversos de factoriales (también en orden inverso, para poder tomar
       1/(n-k)! como rebanada creciente) y 1/k!^2.
    2. Por caso: a = v, b = u, c = w; s = (ab + c)·(ab)^(-1) mód p.
    3. X_k = [1/k!^2]·[1/(n-k)!]·[1/(m-k)!] para k = 0..min(n,m) (2 map).
    4. Σ_k s^k X_k por bloques de B = 512 términos.
    5. Multiplicar por a^n · b^m · n! · m! e imprimir mód p.
    6. Memorizar casos repetidos.

COMPLEJIDAD
    Precálculo O(max(n,m)) ≈ 0,5 s para 10^6. Por caso O(min(n,m)) ≈ 0,35 s
    con n = m = 10^6 (memoria O(max(n,m))). PEOR CASO: 1000 casos con
    min(n,m) ≈ 10^6 serían ~6 minutos en Python, MUY por encima de 5 s (en
    C++ el mismo O(Σ min(n,m)) = 10^9 operaciones ya es justo). Ver
    mediciones en VERIFICACIÓN.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/J")
    - Fuerza bruta (DP sobre la cuadrícula: S(i,j) = a·S(i-1,j) +
      b·S(i,j-1) + c·S(i-1,j-1), con la lectura "producto" descrita
      arriba): OK en 2000 casos aleatorios n, m ≤ 30, costos ≤ 10^6, más
      los bordes n = 1 / m = 1.
    - Rendimiento (tiempo total del proceso): 1 caso ~10^6×10^6 ≈ 0,8 s;
      10 casos ≈ 4,5 s; 30 casos ≈ 11 s; 1000 casos aleatorios (n, m, u,
      v, w ≤ 10^6 uniformes) ≈ 125 s → con datos grandes del juez Python
      NO entra en 5 s.
"""
import sys
from operator import mul

MOD = 1_000_000_007
BLOQUE = 512


def precalcular(limite):
    """Factoriales, inversos de factoriales (también al revés) y 1/k!^2."""
    fact = [1] * (limite + 1)
    for i in range(1, limite + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (limite + 1)
    inv_fact[limite] = pow(fact[limite], MOD - 2, MOD)
    for i in range(limite, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD
    inv_fact2 = [x * x % MOD for x in inv_fact]          # 1/(k!)^2
    # inv_rev[i] = inv_fact[limite - i]: inv_fact[a-k] para k = 0,1,2,…
    # queda como la rebanada creciente inv_rev[limite-a : …].
    inv_rev = inv_fact[::-1]
    return fact, inv_fact2, inv_rev


def resolver(n, m, u, v, w, tablas, limite):
    fact, inv_fact2, inv_rev = tablas
    a, b, c = v, u, w          # ver la nota del enunciado en el docstring
    ab = a * b % MOD
    s = (ab + c) * pow(ab, MOD - 2, MOD) % MOD

    K = min(n, m) + 1          # k = 0..min(n,m)
    # X_k = 1/k!^2 · 1/(n-k)! · 1/(m-k)!  (enteros de ~90 bits, sin mód)
    X = list(map(mul, inv_fact2[:K], inv_rev[limite - n: limite - n + K]))
    X = list(map(mul, X, inv_rev[limite - m: limite - m + K]))

    # Tabla de potencias pequeñas s^0..s^(B-1) y paso grande s^B.
    pot_chica = [1] * BLOQUE
    for r in range(1, BLOQUE):
        pot_chica[r] = pot_chica[r - 1] * s % MOD
    paso = pot_chica[-1] * s % MOD

    total = 0
    pot_grande = 1             # (s^B)^q
    for inicio in range(0, K, BLOQUE):
        trozo = X[inicio: inicio + BLOQUE]
        parcial = sum(map(mul, pot_chica, trozo)) % MOD   # Σ_r s^r X_{qB+r}
        total = (total + parcial * pot_grande) % MOD
        pot_grande = pot_grande * paso % MOD

    total = total * fact[n] % MOD * fact[m] % MOD
    total = total * pow(a, n, MOD) % MOD * pow(b, m, MOD) % MOD
    return total


def main():
    datos = sys.stdin.buffer.read().split()
    casos = [tuple(int(x) for x in datos[i:i + 5])
             for i in range(0, len(datos) - 4, 5)]
    if not casos:
        return
    limite = max(max(c[0], c[1]) for c in casos) + 1
    tablas = precalcular(limite)
    memo = {}
    salida = []
    for caso in casos:
        if caso not in memo:
            memo[caso] = resolver(*caso, tablas, limite)
        salida.append(str(memo[caso]))
    sys.stdout.write("\n".join(salida) + "\n")


if __name__ == "__main__":
    main()
