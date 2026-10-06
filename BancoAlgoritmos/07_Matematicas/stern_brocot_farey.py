"""
Matemáticas — Árbol de Stern–Brocot y sucesión de Farey: mejor aproximación racional
Nivel: Avanzado
Ejecutar: python stern_brocot_farey.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Trabajar con fracciones de denominador acotado: listar todas las
    fracciones irreducibles en [0, 1] con denominador ≤ N en orden (Farey),
    encontrar la fracción con denominador ≤ N más cercana por arriba o por
    abajo a un racional x (mejor aproximación), o recorrer/codificar
    racionales como caminos L/R en el árbol de Stern–Brocot.
    Cómo reconocerlo: «a/b con b ≤ n», «la menor fracción ≥ x que se puede
    formar», «aproximar un número con denominador pequeño», «vecinos» o
    «tangentes» entre fracciones (|ad − bc| = 1), x dado como fracción y n
    hasta 10^9 (no se puede recorrer todo b).

FUNCIÓN
    farey(N) -> list[(p, q)]        F_N: fracciones irreducibles en [0, 1] con
                                    q ≤ N, en orden creciente (O(|F_N|)).
    vecinos(p, q, N) -> ((a, b), (c, d))
        Mayor fracción ≤ p/q y menor fracción ≥ p/q con denominador ≤ N
        (iguales a p/q si su forma reducida ya tiene denominador ≤ N).
        p ≥ 0, q ≥ 1. O(log max(p, q)).
    camino(p, q) -> str              camino L/R desde 1/1 hasta p/q (p, q ≥ 1)
    desde_camino(s) -> (p, q)        la fracción de un camino L/R

IDEA Y ALGORITMO
    Mediante de a/b < c/d: (a+c)/(b+d), que queda estrictamente entre ellas.
    Lema clave: si bc − ad = 1 («vecinas»), toda fracción p/q estrictamente
    entre ellas tiene q ≥ b + d. Prueba: cq − dp ≥ 1 y bp − aq ≥ 1 (son
    enteros positivos), luego q = q(bc − ad) = b(cq − dp) + d(bp − aq) ≥ b + d.
    Así la mediante es LA fracción de menor denominador entre dos vecinas,
    y las vecinas siguen siéndolo con su mediante (se verifica con álgebra).
    Stern–Brocot: empezar con 0/1 y 1/0 e insertar mediantes recursivamente
    genera cada racional positivo exactamente una vez, ya reducido. Para
    buscar x se baja manteniendo l < x < u vecinas: si la mediante es < x,
    pasa a ser l; si es > x, pasa a ser u. Por el lema, cuando el
    denominador de la mediante supera N, NO hay fracciones de denominador
    ≤ N estrictamente entre l y u: l y u son los vecinos de x en F_N.
    Saltos: bajar paso a paso puede tomar N pasos (p. ej. x = 1/N). Pero
    los pasos en la misma dirección son l_t = (a + t·c)/(b + t·d); el mayor t
    con l_t < x y b + t·d ≤ N sale con una división entera. Esos t son los
    cocientes de la fracción continua de x, así que hay O(log) saltos.
    Farey: si a/b, c/d son consecutivas en F_N, la siguiente es
    (k·c − a)/(k·d − b) con k = ⌊(N + b)/d⌋ (es la fracción de mayor
    denominador ≤ N cuya «vecina izquierda» es c/d).
    El camino L/R de p/q es su fracción continua: el algoritmo de Euclides
    (restar el menor del mayor) dice cuántas L/R seguidas hay.

MACROALGORITMO
    1. Reducir x = p/q; si q ≤ N, x mismo es la respuesta.
    2. l = 0/1, u = 1/0.
    3. Mientras el denominador de la mediante de l y u sea ≤ N:
    4.   si mediante < x: avanzar l hacia u el máximo t posible
         (l < x y denominador ≤ N);
    5.   si no: avanzar u hacia l el máximo t posible (u > x, denom. ≤ N).
    6. Devolver (l, u): mejor aproximación por abajo y por arriba.
    7. La más cercana de las dos se elige comparando |x − l| y |u − x|
       con productos cruzados (enteros, sin flotantes).

COMPLEJIDAD
    vecinos: O(log max(p, q)) saltos, memoria O(1).
    farey(N): O(|F_N|) ≈ 3N²/π² fracciones (N = 1000 → ~3·10^5).
    camino: O(longitud del camino) (puede ser grande: 1/N tiene N−1 L);
    con codificación por rachas sería O(log).

EJEMPLO A MANO
    x = 16/25 = 0,64, N = 3. l=0/1, u=1/0: mediante 1/1 > x → u = 1/1
    (t = 1: 1/2 ya es < x). Mediante 1/2 < x → l = 1/2 (t = 1 porque
    2/3 > x). Mediante 2/3 > x → u = 2/3. Mediante 3/5: 5 > 3 → parar.
    Vecinos (1/2, 2/3). Colombia 2018 J: L = 500, n = 3, d = 320 → 2/3·500 = 1000/3.
    F_5: 0/1 1/5 1/4 1/3 2/5 1/2 3/5 2/3 3/4 4/5 1/1.

ERRORES TÍPICOS
    - Comparar fracciones con flotantes (usar a·d < c·b).
    - Bajar por el árbol de a un paso (O(N), demasiado lento con N = 10^9).
    - Olvidar que 1/0 es la cota superior inicial (división por cero al
      calcular el salto si no se trata d = 0 como «sin límite»).
    - No reducir x antes de comparar su denominador con N.
    - En Farey, usar el entero k sin el piso o con N + d en vez de N + b.

VARIANTES Y RELACIONADOS
    - Fracción de menor denominador estrictamente entre dos racionales
      (misma bajada, parando cuando la mediante cae dentro del intervalo).
    - Círculos de Ford: los de p/q y r/s son tangentes ⇔ |ps − rq| = 1
      (vecinas de Farey).
    - Fracciones continuas y convergentes (mejores aproximaciones de
      primera especie); gcd_lcm.py y euclides_extendido.py (mismo Euclides).
    - Árbol de Calkin–Wilf (otra enumeración de los racionales).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/J - Jawbreaking Candy (vecino por arriba de d/L en
      F_n con saltos de Stern–Brocot)
    - ICPC/Colombia 2017/E - Rational Coins (círculos de Ford: tangentes ⇔
      vecinas de Farey |ps − rq| = 1)

VERIFICACIÓN
    - Pruebas: OK de vecinos contra recorrer todos los denominadores
      b ≤ N con Fraction (3000 casos, incluye x > 1 y x entero); farey
      contra el conjunto de fracciones reducidas para N ≤ 40 y la
      propiedad bc − ad = 1; camino ↔ desde_camino para todo p, q ≤ 60
      coprimos (python stern_brocot_farey.py)
"""
import random
from fractions import Fraction
from math import gcd


def farey(N):
    """Sucesión de Farey F_N (N ≥ 1) como lista de (p, q)."""
    a, b, c, d = 0, 1, 1, N            # dos primeros términos: 0/1 y 1/N
    res = [(0, 1)]
    while c <= d:                      # hasta llegar a 1/1
        res.append((c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    return res


def vecinos(p, q, N):
    """(mayor ≤ p/q, menor ≥ p/q) con denominador ≤ N, por bajada de Stern–Brocot."""
    g = gcd(p, q)
    p, q = p // g, q // g
    if q <= N:
        return (p, q), (p, q)
    a, b = 0, 1                        # cota inferior l = a/b < x
    c, d = 1, 0                        # cota superior u = c/d > x (1/0 = infinito)
    while b + d <= N:
        if (a + c) * q < p * (b + d):  # mediante < x: subir l hacia u
            # mayor t con (a + t c)/(b + t d) < x  ⇔  t (c q − p d) < p b − a q
            t = (p * b - a * q - 1) // (c * q - p * d)
            if d:
                t = min(t, (N - b) // d)
            a, b = a + t * c, b + t * d
        else:                          # mediante > x: bajar u hacia l
            # mayor t con (c + t a)/(d + t b) > x  ⇔  t (p b − a q) < c q − p d
            t = min((c * q - p * d - 1) // (p * b - a * q), (N - d) // b)
            c, d = c + t * a, d + t * b
    return (a, b), (c, d)


def camino(p, q):
    """Camino L/R desde la raíz 1/1 hasta p/q (p, q ≥ 1) en Stern–Brocot."""
    g = gcd(p, q)
    p, q = p // g, q // g
    partes = []
    while p != q:
        if p > q:                      # x > 1: ir a la derecha mientras siga > 1 tras restar
            k = (p - 1) // q
            partes.append("R" * k)
            p -= k * q
        else:
            k = (q - 1) // p
            partes.append("L" * k)
            q -= k * p
    return "".join(partes)


def desde_camino(s):
    """Fracción (p, q) que corresponde al camino L/R s."""
    a, b, c, d = 0, 1, 1, 0            # l = 0/1, u = 1/0; el nodo actual es la mediante
    for ch in s:
        m = (a + c, b + d)
        if ch == "L":
            c, d = m                   # la mediante pasa a ser la cota superior
        else:
            a, b = m
    return a + c, b + d


def demo():
    print("F_5:", " ".join(f"{p}/{q}" for p, q in farey(5)))
    lo, hi = vecinos(16, 25, 3)
    print("vecinos de 16/25 con denominador <= 3:", lo, hi)            # (1,2) (2,3)
    L, n, dd = 500, 3, 320                                               # Colombia 2018 J
    lo, hi = vecinos(dd, L, n)
    num, den = hi[0] * L, hi[1]
    g = gcd(num, den)
    print(f"Colombia 2018 J (500 3 320): {num // g}/{den // g}")       # 1000/3
    print("mejores aproximaciones de pi≈355/113 con denom <= 100:", vecinos(355, 113, 100))
    print("camino de 3/5:", camino(3, 5), "->", desde_camino(camino(3, 5)))  # LRL


def pruebas():
    random.seed(1817)

    # Casos borde
    assert farey(1) == [(0, 1), (1, 1)]
    assert vecinos(0, 7, 3) == ((0, 1), (0, 1))
    assert vecinos(6, 4, 2) == ((3, 2), (3, 2))
    assert vecinos(1, 1000, 999) == ((0, 1), (1, 999))
    assert camino(1, 1) == "" and desde_camino("") == (1, 1)

    # vecinos contra recorrer todos los denominadores
    for _ in range(3000):
        q = random.randint(1, 300)
        p = random.randint(0, 3 * q)
        N = random.randint(1, 60)
        x = Fraction(p, q)
        abajo = max(Fraction((p * b) // q, b) for b in range(1, N + 1))
        arriba = min(Fraction(-((-p * b) // q), b) for b in range(1, N + 1))
        lo, hi = vecinos(p, q, N)
        assert Fraction(*lo) == abajo and Fraction(*hi) == arriba
        assert gcd(*lo) == 1 and gcd(*hi) == 1 and lo[1] <= N and hi[1] <= N
        assert Fraction(*lo) <= x <= Fraction(*hi)

    # Farey contra el conjunto ordenado de fracciones reducidas
    for N in range(1, 41):
        F = farey(N)
        esperado = sorted({Fraction(a, b) for b in range(1, N + 1) for a in range(0, b + 1)})
        assert [Fraction(a, b) for a, b in F] == esperado
        assert all(gcd(a, b) == 1 for a, b in F)
        for (a, b), (c, d) in zip(F, F[1:]):
            assert b * c - a * d == 1          # consecutivas son vecinas

    # camino ↔ desde_camino (ida y vuelta)
    for p in range(1, 61):
        for q in range(1, 61):
            if gcd(p, q) == 1:
                s = camino(p, q)
                assert desde_camino(s) == (p, q)
    # cada camino de largo ≤ 10 da una fracción distinta y reducida
    vistos = set()
    for largo in range(0, 11):
        for mask in range(1 << largo):
            s = "".join("R" if mask >> i & 1 else "L" for i in range(largo))
            f = desde_camino(s)
            assert gcd(*f) == 1 and f not in vistos
            vistos.add(f)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
