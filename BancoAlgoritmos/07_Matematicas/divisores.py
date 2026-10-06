"""
Matemáticas — Divisores: enumerar, contar y sumar («Divisors», funciones d(n) y σ(n))
Nivel: Intermedio
Ejecutar: python divisores.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Listar todos los divisores de n, o saber cuántos tiene (d(n)) y cuánto
    suman (σ(n)) sin listarlos, a partir de la factorización. También
    calcular d(i) o σ(i) para TODOS los i ≤ N de una vez.
    Señales en el enunciado: «cuántos divisores tiene», «suma de los
    divisores», «números perfectos / abundantes», «formas de partir n en
    grupos iguales» (= divisores), «a·b = n con condiciones» (recorrer
    divisores hasta √n), «el número con más divisores ≤ N».

FUNCIÓN
    divisores(n) -> list             divisores de n ≥ 1 en orden creciente.
    num_divisores(fact) -> int       d(n) = Π (e + 1), fact = [(p, e), …].
    suma_divisores(fact) -> int      σ(n) = Π (p^(e+1) − 1) / (p − 1).
    divisores_desde_factores(fact) -> list   todos los divisores (sin orden).
    criba_divisores(N) -> (d, s)     d[i] y σ[i] para 0 ≤ i ≤ N (d[0] = s[0] = 0).

IDEA Y ALGORITMO
    Enumerar: los divisores vienen en parejas (i, n/i) con i ≤ √n ≤ n/i
    (si i·j = n e i ≤ j, entonces i² ≤ n). Recorrer i = 1..⌊√n⌋ y, si i | n,
    tomar i y n/i (una sola vez si i = n/i, cuando n es un cuadrado).
    Contar: si n = Π p^e, un divisor es exactamente Π p^f con 0 ≤ f ≤ e
    para cada primo (cualquier divisor solo puede usar los primos de n y
    con exponente no mayor; y cada elección de exponentes da un divisor
    distinto por unicidad de la factorización). Las elecciones son
    independientes: d(n) = Π (e + 1).
    Sumar: al desarrollar el producto
        Π_p (1 + p + p² + … + p^e)
    aparece cada combinación Π p^f exactamente una vez, es decir, cada
    divisor exactamente una vez: σ(n) = Π (1 + p + … + p^e), y la serie
    geométrica vale (p^(e+1) − 1)/(p − 1).
    (d y σ son MULTIPLICATIVAS: f(a·b) = f(a)·f(b) si gcd(a, b) = 1.)
    Para todos los i ≤ N: cada d ≤ N es divisor de d, 2d, 3d, …; recorrer
    los múltiplos de cada d cuesta N/1 + N/2 + … + N/N ≈ N·ln N.
    Ingenuo: probar todos los i ≤ n es O(n) por número; con n = 10^12 es
    inviable, mientras √n = 10^6 sí.
    Cota útil: los n ≤ 10^9 tienen a lo sumo 1344 divisores; los ≤ 10^18,
    a lo sumo 103680. Por eso recorrer «todos los divisores» suele ser barato.

MACROALGORITMO
    Enumerar:
    1. Para i = 1, 2, … mientras i·i ≤ n: si n % i == 0, guardar i y n // i.
    2. Unir las dos mitades (la segunda al revés) para tenerlos ordenados.
    Contar / sumar:
    3. Factorizar n (división de prueba o spf).
    4. d = Π (e + 1);  σ = Π (p^(e+1) − 1) // (p − 1).
    Todos los i ≤ N:
    5. Para d = 1..N, para cada múltiplo k de d: cnt[k] += 1, sum[k] += d.

COMPLEJIDAD
    Enumerar: O(√n) (n ≈ 10^12 en ~0,1 s en Python).
    Contar/sumar con la factorización: O(√n) por factorizar (O(log n) con spf).
    Desde los factores: O(d(n)) para listarlos.
    Criba de divisores: O(N log N); en Python N ≈ 10^6 en ~1–2 s.

EJEMPLO A MANO
    n = 36: i = 1 (1, 36), 2 (2, 18), 3 (3, 12), 4 (4, 9), 5 no, 6 (6, 6 una vez).
      → 1 2 3 4 6 9 12 18 36.
    36 = 2² · 3²: d = (2+1)(2+1) = 9 ✓;
      σ = (1+2+4)(1+3+9) = 7 · 13 = 91 = 1+2+3+4+6+9+12+18+36 ✓.

ERRORES TÍPICOS
    - Contar dos veces √n cuando n es cuadrado perfecto (i == n // i).
    - Usar i <= sqrt(n) flotante: falla para n grandes. Usar i * i <= n.
    - En σ, la división de la serie geométrica con / (float): usar //.
      En C++ σ de n ≤ 10^12 cabe en long long, pero p^(e+1) puede desbordar;
      sumar la serie término a término.
    - Hacer la criba con un doble bucle i, j hasta N «para ver si j | i»: es
      O(N²). Recorrer múltiplos.
    - Olvidar que 1 y n son divisores (d(1) = 1, σ(1) = 1).

VARIANTES Y RELACIONADOS
    - Factorización: factorizacion.py (y miller_rabin_pollard.py para 10^18).
    - Criba de primos y spf: criba_eratostenes.py.
    - φ de Euler (otra función multiplicativa): phi_euler.py.
    - Producto de divisores: n^(d(n)/2).
    - Σ_{i ≤ N} d(i) = Σ_k ⌊N/k⌋ (cada k divide a ⌊N/k⌋ números), en O(√N)
      agrupando los valores iguales de ⌊N/k⌋.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/A - Balanced System Reactor (buscar el menor
      divisor d ≤ √M con una congruencia)
    - ICPC/Guangzhou 2017/B - Between Ceiling and Floor (la respuesta es σ(m))
    - CSES «Counting Divisors», «Divisor Analysis», «Sum of Divisors»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (probar todos los i ≤ n) para todo
      n ≤ 3000 (lista, d y σ, desde factores y por criba), 200 n aleatorios
      hasta 10^10 con propiedades (cada uno divide, pares (i, n/i), d y σ
      coinciden con la lista) y d(735134400) = 1344 (python divisores.py)
"""
import random


def divisores(n):
    """Divisores de n >= 1 en orden creciente, en O(√n)."""
    chicos, grandes = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            chicos.append(i)
            if i != n // i:             # no repetir la raíz de un cuadrado perfecto
                grandes.append(n // i)
        i += 1
    return chicos + grandes[::-1]


def factorizar(n):
    """[(p, e)] por división de prueba (copiado de factorizacion.py)."""
    res = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            res.append((d, e))
        d += 1
    if n > 1:
        res.append((n, 1))
    return res


def num_divisores(fact):
    """d(n) = prod (e + 1): cada primo elige su exponente entre 0 y e."""
    r = 1
    for _, e in fact:
        r *= e + 1
    return r


def suma_divisores(fact):
    """sigma(n) = prod (1 + p + ... + p^e) = prod (p^(e+1) - 1) / (p - 1)."""
    r = 1
    for p, e in fact:
        r *= (p ** (e + 1) - 1) // (p - 1)
    return r


def divisores_desde_factores(fact):
    """Todos los divisores combinando exponentes (útil si n es enorme pero ya factorizado)."""
    divs = [1]
    for p, e in fact:
        # cada divisor existente se multiplica por p^0, p^1, ..., p^e
        divs = [d * p**k for d in divs for k in range(e + 1)]
    return divs


def criba_divisores(N):
    """(cnt, suma): número y suma de divisores de cada i <= N, en O(N log N)."""
    cnt = [0] * (N + 1)
    suma = [0] * (N + 1)
    for d in range(1, N + 1):
        for k in range(d, N + 1, d):    # d divide a todos sus múltiplos
            cnt[k] += 1
            suma[k] += d
    return cnt, suma


def demo():
    print("divisores(36) =", divisores(36))
    f = factorizar(36)
    print("36 =", " · ".join(f"{p}^{e}" for p, e in f))
    print("d(36) =", num_divisores(f), " sigma(36) =", suma_divisores(f))   # 9, 91
    print("desde factores:", sorted(divisores_desde_factores(f)))
    cnt, suma = criba_divisores(12)
    print("d(i) para i=1..12:", cnt[1:])


def pruebas():
    random.seed(23)

    # Casos borde
    assert divisores(1) == [1] and num_divisores([]) == 1 and suma_divisores([]) == 1
    assert divisores(2) == [1, 2] and divisores(49) == [1, 7, 49]
    assert criba_divisores(0) == ([0], [0])

    # Fuerza bruta: probar todos los i <= n
    N = 3000
    cnt, suma = criba_divisores(N)
    for n in range(1, N + 1):
        bruto = [i for i in range(1, n + 1) if n % i == 0]
        f = factorizar(n)
        assert divisores(n) == bruto
        assert sorted(divisores_desde_factores(f)) == bruto
        assert num_divisores(f) == len(bruto) == cnt[n]
        assert suma_divisores(f) == sum(bruto) == suma[n]

    # Números grandes: propiedades
    for _ in range(200):
        n = random.randint(1, 10**10) if random.random() < 0.5 else \
            random.choice([720720, 2**20, 3**12, 997 * 991, 10**9])
        divs = divisores(n)
        assert all(n % d == 0 for d in divs) and divs == sorted(set(divs))
        assert all(divs[i] * divs[-1 - i] == n for i in range(len(divs)))
        f = factorizar(n)
        assert num_divisores(f) == len(divs) and suma_divisores(f) == sum(divs)
        assert sorted(divisores_desde_factores(f)) == divs

    # Resultado conocido: el n <= 10^9 con más divisores tiene 1344
    assert num_divisores(factorizar(735134400)) == 1344


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
