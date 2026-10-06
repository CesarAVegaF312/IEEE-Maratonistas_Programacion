"""
Programación dinámica — Suma sobre subconjuntos («Sum over Subsets, SOS DP»)
Nivel: Avanzado
Ejecutar: python sos_dp.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Dado un valor f[mask] para cada máscara de B bits, calcular para TODAS
    las máscaras a la vez
        g[mask] = Σ_{sub ⊆ mask} f[sub]          (suma sobre subconjuntos)
    o la versión sobre superconjuntos, en O(B · 2^B) en vez de O(3^B) o
    O(4^B). También sirve con max, min, OR o «algún testigo» en vez de suma,
    y se puede invertir (transformada de Möbius).
    Señales: «para cada x, cuántos elementos y cumplen y & x == y» (y
    submáscara de x), «x & y == 0» (y ⊆ complemento de x), «x | y == x»,
    valores < 2^20, n ≤ 10^6.

FUNCIÓN
    sos_subconjuntos(f, B) -> list      g[mask] = Σ f[sub], sub ⊆ mask.
    sos_superconjuntos(f, B) -> list    g[mask] = Σ f[sup], sup ⊇ mask.
    mobius_subconjuntos(g, B) -> list   inversa: recupera f desde g.
    compatibles(a, B) -> list
        Para cada a[i], algún elemento a[j] del arreglo con a[i] & a[j] == 0
        (puede ser él mismo solo si es 0), o -1 si no hay (Codeforces 165E).
    contar_submascaras(a, B) -> list    para cada a[i], cuántos a[j] son
        submáscara de a[i] (a[j] & a[i] == a[j]), contándose a sí mismo.

IDEA Y ALGORITMO
    Se procesan los bits uno por uno:
      ESTADO      tras procesar los bits 0..b-1, g[mask] = Σ f[sub] sobre
                  las sub ⊆ mask que coinciden con mask en los bits ≥ b
                  (solo pueden diferir en los bits ya procesados).
      TRANSICIÓN  al procesar el bit b, para cada mask con el bit b en 1:
                  g[mask] += g[mask sin el bit b]
                  (las submáscaras con el bit b en 0 llegan desde allí).
      CASO BASE   g = f (ningún bit procesado: solo sub = mask).
      ORDEN       bit b externo (0..B-1); dentro, las máscaras en cualquier
                  orden (mask ^ bit no tiene el bit b, así que no se
                  modifica en esta pasada).
      RESPUESTA   g después de procesar los B bits.
    Es una suma prefija en un hipercubo de B dimensiones con lados de largo
    2: igual que la suma prefija 2D se hace «primero por filas y luego por
    columnas», aquí se hace una dimensión (bit) a la vez.
    Superconjuntos: g[mask] += g[mask | bit] para las mask SIN el bit.
    Möbius (inversa): mismo recorrido restando en vez de sumar.
    Compatibles: testigo[mask] = algún elemento ⊆ mask (el SOS con «tomar
    cualquiera que no sea -1» en vez de sumar). El compatible de x es
    testigo[complemento de x].

MACROALGORITMO
    1. g = copia de f.
    2. Para b = 0..B-1:
    3.    para cada mask con el bit b encendido: g[mask] += g[mask ^ (1<<b)].
    4. Devolver g.

COMPLEJIDAD
    O(B · 2^B) tiempo, O(2^B) memoria. B = 20: 2·10^7 pasos, ~5–10 s en
    Python puro con bucles; usar slicing por bloques para acelerar o B ≤ 18.
    La forma ingenua (recorrer submáscaras de cada máscara) es O(3^B).

EJEMPLO A MANO
    B = 2, f = [1, 2, 3, 4] (f[00]=1, f[01]=2, f[10]=3, f[11]=4)
      bit 0: g[01] += g[00] -> 3;  g[11] += g[10] -> 7      g = [1, 3, 3, 7]
      bit 1: g[10] += g[00] -> 4;  g[11] += g[01] -> 10     g = [1, 3, 4, 10]
    g[11] = 1 + 2 + 3 + 4 = 10 ✓, g[10] = f[00] + f[10] = 4 ✓.

ERRORES TÍPICOS
    - Poner el bucle de máscaras por fuera y el de bits por dentro: suma
      submáscaras repetidas (cuenta de más).
    - Olvidar el complemento dentro de B bits: ~x en Python es negativo;
      usar x ^ (2^B - 1).
    - B demasiado grande para Python (2^22 ya es pesado).
    - Confundir subconjuntos con superconjuntos en el enunciado.

VARIANTES Y RELACIONADOS
    - Transformada OR / AND de convoluciones (zeta + Möbius), contar pares
      con a_i | a_j == x, inclusión–exclusión sobre bits.
    - Enumerar submáscaras: sub = (sub - 1) & mask (O(3^B) total).
    - dp_mascaras.py.

DÓNDE PRACTICAR
    - Externos: Codeforces 165E «Compatible Numbers», Codeforces 449D
      «Jzzhu and Numbers».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta O(4^B) / O(n²) en 300 casos aleatorios
      (B ≤ 7) + casos borde; Möbius(SOS(f)) == f (python sos_dp.py)
"""
import random


def sos_subconjuntos(f, B):
    """g[mask] = Σ f[sub] sobre sub ⊆ mask."""
    g = list(f)
    for b in range(B):                       # una dimensión (bit) a la vez
        bit = 1 << b
        for mask in range(1 << B):
            if mask & bit:
                g[mask] += g[mask ^ bit]
    return g


def sos_superconjuntos(f, B):
    """g[mask] = Σ f[sup] sobre sup ⊇ mask."""
    g = list(f)
    for b in range(B):
        bit = 1 << b
        for mask in range(1 << B):
            if not mask & bit:
                g[mask] += g[mask | bit]
    return g


def mobius_subconjuntos(g, B):
    """Inversa de sos_subconjuntos: recupera f."""
    f = list(g)
    for b in range(B):
        bit = 1 << b
        for mask in range(1 << B):
            if mask & bit:
                f[mask] -= f[mask ^ bit]
    return f


def compatibles(a, B):
    """Para cada x en a, algún y en a con x & y == 0, o -1."""
    testigo = [-1] * (1 << B)                # testigo[mask]: algún elemento ⊆ mask
    for x in a:
        testigo[x] = x
    for b in range(B):
        bit = 1 << b
        for mask in range(1 << B):
            if mask & bit and testigo[mask] == -1:
                testigo[mask] = testigo[mask ^ bit]
    lleno = (1 << B) - 1
    return [testigo[x ^ lleno] for x in a]   # y ⊆ complemento de x  ⇔  x & y == 0


def contar_submascaras(a, B):
    """Para cada x en a, cuántos y en a cumplen y & x == y."""
    f = [0] * (1 << B)
    for x in a:
        f[x] += 1
    g = sos_subconjuntos(f, B)
    return [g[x] for x in a]


def demo():
    print("sos_subconjuntos([1, 2, 3, 4], 2) =", sos_subconjuntos([1, 2, 3, 4], 2))      # [1, 3, 4, 10]
    print("sos_superconjuntos([1, 2, 3, 4], 2) =", sos_superconjuntos([1, 2, 3, 4], 2))  # [10, 6, 7, 4]
    a = [90, 36]
    print("compatibles", a, "->", compatibles(a, 7))                                      # [36, 90]
    a = [3, 6, 3, 6]
    print("compatibles", a, "->", compatibles(a, 3))                                      # [-1]*4
    print("contar_submascaras([1, 3, 2, 7]) ->", contar_submascaras([1, 3, 2, 7], 3))     # [1, 3, 1, 4]


def pruebas():
    random.seed(165)

    # Casos borde
    assert sos_subconjuntos([5], 0) == [5]
    assert compatibles([0], 3) == [0]
    assert compatibles([7], 3) == [-1]
    assert contar_submascaras([0, 0], 1) == [2, 2]

    for _ in range(300):
        B = random.randint(0, 7)
        N = 1 << B
        f = [random.randint(-5, 9) for _ in range(N)]
        sub = [sum(f[s] for s in range(N) if s & m == s) for m in range(N)]
        sup = [sum(f[s] for s in range(N) if s & m == m) for m in range(N)]
        assert sos_subconjuntos(f, B) == sub
        assert sos_superconjuntos(f, B) == sup
        assert mobius_subconjuntos(sub, B) == f

        n = random.randint(1, 15)
        a = [random.randrange(N) for _ in range(n)]
        for x, y in zip(a, compatibles(a, B)):
            existe = any(x & z == 0 for z in a)
            if existe:
                assert y in a and x & y == 0
            else:
                assert y == -1
        assert contar_submascaras(a, B) == [sum(1 for y in a if y & x == y) for x in a]


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
