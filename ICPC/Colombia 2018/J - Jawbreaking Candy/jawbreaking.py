"""
Colombia 2018 — J: Jawbreaking Candy («Dulce rompemandíbulas»)
Ejecutar: python jawbreaking.py < jawbreaking.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Una máquina de ACM corta dulces de longitud L en piezas de longitud
    a·L/b con enteros a > 0 y 0 < b ≤ n (n = «resolución» de la máquina).
    Alice quiere la pieza más corta que mida al menos d.

QUÉ HAY QUE HACER
    Entrada: líneas «L n d» hasta «0 0 0».
    Salida:  por línea, la longitud mínima a·L/b ≥ d como fracción reducida
             «p/q» (si es entera, «p/1»).
    Restricciones clave: L < 10^6, n ≤ 5 000, 0 < d ≤ L; número de casos
             desconocido.

IDEA Y ALGORITMO
    Minimizar a·L/b equivale a minimizar la fracción a/b, sujeta a
    a/b ≥ x := d/L y b ≤ n. Es decir: buscamos el «vecino por arriba» de x
    en la sucesión de Farey F_n (la menor fracción con denominador ≤ n que
    es ≥ x). Eso se hace con un descenso por el ÁRBOL DE STERN–BROCOT:
      - Se mantienen dos cotas l = a/b < x < u = c/e (al inicio 0/1 y 1/0),
        que son vecinas en el árbol (c·b − a·e = 1).
      - La mediante (a+c)/(b+e) es la fracción de menor denominador entre
        ellas; si su denominador ya pasa de n, ninguna fracción con
        denominador ≤ n cabe entre l y u, así que u es la respuesta.
      - Si la mediante es < x la cota inferior sube; si es > x baja la
        superior. Para no dar pasos de uno en uno (podrían ser ~n pasos), se
        dan «saltos» de t pasos seguidos en la misma dirección: el mayor t
        que mantiene la desigualdad y el denominador ≤ n, calculado con una
        división entera (es exactamente la fracción continua de x).
    Caso especial: si x = d/L reducido ya tiene denominador ≤ n, la máquina
    corta exactamente d y la respuesta es «d/1».
    Al final la longitud es c·L/e, que se reduce con gcd.
    Nota: el enunciado dice que las longitudes cortables son «más cortas que
    L», pero su propia lista incluye 500/1 = L y longitudes mayores; como
    d ≤ L siempre basta con fracciones ≤ 1, así que no afecta.
    (El enfoque directo «para cada b, a = ⌈d·b/L⌉» es O(n) por caso y
    también sería correcto; se usa como fuerza bruta.)

MACROALGORITMO
    1. Leer L, n, d hasta 0 0 0.
    2. Si L/gcd(d, L) ≤ n → imprimir «d/1».
    3. l = 0/1, u = 1/0.
    4. Mientras el denominador de la mediante sea ≤ n:
       si mediante < x → avanzar l t pasos hacia u (t máximo);
       si no → avanzar u t pasos hacia l (t máximo).
    5. Respuesta = u·L reducida → imprimir «num/den».

COMPLEJIDAD
    Tiempo O(log L) por caso (número de cocientes de la fracción continua),
    memoria O(1). 10^5 casos aleatorios grandes: ~0.6 s.

EJEMPLO A MANO
    500 3 320: x = 320/500 = 16/25 (denominador 25 > 3). Fracciones con
    denominador ≤ 3 alrededor de 0.64: 1/2 < 0.64 < 2/3 → u = 2/3,
    longitud 2·500/3 = 1000/3.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/J")
    - Fuerza bruta: OK en 3 000 casos aleatorios (L ≤ 300, n ≤ 60 y otros con
      L, n grandes) contra el recorrido O(n) sobre todos los denominadores.
"""
import sys
from math import gcd


def menor_fraccion_arriba(d, L, n):
    """Menor fracción c/e ≥ d/L con 1 ≤ e ≤ n, suponiendo que d/L NO es
    representable con denominador ≤ n (así la desigualdad es estricta)."""
    a, b = 0, 1   # cota inferior  a/b < d/L
    c, e = 1, 0   # cota superior  c/e > d/L  (1/0 = «infinito»)
    while b + e <= n:
        # Comparar la mediante (a+c)/(b+e) con d/L usando enteros.
        if L * (a + c) < d * (b + e):
            # La cota inferior sube: a/b -> (a+t·c)/(b+t·e) mientras siga < x.
            # L(a+tc) < d(b+te)  <=>  t·(Lc−de) < db−La
            t = (d * b - L * a - 1) // (L * c - d * e)
            # (Con u = 1/0 nunca se entra aquí porque x ≤ 1 = mediante 1/1;
            #  igual se protege la división por si acaso.)
            if e > 0:
                t = min(t, (n - b) // e)
            a, b = a + t * c, b + t * e
        else:
            # La cota superior baja: c/e -> (c+t·a)/(e+t·b) mientras siga > x.
            # L(c+ta) > d(e+tb)  <=>  t·(db−La) < Lc−de
            t = (L * c - d * e - 1) // (d * b - L * a)
            t = min(t, (n - e) // b)
            c, e = c + t * a, e + t * b
    return c, e


def resolver(L, n, d):
    g = gcd(d, L)
    if L // g <= n:
        # d/L = a/b con b ≤ n: la máquina corta exactamente d.
        return "%d/1" % d
    c, e = menor_fraccion_arriba(d, L, n)
    num, den = c * L, e
    g = gcd(num, den)
    return "%d/%d" % (num // g, den // g)


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for i in range(0, len(datos) - 2, 3):
        L, n, d = int(datos[i]), int(datos[i + 1]), int(datos[i + 2])
        if L == 0 and n == 0 and d == 0:
            break
        salida.append(resolver(L, n, d))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
