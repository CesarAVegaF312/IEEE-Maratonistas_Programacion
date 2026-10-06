"""
Base — Ordenamiento con clave compuesta («Custom sort / sort by key»)
Nivel: Básico
Ejecutar: python ordenamiento_clave_compuesta.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Ordenar registros por varios criterios con desempates: «ordenar por
    puntos de mayor a menor; si empatan, por diferencia de goles; si siguen
    empatados, por nombre alfabéticamente». Es la mitad de muchos problemas
    de simulación (tablas de posiciones, rankings, horarios).
    Señales en el enunciado: «en caso de empate…», «ordenados por X y luego
    por Y», «de mayor a menor», «en orden lexicográfico», «si hay varias
    respuestas imprima la menor».

FUNCIÓN
    tabla_posiciones(equipos) -> list
        equipos: tuplas (nombre, puntos, diferencia, goles_favor).
        Orden: puntos ↓, diferencia ↓, goles ↓, nombre ↑.
    ordenar_texto_desc_numero_asc(registros) -> list
        registros: tuplas (texto, número). Orden: texto ↓ y número ↑
        (no se puede «negar» un texto: se usan dos ordenamientos estables).
    mayor_concatenacion(nums) -> str
        Mayor número formado concatenando todos los nums (cmp_to_key).
    ordenar_fracciones(fracs) -> list
        fracs: tuplas (p, q) con q > 0, de menor a mayor valor p/q, exacto
        (sin flotantes); en empate de valor, la de menor q primero.

IDEA Y ALGORITMO
    Python compara tuplas LEXICOGRÁFICAMENTE: primero el primer componente,
    si empatan el segundo, etc. Por eso basta que la clave sea la tupla de
    criterios en orden de prioridad:  key=lambda e: (-e.puntos, e.nombre).
    - Descendente en un campo numérico: negarlo (-x). sort es ascendente,
      y a < b  <=>  -a > -b.
    - Descendente en un campo que no se puede negar (texto) mezclado con
      otro ascendente: aprovechar la ESTABILIDAD. sort de Python (Timsort)
      es estable: si dos elementos tienen claves iguales, conservan su
      orden relativo. Entonces se ordena primero por el criterio MENOS
      importante y luego por el MÁS importante: en los empates del segundo
      orden queda el orden del primero.
    - Cuando el orden no sale de una clave sino de comparar PARES (p. ej.
      «a va antes que b si a+b > b+a» al concatenar), se escribe una función
      cmp(a, b) que devuelve negativo / 0 / positivo y se usa
      functools.cmp_to_key. Debe ser un orden total consistente (transitivo);
      si no, el resultado no tiene sentido.
    Por qué funciona la concatenación: la relación «a+b > b+a» es transitiva
    (equivale a comparar a/(10^|a|-1) con b/(10^|b|-1)), y un argumento de
    intercambio muestra que en el óptimo ningún par adyacente está «al
    revés».

MACROALGORITMO
    1. Listar los criterios en orden de prioridad (el del enunciado).
    2. Para cada criterio decidir ascendente o descendente.
    3. Si todos los descendentes son numéricos: key = tupla con esos negados.
    4. Si hay un descendente no numérico: ordenar por los criterios del
       menos al más importante, cada uno con su reverse (estabilidad).
    5. Si el orden se define comparando pares: cmp(a, b) + cmp_to_key.
    6. Comprobar a mano con el ejemplo del enunciado, sobre todo los empates.

COMPLEJIDAD
    O(N log N) comparaciones; cada comparación de tuplas cuesta O(#criterios).
    key se evalúa UNA vez por elemento; cmp_to_key llama cmp O(N log N) veces
    en Python (≈ 5–10 veces más lento). 10^6 elementos con key en ~1–2 s.

EJEMPLO A MANO
    Equipos (nombre, pts, dif, gf):
      ("Rojo", 6, 2, 5), ("Azul", 6, 2, 5), ("Verde", 6, 3, 4), ("Gris", 4, 5, 9)
    claves (-pts, -dif, -gf, nombre):
      Rojo  (-6, -2, -5, "Rojo")      Azul (-6, -2, -5, "Azul")
      Verde (-6, -3, -4, "Verde")     Gris (-4, -5, -9, "Gris")
    → Verde (más diferencia), Azul, Rojo (empate total: alfabético), Gris.
    mayor_concatenacion([3, 30, 34, 5, 9]) = "9534330"  ("3"+"30" > "30"+"3").

ERRORES TÍPICOS
    - Escribir reverse=True para TODO cuando solo un criterio es descendente.
    - Hacer dos sorts en el orden equivocado (el MÁS importante va al final).
    - Comparar números leídos como texto: "10" < "9" en orden de cadenas.
    - Mayúsculas: "Zeta" < "alfa" en ASCII; si piden ignorar mayúsculas,
      clave s.lower() (y otro desempate si el enunciado no lo define).
    - cmp que devuelve bool (True/False) en vez de -1/0/1: cmp_to_key lo
      interpreta mal (False = 0 = «iguales»).

VARIANTES Y RELACIONADOS
    - sorted(…, key=…) devuelve copia; lista.sort(key=…) ordena en su lugar.
    - Índices ordenados: sorted(range(n), key=lambda i: (a[i], i)).
    - operator.itemgetter(1, 0) como key: más rápido que lambda.
    - Comparar fracciones exactas: p1*q2 < p2*q1 (o fractions.Fraction).
    - Relacionados: simulacion.py (tablas de posiciones), argumento de
      intercambio en voraces.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/K - Soccer Championship (simulación + clave compuesta)
    - ICPC/Colombia 2018/A - All-star Three-point Contest (-puntos, nombre.lower())
    - UVa 10194 «Football (aka Soccer)»; UVa 10905 «Children's Game»
      (concatenación con cmp)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (ordenamiento por selección con una
      comparación escrita criterio por criterio, y todas las permutaciones
      para la concatenación) en 2100 casos aleatorios + casos borde
      (python ordenamiento_clave_compuesta.py)
"""
import itertools
import random
from fractions import Fraction
from functools import cmp_to_key


def tabla_posiciones(equipos):
    """Ordena (nombre, puntos, diferencia, goles): pts ↓, dif ↓, goles ↓, nombre ↑."""
    # Los numéricos descendentes se niegan; el nombre va tal cual (ascendente).
    return sorted(equipos, key=lambda e: (-e[1], -e[2], -e[3], e[0]))


def ordenar_texto_desc_numero_asc(registros):
    """Ordena (texto, número) por texto descendente y, en empate, número ascendente.

    No se puede negar un texto, así que se usan DOS sorts estables: primero
    el criterio menos importante (número ↑) y luego el más importante
    (texto ↓). En los empates de texto se conserva el orden por número.
    """
    r = sorted(registros, key=lambda e: e[1])          # criterio secundario
    r.sort(key=lambda e: e[0], reverse=True)           # criterio principal
    return r
    # Nota: reverse=True también es estable (no invierte los empates).


def mayor_concatenacion(nums):
    """Mayor número que se forma concatenando todos los enteros de nums."""
    def cmp(a, b):
        # a va antes que b si a+b forma un número mayor que b+a
        if a + b > b + a:
            return -1
        if a + b < b + a:
            return 1
        return 0
    s = sorted(map(str, nums), key=cmp_to_key(cmp))
    r = "".join(s)
    return "0" if r and r[0] == "0" else r    # [0, 0] -> "0", no "00"


def ordenar_fracciones(fracs):
    """Ordena (p, q), q > 0, por valor p/q ascendente; empate: q menor primero."""
    def cmp(x, y):
        # p1/q1 < p2/q2  <=>  p1*q2 < p2*q1   (q > 0: no cambia el signo)
        d = x[0] * y[1] - y[0] * x[1]
        if d != 0:
            return -1 if d < 0 else 1
        return x[1] - y[1]                      # desempate explícito
    return sorted(fracs, key=cmp_to_key(cmp))


def demo():
    equipos = [("Rojo", 6, 2, 5), ("Azul", 6, 2, 5), ("Verde", 6, 3, 4), ("Gris", 4, 5, 9)]
    print("tabla:", [e[0] for e in tabla_posiciones(equipos)])   # Verde Azul Rojo Gris
    regs = [("b", 3), ("a", 1), ("b", 1), ("c", 2), ("a", 0)]
    print("texto ↓ número ↑:", ordenar_texto_desc_numero_asc(regs))
    print("mayor_concatenacion([3, 30, 34, 5, 9]) =", mayor_concatenacion([3, 30, 34, 5, 9]))
    print("fracciones:", ordenar_fracciones([(1, 2), (1, 3), (2, 4), (-1, 5)]))


# ---------- fuerza bruta: selección con comparación explícita ----------

def _seleccion(lista, va_antes):
    """Ordenamiento por selección: en cada paso extrae el que va primero."""
    resto = list(lista)
    salida = []
    while resto:
        mejor = 0
        for i in range(1, len(resto)):
            if va_antes(resto[i], resto[mejor]):
                mejor = i
        salida.append(resto.pop(mejor))
    return salida


def _antes_tabla(x, y):
    if x[1] != y[1]:
        return x[1] > y[1]          # más puntos primero
    if x[2] != y[2]:
        return x[2] > y[2]          # más diferencia primero
    if x[3] != y[3]:
        return x[3] > y[3]          # más goles primero
    return x[0] < y[0]              # nombre alfabético


def _antes_texto(x, y):
    if x[0] != y[0]:
        return x[0] > y[0]
    return x[1] < y[1]


def pruebas():
    random.seed(2024)

    # Casos borde
    assert tabla_posiciones([]) == []
    assert ordenar_texto_desc_numero_asc([]) == []
    assert mayor_concatenacion([0, 0, 0]) == "0"
    assert mayor_concatenacion([10, 2]) == "210"
    assert mayor_concatenacion([3, 30, 34, 5, 9]) == "9534330"
    assert ordenar_fracciones([(1, 2), (2, 4)]) == [(1, 2), (2, 4)]

    # Estabilidad: claves iguales conservan el orden de entrada
    datos = [(random.randint(0, 3), i) for i in range(200)]
    s = sorted(datos, key=lambda e: e[0])
    for a, b in zip(s, s[1:]):
        assert a[0] < b[0] or (a[0] == b[0] and a[1] < b[1])

    nombres = ["Ana", "ana", "Beto", "Zoe", "al", "b", "B", "zz"]
    for _ in range(1000):
        n = random.randint(0, 8)
        eq = [(random.choice(nombres) + str(i), random.randint(0, 3), random.randint(-2, 2),
               random.randint(0, 2)) for i in range(n)]
        # nombres únicos (i al final) para que el orden sea total
        assert tabla_posiciones(eq) == _seleccion(eq, _antes_tabla)

        regs = [(random.choice(nombres), random.randint(0, 3)) for _ in range(n)]
        # (registros repetidos son tuplas idénticas: no importa cuál va primero)
        assert ordenar_texto_desc_numero_asc(regs) == _seleccion(regs, _antes_texto)

        fr = [(random.randint(-5, 5), random.randint(1, 5)) for _ in range(n)]
        esperado = sorted(fr, key=lambda f: (Fraction(f[0], f[1]), f[1]))
        assert ordenar_fracciones(fr) == esperado

    # Concatenación contra todas las permutaciones
    for _ in range(1100):
        n = random.randint(1, 5)
        nums = [random.choice([0, 1, 9, 10, 12, 121, 3, 30, 34, 5, 98, 100]) for _ in range(n)]
        mejor = max(int("".join(map(str, p))) for p in itertools.permutations(nums))
        assert mayor_concatenacion(nums) == str(mejor)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
