"""
ACM ICPC Guangzhou Summer Series 2017 — B: Between Ceiling and Floor («Entre el techo y el piso»)
Ejecutar: python ceilingfloor.py < ceilingfloor.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Dados m y k se define f(x, y) = x·⌈y·√k⌉ − y·⌊x·√k⌋. Hay que contar los
    pares de enteros positivos (a, b) con f(a, b) = m que además NO se
    pueden "reducir": f(a − b, b) ≠ m y f(a, b − a) ≠ m.

QUÉ HAY QUE HACER
    Entrada: hasta 1000 líneas "m k" hasta fin de archivo.
    Salida:  por línea, la cantidad de pares.
    Restricciones clave: 1 ≤ m, k ≤ 10^18 (no se puede buscar pares: hay
    que encontrar una fórmula en m).

IDEA Y ALGORITMO
    Sea α = √k.
    * Si k es cuadrado perfecto, α es entero y f(x, y) = x·yα − y·xα = 0 ≠ m:
      la respuesta es 0.
    * Si α es irracional, escribimos P = (a, ⌊aα⌋) (punto entero justo
      DEBAJO de la recta y = αx) y Q = (b, ⌈bα⌉) (justo ENCIMA). Entonces
      f(a, b) = det(P, Q) = a·dQ + b·dP, con dP = aα − ⌊aα⌋ ∈ (0,1) y
      dQ = ⌈bα⌉ − bα ∈ (0,1).
      - P + Q queda por debajo o por encima de la recta. Si queda debajo,
        P + Q es justamente el punto "piso" de la columna a + b y
        f(a+b, b) = det(P+Q, Q) = det(P, Q); si queda encima, f(a, a+b) = m.
        Así las soluciones de f = m forman CADENAS infinitas (es el
        algoritmo de Euclides por restas sobre (dP, dQ) al revés).
      - Retroceder un paso de la cadena (restar el menor de P, Q del mayor)
        conserva m exactamente cuando dP + dQ < 1. Los pares que piden
        (las "raíces", sin antecesor) son los de dP + dQ ≥ 1; hay
        exactamente una raíz por cadena.
      - Cada raíz genera (con P, Q) un subretículo de Z² de índice
        det = m, y resulta que hay exactamente una raíz por subretículo de
        índice m. El número de subretículos de índice m de Z² (formas de
        Hermite [[d, j], [0, m/d]], d | m, 0 ≤ j < d) es σ(m), la SUMA DE
        DIVISORES de m. Respuesta = σ(m), independiente de k.
      Esta biyección la verifiqué numéricamente (ver VERIFICACIÓN); el
      argumento de las cadenas sí está demostrado arriba, la biyección con
      subretículos es la explicación de por qué sale σ(m).
      Ejemplo: m = 3, k = 5 → raíces (1,9), (3,1), (3,2), (3,3): 4 = σ(3). ✔
    * σ(m) con m ≤ 10^18 exige factorizar: división por primos pequeños,
      test de Miller–Rabin determinista para 64 bits y Pollard rho (variante
      de Brent con gcd acumulado) para lo que quede.
      σ(p1^e1·…·pr^er) = Π (p^(e+1) − 1)/(p − 1).

MACROALGORITMO
    1. Para cada línea (m, k): si isqrt(k)² = k, imprimir 0.
    2. Si no, factorizar m: quitar primos < 1000 por división.
    3. Lo que quede (si > 1) se parte recursivamente con Miller–Rabin +
       Pollard–Brent hasta tener solo primos.
    4. Agrupar exponentes y calcular σ(m) = Π (p^(e+1) − 1)/(p − 1).
    5. Imprimir σ(m).

COMPLEJIDAD
    Por caso: O(168) divisiones + Pollard en O(m^(1/4)) iteraciones
    esperadas (≈ 4·10^4 para m = p·q con p, q ≈ 10^9). 1000 casos
    adversarios (todos semiprimos p·q con p, q ≈ 10^9): ~14 s en Python;
    1000 m aleatorios ≤ 10^18: ~0.5 s. El peor caso adversario puede pasar
    del límite de 5 s del juez en Python (en C++ sobraría).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/B")
    - Fuerza bruta: la búsqueda literal de pares (con la definición exacta de
      f, incluso con argumentos ≤ 0 en las condiciones) acotada por
      min(a, b) < 2m, a·dQ < m, b·dP < m (cotas que cumple toda raíz) da
      σ(m) en 378 combinaciones: m = 1..25 con 14 valores de k no cuadrados
      (2 … 12345678, 10^6 ± 1) y 0 para k cuadrados.
    - Factorización: σ(m) por Pollard comparado con σ por criba para todo
      m ≤ 20000, con 1000 semiprimos p·q (p, q ≈ 10^9), con p² y con 10^18.
"""
import math
import random
import sys

PRIMOS_PEQUENOS = [p for p in range(2, 1000) if all(p % q for q in range(2, int(p ** 0.5) + 1))]


def es_primo(n):
    """Miller–Rabin determinista para n < 3.3·10^24 (bases = primeros 13 primos)."""
    if n < 2:
        return False
    for p in PRIMOS_PEQUENOS[:13]:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in PRIMOS_PEQUENOS[:13]:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def pollard_brent(n):
    """Devuelve un factor no trivial de n (n compuesto e impar)."""
    while True:
        y = random.randrange(1, n)
        c = random.randrange(1, n)
        lote = 128          # se acumula el producto de |x − y| y se hace un gcd por lote
        g = r = q = 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(lote, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = math.gcd(q, n)
                k += lote
            r *= 2
        if g == n:
            # El lote "se pasó": rehacer paso a paso desde ys.
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
        if g != n:
            return g
        # Si aun así falla, se reintenta con otra constante c.


def factorizar(n, factores):
    """Agrega a `factores` (dict primo → exponente) la factorización de n."""
    for p in PRIMOS_PEQUENOS:
        if p * p > n:
            break
        while n % p == 0:
            factores[p] = factores.get(p, 0) + 1
            n //= p
    pendientes = [n] if n > 1 else []
    while pendientes:
        x = pendientes.pop()
        if x == 1:
            continue
        if es_primo(x):
            factores[x] = factores.get(x, 0) + 1
            continue
        r = math.isqrt(x)
        if r * r == x:          # cuadrados perfectos: Pollard falla con frecuencia
            pendientes += [r, r]
            continue
        d = pollard_brent(x)
        pendientes += [d, x // d]


def suma_divisores(m):
    factores = {}
    factorizar(m, factores)
    total = 1
    for p, e in factores.items():
        total *= (p ** (e + 1) - 1) // (p - 1)
    return total


def resolver(m, k):
    raiz = math.isqrt(k)
    if raiz * raiz == k:
        return 0          # √k entero ⇒ f ≡ 0, nunca vale m > 0
    return suma_divisores(m)


def main():
    random.seed(20170801)
    datos = sys.stdin.buffer.read().split()
    salida = []
    for t in range(0, len(datos) - 1, 2):
        salida.append(str(resolver(int(datos[t]), int(datos[t + 1]))))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
