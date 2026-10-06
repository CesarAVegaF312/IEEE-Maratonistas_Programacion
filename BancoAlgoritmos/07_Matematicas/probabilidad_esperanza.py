"""
Matemáticas — Probabilidad y esperanza: linealidad, DP de probabilidad, Fraction y mód p
Nivel: Intermedio
Ejecutar: python probabilidad_esperanza.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular probabilidades y valores esperados de procesos aleatorios
    discretos sin simular: contando casos favorables / totales, con DP
    sobre estados (probabilidad de llegar a cada estado) o con la
    LINEALIDAD DE LA ESPERANZA (sumar la contribución de cada pieza).
    Cómo reconocerlo: «probabilidad de que…», «valor esperado / número
    esperado de…», «imprima P·Q^(-1) mód 10^9+7», «con 6 decimales»;
    procesos con dados, monedas, permutaciones al azar, caminatas.

FUNCIÓN
    esperanza_valores_distintos(n, k) -> Fraction
        Número esperado de caras distintas al lanzar n dados de k caras.
    esperanza_inversiones(n) -> Fraction      inversiones de una permutación
                                              al azar de n: n(n−1)/4.
    prob_suma_dados(n, k, s) -> Fraction      P(suma de n dados de k caras = s)
    prob_suma_dados_mod(n, k, s, p) -> int    la misma, como P·Q^(-1) mód p
    coleccionista(k) -> Fraction              lanzamientos esperados hasta ver
                                              las k caras (k·H_k)
    a_modulo(fr, p) -> int                    Fraction → num · den^(-1) mód p

IDEA Y ALGORITMO
    - Linealidad: E[X + Y] = E[X] + E[Y] SIEMPRE, aunque X e Y sean
      dependientes (la suma Σ_ω (X+Y)(ω)P(ω) se separa en dos sumas). Truco:
      escribir X como suma de indicadoras X = Σ I_j, y E[I_j] = P(evento j).
      · Caras distintas: I_c = «la cara c sale al menos una vez»;
        P = 1 − ((k−1)/k)^n ⇒ E = k·(1 − ((k−1)/k)^n).
      · Inversiones: un par i<j está invertido con probabilidad 1/2 (por
        simetría, cambiar los valores de i y j es una biyección) ⇒
        E = C(n,2)/2 = n(n−1)/4.
    - DP de probabilidad: dp[i][t] = P(los primeros i dados suman t);
      dp[i+1][t + c] += dp[i][t]/k (ley de probabilidad total: se parte
      según el resultado del dado i+1, que es independiente).
    - Esperanza con «volver a intentar»: E[i] = esperanza de pasos que
      faltan con i caras vistas. Condicionando en el siguiente lanzamiento:
        E[i] = 1 + (i/k)·E[i] + ((k−i)/k)·E[i+1]
      ⇒ E[i] = k/(k−i) + E[i+1] (despejar el término que se repite). Es la
      esperanza de una geométrica (1/prob. de éxito). E[0] = k·H_k.
      Si los estados forman ciclos generales, se resuelve un sistema lineal
      (eliminacion_gaussiana.py).
    - Exacto: fractions.Fraction (Python) no pierde precisión. Mód p: si la
      respuesta es P/Q con p ∤ Q, se imprime P·Q^(p−2) mód p (Fermat); la DP
      se hace igual reemplazando «/k» por «·inv(k)», porque la reducción
      mód p respeta sumas y productos.

MACROALGORITMO
    1. Decidir: ¿contar casos (favorables / total, todos equiprobables)?
       ¿DP sobre estados? ¿linealidad con indicadoras?
    2. Linealidad: partir X en indicadoras simples y sumar sus probabilidades.
    3. DP: estado = lo mínimo que determina el futuro; transición =
       probabilidad total condicionando en el siguiente evento.
    4. Esperanzas: E[estado] = costo + Σ P(siguiente)·E[siguiente]; despejar
       autoreferencias o resolver el sistema.
    5. Representar con Fraction (exacto), float (si piden decimales) o mód p.

COMPLEJIDAD
    prob_suma_dados: O(n² k²) con Fraction (O(n·s·k) en general; con sumas
    prefijas O(n·s)). coleccionista: O(k). Fraction es ~100× más lenta que
    int; para n·s·k ~10^7 usar mód p o float.

EJEMPLO A MANO
    2 dados de 6, suma 7: 6 casos de 36 → 1/6; mód 10^9+7: 6^(-1) = 166666668.
    Caras distintas con n = 2, k = 6: 6·(1 − 25/36) = 11/6.
    Coleccionista k = 3: 3/3 + 3/2 + 3/1 = 11/2 = 5,5 lanzamientos.

ERRORES TÍPICOS
    - Creer que la linealidad exige independencia (no la exige; la
      multiplicatividad E[XY] = E[X]E[Y] sí).
    - Usar floats y comparar con == o acumular error en DP largas.
    - Mód p: dividir con / o //; hay que multiplicar por el inverso.
    - Contar casos que NO son equiprobables (p. ej. sumas de dados como si
      cada suma tuviera la misma probabilidad).
    - DP «hacia adelante» de esperanzas cuando el número de pasos depende
      del azar: suele ser más fácil hacia atrás (desde el estado final).

VARIANTES Y RELACIONADOS
    - conteo_complemento.py (P(bueno) = 1 − P(malo)).
    - eliminacion_gaussiana.py (esperanzas en cadenas de Markov con ciclos).
    - Probabilidad geométrica (áreas/integrales): Colombia 2024 I.
    - Martingalas y teorema de parada opcional: Guangzhou 2017 G.
    - ncr_modular.py (probabilidades = cuentas de binomiales / total).

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/I - Omens (probabilidad geométrica con fórmula cerrada)
    - ICPC/Colombia 2026/K - Sample Median Preservation (favorables/total
      impreso como P·Q^(-1) mód 10^9+7)
    - ICPC/Guangzhou 2017/G - Great Coin Game (esperanza del tiempo de
      parada → sistema lineal de probabilidades)
    - CSES «Dice Probability», «Moving Robots», «Candy Lottery»,
      «Inversion Probability»

VERIFICACIÓN
    - Pruebas: OK contra enumeración de todos los resultados equiprobables
      (itertools.product / permutations) para dados (n ≤ 4, k ≤ 5) y
      permutaciones (n ≤ 7); coleccionista contra la cadena de Markov
      resuelta como sistema lineal con Fraction (k ≤ 8); versión mód p
      contra a_modulo(Fraction) (python probabilidad_esperanza.py)
"""
import itertools
import random
from fractions import Fraction

MOD = 1_000_000_007


def a_modulo(fr, p=MOD):
    """Fraction P/Q → P·Q^(-1) mód p (exige p ∤ Q)."""
    return fr.numerator % p * pow(fr.denominator, p - 2, p) % p


def esperanza_valores_distintos(n, k):
    """E[#caras distintas] en n dados de k caras: k·(1 − ((k−1)/k)^n)."""
    return k * (1 - Fraction(k - 1, k) ** n)


def esperanza_inversiones(n):
    """E[#inversiones] de una permutación uniforme de n: cada par con prob. 1/2."""
    return Fraction(n * (n - 1), 4)


def prob_suma_dados(n, k, s):
    """P(suma de n dados de caras 1..k = s), DP exacta con Fraction."""
    dp = {0: Fraction(1)}                 # dp[t] = P(suma parcial = t)
    for _ in range(n):
        nuevo = {}
        for t, pr in dp.items():
            for c in range(1, k + 1):     # el siguiente dado sale c con prob. 1/k
                nuevo[t + c] = nuevo.get(t + c, 0) + pr / k
        dp = nuevo
    return dp.get(s, Fraction(0))


def prob_suma_dados_mod(n, k, s, p=MOD):
    """La misma probabilidad, como P·Q^(-1) mód p (DP con el inverso de k)."""
    inv_k = pow(k, p - 2, p)
    dp = [1] + [0] * s
    for _ in range(n):
        nuevo = [0] * (s + 1)
        for t in range(s + 1):
            if dp[t]:
                for c in range(1, min(k, s - t) + 1):
                    nuevo[t + c] = (nuevo[t + c] + dp[t] * inv_k) % p
        dp = nuevo
    return dp[s]


def coleccionista(k):
    """Lanzamientos esperados de un dado de k caras hasta ver todas: Σ k/(k−i)."""
    E = Fraction(0)                       # E[k] = 0
    for i in range(k - 1, -1, -1):
        E = Fraction(k, k - i) + E        # E[i] = k/(k−i) + E[i+1]
    return E


def demo():
    print("P(2 dados suman 7) =", prob_suma_dados(2, 6, 7),
          "→ mód p:", prob_suma_dados_mod(2, 6, 7))                      # 1/6, 166666668
    print("E[caras distintas], n=2, k=6:", esperanza_valores_distintos(2, 6))  # 11/6
    print("E[inversiones], n=4:", esperanza_inversiones(4))               # 3
    c = coleccionista(3)
    print("coleccionista k=3:", c, "=", float(c), "| mód p:", a_modulo(c))  # 11/2


def _coleccionista_sistema(k):
    """Fuerza bruta: E[i] = 1 + (i/k)E[i] + ((k−i)/k)E[i+1] como sistema lineal (Gauss)."""
    n = k + 1
    M = [[Fraction(0)] * (n + 1) for _ in range(n)]
    for i in range(n):
        M[i][i] += 1
        if i < k:
            M[i][i] -= Fraction(i, k)
            M[i][i + 1] -= Fraction(k - i, k)
            M[i][n] = Fraction(1)
    for c in range(n):                    # Gauss–Jordan (la matriz es invertible)
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        M[c] = [v / M[c][c] for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return M[0][n]


def pruebas():
    random.seed(2024)

    # Casos borde
    assert prob_suma_dados(0, 6, 0) == 1 and prob_suma_dados(1, 6, 7) == 0
    assert prob_suma_dados_mod(0, 6, 0) == 1
    assert esperanza_valores_distintos(0, 5) == 0
    assert esperanza_inversiones(1) == 0 and coleccionista(1) == 1

    # Dados: enumerar las k^n tiradas equiprobables
    for n in range(0, 5):
        for k in range(1, 6):
            tiradas = list(itertools.product(range(1, k + 1), repeat=n))
            total = len(tiradas)
            distintas = Fraction(sum(len(set(t)) for t in tiradas), total)
            assert esperanza_valores_distintos(n, k) == distintas
            for s in range(0, n * k + 2):
                fav = sum(1 for t in tiradas if sum(t) == s)
                assert prob_suma_dados(n, k, s) == Fraction(fav, total)
                for p in (MOD, 998244353):
                    assert prob_suma_dados_mod(n, k, s, p) == a_modulo(Fraction(fav, total), p)

    # Inversiones: promedio sobre todas las permutaciones
    for n in range(0, 8):
        perms = list(itertools.permutations(range(n)))
        inv = sum(sum(1 for i in range(n) for j in range(i + 1, n) if q[i] > q[j]) for q in perms)
        assert esperanza_inversiones(n) == Fraction(inv, len(perms))

    # Coleccionista contra el sistema lineal de la cadena de Markov
    for k in range(1, 9):
        assert coleccionista(k) == _coleccionista_sistema(k)

    # a_modulo: (P/Q)·Q ≡ P
    for _ in range(300):
        fr = Fraction(random.randint(-10**6, 10**6), random.randint(1, 10**6))
        assert a_modulo(fr) * fr.denominator % MOD == fr.numerator % MOD


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
