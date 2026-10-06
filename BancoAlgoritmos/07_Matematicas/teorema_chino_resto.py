"""
Matemáticas — Teorema chino del resto, con módulos no coprimos («Chinese Remainder Theorem», CRT)
Nivel: Intermedio
Ejecutar: python teorema_chino_resto.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Resolver un sistema
        x ≡ r1 (mód m1),  x ≡ r2 (mód m2),  …,  x ≡ rk (mód mk)
    devolviendo la solución como UNA congruencia x ≡ r (mód mcm(m1, …, mk)),
    o informar que es incompatible. Los módulos NO necesitan ser coprimos.
    Señales en el enunciado: «al agrupar de a 3 sobran 2, de a 5 sobran 3…»;
    eventos periódicos con desfase («el planeta A pasa cada 12 días desde el
    día 5, el B cada 18 desde el día 11: ¿cuándo coinciden?»); calcular algo
    módulo un número compuesto juntando los resultados módulo sus factores
    primos; razonar que «solo importa x mód M» (M = producto de módulos).

FUNCIÓN
    tcr(r1, m1, r2, m2) -> (r, m) o None
        m = mcm(m1, m2), r en [0, m) es la solución única módulo m;
        None si el sistema no tiene solución. m1, m2 ≥ 1.
    tcr_lista(restos, modulos) -> (r, m) o None    el sistema completo
        (lista vacía → (0, 1): todo entero sirve).

IDEA Y ALGORITMO
    Dos congruencias. x ≡ r1 (mód m1) significa x = r1 + m1·t. Sustituyendo
    en la segunda: m1·t ≡ r2 − r1 (mód m2), una congruencia lineal en t.
    Con g = gcd(m1, m2):
    - Tiene solución si y solo si g | (r2 − r1): m1·t − m2·s = r2 − r1 es
      una diofántica lineal y el lado izquierdo siempre es múltiplo de g.
      (Intuición: x mód g está determinado por AMBAS congruencias; si no
      coinciden, es imposible.)
    - Dividiendo por g: (m1/g)·t ≡ (r2 − r1)/g (mód m2/g), con m1/g
      invertible módulo m2/g (son coprimos), así que
          t ≡ ((r2 − r1)/g) · inv(m1/g, m2/g)  (mód m2/g)
      y x = r1 + m1·t.
    - Unicidad: si x y x' son soluciones, x − x' es múltiplo de m1 y de m2,
      luego de mcm(m1, m2) = m1·(m2/g). Por eso la solución es única módulo
      el mcm (y el t de arriba es único módulo m2/g, que da x único módulo
      m1·m2/g).
    Varias congruencias: se combinan de a dos, de izquierda a derecha; la
    acumulada siempre es una congruencia (r, m) equivalente a las que ya se
    procesaron (si alguna combinación falla, no hay solución).
    Caso coprimo (la versión «clásica»): con M = Π m_i y M_i = M/m_i,
    x = Σ r_i·M_i·inv(M_i, m_i) mod M; la versión incremental de arriba hace
    lo mismo y además maneja módulos no coprimos.
    El ingenuo (probar x = 0, 1, 2, … hasta mcm) es O(mcm), que puede ser
    10^18.

MACROALGORITMO
    1. (r, m) = (0, 1).
    2. Para cada (ri, mi):
    3.     g = gcd(m, mi); si (ri − r) % g ≠ 0 → no hay solución.
    4.     t = ((ri − r)/g · inv(m/g, mi/g)) mod (mi/g).
    5.     r = r + m·t;  m = m·(mi/g) (el mcm);  r = r mod m.
    6. Devolver (r, m).

COMPLEJIDAD
    O(k · log M) con k congruencias (un Euclides extendido por paso).
    En Python los números crecen sin desbordar; en C++ el mcm acumulado
    puede pasar de 64 bits: usar __int128 o verificar que la respuesta cabe.

EJEMPLO A MANO
    x ≡ 2 (mód 3), x ≡ 3 (mód 5), x ≡ 2 (mód 7)   (Sun Tzu):
      (0, 1) + (2, 3): g = 1, t = 2 · inv(1, 3) = 2 mód 3 → x = 2, m = 3.
      (2, 3) + (3, 5): g = 1, t ≡ (3 − 2) · inv(3, 5) = 1·2 = 2 (mód 5)
                        → x = 2 + 3·2 = 8, m = 15.
      (8, 15) + (2, 7): t ≡ (2 − 8) · inv(15, 7) = −6 · 1 ≡ 1 (mód 7)
                        → x = 8 + 15 = 23, m = 105.
    x ≡ 23 (mód 105).  No coprimos: x ≡ 5 (mód 12), x ≡ 11 (mód 18):
      g = 6, 11 − 5 = 6 ✓ → t ≡ 1 · inv(2, 3) = 2 (mód 3) → x = 29 (mód 36).
    x ≡ 1 (mód 4), x ≡ 2 (mód 6): g = 2 ∤ 1 → sin solución (paridades opuestas).

ERRORES TÍPICOS
    - Suponer módulos coprimos y usar la fórmula clásica con módulos que no
      lo son: resultado basura (o división por cero en el inverso).
    - Usar m1·m2 en vez de mcm(m1, m2) como nuevo módulo.
    - Calcular el inverso módulo m2 en vez de módulo m2/g.
    - No reducir (r2 − r1) correctamente cuando es negativo (en C++).
    - En C++, m1·t con m1 y t de 64 bits desborda: usar __int128.

VARIANTES Y RELACIONADOS
    - Euclides extendido / inverso modular: euclides_extendido.py.
    - Diofántica lineal (es la misma ecuación m1·t − m2·s = r2 − r1):
      diofantica_lineal.py.
    - Garner: reconstruir un número módulo Π p_i (p_i primos) sin números
      grandes, útil en C++.
    - Multiplicatividad de φ (phi_euler.py) se demuestra con el TCR.
    - Lucas generalizado: C(n, k) mód un compuesto = TCR de los resultados
      módulo cada potencia de primo.

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/I - Impossible Primebox (el comportamiento solo
      depende de x módulo el producto de los primos: por el TCR, de los
      restos de x módulo cada primo)
    - Codeforces 687B «Remainders Game»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (recorrer x en [0, mcm)) en 3000
      sistemas aleatorios de 1 a 4 congruencias con módulos ≤ 20 (coprimos
      o no, compatibles o no), y 1000 sistemas con módulos grandes
      verificando x % m_i == r_i y que el módulo sea el mcm
      (python teorema_chino_resto.py)
"""
import math
import random


def euclides_extendido(a, b):
    """(g, x, y) con a*x + b*y = g (copiado de euclides_extendido.py)."""
    r0, x0, y0 = a, 1, 0
    r1, x1, y1 = b, 0, 1
    while r1:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return r0, x0, y0


def tcr(r1, m1, r2, m2):
    """Combina x ≡ r1 (mod m1) y x ≡ r2 (mod m2). Devuelve (r, mcm) o None."""
    g, inv, _ = euclides_extendido(m1, m2)     # m1*inv ≡ g (mod m2)
    d = r2 - r1
    if d % g:
        return None                 # x mod g debería valer r1 y r2 a la vez
    m2g = m2 // g
    # (m1/g)*t ≡ d/g (mod m2/g); inv es inverso de m1/g módulo m2/g
    t = (d // g) * inv % m2g
    m = m1 * m2g                    # mcm(m1, m2)
    return (r1 + m1 * t) % m, m


def tcr_lista(restos, modulos):
    """Sistema x ≡ restos[i] (mod modulos[i]). Devuelve (r, mcm) o None."""
    r, m = 0, 1                     # «x ≡ 0 (mód 1)»: no restringe nada
    for ri, mi in zip(restos, modulos):
        res = tcr(r, m, ri % mi, mi)
        if res is None:
            return None
        r, m = res
    return r, m


def demo():
    print("x≡2 (3), x≡3 (5), x≡2 (7):", tcr_lista([2, 3, 2], [3, 5, 7]))   # (23, 105)
    print("x≡5 (12), x≡11 (18):", tcr(5, 12, 11, 18))                     # (29, 36)
    print("x≡1 (4), x≡2 (6):", tcr(1, 4, 2, 6))                             # None


def pruebas():
    random.seed(687)

    # Casos borde
    assert tcr_lista([], []) == (0, 1)
    assert tcr_lista([5], [7]) == (5, 7) and tcr_lista([12], [7]) == (5, 7)
    assert tcr(0, 1, 0, 1) == (0, 1) and tcr(3, 5, 3, 5) == (3, 5)
    assert tcr(1, 2, 0, 2) is None
    assert tcr_lista([-1], [5]) == (4, 5)

    # Fuerza bruta: recorrer x en [0, mcm)
    for _ in range(3000):
        k = random.randint(1, 4)
        modulos = [random.randint(1, 20) for _ in range(k)]
        if random.random() < 0.5:
            # sistema compatible a propósito (restos de un x real)
            x = random.randint(0, 10**6)
            restos = [x % mi for mi in modulos]
        else:
            restos = [random.randint(0, mi - 1) for mi in modulos]
        L = math.lcm(*modulos)
        sols = [x for x in range(L) if all(x % mi == ri for mi, ri in zip(modulos, restos))]
        res = tcr_lista(restos, modulos)
        if not sols:
            assert res is None
        else:
            assert len(sols) == 1 and res == (sols[0], L)    # única módulo el mcm

    # Módulos grandes: verificar las congruencias y que el módulo sea el mcm
    for _ in range(1000):
        k = random.randint(1, 5)
        base = random.randint(1, 10**6)
        modulos = [random.randint(1, 10**9) * (base if random.random() < 0.5 else 1)
                   for _ in range(k)]
        x = random.randint(0, 10**40)
        restos = [x % mi for mi in modulos]
        r, m = tcr_lista(restos, modulos)
        assert m == math.lcm(*modulos) and 0 <= r < m and r == x % m
        assert all(r % mi == ri for mi, ri in zip(modulos, restos))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
