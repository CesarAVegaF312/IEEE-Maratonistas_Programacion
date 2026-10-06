"""
ACM ICPC Guangzhou Summer Series 2017 — F: Finding Paths («Encontrar caminos»)
Ejecutar: python findingpaths.py < findingpaths.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Caminos en el espacio 3D de (0,0,0) a (n,m,k). Cada paso suma a la
    posición un vector 0/1 no nulo: uno de los 7 vectores (1,1,1), (0,1,1),
    (1,0,1), (1,1,0), (1,0,0), (0,1,0), (0,0,1). Se exige que el camino use
    AL MENOS UNA VEZ un paso "diagonal" (los cuatro primeros, con ≥ 2 unos).

QUÉ HAY QUE HACER
    Entrada: hasta 200 líneas "n m k" hasta fin de archivo.
    Salida:  por línea, el número de caminos módulo 1 000 000 007.
    Restricciones clave: 1 ≤ n, m, k ≤ 1000 (una DP 3D de 10^9 celdas es
    imposible; hace falta una fórmula de O(n+m+k) por caso).

IDEA Y ALGORITMO
    Complemento: respuesta = TOTAL − UNITARIOS, donde
      * UNITARIOS = caminos que solo usan pasos de un eje = coeficiente
        multinomial (n+m+k)! / (n! m! k!).
      * TOTAL = caminos con cualquiera de los 7 pasos.

    Cálculo de TOTAL (combinatoria + inclusión–exclusión):
      Un camino de s pasos es una sucesión de s vectores 0/1. Si se permitiera
      el vector nulo, elegir en qué pasos se avanza en x, en y y en z es
      independiente: g(s) = C(s,n)·C(s,m)·C(s,k) sucesiones.
      Prohibir el vector nulo con inclusión–exclusión (quitar j pasos nulos):
          a(s) = Σ_i (−1)^(s−i) C(s,i) g(i)      (i = pasos no nulos)
      Como cada paso no nulo sube n+m+k en al menos 1, s ≤ S := n+m+k, así
      que TOTAL = Σ_{s=0..S} a(s). Intercambiando las sumas:
          TOTAL = Σ_i g(i) · H(i),   H(i) = Σ_{s=i..S} (−1)^(s−i) C(s,i).
      Calcular cada H(i) directamente costaría O(S²) por caso (demasiado).
      Recurrencia para H: usando Pascal C(s,i) = C(s−1,i) + C(s−1,i−1) y
      reacomodando las sumas telescópicas se obtiene
          2·H(i) = H(i−1) + (−1)^(S−i) · C(S+1, i)
          H(0)   = Σ_{s=0..S} (−1)^s = 1 si S es par, 0 si es impar.
      Así H(0..S) sale en O(S) usando el inverso modular de 2.

MACROALGORITMO
    1. Precalcular factoriales e inversos hasta 3001 (S+1 ≤ 3001).
    2. Para cada caso: S = n+m+k.
    3. H(0) = [S par]; para i = 1..S: H(i) = (H(i−1) + (−1)^(S−i) C(S+1,i)) / 2.
    4. TOTAL = Σ_{i=max(n,m,k)}^{S} C(i,n) C(i,m) C(i,k) H(i)   (mod p).
    5. Restar el multinomial S!/(n! m! k!) e imprimir módulo p.

COMPLEJIDAD
    O(n+m+k) por caso (≤ 3000 pasos), O(3000) memoria. 200 casos con
    n = m = k = 1000: ~0.6 s en Python.

EJEMPLO A MANO
    (1,1,1): S = 3. Los caminos son las particiones ordenadas de {x,y,z} en
    bloques no vacíos (número de Fubini) = 13; los de solo pasos unitarios son
    3! = 6 → 13 − 6 = 7. ✔

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/F")
    - Fuerza bruta: OK en todos los (n,m,k) con 1 ≤ n,m,k ≤ 9 contra una DP
      3D directa con dos tablas (todos los caminos / solo unitarios), además
      de 50 casos aleatorios con coordenadas ≤ 25.
"""
import sys

MOD = 1_000_000_007
MAXF = 3005  # S + 1 ≤ 3001


def preparar_factoriales(limite):
    """fact[i] = i! mod p, inv_fact[i] = (i!)^(-1) mod p."""
    fact = [1] * (limite + 1)
    for i in range(1, limite + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (limite + 1)
    inv_fact[limite] = pow(fact[limite], MOD - 2, MOD)
    for i in range(limite, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD
    return fact, inv_fact


FACT, INV_FACT = preparar_factoriales(MAXF)
INV2 = (MOD + 1) // 2


def comb(a, b):
    """C(a, b) mod p (0 si b está fuera de rango)."""
    if b < 0 or b > a:
        return 0
    return FACT[a] * INV_FACT[b] % MOD * INV_FACT[a - b] % MOD


def resolver(n, m, k):
    s_total = n + m + k

    # H[i] = Σ_{s=i..S} (−1)^(s−i) C(s,i), por la recurrencia
    # 2·H(i) = H(i−1) + (−1)^(S−i)·C(S+1,i).
    h = [0] * (s_total + 1)
    h[0] = 1 if s_total % 2 == 0 else 0
    for i in range(1, s_total + 1):
        termino = comb(s_total + 1, i)
        if (s_total - i) % 2:
            termino = MOD - termino
        h[i] = (h[i - 1] + termino) * INV2 % MOD

    # TOTAL = Σ_i g(i)·H(i) con g(i) = C(i,n)C(i,m)C(i,k); g(i) = 0 si
    # i < max(n, m, k), por eso se empieza ahí.
    total = 0
    for i in range(max(n, m, k), s_total + 1):
        g = comb(i, n) * comb(i, m) % MOD * comb(i, k) % MOD
        total = (total + g * h[i]) % MOD

    # Caminos que solo usan pasos unitarios: multinomial S!/(n! m! k!).
    unitarios = FACT[s_total] * INV_FACT[n] % MOD * INV_FACT[m] % MOD * INV_FACT[k] % MOD
    return (total - unitarios) % MOD


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for t in range(0, len(datos) - 2, 3):
        n, m, k = int(datos[t]), int(datos[t + 1]), int(datos[t + 2])
        salida.append(str(resolver(n, m, k)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
