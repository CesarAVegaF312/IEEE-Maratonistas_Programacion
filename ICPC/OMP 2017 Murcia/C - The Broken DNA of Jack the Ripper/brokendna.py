"""
OMP 2017 Murcia — C: The Broken DNA of Jack the Ripper («El ADN roto de Jack el Destripador»)
Ejecutar: python brokendna.py < brokendna.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    La policía quiere identificar a Jack el Destripador comparando secuencias
    de ADN antiguas. Las secuencias usan A, C, G, T y tienen partes perdidas,
    marcadas con '-', que pueden corresponder a cualquier letra.

QUÉ HAY QUE HACER
    Entrada: N (≤ 20000) y luego N secuencias, todas de la misma longitud
    L ≤ 100, sobre el alfabeto {A, C, G, T, -}.
    Salida:  para cada secuencia M que coincide con alguna anterior, una
    línea "M: S1 S2 … Sn" con los números (1-indexados, crecientes) de las
    secuencias anteriores con las que coincide. Si no coincide con ninguna
    anterior, no se imprime nada.
    Dos secuencias coinciden si en TODAS las posiciones los caracteres son
    iguales o al menos uno de los dos es '-'.
    Restricciones clave: comparar todos los pares cuesta N²/2·L ≈ 2·10^10
    operaciones: imposible en Python.

IDEA Y ALGORITMO
    Bitsets (enteros grandes de Python) por (posición, letra) + intersección.
    Para cada posición p y letra x ∈ {A,C,G,T} se precalcula el conjunto
        compat[p][x] = { secuencias s : s[p] == x  o  s[p] == '-' }
    como un entero de N bits (bit s encendido si s está en el conjunto).
    La secuencia m coincide con s ⇔ para cada posición p donde m tiene una
    letra x (no '-'), s está en compat[p][x]. Las posiciones donde m tiene
    '-' no imponen nada. Así:
        coincidencias(m) = (2^m - 1)  AND  ⋂_{p : m[p] ≠ '-'} compat[p][m[p]]
    donde la máscara 2^m - 1 deja solo las secuencias ANTERIORES (bits
    0..m-1). Cada AND de enteros grandes se ejecuta en C a ~30 bits por
    operación de máquina, y el resultado de un AND tiene el tamaño del
    operando más corto; se empieza por la máscara de m bits, así que el
    trabajo para la secuencia m es O(L·m/30) y se corta en cuanto el
    conjunto queda vacío.
    Los conjuntos se construyen de una vez armando, para cada (p, x), una
    cadena de '0'/'1' y convirtiéndola con int(cadena, 2) (mucho más rápido
    que encender bits uno a uno, que copiaría el entero cada vez).
    Para listar los bits encendidos se usa la representación binaria
    invertida, convertida a bytes 0/1, con itertools.compress sobre una
    lista de etiquetas precalculadas: todo el recorrido ocurre en C.

MACROALGORITMO
    1. Leer N y las N secuencias.
    2. Para cada posición p y letra x: construir el bitset compat[p][x]
       (bit s = 1 si s[p] es x o '-').
    3. Para cada secuencia m (en orden):
       a. conjunto = máscara de las m secuencias anteriores.
       b. Para cada p con m[p] ≠ '-': conjunto &= compat[p][m[p]]; si queda
          vacío, parar.
       c. Si el conjunto no es vacío, extraer sus bits en orden creciente e
          imprimir "m+1: …" (1-indexado).

COMPLEJIDAD
    Construcción O(4·L·N). Consultas O(L·N²/w) en el peor caso con w ≈ 30
    (bits por "dígito" de los enteros de Python), más el tamaño de la salida.
    Medido (N = 20000): L = 100 con 50 % de '-' (casi sin coincidencias)
    ~0.85 s; L = 20 con 50 % de '-' (3·10^6 pares, salida 16 MB) ~2.3 s;
    L = 100 con 90 % de '-' (~9·10^7 pares, salida 487 MB) ~6.8 s, dominado
    por escribir la salida. El peor caso absoluto (todas "-----", ~2·10^8
    números, ~1.2 GB de salida) no se probó: ahí manda el tamaño de la
    salida en cualquier lenguaje.

EJEMPLO A MANO
    Secuencia 8 = "ACACAC". Anteriores: 1 AC-CG- (falla en la 5.ª posición:
    G vs A), 2 A-A-GG (5.ª: G vs A), 3 ACACGT y 4 ACACGG (5.ª: G vs A),
    5 ACACAC (igual), 6 ---TT- (4.ª: T vs C), 7 ------ (comodín total).
    Resultado "8: 5 7".

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "OMP 2017/C")
    - Fuerza bruta: OK en 500 casos aleatorios (N ≤ 30, L ≤ 6, distintas
      probabilidades de '-') contra la comparación literal de todos los
      pares, carácter a carácter.
"""
import sys
from itertools import compress

LETRAS = "ACGT"


def construir_compatibles(secuencias, longitud):
    """compat[p][x] = bitset de secuencias con letra x o '-' en la posición p.

    El bit s corresponde a la secuencia s (0-indexada). Se arma la cadena
    binaria al revés (bit más significativo primero) y se convierte con int().
    """
    compat = []
    for p in range(longitud):
        columna = [s[p] for s in secuencias]
        por_letra = {}
        for x in LETRAS:
            # '1' si la secuencia es compatible con la letra x en p.
            bits = "".join("1" if (c == x or c == "-") else "0" for c in reversed(columna))
            por_letra[x] = int(bits, 2) if bits else 0
        compat.append(por_letra)
    return compat


# Tabla para bytes.translate: b'0' -> byte 0 (falso), b'1' -> byte 1 (verdadero).
CERO_UNO = bytes.maketrans(b"01", bytes([0, 1]))


def numeros_de_bits(conjunto, etiquetas):
    """Etiquetas (números 1-indexados como texto) de los bits a 1, en orden.

    bin() da los bits del más significativo al menos; al invertir, el
    carácter i corresponde al bit i (secuencia i). Se convierte a bytes 0/1
    y itertools.compress elige las etiquetas: todo el recorrido ocurre en C.
    """
    binario = bin(conjunto)[:1:-1]          # quita '0b' e invierte
    selector = binario.encode("ascii").translate(CERO_UNO)
    return compress(etiquetas, selector)


def main():
    datos = sys.stdin.read().split()
    n = int(datos[0])
    secuencias = datos[1:1 + n]
    if not secuencias:
        return
    longitud = len(secuencias[0])
    compat = construir_compatibles(secuencias, longitud)

    # Texto de cada número de secuencia, precalculado una sola vez.
    etiquetas = [str(i + 1) for i in range(n)]
    salida = []
    for m, sec in enumerate(secuencias):
        if m == 0:
            continue                      # la primera no tiene anteriores
        conjunto = (1 << m) - 1           # solo las secuencias 0..m-1
        for p, c in enumerate(sec):
            if c == "-":
                continue                  # comodín: no restringe nada
            conjunto &= compat[p][c]
            if not conjunto:
                break                     # ya no coincide con ninguna
        if conjunto:
            numeros = " ".join(numeros_de_bits(conjunto, etiquetas))
            salida.append(f"{m + 1}: {numeros}")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
