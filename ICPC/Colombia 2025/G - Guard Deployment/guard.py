"""
Colombia 2025 — G: Guard Deployment («Despliegue de guardias»)
Ejecutar: python guard.py < guard.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Una base militar está formada por edificios de base rectangular (posible-
    mente girados) y techo plano. Se quiere rodearla con una cerca poligonal
    CONVEXA de longitud mínima, con una torre de guardia en cada vértice. Todas
    las torres tienen la misma altura, mínima, de forma que entre CADA par de
    torres haya línea de visión: la recta entre ellas no puede tocar ningún
    edificio, y si pasa por encima de uno debe hacerlo al menos 1 m más arriba
    que su techo.

QUÉ HAY QUE HACER
    Entrada: K casos; cada uno N y N líneas "x1 y1 x2 y2 x3 y3 x4 y4 h"
             (las 4 esquinas de la base y la altura).
    Salida:  por caso, "perímetro altura": el perímetro de la cerca óptima con
             6 decimales y la altura mínima de las torres (entero).
             (El enunciado dice "una única línea", pero hay K casos: se
             imprime una línea por caso; el ejemplo solo tiene uno.)
             La altura mínima permitida de una torre es 3 m.
    Restricciones clave: K ≤ 10^4, N ≤ 10^3, |coord| ≤ 10^6, h ≤ 10^3.

IDEA Y ALGORITMO
    1) Cerca = ENVOLVENTE CONVEXA de todas las esquinas (algoritmo de la
       cadena monótona de Andrew). El polígono convexo más corto que contiene
       a un conjunto es su envolvente convexa; sus vértices (sin puntos
       colineales) son las torres, y todos son esquinas de edificios.
    2) Altura: todas las torres miden H, así que la línea de visión entre dos
       torres es horizontal a altura H. Debe pasar ≥ 1 m sobre todo edificio
       cuya base toque el SEGMENTO (en planta) entre las dos torres. Entonces
           H = máx(3, máx{h_b + 1 : la base b toca algún segmento entre dos
                                     vértices de la envolvente}).
       Todo edificio con una esquina en un vértice de la envolvente cuenta
       siempre (la torre está en su esquina). Un edificio interior cuenta
       solo si algún segmento entre torres lo cruza o roza: puede haber
       edificios altos "escondidos" en una celda del dibujo de diagonales
       que NO cuentan (la figura del enunciado justamente muestra líneas de
       visión cruzando un edificio interior).
    3) ¿Algún segmento entre torres toca el rectángulo R? Para una torre p
       (vértice de la envolvente), las demás torres vistas desde p están
       ordenadas por ángulo en el orden de la envolvente (abanico convexo).
       Como R está dentro de la envolvente, el rayo desde p hacia la torre q
       recorre el polígono exactamente de p a q; así que el segmento p–q toca
       R  ⇔  la dirección de q cae en el intervalo angular que ocupa R visto
       desde p (entre su esquina "más a la derecha" y "más a la izquierda").
       Eso se decide con BÚSQUEDA BINARIA en el abanico usando productos
       cruz (todo en enteros, sin errores de redondeo). Si p está dentro o en
       el borde de R, lo toca trivialmente.
       Costo O(V log V) por edificio (V = #torres). Para no hacerlo con todos:
       se ordenan los edificios por altura decreciente y se para en el primero
       que es tocado (los siguientes no pueden subir la respuesta); los
       edificios más bajos que la mejor respuesta ya conocida se ignoran.
    La fuerza bruta (todos los pares de torres contra todos los edificios) es
    O(V²·N), demasiado con V y N de miles.

MACROALGORITMO
    1. Leer los edificios; ordenar las 4 esquinas de cada uno en sentido
       antihorario (envolvente de 4 puntos).
    2. Envolvente convexa de todas las esquinas (sin colineales) y su perímetro.
    3. mejor = 3; para cada edificio con una esquina que sea vértice de la
       envolvente, mejor = máx(mejor, h + 1).
    4. Para los demás edificios, de mayor a menor h, mientras h + 1 > mejor:
       si algún segmento entre torres lo toca (abanico + búsqueda binaria
       desde cada torre), mejor = h + 1 y terminar.
    5. Imprimir "perímetro mejor".

COMPLEJIDAD
    Tiempo O(N log N) por la envolvente + O(V log V) por cada edificio que
    haya que revisar (en la práctica pocos, por la poda). Medido: N = 1000
    edificios: ~30 ms por caso. El límite K = 10^4 casos con N = 10^3
    cada uno (9·10^7 números de entrada) sería lento en Python solo por leer.

EJEMPLO A MANO
    Envolvente: (3,0) (8,3) (9,8) (8,9) (2,8) (0,3); perímetro
    √34 + √26 + √2 + √37 + √29 + √18 = 28.054753.
    El edificio de 31 m (6..8 × 5..6) no tiene esquinas en la envolvente,
    pero el segmento (8,3)–(8,9) roza su lado x = 8 → H = 31 + 1 = 32.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/G")
    - Fuerza bruta (todos los pares de torres × todos los edificios con
      intersección segmento–polígono convexo cerrado): OK en 1000 casos
      aleatorios con rectángulos sin solapamiento (ejes alineados y girados,
      algunos tocándose; en 15 de ellos la respuesta NO es máx h + 1 porque
      el más alto queda escondido en el interior).
    - Rendimiento: N = 1000 (rejilla, anillo de 500 edificios con ~990
      torres + 500 interiores altos, y 997 edificios altos escondidos que
      hay que revisar todos): ~0.03 s por caso.
    - Interpretación: se tomó la lectura literal (solo cuentan los edificios
      que alguna línea de visión cruza o roza). La lectura alternativa
      "máx h + 1 de todos los edificios" coincide en el ejemplo; difiere solo
      si el edificio más alto queda en una celda que ningún segmento entre
      torres toca.
"""
import sys
from math import hypot


def cruz(o, a, b):
    """Producto cruz (a − o) × (b − o): > 0 si o→a→b gira a la izquierda."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def envolvente(puntos):
    """Cadena monótona de Andrew; devuelve los vértices en orden antihorario,
    sin puntos repetidos ni colineales."""
    pts = sorted(set(puntos))
    if len(pts) <= 2:
        return pts
    inferior, superior = [], []
    for p in pts:
        while len(inferior) >= 2 and cruz(inferior[-2], inferior[-1], p) <= 0:
            inferior.pop()
        inferior.append(p)
    for p in reversed(pts):
        while len(superior) >= 2 and cruz(superior[-2], superior[-1], p) <= 0:
            superior.pop()
        superior.append(p)
    return inferior[:-1] + superior[:-1]


def dentro_cerrado(poli, p):
    """p dentro o en el borde del polígono convexo poli (antihorario)."""
    n = len(poli)
    return all(cruz(poli[k], poli[(k + 1) % n], p) >= 0 for k in range(n))


def segmentos_se_tocan(a, b, c, d):
    """¿Los segmentos cerrados ab y cd comparten algún punto?"""
    d1, d2 = cruz(a, b, c), cruz(a, b, d)
    d3, d4 = cruz(c, d, a), cruz(c, d, b)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    def sobre(p, q, r):  # r colineal con pq: ¿está en el segmento?
        return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and \
            min(p[1], q[1]) <= r[1] <= max(p[1], q[1])
    return (d1 == 0 and sobre(a, b, c)) or (d2 == 0 and sobre(a, b, d)) or \
           (d3 == 0 and sobre(c, d, a)) or (d4 == 0 and sobre(c, d, b))


def segmento_toca_poligono(a, b, poli):
    """Segmento cerrado ab contra polígono convexo cerrado (caso general)."""
    if dentro_cerrado(poli, a) or dentro_cerrado(poli, b):
        return True
    n = len(poli)
    return any(segmentos_se_tocan(a, b, poli[k], poli[(k + 1) % n]) for k in range(n))


def tocado_desde_abanico(hull, rect):
    """¿Algún segmento entre dos vértices de la envolvente (≥ 3 vértices)
    toca el rectángulo rect? Abanico + búsqueda binaria desde cada vértice."""
    V = len(hull)
    for i in range(V):
        p = hull[i]
        if dentro_cerrado(rect, p):
            return True
        px, py = p
        # Esquinas extremas de rect vistas desde p (todo cabe en el cono < 180°
        # de p, así que el producto cruz ordena los ángulos correctamente).
        cmin = cmax = rect[0]
        for c in rect[1:]:
            if cruz(p, cmin, c) < 0:
                cmin = c  # c está más "a la derecha" (horario) que cmin
            if cruz(p, cmax, c) > 0:
                cmax = c  # c está más "a la izquierda" (antihorario)
        # Abanico: hull[i+1], ..., hull[i-1] en orden angular creciente.
        # Primer k con dirección hacia el vértice no horaria respecto a cmin.
        lo, hi = 1, V  # desplazamientos 1..V-1; hi = "no existe"
        while lo < hi:
            mid = (lo + hi) // 2
            if cruz(p, cmin, hull[(i + mid) % V]) >= 0:
                hi = mid
            else:
                lo = mid + 1
        if lo < V and cruz(p, hull[(i + lo) % V], cmax) >= 0:
            return True  # esa dirección cae dentro del intervalo de rect
    return False


def resolver(edificios):
    esquinas = []
    for rect, _ in edificios:
        esquinas.extend(rect)
    hull = envolvente(esquinas)
    V = len(hull)
    perimetro = sum(hypot(hull[k][0] - hull[(k + 1) % V][0],
                          hull[k][1] - hull[(k + 1) % V][1]) for k in range(V)) if V > 1 else 0.0
    # (V = 2 solo ocurriría con bases degeneradas: la "cerca" es ida y vuelta.)

    mejor = 3  # altura mínima permitida
    vertices = set(hull)
    pendientes = []
    for rect, h in edificios:
        if any(c in vertices for c in rect):
            mejor = max(mejor, h + 1)  # una torre está en su esquina
        else:
            pendientes.append((h, rect))

    # De mayor a menor altura: el primero tocado fija la respuesta.
    pendientes.sort(key=lambda e: -e[0])
    for h, rect in pendientes:
        if h + 1 <= mejor:
            break
        if V >= 3:
            tocado = tocado_desde_abanico(hull, rect)
        elif V == 2:
            tocado = segmento_toca_poligono(hull[0], hull[1], rect)
        else:
            tocado = False
        if tocado:
            mejor = h + 1
            break
    return perimetro, mejor


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    casos = int(datos[pos])
    pos += 1
    salida = []
    for _ in range(casos):
        n = int(datos[pos])
        pos += 1
        edificios = []
        for _ in range(n):
            v = list(map(int, datos[pos:pos + 9]))
            pos += 9
            # Ordenar las 4 esquinas en sentido antihorario.
            rect = envolvente([(v[0], v[1]), (v[2], v[3]), (v[4], v[5]), (v[6], v[7])])
            edificios.append((rect, v[8]))
        perimetro, altura = resolver(edificios)
        salida.append(f"{perimetro:.6f} {altura}")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
