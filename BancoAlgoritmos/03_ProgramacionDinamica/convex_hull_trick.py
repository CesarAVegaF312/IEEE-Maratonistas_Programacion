"""
Programación dinámica — Convex hull trick y árbol de Li Chao («CHT / Li Chao tree»)
Nivel: Avanzado
Ejecutar: python convex_hull_trick.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Acelerar DP del tipo
        dp[i] = min_{j < i} ( dp[j] + b_j · x_i + c_j ) + d_i
    donde el término que mezcla i y j es un PRODUCTO (algo de j) · (algo de
    i). Para cada j eso es una RECTA y = m_j · x + b_j evaluada en x = x_i:
    el problema se vuelve «insertar rectas y preguntar el mínimo en un
    punto», que se responde en O(log n) o O(1) amortizado en vez de O(n).
    Total O(n log n) en vez de O(n²).
    Señales: al expandir la transición aparece (h_i - h_j)², h_i·h_j,
    p_j·t_i…; n ≤ 2·10^5.

FUNCIÓN
    class CHTMonotono      rectas agregadas con pendiente DECRECIENTE.
        agregar(m, b); consultar(x) (binaria, x cualquiera);
        consultar_creciente(x) (puntero, x no decreciente entre llamadas).
    class LiChao(lo, hi)   rectas en cualquier orden; x entero en [lo, hi].
        agregar(m, b); consultar(x).
    Ambas devuelven el MÍNIMO de m·x + b (para máximo: negar m y b).
    rana_cht(h, C) -> int        AtCoder DP «Frog 3» (h estrictamente creciente).
    rana_lichao(h, C) -> int     la misma DP con h en cualquier orden.
        dp[0] = 0, dp[i] = min_{j<i} dp[j] + (h_i - h_j)² + C; devuelve dp[n-1].

IDEA Y ALGORITMO
    DP ejemplo (rana):
      ESTADO      dp[i] = costo mínimo para llegar a la piedra i.
      TRANSICIÓN  dp[i] = min_j dp[j] + (h_i - h_j)² + C
                        = h_i² + C + min_j ( (-2 h_j) · h_i + (dp[j] + h_j²) ).
                  Recta de j: pendiente m_j = -2 h_j, ordenada b_j = dp[j] + h_j².
      CASO BASE   dp[0] = 0.  ORDEN  i creciente (agregar la recta de i
                  después de calcular dp[i]).  RESPUESTA  dp[n-1].
    Envolvente con pendientes monótonas: el mínimo de varias rectas es una
    función cóncava formada por trozos de algunas rectas («envolvente
    inferior»). Si llegan con pendiente decreciente, cada nueva recta es la
    mejor para x muy grande; al agregarla se borran del final las rectas
    que quedaron inútiles: la del medio (l2) sobra si la nueva (l3) corta a
    l1 antes que l2:  x(l1,l3) ≤ x(l1,l2)  ⇔
        (b3 - b1)(m1 - m2) ≤ (b2 - b1)(m1 - m3)    (sin divisiones).
    Las rectas que quedan están ordenadas por el x donde son óptimas: para
    una consulta se busca con binaria; si las x de consulta crecen, un
    puntero que solo avanza da O(1) amortizado.
    Li Chao: árbol de segmentos sobre los x posibles; cada nodo guarda la
    recta que gana en su punto medio. Al insertar, se comparan la recta del
    nodo y la nueva en mid: la ganadora se queda; la perdedora solo puede
    ganar en UNA mitad (dos rectas se cruzan a lo sumo una vez), y baja por
    esa mitad. Consulta: bajar hacia x tomando el mínimo de los nodos del
    camino. Ambas operaciones O(log rango), sin exigir orden.

MACROALGORITMO
    (Monótono, para la rana)
    1. Agregar la recta de j = 0.
    2. Para i = 1..n-1: dp[i] = consultar(h_i) + h_i² + C.
    3.    Agregar la recta (-2 h_i, dp[i] + h_i²).
    Agregar(m, b): si hay misma pendiente, quedarse con la menor b; borrar
    del final mientras la penúltima, la última y la nueva hagan inútil a
    la última; apilar.
    (Li Chao) Insertar bajando desde la raíz con el intercambio en mid.

COMPLEJIDAD
    Monótono: O(1) amortizado por inserción, O(log n) por consulta (O(1)
    amortizado con el puntero). Li Chao: O(log(hi - lo)) cada operación,
    memoria O(#rectas). n = 2·10^5 en ~1 s en Python.

EJEMPLO A MANO
    Rana, h = [1, 2, 3, 4, 5], C = 6 (recta de j: y = -2h_j·x + dp[j] + h_j²):
      j=0: y = -2x + 1.          dp[1] = mín(-3) + 4 + 6 = 7
      j=1: y = -4x + 11.         dp[2] = mín(-5, -1) + 9 + 6 = 10
      j=2: y = -6x + 19; al agregarla, y = -4x + 11 sobra
           ((19-1)(-2+4) = 36 ≤ (11-1)(-2+6) = 40) y se borra.
                                 dp[3] = mín(-7, -5) + 16 + 6 = 15
      j=3: y = -8x + 31.         dp[4] = mín(-9, -11, -9) + 25 + 6 = 20
    Respuesta 20 (saltos 1 -> 3 -> 5: (4 + 6) + (4 + 6)).

ERRORES TÍPICOS
    - Pendientes en el orden contrario al que exige la estructura (para
      mínimo con pendientes CRECIENTES, invertir el signo de x).
    - Usar divisiones de punto flotante para las intersecciones: errores de
      redondeo; comparar con productos cruzados en enteros.
    - Pendientes iguales sin tratamiento: división por cero.
    - Li Chao con x fuera de [lo, hi], o rango gigante con arreglo fijo
      (usar nodos creados a demanda, como aquí).
    - Olvidar sumar los términos que solo dependen de i (h_i² + C) fuera
      del mínimo.

VARIANTES Y RELACIONADOS
    - Máximo: negar las rectas. Segmentos (rectas en un rango de x): Li Chao
      sobre segmentos, O(log²).
    - Rectas que se borran: CHT con deshacer (rollback) o Li Chao persistente.
    - dp_divide_venceras.py, optimizacion_knuth.py (otras optimizaciones
      cuando el costo no se separa en producto).

DÓNDE PRACTICAR
    - Externos: AtCoder Educational DP Contest Z «Frog 3»; CSES «Monster
      Game I» (pendientes monótonas) y «Monster Game II» (Li Chao);
      Codeforces 319C «Kalila and Dimna in the Logging Industry».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (mínimo sobre todas las rectas / DP
      O(n²)) en 400 conjuntos de rectas con 30 consultas cada uno, 100
      secuencias de inserciones y consultas intercaladas con valores hasta
      10^9 y 300 DP aleatorias + casos borde (python convex_hull_trick.py)
"""
import random


class CHTMonotono:
    """Mínimo de rectas y = m·x + b agregadas con pendiente estrictamente decreciente
    (o igual: se conserva la de menor b)."""

    def __init__(self):
        self.M, self.B = [], []
        self.ptr = 0

    def _sobra_ultima(self, m3, b3):
        """¿La última recta queda inútil entre la penúltima y la nueva (m3, b3)?"""
        m1, b1, m2, b2 = self.M[-2], self.B[-2], self.M[-1], self.B[-1]
        return (b3 - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m3)

    def agregar(self, m, b):
        if self.M and self.M[-1] == m:
            if self.B[-1] <= b:
                return                          # misma pendiente y peor: no sirve
            self.M.pop()
            self.B.pop()
        while len(self.M) >= 2 and self._sobra_ultima(m, b):
            self.M.pop()
            self.B.pop()
        self.M.append(m)
        self.B.append(b)
        self.ptr = min(self.ptr, len(self.M) - 1)

    def _valor(self, i, x):
        return self.M[i] * x + self.B[i]

    def consultar(self, x):
        """Mínimo en x cualquiera: binaria sobre «la siguiente recta ya es mejor»."""
        lo, hi = 0, len(self.M) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if self._valor(mid, x) >= self._valor(mid + 1, x):
                lo = mid + 1                    # el óptimo está más a la derecha
            else:
                hi = mid
        return self._valor(lo, x)

    def consultar_creciente(self, x):
        """Mínimo en x, si las x de las consultas no decrecen: puntero que solo avanza."""
        while self.ptr + 1 < len(self.M) and self._valor(self.ptr + 1, x) <= self._valor(self.ptr, x):
            self.ptr += 1
        return self._valor(self.ptr, x)


class LiChao:
    """Mínimo de rectas en x entero de [lo, hi]; inserciones en cualquier orden.
    Nodos creados a demanda (sirve para rangos como [-10^9, 10^9])."""

    def __init__(self, lo, hi):
        self.lo, self.hi = lo, hi
        self.m, self.b = [None], [None]         # nodo 0 = raíz
        self.izq, self.der = [-1], [-1]

    def _nuevo(self):
        self.m.append(None)
        self.b.append(None)
        self.izq.append(-1)
        self.der.append(-1)
        return len(self.m) - 1

    def agregar(self, m, b):
        nodo, lo, hi = 0, self.lo, self.hi
        while True:
            if self.m[nodo] is None:
                self.m[nodo], self.b[nodo] = m, b
                return
            mid = (lo + hi) // 2
            if m * mid + b < self.m[nodo] * mid + self.b[nodo]:
                # la nueva gana en mid: se queda en el nodo y baja la vieja
                self.m[nodo], m = m, self.m[nodo]
                self.b[nodo], b = b, self.b[nodo]
            if lo == hi:
                return
            cm, cb = self.m[nodo], self.b[nodo]
            if m * lo + b < cm * lo + cb:       # la perdedora gana a la izquierda
                if self.izq[nodo] == -1:
                    self.izq[nodo] = self._nuevo()
                nodo, hi = self.izq[nodo], mid
            elif m * hi + b < cm * hi + cb:     # o a la derecha
                if self.der[nodo] == -1:
                    self.der[nodo] = self._nuevo()
                nodo, lo = self.der[nodo], mid + 1
            else:
                return                          # nunca gana: se descarta

    def consultar(self, x):
        nodo, lo, hi = 0, self.lo, self.hi
        mejor = float("inf")
        while nodo != -1 and self.m[nodo] is not None:
            v = self.m[nodo] * x + self.b[nodo]
            if v < mejor:
                mejor = v
            mid = (lo + hi) // 2
            if x <= mid:
                nodo, hi = self.izq[nodo], mid
            else:
                nodo, lo = self.der[nodo], mid + 1
        return mejor


def rana_cht(h, C):
    """Frog 3 con h estrictamente creciente: pendientes -2h_j decrecientes y x = h_i crecientes."""
    n = len(h)
    dp = [0] * n
    cht = CHTMonotono()
    cht.agregar(-2 * h[0], h[0] * h[0])
    for i in range(1, n):
        dp[i] = cht.consultar_creciente(h[i]) + h[i] * h[i] + C
        cht.agregar(-2 * h[i], dp[i] + h[i] * h[i])
    return dp[n - 1]


def rana_lichao(h, C):
    """La misma DP con h en cualquier orden (pendientes y consultas desordenadas)."""
    n = len(h)
    dp = [0] * n
    arbol = LiChao(min(h), max(h))
    arbol.agregar(-2 * h[0], h[0] * h[0])
    for i in range(1, n):
        dp[i] = arbol.consultar(h[i]) + h[i] * h[i] + C
        arbol.agregar(-2 * h[i], dp[i] + h[i] * h[i])
    return dp[n - 1]


def demo():
    h, C = [1, 2, 3, 4, 5], 6
    print("Frog 3, h =", h, "C =", C, "-> CHT", rana_cht(h, C), "| Li Chao", rana_lichao(h, C))  # 20
    cht = CHTMonotono()
    for m, b in [(2, 0), (0, 3), (-1, 8)]:          # pendientes decrecientes
        cht.agregar(m, b)
    print("mín de {2x, 3, -x+8} en x = 0, 2, 6:", [cht.consultar(x) for x in (0, 2, 6)])  # [0, 3, 2]


def pruebas():
    random.seed(319)

    # Estructuras contra el mínimo directo sobre todas las rectas
    for _ in range(400):
        k = random.randint(1, 25)
        rectas = [(random.randint(-20, 20), random.randint(-50, 50)) for _ in range(k)]
        consultas = sorted(random.randint(-30, 30) for _ in range(30))
        directo = [min(m * x + b for m, b in rectas) for x in consultas]

        cht = CHTMonotono()
        for m, b in sorted(rectas, key=lambda r: -r[0]):   # pendiente decreciente
            cht.agregar(m, b)
        assert [cht.consultar(x) for x in consultas] == directo
        assert [cht.consultar_creciente(x) for x in consultas] == directo

        arbol = LiChao(-30, 30)
        for m, b in rectas:                               # en cualquier orden
            arbol.agregar(m, b)
        assert [arbol.consultar(x) for x in consultas] == directo

    # Consultas intercaladas con inserciones (como en una DP)
    for _ in range(100):
        cht, arbol, rectas = CHTMonotono(), LiChao(-10**9, 10**9), []
        m = 10**6
        for _ in range(40):
            m -= random.randint(0, 3)
            b = random.randint(-10**9, 10**9)
            cht.agregar(m, b)
            arbol.agregar(m, b)
            rectas.append((m, b))
            x = random.randint(-10**9, 10**9)
            esperado = min(mm * x + bb for mm, bb in rectas)
            assert cht.consultar(x) == arbol.consultar(x) == esperado

    # DP de la rana contra O(n²)
    def rana_lenta(h, C):
        dp = [0] * len(h)
        for i in range(1, len(h)):
            dp[i] = min(dp[j] + (h[i] - h[j]) ** 2 + C for j in range(i))
        return dp[-1]

    assert rana_cht([5], 7) == rana_lichao([5], 7) == 0
    assert rana_cht([1, 2, 3, 4, 5], 6) == 20
    assert rana_cht([10, 30, 40, 50, 70, 90], 100) == 1900
    for _ in range(300):
        n = random.randint(1, 40)
        h = sorted(random.sample(range(1, 500), n))
        C = random.randint(0, 3000)
        assert rana_cht(h, C) == rana_lenta(h, C) == rana_lichao(h, C)
        random.shuffle(h)
        assert rana_lichao(h, C) == rana_lenta(h, C)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
