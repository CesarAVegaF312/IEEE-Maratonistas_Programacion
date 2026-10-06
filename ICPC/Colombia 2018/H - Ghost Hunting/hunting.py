"""
Colombia 2018 — H: Ghost Hunting («Cacería de fantasmas»)
Ejecutar: python hunting.py < hunting.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En Lavender City sólo quedan 3 balizas que hacen visibles a los Pokémon
    fantasma que estén «rodeados» (encerrados por las cercas virtuales que
    unen pares de balizas). Las balizas van en postes de luz existentes y el
    alcalde quiere la mayor zona de visibilidad posible.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta fin de archivo: N y N puntos enteros (x, y).
    Salida:  el área máxima de un triángulo con vértices en 3 de los postes,
             TRUNCADA a un decimal (p. ej. «7.5», «8.0»).
    Restricciones clave: 3 ≤ N ≤ 2 000, |x|, |y| < 10^6. O(N^3) ≈ 1.3·10^9
             es imposible; hace falta ~O(N^2) o menos.

IDEA Y ALGORITMO
    Las tres balizas encierran exactamente el triángulo que forman, así que
    se pide el TRIÁNGULO DE ÁREA MÁXIMA con vértices en el conjunto.
    1. Envolvente convexa (cadena monótona de Andrew): los vértices del
       triángulo máximo pueden tomarse en la envolvente (si un vértice está
       dentro, moverlo hacia el vértice de la envolvente más lejano de la
       recta opuesta no disminuye el área, porque el área es lineal en cada
       vértice y su máximo sobre un polígono se alcanza en un vértice).
    2. Sobre el polígono convexo P[0..h-1] (sin puntos colineales) se usa
       el método de DOS PUNTEROS O(h^2): para i fijo y j > i, el área de
       (i, j, k) como función de k ∈ (j, h) es unimodal (es la distancia de
       P[k] a la recta i–j, que sobre un arco convexo sube y luego baja), y
       el k óptimo no retrocede cuando j avanza. Así, para cada i, j y k sólo
       avanzan: O(h) por i, O(h^2) en total.
    - Todo se hace con productos cruz ENTEROS (dos veces el área), así que
      no hay error de punto flotante: 2·área es entero, y el área truncada a
      un decimal es «2A//2» seguido de «.5» si 2A es impar o «.0» si es par.
    (El famoso algoritmo O(n) «rotando tres punteros» se sabe que es
    incorrecto en algunos polígonos; por eso se usa la versión O(h^2), que
    sí es correcta.)

MACROALGORITMO
    1. Leer N y los puntos; eliminar duplicados.
    2. Calcular la envolvente convexa (sin puntos colineales).
    3. Si tiene < 3 vértices, el área es 0.
    4. Para cada i: k = i+2; para cada j en i+1..h-2: asegurar k > j y
       avanzar k mientras el área (i, j, k+1) ≥ área (i, j, k); actualizar
       el máximo con el área (i, j, k).
    5. Imprimir el máximo (2A) como «2A//2.(0|5)».

COMPLEJIDAD
    Tiempo O(N log N + h^2), memoria O(N), con h = vértices de la
    envolvente. Peor caso h = 2 000 (todos los puntos en posición convexa):
    ~1.1 s en Python por caso (medido con 2 000 puntos sobre un círculo de
    radio ~10^6); con puntos aleatorios h es pequeño y es instantáneo. Si el
    juez trae muchos casos con h ≈ 2 000, Python podría quedar justo.

EJEMPLO A MANO
    Caso 3: (1,1), (2,1), (4,1), (4,6). Envolvente: (1,1), (4,1), (4,6)
    → 2A = |3·5 − 0·3| = 15 → «7.5».

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/H")
    - Fuerza bruta: OK en 600 casos aleatorios pequeños (N ≤ 12, también
      con muchos colineales y duplicados) y 300 casos de hasta 60 puntos en
      posición casi convexa (elipses), contra el O(N^3) de todos los tríos.
"""
import sys


def cruz(o, a, b):
    """Producto cruz (a − o) × (b − o): dos veces el área con signo."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def envolvente_convexa(puntos):
    """Cadena monótona de Andrew; devuelve los vértices en sentido
    antihorario, sin puntos colineales."""
    pts = sorted(set(puntos))
    if len(pts) <= 2:
        return pts
    inferior = []
    for p in pts:
        while len(inferior) >= 2 and cruz(inferior[-2], inferior[-1], p) <= 0:
            inferior.pop()
        inferior.append(p)
    superior = []
    for p in reversed(pts):
        while len(superior) >= 2 and cruz(superior[-2], superior[-1], p) <= 0:
            superior.pop()
        superior.append(p)
    return inferior[:-1] + superior[:-1]


def doble_area_maxima(puntos):
    P = envolvente_convexa(puntos)
    h = len(P)
    if h < 3:
        return 0
    mejor = 0
    for i in range(h - 2):
        xi, yi = P[i]
        # Coordenadas relativas a P[i] para que el área sea dx*ys − dy*xs.
        xs = [p[0] - xi for p in P]
        ys = [p[1] - yi for p in P]
        k = i + 2
        for j in range(i + 1, h - 1):
            dx, dy = xs[j], ys[j]
            if k <= j:
                k = j + 1
            # Como el polígono es antihorario y k está «después» de j, el
            # área (i, j, k) es positiva; avanzamos k mientras no baje.
            actual = dx * ys[k] - dy * xs[k]
            while k + 1 < h:
                sig = dx * ys[k + 1] - dy * xs[k + 1]
                if sig < actual:
                    break
                actual = sig
                k += 1
            if actual > mejor:
                mejor = actual
    return mejor


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos]); pos += 1
        puntos = [(int(datos[pos + 2 * t]), int(datos[pos + 2 * t + 1])) for t in range(n)]
        pos += 2 * n
        a2 = doble_area_maxima(puntos)
        # Truncar a un decimal: 2A entero → parte entera A//1 y .5 o .0
        salida.append("%d.%d" % (a2 // 2, 5 if a2 % 2 else 0))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
