r"""
Geometría — Línea de barrido: máximo de intervalos solapados y área de la unión de rectángulos («sweep line»)
Nivel: Avanzado
Ejecutar: python linea_de_barrido.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Convertir un problema 2D (o de intervalos) en una secuencia ORDENADA de
    eventos que una recta imaginaria va encontrando al barrer el plano de
    izquierda a derecha, manteniendo una estructura con «lo que la recta
    está cortando ahora». Dos clásicos:
    - Máximo número de intervalos que se solapan en un punto (cuántos
      clientes hay a la vez en el restaurante, salas de reunión mínimas).
    - Área de la UNIÓN de n rectángulos alineados a los ejes (que se
      solapan), en O(n log n) con un árbol de segmentos.
    Señales en el enunciado: intervalos de tiempo [llegada, salida],
    «máximo simultáneo», «cuántas salas», rectángulos con lados paralelos
    a los ejes que se solapan, «área total cubierta», n hasta 10^5.

FUNCIÓN
    max_solapados(intervalos, cerrados=True) -> (int, x)
        Máximo número de intervalos que contienen un mismo punto y un punto
        x donde se alcanza. cerrados=True: [l, r] (si uno termina en x y
        otro empieza en x, se solapan); False: [l, r) (no se solapan).
        Con lista vacía devuelve (0, None).
    area_union_rectangulos(rects) -> int
        rects: lista de (x1, y1, x2, y2) con x1 <= x2, y1 <= y2 (enteros).
        Área de la unión (exacta).

IDEA Y ALGORITMO
    INTERVALOS: cada intervalo da dos eventos: +1 al empezar y −1 al
    terminar. Ordenados por coordenada, la suma acumulada es cuántos
    intervalos contienen el punto actual; el máximo de esa suma es la
    respuesta. El único detalle es el EMPATE en una misma coordenada: con
    intervalos cerrados, procesar los +1 antes que los −1 (en x ambos
    están); con semiabiertos, los −1 antes.

        [-------]                 activos:  1  2  3  2  1
            [-------]                         |  |  |  |  |
                [-------]         eventos:   +1 +1 +1 −1 −1 ...
        ^   ^   ^   ^   ^         el máximo de la suma acumulada

    UNIÓN DE RECTÁNGULOS: barrer con una recta vertical. Cada rectángulo
    da dos eventos: en x1 «se activa el intervalo [y1, y2)», en x2 «se
    desactiva». Entre dos eventos consecutivos x_i < x_{i+1}, la recta corta
    la unión en un conjunto fijo de tramos verticales de largo total L, y
    esa franja aporta L · (x_{i+1} − x_i).

             y ^        ┌─────┐          franja entre dos eventos:
               |   ┌────┼──┐  │          área = (largo cubierto en y)
               |   │    └──┼──┘                 × (ancho de la franja)
               |   └───────┘
               +---|----|--|--|---> x   (eventos en cada x1, x2)

    Para obtener L rápido: comprimir las y (ordenar los y1, y2 distintos)
    y usar un ÁRBOL DE SEGMENTOS sobre los intervalos elementales
    [ys[i], ys[i+1]). Cada nodo guarda cnt (cuántos rectángulos lo cubren
    COMPLETO, sumados directamente en ese nodo) y cub (largo cubierto en su
    rango): si cnt > 0, cub = todo el largo del nodo; si no, la suma de los
    hijos (0 en una hoja). Nunca hace falta «empujar» (lazy) porque cada
    +1 tiene su −1 exactamente sobre los mismos nodos. L = cub de la raíz.

MACROALGORITMO
    Intervalos:
    1. Eventos (l, +1) y (r, −1); ordenar por coordenada y desempate.
    2. Recorrer acumulando; guardar el máximo y dónde ocurre.
    Unión de rectángulos:
    1. ys = valores distintos de y1, y2, ordenados; índice de cada uno.
    2. Eventos (x1, +1, y1, y2) y (x2, −1, y1, y2); ordenar por x.
    3. Para cada evento: área += cub(raíz) · (x − x_anterior); aplicar
       ±1 en el rango [idx(y1), idx(y2)) del árbol; x_anterior = x.

COMPLEJIDAD
    Intervalos: O(n log n) por el orden, memoria O(n). En Python ~10^5
    intervalos en ~0.5 s (10^6 tarda varios segundos: ordenar 2·10^6 tuplas).
    Unión de rectángulos: O(n log n) tiempo, O(n) memoria. Medido en Python:
    10^5 rectángulos ~8 s (árbol recursivo); hasta ~2·10^4 va holgado.

EJEMPLO A MANO
    Intervalos cerrados [1,4] [2,5] [4,7] [6,8]:
      eventos: 1:+1 (1)  2:+1 (2)  4:+1 (3) 4:−1 (2)  5:−1 (1)  6:+1 (2) …
      máximo 3 en x = 4 ([1,4], [2,5] y [4,7] contienen al 4).
      Como semiabiertos [1,4) [2,5) [4,7) [6,8): en x = 4 primero sale
      [1,4) -> máximo 2.
    Rectángulos (0,0,2,2) y (1,1,3,3): 4 + 4 − 1 = 7.
      Franjas: x∈[0,1): cubierto [0,2) = 2 -> 2; x∈[1,2): [0,3) = 3 -> 3;
      x∈[2,3): [1,3) = 2 -> 2. Total 7.

ERRORES TÍPICOS
    - Desempate equivocado en una misma coordenada (cerrados vs.
      semiabiertos): cambia la respuesta en los casos frontera.
    - Sumar las áreas de los rectángulos sin descontar solapes, o
      inclusión-exclusión (exponencial).
    - Árbol de segmentos sobre las coordenadas y SIN comprimir (10^9 nodos).
    - Confundir puntos con intervalos elementales: el árbol tiene
      len(ys) − 1 hojas (los tramos entre y's consecutivos).
    - Acumular el área DESPUÉS de aplicar el evento (debe ser antes: la
      franja anterior usa el estado anterior).

VARIANTES Y RELACIONADOS
    - Perímetro de la unión de rectángulos: mismo barrido contando también
      cuántos tramos cubiertos hay.
    - Contar intersecciones entre segmentos horizontales y verticales:
      barrido + Fenwick.
    - Par más cercano con barrido + conjunto ordenado (par_mas_cercano.py).
    - Salas mínimas = máximo de solapados (versión voraz con montículo).
    - Shamos–Hoey: ¿algún par de n segmentos se corta? (interseccion_segmentos.py).
    - Árbol de segmentos (06_EstructurasDatos/segment_tree.py,
      segment_tree_lazy.py); Fenwick (06_EstructurasDatos/fenwick.py).
    - Intervalos con voraces (02_Voraz/intervalos.py).

DÓNDE PRACTICAR
    - CSES «Restaurant Customers» (máximo de solapados)

VERIFICACIÓN
    - Pruebas: max_solapados OK en 3000 conjuntos aleatorios (cerrados y
      semiabiertos, extremos repetidos, intervalos de largo 0) contra
      contar en cada coordenada entera y media; area_union_rectangulos OK
      en 1500 conjuntos de hasta 8 rectángulos (coordenadas chicas,
      degenerados incluidos) contra contar las celdas unitarias cubiertas
      (python linea_de_barrido.py)
"""
import random


def max_solapados(intervalos, cerrados=True):
    """(máximo de intervalos que comparten un punto, un punto donde ocurre)."""
    # Desempate en la misma coordenada: con cerrados entran (+1) antes de
    # salir (−1); con semiabiertos salen antes de entrar.
    entra, sale = (0, 1) if cerrados else (1, 0)
    eventos = []
    for l, r in intervalos:
        if not cerrados and l == r:
            continue                        # [l, l) es vacío
        eventos.append((l, entra, 1))
        eventos.append((r, sale, -1))
    eventos.sort()
    activos, mejor, donde = 0, 0, None
    for x, _, delta in eventos:
        activos += delta
        if activos > mejor:
            mejor, donde = activos, x
    return mejor, donde


def area_union_rectangulos(rects):
    """Área de la unión de rectángulos (x1, y1, x2, y2) alineados a los ejes."""
    rects = [r for r in rects if r[0] < r[2] and r[1] < r[3]]   # sin área: fuera
    if not rects:
        return 0
    ys = sorted({y for r in rects for y in (r[1], r[3])})
    idx = {y: i for i, y in enumerate(ys)}
    m = len(ys) - 1                         # hojas = intervalos elementales
    cnt = [0] * (4 * m)                     # rectángulos que cubren todo el nodo
    cub = [0] * (4 * m)                     # largo cubierto dentro del nodo

    def actualizar(nodo, l, r, ql, qr, v):
        # nodo cubre las hojas [l, r), es decir y en [ys[l], ys[r])
        if qr <= l or r <= ql:
            return
        if ql <= l and r <= qr:
            cnt[nodo] += v
        else:
            mid = (l + r) // 2
            actualizar(2 * nodo, l, mid, ql, qr, v)
            actualizar(2 * nodo + 1, mid, r, ql, qr, v)
        if cnt[nodo] > 0:
            cub[nodo] = ys[r] - ys[l]       # cubierto entero
        elif r - l == 1:
            cub[nodo] = 0                   # hoja sin cubrir
        else:
            cub[nodo] = cub[2 * nodo] + cub[2 * nodo + 1]

    eventos = []
    for x1, y1, x2, y2 in rects:
        eventos.append((x1, 1, idx[y1], idx[y2]))
        eventos.append((x2, -1, idx[y1], idx[y2]))
    eventos.sort()
    area, x_ant = 0, eventos[0][0]
    for x, v, a, b in eventos:
        area += cub[1] * (x - x_ant)        # franja anterior, con el estado anterior
        actualizar(1, 0, m, a, b, v)
        x_ant = x
    return area


def demo():
    iv = [(1, 4), (2, 5), (4, 7), (6, 8)]
    print("intervalos:", iv)
    print("cerrados     -> máximo, punto:", max_solapados(iv))                   # (3, 4)
    print("semiabiertos -> máximo, punto:", max_solapados(iv, cerrados=False))   # (2, 2)
    rs = [(0, 0, 2, 2), (1, 1, 3, 3)]
    print("unión de", rs, "-> área", area_union_rectangulos(rs))                 # 7
    rs = [(0, 0, 10, 10), (2, 2, 4, 4), (5, -5, 15, 5)]
    print("unión de", rs, "-> área", area_union_rectangulos(rs))                 # 175


def pruebas():
    random.seed(1983)

    # Casos borde
    assert max_solapados([]) == (0, None)
    assert max_solapados([(3, 3)]) == (1, 3) and max_solapados([(3, 3)], False) == (0, None)
    assert max_solapados([(1, 2), (2, 3)])[0] == 2
    assert max_solapados([(1, 2), (2, 3)], cerrados=False)[0] == 1
    assert area_union_rectangulos([]) == 0
    assert area_union_rectangulos([(0, 0, 5, 0)]) == 0
    assert area_union_rectangulos([(0, 0, 3, 3)] * 4) == 9
    big = 10 ** 9
    assert area_union_rectangulos([(-big, -big, big, big), (0, 0, 1, 1)]) == 4 * big * big

    for _ in range(3000):
        n = random.randint(0, 10)
        iv = []
        for _ in range(n):
            l = random.randint(-5, 5)
            iv.append((l, l + random.randint(0, 5)))
        for cerrados in (True, False):
            mejor, donde = max_solapados(iv, cerrados)
            # Fuerza bruta: probar todas las coordenadas enteras y medias
            def cuantos(x):
                if cerrados:
                    return sum(1 for l, r in iv if l <= x <= r)
                return sum(1 for l, r in iv if l <= x < r)
            esperado = max([cuantos(k / 2) for k in range(-22, 23)], default=0)
            assert mejor == esperado
            if mejor > 0:
                assert cuantos(donde) == mejor

    for _ in range(1500):
        rs = []
        for _ in range(random.randint(0, 8)):
            x1, y1 = random.randint(-6, 6), random.randint(-6, 6)
            rs.append((x1, y1, x1 + random.randint(0, 6), y1 + random.randint(0, 6)))
        # Fuerza bruta: celdas unitarias [x, x+1) × [y, y+1) cubiertas
        celdas = set()
        for x1, y1, x2, y2 in rs:
            for x in range(x1, x2):
                for y in range(y1, y2):
                    celdas.add((x, y))
        assert area_union_rectangulos(rs) == len(celdas)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
