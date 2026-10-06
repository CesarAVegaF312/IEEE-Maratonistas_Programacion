"""
Búsqueda completa — Backtracking con poda («Backtracking with pruning»)
Nivel: Intermedio
Ejecutar: python backtracking_poda.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Construir una solución decisión por decisión (fila por fila, elemento
    por elemento) y RETROCEDER apenas una decisión parcial ya no puede
    terminar en una solución válida. Explora el mismo espacio que la fuerza
    bruta, pero corta ramas enteras sin recorrerlas.
    Señales en el enunciado: N pequeño (≤ 15–30) y restricciones fuertes
    entre elementos (no atacarse, no repetir, sumar exactamente S);
    «encuentre todas las configuraciones / cuántas hay / alguna»; tableros
    y rompecabezas (reinas, sudoku, cuadrados mágicos).

FUNCIÓN
    n_reinas(n) -> int
        Cantidad de formas de poner n reinas en un tablero n×n sin que se
        ataquen. Usa máscaras de bits y simetría (espejo de la primera fila).
    n_reinas_una(n) -> list | None
        Una solución: col[f] = columna de la reina de la fila f.
    suma_subconjuntos(a, objetivo) -> int
        a de enteros POSITIVOS. Cuántos subconjuntos (por índice) suman
        exactamente objetivo.

IDEA Y ALGORITMO
    Esquema general: resolver(estado parcial)
        si es completo: contar / guardar
        para cada opción válida: aplicarla, resolver, DESHACERLA
    La poda es la clave: comprobar lo antes posible que la rama no sirve.
    N-reinas: una reina por fila (si no, dos se atacan), así que la
    decisión es la columna de cada fila: n^n → con poda, muchísimo menos.
    Para cada fila se mantienen tres máscaras de casillas atacadas por las
    reinas ya puestas: columnas, diagonal «\\» y diagonal «/». Al bajar una
    fila, las diagonales se desplazan un bit (<<1 y >>1). Las columnas
    libres son ~(col | d1 | d2) & lleno, y se recorren con el bit más bajo.
    Simetría: el reflejo izquierda–derecha de una solución es otra
    solución distinta (nunca es la misma: la reina de la primera fila
    cambiaría de columna salvo que esté al centro). Así basta poner la
    primera reina en la mitad izquierda y multiplicar por 2; si n es impar,
    se suma aparte el caso de la columna central (sin duplicar).
    Suma de subconjuntos: ordenar DESCENDENTE (los grandes se pasan antes y
    podan antes) y llevar el resto[i] = suma de a[i:]. Poda:
      - suma_actual > objetivo → no hay nada que hacer (todos positivos).
      - suma_actual + resto[i] < objetivo → aun tomando todo no se llega.

MACROALGORITMO
    1. Definir el orden de las decisiones (fila por fila, elemento por elemento).
    2. Representar el estado para que validar una opción sea O(1)
       (máscaras, arreglos de usados, sumas acumuladas).
    3. Escribir la recursión: caso completo; para cada opción válida,
       aplicar → recursión → deshacer.
    4. Agregar podas por COTA (no se puede llegar / ya se pasó).
    5. Romper simetrías (fijar la primera decisión en media rango, etc.).
    6. Ordenar las opciones para podar o encontrar antes (las más
       restrictivas o las más grandes primero).

COMPLEJIDAD
    Exponencial en el peor caso; la poda la hace práctica. N-reinas con
    máscaras: n = 12 (14200 soluciones) en ~1 s en Python; n = 14 ya es
    lento. Suma de subconjuntos: O(2^n) peor caso; n ≤ 25–30 según la poda.
    Profundidad de recursión = n (no hace falta pila explícita).

EJEMPLO A MANO
    n = 4 (columnas 0..3), primera reina solo en columnas 0 y 1:
      fila0 col0 → fila1 col2 → fila2: ninguna libre ✗; fila1 col3 → fila2
        col1 → fila3: ninguna ✗          → 0 soluciones
      fila0 col1 → fila1 col3 → fila2 col0 → fila3 col2 ✓ → 1 solución
    total = 2 × 1 = 2   (la otra es su espejo: 2, 0, 3, 1)
    suma_subconjuntos([3, 1, 4, 2], 6): {4,2}, {3,1,2}  → 2

ERRORES TÍPICOS
    - Olvidar DESHACER el cambio al volver (marcas de usado, sumas): las
      ramas siguientes ven un estado sucio.
    - Podar con una condición incorrecta (que también elimina soluciones):
      verificar la poda contra la versión sin poda en casos chicos.
    - Duplicar soluciones simétricas al usar la simetría (columna central
      con n impar).
    - Podas de suma con números negativos: «ya me pasé» deja de ser válida.
    - Copiar listas en cada llamada (O(n) extra por nodo): modificar y deshacer.

VARIANTES Y RELACIONADOS
    - Sudoku, cuadrados mágicos, palabras cruzadas: misma estructura.
    - Cota más fina = branch_and_bound.py; con heurística de distancia =
      a_estrella.py.
    - Sin restricciones entre elementos: subconjuntos_mascaras.py.
    - Muchos estados repetidos: memorizar (programación dinámica).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/D - Dominoes Magic Squares (backtracking con poda por líneas)
    - ICPC/Colombia 2026/L - Don't Ask Why 2D (búsqueda exhaustiva con simetría)
    - UVa 750 «8 Queens Chess Problem»; CSES «Chessboard and Queens»

VERIFICACIÓN
    - Pruebas: OK. N-reinas contra los valores conocidos (n = 1..12) y
      contra fuerza bruta con itertools.permutations (n ≤ 8); la solución
      única se valida; suma de subconjuntos contra las 2^n máscaras en 2000
      casos aleatorios + casos borde (python backtracking_poda.py)
"""
import itertools
import random


def n_reinas(n):
    """Cantidad de soluciones de las n reinas (máscaras + simetría)."""
    lleno = (1 << n) - 1

    def contar(cols, d1, d2):
        # cols: columnas ocupadas; d1/d2: casillas atacadas en ESTA fila por diagonales
        if cols == lleno:
            return 1
        total = 0
        libres = ~(cols | d1 | d2) & lleno
        while libres:
            b = libres & -libres            # tomar la columna libre más baja
            libres ^= b
            total += contar(cols | b, (d1 | b) << 1 & lleno, (d2 | b) >> 1)
        return total

    if n == 0:
        return 1
    total = 0
    for c in range(n // 2):                 # primera reina en la mitad izquierda
        b = 1 << c
        total += 2 * contar(b, b << 1 & lleno, b >> 1)   # ×2 por el espejo
    if n % 2 == 1:                          # columna central: su espejo es ella misma
        b = 1 << (n // 2)
        total += contar(b, b << 1 & lleno, b >> 1)
    return total


def n_reinas_una(n):
    """Una solución de n reinas (col[f] por fila) o None si no hay."""
    col = []
    usadas, diag1, diag2 = set(), set(), set()   # columnas, f - c, f + c

    def poner(f):
        if f == n:
            return True
        for c in range(n):
            if c in usadas or f - c in diag1 or f + c in diag2:
                continue                    # poda: atacada
            col.append(c); usadas.add(c); diag1.add(f - c); diag2.add(f + c)
            if poner(f + 1):
                return True
            col.pop(); usadas.remove(c); diag1.remove(f - c); diag2.remove(f + c)  # deshacer
        return False

    return col if poner(0) else None


def suma_subconjuntos(a, objetivo):
    """Cuántos subconjuntos de a (positivos) suman exactamente objetivo."""
    a = sorted(a, reverse=True)             # grandes primero: podan antes
    n = len(a)
    resto = [0] * (n + 1)                   # resto[i] = a[i] + ... + a[n-1]
    for i in range(n - 1, -1, -1):
        resto[i] = resto[i + 1] + a[i]

    def contar(i, suma):
        if suma == objetivo:
            return 1                        # positivos: agregar más solo sube la suma
        if i == n or suma > objetivo or suma + resto[i] < objetivo:
            return 0                        # poda por cota
        return contar(i + 1, suma + a[i]) + contar(i + 1, suma)

    return contar(0, 0)


def demo():
    print("n_reinas(n), n = 1..10:", [n_reinas(n) for n in range(1, 11)])
    print("una solución para n = 8:", n_reinas_una(8))
    print("suma_subconjuntos([3, 1, 4, 2], 6) =", suma_subconjuntos([3, 1, 4, 2], 6))   # 2


def _valida(col):
    n = len(col)
    return all(col[i] != col[j] and abs(col[i] - col[j]) != j - i
               for i in range(n) for j in range(i + 1, n))


def pruebas():
    random.seed(750)

    conocidos = [1, 1, 0, 0, 2, 10, 4, 40, 92, 352, 724, 2680, 14200]   # n = 0..12
    for n, v in enumerate(conocidos):
        assert n_reinas(n) == v
    # fuerza bruta: una reina por fila y columna = permutación; revisar diagonales
    for n in range(1, 9):
        assert n_reinas(n) == sum(1 for p in itertools.permutations(range(n)) if _valida(p))
    for n in range(0, 13):
        s = n_reinas_una(n)
        if conocidos[n] == 0:
            assert s is None
        else:
            assert len(s) == n and _valida(s)

    # Casos borde de suma de subconjuntos
    assert suma_subconjuntos([], 0) == 1                    # el vacío
    assert suma_subconjuntos([], 5) == 0
    assert suma_subconjuntos([5], 5) == 1
    assert suma_subconjuntos([1, 1, 1], 2) == 3             # por índice, no por valor

    for _ in range(2000):
        n = random.randint(0, 12)
        a = [random.randint(1, 15) for _ in range(n)]
        obj = random.randint(0, 60)
        bruta = sum(1 for m in range(1 << n) if sum(a[i] for i in range(n) if m >> i & 1) == obj)
        assert suma_subconjuntos(a, obj) == bruta


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
