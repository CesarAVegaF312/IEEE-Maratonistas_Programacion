"""
Geometría — Vectores, producto punto y producto cruz («dot / cross product»)
Nivel: Básico
Ejecutar: python vectores_productos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Es el «alfabeto» de toda la geometría computacional: casi cualquier
    pregunta (¿gira a la izquierda?, ¿son perpendiculares?, ¿qué ángulo
    forman?, ¿qué área tiene?, ¿dónde cae la proyección?) se responde con
    sumas, restas, producto punto y producto cruz de vectores 2D.
    Señales en el enunciado: puntos con coordenadas, «ángulo», «girar»,
    «perpendicular», «paralelo», «a la izquierda/derecha», «área».

FUNCIÓN
    Puntos y vectores son tuplas (x, y) (enteros siempre que se pueda).
    suma(a, b), resta(a, b), escalar(a, k)  -> vector
    punto(a, b) -> número        a·b = ax·bx + ay·by
    cruz(a, b)  -> número        a×b = ax·by − ay·bx   (componente z del 3D)
    norma2(a) -> número (exacto con enteros);  norma(a) -> float
    angulo(a) -> float           ángulo polar de a en (−π, π] (atan2)
    angulo_entre(a, b) -> float  ángulo CON SIGNO de a hacia b, en (−π, π]
    rotar(a, theta) -> (float, float)   rotación antihoraria theta radianes
    rotar90(a) -> vector         rotación exacta de +90°: (−y, x)

IDEA Y ALGORITMO
    Producto punto: a·b = |a||b| cos θ.  Dice si el ángulo es agudo (> 0),
    recto (= 0) u obtuso (< 0), y a·b/|b| es la longitud de la sombra
    (proyección) de a sobre b.
    Producto cruz: a×b = |a||b| sen θ (θ medido de a hacia b, antihorario).
    Su signo dice si b está a la IZQUIERDA (> 0) o a la DERECHA (< 0) de a, y
    |a×b| es el área del paralelogramo que forman (el doble del triángulo).

              b                      a×b > 0  (b a la izquierda de a)
             /                       a×b = 0  (paralelos / colineales)
            /  θ                     a×b < 0  (b a la derecha de a)
           o-------> a

    De dónde salen: si a = |a|(cos α, sen α) y b = |b|(cos β, sen β),
        a·b = |a||b|(cos α cos β + sen α sen β) = |a||b| cos(β − α)
        a×b = |a||b|(cos α sen β − sen α cos β) = |a||b| sen(β − α).
    Por eso el ángulo con signo de a a b es atan2(a×b, a·b): atan2 recibe
    (seno, coseno) escalados por el mismo factor positivo |a||b| y devuelve
    el ángulo correcto en los cuatro cuadrantes. Es MÁS ESTABLE que
    acos(a·b / (|a||b|)), que pierde precisión cerca de 0 y π y además
    puede recibir 1.0000000002 y lanzar error de dominio.
    Rotación por θ: (x cos θ − y sen θ, x sen θ + y cos θ), que es multiplicar
    por el número complejo e^{iθ}. Para 90° es exacta: (x, y) -> (−y, x).
    Con coordenadas enteras, punto, cruz y norma2 son EXACTOS: compara
    distancias con norma2 (sin raíz) y decide giros con el signo de cruz.

MACROALGORITMO
    1. Representar cada punto/vector como tupla (x, y).
    2. Vector de P a Q: resta(Q, P).
    3. ¿Ángulo agudo/recto/obtuso?  signo de punto.
    4. ¿Izquierda/derecha/paralelo?  signo de cruz.
    5. ¿Ángulo exacto?  atan2(cruz, punto).
    6. ¿Distancias?  comparar norma2; sacar raíz solo al imprimir.

COMPLEJIDAD
    O(1) cada operación, memoria O(1). Millones por segundo en Python
    (si se escriben en línea, sin llamar funciones, aún más rápido).

EJEMPLO A MANO
    a = (3, 1), b = (1, 2):
      a·b = 3·1 + 1·2 = 5,  a×b = 3·2 − 1·1 = 5 > 0  (b está a la izquierda)
      |a| = √10, |b| = √5  ->  cos θ = 5/√50 = 1/√2  ->  θ = 45°
      atan2(5, 5) = 45°.  rotar90(a) = (−1, 3), y a·rotar90(a) = 0.

ERRORES TÍPICOS
    - Usar acos para el ángulo entre vectores (error de dominio por
      redondeo); usar atan2(cruz, punto).
    - atan2(y, x): el PRIMER argumento es y. atan2(x, y) da otro ángulo.
    - Confundir el orden: a×b = −(b×a). El signo depende del orden.
    - Comparar distancias con sqrt y floats cuando las coordenadas son
      enteras: usar norma2 (exacto).
    - Rotar en grados sin convertir: math.radians(grados).

VARIANTES Y RELACIONADOS
    - cruz(o, a, b) = (a − o)×(b − o): orientación de tres puntos
      (orientacion_ccw.py).
    - Área de polígonos con sumas de cruces (area_poligono.py).
    - Proyecciones y distancias a rectas (proyeccion_distancias.py).
    - Ordenar por ángulo polar sin floats: por semiplano y luego por cruz
      (ver _comparar_angulo en semiplanos.py).
    - Alternativa: usar complex de Python (z = x + yj): z1 * z2.conjugate()
      tiene parte real = punto y parte imaginaria = −cruz; rotar = z * e^{iθ}.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/F - Fish (proyecciones con producto punto)
    - ICPC/Colombia 2018/H - Ghost Hunting (áreas con producto cruz)
    - Es la base de todos los demás archivos de 08_Geometria.

VERIFICACIÓN
    - Pruebas: OK en 3000 pares aleatorios contra las definiciones
      trigonométricas (|a||b|cos θ, |a||b|sen θ con θ de atan2 por separado),
      propiedades algebraicas exactas (antisimetría, bilinealidad,
      a·b² + a×b² = |a|²|b|²) y rotaciones (preservan norma y ángulo)
      (python vectores_productos.py)
"""
import math
import random


def suma(a, b):
    return (a[0] + b[0], a[1] + b[1])


def resta(a, b):
    """Vector que va de b hacia a (a − b)."""
    return (a[0] - b[0], a[1] - b[1])


def escalar(a, k):
    return (a[0] * k, a[1] * k)


def punto(a, b):
    """Producto punto: |a||b|cos θ. > 0 agudo, = 0 perpendicular, < 0 obtuso."""
    return a[0] * b[0] + a[1] * b[1]


def cruz(a, b):
    """Producto cruz: |a||b|sen θ. > 0 si b está a la izquierda de a."""
    return a[0] * b[1] - a[1] * b[0]


def norma2(a):
    """Longitud al cuadrado (exacta con enteros)."""
    return a[0] * a[0] + a[1] * a[1]


def norma(a):
    return math.hypot(a[0], a[1])


def angulo(a):
    """Ángulo polar de a en (−π, π]. atan2 recibe (y, x), en ese orden."""
    return math.atan2(a[1], a[0])


def angulo_entre(a, b):
    """Ángulo con signo para girar a hasta b, en (−π, π].

    atan2(sen, cos) con sen y cos escalados por |a||b| > 0: estable y sin
    errores de dominio (a diferencia de acos).
    """
    return math.atan2(cruz(a, b), punto(a, b))


def rotar(a, theta):
    """Rota a en sentido antihorario theta radianes (resultado en floats)."""
    c, s = math.cos(theta), math.sin(theta)
    return (a[0] * c - a[1] * s, a[0] * s + a[1] * c)


def rotar90(a):
    """Rotación exacta de +90° (antihoraria): (x, y) -> (−y, x)."""
    return (-a[1], a[0])


def demo():
    a, b = (3, 1), (1, 2)
    print("a =", a, " b =", b)
    print("a + b =", suma(a, b), " a - b =", resta(a, b))
    print("punto(a, b) =", punto(a, b))                       # 5
    print("cruz(a, b)  =", cruz(a, b), "(> 0: b a la izquierda de a)")  # 5
    print("ángulo entre a y b = %.1f°" % math.degrees(angulo_entre(a, b)))  # 45.0
    print("ángulo entre b y a = %.1f°" % math.degrees(angulo_entre(b, a)))  # -45.0
    print("rotar90(a) =", rotar90(a), " punto con a:", punto(a, rotar90(a)))
    x, y = rotar(a, math.radians(90))
    print("rotar(a, 90°) = (%.6f, %.6f)" % (x, y))


def pruebas():
    random.seed(2024)
    cerca = math.isclose

    # Casos borde
    assert cruz((1, 0), (0, 1)) == 1 and cruz((0, 1), (1, 0)) == -1
    assert punto((1, 0), (0, 1)) == 0
    assert cruz((2, 4), (1, 2)) == 0                       # paralelos
    assert angulo_entre((1, 0), (-1, 0)) == math.pi        # 180° exacto
    assert angulo_entre((1, 0), (1, 0)) == 0.0
    assert angulo((0, -1)) == -math.pi / 2
    assert norma2((3, 4)) == 25 and norma((3, 4)) == 5.0
    assert rotar90(rotar90(rotar90(rotar90((7, -3))))) == (7, -3)

    for _ in range(3000):
        a = (random.randint(-50, 50), random.randint(-50, 50))
        b = (random.randint(-50, 50), random.randint(-50, 50))
        c = (random.randint(-50, 50), random.randint(-50, 50))
        k = random.randint(-5, 5)

        # Propiedades algebraicas exactas (enteros)
        assert cruz(a, b) == -cruz(b, a) and punto(a, b) == punto(b, a)
        assert cruz(a, suma(b, c)) == cruz(a, b) + cruz(a, c)
        assert punto(escalar(a, k), b) == k * punto(a, b)
        assert punto(a, b) ** 2 + cruz(a, b) ** 2 == norma2(a) * norma2(b)
        assert punto(a, rotar90(a)) == 0 and cruz(a, rotar90(a)) == norma2(a)
        assert resta(suma(a, b), b) == a

        if a == (0, 0) or b == (0, 0):
            continue
        # Fuerza bruta trigonométrica: θ = ángulo(b) − ángulo(a) por separado
        theta = math.atan2(b[1], b[0]) - math.atan2(a[1], a[0])
        na, nb = math.sqrt(a[0] ** 2 + a[1] ** 2), math.sqrt(b[0] ** 2 + b[1] ** 2)
        assert cerca(punto(a, b), na * nb * math.cos(theta), abs_tol=1e-7)
        assert cerca(cruz(a, b), na * nb * math.sin(theta), abs_tol=1e-7)
        # angulo_entre coincide con θ normalizado a (−π, π]
        while theta <= -math.pi:
            theta += 2 * math.pi
        while theta > math.pi:
            theta -= 2 * math.pi
        dif = abs(angulo_entre(a, b) - theta)
        assert min(dif, 2 * math.pi - dif) < 1e-9

        # Rotar: preserva la norma y el ángulo entre a y su imagen es t
        t = random.uniform(-3.1, 3.1)
        r = rotar(a, t)
        assert cerca(norma(r), norma(a), rel_tol=1e-12)
        assert abs(angulo_entre(a, r) - t) < 1e-9
        r90 = rotar(a, math.pi / 2)
        assert cerca(r90[0], rotar90(a)[0], abs_tol=1e-9)
        assert cerca(r90[1], rotar90(a)[1], abs_tol=1e-9)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
