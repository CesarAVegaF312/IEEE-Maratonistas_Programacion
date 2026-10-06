r"""
Geometría — Precisión: epsilon, enteros, Fraction y redondeo de salida
Nivel: Básico
Ejecutar: python precision_flotantes.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Evitar el error más común en geometría: decidir mal una comparación
    porque 0.1 + 0.2 != 0.3. Este archivo reúne las cuatro defensas:
    (1) no usar floats (enteros exactos), (2) si no se puede, comparar con
    epsilon, (3) Fraction para cálculos racionales exactos, (4) imprimir
    bien (redondeo, truncamiento y el temido «-0.00»).
    Señales en el enunciado: coordenadas enteras (¡aprovecharlas!), «imprima
    con k decimales», «error absoluto o relativo de 10^-6», «trunque»,
    preguntas de sí/no sobre tangencias, colinealidad o igualdad.

FUNCIÓN
    signo(x, eps=EPS) -> int          −1, 0 o 1 tolerando |x| <= eps como 0
    casi_igual(a, b, eps=EPS) -> bool  |a − b| <= eps·max(1, |a|, |b|)
    mas_cerca(p, a, b) -> int          ¿p está más cerca de a (−1), de b (1)
                                       o a igual distancia (0)? Exacto
    interseccion_exacta(a, b, c, d) -> (Fraction, Fraction) | None
                                       intersección de las rectas ab y cd
    formatear(x, dec) -> str           redondeo a dec decimales sin «-0.00»
    truncar_fraccion(num, den, dec) -> str     num/den truncado, exacto
    redondear_fraccion(num, den, dec) -> str   num/den a dec decimales,
                                       mitades hacia afuera del 0, exacto
    es_cuadrado(n) -> bool             con math.isqrt (sin sqrt de floats)

IDEA Y ALGORITMO
    Un float (double) guarda ~15–16 cifras significativas en BINARIO: 0.1 no
    es representable, y cada operación agrega un error relativo ~1.1e-16.
    1) ENTEROS PRIMERO. Con coordenadas enteras, cruz, punto y distancias
       al cuadrado son exactos. Trucos: comparar d1 < d2 como d1² < d2²;
       dist <= (3/2)·d como 4·dist² <= 9·d²; r1 + r2 vs d como
       (r1 + r2)² vs d²; ángulos con cruz/punto en vez de atan2.
    2) EPSILON cuando hay raíces, divisiones o trigonometría. Se decide
       «x == 0» como |x| <= eps. ¿Qué eps? Si los datos son ~10^4 y se
       multiplican dos (productos ~10^8), el error absoluto es ~10^8·1e-16 =
       1e-8: un eps de 1e-9 sería demasiado chico y uno de 1e-3 confundiría
       valores distintos. Regla práctica: eps ~ 1e-9 para magnitudes ~1,
       escalarlo con la magnitud de lo que se compara (tolerancia RELATIVA,
       como en casi_igual), y siempre muy por debajo de la diferencia
       mínima posible entre dos respuestas distintas.
    3) FRACTION: aritmética racional exacta (numerador/denominador enteros).
       Sirve cuando la respuesta es racional (intersección de rectas con
       datos enteros, pendientes, promedios). Es ~10–50 veces más lenta que
       float: úsala con pocos miles de operaciones o para verificar.
    4) SALIDA. "%.2f" redondea el valor binario: 2.675 se guarda como
       2.67499999… y sale «2.67». Si la respuesta es num/den con enteros,
       redondear/truncar con aritmética entera es exacto. Además, −0.001
       con "%.2f" da «-0.00», que muchos jueces rechazan.
       Ojo: round(2.5) = 2 en Python (redondeo bancario, al par).

        recta real:   ... |----x----|----y----| ...
                            x − eps   x   x + eps
        «x == y» <=> y cae dentro de la ventana de ancho 2·eps

MACROALGORITMO
    1. ¿Los datos son enteros? Reformular las comparaciones para no dividir
       ni sacar raíz (elevar al cuadrado, multiplicar en cruz).
    2. ¿Hace falta dividir pero el resultado es racional? Fraction.
    3. ¿Hay raíces/trigonometría? floats + signo(x, eps) en TODA comparación.
    4. Elegir eps según la magnitud de los datos (ver arriba).
    5. Al imprimir: formatear (evita «-0.00») o, si es racional,
       redondear_fraccion / truncar_fraccion con enteros.

COMPLEJIDAD
    O(1) por operación con enteros/floats; Fraction cuesta O(log) por el
    gcd interno y es ~10–50 veces más lenta en la práctica.

EJEMPLO A MANO
    0.1 + 0.2 == 0.3 -> False;  casi_igual(0.1 + 0.2, 0.3) -> True.
    Rectas (0,0)-(3,1) y (0,2)-(2,0): se cortan en (3/2, 1/2) exacto.
    2.675 con "%.2f" -> 2.67 (!), redondear_fraccion(2675, 1000, 2) -> 2.68.
    formatear(-0.001, 2) -> "0.00" (no "-0.00").
    truncar_fraccion(15, 2, 1) -> "7.5";  truncar_fraccion(-7, 3, 2) -> "-2.33".

ERRORES TÍPICOS
    - Comparar floats con == (o con < cuando deberían ser iguales).
    - eps fijo de 1e-9 con coordenadas de 10^6 (productos de 10^12: el error
      ya es ~1e-4) -> tolerancia relativa o reformular con enteros.
    - int(x) para truncar un float que «debería» ser 3 pero vale
      2.9999999 -> da 2. Truncar con enteros o sumar eps antes.
    - Imprimir «-0.00».
    - math.sqrt(n) para decidir cuadrados perfectos con n grande: usar
      math.isqrt (exacto para cualquier entero).

VARIANTES Y RELACIONADOS
    - decimal.Decimal con contexto de precisión alta (más lenta).
    - Todos los archivos de 08_Geometria usan enteros donde se puede:
      orientacion_ccw.py, area_poligono.py, circulos.py (anillo exacto).
    - Búsqueda binaria sobre reales: iterar un número fijo de veces
      (00_Base/busqueda_binaria.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/D - Robot Arm (anillo comparando cuadrados enteros)
    - ICPC/Colombia 2026/C - Into the Onion (4·dist² <= 9·d², sin raíces)
    - ICPC/Colombia 2018/H - Ghost Hunting (truncar un área con enteros)
    - ICPC/OMP 2017 Murcia/H - Rogue One (truncar con división entera)
    - ICPC/Colombia 2026/F - Heist (tolerancias explícitas y «-0.00»)

VERIFICACIÓN
    - Pruebas: OK en 4000 casos aleatorios: truncar/redondear_fraccion
      contra decimal.Decimal (ROUND_DOWN / ROUND_HALF_UP con precisión
      alta), interseccion_exacta comprobando con Fraction que el punto está
      en ambas rectas, mas_cerca contra distancias con Fraction, es_cuadrado
      contra enumeración, y formatear nunca devuelve «-0» (python precision_flotantes.py)
"""
import math
import random
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP, localcontext
from fractions import Fraction

EPS = 1e-9


def signo(x, eps=EPS):
    """−1, 0 o 1, considerando 0 todo valor con |x| <= eps."""
    return 0 if abs(x) <= eps else (1 if x > 0 else -1)


def casi_igual(a, b, eps=EPS):
    """Igualdad con tolerancia mixta: absoluta cerca de 0, relativa lejos."""
    return abs(a - b) <= eps * max(1.0, abs(a), abs(b))


def mas_cerca(p, a, b):
    """−1 si p está más cerca de a, 1 si de b, 0 si equidista. Sin raíces."""
    da = (p[0] - a[0]) ** 2 + (p[1] - a[1]) ** 2
    db = (p[0] - b[0]) ** 2 + (p[1] - b[1]) ** 2
    return (da > db) - (da < db)


def interseccion_exacta(a, b, c, d):
    """Punto de corte de las rectas ab y cd como Fractions; None si paralelas.

    p = a + t(b − a) con t = (c − a)×(d − c) / (b − a)×(d − c): todo entero
    salvo la división final, que Fraction hace exacta.
    """
    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = d[0] - c[0], d[1] - c[1]
    den = rx * sy - ry * sx
    if den == 0:
        return None
    t = Fraction((c[0] - a[0]) * sy - (c[1] - a[1]) * sx, den)
    return (a[0] + t * rx, a[1] + t * ry)


def formatear(x, dec):
    """f"{x:.{dec}f}" pero sin «-0.00» cuando el valor redondeado es cero."""
    s = f"{x:.{dec}f}"
    if s.startswith("-") and float(s) == 0:
        s = s[1:]
    return s


def _a_texto(q, dec):
    """Entero q = valor·10^dec (con signo) -> texto con dec decimales."""
    neg = q < 0
    q = abs(q)
    ent, frac = divmod(q, 10 ** dec)
    s = str(ent) + ("." + str(frac).zfill(dec) if dec > 0 else "")
    return "-" + s if neg and q != 0 else s


def truncar_fraccion(num, den, dec):
    """num/den truncado (hacia 0) a dec decimales, con aritmética entera."""
    if den < 0:
        num, den = -num, -den
    q = abs(num) * 10 ** dec // den          # truncar el valor absoluto
    return _a_texto(-q if num < 0 else q, dec)


def redondear_fraccion(num, den, dec):
    """num/den redondeado a dec decimales; las mitades se alejan del 0."""
    if den < 0:
        num, den = -num, -den
    q = (2 * abs(num) * 10 ** dec + den) // (2 * den)   # floor(x + 1/2)
    return _a_texto(-q if num < 0 else q, dec)


def es_cuadrado(n):
    """¿n es cuadrado perfecto? math.isqrt es exacto para enteros grandes."""
    return n >= 0 and math.isqrt(n) ** 2 == n


def demo():
    print("0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3)
    print("casi_igual(0.1 + 0.2, 0.3) ->", casi_igual(0.1 + 0.2, 0.3))
    p = interseccion_exacta((0, 0), (3, 1), (0, 2), (2, 0))
    print("intersección exacta:", p[0], p[1])                  # 3/2 1/2
    print('"%.2f" % 2.675 ->', "%.2f" % 2.675)                 # 2.67 (!)
    print("redondear_fraccion(2675, 1000, 2) ->", redondear_fraccion(2675, 1000, 2))
    print("round(2.5) ->", round(2.5), " (redondeo bancario)")
    print('formatear(-0.001, 2) ->', formatear(-0.001, 2))
    print("truncar_fraccion(15, 2, 1) ->", truncar_fraccion(15, 2, 1))
    print("truncar_fraccion(-7, 3, 2) ->", truncar_fraccion(-7, 3, 2))
    print("es_cuadrado(10**30) ->", es_cuadrado(10 ** 30),
          " es_cuadrado(10**30 + 1) ->", es_cuadrado(10 ** 30 + 1))


def pruebas():
    random.seed(99)

    # Casos borde
    assert signo(1e-12) == 0 and signo(-1e-3) == -1 and signo(0.0) == 0
    assert casi_igual(1e12, 1e12 + 1e-1) and not casi_igual(1.0, 1.001)
    assert interseccion_exacta((0, 0), (1, 1), (0, 1), (1, 2)) is None
    assert formatear(-0.004, 2) == "0.00" and formatear(-0.005001, 2) == "-0.01"
    assert formatear(0.0, 0) == "0" and formatear(-0.4, 0) == "0"
    assert truncar_fraccion(0, 5, 3) == "0.000"
    assert truncar_fraccion(-1, 3, 0) == "0"           # −0.33 truncado = 0, sin «-»
    assert redondear_fraccion(5, 2, 0) == "3" and redondear_fraccion(-5, 2, 0) == "-3"
    assert es_cuadrado(0) and es_cuadrado(1) and not es_cuadrado(-4)
    assert es_cuadrado((10 ** 20 + 7) ** 2) and not es_cuadrado((10 ** 20 + 7) ** 2 - 1)

    with localcontext() as ctx:
        ctx.prec = 80
        for _ in range(4000):
            num = random.randint(-10 ** 6, 10 ** 6)
            den = random.choice([1, 2, 3, 4, 7, 8, 10, 1000, random.randint(1, 10 ** 6)])
            if random.random() < 0.3:
                den = -den
            dec = random.randint(0, 6)
            # Fuerza bruta: Decimal con mucha precisión y su modo de redondeo
            exacto = Decimal(num) / Decimal(den)
            paso = Decimal(1).scaleb(-dec)
            t = exacto.quantize(paso, rounding=ROUND_DOWN)
            r = exacto.quantize(paso, rounding=ROUND_HALF_UP)
            t_s, r_s = format(t, "f"), format(r, "f")
            if Decimal(t_s) == 0:
                t_s = t_s.lstrip("-")
            if Decimal(r_s) == 0:
                r_s = r_s.lstrip("-")
            assert truncar_fraccion(num, den, dec) == t_s, (num, den, dec)
            assert redondear_fraccion(num, den, dec) == r_s, (num, den, dec)

            # formatear nunca deja «-0.000…»
            x = random.uniform(-1, 1) * 10 ** random.randint(-8, 3)
            s = formatear(x, dec)
            assert not (s.startswith("-") and float(s) == 0)
            assert abs(float(s) - x) <= 0.5 * 10 ** -dec + 1e-9

            # Intersección exacta: el punto está en ambas rectas (cruz == 0)
            a, b, c, d = [(random.randint(-9, 9), random.randint(-9, 9)) for _ in range(4)]
            if a == b or c == d:
                continue
            p = interseccion_exacta(a, b, c, d)
            par = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0]) == 0
            assert (p is None) == par
            if p is not None:
                for u, v in ((a, b), (c, d)):
                    assert (v[0] - u[0]) * (p[1] - u[1]) - (v[1] - u[1]) * (p[0] - u[0]) == 0

            # mas_cerca contra distancias con Fraction (y raíz «de verdad»)
            q = (random.randint(-9, 9), random.randint(-9, 9))
            da = Fraction((q[0] - a[0]) ** 2 + (q[1] - a[1]) ** 2)
            db = Fraction((q[0] - b[0]) ** 2 + (q[1] - b[1]) ** 2)
            esperado = 0 if da == db else (-1 if da < db else 1)
            assert mas_cerca(q, a, b) == esperado

    for n in range(0, 3000):
        assert es_cuadrado(n) == any(k * k == n for k in range(0, 60))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
