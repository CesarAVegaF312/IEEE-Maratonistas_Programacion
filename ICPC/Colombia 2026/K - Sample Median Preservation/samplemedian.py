"""
Colombia 2026 — K: Sample Median Preservation («Preservación de la mediana muestral»)
Ejecutar: python samplemedian.py < samplemedian.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un instituto de metrología tiene N mediciones (N impar) cuya mediana es
    el valor de referencia. Para ahorrar cómputo toman una muestra aleatoria
    uniforme de K mediciones sin reemplazo (K impar) y usan su mediana.
    Quieren la probabilidad de que la mediana muestral sea igual a la real.

QUÉ HAY QUE HACER
    Entrada: varios casos: "N K" y luego N enteros A_i. Termina con "0 0".
    Salida:  por caso, la probabilidad P/Q como P · Q^(-1) mod 10^9+7.
    Restricciones clave: 1 <= K <= N <= 10^6, ambos impares; |A_i| <= 10^9
             (puede haber repetidos); suma de N <= 10^6.

IDEA Y ALGORITMO
    Combinatoria (conteo por complemento) + factoriales modulares.

    1) Sea v la mediana real (posición (N+1)/2 del arreglo ordenado),
       menores = #{A_i < v}, mayores = #{A_i > v} y el resto (>= 1 elemento)
       son iguales a v. Sea h = (K-1)/2.
    2) Caracterización: la mediana de la muestra (posición h+1 de la muestra
       ordenada) vale v  <=>  la muestra tiene a lo sumo h elementos < v y a
       lo sumo h elementos > v.
       (=>) si hubiera >= h+1 menores, la posición h+1 sería un menor; igual
       con mayores.  (<=) si hay <= h menores y <= h mayores, las posiciones
       1..h+1 no pueden ser todas menores, ni las posiciones h+1..K todas
       mayores, así que la posición h+1 es un elemento igual a v.
    3) Contar las muestras "malas" es más fácil:
         malo_menor = #muestras con >= h+1 menores
                    = sum_{a=h+1}^{min(menores,K)} C(menores, a) · C(N-menores, K-a)
         malo_mayor = lo mismo con "mayores".
       Los dos eventos son DISJUNTOS: tener >= h+1 menores y >= h+1 mayores
       exigiría 2h+2 = K+1 > K elementos. Por tanto
         buenas = C(N,K) - malo_menor - malo_mayor,
         probabilidad = buenas / C(N,K).
       Todas las muestras son igual de probables, así que contar subconjuntos
       basta (cada subconjunto de K índices es un resultado).
    4) Módulo primo 10^9+7: C(n,r) con factoriales y factoriales inversos
       precalculados; la división es multiplicar por el inverso (Fermat).
       El inverso de C(N,K) existe: como N <= 10^6 < p, el primo p no
       divide a N! y por tanto tampoco a C(N,K). Por eso se puede dividir
       por C(N,K) directamente, sin simplificar antes la fracción (el
       resultado mod p es el mismo que con la fracción irreducible).

    Por qué no lo ingenuo: hay C(N,K) muestras (astronómico). La suma tiene a
    lo sumo (N-1)/2 términos, porque menores, mayores <= (N-1)/2.

MACROALGORITMO
    1. Leer todos los casos y precalcular factoriales hasta el N máximo.
    2. Por caso: ordenar A y tomar v = A[(N+1)/2 - 1].
    3. menores = bisect_left(A, v), mayores = N - bisect_right(A, v).
    4. Calcular malo_menor y malo_mayor con la suma de productos de
       binomiales (h+1 .. min(grupo, K)).
    5. buenas = C(N,K) - malo_menor - malo_mayor (mod p).
    6. Imprimir buenas · C(N,K)^(-1) mod p.

COMPLEJIDAD
    Tiempo O(N log N) por el ordenamiento + O(N) de la suma; memoria O(N).
    Caso grande (un solo caso N = 999 999 con valores aleatorios): ~1.2 s
    con K = 1001, ~1.8 s con K = 499 999 (la suma tiene más términos) y
    ~1.0 s con K = N. La versión del usuario tarda 1.2–2.0 s en los mismos.

EJEMPLO A MANO
    N=5, K=3, A=[1,2,3,4,5]: v=3, menores=2, mayores=2, h=1.
    malo_menor = C(2,2)·C(3,1) = 3; malo_mayor = 3; C(5,3) = 10.
    buenas = 10 - 3 - 3 = 4 -> 4/10 = 2/5 -> 2 · 5^(-1) = 800000006.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/K")
    - Fuerza bruta: OK en 1500 casos aleatorios (N <= 11, valores en rangos
      pequeños para forzar repetidos) contra la enumeración de TODOS los
      subconjuntos de tamaño K con fracciones exactas (Fraction).
    - Coincide con samplemedian.py del usuario en los casos grandes.
"""
import sys
from bisect import bisect_left, bisect_right

MOD = 10**9 + 7


def preparar_factoriales(limite):
    """fact[i] = i! mod p y inv_fact[i] = (i!)^(-1) mod p para i <= limite."""
    fact = [1] * (limite + 1)
    for i in range(1, limite + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (limite + 1)
    inv_fact[limite] = pow(fact[limite], MOD - 2, MOD)   # Fermat
    for i in range(limite, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD
    return fact, inv_fact


def resolver(n, k, valores, fact, inv_fact):
    def comb(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

    def muestras_con_mas_de_h(grupo, h):
        """# de K-subconjuntos con >= h+1 elementos de un grupo de tamaño
        'grupo' (y el resto de los N - grupo elementos de afuera)."""
        afuera = n - grupo
        total = 0
        for a in range(h + 1, min(grupo, k) + 1):
            total += comb(grupo, a) * comb(afuera, k - a)
        return total % MOD

    valores.sort()
    v = valores[(n + 1) // 2 - 1]                # mediana real
    menores = bisect_left(valores, v)            # elementos < v
    mayores = n - bisect_right(valores, v)       # elementos > v
    h = (k - 1) // 2

    total = comb(n, k)
    buenas = (total - muestras_con_mas_de_h(menores, h)
              - muestras_con_mas_de_h(mayores, h)) % MOD
    return buenas * pow(total, MOD - 2, MOD) % MOD


def main():
    datos = sys.stdin.buffer.read().split()
    # Primera pasada: ubicar los casos para saber hasta dónde hay factoriales.
    casos, idx, max_n = [], 0, 1
    while idx + 1 < len(datos):
        n, k = int(datos[idx]), int(datos[idx + 1])
        idx += 2
        if n == 0 and k == 0:                    # fin de la entrada
            break
        casos.append((n, k, idx))
        idx += n
        max_n = max(max_n, n)

    fact, inv_fact = preparar_factoriales(max_n)
    salida = []
    for n, k, ini in casos:
        valores = list(map(int, datos[ini: ini + n]))
        salida.append(resolver(n, k, valores, fact, inv_fact))
    sys.stdout.write("\n".join(map(str, salida)) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
