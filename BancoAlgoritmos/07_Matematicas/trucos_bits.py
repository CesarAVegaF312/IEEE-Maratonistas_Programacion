"""
Matemáticas — Trucos de bits y XOR: x & -x, popcount, submáscaras, contribución por bit
Nivel: Básico/Intermedio
Ejecutar: python trucos_bits.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Operar con enteros como conjuntos de bits (máscaras) en O(1), y
    resolver sumas sobre XOR (o AND/OR) separando la cuenta POR BIT: cada
    bit se comporta de forma independiente.
    Cómo reconocerlo: «XOR» en el enunciado; n ≤ 20 elementos (subconjuntos
    como máscaras); «suma de a_i XOR a_j sobre todos los pares /
    subarreglos» con n = 10^5 (O(n²) no alcanza); nodos que son cadenas
    binarias (hipercubos); «cuántos bits en 1».

FUNCIÓN
    bit_bajo(x) -> int              x & -x: el bit 1 más bajo (como valor 2^i)
    sin_bit_bajo(x) -> int          x & (x − 1): apaga el bit 1 más bajo
    popcount(x) -> int              número de bits en 1 (x.bit_count())
    bits(x) -> list[int]            posiciones de los bits en 1 (de menor a mayor)
    submascaras(m) -> list[int]     todas las submáscaras de m (incluye 0 y m)
    xor_0_a_n(n) -> int             0 ⊕ 1 ⊕ … ⊕ n en O(1)
    suma_xor_pares(a) -> int        Σ_{i<j} a_i ⊕ a_j en O(n · bits)
    suma_xor_subarreglos(a) -> int  Σ_{l≤r} a_l ⊕ … ⊕ a_r en O(n · bits)
    costo_bits(a, b) -> int         Σ (i + 1) sobre los bits i de a ⊕ b
                                    (Colombia 2026 H: cambiar el bit i cuesta i+1)

IDEA Y ALGORITMO
    - x & -x: en complemento a dos −x = ~x + 1. ~x invierte todo; sumar 1
      convierte los ceros finales de ~x (que eran los ceros finales de x) en
      0 y enciende el primer bit 1 de x. Así x y −x coinciden SOLO en ese bit.
    - x & (x − 1): restar 1 apaga el bit 1 más bajo y enciende los ceros a
      su derecha; el AND borra todo eso. Repetirlo recorre los bits en
      O(popcount) (también: x es potencia de 2 ⇔ x > 0 y x & (x−1) == 0).
    - Submáscaras: s = (s − 1) & m da la siguiente submáscara MENOR de m
      (restar 1 y quitar los bits fuera de m). Recorrer las submáscaras de
      todas las máscaras de n bits cuesta Σ 2^{popcount} = 3^n.
    - Propiedades del XOR: asociativo, conmutativo, x ⊕ x = 0, x ⊕ 0 = x;
      por eso XOR de un rango = pre[r+1] ⊕ pre[l] (prefijos), y
      xor_0_a_n tiene periodo 4: n, 1, n+1, 0 según n mód 4 (cada par
      (2k, 2k+1) da 1).
    - Contribución por bit: el bit b de x ⊕ y vale 1 ⇔ exactamente uno de
      x, y tiene el bit b. Entonces
        Σ_{i<j} a_i ⊕ a_j = Σ_b 2^b · (#con bit b en 1) · (#con bit b en 0).
      Para subarreglos: XOR(l..r) = pre[r+1] ⊕ pre[l], así que es la misma
      cuenta sobre los n+1 prefijos.
    - Hipercubo (Colombia 2026 H): para ir de a a b hay que cambiar un
      número impar de veces cada bit de a ⊕ b y par los demás; con costos
      positivos lo óptimo es cambiar cada bit de a ⊕ b una sola vez.

MACROALGORITMO
    1. Representar conjuntos pequeños como máscaras (bit i = elemento i).
    2. Para recorrer bits o submáscaras usar x & (x−1) / (s−1) & m.
    3. Para sumas de XOR: para cada bit b, contar cuántos números (o
       prefijos) lo tienen en 1 (c1) y en 0 (c0).
    4. Sumar c1 · c0 · 2^b sobre todos los bits.
    5. Para XOR de rangos usar prefijos: x(l..r) = pre[r+1] ⊕ pre[l].

COMPLEJIDAD
    Operaciones de bits: O(1) (en Python, enteros grandes O(bits/30)).
    suma_xor_pares / subarreglos: O(n · B) con B = número de bits (≈ 30):
    n = 10^5 en ~0,5 s. Submáscaras de todas las máscaras: O(3^n), n ≤ 15.

EJEMPLO A MANO
    x = 12 = 1100₂: x & -x = 0100₂ = 4; x & (x−1) = 1000₂ = 8; popcount 2.
    a = [1, 2, 3]: bit 0: unos {1,3} = 2, ceros 1 → 2·1·1 = 2;
    bit 1: unos {2,3} = 2, ceros 1 → 2·1·2 = 4. Total 6 = (1⊕2)+(1⊕3)+(2⊕3)
    = 3 + 2 + 1. ✔
    Colombia 2026 H: a = 0 (000), b = 5 (101): bits 0 y 2 → 1 + 3 = 4.

ERRORES TÍPICOS
    - Precedencia: en Python (y C++) «x & 1 == 0» se lee x & (1 == 0);
      usar paréntesis: (x & 1) == 0.
    - Olvidar la submáscara 0 al recorrer con s = (s−1) & m (el bucle
      termina en 0; procesarla aparte o usar «while True … if s == 0: break»).
    - En C++, 1 << 40 desborda (usar 1LL << 40); en Python no.
    - Contribución por bit: contar pares ordenados en vez de i < j (o al revés).
    - Olvidar el prefijo vacío pre[0] = 0 en la versión de subarreglos.

VARIANTES Y RELACIONADOS
    - Base XOR (Gauss en GF(2)): máximo XOR de un subconjunto
      (eliminacion_gaussiana.py).
    - Trie binario: máximo a_i ⊕ a_j en O(n · B).
    - Suma sobre subconjuntos (SOS DP) en O(n 2^n).
    - Código Gray: g(i) = i ⊕ (i >> 1), consecutivos difieren en un bit.
    - nim_sprague_grundy.py (el XOR decide los juegos de Nim).
    - DP sobre máscaras (programación dinámica con subconjuntos).

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/H - HCubes Costs (XOR + costo por bit: costo_bits)
    - ICPC/Colombia 2018/B - Forming Better Groups (DP sobre máscaras con
      (libres & -libres) para el menor elemento libre)
    - ICPC/Colombia 2024/F - Turnswitch (filas como máscaras; girar p
      cambia la fila por p ⊕ (p << 1) ⊕ (p >> 1))
    - ICPC/OMP 2017 Murcia/C - The Broken DNA of Jack the Ripper (enteros
      grandes como bitsets)
    - CSES «Gray Code», «Counting Bits», «Maximum Xor Subarray»

VERIFICACIÓN
    - Pruebas: OK contra versiones directas (recorrer bit a bit, bin(x).count,
      probar todas las máscaras ⊆ m, doble/triple bucle para sumas de XOR)
      en 2000 casos aleatorios + casos borde (python trucos_bits.py)
"""
import heapq
import random


def bit_bajo(x):
    """Valor del bit 1 más bajo de x (0 si x == 0)."""
    return x & -x


def sin_bit_bajo(x):
    """x sin su bit 1 más bajo."""
    return x & (x - 1)


def popcount(x):
    """Número de bits en 1 de x ≥ 0."""
    return x.bit_count()            # Python 3.10+; antes: bin(x).count("1")


def bits(x):
    """Posiciones de los bits en 1 de x, de menor a mayor (O(popcount))."""
    res = []
    while x:
        b = x & -x
        res.append(b.bit_length() - 1)
        x ^= b                      # quitar ese bit
    return res


def submascaras(m):
    """Todas las submáscaras de m en orden decreciente (incluye m y 0)."""
    res = []
    s = m
    while True:
        res.append(s)
        if s == 0:
            break
        s = (s - 1) & m             # siguiente submáscara menor
    return res


def xor_0_a_n(n):
    """0 ⊕ 1 ⊕ … ⊕ n (periodo 4)."""
    return (n, 1, n + 1, 0)[n % 4]


def suma_xor_pares(a):
    """Σ_{i<j} a[i] ⊕ a[j] contando por bit."""
    n = len(a)
    total = 0
    B = max(a, default=0).bit_length()
    for b in range(B):
        unos = sum((x >> b) & 1 for x in a)
        total += unos * (n - unos) << b      # pares con exactamente un bit b en 1
    return total


def suma_xor_subarreglos(a):
    """Σ sobre subarreglos no vacíos del XOR del subarreglo (prefijos + por bit)."""
    pre = [0]
    for x in a:
        pre.append(pre[-1] ^ x)              # XOR(l..r) = pre[r+1] ⊕ pre[l]
    return suma_xor_pares(pre)


def costo_bits(a, b):
    """Σ (i + 1) sobre los bits i en los que a y b difieren."""
    return sum(i + 1 for i in bits(a ^ b))


def demo():
    x = 12
    print(f"x = {x} = {x:b}b: x&-x = {bit_bajo(x)}, x&(x-1) = {sin_bit_bajo(x)}, "
          f"popcount = {popcount(x)}, bits = {bits(x)}")
    print("submáscaras de 1011b:", [f"{s:04b}" for s in submascaras(0b1011)])
    print("suma XOR de pares [1,2,3]:", suma_xor_pares([1, 2, 3]))            # 6
    print("suma XOR de subarreglos [1,2,3]:", suma_xor_subarreglos([1, 2, 3]))  # 1+2+3+3+1+0 = 10
    print("Colombia 2026 H, 0 -> 5:", costo_bits(0, 5))                         # 4
    print("Gray de 0..7:", [i ^ (i >> 1) for i in range(8)])


def pruebas():
    random.seed(2026)

    # Casos borde
    assert bit_bajo(0) == 0 and sin_bit_bajo(0) == 0 and popcount(0) == 0 and bits(0) == []
    assert submascaras(0) == [0]
    assert suma_xor_pares([]) == 0 and suma_xor_pares([5]) == 0
    assert suma_xor_subarreglos([]) == 0 and suma_xor_subarreglos([7]) == 7
    assert costo_bits(9, 9) == 0

    for _ in range(2000):
        x = random.choice([random.randint(1, 2**20), random.randint(1, 2**70)])
        # bit bajo: el menor i con bit i en 1, recorriendo bit a bit
        i = 0
        while not (x >> i) & 1:
            i += 1
        assert bit_bajo(x) == 1 << i
        assert sin_bit_bajo(x) == x - (1 << i)
        assert popcount(x) == bin(x).count("1")
        assert bits(x) == [j for j in range(x.bit_length()) if (x >> j) & 1]
        assert ((x & (x - 1)) == 0) == (bin(x).count("1") == 1)

    for m in range(0, 1 << 8):
        esperado = sorted((s for s in range(m + 1) if s & m == s), reverse=True)
        assert submascaras(m) == esperado

    acc = 0
    for n in range(0, 300):
        acc ^= n
        assert xor_0_a_n(n) == acc

    for _ in range(300):
        a = [random.randint(0, 1000) for _ in range(random.randint(0, 25))]
        n = len(a)
        assert suma_xor_pares(a) == sum(a[i] ^ a[j] for i in range(n) for j in range(i + 1, n))
        bruto = 0
        for l in range(n):
            x = 0
            for r in range(l, n):
                x ^= a[r]
                bruto += x
        assert suma_xor_subarreglos(a) == bruto

    # Colombia 2026 H: costo mínimo = camino más barato en el hipercubo (Dijkstra pequeño)
    for nbits in range(1, 6):
        N = 1 << nbits
        for a in range(N):
            dist = [None] * N
            pq = [(0, a)]
            while pq:
                d, u = heapq.heappop(pq)
                if dist[u] is not None:
                    continue
                dist[u] = d
                for i in range(nbits):
                    v = u ^ (1 << i)
                    if dist[v] is None:
                        heapq.heappush(pq, (d + i + 1, v))
            assert all(dist[b] == costo_bits(a, b) for b in range(N))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
