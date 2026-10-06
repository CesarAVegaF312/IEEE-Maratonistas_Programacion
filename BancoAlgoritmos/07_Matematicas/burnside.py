"""
Matemáticas — Lema de Burnside: collares, pulseras y coloreos bajo simetría («Burnside's lemma»)
Nivel: Avanzado
Ejecutar: python burnside.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Contar objetos «distintos salvo simetría»: dos coloreos se consideran
    iguales si uno se obtiene del otro rotando (o reflejando, girando la
    cuadrícula…). Se cuentan ÓRBITAS de la acción de un grupo de simetrías.
    Cómo reconocerlo: «collares», «pulseras», «se consideran iguales si se
    pueden rotar», «salvo rotaciones/reflexiones», «cuadrículas distintas
    al girarlas»; n grande (10^9) con k colores y módulo primo.

FUNCIÓN
    burnside(n, k, permutaciones) -> int
        Coloreos de n posiciones con k colores, salvo las permutaciones dadas
        (deben formar un grupo: incluir la identidad, cerradas por composición).
    collares(n, k) -> int        coloreos de un ciclo de n cuentas salvo rotación
    pulseras(n, k) -> int        salvo rotación y reflexión (grupo diédrico)
    collares_mod(n, k, p) -> int collares mód p primo (p ∤ n), n hasta ~10^12

IDEA Y ALGORITMO
    Lema de Burnside: #órbitas = (1/|G|) · Σ_{g∈G} |Fix(g)|, donde Fix(g)
    son los coloreos que g deja iguales.
    Prueba: contar los pares (g, x) con g·x = x de dos formas. Por g:
    Σ_g |Fix(g)|. Por x: Σ_x |Stab(x)|. Por órbita–estabilizador,
    |Stab(x)| = |G| / |Órb(x)|, así que cada órbita O aporta
    Σ_{x∈O} |G|/|O| = |G|. Entonces Σ_g |Fix(g)| = |G|·#órbitas.
    Puntos fijos de una permutación g: un coloreo queda igual ⇔ es constante
    en cada CICLO de g, así que |Fix(g)| = k^{ciclos(g)}.
    - Rotación de i posiciones en un ciclo de n: tiene gcd(i, n) ciclos (de
      largo n/gcd). Agrupando por d = n / gcd(i, n), hay φ(d) rotaciones con
      ese d:  collares(n, k) = (1/n) Σ_{d | n} φ(d) · k^{n/d}.
    - Reflexiones (n de ellas): si n es impar, cada una fija 1 cuenta y
      empareja las demás → (n+1)/2 ciclos. Si n es par, n/2 reflexiones por
      dos cuentas opuestas (n/2 + 1 ciclos) y n/2 por puntos medios de
      aristas (n/2 ciclos). pulseras = (n·collares + Σ_refl k^{ciclos}) / (2n).
    La fuerza bruta (generar k^n coloreos y normalizarlos) es exponencial.

MACROALGORITMO
    1. Identificar el grupo G de simetrías (rotaciones, reflexiones, giros
       de la cuadrícula…) y su tamaño.
    2. Para cada g (o cada CLASE de g con igual estructura de ciclos),
       contar sus ciclos sobre las posiciones.
    3. |Fix(g)| = k^{ciclos(g)} (o lo que corresponda si hay restricciones
       sobre el coloreo: contar los coloreos «constantes por ciclo» válidos).
    4. Sumar y dividir por |G| (con módulo: multiplicar por |G|^(-1)).
    5. Para collares con n grande: enumerar divisores d de n y usar φ(d).

COMPLEJIDAD
    burnside genérico: O(|G| · n). collares: O(√n) para divisores y φ +
    O(número de divisores · log n) potencias. pulseras: igual.

EJEMPLO A MANO
    n = 4, k = 2 (collares): rotaciones 0,1,2,3 con gcd 4,1,2,1 ciclos:
    (2^4 + 2^1 + 2^2 + 2^1)/4 = 24/4 = 6:
    0000, 0001, 0011, 0101, 0111, 1111.
    Pulseras n = 4, k = 2: reflexiones: 2 por vértices (3 ciclos) y 2 por
    aristas (2 ciclos): (24 + 2·8 + 2·4)/8 = 48/8 = 6.
    Con n = 6, k = 2: collares 14, pulseras 13 (se juntan 001011 y 001101).

ERRORES TÍPICOS
    - Olvidar la identidad en G o usar un conjunto de simetrías que no es
      grupo (la fórmula deja de valer).
    - Dividir por |G| con / (flotantes) o, con módulo, olvidar el inverso.
    - Contar posiciones fijas en vez de CICLOS de la permutación.
    - En pulseras con n par, tratar todas las reflexiones igual.
    - Con módulo p que divide a |G| (raro) el inverso no existe.

VARIANTES Y RELACIONADOS
    - Teorema de enumeración de Pólya: con pesos por color (contar
      collares con exactamente a cuentas rojas) se usa el índice de ciclos.
    - Collares con cuentas que no se repiten al rotar = palabras de Lyndon:
      L(n,k) = (1/n) Σ_{d|n} μ(d) k^{n/d} (Möbius en vez de φ).
    - Contar cuadrículas n×n salvo rotaciones de 90°: grupo de 4 giros.
    - phi_euler.py (φ), divisores.py, exponenciacion_rapida.py.

DÓNDE PRACTICAR
    - No hay problemas del repo que lo usen directamente (relacionado:
      ICPC/Colombia 2017/D - Rotating Drum genera palabras de Lyndon, que
      son representantes de collares, pero no usa Burnside).
    - CSES «Counting Necklaces» (collares mód 10^9+7), «Counting Grids»
      (cuadrículas salvo rotación)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (generar los k^n coloreos y contar
      formas canónicas mínimas bajo rotación / rotación+reflexión) para
      n ≤ 8, k ≤ 4; cuadrículas 2×2..4×4 con el grupo de giros; versión
      mód p contra la exacta para n ≤ 2000 (python burnside.py)
"""
import itertools
from math import gcd

MOD = 1_000_000_007


def ciclos(perm):
    """Número de ciclos de una permutación dada como lista perm[i] = destino de i."""
    n = len(perm)
    visto = [False] * n
    c = 0
    for i in range(n):
        if not visto[i]:
            c += 1
            j = i
            while not visto[j]:
                visto[j] = True
                j = perm[j]
    return c


def burnside(n, k, permutaciones):
    """Coloreos de n posiciones con k colores salvo el grupo dado (lista de perms)."""
    total = sum(k ** ciclos(g) for g in permutaciones)   # Σ |Fix(g)|
    return total // len(permutaciones)                   # división exacta (lema)


def _divisores_y_phi(n):
    """Lista de (d, φ(d)) para cada divisor d de n (factorización por prueba)."""
    fac = []
    m, q = n, 2
    while q * q <= m:
        if m % q == 0:
            e = 0
            while m % q == 0:
                m //= q
                e += 1
            fac.append((q, e))
        q += 1
    if m > 1:
        fac.append((m, 1))
    res = [(1, 1)]
    for q, e in fac:
        nuevo = []
        for d, ph in res:
            pq = 1
            for j in range(e + 1):
                # φ(q^j) = q^j − q^(j−1) para j ≥ 1; φ es multiplicativa
                nuevo.append((d * pq, ph * (pq - pq // q if j else 1)))
                pq *= q
        res = nuevo
    return res


def collares(n, k):
    """Collares de n cuentas con k colores (salvo rotación)."""
    if n == 0:
        return 1
    return sum(ph * k ** (n // d) for d, ph in _divisores_y_phi(n)) // n


def pulseras(n, k):
    """Pulseras de n cuentas con k colores (salvo rotación y reflexión)."""
    if n == 0:
        return 1
    rot = sum(ph * k ** (n // d) for d, ph in _divisores_y_phi(n))   # Σ Fix de rotaciones
    if n % 2 == 1:
        refl = n * k ** ((n + 1) // 2)
    else:
        refl = (n // 2) * k ** (n // 2 + 1) + (n // 2) * k ** (n // 2)
    return (rot + refl) // (2 * n)


def collares_mod(n, k, p=MOD):
    """Collares mód p (p primo que no divide a n); n hasta ~10^12."""
    s = sum(ph % p * pow(k, n // d, p) for d, ph in _divisores_y_phi(n)) % p
    return s * pow(n, p - 2, p) % p


def giros_cuadricula(m):
    """Grupo de las 4 rotaciones de una cuadrícula m×m como permutaciones de celdas."""
    def rot(perm):  # componer con un giro de 90°: (r, c) -> (c, m-1-r)
        return [perm[(c) * m + (m - 1 - r)] for r in range(m) for c in range(m)]
    g = [list(range(m * m))]
    for _ in range(3):
        g.append(rot(g[-1]))
    return g


def _canon(col, con_reflexion):
    n = len(col)
    rots = [col[i:] + col[:i] for i in range(n)] or [col]
    if con_reflexion:
        inv = col[::-1]
        rots += [inv[i:] + inv[:i] for i in range(n)]
    return min(rots)


def demo():
    print("collares n=4, k=2:", collares(4, 2))      # 6
    print("pulseras n=4, k=2:", pulseras(4, 2))      # 6
    print("collares n=6, k=2:", collares(6, 2), "pulseras:", pulseras(6, 2))  # 14 13
    rot4 = [[(i + s) % 4 for i in range(4)] for s in range(4)]
    print("burnside genérico (rotaciones de 4):", burnside(4, 2, rot4))      # 6
    print("cuadrículas 2x2 con 2 colores salvo giros:", burnside(4, 2, giros_cuadricula(2)))  # 6
    print("collares n=10^9, k=3 mód 1e9+7:", collares_mod(10**9, 3))


def pruebas():
    # Casos borde
    assert collares(1, 5) == 5 and pulseras(1, 5) == 5 and collares(5, 1) == 1
    assert collares(3, 0) == 0 and pulseras(2, 3) == 6

    # Fuerza bruta: formas canónicas
    for n in range(1, 9):
        for k in range(1, 5):
            if k ** n > 70000:
                continue
            todos = [list(c) for c in itertools.product(range(k), repeat=n)]
            assert collares(n, k) == len({tuple(_canon(c, False)) for c in todos})
            assert pulseras(n, k) == len({tuple(_canon(c, True)) for c in todos})
            rot = [[(i + s) % n for i in range(n)] for s in range(n)]
            assert burnside(n, k, rot) == collares(n, k)

    # Cuadrículas m×m salvo giros de 90°
    for m in range(2, 5):
        for k in range(1, 4 if m < 4 else 3):
            g = giros_cuadricula(m)
            canon = set()
            for c in itertools.product(range(k), repeat=m * m):
                canon.add(min(tuple(c[g[t][i]] for i in range(m * m)) for t in range(4)))
            assert burnside(m * m, k, g) == len(canon)

    # Versión modular contra la exacta
    for n in range(1, 2001, 7):
        for k in (2, 3, 10):
            assert collares_mod(n, k) == collares(n, k) % MOD
    # φ: la suma de φ(d) sobre los divisores es n
    for n in range(1, 1000):
        dp = dict(_divisores_y_phi(n))
        assert sum(dp.values()) == n
        assert dp[n] == sum(1 for i in range(1, n + 1) if gcd(i, n) == 1)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
