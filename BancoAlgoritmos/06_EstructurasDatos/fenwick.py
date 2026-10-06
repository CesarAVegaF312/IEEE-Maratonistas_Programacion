"""
Estructuras de datos — Árbol de Fenwick («Fenwick tree / Binary Indexed Tree, BIT»)
Nivel: Intermedio
Ejecutar: python fenwick.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Mantener un arreglo que cambia con dos operaciones en O(log N):
    «sumar delta a la posición i» y «suma de los primeros i elementos»
    (y por resta, la suma de cualquier rango). Es más corto y rápido que un
    segment tree cuando solo se necesitan sumas.
    Usos típicos: conteo de inversiones, «cuántos valores <= x he visto»,
    k-ésimo elemento de un multiconjunto dinámico, consultas offline.
    Señales en el enunciado: N y Q hasta 10^5–10^6, actualizaciones
    puntuales mezcladas con sumas de rango; «cuántos pares i < j con
    a[i] > a[j]»; «posición del k-ésimo que sigue vivo».

FUNCIÓN
    class Fenwick(n | lista)      índices de 0 a n-1 (internamente 1..n)
        sumar(i, delta)           a[i] += delta
        prefijo(i) -> int         a[0] + … + a[i-1]   (i en 0..n; semiabierto)
        rango(l, r) -> int        a[l] + … + a[r-1]
        k_esimo(k) -> int         menor i con a[0] + … + a[i] >= k
                                  (exige a[j] >= 0; n si no existe)
    contar_inversiones(a) -> int  pares i < j con a[i] > a[j]

IDEA Y ALGORITMO
    La celda t[i] (1-indexada) guarda la suma de los elementos del bloque
    (i - lowbit(i), i], donde lowbit(i) = i & -i es el bit encendido más
    bajo. Ejemplo: t[12] (1100b) cubre (8, 12]; t[8] cubre (0, 8].
    - prefijo(i): la suma (0, i] se parte en bloques quitando el bit más
      bajo cada vez: (0,13] = t[13] + t[12] + t[8]. A lo sumo log N
      bloques.
    - sumar(i): las celdas cuyo bloque contiene a i son i, i + lowbit(i),
      … (sumar el bit más bajo sube al siguiente bloque que lo contiene).
    - k_esimo(k): descenso binario. Se prueba avanzar pos en saltos 2^b de
      mayor a menor: si t[pos + 2^b] < k, ese bloque entero queda a la
      izquierda de la respuesta (k -= t[…], pos += 2^b). Es la búsqueda
      binaria sobre prefijos, pero en O(log N) en lugar de O(log² N).
    - Construcción en O(N): t[i] += a[i]; t[i + lowbit(i)] += t[i].
    - Inversiones: recorrer de izquierda a derecha; las inversiones que
      terminan en j son los vistos con valor > a[j] = vistos - (vistos con
      valor <= a[j]). Los valores se COMPRIMEN a rangos 1..K para que el
      BIT tenga tamaño <= N sin importar lo grandes que sean.
    El ingenuo (recalcular sumas) es O(N) por consulta; las sumas prefijas
    fijas son O(1) pero cada actualización cuesta O(N).

MACROALGORITMO
    sumar(i, d):  i += 1; mientras i <= n: t[i] += d; i += i & -i.
    prefijo(i):   s = 0; mientras i > 0: s += t[i]; i -= i & -i.
    k_esimo(k):   pos = 0; para b de log n hacia 0: si pos + 2^b <= n y
                  t[pos + 2^b] < k: pos += 2^b; k -= t[pos].  Devolver pos.
    Inversiones:  comprimir; para cada x: inv += vistos - prefijo(rango(x)+1);
                  sumar(rango(x), 1).

COMPLEJIDAD
    sumar, prefijo, rango, k_esimo: O(log N). Construcción O(N).
    Memoria O(N). En Python ~10^6 operaciones (sumar+prefijo) en ~1–2 s;
    contar_inversiones con N = 10^5 en ~0,3 s.

EJEMPLO A MANO
    a = [5, 2, 0, 3, 1] → t (1..5) = [5, 7, 0, 10, 1]
      prefijo(4) = t[4] = 10;  prefijo(5) = t[5] + t[4] = 11
      sumar(2, 4): t[3] += 4, t[4] += 4  → a = [5, 2, 4, 3, 1]
      rango(1, 4) = prefijo(4) - prefijo(1) = 14 - 5 = 9  (2 + 4 + 3)
      k_esimo(8): prefijos 5, 7, 11 → índice 2.
    Inversiones de [3, 1, 2]: (3,1), (3,2) → 2.

ERRORES TÍPICOS
    - Mezclar índices 0 y 1: el BIT es 1-indexado por dentro (i = 0 haría
      un ciclo infinito porque 0 & -0 = 0).
    - prefijo inclusivo vs exclusivo: decidir una convención y no cambiarla.
    - k_esimo con valores negativos: los prefijos dejan de ser monótonos y
      el descenso binario no sirve.
    - No comprimir coordenadas con valores grandes o negativos.
    - «Asignar» a[i] = v: hay que sumar v - a[i] (guardar el arreglo aparte).

VARIANTES Y RELACIONADOS
    - Actualización de rango + consulta puntual: BIT sobre las diferencias
      (sumar(l, d), sumar(r, -d); el valor en i es prefijo(i+1)).
    - Rango + rango: dos BIT. BIT 2D para rejillas.
    - Mínimo/máximo con actualizaciones que solo mejoran (BIT de máximos).
    - 06_EstructurasDatos/segment_tree.py (operaciones más generales),
      06_EstructurasDatos/consultas_offline.py (BIT + orden de consultas).

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/K - Skyline (conteo de inversiones con Fenwick)
    - ICPC/Colombia 2026/I - Fair Workload Distribution (Fenwick con
      consultas offline y compresión)
    - CSES «Dynamic Range Sum Queries»; CSES «List Removals» (k-ésimo);
      CSES «Range Update Queries» (diferencias).

VERIFICACIÓN
    - Pruebas (python fenwick.py): contra un arreglo simple en 300
      secuencias aleatorias de 80 operaciones (sumar, prefijo, rango,
      k_esimo contra búsqueda lineal); contar_inversiones contra O(N²) en
      1000 casos con repetidos y negativos; casos borde y N = 10^5.
"""
import random
from bisect import bisect_left


class Fenwick:
    """Sumas de prefijo con actualización puntual. Índices externos 0..n-1."""

    def __init__(self, n_o_lista):
        if isinstance(n_o_lista, int):
            self.n = n_o_lista
            self.t = [0] * (self.n + 1)
        else:
            # Construcción O(N): cada celda empuja su suma a su «padre».
            self.n = len(n_o_lista)
            self.t = [0] + list(n_o_lista)
            for i in range(1, self.n + 1):
                j = i + (i & -i)
                if j <= self.n:
                    self.t[j] += self.t[i]

    def sumar(self, i, delta):
        """a[i] += delta."""
        i += 1
        t, n = self.t, self.n
        while i <= n:
            t[i] += delta
            i += i & -i            # siguiente bloque que contiene a i

    def prefijo(self, i):
        """a[0] + … + a[i-1]."""
        s, t = 0, self.t
        while i > 0:
            s += t[i]
            i -= i & -i            # quitar el bloque (i - lowbit, i]
        return s

    def rango(self, l, r):
        """a[l] + … + a[r-1]."""
        return self.prefijo(r) - self.prefijo(l)

    def k_esimo(self, k):
        """Menor i con a[0] + … + a[i] >= k (valores >= 0); n si no existe."""
        pos, t = 0, self.t
        paso = 1 << self.n.bit_length()
        while paso:
            sig = pos + paso
            if sig <= self.n and t[sig] < k:
                pos = sig          # todo (0, sig] queda antes de la respuesta
                k -= t[sig]
            paso >>= 1
        return pos                 # 1-indexado pos+1 → 0-indexado pos


def contar_inversiones(a):
    """Número de pares i < j con a[i] > a[j], en O(N log N)."""
    valores = sorted(set(a))                     # compresión de coordenadas
    bit = Fenwick(len(valores))
    inv = 0
    for vistos, x in enumerate(a):
        r = bisect_left(valores, x)              # rango 0-indexado de x
        inv += vistos - bit.prefijo(r + 1)       # vistos con valor > x
        bit.sumar(r, 1)
    return inv


def demo():
    a = [5, 2, 0, 3, 1]
    f = Fenwick(a)
    print("a =", a, " t =", f.t[1:])                       # [5, 7, 0, 10, 1]
    print("prefijo(4) =", f.prefijo(4))                    # 10
    f.sumar(2, 4)
    print("tras sumar(2, 4): rango(1, 4) =", f.rango(1, 4))  # 9
    print("k_esimo(8) =", f.k_esimo(8))                    # 2
    print("inversiones de [3, 1, 2] =", contar_inversiones([3, 1, 2]))   # 2


def pruebas():
    random.seed(1994)

    # Casos borde
    f = Fenwick(0)
    assert f.prefijo(0) == 0 and f.k_esimo(1) == 0
    f = Fenwick(1)
    f.sumar(0, 7)
    assert f.prefijo(1) == 7 and f.k_esimo(7) == 0 and f.k_esimo(8) == 1
    assert contar_inversiones([]) == 0 and contar_inversiones([4]) == 0
    assert contar_inversiones([2, 2, 2]) == 0
    assert contar_inversiones([3, 2, 1]) == 3

    # Operaciones aleatorias contra un arreglo simple
    for _ in range(300):
        n = random.randint(1, 20)
        a = [random.randint(0, 5) for _ in range(n)]
        if random.random() < 0.5:
            f = Fenwick(a)                  # construcción O(N)
        else:
            f = Fenwick(n)                  # vacío y cargado con sumar
            for i, x in enumerate(a):
                f.sumar(i, x)
        for _ in range(80):
            op = random.randint(0, 3)
            if op == 0:
                i = random.randrange(n)
                d = random.randint(-a[i], 6)          # mantiene a[i] >= 0
                a[i] += d
                f.sumar(i, d)
            elif op == 1:
                i = random.randint(0, n)
                assert f.prefijo(i) == sum(a[:i])
            elif op == 2:
                l = random.randint(0, n)
                r = random.randint(l, n)
                assert f.rango(l, r) == sum(a[l:r])
            else:
                k = random.randint(1, sum(a) + 2)
                acum, esperado = 0, n
                for i in range(n):
                    acum += a[i]
                    if acum >= k:
                        esperado = i
                        break
                assert f.k_esimo(k) == esperado

    # Inversiones contra O(N²)
    for _ in range(1000):
        a = [random.randint(-5, 5) for _ in range(random.randint(0, 30))]
        bruta = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])
        assert contar_inversiones(a) == bruta

    # N grande: permutación invertida tiene N(N-1)/2 inversiones
    n = 100000
    assert contar_inversiones(list(range(n, 0, -1))) == n * (n - 1) // 2


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
