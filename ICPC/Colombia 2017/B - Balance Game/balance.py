"""
Colombia 2017 — B: Balance Game («Juego de la balanza»)
Ejecutar: python balance.py < balance.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Hay tres tipos de fichas con pesos distintos n1, n2, n3 y M copias de cada
    tipo, una balanza de dos platos y un objeto de peso W. Se quiere equilibrar
    la balanza (objeto + algunas fichas en un plato, fichas en el otro). Las
    fichas de un mismo tipo, si se usan, van todas en el mismo plato.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta EOF; cada uno "M W" y luego "n1 n2 n3".
    Salida:  por caso, el número de maneras distintas de equilibrar
             (sin importar el orden de los platos).
    Restricciones clave: M <= 5000, W <= 5*10^6, n_i <= 1000 distintos.

IDEA Y ALGORITMO
    Modelo: como los platos no tienen orden, fijamos el objeto en el plato 1.
    Para cada tipo i elegimos una cantidad c_i en [0, M] y, si c_i > 0, un
    plato. Codificamos ambas cosas en un ENTERO CON SIGNO x_i en [-M, M]:
        x_i > 0  -> c_i = x_i fichas en el plato 2 (el opuesto al objeto),
        x_i < 0  -> c_i = -x_i fichas junto al objeto,
        x_i = 0  -> el tipo no se usa (no hay plato que elegir).
    Esta codificación es una biyección con las "maneras", y el equilibrio es
        n1*x1 + n2*x2 + n3*x3 = W ,   |x_i| <= M.
    (Se comprobó con el ejemplo: 140 con 20, 50, 40 y M = 3 da exactamente 5.)

    Contar soluciones: probar todos los (x1, x2) son (2M+1)^2 ~ 10^8, demasiado
    para Python. En cambio fijamos x1 (2M+1 valores) y resolvemos la ECUACIÓN
    DIOFÁNTICA LINEAL  n2*x2 + n3*x3 = R  (R = W - n1*x1) en O(1):
      - g = gcd(n2, n3); si g no divide a R no hay solución.
      - Con el algoritmo de Euclides extendido obtenemos una solución
        particular (x2_0, x3_0); todas las soluciones son
            x2 = x2_0 + t*(n3/g),   x3 = x3_0 - t*(n2/g),   t entero.
      - Cada cota |x2| <= M y |x3| <= M da un intervalo de t (división con
        techo/piso exacta en enteros); se cuenta el tamaño de la intersección.

MACROALGORITMO
    1. Leer M, W, n1, n2, n3.
    2. g, (u, v) = euclides_extendido(n2, n3)  ->  n2*u + n3*v = g.
    3. Para cada x1 en [-M, M]: R = W - n1*x1; si R % g != 0 seguir.
    4. Solución particular x2_0 = u*R/g, x3_0 = v*R/g; pasos a = n3/g, b = n2/g.
    5. t debe cumplir -M <= x2_0 + a*t <= M  y  -M <= x3_0 - b*t <= M:
       calcular [t_lo, t_hi] de cada una, intersecar y sumar su tamaño.
    6. Imprimir el total.

COMPLEJIDAD
    Tiempo O(M) por caso (~10^4 iteraciones simples), memoria O(1).
    Medido: 22 casos con M = 5000 en 0.27 s en total.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/B")
    - Fuerza bruta: OK en 1000 casos aleatorios (M <= 12, pesos <= 30):
      enumeración directa de las (2M+1)^3 ternas con signo; además una segunda
      fuerza bruta que enumera (cantidad, plato) explícitamente sin la
      codificación con signo, para validar el modelo.
"""
import sys


def euclides_extendido(a, b):
    """Devuelve (g, x, y) con a*x + b*y = g = gcd(a, b)."""
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def rango_t(base, paso, m):
    """Intervalo [lo, hi] de enteros t con -m <= base + paso*t <= m (paso > 0)."""
    # t >= (-m - base)/paso  (techo)   y   t <= (m - base)/paso  (piso)
    lo = -((m + base) // paso)          # techo de (-m - base)/paso
    hi = (m - base) // paso
    return lo, hi


def contar(m, w, n1, n2, n3):
    g, u, v = euclides_extendido(n2, n3)
    a = n3 // g   # paso de x2 al avanzar t
    b = n2 // g   # paso de x3 al avanzar t (con signo negativo)
    total = 0
    for x1 in range(-m, m + 1):
        r = w - n1 * x1
        if r % g:
            continue
        k = r // g
        x2_0 = u * k
        x3_0 = v * k
        # Restricción sobre x2 = x2_0 + a*t
        lo1, hi1 = rango_t(x2_0, a, m)
        # Restricción sobre x3 = x3_0 - b*t  <=>  -x3 = -x3_0 + b*t en [-m, m]
        lo2, hi2 = rango_t(-x3_0, b, m)
        lo = lo1 if lo1 > lo2 else lo2
        hi = hi1 if hi1 < hi2 else hi2
        if hi >= lo:
            total += hi - lo + 1
    return total


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    pos = 0
    while pos + 4 < len(datos):
        m, w, n1, n2, n3 = map(int, datos[pos:pos + 5])
        pos += 5
        salida.append(str(contar(m, w, n1, n2, n3)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
