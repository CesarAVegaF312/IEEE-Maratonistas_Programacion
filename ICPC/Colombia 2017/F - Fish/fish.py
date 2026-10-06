"""
Colombia 2017 — F: Fish («Peces»)
Ejecutar: python fish.py < fish.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un acuario circular (centro (0,0), radio r) tiene peces de dos tipos, A y
    B, vistos desde arriba como puntos. Se quiere saber si un único panel de
    vidrio plano (una cuerda del círculo, de borde a borde) puede separar
    completamente los dos tipos sin tocar ningún pez.

QUÉ HAY QUE HACER
    Entrada: varios casos; cada uno "n r" y n líneas "x y t" (t = A o B).
             Termina con "0 0".
    Salida:  "FEED" si se pueden separar, "NOT YET" si no.
    Restricciones clave: 2 <= n <= 500, |coordenadas| <= 10^4, enteras.

IDEA Y ALGORITMO
    Todos los peces están dentro del círculo, así que cualquier recta que
    separe los dos grupos corta el círculo y define una cuerda válida: el
    problema es SEPARABILIDAD LINEAL ESTRICTA de dos conjuntos de puntos
    ("sin tocar ningún pez" = estricta). Dos conjuntos finitos son
    estrictamente separables  <=>  sus ENVOLVENTES CONVEXAS son disjuntas.
    1) Envolvente convexa de cada tipo (cadena monótona de Andrew),
       descartando puntos colineales. Puede degenerar en 1 punto o en un
       segmento (2 vértices).
    2) TEOREMA DEL EJE SEPARADOR (SAT): dos polígonos convexos son disjuntos
       si y sólo si existe un eje, perpendicular a alguna ARISTA de uno de
       ellos, en el que las proyecciones de ambos son intervalos disjuntos.
       Por qué: tome el par de puntos más cercanos entre ambos conjuntos; la
       mediatriz de ese par separa estrictamente, y su dirección es la normal
       de la arista que contiene a uno de los puntos más cercanos... salvo
       cuando ambos puntos más cercanos son VÉRTICES de figuras degeneradas
       (punto o segmento), donde la dirección es la diferencia entre dos
       vértices. Por eso, si alguna envolvente tiene <= 2 vértices, se
       agregan también como ejes las diferencias de todos los pares de
       vértices (a lo sumo 2*500).
    3) Todo con enteros (productos punto exactos): sin errores de redondeo.

MACROALGORITMO
    1. Leer n, r; si ambos son 0, terminar.
    2. Separar los puntos en A y B; calcular la envolvente de cada uno.
    3. Ejes candidatos = normales de las aristas de ambas envolventes
       (+ diferencias de vértices si alguna envolvente es degenerada).
    4. Para cada eje: proyectar los vértices de ambas envolventes; si
       max(A) < min(B) o max(B) < min(A), son separables -> "FEED".
    5. Si ningún eje separa -> "NOT YET".

COMPLEJIDAD
    Envolventes O(n log n); a lo sumo O(h) ejes, cada uno O(h) para
    proyectar: O(n^2) = 2.5*10^5 operaciones en el peor caso. Caso grande
    (n = 500 sobre la circunferencia, casi todos en la envolvente):
    10 casos en 0.23 s.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/F")
    - Fuerza bruta: OK en 3000 casos aleatorios pequeños (n <= 8, coords en
      [-3, 3], muchos casos colineales/degenerados). La fuerza bruta usa otra
      caracterización: las envolventes se intersecan sii algún segmento
      (a1,a2) de A corta a algún segmento (b1,b2) de B (incluyendo
      segmentos degenerados = puntos), o algún punto de un tipo está dentro
      de un triángulo de puntos del otro tipo.
"""
import sys


def cruz(o, a, b):
    """Producto cruz (a - o) x (b - o): >0 giro a la izquierda."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def envolvente(puntos):
    """Cadena monótona de Andrew; devuelve vértices en orden antihorario sin
    puntos colineales. 1 punto -> [p]; colineales -> [extremo1, extremo2]."""
    pts = sorted(set(puntos))
    if len(pts) <= 1:
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


def ejes_candidatos(ha, hb):
    ejes = []
    # Normales de las aristas de cada envolvente (un segmento aporta su normal).
    for h in (ha, hb):
        k = len(h)
        if k >= 2:
            for i in range(k):
                x1, y1 = h[i]
                x2, y2 = h[(i + 1) % k]
                ejes.append((y1 - y2, x2 - x1))
    # Casos degenerados: dirección entre vértices más cercanos.
    if len(ha) <= 2 or len(hb) <= 2:
        for a in ha:
            for b in hb:
                ejes.append((a[0] - b[0], a[1] - b[1]))
    return ejes


def separables(tipo_a, tipo_b):
    ha, hb = envolvente(tipo_a), envolvente(tipo_b)
    for ex, ey in ejes_candidatos(ha, hb):
        proy_a = [x * ex + y * ey for x, y in ha]
        proy_b = [x * ex + y * ey for x, y in hb]
        # Intervalos de proyección estrictamente disjuntos => hay un panel.
        if max(proy_a) < min(proy_b) or max(proy_b) < min(proy_a):
            return True
    return False


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        n, r = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        if n == 0 and r == 0:
            break
        tipo_a, tipo_b = [], []
        for _ in range(n):
            x, y, t = int(datos[pos]), int(datos[pos + 1]), datos[pos + 2]
            pos += 3
            (tipo_a if t == b"A" else tipo_b).append((x, y))
        salida.append("FEED" if separables(tipo_a, tipo_b) else "NOT YET")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
