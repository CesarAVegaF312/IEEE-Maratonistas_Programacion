"""
Estructuras de datos — Segment tree con propagación perezosa («Lazy propagation»)
Nivel: Avanzado
Ejecutar: python segment_tree_lazy.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Actualizaciones de RANGO y consultas de RANGO, ambas en O(log N). El
    caso clásico (el de este archivo): «sumar v a todos los a[l..r-1]» y
    «suma de a[l..r-1]».
    Señales en el enunciado: «a todos los elementos entre l y r sumarles /
    asignarles / voltearles…» mezclado con «suma / mínimo / máximo entre l
    y r», N y Q hasta 10^5. Sin actualizaciones de rango basta
    06_EstructurasDatos/segment_tree.py; si la consulta es PUNTUAL basta un
    Fenwick sobre las diferencias.

FUNCIÓN
    class SegmentTreeLazy(datos)       índices desde 0, rangos [l, r)
        sumar_rango(l, r, v)           a[i] += v para l <= i < r
        suma(l, r) -> int              a[l] + … + a[r-1]  (0 si l >= r)

IDEA Y ALGORITMO
    Cada nodo cubre un segmento [ini, fin) y guarda la SUMA de ese
    segmento. Una actualización de rango tocaría muchas hojas, así que se
    hace «perezosa»: cuando un nodo queda COMPLETAMENTE dentro del rango a
    actualizar, se corrige su suma (suma += v · largo) y se anota
    pend[nodo] += v: «a todos mis descendientes les debo sumar v», sin
    bajar más. Si más tarde una operación necesita entrar a los hijos de
    ese nodo, primero se EMPUJA la deuda: cada hijo recibe suma += v·largo
    y pend += v, y el nodo queda con pend = 0.
    Invariante: la suma guardada en un nodo es correcta considerando todas
    las deudas de él y de sus descendientes, pero NO las deudas pendientes
    en sus ancestros (por eso se empuja al bajar).
    Igual que en la consulta normal, cualquier rango [l, r) se parte en
    O(log N) nodos completos más O(log N) nodos parciales en los que se
    baja: ambas operaciones son O(log N).
    La recursión solo tiene profundidad log2(N) (~17 para 10^5): no hay
    riesgo de pasar el límite de Python.
    Generalizar: hace falta (1) cómo se aplica una etiqueta a un nodo
    completo y (2) cómo se COMPONEN dos etiquetas. Suma+suma es lo más
    fácil; «asignar» compone como «la última gana»; «asignar y sumar»
    necesita la etiqueta (asignar?, valor, suma).

MACROALGORITMO
    sumar_rango(nodo, ini, fin, l, r, v):
      1. Si [ini, fin) no toca [l, r): nada.
      2. Si [ini, fin) está dentro de [l, r): suma[nodo] += v·(fin - ini);
         pend[nodo] += v; terminar.
      3. Si no: empujar(nodo); bajar a los dos hijos; suma[nodo] = suma de
         los hijos.
    suma(nodo, ini, fin, l, r):
      1. Sin intersección: 0.  Dentro: suma[nodo].
      2. Si no: empujar(nodo) y devolver la suma de los dos hijos.

COMPLEJIDAD
    Construcción O(N); cada operación O(log N). Memoria O(4N).
    En Python (recursivo), ~5·10^4–10^5 operaciones por segundo: con
    N = Q = 10^5 puede tardar 1–3 s. Para más velocidad: versión iterativa
    o Fenwick doble (ver variantes).

EJEMPLO A MANO
    a = [1, 2, 3, 4] (raíz [0,4) = 10; hijos [0,2) = 3 y [2,4) = 7)
    sumar_rango(1, 4, 10):
      raíz parcial → empujar (nada), bajar
        [0,2) parcial → bajar: [0,1) fuera; [1,2) dentro: suma 12, pend 10
          → [0,2) = 1 + 12 = 13
        [2,4) dentro: suma 7 + 10·2 = 27, pend 10 (las hojas 3 y 4 NO se tocan)
      raíz = 13 + 27 = 40
    suma(2, 3): raíz → [2,4) parcial → empujar pend 10 a [2,3) y [3,4):
      [2,3) = 3 + 10 = 13 → respuesta 13.

ERRORES TÍPICOS
    - Olvidar empujar antes de bajar (en la actualización Y en la
      consulta): los hijos quedan desactualizados.
    - Aplicar la etiqueta sin multiplicar por el largo del segmento.
    - Recalcular suma[nodo] tras actualizar los hijos: olvidarlo deja la
      suma del padre vieja.
    - Arreglos de tamaño 2N en la versión recursiva: hace falta 4N.
    - Etiquetas que no conmutan (asignar después de sumar): componerlas
      en el orden correcto.

VARIANTES Y RELACIONADOS
    - Asignación en rango + mínimo/suma; sumar en rango + mínimo en rango
      (el mínimo de un nodo completo sube en v, sin multiplicar).
    - Solo «sumar en rango + suma en rango»: dos Fenwick (más rápido en
      Python): suma(0, i) = B1(i)·i − B2(i).
    - 06_EstructurasDatos/segment_tree.py (sin perezosa),
      06_EstructurasDatos/fenwick.py, 06_EstructurasDatos/descomposicion_raiz.py
      (alternativa más simple de escribir con O(√N) por operación).

DÓNDE PRACTICAR
    - (No hay problemas del repo ICPC/ que lo usen.)
    - SPOJ HORRIBLE «Horrible Queries» (exactamente este problema).
    - CSES «Range Updates and Sums» (sumar y asignar en rango).

VERIFICACIÓN
    - Pruebas (python segment_tree_lazy.py): contra un arreglo simple en
      500 secuencias aleatorias de 60 operaciones (N <= 25), casos borde y
      N = 10^5 con 2·10^4 operaciones.
"""
import random


class SegmentTreeLazy:
    """Suma en rango + consulta de suma en rango, con propagación perezosa."""

    def __init__(self, datos):
        self.n = n = len(datos)
        self.suma_ = [0] * (4 * max(n, 1))   # suma del segmento de cada nodo
        self.pend = [0] * (4 * max(n, 1))    # cuánto deben sumar los descendientes
        if n:
            self._construir(1, 0, n, datos)

    def _construir(self, nodo, ini, fin, datos):
        if fin - ini == 1:
            self.suma_[nodo] = datos[ini]
            return
        m = (ini + fin) // 2
        self._construir(2 * nodo, ini, m, datos)
        self._construir(2 * nodo + 1, m, fin, datos)
        self.suma_[nodo] = self.suma_[2 * nodo] + self.suma_[2 * nodo + 1]

    def _empujar(self, nodo, ini, fin):
        """Pasar la deuda del nodo a sus dos hijos."""
        v = self.pend[nodo]
        if v:
            m = (ini + fin) // 2
            for hijo, largo in ((2 * nodo, m - ini), (2 * nodo + 1, fin - m)):
                self.suma_[hijo] += v * largo
                self.pend[hijo] += v
            self.pend[nodo] = 0

    def sumar_rango(self, l, r, v, nodo=1, ini=0, fin=None):
        """a[i] += v para l <= i < r."""
        if fin is None:
            fin = self.n
        if r <= ini or fin <= l or l >= r:
            return                                  # sin intersección
        if l <= ini and fin <= r:                   # nodo completo: perezoso
            self.suma_[nodo] += v * (fin - ini)
            self.pend[nodo] += v
            return
        self._empujar(nodo, ini, fin)
        m = (ini + fin) // 2
        self.sumar_rango(l, r, v, 2 * nodo, ini, m)
        self.sumar_rango(l, r, v, 2 * nodo + 1, m, fin)
        self.suma_[nodo] = self.suma_[2 * nodo] + self.suma_[2 * nodo + 1]

    def suma(self, l, r, nodo=1, ini=0, fin=None):
        """a[l] + … + a[r-1]."""
        if fin is None:
            fin = self.n
        if r <= ini or fin <= l or l >= r:
            return 0
        if l <= ini and fin <= r:
            return self.suma_[nodo]
        self._empujar(nodo, ini, fin)
        m = (ini + fin) // 2
        return (self.suma(l, r, 2 * nodo, ini, m)
                + self.suma(l, r, 2 * nodo + 1, m, fin))


def demo():
    a = [1, 2, 3, 4]
    st = SegmentTreeLazy(a)
    print("a =", a)
    st.sumar_rango(1, 4, 10)
    print("tras sumar 10 a [1, 4): suma total =", st.suma(0, 4))   # 40
    print("suma [2, 3) =", st.suma(2, 3))                          # 13
    print("suma [0, 2) =", st.suma(0, 2))                          # 13


def pruebas():
    random.seed(4096)

    # Casos borde
    st = SegmentTreeLazy([])
    assert st.suma(0, 0) == 0
    st = SegmentTreeLazy([5])
    st.sumar_rango(0, 1, -3)
    assert st.suma(0, 1) == 2 and st.suma(0, 0) == 0
    st = SegmentTreeLazy([0] * 7)
    st.sumar_rango(0, 7, 1)
    st.sumar_rango(3, 3, 100)                      # rango vacío
    assert st.suma(0, 7) == 7 and st.suma(2, 5) == 3

    for _ in range(500):
        n = random.randint(1, 25)
        a = [random.randint(-10, 10) for _ in range(n)]
        st = SegmentTreeLazy(a)
        for _ in range(60):
            l = random.randint(0, n)
            r = random.randint(l, n)
            if random.random() < 0.5:
                v = random.randint(-5, 5)
                st.sumar_rango(l, r, v)
                for i in range(l, r):
                    a[i] += v
            else:
                assert st.suma(l, r) == sum(a[l:r])

    # N grande
    n = 100000
    a = [random.randint(0, 10**9) for _ in range(n)]
    st = SegmentTreeLazy(a)
    total = sum(a)
    for _ in range(10000):
        l = random.randrange(n)
        r = random.randint(l, n)
        v = random.randint(-1000, 1000)
        st.sumar_rango(l, r, v)
        total += v * (r - l)
        st.suma(random.randrange(n), n)
    assert st.suma(0, n) == total


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
