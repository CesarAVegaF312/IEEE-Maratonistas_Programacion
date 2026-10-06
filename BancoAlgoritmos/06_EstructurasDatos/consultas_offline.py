"""
Estructuras de datos — Consultas offline con Fenwick («Offline queries + BIT»)
Nivel: Intermedio
Ejecutar: python consultas_offline.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Cuando TODAS las consultas se conocen de antemano (se leen todas antes
    de responder), se pueden reordenar como convenga y procesarlas junto
    con los datos en un barrido, con un Fenwick que mantiene «lo que ya
    pasó». Así, preguntas que en línea necesitarían estructuras
    persistentes o árboles de mezcla salen con un BIT de 20 líneas.
    Dos ejemplos clásicos de este archivo:
      1. Número de valores DISTINTOS en a[l..r-1].
      2. Cuántos a[i] <= x hay en a[l..r-1].
    Señales en el enunciado: Q consultas de rango que NO dependen de las
    respuestas anteriores (no hay «last answer xor…»), sin
    actualizaciones intercaladas (o con ellas en orden de tiempo), N y Q
    hasta 10^5–5·10^5, preguntas de tipo «conteo con dos condiciones»
    (posición en rango Y valor <= x / día <= d).

FUNCIÓN
    distintos_en_rangos(a, consultas) -> list[int]
        consultas: lista de (l, r) semiabiertos; devuelve, en el ORDEN
        ORIGINAL, cuántos valores distintos hay en a[l:r].
    contar_menores_iguales(a, consultas) -> list[int]
        consultas: lista de (l, r, x); cuántos i en [l, r) con a[i] <= x.

IDEA Y ALGORITMO
    1. Distintos: ordenar las consultas por r (extremo derecho) y barrer
       las posiciones i = 0, 1, 2, … Para cada valor se mantiene marcada
       con +1 SOLO su ÚLTIMA aparición vista hasta ahora (al ver a[i] se
       desmarca su aparición anterior y se marca i). Cuando el barrido ya
       cubrió [0, r), cada valor presente en a[l:r] tiene su última
       aparición < r; y esa última aparición está en [l, r) si y solo si
       el valor aparece en a[l:r]. Luego la respuesta es la suma de marcas
       en [l, r): una consulta de rango del Fenwick.
    2. Menores o iguales: ordenar los elementos por valor y las consultas
       por x. Al procesar la consulta con umbral x, ya se activaron (+1 en
       su posición) todos los a[i] <= x y ninguno mayor; la respuesta es la
       suma en [l, r). Es «barrer en una dimensión (valor o tiempo) y
       consultar en la otra (posición)».
    Patrón general: de las dos condiciones de la consulta, una se convierte
    en el ORDEN del barrido y la otra en el índice del Fenwick. Por eso hay
    que responder fuera de orden y guardar cada respuesta en su índice
    original.
    El ingenuo recorre el rango por consulta: O(N·Q) ≈ 10^10.

MACROALGORITMO
    Distintos:
    1. Ordenar los índices de consulta por r.
    2. ultima = {} (valor → última posición marcada); BIT de tamaño N.
    3. puntero i = 0. Para cada consulta (l, r) en ese orden:
       a. Mientras i < r: si a[i] estaba en ultima, BIT[ultima] -= 1;
          BIT[i] += 1; ultima[a[i]] = i; i += 1.
       b. resp[id] = BIT.rango(l, r).
    4. Devolver resp en el orden original.

COMPLEJIDAD
    O((N + Q) log N) tiempo (más el ordenamiento), O(N + Q) memoria.
    En Python, N = Q = 2·10^5 en ~1 s.

EJEMPLO A MANO
    a = [1, 2, 1, 3, 2], consultas (0,3) (1,5) (2,4)
    por r: (0,3) r=3, (2,4) r=4, (1,5) r=5
      i=0 (1): marca 0          marcas: [1,0,0,0,0]
      i=1 (2): marca 1          marcas: [1,1,0,0,0]
      i=2 (1): desmarca 0, marca 2 → [0,1,1,0,0]
      (0,3): suma [0,3) = 2       (valores 1 y 2)
      i=3 (3): marca 3          → [0,1,1,1,0]
      (2,4): suma [2,4) = 2       (valores 1 y 3)
      i=4 (2): desmarca 1, marca 4 → [0,0,1,1,1]
      (1,5): suma [1,5) = 3       (valores 1, 3, 2)
    Respuestas en orden original: [2, 3, 2].

ERRORES TÍPICOS
    - Imprimir las respuestas en el orden procesado y no en el original.
    - Marcar la PRIMERA aparición con el barrido por r (debe ser la última;
      si se barre por l de derecha a izquierda, es la primera).
    - Usar esta técnica cuando las consultas son «forzadas en línea»
      (dependen de la respuesta anterior): ahí no se pueden reordenar.
    - En contar_menores_iguales, empates: activar los a[i] == x ANTES de
      responder la consulta x (orden por valor, luego consultas).

VARIANTES Y RELACIONADOS
    - Algoritmo de Mo (06_EstructurasDatos/algoritmo_mo.py): también offline,
      para cualquier función de rango que se pueda extender/encoger.
    - Con actualizaciones: tratar el tiempo como una dimensión más (CDQ /
      divide y vencerás offline) o barrer por tiempo.
    - Conteo de puntos en rectángulos: barrer por x, BIT por y, cada
      consulta como 4 prefijos (inclusión–exclusión) o 2 si es prefijo.
    - 06_EstructurasDatos/fenwick.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/I - Fair Workload Distribution (barrido por día,
      Fenwick por trabajador comprimido, consultas offline)
    - CSES «Distinct Values Queries»; SPOJ DQUERY «D-query».

VERIFICACIÓN
    - Pruebas (python consultas_offline.py): contra len(set(a[l:r])) y el
      conteo directo en 600 arreglos aleatorios con 40 consultas cada uno,
      más casos borde (rangos vacíos, todos iguales) y N = Q = 10^5.
"""
import random


class Fenwick:
    """BIT mínimo (copiado de 06_EstructurasDatos/fenwick.py): índices 0..n-1."""

    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)

    def sumar(self, i, d):
        i += 1
        while i <= self.n:
            self.t[i] += d
            i += i & -i

    def prefijo(self, i):           # a[0] + … + a[i-1]
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def rango(self, l, r):          # a[l] + … + a[r-1]
        return self.prefijo(r) - self.prefijo(l)


def distintos_en_rangos(a, consultas):
    """Cantidad de valores distintos en a[l:r] para cada (l, r), en orden original."""
    resp = [0] * len(consultas)
    bit = Fenwick(len(a))
    ultima = {}                     # valor -> posición donde está marcado (+1)
    i = 0
    for q in sorted(range(len(consultas)), key=lambda q: consultas[q][1]):
        l, r = consultas[q]
        while i < r:                # extender el barrido hasta cubrir [0, r)
            x = a[i]
            if x in ultima:
                bit.sumar(ultima[x], -1)   # solo la última aparición cuenta
            bit.sumar(i, 1)
            ultima[x] = i
            i += 1
        resp[q] = bit.rango(l, r) if l < r else 0
    return resp


def contar_menores_iguales(a, consultas):
    """Para cada (l, r, x): cuántos i en [l, r) cumplen a[i] <= x."""
    resp = [0] * len(consultas)
    bit = Fenwick(len(a))
    elems = sorted(range(len(a)), key=lambda i: a[i])   # posiciones por valor
    j = 0
    for q in sorted(range(len(consultas)), key=lambda q: consultas[q][2]):
        l, r, x = consultas[q]
        while j < len(elems) and a[elems[j]] <= x:      # activar todos los <= x
            bit.sumar(elems[j], 1)
            j += 1
        resp[q] = bit.rango(l, r) if l < r else 0
    return resp


def demo():
    a = [1, 2, 1, 3, 2]
    cons = [(0, 3), (1, 5), (2, 4)]
    print("a =", a, " consultas =", cons)
    print("distintos   =", distintos_en_rangos(a, cons))               # [2, 3, 2]
    cons2 = [(0, 5, 1), (1, 4, 2), (2, 5, 0)]
    print("consultas (l, r, x) =", cons2)
    print("a[i] <= x   =", contar_menores_iguales(a, cons2))            # [2, 2, 0]


def pruebas():
    random.seed(2026)

    # Casos borde
    assert distintos_en_rangos([], []) == []
    assert distintos_en_rangos([], [(0, 0)]) == [0]
    assert distintos_en_rangos([4, 4, 4], [(0, 3), (1, 1), (2, 3)]) == [1, 0, 1]
    assert contar_menores_iguales([5], [(0, 1, 5), (0, 1, 4), (0, 0, 9)]) == [1, 0, 0]

    for _ in range(600):
        n = random.randint(0, 25)
        a = [random.randint(0, 6) for _ in range(n)]
        cons, cons2 = [], []
        for _ in range(40):
            l = random.randint(0, n)
            r = random.randint(l, n)
            cons.append((l, r))
            cons2.append((l, r, random.randint(-1, 7)))
        assert distintos_en_rangos(a, cons) == [len(set(a[l:r])) for l, r in cons]
        assert contar_menores_iguales(a, cons2) == \
            [sum(1 for v in a[l:r] if v <= x) for l, r, x in cons2]

    # N = Q = 10^5 (solo tiempo y coherencia básica)
    n = 100000
    a = [random.randint(1, 1000) for _ in range(n)]
    cons = []
    for _ in range(n):
        l = random.randrange(n)
        cons.append((l, random.randint(l, n)))
    res = distintos_en_rangos(a, cons)
    assert all(0 <= d <= min(r - l, 1000) for d, (l, r) in zip(res, cons))
    assert distintos_en_rangos(a, [(0, n)]) == [len(set(a))]


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
