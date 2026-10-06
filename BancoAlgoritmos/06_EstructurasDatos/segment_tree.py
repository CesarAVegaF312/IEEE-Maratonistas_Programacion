"""
Estructuras de datos — Segment tree iterativo («Segment tree, bottom-up»)
Nivel: Intermedio
Ejecutar: python segment_tree.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Mantener un arreglo con actualizaciones PUNTUALES y consultas de RANGO
    de cualquier operación asociativa (suma, mínimo, máximo, gcd, xor,
    composición de funciones…) en O(log N) cada una.
    Señales en el enunciado: «cambia el valor en la posición i» mezclado con
    «mínimo / suma / máximo entre l y r», N y Q hasta 10^5–2·10^5. Si solo
    hay sumas, Fenwick es más corto; si no hay actualizaciones y es mínimo,
    sparse table es O(1) por consulta.

FUNCIÓN
    class SegmentTree(datos, op, neutro)
        datos: lista inicial; op(a, b): operación ASOCIATIVA; neutro: e con
        op(e, x) = op(x, e) = x (0 para suma, inf para mínimo…).
        asignar(i, valor)       a[i] = valor                     O(log N)
        consultar(l, r)         op(a[l], a[l+1], …, a[r-1])       O(log N)
                                (semiabierto; neutro si l >= r)
    Índices desde 0.

IDEA Y ALGORITMO
    Árbol binario guardado en un arreglo t de tamaño 2n: las hojas son
    t[n..2n-1] (= el arreglo) y cada nodo interno i < n guarda
    t[i] = op(t[2i], t[2i+1]). (Funciona con cualquier n, no hace falta
    potencia de 2.)
    - asignar(i): cambiar la hoja t[n+i] y recalcular sus ancestros
      (i //= 2) hasta la raíz: log N nodos.
    - consultar(l, r): l += n, r += n y subir las dos fronteras a la vez.
      Si l es hijo DERECHO (impar), su padre cubriría también algo a la
      izquierda del rango, así que t[l] se usa ya y l avanza; si r es
      impar, t[r-1] es hijo izquierdo cuyo padre se sale por la derecha:
      se usa y r retrocede. Luego ambos suben un nivel. En cada nivel se
      toman a lo sumo 2 nodos: O(log N).
    Para operaciones NO conmutativas (concatenar, componer funciones,
    multiplicar matrices) se acumula por separado lo de la izquierda
    (izq = op(izq, t[l])) y lo de la derecha (der = op(t[r], der)) y al
    final se combina op(izq, der). Así el orden siempre es correcto.
    El ingenuo recorre el rango: O(N) por consulta, O(N·Q) = 10^10.

MACROALGORITMO
    Construir: t[n+i] = datos[i]; para i = n-1..1: t[i] = op(t[2i], t[2i+1]).
    Asignar:   i += n; t[i] = v; mientras i > 1: i //= 2; recalcular t[i].
    Consultar: l += n, r += n; izq = der = neutro; mientras l < r:
               si l impar: izq = op(izq, t[l]); l += 1
               si r impar: r -= 1; der = op(t[r], der)
               l //= 2; r //= 2.
               Devolver op(izq, der).

COMPLEJIDAD
    Construcción O(N); asignar y consultar O(log N). Memoria O(N).
    En Python, ~2–3·10^5 operaciones por segundo con op genérica; con la
    operación escrita en línea (p. ej. min directo) ~2 veces más rápido.

EJEMPLO A MANO
    a = [5, 3, 8, 6], suma (n = 4):
      hojas t[4..7] = 5 3 8 6;  t[2] = 8, t[3] = 14, t[1] = 22
      consultar(1, 4): l = 5, r = 8
        l impar → izq = t[5] = 3, l = 6;  r par;  l = 3, r = 4
        l impar → izq = 3 + t[3] = 17, l = 4; l = 2, r = 2 → fin → 17
      asignar(2, 1): t[6] = 1, t[3] = 7, t[1] = 15.

ERRORES TÍPICOS
    - Rango cerrado [l, r] vs semiabierto [l, r): pasar r + 1.
    - Neutro equivocado (0 para mínimo da respuestas falsas).
    - Operación no conmutativa con un solo acumulador: invierte el orden.
    - Consultas en lugar de "asignar" quieren "sumar": hacer
      asignar(i, valor_actual + d), o mantener el arreglo aparte.
    - Usar la versión recursiva en Python con N = 2·10^5: funciona pero es
      varias veces más lenta.

VARIANTES Y RELACIONADOS
    - Actualización de RANGO: 06_EstructurasDatos/segment_tree_lazy.py.
    - Solo sumas: 06_EstructurasDatos/fenwick.py. Estático y mínimo:
      06_EstructurasDatos/sparse_table.py.
    - «Primer índice con valor >= x» (descender por el árbol), segment tree
      de nodos con varios campos (máximo subarreglo: suma, mejor prefijo,
      mejor sufijo, mejor total).
    - Segment tree sobre valores comprimidos como multiconjunto ordenado.

DÓNDE PRACTICAR
    - (No hay problemas del repo ICPC/ que usen segment tree.)
    - CSES «Dynamic Range Minimum Queries»; CSES «Dynamic Range Sum Queries».
    - CSES «Hotel Queries» (descenso por el árbol de máximos).

VERIFICACIÓN
    - Pruebas (python segment_tree.py): contra un arreglo simple en 600
      secuencias aleatorias de 60 operaciones con suma, mínimo y una
      operación NO conmutativa (concatenar cadenas), más casos borde y
      N = 10^5 con 10^4 operaciones.
"""
import random


class SegmentTree:
    """Segment tree iterativo: asignación puntual y consulta de rango [l, r)."""

    def __init__(self, datos, op, neutro):
        self.n = n = len(datos)
        self.op = op
        self.neutro = neutro
        self.t = [neutro] * n + list(datos)       # hojas en t[n..2n-1]
        for i in range(n - 1, 0, -1):
            self.t[i] = op(self.t[2 * i], self.t[2 * i + 1])

    def asignar(self, i, valor):
        """a[i] = valor y recalcular los ancestros."""
        t, op = self.t, self.op
        i += self.n
        t[i] = valor
        while i > 1:
            i >>= 1
            t[i] = op(t[2 * i], t[2 * i + 1])

    def consultar(self, l, r):
        """op(a[l], …, a[r-1]); neutro si el rango está vacío."""
        t, op = self.t, self.op
        izq = der = self.neutro        # acumuladores: respetan el orden
        l += self.n
        r += self.n
        while l < r:
            if l & 1:                  # l es hijo derecho: usarlo y avanzar
                izq = op(izq, t[l])
                l += 1
            if r & 1:                  # r-1 es hijo izquierdo: usarlo y retroceder
                r -= 1
                der = op(t[r], der)
            l >>= 1
            r >>= 1
        return op(izq, der)


def demo():
    a = [5, 3, 8, 6]
    st = SegmentTree(a, lambda x, y: x + y, 0)
    print("a =", a)
    print("suma [1, 4) =", st.consultar(1, 4))          # 17
    st.asignar(2, 1)
    print("tras a[2] = 1, suma total =", st.consultar(0, 4))   # 15
    sm = SegmentTree(a, min, float("inf"))
    print("mínimo [0, 3) =", sm.consultar(0, 3))        # 3


def pruebas():
    random.seed(1337)
    INF = float("inf")

    # Casos borde
    st = SegmentTree([], lambda x, y: x + y, 0)
    assert st.consultar(0, 0) == 0
    st = SegmentTree([7], min, INF)
    assert st.consultar(0, 1) == 7 and st.consultar(0, 0) == INF
    st.asignar(0, -2)
    assert st.consultar(0, 1) == -2
    st = SegmentTree([4, 4, 4], lambda x, y: x + y, 0)
    assert st.consultar(0, 3) == 12

    operaciones = [
        (lambda x, y: x + y, 0, lambda: random.randint(-10, 10), sum),
        (min, INF, lambda: random.randint(-10, 10), lambda s: min(s, default=INF)),
        (lambda x, y: x + y, "", lambda: random.choice("abc"), "".join),  # no conmutativa
    ]
    for _ in range(600):
        op, neutro, gen, bruta = random.choice(operaciones)
        n = random.randint(1, 20)
        a = [gen() for _ in range(n)]
        st = SegmentTree(a, op, neutro)
        for _ in range(60):
            if random.random() < 0.4:
                i = random.randrange(n)
                a[i] = gen()
                st.asignar(i, a[i])
            else:
                l = random.randint(0, n)
                r = random.randint(l, n)
                assert st.consultar(l, r) == bruta(a[l:r])

    # N grande
    n = 100000
    a = [random.randint(1, 10**9) for _ in range(n)]
    st = SegmentTree(a, min, INF)
    for _ in range(10000):
        i = random.randrange(n)
        a[i] = random.randint(1, 10**9)
        st.asignar(i, a[i])
        st.consultar(random.randrange(n), n)
    assert st.consultar(0, n) == min(a)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
