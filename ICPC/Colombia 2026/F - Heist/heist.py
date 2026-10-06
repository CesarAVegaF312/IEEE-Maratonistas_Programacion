"""
Colombia 2026 — F: Heist («El golpe»)
Ejecutar: python heist.py < heist.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Danny O'Sea planea robar el McGuffin de una sala rectangular W × L
    cruzada por Z láseres. Hay que encontrar el punto de la sala más alejado
    de todo láser y de toda pared, y decir esa distancia.

QUÉ HAY QUE HACER
    Entrada: varios casos; "W L Z" y Z líneas "ex ey rx ry" (emisor y
             receptor, cada uno sobre una pared distinta). Termina con 0 0 0.
    Salida:  por caso "sx sy d" con dos decimales: el punto más seguro y su
             distancia al láser o pared más cercano.
             Desempates: si varios puntos alcanzan la distancia máxima, el
             que está en la región (celda) de MAYOR ÁREA; si aún hay varios
             (o varias celdas de igual área), el más cercano a (0, 0).
    Restricciones clave: 1 <= W, L <= 1000, 1 <= Z <= 100, error 10^-2.

IDEA Y ALGORITMO
    1) Arreglo de rectas → celdas convexas. Cada láser va de pared a pared,
       así que es una cuerda que atraviesa toda la sala: corta en dos cada
       celda por la que pasa. Se parte del rectángulo y, láser por láser, se
       recorta cada celda con la recta (recorte de polígono convexo por un
       semiplano, tipo Sutherland–Hodgman). Con Z rectas hay O(Z²) celdas
       convexas.
    2) Dentro de una celda convexa, la distancia al láser o pared más
       cercano es la distancia al BORDE de la celda, que es el mínimo de las
       distancias con signo a las rectas de sus lados. (Detalle: la
       distancia a un láser es a un SEGMENTO, no a una recta infinita, pero
       si el pie de la perpendicular cae fuera de la sala, antes se cruza
       una pared, que queda más cerca: el mínimo no cambia.)
       El punto más seguro de la celda es el centro del mayor círculo
       inscrito (centro de Chebyshev), que es un programa lineal en
       (x, y, r):   max r   s.a.   n_i·p − c_i >= r   para cada lado i.
       Como la región factible en (x, y, r) es un politopo acotado, el
       óptimo se alcanza en un vértice: un punto donde 3 restricciones son
       iguales. → Se prueban todas las ternas de lados, se resuelve el
       sistema 3×3 (Cramer) y se queda el mayor r que respeta TODOS los
       lados. Si el óptimo no es único (p. ej. una franja entre dos lados
       paralelos), el conjunto óptimo es un segmento cuyos extremos también
       son vértices (ternas) con el mismo r.
    3) Poda: para una celda de área A y perímetro P, el radio inscrito
       cumple r <= 2A/P (A = ½ Σ h_i·ℓ_i >= ½·r·P). Se procesan las celdas
       en orden decreciente de esa cota y se para cuando la cota ya es menor
       que el mejor r encontrado: casi ninguna celda necesita el paso 2.
    4) Desempates: celdas con r = r* (tolerancia 1e-7) → la de mayor área
       (tolerancia 1e-6) → en cada una, el punto del conjunto óptimo
       (punto o segmento entre los vértices óptimos) más cercano a (0, 0)
       → el de menor norma.

    HUECO DEL ENUNCIADO: dos celdas distintas de igual radio e igual área
    pueden tener sus puntos óptimos a la MISMA distancia de (0, 0) (p. ej.
    una sala cuadrada con láseres simétricos respecto a y = x: (0.29, 0.71)
    y (0.71, 0.29)). El enunciado no dice cuál elegir; aquí se toma el de
    menor x. Pasa en ~1.4 % de los casos aleatorios pequeños.

    Sobre la precisión: el resultado es en punto flotante; las tolerancias
    absorben los errores de redondeo de los cortes. Se imprime con "%.2f"
    y se evita el "-0.00".

MACROALGORITMO
    1. Celdas = [rectángulo]. Para cada láser: recortar cada celda con su
       recta; si ambas mitades tienen área > 0, reemplazarla por las dos.
    2. Para cada celda: área, perímetro, lados (normal unitaria interior n y
       constante c, de modo que la distancia con signo es n·p − c).
    3. Ordenar celdas por la cota 2A/P (de mayor a menor).
    4. Recorrerlas mientras la cota >= mejor r − ε: calcular el centro de
       Chebyshev por ternas de lados (r de la celda y sus vértices óptimos).
    5. Entre las celdas con r ≈ r*, quedarse con las de área máxima.
    6. En cada una, proyectar el origen sobre el segmento óptimo (o tomar el
       punto) y elegir el más cercano a (0, 0).
    7. Imprimir "sx sy d" con dos decimales.

COMPLEJIDAD
    Construcción: Σ_k (celdas tras k rectas) ≈ Z³/6 recortes pequeños.
    Centros: O(m⁴) por celda de m lados, pero la poda deja muy pocas celdas
    (y Σ m² sobre las celdas de un arreglo de rectas es O(Z²)).
    Medido (sala 1000 × 1000): 3 casos con Z = 100 rectas aleatorias
    (≈ 2 500 celdas cada uno) → 0.3 s en total; 100 rectas tangentes a un
    círculo (3 221 celdas, la central con 100 lados) → 0.4 s; 100 rectas por
    un mismo punto → 0.07 s; 30 casos aleatorios con Z <= 100 → 0.6 s.

EJEMPLO A MANO
    Caso 3 (12 × 8, láseres y = 4 y de (0,8) a (6,0)): las dos celdas de la
    derecha tienen altura 4, así que r* = 2 en ambas. Arriba: trapecio de
    área 42; abajo: área 30 → gana la de arriba. Ahí los centros óptimos son
    el segmento y = 6, 4 <= x <= 10 (la recta 4x + 3y = 24 exige x >= 4);
    el más cercano a (0,0) es (4, 6) → "4.00 6.00 2.00".

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/F")
    - Fuerza bruta independiente: candidatos = puntos equidistantes de 3
      rectas cualesquiera (paredes + láseres, todas las combinaciones de
      signos), valor = distancia mínima a todas las rectas; la celda de cada
      candidato se obtiene recortando el rectángulo con el semiplano de cada
      láser que lo contiene; desempates literales (área, luego proyección
      del origen sobre cada par de candidatos óptimos de la misma celda).
      Idéntica (±0.01) en 3000 casos aleatorios pequeños (W, L <= 8 con
      Z <= 5 y W, L <= 20 con Z <= 6; coordenadas enteras: muchísimos
      empates) usando en ambas el mismo desempate final por menor x (sin él
      difieren solo en los 21 casos simétricos descritos arriba).
    - Contra la solución del usuario (40icpc/heist.py) en 30 casos grandes
      aleatorios (Z <= 100): idéntica.
"""
import sys
from math import hypot

EPS = 1e-9


def recta(a, b):
    """Recta por a y b normalizada: (nx, ny, c) con n unitaria a la IZQUIERDA
    de a→b; la distancia con signo de p es nx·px + ny·py − c."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    largo = hypot(dx, dy)
    nx, ny = -dy / largo, dx / largo
    return nx, ny, nx * a[0] + ny * a[1]


def cortar(poli, nx, ny, c):
    """Parte el polígono convexo poli con la recta n·p = c.
    Devuelve (lado >= 0, lado <= 0); los vértices sobre la recta van a ambos."""
    izq, der = [], []
    m = len(poli)
    vals = [nx * x + ny * y - c for x, y in poli]
    for i in range(m):
        p, sp, sq = poli[i], vals[i], vals[(i + 1) % m]
        if sp >= -EPS:
            izq.append(p)
        if sp <= EPS:
            der.append(p)
        # La arista p→q cruza la recta estrictamente: agregar la intersección.
        if (sp > EPS and sq < -EPS) or (sp < -EPS and sq > EPS):
            q = poli[(i + 1) % m]
            t = sp / (sp - sq)
            x = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
            izq.append(x)
            der.append(x)
    return izq, der


def area(poli):
    s = 0.0
    m = len(poli)
    for i in range(m):
        x1, y1 = poli[i]
        x2, y2 = poli[(i + 1) % m]
        s += x1 * y2 - x2 * y1
    return s / 2          # positiva: los polígonos se mantienen antihorarios


def construir_celdas(w, l, laseres):
    """Celdas convexas (antihorarias) del arreglo de láseres en la sala."""
    celdas = [[(0.0, 0.0), (float(w), 0.0), (float(w), float(l)), (0.0, float(l))]]
    for ex, ey, rx, ry in laseres:
        if (ex, ey) == (rx, ry):
            continue                            # láser degenerado (no debería haber)
        nx, ny, c = recta((ex, ey), (rx, ry))
        nuevas = []
        for poli in celdas:
            # Rechazo rápido: si todos los vértices quedan del mismo lado, la
            # recta no atraviesa esta celda.
            vals = [nx * x + ny * y - c for x, y in poli]
            if min(vals) >= -EPS or max(vals) <= EPS:
                nuevas.append(poli)
                continue
            izq, der = cortar(poli, nx, ny, c)
            if len(izq) >= 3 and len(der) >= 3 and area(izq) > EPS and area(der) > EPS:
                nuevas.append(izq)
                nuevas.append(der)
            else:
                nuevas.append(poli)
        celdas = nuevas
    return celdas


def lados(poli):
    """(nx, ny, c) de cada lado con normal unitaria hacia ADENTRO (polígono
    antihorario ⇒ el interior queda a la izquierda de cada arista)."""
    res = []
    m = len(poli)
    for i in range(m):
        a, b = poli[i], poli[(i + 1) % m]
        if hypot(b[0] - a[0], b[1] - a[1]) > EPS:
            res.append(recta(a, b))
    return res


def chebyshev(ls):
    """Centro de Chebyshev por enumeración de ternas de lados.
    Devuelve (r*, lista de vértices óptimos (x, y))."""
    mejor_r, puntos = -1.0, []
    m = len(ls)
    for i in range(m):
        a1, b1, d1 = ls[i]
        for j in range(i + 1, m):
            a2, b2, d2 = ls[j]
            for k in range(j + 1, m):
                a3, b3, d3 = ls[k]
                # Sistema: a·x + b·y − r = d para los 3 lados (Cramer).
                det = a1 * (b3 - b2) - b1 * (a3 - a2) - (a2 * b3 - a3 * b2)
                if abs(det) < 1e-12:
                    continue                    # lados paralelos: sin vértice
                x = (d1 * (b3 - b2) - b1 * (d3 - d2) - (d2 * b3 - d3 * b2)) / det
                y = (a1 * (d3 - d2) - d1 * (a3 - a2) - (a2 * d3 - a3 * d2)) / det
                r = (a1 * (b2 * d3 - b3 * d2) - b1 * (a2 * d3 - a3 * d2)
                     + d1 * (a2 * b3 - a3 * b2)) / det
                if r < mejor_r - 1e-7:
                    continue                    # no mejora: ni comprobarlo
                # El punto debe estar a distancia >= r de TODOS los lados.
                if all(nx * x + ny * y - c >= r - 1e-7 for nx, ny, c in ls):
                    if r > mejor_r + 1e-7:
                        mejor_r, puntos = r, [(x, y)]
                    else:
                        puntos.append((x, y))
                        mejor_r = max(mejor_r, r)
    return mejor_r, puntos


def mas_cercano_al_origen(puntos):
    """Los vértices óptimos de una celda generan un punto o un segmento:
    se toman sus dos extremos (el par más alejado) y se proyecta el origen."""
    if len(puntos) == 1:
        return puntos[0]
    p, q, dmax = puntos[0], puntos[0], -1.0
    for i in range(len(puntos)):
        for j in range(i + 1, len(puntos)):
            d = hypot(puntos[i][0] - puntos[j][0], puntos[i][1] - puntos[j][1])
            if d > dmax:
                p, q, dmax = puntos[i], puntos[j], d
    dx, dy = q[0] - p[0], q[1] - p[1]
    l2 = dx * dx + dy * dy
    if l2 < 1e-18:
        return p
    t = max(0.0, min(1.0, -(p[0] * dx + p[1] * dy) / l2))
    return p[0] + t * dx, p[1] + t * dy


def resolver(w, l, laseres):
    celdas = construir_celdas(w, l, laseres)

    # Cota superior del radio inscrito de cada celda: 2·área / perímetro.
    info = []
    for poli in celdas:
        a = area(poli)
        per = sum(hypot(poli[(i + 1) % len(poli)][0] - poli[i][0],
                        poli[(i + 1) % len(poli)][1] - poli[i][1])
                  for i in range(len(poli)))
        info.append((2 * a / per, a, poli))
    info.sort(key=lambda t: -t[0])

    # Calcular el centro exacto solo de las celdas que aún pueden empatar o
    # superar al mejor radio encontrado.
    mejor_r = -1.0
    evaluadas = []                        # (r, área, vértices óptimos)
    for cota, a, poli in info:
        if cota < mejor_r - 1e-7:
            break
        r, puntos = chebyshev(lados(poli))
        evaluadas.append((r, a, puntos))
        mejor_r = max(mejor_r, r)

    # Desempates: radio máximo → mayor área → más cercano a (0, 0).
    candidatas = [e for e in evaluadas if e[0] >= mejor_r - 1e-7]
    a_max = max(e[1] for e in candidatas)
    mejor_p, mejor_n2 = None, float("inf")
    for r, a, puntos in candidatas:
        if a < a_max - 1e-6:
            continue
        x, y = mas_cercano_al_origen(puntos)
        n2 = x * x + y * y
        # Más cercano a (0,0); si dos celdas empatan también en eso (caso no
        # definido por el enunciado, p. ej. celdas simétricas respecto a la
        # diagonal y = x), se elige el de menor x.
        if n2 < mejor_n2 - 1e-9 or (n2 <= mejor_n2 + 1e-9 and x < mejor_p[0] - 1e-9):
            mejor_p, mejor_n2 = (x, y), min(n2, mejor_n2)
    return mejor_p[0], mejor_p[1], mejor_r


def formato(v):
    s = "%.2f" % v
    return "0.00" if s == "-0.00" else s


def main():
    datos = sys.stdin.buffer.read().split()
    idx, salida = 0, []
    while idx + 2 < len(datos):
        w, l, z = int(datos[idx]), int(datos[idx + 1]), int(datos[idx + 2])
        idx += 3
        if w == 0 and l == 0 and z == 0:          # fin de la entrada
            break
        laseres = []
        for _ in range(z):
            laseres.append(tuple(int(t) for t in datos[idx: idx + 4]))
            idx += 4
        x, y, d = resolver(w, l, laseres)
        salida.append("%s %s %s" % (formato(x), formato(y), formato(d)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
