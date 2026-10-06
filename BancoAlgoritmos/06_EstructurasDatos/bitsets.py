"""
Estructuras de datos — Enteros de Python como bitsets («Bitset with Python big ints»)
Nivel: Intermedio
Ejecutar: python bitsets.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Un int de Python tiene tamaño arbitrario: un entero de N bits ES un
    conjunto de {0..N-1} (bit i encendido = i pertenece). Las operaciones
    &, |, ^, <<, >> sobre él se ejecutan en C de a ~30–64 bits por
    instrucción, así que procesar N elementos «a la vez» cuesta ~N/64. Es el
    equivalente al std::bitset de C++ y en Python es a menudo la ÚNICA
    forma de que un O(N²) o un O(N·S) pase.
    Usos típicos:
      - Subset sum / mochila de factibilidad: alcanzables |= alcanzables << w.
      - Intersección masiva de conjuntos: «qué elementos cumplen TODAS estas
        condiciones» = AND de los bitsets de cada condición.
      - Contar triángulos, alcanzabilidad (cierre transitivo) por filas.
    Señales en el enunciado: «¿se puede formar la suma S?» con S·N ~ 10^8,
    N hasta 2·10^4 con comparación de todos los pares, conjuntos sobre un
    universo de hasta ~10^5–10^6 elementos.

FUNCIÓN
    sumas_alcanzables(pesos, limite) -> int
        Bitset: bit s encendido ⇔ alguna submulticolección de pesos suma s
        (s <= limite). Cada peso se usa a lo sumo una vez.
    se_puede_partir(pesos) -> bool
        ¿Se pueden repartir en dos grupos de igual suma?
    bits_encendidos(x) -> list[int]
        Índices de los bits encendidos de x, en orden creciente.
    coincidencias(secuencias) -> list[list[int]]
        Para cada secuencia m (cadenas de igual largo sobre A,C,G,T y el
        comodín '-'), los índices j < m compatibles con ella (en cada
        posición, igual letra o algún '-'). Es el núcleo de OMP 2017 C.

IDEA Y ALGORITMO
    1. Subset sum: alc = 1 (solo la suma 0). Agregar un peso w a todas las
       sumas alcanzables = desplazar el conjunto w posiciones:
       alc |= alc << w. Recortar con & ((1 << (limite+1)) - 1) para que el
       entero no crezca de más. O(N · limite / 64) en vez de O(N · limite)
       de la DP booleana con listas.
    2. AND masivo: precalcular, para cada (posición p, letra x), el bitset
       compat[p][x] = {secuencias s : s[p] == x o s[p] == '-'}. La
       secuencia m coincide con s ⇔ para toda p donde m tiene letra x, s
       está en compat[p][x]. Entonces
           coinciden(m) = (2^m − 1) & AND_{p: m[p] ≠ '-'} compat[p][m[p]]
       (la máscara 2^m − 1 deja solo las anteriores). Un AND de enteros de
       N bits son N/64 operaciones en C, contra N comparaciones de cadenas
       de Python.
    Construcción rápida: armar la cadena de '0'/'1' y convertir con
    int(cadena, 2) (encender bits uno a uno con x |= 1 << i copia el entero
    cada vez: O(N²)). Ojo: en int(s, 2) el PRIMER carácter es el bit más
    alto, por eso se invierte la cadena.
    Listar los bits: bin(x)[:1:-1] da los bits del menos al más
    significativo; se toman las posiciones con '1' (o, para pocos bits,
    repetir x & -x).

MACROALGORITMO
    Subset sum:
    1. alc = 1; mascara = (1 << (limite + 1)) - 1.
    2. Para cada w: alc = (alc | (alc << w)) & mascara.
    3. La suma s es posible ⇔ (alc >> s) & 1.
    Coincidencias:
    1. Para cada posición p y letra x: cadena con '1' en las s compatibles;
       compat[p][x] = int(cadena invertida, 2).
    2. Para cada m: res = (1 << m) - 1; para cada p con letra x:
       res &= compat[p][x]; si res == 0, cortar.
    3. Listar los bits de res.

COMPLEJIDAD
    Subset sum: O(N · S / w) con w ≈ 30–64 (palabra de máquina);
    N = 1000, S = 10^5 en ~0,05 s. Coincidencias: O(L · N² / w) en el peor
    caso (más el tamaño de la salida, que puede ser O(N²) si casi todo
    coincide); N = 2·10^4, L = 100 aleatorias en ~1 s.
    Memoria O(L · 4 · N / 8) bytes.

EJEMPLO A MANO
    pesos [3, 5, 6], limite 15:
      alc = 1                  {0}
      << 3: 1001b              {0, 3}
      << 5: 100101001b         {0, 3, 5, 8}
      << 6: {0,3,5,8} ∪ {6,9,11,14} = {0,3,5,6,8,9,11,14}
    se_puede_partir([3, 1, 1, 2, 2, 1]): total 10, ¿suma 5? sí (3+2).
    coincidencias(["AC-", "A-G", "TCG"]):
      m=1 "A-G": con "AC-": A=A, C/-, -/G → compatible → [0]
      m=2 "TCG": con "AC-": T≠A → no; con "A-G": T≠A → no → []

ERRORES TÍPICOS
    - No recortar el bitset con la máscara: crece hasta Σ pesos bits y se
      vuelve lento.
    - Construir bitsets con |= 1 << i dentro de un ciclo largo (cuadrático).
    - Olvidar que int('0101', 2) lee de izquierda a derecha como bit alto
      primero.
    - Usar este truco para la mochila de VALOR máximo: el bitset solo dice
      sí/no, no maximiza valores.

VARIANTES Y RELACIONADOS
    - x.bit_count() (Python 3.10+) cuenta los bits encendidos: tamaño de
      un conjunto o de una intersección en O(N/64).
    - Subset sum con muchos pesos repetidos: agrupar en potencias de 2
      (descomposición binaria) para reducir el número de desplazamientos.
    - Distancia de edición bit-paralela (Myers) y LCS bit-paralela: misma
      idea, sumas y desplazamientos sobre enteros grandes.
    - DP sobre máscaras de bits (subconjuntos pequeños, N <= 20) es otra
      técnica distinta aunque use bits.

DÓNDE PRACTICAR
    - ICPC/OMP 2017 Murcia/C - The Broken DNA of Jack the Ripper (AND de
      bitsets por posición y letra: coincidencias)
    - ICPC/Colombia 2026/M - Byte Flu (distancia de edición bit-paralela de
      Myers con enteros grandes)
    - CSES «Money Sums» (subset sum, se puede con bitset).

VERIFICACIÓN
    - Pruebas (python bitsets.py): sumas_alcanzables contra la DP con
      conjuntos de Python en 800 casos; se_puede_partir contra fuerza bruta
      sobre subconjuntos en 500 casos; coincidencias contra la comparación
      directa de todos los pares en 300 casos; bits_encendidos contra un
      ciclo bit a bit; más casos borde y un caso grande de tiempo.
"""
import random


def sumas_alcanzables(pesos, limite):
    """Bitset de las sumas s <= limite que se pueden formar (cada peso una vez)."""
    mascara = (1 << (limite + 1)) - 1
    alc = 1                                  # solo la suma 0
    for w in pesos:
        alc = (alc | (alc << w)) & mascara   # a cada suma alcanzable se le suma w
    return alc


def se_puede_partir(pesos):
    """¿Hay un subconjunto con exactamente la mitad de la suma total?"""
    total = sum(pesos)
    if total % 2:
        return False
    return bool(sumas_alcanzables(pesos, total // 2) >> (total // 2) & 1)


def bits_encendidos(x):
    """Índices de los bits en 1 de x (x >= 0), de menor a mayor."""
    # bin(x) = '0b…'; [:1:-1] lo invierte y quita el '0b': el carácter k es el bit k.
    return [k for k, c in enumerate(bin(x)[:1:-1]) if c == "1"]


def coincidencias(secuencias):
    """Para cada m, los j < m compatibles (igual letra o '-' en cada posición)."""
    n = len(secuencias)
    if n == 0:
        return []
    largo = len(secuencias[0])
    # compat[p][x]: bitset de las secuencias que aceptan la letra x en la posición p.
    compat = []
    for p in range(largo):
        col = [s[p] for s in secuencias]
        fila = {}
        for x in "ACGT":
            cadena = "".join("1" if c == x or c == "-" else "0" for c in col)
            fila[x] = int(cadena[::-1], 2)   # invertida: el carácter s va al bit s
        compat.append(fila)
    res = []
    for m, s in enumerate(secuencias):
        conj = (1 << m) - 1                  # solo las anteriores
        for p, x in enumerate(s):
            if x != "-":
                conj &= compat[p][x]
                if not conj:
                    break                    # ya no queda nadie
        res.append(bits_encendidos(conj))
    return res


def demo():
    alc = sumas_alcanzables([3, 5, 6], 15)
    print("pesos [3, 5, 6]: sumas alcanzables <= 15 ->", bits_encendidos(alc))
    print("se_puede_partir([3, 1, 1, 2, 2, 1]) =", se_puede_partir([3, 1, 1, 2, 2, 1]))  # True
    secs = ["AC-", "A-G", "TCG"]
    print("coincidencias", secs, "->", coincidencias(secs))     # [[], [0], []]


def _compatibles(a, b):
    return all(x == y or x == "-" or y == "-" for x, y in zip(a, b))


def pruebas():
    random.seed(2017)

    # Casos borde
    assert sumas_alcanzables([], 10) == 1 and bits_encendidos(1) == [0]
    assert bits_encendidos(0) == []
    assert sumas_alcanzables([20], 10) == 1                # peso mayor que el límite
    assert se_puede_partir([]) and not se_puede_partir([1])
    assert se_puede_partir([7, 7]) and not se_puede_partir([1, 2])
    assert coincidencias([]) == [] and coincidencias(["A"]) == [[]]
    assert coincidencias(["---", "ACG", "TTT"]) == [[], [0], [0]]

    # bits_encendidos contra un ciclo bit a bit
    for _ in range(300):
        x = random.getrandbits(random.randint(0, 200))
        assert bits_encendidos(x) == [k for k in range(x.bit_length()) if x >> k & 1]

    # Subset sum contra conjuntos de Python
    for _ in range(800):
        pesos = [random.randint(0, 15) for _ in range(random.randint(0, 10))]
        limite = random.randint(0, 60)
        sumas = {0}
        for w in pesos:
            sumas |= {s + w for s in sumas}
        assert bits_encendidos(sumas_alcanzables(pesos, limite)) == \
            sorted(s for s in sumas if s <= limite)

    # Partición contra todos los subconjuntos
    for _ in range(500):
        pesos = [random.randint(1, 10) for _ in range(random.randint(0, 10))]
        n, total = len(pesos), sum(pesos)
        bruta = any(2 * sum(pesos[i] for i in range(n) if m >> i & 1) == total
                    for m in range(1 << n))
        assert se_puede_partir(pesos) == bruta

    # Coincidencias contra todos los pares
    for _ in range(300):
        largo = random.randint(1, 6)
        secs = ["".join(random.choice("ACGT--") for _ in range(largo))
                for _ in range(random.randint(1, 15))]
        assert coincidencias(secs) == [[j for j in range(m) if _compatibles(secs[j], s)]
                                       for m, s in enumerate(secs)]

    # Tiempo: subset sum con 1000 pesos y límite 10^5
    pesos = [random.randint(1, 1000) for _ in range(1000)]
    assert sumas_alcanzables(pesos, 100000) & 1


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
