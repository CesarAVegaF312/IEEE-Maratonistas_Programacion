"""
Matemáticas — Exponenciación de matrices: Fibonacci y recurrencias lineales («matrix exponentiation»)
Nivel: Intermedio
Ejecutar: python exponenciacion_matrices.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Calcular el término n-ésimo de un proceso lineal (recurrencia lineal,
    número de caminos de largo n en un grafo, DP cuya transición es la misma
    en cada paso) cuando n es ENORME (10^9–10^18), en O(k³ log n) con k el
    tamaño del estado.
    Cómo reconocerlo: «f(n) = a·f(n−1) + b·f(n−2) + …» con n ≤ 10^18;
    «cuántos caminos de exactamente L pasos» con L gigante y pocos nodos;
    una DP f[i+1] = (combinación lineal fija de f[i]) con pocos estados
    (k ≤ ~50 en Python) y muchísimos pasos.

FUNCIÓN
    mat_mult(A, B, p) -> matriz           producto mód p
    mat_pow(M, e, p) -> matriz            M^e mód p (e ≥ 0; M^0 = identidad)
    fibonacci(n, p) -> int                F(n) mód p, F(0)=0, F(1)=1
    recurrencia(coefs, iniciales, n, p) -> int
        f(i) = coefs[0]·f(i−1) + … + coefs[k−1]·f(i−k) para i ≥ k,
        con f(0..k−1) = iniciales. Devuelve f(n) mód p.
    caminos(adj, L, p) -> matriz          (adj^L)[u][v] = caminos de u a v
                                          con exactamente L aristas

IDEA Y ALGORITMO
    - Estado: el vector v_i = (f(i+k−1), …, f(i)) contiene todo lo necesario
      para dar un paso. La recurrencia dice que v_{i+1} = M·v_i con la
      matriz «compañera»: primera fila = coefs, y debajo una identidad
      desplazada (copia f(i+k−1) … f(i+1) una posición hacia abajo).
      Entonces v_n = M^n · v_0.
    - Exponenciación binaria: M^e = (M^{e/2})² si e es par y M·M^{e−1} si es
      impar; vale porque el producto de matrices es ASOCIATIVO (aunque no
      conmutativo, las potencias de una misma M sí conmutan entre sí). Así
      bastan O(log e) productos.
    - Caminos: (A^L)[u][v] = Σ_w (A^{L−1})[u][w]·A[w][v]: por inducción, un
      camino de largo L de u a v es uno de largo L−1 hasta w más la arista
      (w, v).
    - El ingenuo (iterar n pasos) es O(n·k): imposible con n = 10^18.

MACROALGORITMO
    1. Elegir el vector de estado (lo mínimo que determina el siguiente paso).
    2. Escribir la matriz de transición M (k×k) con v_{i+1} = M·v_i.
    3. Calcular M^n con exponenciación binaria (cuadrados + multiplicaciones
       según los bits de n), todo mód p.
    4. Multiplicar M^n por el vector inicial y leer la componente pedida.
    5. Si k es grande (≥ 50) y es una recurrencia de una sola sucesión,
       preferir Kitamasa (kitamasa.py, O(k² log n)).

COMPLEJIDAD
    O(k³ log n) tiempo, O(k²) memoria. En Python puro: k = 2 con n = 10^18
    es instantáneo; k ≈ 30 son ~60 productos de 27 000 operaciones (~0,1 s);
    k = 100 ya pasa de 1 s por consulta.

EJEMPLO A MANO
    Fibonacci con M = [[1,1],[1,0]]: M^n = [[F(n+1), F(n)], [F(n), F(n−1)]].
    n = 5 = 101₂: M¹ = [[1,1],[1,0]]; M² = [[2,1],[1,1]]; M⁴ = [[5,3],[3,2]];
    M⁵ = M⁴·M¹ = [[8,5],[5,3]] → F(5) = 5.

ERRORES TÍPICOS
    - Orden de los índices del estado (¿f(i) arriba o abajo?) desalineado
      con la primera fila de la matriz.
    - Usar n en vez de n − (k − 1) pasos cuando el vector empieza en
      (f(k−1), …, f(0)): hay que leer la componente correcta.
    - Olvidar el «% p» dentro del producto (en Python solo es lento; en C++
      desborda: reducir tras cada suma de productos de 64 bits).
    - Recurrencias con término constante o polinomial en i: agregar
      componentes al estado (un 1 constante, i, i²…).

VARIANTES Y RELACIONADOS
    - kitamasa.py: O(k² log n) solo para el término n de una recurrencia.
    - berlekamp_massey.py: encontrar la recurrencia a partir de términos.
    - Semianillo (min, +): la misma exponenciación da caminos MÍNIMOS con
      exactamente L aristas.
    - Sumas Σ_{i<n} f(i): agregar una componente acumuladora al estado.
    - exponenciacion_rapida.py (la misma idea con números).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/F - A Fibonacci Family Formula (recurrencia de
      orden k ≤ 100 con n ≤ 10^15; la matriz k×k es correcta pero lenta en
      Python, la solución del repo usa Kitamasa)
    - ICPC/Guangzhou 2017/E - Easy Tiling Problem (matriz de transferencia
      entre patrones; con 187 estados se pasa a Berlekamp–Massey + Kitamasa)
    - CSES «Fibonacci Numbers», «Throwing Dice», «Graph Paths I»

VERIFICACIÓN
    - Pruebas: OK contra iteración directa de la recurrencia (500
      recurrencias aleatorias de orden ≤ 5, n ≤ 60), Fibonacci hasta 300 y
      conteo de caminos por DP en grafos aleatorios (300 casos)
      (python exponenciacion_matrices.py)
"""
import random

MOD = 1_000_000_007


def mat_mult(A, B, p=MOD):
    """Producto de matrices mód p (filas de A por columnas de B)."""
    Bt = list(zip(*B))                       # columnas de B como tuplas
    return [[sum(a * b for a, b in zip(fila, col)) % p for col in Bt] for fila in A]


def mat_pow(M, e, p=MOD):
    """M^e mód p con exponenciación binaria."""
    k = len(M)
    R = [[int(i == j) for j in range(k)] for i in range(k)]   # identidad
    B = [fila[:] for fila in M]
    while e:
        if e & 1:
            R = mat_mult(R, B, p)            # incluir la potencia de este bit
        B = mat_mult(B, B, p)                # M^(2^t) -> M^(2^(t+1))
        e >>= 1
    return R


def fibonacci(n, p=MOD):
    """F(n) mód p con [[1,1],[1,0]]^n = [[F(n+1),F(n)],[F(n),F(n-1)]]."""
    return mat_pow([[1, 1], [1, 0]], n, p)[0][1]


def recurrencia(coefs, iniciales, n, p=MOD):
    """f(n) mód p para f(i) = Σ_j coefs[j]·f(i-1-j), con f(0..k-1) = iniciales."""
    k = len(coefs)
    if n < k:
        return iniciales[n] % p
    # Matriz compañera: fila 0 = coefs; fila i = desplazar f(...) hacia abajo.
    M = [[c % p for c in coefs]] + [[int(j == i - 1) for j in range(k)] for i in range(1, k)]
    P = mat_pow(M, n - (k - 1), p)
    v = iniciales[::-1]                      # (f(k-1), …, f(0))
    return sum(P[0][j] * v[j] for j in range(k)) % p


def caminos(adj, L, p=MOD):
    """(adj^L)[u][v] = número de caminos con exactamente L aristas de u a v."""
    return mat_pow(adj, L, p)


def demo():
    print("M^5 de Fibonacci:", mat_pow([[1, 1], [1, 0]], 5))   # [[8,5],[5,3]]
    print("F(10) =", fibonacci(10), " F(10^18) mód 1e9+7 =", fibonacci(10**18))
    print("tribonacci f(10) (1,1,2,...) =", recurrencia([1, 1, 1], [1, 1, 2], 10))  # 274
    tri = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    print("caminos de 4 aristas 0->0 en un triángulo:", caminos(tri, 4)[0][0])   # 6


def pruebas():
    random.seed(99)

    # Casos borde
    assert mat_pow([[7]], 0) == [[1]]
    assert fibonacci(0) == 0 and fibonacci(1) == 1 and fibonacci(2) == 1
    assert recurrencia([3], [5], 0) == 5 and recurrencia([3], [5], 4) == 5 * 81

    a, b = 0, 1
    for n in range(300):
        assert fibonacci(n) == a % MOD
        a, b = b, a + b

    for _ in range(500):
        k = random.randint(1, 5)
        p = random.choice([MOD, 998244353, 97, 2])
        coefs = [random.randint(0, 10) for _ in range(k)]
        ini = [random.randint(0, 10) for _ in range(k)]
        f = ini[:]
        for i in range(k, 61):
            f.append(sum(coefs[j] * f[i - 1 - j] for j in range(k)))
        n = random.randint(0, 60)
        assert recurrencia(coefs, ini, n, p) == f[n] % p

    for _ in range(300):
        nodos = random.randint(1, 5)
        adj = [[random.randint(0, 1) for _ in range(nodos)] for _ in range(nodos)]
        L = random.randint(0, 12)
        # DP: cnt[v] = caminos de largo t desde u hasta v
        P = caminos(adj, L)
        for u in range(nodos):
            cnt = [int(v == u) for v in range(nodos)]
            for _ in range(L):
                cnt = [sum(cnt[w] * adj[w][v] for w in range(nodos)) for v in range(nodos)]
            assert [c % MOD for c in cnt] == P[u]


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
