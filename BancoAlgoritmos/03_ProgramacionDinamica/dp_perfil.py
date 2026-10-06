"""
Programación dinámica — DP de perfil / perfil roto («Broken profile DP»)
Nivel: Avanzado
Ejecutar: python dp_perfil.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Contar formas de llenar una grilla n×m (con m pequeño, m ≤ ~10–12) con
    piezas que se tocan solo entre celdas vecinas: el clásico es contar los
    embaldosados con dominós 1×2 (horizontales o verticales), con o sin
    celdas bloqueadas. El estado guarda solo la «frontera» entre la parte
    ya decidida y la que falta, como una máscara de m bits.
    Señales: «grilla n×m con m ≤ 10» (n puede ser grande), «de cuántas
    formas cubrir / pintar / colocar», restricciones solo entre vecinos.

FUNCIÓN
    contar_dominos(n, m, bloqueadas=(), mod=None) -> int
        Número de formas de cubrir todas las celdas libres de la grilla n×m
        con dominós sin superponerlos; bloqueadas = conjunto de (fila, col)
        que no se cubren.

IDEA Y ALGORITMO
    Se recorren las celdas en orden fila por fila, izquierda a derecha.
    Antes de decidir la celda (i, j), la frontera son las m celdas
    (i, j), (i, j+1), …, (i, m-1), (i+1, 0), …, (i+1, j-1): exactamente una
    por columna. El bit c de la máscara dice si la celda de la frontera en
    la columna c YA está cubierta por un dominó que sobresale de lo decidido.
      ESTADO      dp[mask] = número de formas de colocar dominós en todas
                  las celdas anteriores a (i, j) dejando la frontera `mask`.
      TRANSICIÓN  en la celda (i, j), con b = bit j:
                  - si b = 1: ya está cubierta; queda libre la celda de
                    abajo -> bit j = 0.
                  - si b = 0 (hay que cubrirla ahora):
                    vertical (con (i+1, j)): bit j = 1 (sobresale abajo);
                    horizontal (con (i, j+1)), si el bit j+1 es 0: bit j = 0
                    y bit j+1 = 1.
                  - celda bloqueada: debe tener b = 0 y queda b = 0.
      CASO BASE   antes de la primera celda: dp[0] = 1.
      ORDEN       celda por celda (i, luego j), una capa de 2^m por celda.
      RESPUESTA   dp[0] tras la última celda (nada sobresale de la grilla).
    Se llama «perfil roto» porque la frontera tiene un escalón en j; avanzar
    de a una celda hace que cada transición sea O(1) en vez de enumerar
    todas las formas de llenar una fila entera (O(4^m) o peor).
    Si m > n se transpone la grilla (2^min(n, m)).

MACROALGORITMO
    1. Transponer si m > n; marcar las bloqueadas.
    2. dp = [0]*2^m; dp[0] = 1.
    3. Para cada celda (i, j): nuevo = [0]*2^m; para cada mask con dp > 0
       aplicar las transiciones (respetando bordes y bloqueadas); dp = nuevo.
    4. Respuesta dp[0].

COMPLEJIDAD
    O(n · m · 2^m) tiempo, O(2^m) memoria. En Python, n·m·2^m ≤ ~3·10^6 en
    ~1–2 s (p. ej. 10×10: 10^5; 12×12: 6·10^5; 20×10: 2·10^5).
    Para n gigante (10^18) con m fijo: matriz de transferencia y potencia.

EJEMPLO A MANO
    2×2 (m = 2):  celda (0,0) mask 00 -> vertical: 01, horizontal: 10.
                  celda (0,1) mask 01 -> bit1 = 0: vertical -> 11 (horizontal
                  no: no hay columna 2); mask 10 -> bit1 = 1: pasa a 00.
                  celda (1,0) mask 11 -> 10; mask 00 -> horizontal -> 10.
                  celda (1,1) mask 10 (2 formas) -> 00.   Respuesta 2.
    Valores conocidos: 2×n = Fibonacci, 3×4 = 11, 8×8 = 12 988 816.

ERRORES TÍPICOS
    - Confundir qué celda representa cada bit (antes y después de j).
    - Permitir un vertical en la última fila o un horizontal en la última
      columna (sobresale de la grilla).
    - Olvidar que horizontal exige que (i, j+1) NO esté ya cubierta.
    - Grillas con n·m impar: 0 (sale solo, pero sirve de prueba).
    - No transponer cuando m es el lado grande: 2^m explota.

VARIANTES Y RELACIONADOS
    - Fichas de otras formas (L, tetraminós), pintar sin vecinos iguales
      (máscara con más estados por columna), caminos/ciclos en grilla
      (perfil con etiquetas de componentes, «plug DP»).
    - dp_mascaras.py, caminos_grilla.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/G - Tron Garbage Collector (DP de perfil con
      etiquetas de componentes).
    - ICPC/Guangzhou 2017/E - Easy Tiling Problem (matriz de transferencia
      por columnas sobre embaldosados).
    - Externos: CSES «Counting Tilings»; UVa 11270 «Tiling Dominoes».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (backtracking: cubrir siempre la
      primera celda libre) en 500 grillas aleatorias hasta 5×5 con celdas
      bloqueadas, y contra valores conocidos (2×n Fibonacci, 8×8)
      (python dp_perfil.py)
"""
import random


def contar_dominos(n, m, bloqueadas=(), mod=None):
    """Número de embaldosados con dominós 1×2 de la grilla n×m sin las celdas bloqueadas."""
    libre = [[(i, j) not in bloqueadas for j in range(m)] for i in range(n)]
    if m > n:                                    # transponer: la máscara usa el lado corto
        libre = [list(col) for col in zip(*libre)]
        n, m = m, n
    dp = [0] * (1 << m)
    dp[0] = 1
    for i in range(n):
        for j in range(m):
            nuevo = [0] * (1 << m)
            bit = 1 << j
            for mask in range(1 << m):
                w = dp[mask]
                if not w:
                    continue
                if not libre[i][j]:
                    if not mask & bit:           # bloqueada: nadie debe cubrirla
                        nuevo[mask] += w
                    continue
                if mask & bit:                   # ya cubierta desde arriba
                    nuevo[mask ^ bit] += w
                    continue
                if i + 1 < n and libre[i + 1][j]:                     # vertical
                    nuevo[mask | bit] += w
                if j + 1 < m and libre[i][j + 1] and not mask & (bit << 1):  # horizontal
                    nuevo[mask | (bit << 1)] += w
            if mod:
                nuevo = [x % mod for x in nuevo]
            dp = nuevo
    return dp[0]


def demo():
    print("2×2 ->", contar_dominos(2, 2))                          # 2
    print("3×4 ->", contar_dominos(3, 4))                          # 11
    print("8×8 ->", contar_dominos(8, 8))                          # 12988816
    print("3×3 sin el centro ->", contar_dominos(3, 3, {(1, 1)}))  # 2
    print("CSES 4×7 ->", contar_dominos(4, 7))                     # 781


def pruebas():
    random.seed(11270)

    def bruta(n, m, bloqueadas):
        tabla = [[(i, j) in bloqueadas for j in range(m)] for i in range(n)]

        def rec(pos):
            while pos < n * m and tabla[pos // m][pos % m]:
                pos += 1
            if pos == n * m:
                return 1
            i, j = divmod(pos, m)
            total = 0
            tabla[i][j] = True
            if j + 1 < m and not tabla[i][j + 1]:
                tabla[i][j + 1] = True
                total += rec(pos + 1)
                tabla[i][j + 1] = False
            if i + 1 < n and not tabla[i + 1][j]:
                tabla[i + 1][j] = True
                total += rec(pos + 1)
                tabla[i + 1][j] = False
            tabla[i][j] = False
            return total

        return rec(0)

    # Valores conocidos
    fib = [1, 1]
    for _ in range(30):
        fib.append(fib[-1] + fib[-2])
    for k in range(1, 25):
        assert contar_dominos(2, k) == contar_dominos(k, 2) == fib[k]
    assert contar_dominos(8, 8) == 12988816
    assert contar_dominos(3, 3) == 0 and contar_dominos(1, 1) == 0
    assert contar_dominos(1, 1, {(0, 0)}) == 1
    assert contar_dominos(4, 7, mod=10**9 + 7) == 781

    for _ in range(500):
        n, m = random.randint(1, 5), random.randint(1, 5)
        p = random.choice([0.0, 0.1, 0.25])
        bloqueadas = {(i, j) for i in range(n) for j in range(m) if random.random() < p}
        assert contar_dominos(n, m, bloqueadas) == bruta(n, m, bloqueadas)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
