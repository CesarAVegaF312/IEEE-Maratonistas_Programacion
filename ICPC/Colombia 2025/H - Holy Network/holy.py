"""
Colombia 2025 — H: Holy Network («Red sagrada»)
Ejecutar: python holy.py < holy.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En el Cónclave Arcano cada alquimista trae un ingrediente con un número
    (Resonancia). Un grupo es armónico si TODO par de números del grupo
    comparte un factor mayor que 1 (gcd > 1). Se busca el grupo armónico más
    grande.

QUÉ HAY QUE HACER
    Entrada: varios casos: N y luego N enteros p_i. Termina con N = 0.
    Salida:  por caso, el tamaño del mayor grupo armónico.
    Restricciones clave: N ≤ 50, p_i ≤ 10^12.

IDEA Y ALGORITMO
    Es exactamente el problema de CLIQUE MÁXIMO en el grafo con un vértice
    por número y una arista i–j cuando gcd(p_i, p_j) > 1.
      - Ojo: NO basta con agrupar por un primo común: 6, 10, 15 forman un
        grupo armónico (cada par comparte un primo distinto) sin que haya un
        primo que divida a los tres. Por eso hace falta clique general.
      - Un solo ingrediente siempre forma un grupo válido (no hay pares), así
        que la respuesta es ≥ 1 (p_i = 1 no es compatible con nadie).
    Clique máximo es NP-difícil, pero con N ≤ 50 un BRANCH AND BOUND con
    cotas por COLOREO VORAZ (algoritmo de Tomita, "MCQ") es muy rápido:
      - Conjuntos de vértices como máscaras de bits (enteros de Python):
        intersectar candidatos con vecinos es un AND.
      - En cada nodo se colorean vorazmente los candidatos P: los vértices de
        un mismo color son no adyacentes entre sí, así que una clique puede
        tomar a lo más un vértice por color. Si |R| + #colores ≤ mejor
        conocido, ninguna extensión mejora → se poda.
      - Se ramifica sobre los vértices en orden decreciente de color, y al
        terminar con v se lo saca de P (las cliques con v ya se exploraron).
    Fuerza bruta 2^50 subconjuntos sería imposible; enumerar todas las
    cliques maximales (Bron–Kerbosch) puede ser 3^(50/3) ≈ 10^8 en el peor
    caso; el B&B con coloreo poda mucho más.

MACROALGORITMO
    1. Leer N y los N números; si N = 0, terminar.
    2. Construir ady[i] = máscara de los j ≠ i con gcd(p_i, p_j) > 1.
    3. mejor = 1. Llamar expandir(tamaño=0, P = todos).
    4. En expandir: colorear P vorazmente; recorrer vértices de mayor a menor
       color; podar si tamaño + color ≤ mejor; si no, recursión con
       P ∩ ady[v] (o actualizar mejor si queda vacío); sacar v de P.
    5. Imprimir mejor.

COMPLEJIDAD
    Exponencial en el peor caso teórico, pero en la práctica con N ≤ 50 son
    milisegundos por caso (el gcd de 1225 pares es O(N² log p)).
    Medido: grafos ALEATORIOS de 50 vértices con densidad 0.5–0.95 y el
    grafo de Moon–Moser (el peor para Bron–Kerbosch): ≤ 3 ms por caso.

EJEMPLO A MANO
    30 42 70 105 154: todos pares comparten 2, 3, 5, 7 u 11
    (p. ej. 105 y 154 comparten 7) → clique de 5.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/H")
    - Fuerza bruta (probar todos los subconjuntos, N ≤ 13): OK en 600 casos
      aleatorios con números formados por productos de primos pequeños.
    - La rutina de clique se comparó además con Bron–Kerbosch con pivote en
      300 grafos aleatorios de hasta 50 vértices: OK.
    - Rendimiento: 100 casos con N = 50 de productos de primos chicos ≤ 10^12:
      ~0.1 s en total.
"""
import sys
from math import gcd

sys.setrecursionlimit(10000)


def clique_maxima(n, ady):
    """Tamaño de la clique máxima (ady[i] = máscara de vecinos de i)."""
    mejor = 1 if n > 0 else 0

    def colorear(p):
        """Coloreo voraz de los vértices de la máscara p.
        Devuelve listas (vértices, colores) en orden creciente de color."""
        orden, colores = [], []
        sin_color = p
        color = 0
        while sin_color:
            color += 1
            # Clase de color: vértices de sin_color sin aristas entre sí.
            disponibles = sin_color
            while disponibles:
                bajo = disponibles & -disponibles
                v = bajo.bit_length() - 1
                disponibles &= ~bajo & ~ady[v]  # quita v y sus vecinos
                sin_color &= ~bajo
                orden.append(v)
                colores.append(color)
        return orden, colores

    def expandir(tam, p):
        nonlocal mejor
        orden, colores = colorear(p)
        # Del mayor color al menor: las cotas se ajustan cada vez más.
        for idx in range(len(orden) - 1, -1, -1):
            if tam + colores[idx] <= mejor:
                return  # ni tomando un vértice por color se mejora
            v = orden[idx]
            nuevo_p = p & ady[v]
            if nuevo_p:
                expandir(tam + 1, nuevo_p)
            elif tam + 1 > mejor:
                mejor = tam + 1
            p &= ~(1 << v)  # cliques con v ya exploradas

    expandir(0, (1 << n) - 1)
    return mejor


def resolver(nums):
    n = len(nums)
    ady = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if gcd(nums[i], nums[j]) > 1:  # compatibles: factor común > 1
                ady[i] |= 1 << j
                ady[j] |= 1 << i
    return clique_maxima(n, ady)


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos])
        pos += 1
        if n == 0:  # fin de la entrada
            break
        nums = [int(t) for t in datos[pos:pos + n]]
        pos += n
        salida.append(str(resolver(nums)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
