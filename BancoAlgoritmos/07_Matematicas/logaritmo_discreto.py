"""
Matemáticas — Logaritmo discreto: paso de bebé, paso de gigante («Baby-step giant-step», BSGS)
Nivel: Avanzado
Ejecutar: python logaritmo_discreto.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Hallar el menor x ≥ 0 con a^x ≡ b (mód m), en O(√m) en vez de O(m).
    Es el «logaritmo» en aritmética modular, donde no hay fórmula.
    Señales en el enunciado: «¿después de cuántos pasos el valor
    (multiplicado por a cada vez, módulo m) llega a b?»; «menor exponente x
    con a^x mod m = b»; generadores lineales congruenciales x → a·x (+ c)
    mód m preguntando por el primer instante en que se alcanza un valor;
    orden multiplicativo de a (b = 1, x > 0). Con m hasta ~10^12 en Python.

FUNCIÓN
    log_discreto(a, b, m) -> int
        Menor x ≥ 0 con a^x ≡ b (mód m), o −1 si no existe. m ≥ 1, a y b
        cualesquiera (se reducen módulo m). Convención: a^0 = 1, así que
        si b ≡ 1 la respuesta es 0. Funciona aunque gcd(a, m) ≠ 1.

IDEA Y ALGORITMO
    Caso gcd(a, m) = 1. Sea n = ⌈√m⌉. Todo x en [1, n²] se escribe como
    x = i·n − j con 1 ≤ i ≤ n y 0 ≤ j < n. Entonces
        a^x ≡ b  ⇔  a^(i·n) ≡ b·a^j   (multiplicando por a^j, que es invertible).
    Pasos de bebé: guardar en un diccionario b·a^j → j para j = 0..n−1.
    Pasos de gigante: para i = 1..n calcular (a^n)^i y buscarlo en el
    diccionario. Es un «encuentro en el medio»: n + n operaciones en vez de
    n². Como a^x es periódica con período (el orden de a) ≤ φ(m) < m ≤ n²,
    si existe solución existe una en [0, n²], así que no se pierde nada.
    Mínimo: con i creciente los rangos de x crecen; dentro de un mismo i,
    el x menor es el de j MAYOR, por eso el diccionario guarda el último j
    (se sobrescribe). x = 0 se revisa aparte (¿b ≡ 1?).
    Caso gcd(a, m) = g > 1 (reducción). Para x ≥ 1: a·a^(x−1) − b = m·t
    obliga a que g | b (si no, solo queda la posibilidad x = 0). Dividiendo
    por g:  (a/g)·a^(x−1) ≡ b/g (mód m/g), una ecuación del mismo tipo con
    un coeficiente delante y un módulo menor. Se repite mientras
    gcd(a, m) > 1 (a lo sumo log2 m veces, el módulo se divide al menos por
    2), acumulando el coeficiente c y el desplazamiento k, y antes de cada
    reducción se revisa si x = k ya es solución (c ≡ b). Al final se resuelve
    c·a^y ≡ b (mód m') con gcd(a, m') = 1 por BSGS (c no necesita ser
    invertible: solo se cancela a^j) y la respuesta es k + y.

MACROALGORITMO
    1. Reducir a, b módulo m; c = 1 mód m; k = 0.
    2. Mientras g = gcd(a, m) > 1:
    3.     si c ≡ b → devolver k.   si g ∤ b → devolver −1.
    4.     b /= g; m /= g; c = c·(a/g) mód m; k += 1.
    5. Si c ≡ b → devolver k.
    6. n = ⌈√m⌉; tabla[b·a^j mod m] = j para j = 0..n−1 (el último j gana).
    7. paso = a^n; cur = c; para i = 1..n: cur = cur·paso mod m;
       si cur está en la tabla → devolver k + i·n − tabla[cur].
    8. Devolver −1.

COMPLEJIDAD
    O(√m) tiempo y memoria (diccionario de √m entradas), más O(log² m) de
    la reducción. En Python, m ≈ 10^12 (10^6 entradas) en ~1 s.

EJEMPLO A MANO
    3^x ≡ 13 (mód 17). n = ⌈√17⌉ = 5.
      Bebés b·3^j: j=0: 13, j=1: 39 ≡ 5, j=2: 15, j=3: 45 ≡ 11, j=4: 33 ≡ 16.
      Gigantes (3^5 = 243 ≡ 5): i=1: 5 → está con j = 1 → x = 1·5 − 1 = 4.
      Verificación: 3^4 = 81 = 4·17 + 13 ✓.
    Con gcd ≠ 1: 2^x ≡ 8 (mód 24), c = 1, k = 0:
      g = 2: m 24 → 12, b 8 → 4, c = 1·(2/2) = 1, k = 1
      g = 2: m 12 → 6,  b 4 → 2, c = 1, k = 2
      g = 2: m 6 → 3,   b 2 → 1, c = 1, k = 3
      gcd(2, 3) = 1 y c ≡ b → x = 3 (2^3 = 8 ✓), sin llegar a BSGS.

ERRORES TÍPICOS
    - Aplicar BSGS directo cuando gcd(a, m) ≠ 1: a^j no es invertible y se
      pierden o inventan soluciones. Hacer la reducción.
    - Olvidar x = 0 (b ≡ 1) o, al revés, devolver 0 cuando piden el orden
      (x > 0): para el orden, buscar a^x ≡ 1 con x ≥ 1 (= la respuesta de
      log_discreto(a, a, m) + 1 si gcd(a, m) = 1).
    - Guardar el PRIMER j en la tabla en vez del último: la respuesta sale
      válida pero no mínima.
    - m = 1: todo es ≡ 0 y la respuesta es 0.
    - n = isqrt(m) en lugar de ⌈√m⌉: n² < m y se puede perder la solución.

VARIANTES Y RELACIONADOS
    - Raíz discreta x^k ≡ b (mód p): con una raíz primitiva g, se reduce a
      un logaritmo discreto.
    - Orden multiplicativo: divide a φ(m) (phi_euler.py); también se halla
      probando divisores de φ(m).
    - Pohlig–Hellman: más rápido cuando p − 1 tiene solo factores chicos.
    - Encuentro en el medio general (dividir el espacio en dos mitades).
    - Exponenciación rápida: exponenciacion_rapida.py; inverso:
      euclides_extendido.py.

DÓNDE PRACTICAR
    - En los problemas del repo no aparece.
    - Library Checker «Discrete Logarithm» (con gcd(a, m) ≠ 1)
    - SPOJ MOD «Power Modulo Inverted»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (probar x = 0, 1, 2, … hasta 2m) para
      TODAS las ternas (a, b, m) con m ≤ 40, 3000 ternas aleatorias con
      m ≤ 2000, y con m grandes (hasta 10^10) verificando a^x ≡ b y que
      ningún x menor funcione cuando la respuesta es chica
      (python logaritmo_discreto.py)
"""
import math
import random


def log_discreto(a, b, m):
    """Menor x >= 0 con a^x ≡ b (mod m); -1 si no existe."""
    a %= m
    b %= m
    c = 1 % m                   # ecuación actual: c · a^y ≡ b (mod m), x = k + y
    k = 0
    # Reducción mientras a no sea invertible módulo m
    while (g := math.gcd(a, m)) > 1:
        if c == b:
            return k            # y = 0 funciona
        if b % g:
            return -1           # para y >= 1, g divide al lado izquierdo y no a b
        b //= g
        m //= g
        c = c * (a // g) % m    # se "consumió" un factor a
        k += 1
        a %= m
        b %= m
    if c == b:
        return k                # y = 0
    # BSGS con gcd(a, m) = 1: y = i*n - j, 1 <= i <= n, 0 <= j < n
    n = math.isqrt(m - 1) + 1   # ⌈√m⌉ (n² >= m)
    tabla = {}
    cur = b
    for j in range(n):
        tabla[cur] = j          # se sobrescribe: queda el j MÁS GRANDE (x más chico)
        cur = cur * a % m
    paso = pow(a, n, m)
    cur = c
    for i in range(1, n + 1):
        cur = cur * paso % m    # c · a^(i·n)
        j = tabla.get(cur)
        if j is not None:
            return k + i * n - j
    return -1


def demo():
    print("3^x ≡ 13 (mód 17): x =", log_discreto(3, 13, 17))              # 4
    print("2^x ≡ 8 (mód 24):  x =", log_discreto(2, 8, 24))               # 3
    print("2^x ≡ 3 (mód 7):   x =", log_discreto(2, 3, 7))                # -1
    p = 10**9 + 7
    x = log_discreto(5, 123456789, p)
    print(f"5^x ≡ 123456789 (mód 1e9+7): x = {x}, comprobación:", pow(5, x, p))


def pruebas():
    random.seed(1234)

    def bruto(a, b, m):
        for x in range(2 * m + 2):      # la sucesión a^x mod m se repite antes de 2m
            if pow(a, x, m) == b % m:
                return x
        return -1

    # Casos borde
    assert log_discreto(5, 7, 1) == 0
    assert log_discreto(0, 1, 7) == 0 and log_discreto(0, 0, 7) == 1 and log_discreto(0, 3, 7) == -1
    assert log_discreto(1, 1, 10) == 0 and log_discreto(1, 2, 10) == -1
    assert log_discreto(-1, 6, 7) == 1                  # -1 ≡ 6
    assert log_discreto(2, 0, 16) == 4 and log_discreto(2, 0, 12) == -1

    # Exhaustivo para m pequeños
    for m in range(1, 41):
        for a in range(m):
            for b in range(m):
                assert log_discreto(a, b, m) == bruto(a, b, m), (a, b, m)

    # Aleatorios medianos
    for _ in range(3000):
        m = random.randint(1, 2000)
        a = random.randint(0, 10**6)
        b = random.randint(0, 10**6) if random.random() < 0.5 else pow(a, random.randint(0, 50), m)
        assert log_discreto(a, b, m) == bruto(a, b, m)

    # Módulos grandes: la respuesta es válida y, si es chica, mínima
    for _ in range(40):
        m = random.choice([10**9 + 7, 998244353, random.randint(2, 10**10)])
        a = random.randint(0, m - 1)
        x_real = random.randint(0, 10**6) if random.random() < 0.5 else random.randint(0, 30)
        b = pow(a, x_real, m)
        x = log_discreto(a, b, m)
        assert x != -1 and pow(a, x, m) == b % m and x <= x_real
        if x_real <= 30:
            assert all(pow(a, y, m) != b for y in range(x))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
