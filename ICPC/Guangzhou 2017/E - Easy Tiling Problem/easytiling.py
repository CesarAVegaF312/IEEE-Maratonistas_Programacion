"""
ACM ICPC Guangzhou Summer Series 2017 — E: Easy Tiling Problem («Un problema fácil de embaldosado»)
Ejecutar: python easytiling.py < easytiling.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Contar de cuántas formas se puede cubrir exactamente un rectángulo N×M
    con T-tetrominós (la pieza en forma de "T" de 4 cuadritos), que se
    pueden rotar y reflejar.

QUÉ HAY QUE HACER
    Entrada: hasta 100 líneas "N M" hasta fin de archivo.
    Salida:  por línea, el número de embaldosados módulo 1 000 000 007.
    Restricciones clave: 4 ≤ N ≤ 24, 4 ≤ M ≤ 10^9, ambos múltiplos de 4.
    Una DP de perfil por columnas tiene ~154 000 estados para N = 24 y M es
    enorme: inviable. Hace falta la estructura de estos embaldosados.

IDEA Y ALGORITMO
    1) Teorema (Walkup 1965; Korn 2004; "On the number of tilings of the
       rectangular board with T-tetrominoes", Australas. J. Combin. 41
       (2008) 107–114): partiendo el tablero en bloques 4×4, todo T-tiling
       se organiza alrededor de los centros de los bloques, y el número de
       embaldosados de un tablero 4n × 4m es
             f(n, m) = 2 · T(L_{n,m}; 3, 3),
       donde L_{n,m} es la grilla de n×m vértices (un vértice por bloque
       4×4) y T es su polinomio de Tutte.
    2) Polinomio de Tutte en (3,3) = modelo de Potts de 4 colores. Por la
       expansión de Fortuin–Kasteleyn, con q = (x−1)(y−1) = 4 y v = y−1 = 2:
             T(G; 3, 3) = Z / (2 · 2^{|V|}),
             Z = Σ_{coloreos σ: V → {4 colores}} Π_{aristas uv} (1 + 2·[σu = σv])
               = Σ_σ 3^{(número de aristas monocromáticas)}.
       Por lo tanto  f(n, m) = Z / 2^{n·m}.
       Comprobación: 4×4 → un vértice: Z = 4, f = 4/2 = 2 ✔.
                     4×8 → una arista: Z = 4·3 + 12·1 = 24, f = 24/4 = 6 ✔.
    3) Z se calcula con MATRIZ DE TRANSFERENCIA por columnas de la grilla
       (n = N/4 ≤ 6 filas, m = M/4 columnas). Un estado sería el coloreo
       de una columna (4^6 = 4096), pero el vector siempre es invariante
       bajo permutar los 4 colores, así que basta guardar un valor por
       PATRÓN (partición de las n filas en ≤ 4 grupos de igual color,
       codificada como "restricted growth string"): 187 patrones para n = 6.
       Transición: valor_nuevo(τ) = 3^{verticales iguales en τ} ·
                   Σ_σ valor(σ) · 3^{#filas con σ_i = τ_i}.
    4) M llega a 10^9 (m ≤ 2.5·10^8): la sucesión Z_m (m = columnas) cumple
       una recurrencia lineal de orden ≤ 187 (Cayley–Hamilton). Se generan
       ~2·187 términos, se obtiene la recurrencia mínima con
       BERLEKAMP–MASSEY (orden real: 1, 2, 4, 10, 26, 76 para n = 1..6) y el
       término m se calcula con KITAMASA: x^(m−1) mod polinomio
       característico por exponenciación binaria. Las multiplicaciones de
       polinomios se hacen con sustitución de Kronecker (empaquetar los
       coeficientes en un entero grande y multiplicar en C).
    5) Respuesta = Z_m · (2^{−1})^{n·m} mod p (la división es exacta en
       los enteros, así que vale con el inverso modular).

MACROALGORITMO
    1. Para cada n = N/4 distinto que aparezca (se cachea):
       a. enumerar los patrones de columna y los 4^n coloreos;
       b. armar la matriz de transferencia entre patrones;
       c. generar Z_1 … Z_T (T = 2·#patrones + 10) iterando la matriz;
       d. Berlekamp–Massey → recurrencia mínima y precomputar las
          reducciones x^{d+j} mod P empaquetadas.
    2. Para cada consulta, m = M/4: si m ≤ T usar Z_m directo; si no,
       Kitamasa para obtener Z_m.
    3. Imprimir Z_m · inv(2)^{n·m} mod 10^9+7.

COMPLEJIDAD
    Preparación para n = 6: 187·4096 sumas para la matriz + 384·187² para
    los términos ≈ 1.5–2 s (una sola vez y solo si aparece N = 24; para
    N ≤ 20 la preparación tarda < 0.1 s). Consulta: O(d² · log m) con d ≤ 76, pero
    con multiplicación de enteros grandes en C: ~10 ms. Medido: 100
    consultas con N al azar entre los 6 valores y M ≈ 10^9: ~2 s en total
    (incluida la preparación de todos los N).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/E")
    - Fuerza bruta independiente: (a) backtracking que enumera todos los
      embaldosados de los tableros 4×4 … 12×12 y 8×12, 12×8; (b) DP de
      perfil por columnas (celda a celda con las 8 orientaciones de la T,
      sin usar el teorema) que generó 80 términos para N ≤ 20 y 200 para
      N = 24 (M hasta 800). La solución coincide en todos (incluye M
      grandes respecto al orden de la recurrencia, así que valida también
      Berlekamp–Massey + Kitamasa).
"""
import sys

MOD = 1_000_000_007
INV2 = (MOD + 1) // 2
ANCHO_BITS = 80          # bits por coeficiente al empaquetar (< 2^80 sobra)
ANCHO_BYTES = ANCHO_BITS // 8


# ---------------------------------------------------------------------------
# Matriz de transferencia del modelo de Potts (4 colores, peso 3 por arista
# monocromática) sobre columnas de n vértices, reducida a patrones.
# ---------------------------------------------------------------------------
def patron(coloreo):
    """Etiquetado canónico (restricted growth string) de un coloreo."""
    etiqueta = {}
    salida = []
    for c in coloreo:
        if c not in etiqueta:
            etiqueta[c] = len(etiqueta)
        salida.append(etiqueta[c])
    return tuple(salida)


def iguales_verticales(col):
    return sum(1 for i in range(len(col) - 1) if col[i] == col[i + 1])


def secuencia_potts(n):
    """Z_1 … Z_T de la grilla n × m (m = 1, 2, …), módulo MOD, con
    T = 2·(número de patrones) + 10: suficiente para Berlekamp–Massey,
    porque el orden de la recurrencia no supera la dimensión de la matriz."""
    # Todos los coloreos de una columna (4^n) y el patrón de cada uno.
    coloreos = [()]
    for _ in range(n):
        coloreos = [c + (x,) for c in coloreos for x in range(4)]
    patrones = sorted(set(patron(c) for c in coloreos))
    indice = {p: i for i, p in enumerate(patrones)}
    idx_de_coloreo = [indice[patron(c)] for c in coloreos]
    k = len(patrones)

    # Cantidad de coloreos con cada patrón = 4·3·…(4 − bloques + 1).
    tamano = []
    for p in patrones:
        bloques = max(p) + 1
        t = 1
        for i in range(bloques):
            t *= 4 - i
        tamano.append(t)

    pot3 = [3 ** e for e in range(n + 1)]
    # matriz[Q][P] = 3^{v(τ_Q)} · Σ_{σ con patrón P} 3^{coincidencias(σ, τ_Q)}
    # (τ_Q = representante canónico del patrón Q, que también es un coloreo).
    matriz = []
    for q in patrones:
        fila = [0] * k
        for col, ip in zip(coloreos, idx_de_coloreo):
            coincide = 0
            for a, b in zip(col, q):
                if a == b:
                    coincide += 1
            fila[ip] += pot3[coincide]
        peso = pot3[iguales_verticales(q)]
        matriz.append([x * peso % MOD for x in fila])

    terminos = 2 * k + 10
    # Primera columna: solo las aristas verticales.
    vec = [pot3[iguales_verticales(p)] for p in patrones]
    seq = []
    for _ in range(terminos):
        seq.append(sum(map(int.__mul__, tamano, vec)) % MOD)
        vec = [sum(map(int.__mul__, fila, vec)) % MOD for fila in matriz]
    return seq


# ---------------------------------------------------------------------------
# Berlekamp–Massey y Kitamasa con multiplicación de polinomios por Kronecker.
# ---------------------------------------------------------------------------
def berlekamp_massey(s):
    """Devuelve c[1..L] con s[i] = Σ c[j]·s[i−j] (mod MOD) para i ≥ L."""
    C, B = [1], [1]
    L, m, b = 0, 1, 1
    for i in range(len(s)):
        d = s[i]
        for j in range(1, L + 1):
            d = (d + C[j] * s[i - j]) % MOD
        if d == 0:
            m += 1
            continue
        T = C[:]
        coef = d * pow(b, MOD - 2, MOD) % MOD
        if len(C) < len(B) + m:
            C += [0] * (len(B) + m - len(C))
        for j in range(len(B)):
            C[j + m] = (C[j + m] - coef * B[j]) % MOD
        if 2 * L <= i:
            L, B, b, m = i + 1 - L, T, d, 1
        else:
            m += 1
    return [(-x) % MOD for x in C[1:L + 1]]


def empaquetar(coefs):
    """Polinomio (lista de coeficientes) → entero grande, 80 bits por casilla."""
    return int.from_bytes(b"".join(c.to_bytes(ANCHO_BYTES, "little") for c in coefs), "little")


def desempaquetar(x, cuantos):
    datos = x.to_bytes(cuantos * ANCHO_BYTES, "little")
    return [int.from_bytes(datos[i:i + ANCHO_BYTES], "little")
            for i in range(0, cuantos * ANCHO_BYTES, ANCHO_BYTES)]


class Recurrencia:
    """Calcula términos lejanos de s con s[i] = Σ c[j]·s[i−j] (Kitamasa)."""

    def __init__(self, seq, c):
        self.seq = seq
        self.c = c
        self.d = d = len(c)
        # reduccion[j] = x^{d+j} mod P(x), j = 0..d−2, empaquetado.
        # P(x) = x^d − Σ c[j]·x^{d−j}  ⇒  x^d ≡ Σ c[j]·x^{d−j}.
        actual = [c[d - 1 - i] for i in range(d)]      # x^d mod P
        self.reduccion = []
        for _ in range(max(d - 1, 0)):
            self.reduccion.append(empaquetar(actual))
            # multiplicar por x y reducir el término x^d
            alto = actual[-1]
            actual = [0] + actual[:-1]
            if alto:
                actual = [(a + alto * c[d - 1 - i]) % MOD for i, a in enumerate(actual)]

    def mulmod(self, a, b):
        """(a·b) mod P con a, b de grado < d."""
        d = self.d
        prod = desempaquetar(empaquetar(a) * empaquetar(b), 2 * d)
        prod = [x % MOD for x in prod]
        # Parte baja + Σ coef_alto[j] · (x^{d+j} mod P), todo en enteros grandes.
        acumulado = empaquetar(prod[:d])
        for j in range(d - 1):
            if prod[d + j]:
                acumulado += prod[d + j] * self.reduccion[j]
        return [x % MOD for x in desempaquetar(acumulado, d)]

    def termino(self, idx):
        """seq[idx] (índice desde 0), aunque idx sea enorme."""
        if idx < len(self.seq):
            return self.seq[idx]
        d = self.d
        if d == 1:
            # s[i] = c·s[i−1]  ⇒  s[idx] = s[0]·c^idx (caso N = 4: 2·3^(m−1)).
            return self.seq[0] * pow(self.c[0], idx, MOD) % MOD
        # Potencia binaria x^idx mod P(x), partiendo del polinomio x.
        resultado = [1] + [0] * (d - 1)
        base = [0, 1] + [0] * (d - 2)
        e = idx
        while e:
            if e & 1:
                resultado = self.mulmod(resultado, base)
            e >>= 1
            if e:
                base = self.mulmod(base, base)
        # s[idx] = Σ r_i · s[i]
        return sum(r * s for r, s in zip(resultado, self.seq)) % MOD


CACHE = {}


def preparar(n):
    if n not in CACHE:
        seq = secuencia_potts(n)
        CACHE[n] = Recurrencia(seq, berlekamp_massey(seq))
    return CACHE[n]


def resolver(N, M):
    n, m = N // 4, M // 4
    z = preparar(n).termino(m - 1)       # Z_m (seq[0] = Z_1)
    return z * pow(INV2, n * m, MOD) % MOD


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for t in range(0, len(datos) - 1, 2):
        salida.append(str(resolver(int(datos[t]), int(datos[t + 1]))))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
