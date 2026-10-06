"""
Matemáticas — Prueba de primalidad por división hasta √n («Trial division», forma 6k ± 1)
Nivel: Básico
Ejecutar: python primalidad.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Decidir si UN número n es primo, sin precalcular nada, en O(√n).
    Alcanza para pocas consultas con n hasta ~10^12 en Python.
    Señales en el enunciado: «¿es primo n?» con pocas consultas y n
    demasiado grande para una criba (10^9–10^12); verificar un candidato
    dentro de otra búsqueda («el menor primo mayor que n»: los primos están
    a distancia media ln n, así que se prueban pocos candidatos).
    Si hay MUCHAS consultas con n ≤ 10^7 → criba_eratostenes.py; si n llega
    a 10^18 → miller_rabin_pollard.py.

FUNCIÓN
    es_primo(n) -> bool         True si n es primo (n < 2 → False).
    siguiente_primo(n) -> int   menor primo ≥ n.

IDEA Y ALGORITMO
    1) Basta probar divisores d ≤ √n. Si n = a·b con 1 < a ≤ b, entonces
       a·a ≤ a·b = n, es decir a ≤ √n. Así, si ningún d en [2, √n] divide a
       n, n no puede tener factorización no trivial: es primo.
    2) Basta probar 2, 3 y los d de la forma 6k ± 1. Todo entero es 6k + r
       con r ∈ {0, 1, 2, 3, 4, 5}; los de residuo 0, 2, 4 son pares y los de
       residuo 3 son múltiplos de 3. Si n no es divisible por 2 ni por 3,
       tampoco lo es por ningún múltiplo de 2 o de 3, así que solo quedan
       candidatos 6k + 1 y 6k + 5 = 6(k+1) − 1. Se prueban 2 de cada 6
       números: √n / 3 divisiones en lugar de √n.
    El ingenuo (probar todos los d < n) es O(n): con n = 10^12 imposible.

MACROALGORITMO
    1. Si n < 2 → no primo. Si n ≤ 3 → primo.
    2. Si n es divisible por 2 o por 3 → no primo.
    3. Para i = 5, 11, 17, … mientras i·i ≤ n:
         si n % i == 0 o n % (i + 2) == 0 → no primo.
    4. Si ningún divisor apareció → primo.

COMPLEJIDAD
    O(√n) en el peor caso (cuando n es primo o producto de dos primos
    cercanos), ~√n / 3 divisiones; memoria O(1).
    En Python ~10^7 operaciones simples por segundo: n ≈ 10^12 (3·10^5
    iteraciones) tarda unos 0,05 s por número; n ≈ 10^14 ya ~0,5 s.

EJEMPLO A MANO
    n = 221: no es par ni múltiplo de 3. √221 ≈ 14,9.
      i = 5:  221 % 5 = 1,  221 % 7 = 4
      i = 11: 221 % 11 = 1, 221 % 13 = 0  → 221 = 13 · 17, no es primo.
    n = 97: √97 ≈ 9,8. i = 5: 97 % 5 = 2, 97 % 7 = 6. i = 11: 121 > 97 → primo.

ERRORES TÍPICOS
    - Usar i <= sqrt(n) con flotantes: para n grandes (> 2^52) el redondeo
      falla. Comparar con enteros: i * i <= n (o math.isqrt).
    - Olvidar los casos n = 0, 1 (no son primos) y n = 2, 3 (sí lo son).
    - Probar solo i y no i + 2 en el paso de 6: se escapan los 6k + 1.
    - Usarla con 10^5 consultas de números grandes: TLE. Ahí va la criba o
      Miller–Rabin.

VARIANTES Y RELACIONADOS
    - Muchas consultas pequeñas: criba_eratostenes.py.
    - n hasta 10^18 o más: Miller–Rabin determinista (miller_rabin_pollard.py).
    - Mismo bucle hasta √n para factorizar (factorizacion.py) y para
      enumerar divisores (divisores.py).
    - Un número con exactamente 3 divisores es el cuadrado de un primo.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/A - Balanced System Reactor (hay solución con a = 2
      salvo cuando 2n − 1 es primo; se descubre buscando divisores hasta √)
    - ICPC/Guangzhou 2017/B - Between Ceiling and Floor (primos < 1000 por
      división de prueba antes de Miller–Rabin)
    - Codeforces 230B «T-primes»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todos los divisores 2..n−1) para
      n ≤ 3000, contra una criba hasta 2·10^5, 300 números aleatorios
      hasta 10^10 contra división de prueba simple, y primos/compuestos
      conocidos (10^9+7, 998244353, 999983², 561…) (python primalidad.py)
"""
import random


def es_primo(n):
    """True si n es primo. División de prueba por 2, 3 y los 6k ± 1 hasta √n."""
    if n < 2:
        return False
    if n < 4:
        return True             # 2 y 3
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:           # comparar con enteros, nunca con sqrt flotante
        if n % i == 0 or n % (i + 2) == 0:     # i = 6k - 1, i + 2 = 6k + 1
            return False
        i += 6
    return True


def siguiente_primo(n):
    """Menor primo >= n (los primos están a distancia media ~ ln n)."""
    n = max(n, 2)
    while not es_primo(n):
        n += 1
    return n


def demo():
    for n in (1, 2, 97, 221, 1_000_000_007):
        print(f"es_primo({n}) = {es_primo(n)}")
    print("siguiente_primo(10**9) =", siguiente_primo(10**9))    # 1000000007


def pruebas():
    random.seed(31)

    # Casos borde y conocidos
    assert [n for n in range(-5, 12) if es_primo(n)] == [2, 3, 5, 7, 11]
    assert es_primo(1_000_000_007) and es_primo(998_244_353) and es_primo(2_147_483_647)
    assert not es_primo(561)                    # Carmichael (engaña a Fermat, no a esto)
    assert not es_primo(25) and not es_primo(49) and not es_primo(999_983 * 999_983)
    assert es_primo(999_983) and not es_primo(1_000_000_007 * 3)
    assert siguiente_primo(-3) == 2 and siguiente_primo(14) == 17
    assert siguiente_primo(10**9) == 1_000_000_007

    # Fuerza bruta literal: ningún d en 2..n-1 divide a n
    for n in range(3001):
        assert es_primo(n) == (n >= 2 and all(n % d for d in range(2, n)))

    # Contra una criba de Eratóstenes (independiente)
    N = 200_000
    criba = bytearray([1]) * (N + 1)
    criba[0] = criba[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if criba[i]:
            criba[i * i::i] = bytearray(len(range(i * i, N + 1, i)))
    for n in range(N + 1):
        assert es_primo(n) == bool(criba[n])

    # Números grandes contra división de prueba por TODOS los d hasta √n
    primos_chicos = [p for p in range(2, N + 1) if criba[p]]
    for _ in range(300):
        n = random.randint(2, 10**10)
        esperado = all(n % p for p in primos_chicos if p * p <= n) if n > N else bool(criba[n])
        assert es_primo(n) == esperado


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
