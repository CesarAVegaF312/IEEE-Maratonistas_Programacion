"""
Matemáticas — Ecuación de Pell x² − D·y² = ±1 con fracciones continuas («Pell's equation»)
Nivel: Avanzado
Ejecutar: python pell.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar los enteros positivos x, y con x² − D·y² = 1 (o = −1), D > 0 no
    cuadrado perfecto. Hay infinitas soluciones (para +1) que crecen
    exponencialmente y se generan todas a partir de la más pequeña
    (fundamental), que puede ser ENORME aun con D chico (D = 61 → x de 10
    cifras), así que buscarla probando y no sirve.
    Señales en el enunciado: una condición cuadrática en dos enteros que, al
    completar cuadrados, queda «X² − D·Y² = constante» (números triangulares
    que son cuadrados, «suma de 1..k = suma de (k+1)..n», triángulos casi
    equiláteros…); sucesiones de respuestas que crecen por un factor fijo
    (~5,83 = 3 + 2√2 para D = 2).

FUNCIÓN
    pell_fundamental(D, signo=1) -> (x, y) o None
        Menor solución positiva de x² − D·y² = signo (signo = 1 o −1).
        None si D es cuadrado perfecto o si signo = −1 no tiene solución.
    pell_soluciones(D, signo, cuantas) -> list[(x, y)]
        Las primeras soluciones positivas en orden creciente.
    fraccion_continua_raiz(D) -> (a0, periodo)
        √D = [a0; periodo, periodo, …] (periodo vacío si D es cuadrado).

IDEA Y ALGORITMO
    1) Fracción continua de √D. Escribiendo √D = a0 + 1/(a1 + 1/(a2 + …)),
       los términos se obtienen con enteros: con m0 = 0, d0 = 1, a0 = ⌊√D⌋,
           m_{k+1} = d_k·a_k − m_k,  d_{k+1} = (D − m_{k+1}²)/d_k,
           a_{k+1} = ⌊(a0 + m_{k+1}) / d_{k+1}⌋,
       donde (√D + m_k)/d_k es el «resto» en el paso k (la división es
       siempre exacta). Lagrange: la expansión es periódica y el período
       termina cuando a_k = 2·a0 (equivalentemente d_k = 1).
    2) Las soluciones son convergentes. Las convergentes h_k/k_k
       (h_k = a_k·h_{k−1} + h_{k−2}, igual k_k) son las mejores aproximaciones
       racionales de √D. Si x² − D·y² = ±1 con y ≥ 1, entonces
       |x/y − √D| = 1/(y·(x + y√D)) < 1/(2y²) (porque x + y√D > 2y), y por el
       criterio de Legendre toda fracción tan cercana es una convergente.
       Además se cumple h_k² − D·k_k² = (−1)^(k+1)·d_{k+1}, que vale ±1
       exactamente cuando d_{k+1} = 1, es decir al final de cada período
       (k = r − 1, 2r − 1, …, con r la longitud del período). Por eso:
         - Si r es par, la primera tiene signo +1: es la fundamental de +1 y
           x² − D·y² = −1 NO tiene solución.
         - Si r es impar, la primera es la fundamental de −1, y la de +1 es
           la siguiente (k = 2r − 1), o lo que es igual su «cuadrado».
       En código basta recorrer convergentes hasta ver el primer ±1.
    3) Todas las soluciones. Identidad de Brahmagupta:
           (x1² − D·y1²)(x2² − D·y2²) = (x1x2 + D·y1y2)² − D·(x1y2 + x2y1)²,
       es decir, multiplicar x + y√D por x' + y'√D multiplica los valores.
       Si (x1, y1) es la fundamental de +1, las soluciones de +1 son
       (x1 + y1√D)^n (n = 1, 2, …): si hubiera otra, dividiéndola por la
       mayor potencia que no la supere quedaría una solución menor que la
       fundamental, absurdo. Para −1 son las potencias IMPARES de la
       fundamental de −1. En la práctica:
           x_{n+1} = x1·x_n + D·y1·y_n,  y_{n+1} = x1·y_n + y1·x_n.
    El ingenuo (probar y = 1, 2, … hasta que D·y² ± 1 sea cuadrado) no
    termina para D = 61 (y = 226 153 980) ni D = 661 (y ≈ 1,6·10^18).

MACROALGORITMO
    1. Si D es cuadrado perfecto → no hay soluciones no triviales.
    2. a0 = ⌊√D⌋; m = 0, d = 1, a = a0; (h_{−1}, h_{−2}) = (1, 0), (k_{−1}, k_{−2}) = (0, 1).
    3. Repetir: h = a·h1 + h2, k = a·k1 + k2; v = h² − D·k².
    4.     Si v == signo → devolver (h, k).
    5.     Si v == +1 y signo == −1 → el período es par: no hay solución.
    6.     m = d·a − m;  d = (D − m²)/d;  a = (a0 + m) // d.
    7. Para más soluciones: multiplicar repetidamente por la fundamental de
       +1 (para −1, partir de la de −1 y multiplicar por la de +1).

COMPLEJIDAD
    El período tiene longitud O(√D·log D); la solución fundamental puede
    tener O(√D) dígitos. Con Python (enteros grandes) D ≤ 10^6 es inmediato
    para un D; cada solución siguiente cuesta O(1) multiplicaciones.
    Las soluciones crecen geométricamente: hasta 10^18 hay ~log(10^18)/log(x1+y1√D).

EJEMPLO A MANO
    D = 7, √7 = [2; 1, 1, 1, 4] (período r = 4, par):
      k: a_k  h_k  k_k   h² − 7k²
      0:  2    2    1    4 − 7  = −3
      1:  1    3    1    9 − 7  =  2
      2:  1    5    2    25 − 28 = −3
      3:  1    8    3    64 − 63 =  1   → fundamental (8, 3); −1 sin solución.
    Siguiente: (8·8 + 7·3·3, 8·3 + 3·8) = (127, 48): 16129 − 7·2304 = 1 ✓.
    D = 2, signo −1: √2 = [1; 2] (r = 1, impar): (1, 1) → 1 − 2 = −1.
      Siguientes (potencias impares): (7, 5), (41, 29), (239, 169)…
      Colombia 2023 J: x = 2n + 1 → n = 3, 20, 119 (los TNumbers).

ERRORES TÍPICOS
    - Buscar la solución probando y: para D como 61, 109, 181, 661 no termina.
    - Usar flotantes para √D o para los términos: se pierde precisión en
      pocos pasos. Todo con enteros (math.isqrt).
    - Suponer que −1 siempre tiene solución: solo si el período es impar.
    - Olvidar el caso D cuadrado perfecto (solo la trivial x = ±1, y = 0).
    - Para −1, generar con la fundamental de −1 en vez de la de +1: se
      saltan o se cambian de signo.
    - En C++ los valores desbordan muy rápido; normalmente el problema solo
      pide las soluciones ≤ 10^18, que son pocas.

VARIANTES Y RELACIONADOS
    - x² − D·y² = N general: soluciones fundamentales por clase, multiplicadas
      por las de +1 (fuera de este archivo).
    - Recurrencia lineal de las soluciones: x_{n+1} = 2·x1·x_n − x_{n−1}
      (útil con exponenciación de matrices si piden la n-ésima módulo m).
    - Fracciones continuas y árbol de Stern–Brocot (aproximaciones racionales).
    - Ecuaciones lineales en enteros: diofantica_lineal.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/J - TNumbers (x² − 2y² = −1)
    - Project Euler 66 «Diophantine equation»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (menor y ≤ 10^4 con D·y² ± 1 cuadrado)
      para todo D ≤ 80 en ambos signos, todas las soluciones de las listas
      verificadas (x² − D·y² = ±1 y crecientes) para D ≤ 1000, el período
      contra la expansión con fracciones exactas, D = 61 y los TNumbers de
      Colombia 2023 J (python pell.py)
"""
import math
from fractions import Fraction


def fraccion_continua_raiz(D):
    """(a0, periodo) con √D = [a0; periodo repetido]. periodo = [] si D es cuadrado."""
    a0 = math.isqrt(D)
    if a0 * a0 == D:
        return a0, []
    m, d, a = 0, 1, a0
    periodo = []
    while a != 2 * a0:          # el período termina en a_k = 2·a0
        m = d * a - m
        d = (D - m * m) // d    # división exacta
        a = (a0 + m) // d
        periodo.append(a)
    return a0, periodo


def pell_fundamental(D, signo=1):
    """Menor (x, y) positivo con x² - D·y² = signo (±1); None si no existe."""
    a0 = math.isqrt(D)
    if a0 * a0 == D:
        return None             # D cuadrado: solo la trivial
    m, d, a = 0, 1, a0
    h1, h2 = 1, 0               # h_{k-1}, h_{k-2}
    k1, k2 = 0, 1
    while True:
        h, k = a * h1 + h2, a * k1 + k2     # convergente h/k
        v = h * h - D * k * k
        if v == signo:
            return h, k
        if v == 1:              # primer ±1 fue +1: período par, -1 imposible
            return None
        h1, h2, k1, k2 = h, h1, k, k1
        m = d * a - m           # siguiente término de la fracción continua
        d = (D - m * m) // d
        a = (a0 + m) // d


def pell_soluciones(D, signo, cuantas):
    """Primeras `cuantas` soluciones positivas de x² - D·y² = signo."""
    base = pell_fundamental(D, signo)
    if base is None:
        return []
    x1, y1 = pell_fundamental(D, 1)     # unidad que multiplica (norma +1)
    res = [base]
    x, y = base
    while len(res) < cuantas:
        # (x + y√D)(x1 + y1√D): conserva el signo de la norma
        x, y = x1 * x + D * y1 * y, x1 * y + y1 * x
        res.append((x, y))
    return res


def demo():
    print("√7 =", fraccion_continua_raiz(7))                    # (2, [1, 1, 1, 4])
    print("x² - 7y² = 1:", pell_soluciones(7, 1, 3))           # (8,3), (127,48), ...
    print("x² - 7y² = -1:", pell_fundamental(7, -1))           # None
    print("x² - 61y² = 1:", pell_fundamental(61))              # (1766319049, 226153980)
    sols = pell_soluciones(2, -1, 6)
    print("x² - 2y² = -1:", sols)
    print("TNumbers (Colombia 2023 J):", [(x - 1) // 2 for x, _ in sols][1:])   # 3, 20, 119, ...


def pruebas():
    # Casos borde
    assert pell_fundamental(4) is None and pell_fundamental(9, -1) is None
    assert fraccion_continua_raiz(16) == (4, [])
    assert pell_soluciones(1, 1, 5) == []
    assert pell_fundamental(2) == (3, 2) and pell_fundamental(2, -1) == (1, 1)
    assert pell_fundamental(61) == (1766319049, 226153980)
    assert pell_fundamental(13, -1) == (18, 5)
    assert fraccion_continua_raiz(7) == (2, [1, 1, 1, 4])

    # Fuerza bruta: menor y <= LIM con D·y² + signo cuadrado perfecto
    LIM = 10**4
    for D in range(2, 81):
        if math.isqrt(D) ** 2 == D:
            continue
        for signo in (1, -1):
            bruto = None
            for y in range(1, LIM + 1):
                t = D * y * y + signo
                x = math.isqrt(t)
                if x * x == t:
                    bruto = (x, y)
                    break
            sol = pell_fundamental(D, signo)
            if bruto is not None:
                assert sol == bruto, (D, signo)
            else:
                # la fuerza bruta no la alcanzó: o no existe o es más grande
                assert sol is None or sol[1] > LIM
            # existe -1  <=>  período impar
            if signo == -1:
                assert (sol is not None) == (len(fraccion_continua_raiz(D)[1]) % 2 == 1)

    # Todas las soluciones generadas cumplen la ecuación y crecen
    for D in range(2, 1001):
        for signo in (1, -1):
            sols = pell_soluciones(D, signo, 5)
            for x, y in sols:
                assert x * x - D * y * y == signo
            assert all(sols[i][1] < sols[i + 1][1] for i in range(len(sols) - 1))

    # Período contra la expansión con fracciones exactas (√D aproximada con
    # muchos dígitos: Fraction(isqrt(D·10^80), 10^40))
    for D in (2, 3, 7, 13, 19, 31, 46, 61, 94, 133):
        a0, per = fraccion_continua_raiz(D)
        x = Fraction(math.isqrt(D * 10**80), 10**40)
        terminos = []
        for _ in range(1 + len(per)):
            a = math.floor(x)
            terminos.append(a)
            x = 1 / (x - a)
        assert terminos == [a0] + per

    # Colombia 2023 J: TNumbers = (x-1)/2 con x² - 2y² = -1
    tn = [(x - 1) // 2 for x, _ in pell_soluciones(2, -1, 11)][1:]
    assert tn == [3, 20, 119, 696, 4059, 23660, 137903, 803760, 4684659, 27304196]
    for n in tn[:5]:
        k = (math.isqrt(2 * n * n + 2 * n + 1) - 1) // 2       # y = 2k + 1
        assert k * (k + 1) // 2 == n * (n + 1) // 2 - k * (k + 1) // 2


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
