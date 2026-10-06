"""
Estructuras de datos — Descomposición en raíz cuadrada («Sqrt decomposition»)
Nivel: Avanzado
Ejecutar: python descomposicion_raiz.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Partir el arreglo en ~√N bloques de ~√N elementos y guardar un resumen
    por bloque (suma, mínimo, arreglo ordenado, etiqueta perezosa…). Una
    operación de rango toca a lo sumo 2 bloques «parciales» (elemento por
    elemento) y el resto como bloques «completos» (por su resumen):
    O(√N) por operación. Es más lento que un segment tree, pero MUCHO más
    fácil de adaptar a operaciones raras: «cuántos >= x en [l, r) con
    actualizaciones», «reconstruir cada √Q operaciones», saltos tipo
    Codeforces 13E «Holes».
    Señales en el enunciado: N, Q hasta ~10^5 con operaciones de rango que
    no se combinan bien en un segment tree, o cuando no hay tiempo para
    pensar la etiqueta perezosa correcta.

FUNCIÓN
    class BloquesRaiz(datos)          índices desde 0, rangos [l, r)
        sumar_rango(l, r, v)          a[i] += v para l <= i < r
        asignar(i, v)                 a[i] = v
        suma(l, r) -> int             a[l] + … + a[r-1]
        contar_mayores(l, r, x) -> int    cuántos i en [l, r) con a[i] > x
    (contar_mayores muestra lo que el segment tree no hace fácil: cada
    bloque guarda además sus valores ORDENADOS y responde con bisect.)

IDEA Y ALGORITMO
    Bloque b cubre [b·B, (b+1)·B). Por bloque se guarda:
      suma_b  = suma de sus valores REALES (incluida su etiqueta)
      pend_b  = cantidad sumada a TODO el bloque y aún no aplicada a sus
                elementos (perezosa: el valor real de a[i] es
                base[i] + pend_b)
      orden_b = valores base del bloque, ordenados (para contar_mayores)
    - Rango parcial (los extremos): se modifica base[i] uno por uno y se
      RECONSTRUYE el resumen del bloque (re-ordenar: O(B log B)).
    - Bloques completos: solo se toca el resumen: pend_b += v,
      suma_b += v·B. O(1) cada uno.
    - contar_mayores en bloque completo: a[i] > x ⇔ base[i] > x - pend_b,
      con bisect sobre orden_b: O(log B).
    Con B ≈ √N, cada operación toca <= 2·B elementos sueltos y <= N/B
    bloques completos: O(√N) (o O(√N log N) con el reordenamiento).
    Elegir B: si los bloques completos son más caros (log), conviene un B
    algo mayor; en Python B entre 64 y 512 suele ir bien.

MACROALGORITMO
    1. B = max(1, ⌊√N⌋); base = copia de datos; armar resúmenes.
    2. Para una operación en [l, r):
       a. Si l y r - 1 están en el mismo bloque: recorrer elemento por
          elemento (y reconstruir ese bloque si se modificó).
       b. Si no: parte izquierda [l, fin del bloque de l) a mano;
          bloques completos intermedios por su resumen; parte derecha
          [inicio del bloque de r-1, r) a mano.
    3. Reconstruir un bloque = recalcular suma y orden con sus base[i]
       (pend del bloque se mantiene aparte).

COMPLEJIDAD
    sumar_rango, suma: O(√N) (+ O(B log B) al reconstruir los parciales).
    contar_mayores: O(√N · log N). asignar: O(B log B). Memoria O(N).
    En Python, ~10^4–5·10^4 operaciones por segundo con N = 10^5.

EJEMPLO A MANO
    a = [3, 1, 4, 1, 5, 9, 2, 6, 5], N = 9, B = 3
    bloques: [3 1 4] suma 8 | [1 5 9] suma 15 | [2 6 5] suma 13
    sumar_rango(1, 8, 10):
      bloque 0 parcial: a[1], a[2] += 10 → [3 11 14], suma 28
      bloque 1 completo: pend 10, suma 15 + 30 = 45
      bloque 2 parcial: a[6], a[7] += 10 → [12 16 5], suma 33
    suma(2, 7) = a[2] (14) + bloque 1 (45) + a[6] (12) = 71.
    contar_mayores(0, 9, 10): bloque 0: {11,14} → 2; bloque 1: base > 0 → 3;
      bloque 2: {12,16} → 2;  total 7.

ERRORES TÍPICOS
    - Olvidar sumar pend_b al leer un elemento suelto de un bloque con
      etiqueta.
    - No reconstruir el resumen tras modificar un bloque parcial.
    - Caso «l y r en el mismo bloque»: si se trata como izquierda + derecha
      se cuentan elementos dos veces.
    - B = 0 con N = 0 (usar max(1, …)).

VARIANTES Y RELACIONADOS
    - Descomposición sobre CONSULTAS: acumular √Q actualizaciones y
      reconstruir todo cada tanto.
    - División de casos por tamaño («pesados» vs «livianos»: grados >= √M
      en grafos, divisores pequeños vs grandes).
    - 06_EstructurasDatos/algoritmo_mo.py (√N sobre el orden de consultas),
      06_EstructurasDatos/segment_tree_lazy.py (lo mismo en O(log N), si la
      operación lo permite).

DÓNDE PRACTICAR
    - (No hay problemas del repo ICPC/ que lo usen.)
    - Codeforces 13E «Holes» (bloques con saltos precalculados).
    - SPOJ HORRIBLE «Horrible Queries» (también sale así en O(√N)).

VERIFICACIÓN
    - Pruebas (python descomposicion_raiz.py): contra un arreglo simple en
      400 secuencias aleatorias de 60 operaciones (N <= 30, bloques de
      varios tamaños), casos borde (N = 0, 1, todos iguales) y N = 5·10^4
      con 5000 operaciones.
"""
import random
from bisect import bisect_right
from math import isqrt


class BloquesRaiz:
    """Suma en rango, suma de rango, asignación y conteo de mayores en O(√N)."""

    def __init__(self, datos, tam_bloque=None):
        self.n = n = len(datos)
        self.B = B = tam_bloque or max(1, isqrt(n))
        self.base = list(datos)                    # valor real = base[i] + pend[bloque]
        nb = (n + B - 1) // B
        self.pend = [0] * nb
        self.sumab = [0] * nb
        self.orden = [None] * nb
        for b in range(nb):
            self._reconstruir(b)

    def _reconstruir(self, b):
        """Recalcular el resumen del bloque b a partir de base (pend aparte)."""
        ini, fin = b * self.B, min(self.n, (b + 1) * self.B)
        trozo = self.base[ini:fin]
        self.orden[b] = sorted(trozo)
        self.sumab[b] = sum(trozo) + self.pend[b] * (fin - ini)

    def sumar_rango(self, l, r, v):
        if l >= r:
            return
        B, base = self.B, self.base
        bl, br = l // B, (r - 1) // B
        if bl == br:                                    # todo en un bloque
            for i in range(l, r):
                base[i] += v
            self._reconstruir(bl)
            return
        for i in range(l, (bl + 1) * B):                # parcial izquierdo
            base[i] += v
        self._reconstruir(bl)
        for b in range(bl + 1, br):                     # completos: solo resumen
            self.pend[b] += v
            self.sumab[b] += v * B
        for i in range(br * B, r):                      # parcial derecho
            base[i] += v
        self._reconstruir(br)

    def asignar(self, i, v):
        b = i // self.B
        self.base[i] = v - self.pend[b]                 # que base + pend dé v
        self._reconstruir(b)

    def suma(self, l, r):
        if l >= r:
            return 0
        B, base, pend = self.B, self.base, self.pend
        bl, br = l // B, (r - 1) // B
        if bl == br:
            return sum(base[l:r]) + pend[bl] * (r - l)
        s = sum(base[l:(bl + 1) * B]) + pend[bl] * ((bl + 1) * B - l)
        s += sum(self.sumab[bl + 1:br])
        s += sum(base[br * B:r]) + pend[br] * (r - br * B)
        return s

    def contar_mayores(self, l, r, x):
        """Cuántos i en [l, r) tienen a[i] > x."""
        if l >= r:
            return 0
        B, base, pend = self.B, self.base, self.pend
        bl, br = l // B, (r - 1) // B
        if bl == br:
            return sum(1 for i in range(l, r) if base[i] + pend[bl] > x)
        c = sum(1 for i in range(l, (bl + 1) * B) if base[i] + pend[bl] > x)
        for b in range(bl + 1, br):                     # bisect en el bloque ordenado
            o = self.orden[b]
            c += len(o) - bisect_right(o, x - pend[b])
        c += sum(1 for i in range(br * B, r) if base[i] + pend[br] > x)
        return c


def demo():
    a = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    s = BloquesRaiz(a)
    print("a =", a, " B =", s.B)
    s.sumar_rango(1, 8, 10)
    print("tras sumar 10 a [1, 8): suma(2, 7) =", s.suma(2, 7))        # 71
    print("contar_mayores(0, 9, 10) =", s.contar_mayores(0, 9, 10))   # 7


def pruebas():
    random.seed(13)

    # Casos borde
    s = BloquesRaiz([])
    assert s.suma(0, 0) == 0 and s.contar_mayores(0, 0, 5) == 0
    s = BloquesRaiz([4])
    s.sumar_rango(0, 1, 3)
    assert s.suma(0, 1) == 7 and s.contar_mayores(0, 1, 6) == 1
    s.asignar(0, -1)
    assert s.suma(0, 1) == -1
    s = BloquesRaiz([2] * 10)
    s.sumar_rango(0, 10, 1)
    assert s.suma(0, 10) == 30 and s.contar_mayores(3, 9, 2) == 6

    for _ in range(400):
        n = random.randint(1, 30)
        a = [random.randint(-10, 10) for _ in range(n)]
        s = BloquesRaiz(a, random.choice([None, 1, 2, 3, 7, 50]))
        for _ in range(60):
            op = random.randint(0, 3)
            l = random.randint(0, n)
            r = random.randint(l, n)
            if op == 0:
                v = random.randint(-5, 5)
                s.sumar_rango(l, r, v)
                for i in range(l, r):
                    a[i] += v
            elif op == 1:
                i, v = random.randrange(n), random.randint(-20, 20)
                s.asignar(i, v)
                a[i] = v
            elif op == 2:
                assert s.suma(l, r) == sum(a[l:r])
            else:
                x = random.randint(-15, 15)
                assert s.contar_mayores(l, r, x) == sum(1 for v in a[l:r] if v > x)

    # N grande
    n = 50000
    a = [random.randint(0, 1000) for _ in range(n)]
    s = BloquesRaiz(a)
    total = sum(a)
    for _ in range(5000):
        l = random.randrange(n)
        r = random.randint(l, n)
        v = random.randint(-5, 5)
        s.sumar_rango(l, r, v)
        total += v * (r - l)
        s.contar_mayores(random.randrange(n), n, 500)
    assert s.suma(0, n) == total


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
