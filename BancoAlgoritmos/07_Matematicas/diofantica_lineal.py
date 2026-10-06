"""
Matemáticas — Ecuación diofántica lineal a·x + b·y = c («Linear Diophantine equation»)
Nivel: Intermedio
Ejecutar: python diofantica_lineal.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Encontrar soluciones ENTERAS de a·x + b·y = c: decidir si existen, dar
    todas (familia con un parámetro t) y contar cuántas caen en un rango
    x1 ≤ x ≤ x2, y1 ≤ y ≤ y2 en O(log), sin recorrer el rango.
    Señales en el enunciado: «con monedas/pesas/pasos de a y b, ¿se puede
    llegar exactamente a c?», «¿de cuántas formas…?» con dos variables y
    cotas, saltos de longitud a y b sobre una recta, «puntos enteros sobre
    la recta a·x + b·y = c dentro de un rectángulo».

FUNCIÓN
    resolver(a, b, c) -> (x0, y0, dx, dy) o None
        Con (a, b) ≠ (0, 0). Todas las soluciones son
            x = x0 + t·dx,   y = y0 − t·dy,   t entero,
        con dx = b/g, dy = a/g (g = gcd(|a|, |b|)). None si no hay solución.
    contar_en_rango(a, b, c, x1, x2, y1, y2) -> int
        Número de (x, y) enteros con a·x + b·y = c, x1 ≤ x ≤ x2, y1 ≤ y ≤ y2.
        (Acepta a = b = 0.)

IDEA Y ALGORITMO
    Sea g = gcd(a, b).
    1) Existencia: a·x + b·y es siempre múltiplo de g, así que si g ∤ c no
       hay solución. Si g | c, Euclides extendido da a·u + b·v = g y,
       multiplicando por k = c/g, (x0, y0) = (u·k, v·k) es solución.
    2) Todas las soluciones: si (x, y) y (x0, y0) son soluciones, restando
       a·(x − x0) = −b·(y − y0). Dividiendo por g con a = g·a', b = g·b' y
       gcd(a', b') = 1: a'·(x − x0) = −b'·(y − y0). Entonces b' divide a
       a'·(x − x0) y, como es coprimo con a', divide a (x − x0): x = x0 + t·b'
       y, sustituyendo, y = y0 − t·a'. Y cualquier t sirve:
       a·(x0 + t·b') + b·(y0 − t·a') = c + t·(a·b' − b·a') = c + t·(g·a'·b' − g·b'·a') = c.
       Las soluciones forman una «escalera» de puntos equiespaciados sobre
       la recta.
    3) Contar en un rango: cada cota x1 ≤ x0 + t·dx ≤ x2 es un intervalo de
       t (dividir entre dx con techo/piso, cuidando el signo); lo mismo con
       y. La respuesta es el tamaño de la intersección de los intervalos.
    El ingenuo (recorrer todos los x del rango y ver si (c − a·x)/b es
    entero y está en rango) es O(x2 − x1): con rangos de 10^9 no alcanza, y
    si hay que repetirlo para muchos valores (como en Colombia 2017 B) el
    O(1) por consulta es lo que hace pasar.

MACROALGORITMO
    1. (g, u, v) = euclides_extendido(|a|, |b|); ajustar los signos de u, v
       según los signos de a y b para que a·u + b·v = g.
    2. Si c % g ≠ 0 → no hay solución.
    3. x0 = u·(c/g), y0 = v·(c/g), dx = b/g, dy = a/g.
    4. Intervalo de t por x: de x1 ≤ x0 + t·dx ≤ x2 (si dx = 0, exigir
       x1 ≤ x0 ≤ x2 y no restringir t). Igual por y con −dy.
    5. Contar = max(0, t_alto − t_bajo + 1) de la intersección.

COMPLEJIDAD
    O(log min(|a|, |b|)) por Euclides extendido; el conteo es O(1) más.
    Memoria O(1).

EJEMPLO A MANO
    3x + 5y = 22 con 0 ≤ x, y ≤ 10.
    Euclides extendido: 3·2 + 5·(−1) = 1 (g = 1). k = 22:
        x = 44 + 5t,  y = −22 − 3t.
    0 ≤ 44 + 5t ≤ 10   → −8,8 ≤ t ≤ −6,8 → t ∈ {−8, −7}
    0 ≤ −22 − 3t ≤ 10  → −10,7 ≤ t ≤ −7,3 → t ∈ {−10, −9, −8}
    Intersección: t = −8 → (x, y) = (4, 2): 12 + 10 = 22 ✓. Una solución.
    6x + 10y = 15: g = 2 no divide a 15 → sin solución.

ERRORES TÍPICOS
    - Olvidar dividir los pasos por g: x = x0 + t·b (en vez de b/g) se salta
      soluciones.
    - Techo/piso con división de C++ (trunca hacia 0) o con flotantes: usar
      enteros y cuidar el signo del divisor. En Python, piso = p // q y
      techo = −((−p) // q), válidos para cualquier signo de q.
    - No invertir el intervalo cuando el paso es negativo (a o b negativos).
    - Casos a = 0 o b = 0 (una variable libre) y a = b = 0 (o todo el rango
      o nada, según c).
    - x0 = u·c/g puede ser enorme (≈ |b|·|c|/g): en C++ puede desbordar
      long long; reducir x0 módulo dx antes de usarlo.

VARIANTES Y RELACIONADOS
    - Euclides extendido e inverso modular: euclides_extendido.py.
    - Congruencia lineal a·x ≡ c (mód m) = a·x + m·y = c.
    - Menor x ≥ 0: x0 mod |dx| (si dx ≠ 0).
    - Tres variables (Colombia 2017 B): fijar una y resolver la ecuación de
      dos con este archivo para cada valor.
    - Problema de Frobenius (con a, b ≥ 1 coprimos, el mayor c sin solución
      con x, y ≥ 0 es a·b − a − b).
    - Teorema chino del resto con módulos no coprimos: teorema_chino_resto.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2017/B - Balance Game (n2·x2 + n3·x3 = R con |x_i| ≤ M,
      contar soluciones para cada x1)
    - Codeforces 7C «Line», Codeforces 633A «Ebony and Ivory»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (recorrer todo el rectángulo) en 4000
      casos aleatorios con a, b, c de cualquier signo (incluye a = 0, b = 0
      y a = b = 0), y la familia (x0 + t·dx, y0 − t·dy) verificada en casos
      grandes (python diofantica_lineal.py)
"""
import random


def euclides_extendido(a, b):
    """(g, x, y) con a*x + b*y = g = gcd(a, b), a, b >= 0 (copiado de euclides_extendido.py)."""
    r0, x0, y0 = a, 1, 0
    r1, x1, y1 = b, 0, 1
    while r1:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return r0, x0, y0


def resolver(a, b, c):
    """(x0, y0, dx, dy): soluciones x = x0 + t*dx, y = y0 - t*dy; None si no hay.

    Requiere (a, b) != (0, 0).
    """
    g, u, v = euclides_extendido(abs(a), abs(b))
    if a < 0:
        u = -u              # |a|*u = a*(-u)
    if b < 0:
        v = -v
    # ahora a*u + b*v = g
    if c % g:
        return None         # a*x + b*y siempre es múltiplo de g
    k = c // g
    return u * k, v * k, b // g, a // g


def _intervalo_t(v0, d, lo, hi):
    """Intervalo [t_bajo, t_alto] de enteros t con lo <= v0 + t*d <= hi (d != 0)."""
    def piso(p, q):
        return p // q

    def techo(p, q):
        return -((-p) // q)

    if d > 0:
        return techo(lo - v0, d), piso(hi - v0, d)
    return techo(hi - v0, d), piso(lo - v0, d)     # dividir por negativo invierte


def contar_en_rango(a, b, c, x1, x2, y1, y2):
    """Número de soluciones enteras de a*x + b*y = c con x en [x1, x2], y en [y1, y2]."""
    if x1 > x2 or y1 > y2:
        return 0
    if a == 0 and b == 0:
        return (x2 - x1 + 1) * (y2 - y1 + 1) if c == 0 else 0
    sol = resolver(a, b, c)
    if sol is None:
        return 0
    x0, y0, dx, dy = sol
    INF = float("inf")
    t_bajo, t_alto = -INF, INF
    # restricción sobre x = x0 + t*dx
    if dx == 0:
        if not x1 <= x0 <= x2:
            return 0
    else:
        lo, hi = _intervalo_t(x0, dx, x1, x2)
        t_bajo, t_alto = max(t_bajo, lo), min(t_alto, hi)
    # restricción sobre y = y0 - t*dy  (paso -dy)
    if dy == 0:
        if not y1 <= y0 <= y2:
            return 0
    else:
        lo, hi = _intervalo_t(y0, -dy, y1, y2)
        t_bajo, t_alto = max(t_bajo, lo), min(t_alto, hi)
    # dx y dy no son ambos 0, así que el intervalo quedó acotado
    return max(0, t_alto - t_bajo + 1)


def demo():
    x0, y0, dx, dy = resolver(3, 5, 22)
    print(f"3x + 5y = 22: x = {x0} + {dx}t, y = {y0} - {dy}t")
    print("soluciones con 0 <= x, y <= 10:", contar_en_rango(3, 5, 22, 0, 10, 0, 10))   # 1
    print("6x + 10y = 15:", resolver(6, 10, 15))                                        # None
    print("2x - 3y = 1 con |x|, |y| <= 20:", contar_en_rango(2, -3, 1, -20, 20, -20, 20))


def pruebas():
    random.seed(2017)

    # Casos borde
    assert resolver(6, 10, 15) is None
    assert contar_en_rango(0, 0, 0, 1, 3, 1, 2) == 6 and contar_en_rango(0, 0, 5, 1, 3, 1, 2) == 0
    assert contar_en_rango(0, 2, 4, -5, 5, 0, 10) == 11        # y = 2, x libre
    assert contar_en_rango(3, 0, 9, -5, 5, -1, 1) == 3         # x = 3, y libre
    assert contar_en_rango(1, 1, 0, 3, 2, 0, 0) == 0           # rango vacío

    # Fuerza bruta sobre el rectángulo
    for _ in range(4000):
        a = random.randint(-6, 6)
        b = random.randint(-6, 6)
        c = random.randint(-25, 25)
        x1 = random.randint(-12, 12)
        x2 = random.randint(x1 - 1, 12)
        y1 = random.randint(-12, 12)
        y2 = random.randint(y1 - 1, 12)
        bruto = sum(1 for x in range(x1, x2 + 1) for y in range(y1, y2 + 1) if a * x + b * y == c)
        assert contar_en_rango(a, b, c, x1, x2, y1, y2) == bruto
        if (a, b) != (0, 0):
            sol = resolver(a, b, c)
            existe = any(a * x + b * y == c for x in range(-40, 41) for y in range(-40, 41))
            assert (sol is not None) == existe
            if sol:
                x0, y0, dx, dy = sol
                for t in range(-3, 4):
                    assert a * (x0 + t * dx) + b * (y0 - t * dy) == c

    # Casos grandes: la familia sigue siendo solución y el conteo es coherente
    for _ in range(500):
        a = random.randint(-10**9, 10**9)
        b = random.randint(-10**9, 10**9)
        if a == 0 or b == 0:
            continue
        c = random.randint(-10**18, 10**18)
        sol = resolver(a, b, c)
        if sol is None:
            continue
        x0, y0, dx, dy = sol
        t = random.randint(-10**6, 10**6)
        assert a * (x0 + t * dx) + b * (y0 - t * dy) == c
        # en un rango de x de largo exactamente |dx| hay justo una solución (y libre)
        x1 = random.randint(-10**12, 10**12)
        assert contar_en_rango(a, b, c, x1, x1 + abs(dx) - 1, -10**40, 10**40) == 1


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
