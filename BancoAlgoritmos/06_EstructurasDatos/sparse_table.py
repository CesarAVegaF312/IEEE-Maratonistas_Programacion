"""
Estructuras de datos — Sparse table para RMQ estático («Sparse table, range minimum query»)
Nivel: Intermedio
Ejecutar: python sparse_table.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Responder en O(1) muchas consultas «mínimo (o máximo, gcd, AND, OR) de
    a[l..r-1]» sobre un arreglo que NO cambia, tras un preprocesamiento
    O(N log N).
    Señales en el enunciado: arreglo fijo + Q consultas de mínimo/máximo
    en rango con Q muy grande (10^5–10^6), LCA por recorrido de Euler,
    «el más bajo entre las posiciones i y j», arreglo de sufijos + LCP.
    Si el arreglo cambia, usar 06_EstructurasDatos/segment_tree.py.

FUNCIÓN
    class SparseTable(a, op=min)
        op debe ser asociativa e IDEMPOTENTE: op(x, x) = x
        (min, max, gcd, &, |). NO sirve para suma (ver variantes).
        consultar(l, r) -> valor     op(a[l], …, a[r-1]), exige l < r.
    Índices desde 0, rango semiabierto [l, r).

IDEA Y ALGORITMO
    tabla[k][i] = op de los 2^k elementos a[i .. i + 2^k - 1].
    Se construye por niveles: un bloque de 2^k es la unión de dos de 2^(k-1):
        tabla[k][i] = op(tabla[k-1][i], tabla[k-1][i + 2^(k-1)]).
    Consulta: con largo L = r - l y k = ⌊log2 L⌋, los dos bloques de 2^k
    que empiezan en l y terminan en r-1 CUBREN [l, r) (porque 2·2^k >= L),
    aunque se solapen. Como op es idempotente, contar dos veces el solape
    no cambia el resultado:
        consultar(l, r) = op(tabla[k][l], tabla[k][r - 2^k]).
    Dos accesos y una operación: O(1).
    El ingenuo es O(N) por consulta; precalcular todos los pares (l, r) es
    O(N²) de memoria. La tabla dispersa guarda solo los bloques de tamaño
    potencia de 2: N·log N valores.

MACROALGORITMO
    1. tabla[0] = a.
    2. Para k = 1 mientras 2^k <= N: tabla[k][i] = op(tabla[k-1][i],
       tabla[k-1][i + 2^(k-1)]) para i = 0..N - 2^k.
    3. Consulta (l, r): k = (r - l).bit_length() - 1;
       devolver op(tabla[k][l], tabla[k][r - 2^k]).

COMPLEJIDAD
    Construcción O(N log N) tiempo y memoria; consulta O(1).
    En Python, N = 10^6 se construye en ~1–2 s (con map en C); ~10^6
    consultas por segundo.

EJEMPLO A MANO
    a = [5, 2, 4, 7, 1, 3, 6, 8]
      tabla[0] = 5 2 4 7 1 3 6 8
      tabla[1] = 2 2 4 1 1 3 6          (mínimo de pares)
      tabla[2] = 2 1 1 1 1              (mínimo de bloques de 4)
      tabla[3] = 1
    consultar(1, 7) (a[1..6] = 2 4 7 1 3 6): L = 6, k = 2 (bloques de 4)
      min(tabla[2][1], tabla[2][3]) = min(1, 1) = 1     (a[1..4] y a[3..6])
    consultar(0, 3): L = 3, k = 1 → min(tabla[1][0], tabla[1][1]) = 2.

ERRORES TÍPICOS
    - Usarla con suma u otra operación no idempotente: el solape se cuenta
      doble.
    - Calcular log2 con flotantes (math.log2 puede redondear mal en
      potencias de 2 grandes): usar bit_length().
    - Rangos cerrados vs semiabiertos (aquí [l, r)).
    - Consultar con l == r (rango vacío): no hay valor neutro.

VARIANTES Y RELACIONADOS
    - Devolver el ÍNDICE del mínimo: guardar índices y comparar a[i].
    - Suma con sparse table: O(log N) partiendo en bloques disjuntos (pero
      para eso basta un arreglo de sumas prefijas).
    - LCA en O(1): sparse table sobre el recorrido de Euler (profundidades);
      ver 05_Grafos/lca.py.
    - Disjoint sparse table: O(1) para cualquier operación asociativa.
    - 06_EstructurasDatos/segment_tree.py (con actualizaciones),
      06_EstructurasDatos/pila_monotona.py (otras preguntas de mínimos).

DÓNDE PRACTICAR
    - (No hay problemas del repo ICPC/ que la usen.)
    - CSES «Static Range Minimum Queries».

VERIFICACIÓN
    - Pruebas (python sparse_table.py): contra min/max/gcd/AND por fuerza
      bruta sobre todos los rangos en 800 arreglos aleatorios (N <= 40),
      casos borde (N = 1, todos iguales, potencias de 2) y N = 2·10^5.
"""
import random
from math import gcd


class SparseTable:
    """Consultas O(1) de una operación idempotente sobre un arreglo fijo."""

    def __init__(self, a, op=min):
        self.op = op
        self.tabla = [list(a)]
        k = 1
        while (1 << k) <= len(a):
            ant = self.tabla[-1]
            mitad = 1 << (k - 1)
            # Bloque 2^k en i = op(bloque 2^(k-1) en i, bloque 2^(k-1) en i + mitad)
            self.tabla.append(list(map(op, ant[:len(ant) - mitad], ant[mitad:])))
            k += 1

    def consultar(self, l, r):
        """op(a[l], …, a[r-1]) con l < r."""
        k = (r - l).bit_length() - 1          # mayor potencia de 2 <= largo
        fila = self.tabla[k]
        return self.op(fila[l], fila[r - (1 << k)])   # dos bloques que se solapan


def demo():
    a = [5, 2, 4, 7, 1, 3, 6, 8]
    st = SparseTable(a)
    print("a =", a)
    for k, fila in enumerate(st.tabla):
        print(f"  tabla[{k}] =", fila)
    print("mínimo [1, 7) =", st.consultar(1, 7))     # 1
    print("mínimo [0, 3) =", st.consultar(0, 3))     # 2
    print("máximo [2, 5) =", SparseTable(a, max).consultar(2, 5))   # 7


def pruebas():
    random.seed(2718)

    # Casos borde
    st = SparseTable([9])
    assert st.consultar(0, 1) == 9
    st = SparseTable([3] * 16)
    assert all(st.consultar(l, r) == 3 for l in range(16) for r in range(l + 1, 17))
    st = SparseTable(list(range(64, 0, -1)))       # largo potencia de 2
    assert st.consultar(0, 64) == 1 and st.consultar(0, 32) == 33

    ops = [min, max, gcd, lambda x, y: x & y]
    for _ in range(800):
        op = random.choice(ops)
        n = random.randint(1, 40)
        a = [random.randint(0, 60) for _ in range(n)]
        st = SparseTable(a, op)
        for l in range(n):
            acc = a[l]
            for r in range(l + 1, n + 1):
                acc = op(acc, a[r - 1])            # acumulado obvio de a[l..r-1]
                assert st.consultar(l, r) == acc

    # N grande
    n = 200000
    a = [random.randint(-10**9, 10**9) for _ in range(n)]
    st = SparseTable(a)
    assert st.consultar(0, n) == min(a)
    for _ in range(1000):
        l = random.randrange(n)
        r = random.randint(l + 1, min(n, l + 50))
        assert st.consultar(l, r) == min(a[l:r])


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
