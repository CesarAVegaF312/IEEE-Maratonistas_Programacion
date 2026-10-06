"""
Colombia 2017 — E: Rational Coins («Monedas racionales»)
Ejecutar: python coins.py < coins.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En Ratioland hay monedas de 1/q Rations con radio 1/(2q^2). En un marco se
    colocan: M(0/1) y M(1/1) con centros (0, 1/2) y (1, 1/2), y para cada
    fracción irreducible 0 < p/q < 1 la moneda M(p/q) con centro
    (p/q, 1/(2q^2)). Todas tocan el eje x. (Son los CÍRCULOS DE FORD.)

QUÉ HAY QUE HACER
    Entrada: varios casos hasta EOF; cada uno "p q n" con p/q irreducible,
             0 <= p/q <= 1.
    Salida:  por caso, en una línea, los nombres "M(r/s)" de las primeras n
             monedas que tocan a M(p/q), ordenadas por s creciente (radio
             decreciente) y, a igual s, por r creciente.
    Restricciones clave: q <= 10^6, n <= 1000.

IDEA Y ALGORITMO
    Propiedad de los círculos de Ford: los círculos de p/q y r/s son
    tangentes si y sólo si |p*s - r*q| = 1, y nunca se superponen.
    (Distancia^2 entre centros = (p/q - r/s)^2 + (1/(2q^2) - 1/(2s^2))^2 y
    (suma de radios)^2 = (1/(2q^2) + 1/(2s^2))^2; restando queda
    (ps - rq)^2/(qs)^2 = 1/(q s)^2  <=>  |ps - rq| = 1.)
    Así que buscamos los r/s en [0, 1] con p*s - r*q = +1 ó -1:
      * q = 1, p = 0 (moneda 0/1): r = 1 y cualquier s >= 1 -> 1/1, 1/2, 1/3...
      * q = 1, p = 1 (moneda 1/1): r = s - 1 -> 0/1, 1/2, 2/3, ...
      * q >= 2: p*s ≡ +-1 (mod q), es decir s ≡ inv(p) ó s ≡ -inv(p) (mod q).
        Son DOS PROGRESIONES ARITMÉTICAS de paso q:
            s = s1 + t*q  con r = (p*s - 1)/q        (s1 = p^{-1} mod q)
            s = s2 + t*q  con r = (p*s + 1)/q        (s2 = q - s1)
        y r/s = p/q -+ 1/(q s) siempre cae en [0, 1] porque
        1/q <= p/q <= 1 - 1/q y 1/(qs) <= 1/q. Además gcd(r, s) = 1 sale
        gratis de |ps - rq| = 1, así que todas son monedas del marco.
      Se mezclan las dos progresiones (ordenadas por s, luego por r) y se
      toman las primeras n. El inverso modular se calcula con pow(p, -1, q).

MACROALGORITMO
    1. Leer p, q, n.
    2. Si q = 1: generar directamente la sucesión del caso 0/1 o 1/1.
    3. Si q >= 2: s1 = inverso de p módulo q, s2 = q - s1.
    4. Generar candidatos de ambas progresiones con s creciente hasta tener
       al menos n de cada una (bastan n términos de cada progresión).
    5. Ordenar por (s, r) y quedarse con los n primeros.
    6. Imprimir "M(r/s)" separados por espacio.

COMPLEJIDAD
    Tiempo O(n log n) por caso, memoria O(n).

EJEMPLO A MANO
    p/q = 2/5: inv(2) mod 5 = 3. Progresión A: s = 3, 8 -> r = 1, 3 (1/3, 3/8).
    Progresión B: s = 2, 7 -> r = 1, 3 (1/2, 3/7). Orden por s:
    M(1/2) M(1/3) M(3/7) M(3/8), igual al ejemplo.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/E")
    - Fuerza bruta: OK en 400 casos aleatorios (q <= 20, n <= 10): se
      enumeran TODAS las monedas r/s con s <= q(n+2)+2 y se prueba tangencia
      geométricamente con aritmética entera exacta (distancia^2 entre centros
      contra (suma de radios)^2, escalado por 2q^2s^2), sin usar la fórmula
      |ps - rq| = 1; también se comprueba que ningún par se superpone.
    - Rendimiento: 200 casos con q ~ 10^6 y n = 1000 en 0.36 s.
"""
import sys


def vecinos(p, q, n):
    """Lista de (s, r) de las n primeras monedas tangentes a M(p/q)."""
    if q == 1:
        if p == 0:
            return [(s, 1) for s in range(1, n + 1)]          # 1/1, 1/2, ...
        return [(s, s - 1) for s in range(1, n + 1)]          # 0/1, 1/2, ...
    s1 = pow(p, -1, q)            # p * s1 ≡ 1 (mod q)
    s2 = q - s1                   # p * s2 ≡ -1 (mod q)
    candidatos = []
    for t in range(n):
        s = s1 + t * q
        candidatos.append((s, (p * s - 1) // q))   # p*s - r*q = +1
        s = s2 + t * q
        candidatos.append((s, (p * s + 1) // q))   # p*s - r*q = -1
    candidatos.sort()             # por s creciente y luego r creciente
    return candidatos[:n]


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for i in range(0, len(datos) - 2, 3):
        p, q, n = int(datos[i]), int(datos[i + 1]), int(datos[i + 2])
        salida.append(" ".join(f"M({r}/{s})" for s, r in vecinos(p, q, n)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
