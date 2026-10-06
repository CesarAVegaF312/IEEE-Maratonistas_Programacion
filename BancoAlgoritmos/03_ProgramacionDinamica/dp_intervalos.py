"""
Programación dinámica — DP de intervalos: cadena de matrices («Interval DP / Matrix chain multiplication»)
Nivel: Intermedio
Ejecutar: python dp_intervalos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Problemas donde la respuesta para un tramo contiguo [i, j] se arma
    eligiendo DÓNDE partirlo (o qué elemento queda último/primero) y
    combinando las respuestas de los dos pedazos. El clásico: multiplicar
    A0·A1·…·A(n-1) (Ai de dims[i] × dims[i+1]) eligiendo los paréntesis que
    minimizan el número de multiplicaciones escalares.
    Señales: «unir elementos ADYACENTES con costo», «paréntesis / orden de
    evaluación», «cortar un palo en puntos dados», «eliminar elementos de
    una fila y lo que queda se junta», «palíndromos», gramáticas sobre
    subcadenas; n ≤ ~300–500 (O(n³)).

FUNCIÓN
    cadena_matrices(dims) -> (int, arbol)
        Costo mínimo de multiplicar las n = len(dims) - 1 matrices y el árbol
        de paréntesis: un entero k (la matriz Ak) o una tupla (izq, der).
    parentizar(arbol) -> str      p. ej. "((A0 A1) A2)".
    costo_arbol(arbol, dims) -> int   costo de multiplicar según ese árbol.

IDEA Y ALGORITMO
    ESTADO      dp[i][j] = costo mínimo de multiplicar Ai·…·Aj (i ≤ j).
    TRANSICIÓN  la ÚLTIMA multiplicación parte en k (i ≤ k < j):
                (Ai…Ak)·(Ak+1…Aj), que cuesta dims[i]·dims[k+1]·dims[j+1]:
                dp[i][j] = min_k dp[i][k] + dp[k+1][j] + dims[i]·dims[k+1]·dims[j+1].
    CASO BASE   dp[i][i] = 0 (una sola matriz no se multiplica).
    ORDEN       por LARGO del intervalo creciente (largo 2, 3, …, n): así
                dp[i][k] y dp[k+1][j], que son más cortos, ya están listos.
                (Alternativa: i decreciente y j creciente.)
    RESPUESTA   dp[0][n-1]; para la parentización se guarda corte[i][j] = k
                óptimo y se arma el árbol bajando desde [0, n-1].
    Por qué: toda parentización tiene una última multiplicación; fijada en
    k, los dos lados son independientes y cada uno debe ser óptimo
    (subestructura óptima). El número de parentizaciones es el número de
    Catalan (exponencial), pero solo hay O(n²) intervalos distintos.
    Patrón general de DP de intervalos: dp[i][j] = mejor sobre «cómo se
    parte [i, j]» (o «cuál elemento se procesa al final») + costo de unir.

MACROALGORITMO
    1. dp[i][i] = 0.
    2. Para largo = 2..n, para i = 0..n-largo (j = i + largo - 1):
    3.    probar cada k en [i, j-1] y quedarse con el mínimo; guardar k.
    4. Respuesta dp[0][n-1].
    5. Reconstruir con una pila: el intervalo [i, j] se parte en corte[i][j].

COMPLEJIDAD
    Tiempo O(n³), memoria O(n²). En Python: n ≈ 200 en ~1 s
    (n³/6 ≈ 1,3·10^6 operaciones). Si el costo cumple la desigualdad del
    cuadrángulo se baja a O(n²) con la optimización de Knuth
    (optimizacion_knuth.py).

EJEMPLO A MANO
    dims = [10, 30, 5, 60] (A0: 10×30, A1: 30×5, A2: 5×60)
      dp[0][1] = 10·30·5 = 1500;  dp[1][2] = 30·5·60 = 9000
      dp[0][2] = min( k=0: 0 + 9000 + 10·30·60 = 27000,
                      k=1: 1500 + 0 + 10·5·60  = 4500 ) = 4500 -> ((A0 A1) A2)

ERRORES TÍPICOS
    - Recorrer i y j en orden creciente simple: dp[k+1][j] aún no existe.
    - Confundir el índice de la dimensión: Ai es dims[i] × dims[i+1], así
      que el costo de unir es dims[i]·dims[k+1]·dims[j+1].
    - Inicializar con 0 en vez de infinito para el mínimo.
    - Recursión top-down con n = 500: 125 000 estados y muchas llamadas; en
      Python mejor bottom-up.

VARIANTES Y RELACIONADOS
    - Cortar un palo (UVa 10003): dp sobre puntos de corte consecutivos.
    - Unir pilas adyacentes con costo = suma (optimizacion_knuth.py).
    - Subsecuencia palindrómica más larga, eliminar bloques («Zuma»),
      reconocer gramáticas (CYK).
    - optimizacion_knuth.py, reconstruccion_solucion.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/A - Arctic Virus (DP por intervalos sobre una
      gramática).
    - ICPC/Colombia 2023/I - Stack Solitaire (DP de intervalos; la versión
      O(n³) no alcanza y se necesita Knuth).
    - Externos: UVa 348 «Optimal Array Multiplication Sequence»; UVa 10003
      «Cutting Sticks».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (generar TODOS los árboles de
      paréntesis, n ≤ 7) en 400 casos aleatorios + casos borde; se verifica
      además que el árbol devuelto cueste exactamente el óptimo
      (python dp_intervalos.py)
"""
import random


def cadena_matrices(dims):
    """(costo mínimo, árbol de paréntesis) para A0…A(n-1), Ai de dims[i] × dims[i+1]."""
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]          # dp[i][i] = 0: caso base
    corte = [[0] * n for _ in range(n)]
    for largo in range(2, n + 1):             # intervalos más cortos primero
        for i in range(n - largo + 1):
            j = i + largo - 1
            mejor, mk = None, i
            for k in range(i, j):             # última multiplicación entre k y k+1
                c = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if mejor is None or c < mejor:
                    mejor, mk = c, k
            dp[i][j], corte[i][j] = mejor, mk
    return dp[0][n - 1], _armar_arbol(corte, n)


def _armar_arbol(corte, n):
    """Arma el árbol desde [0, n-1] con una pila (sin recursión)."""
    nodo = {}
    pila = [(0, n - 1, False)]
    while pila:
        i, j, listo = pila.pop()
        if i == j:
            nodo[i, j] = i
        elif listo:                            # los hijos ya están armados
            k = corte[i][j]
            nodo[i, j] = (nodo[i, k], nodo[k + 1, j])
        else:
            k = corte[i][j]
            pila.append((i, j, True))
            pila.append((i, k, False))
            pila.append((k + 1, j, False))
    return nodo[0, n - 1]


def parentizar(arbol):
    if isinstance(arbol, int):
        return f"A{arbol}"
    return f"({parentizar(arbol[0])} {parentizar(arbol[1])})"


def costo_arbol(arbol, dims):
    """Costo de multiplicar según el árbol (independiente de la DP)."""
    def rec(t):                                # devuelve (filas, columnas, costo)
        if isinstance(t, int):
            return dims[t], dims[t + 1], 0
        f1, c1, x = rec(t[0])
        f2, c2, y = rec(t[1])
        assert c1 == f2
        return f1, c2, x + y + f1 * c1 * c2
    return rec(arbol)[2]


def demo():
    dims = [10, 30, 5, 60]
    costo, arbol = cadena_matrices(dims)
    print("dims =", dims, "->", costo, parentizar(arbol))          # 4500 ((A0 A1) A2)
    dims = [40, 20, 30, 10, 30]
    costo, arbol = cadena_matrices(dims)
    print("dims =", dims, "->", costo, parentizar(arbol))          # 26000


def pruebas():
    random.seed(348)

    def todos_los_arboles(i, j):
        if i == j:
            yield i
            return
        for k in range(i, j):
            for izq in todos_los_arboles(i, k):
                for der in todos_los_arboles(k + 1, j):
                    yield (izq, der)

    # Casos borde
    assert cadena_matrices([3, 7]) == (0, 0)
    assert cadena_matrices([2, 3, 4]) == (24, (0, 1))
    assert cadena_matrices([10, 30, 5, 60])[0] == 4500

    for _ in range(400):
        n = random.randint(1, 7)
        dims = [random.randint(1, 30) for _ in range(n + 1)]
        mejor = min(costo_arbol(t, dims) for t in todos_los_arboles(0, n - 1))
        costo, arbol = cadena_matrices(dims)
        assert costo == mejor == costo_arbol(arbol, dims)

    # Intervalos grandes: el árbol devuelto siempre cuesta lo que dice la DP
    for _ in range(5):
        dims = [random.randint(1, 100) for _ in range(61)]
        costo, arbol = cadena_matrices(dims)
        assert costo == costo_arbol(arbol, dims)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
