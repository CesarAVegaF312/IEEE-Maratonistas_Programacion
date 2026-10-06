"""
ACM ICPC Guangzhou Summer Series 2017 — D: Determinant Fun («Diversión con determinantes»)
Ejecutar: python determinantfun.py < determinantfun.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Para cada N se define la matriz N×N  M_N = (m_ij), 0 ≤ i, j < N, con
        m_ij = A·cos((i + Q·j)·x) + B·sin((i + Q·j)·x),   x = K·π / N.
    Se pide la suma de det(I + M_N) para todos los N de un intervalo.

QUÉ HAY QUE HACER
    Entrada: hasta 1000 líneas "Q K A B L R" hasta fin de archivo.
    Salida:  Σ_{N=L..R} det(I + M_N) con 6 decimales.
    Restricciones clave: 1 ≤ K, A, B ≤ 10^9, 1 ≤ L ≤ R ≤ 10^9, |Q| ≤ 1;
    si Q = 0 y K es impar entonces R − L ≤ 300. (Ni siquiera se puede
    recorrer cada N: hace falta una fórmula cerrada para det(I + M_N).)

IDEA Y ALGORITMO
    1) M_N tiene RANGO ≤ 2. Con ω = e^{i·x} y c = (A − iB)/2 se cumple
           A cos θ + B sin θ = c·e^{iθ} + c̄·e^{−iθ},
       y e^{i(i+Qj)x} = ω^i · ω^{Qj}. Por lo tanto
           M = c·a·bᵀ + c̄·ā·b̄ᵀ,   a_i = ω^i,  b_j = ω^{Qj},
       es decir M = U·W con U = [c·a | c̄·ā] (N×2) y W = [bᵀ ; b̄ᵀ] (2×N).
    2) Lema del determinante (Sylvester): det(I_N + U·W) = det(I_2 + W·U).
       Con S_t = Σ_{j=0}^{N−1} ω^{t·j} queda
           det = (1 + c·S_{Q+1})(1 + c̄·S_{−Q−1}) − |c|²·S_{Q−1}·S_{1−Q}.
    3) S_t es una serie geométrica con razón e^{iπKt/N}:
           · si K·t ≡ 0 (mod 2N)              → S_t = N
           · si K·t es par (y no lo anterior) → S_t = 0  (numerador 1 − 1)
           · si K·t es impar                  → S_t = 2 / (1 − e^{iπKt/N})
                                                  = 1 + i·cot(πKt/(2N)).
    4) Casos (|c|² = (A² + B²)/4, 2·Re(c) = A):
         Q =  1: S_0 = N, S_{±2} = N si N | K, si no 0.
                 det = 1 + A·N                 si N | K
                 det = 1 − (A²+B²)·N²/4        si no.
         Q = −1: S_{0} = N en la diagonal, S_{±2} igual que arriba.
                 det = 1 + A·N                 si N | K
                 det = 1 + A·N + (A²+B²)·N²/4  si no.
         Q =  0: det = 1 + 2·Re(c·S_1)  (S_{−1} = conj(S_1)).
                 K par:   det = 1 + A·N si 2N | K, si no 1.
                 K impar: det = 1 + A + B·cot(π·K / (2N))   (R − L ≤ 300).
    5) Sumas sobre [L, R]: los términos "genéricos" son polinomios en N
       (Σ1, ΣN, ΣN² con fórmulas cerradas) y la corrección solo ocurre en
       los divisores de K (o de K/2) que caen en [L, R]: se factoriza K por
       división de prueba con primos ≤ 31623 y se generan sus divisores.
    Todo en los casos Q = ±1 y Q = 0 con K par es racional con denominador
    4, así que se calcula EXACTO con enteros (4·respuesta) y se imprime
    exacto; solo Q = 0 con K impar usa flotantes (cot).
    Nota: los valores pueden ser enormes (~10^44); se imprimen exactos. Un
    juez en C++ con double no podría representarlos, así que en esos casos
    extremos el .out oficial podría diferir en las cifras bajas.

MACROALGORITMO
    1. Criba de primos hasta 31623.
    2. Leer cada línea Q K A B L R.
    3. Q = ±1: 4·suma = Σ_N de la fórmula genérica (fórmulas de Σ1, ΣN, ΣN²)
       + Σ sobre divisores d de K en [L, R] de (valor_divisor − valor_genérico).
    4. Q = 0, K par: 4·suma = 4·(R−L+1) + Σ_{d | K/2, L≤d≤R} 4·A·d.
    5. Q = 0, K impar: sumar 1 + A + B·cot(π·r/(2N)), r = K mod 2N, N = L..R.
    6. Imprimir con 6 decimales (exacto para los casos racionales).

COMPLEJIDAD
    Por caso O(π(√K) + d(K)) ≈ 3400 divisiones + ≤ 1344 divisores, o
    O(R − L) ≤ 301 cotangentes. 1000 casos grandes: ~0.6 s.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/D")
    - Fuerza bruta: OK en 600 casos aleatorios (N ≤ 12, Q ∈ {−1,0,1}, K, A,
      B ≤ 30) contra el determinante calculado numéricamente (eliminación
      gaussiana en flotantes sobre la matriz construida con cos/sin).
"""
import math
import sys


def criba(limite):
    es = bytearray([1]) * (limite + 1)
    es[0] = es[1] = 0
    for i in range(2, int(limite ** 0.5) + 1):
        if es[i]:
            es[i * i::i] = bytearray(len(es[i * i::i]))
    return [i for i in range(limite + 1) if es[i]]


PRIMOS = criba(31623)  # √(10^9) < 31623


def divisores(n):
    """Lista de divisores de n (n ≤ 10^9) por factorización con trial division."""
    factores = []
    for p in PRIMOS:
        if p * p > n:
            break
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            factores.append((p, e))
    if n > 1:
        factores.append((n, 1))
    divs = [1]
    for p, e in factores:
        nuevos = []
        for d in divs:
            q = d
            for _ in range(e + 1):
                nuevos.append(q)
                q *= p
        divs = nuevos
    return divs


def suma_potencias(L, R):
    """(Σ1, ΣN, ΣN²) para N = L..R, exactos."""
    def s1(n):
        return n * (n + 1) // 2

    def s2(n):
        return n * (n + 1) * (2 * n + 1) // 6
    return R - L + 1, s1(R) - s1(L - 1), s2(R) - s2(L - 1)


def formatear_cuartos(x4):
    """Imprime x4/4 exacto con 6 decimales (x4 entero)."""
    signo = "-" if x4 < 0 else ""
    x4 = abs(x4)
    entero, resto = divmod(x4, 4)
    return "%s%d.%06d" % (signo, entero, resto * 250000)


def resolver(Q, K, A, B, L, R):
    if Q == 0 and K % 2 == 1:
        # Único caso con irracionales: det = 1 + A + B·cot(πK/(2N)).
        # cot tiene período π, así que se reduce K módulo 2N en enteros
        # (exacto) antes de pasar a flotante; r es impar ⇒ nunca 0.
        suma_cot = []
        for n in range(L, R + 1):
            r = K % (2 * n)
            suma_cot.append(1.0 / math.tan(math.pi * r / (2 * n)))
        total = (R - L + 1) * (1 + A) + B * math.fsum(suma_cot)
        texto = "%.6f" % total
        return "0.000000" if texto == "-0.000000" else texto

    cuenta, sum_n, sum_n2 = suma_potencias(L, R)
    norma = A * A + B * B  # = 4·|c|²
    if Q == 0:
        # K par: det = 1 salvo cuando 2N | K, que vale 1 + A·N.
        x4 = 4 * cuenta
        for d in divisores(K // 2):
            if L <= d <= R:
                x4 += 4 * A * d
        return formatear_cuartos(x4)

    # Q = ±1: valor genérico (cuando N ∤ K), multiplicado por 4.
    if Q == 1:
        x4 = 4 * cuenta - norma * sum_n2
    else:
        x4 = 4 * cuenta + 4 * A * sum_n + norma * sum_n2
    # Corrección en los divisores de K: ahí det = 1 + A·N.
    for d in divisores(K):
        if L <= d <= R:
            especial = 4 + 4 * A * d
            if Q == 1:
                generico = 4 - norma * d * d
            else:
                generico = 4 + 4 * A * d + norma * d * d
            x4 += especial - generico
    return formatear_cuartos(x4)


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for t in range(0, len(datos) - 5, 6):
        Q, K, A, B, L, R = (int(v) for v in datos[t:t + 6])
        salida.append(resolver(Q, K, A, B, L, R))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
