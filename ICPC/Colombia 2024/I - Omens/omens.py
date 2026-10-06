"""
Colombia 2024 — I: Omens («Presagios»)
Ejecutar: python omens.py < omens.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En el Día de los Presagios de Fomana, la Oráculo Real lanza dos Piedras
    Sagradas (puntos uniformes e independientes) dentro del Rectángulo de la
    Fortuna L × W y traza el Círculo del Destino que tiene a las dos piedras
    como extremos de un diámetro. Es buen presagio si el círculo queda
    completamente dentro del rectángulo.

QUÉ HAY QUE HACER
    Entrada: varias líneas "L W" (1 ≤ L, W ≤ 1000) terminadas en "0 0".
    Salida:  por caso, la probabilidad de buen presagio con 4 decimales.

IDEA Y ALGORITMO
    Probabilidad geométrica con cambio de variables (integral cerrada).
    Sean P, Q las piedras. Centro M = (P+Q)/2 y semidiferencia D = (P−Q)/2;
    el círculo tiene centro M y radio |D|. El cambio (P, Q) → (M, D) en R⁴
    tiene jacobiano 4 (P = M + D, Q = M − D; en cada eje |det[[1,1],[1,−1]]|
    = 2, y hay dos ejes), así que dP dQ = 4 dM dD.
    El círculo cabe ⇔ |D| ≤ d(M), donde d(M) = distancia de M al borde del
    rectángulo (mín(Mx, L−Mx, My, W−My)). Si cabe, P y Q también están dentro
    (son puntos del círculo), así que no hay restricción extra. Para un M
    fijo, los D válidos forman un disco de área π·d(M)². Entonces
        Prob = 4/(L²W²) · ∫_rect π·d(M)² dM.
    Para integrar d² usamos la "fórmula de las capas": el conjunto de puntos
    con d(M) ≥ t es un rectángulo (L−2t)(W−2t), para 0 ≤ t ≤ a/2 con
    a = mín(L, W), b = máx(L, W). Como d² = ∫₀^d 2t dt,
        ∫ d² dM = ∫₀^{a/2} 2t (L−2t)(W−2t) dt = a³b/12 − a⁴/24.
    Sustituyendo y simplificando:
        Prob = π · a · (2b − a) / (6 b²).
    Comprobación: L = W = 1 ⇒ π/6 = 0.5236 ✔; 20×40 ⇒ π/8 = 0.3927 ✔.

MACROALGORITMO
    1. Leer L, W hasta "0 0".
    2. a = mín(L, W), b = máx(L, W).
    3. Imprimir π·a·(2b − a)/(6b²) con 4 decimales.

COMPLEJIDAD
    O(1) por caso.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/I")
    - Fuerza bruta: simulación Monte Carlo (10⁶ lanzamientos) para 8
      rectángulos distintos: la diferencia con la fórmula es < 0.002 en todos
      (error estadístico esperado ≈ 0.0005); además la integral ∫ d² se
      comparó con una suma de Riemann en malla fina (error < 10⁻⁵).
    - Redondeo: "%.4f" (como printf de C), sin casos de empate prácticos
      porque el valor es irracional (múltiplo de π).
"""
import math
import sys


def probabilidad(L, W):
    """Probabilidad de que el círculo de diámetro PQ quepa en el rectángulo."""
    a, b = min(L, W), max(L, W)
    return math.pi * a * (2 * b - a) / (6 * b * b)


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for i in range(0, len(datos) - 1, 2):
        L, W = int(datos[i]), int(datos[i + 1])
        if L == 0 and W == 0:
            break
        salida.append("%.4f" % probabilidad(L, W))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
