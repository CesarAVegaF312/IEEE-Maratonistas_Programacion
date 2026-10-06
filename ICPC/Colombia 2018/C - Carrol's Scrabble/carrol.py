"""
Colombia 2018 — C: Carrol's Scrabble («El Scrabble de Carroll»)
Ejecutar: python carrol.py < carrol.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Lewis Carroll inventó «Word Links» (Doublets): ir de una palabra a otra
    pasando por palabras válidas, donde dos palabras consecutivas tienen la
    misma longitud y difieren en una sola letra o son anagramas. En la
    versión «Scrabble», entre los caminos más cortos se busca el de mayor
    puntaje (suma de valores de Scrabble de las palabras intermedias).

QUÉ HAY QUE HACER
    Entrada: N palabras del diccionario (sin repetir, ≤ 20 letras), Q y Q
             líneas «w1 TO w2».
    Salida:  «w1 TO w2 NS Val» con NS = mínimo número de pasos y Val =
             máximo puntaje entre los caminos de NS pasos (sin contar w1 ni
             w2), o «w1 TO w2 IMPOSSIBLE» si no hay camino.
    Restricciones clave: N < 10 000, Q < 200.

IDEA Y ALGORITMO
    BFS por capas + DP de máximo sobre el DAG de caminos más cortos, usando
    «CUBETAS» (buckets) para no construir las aristas explícitamente.
    - Dos palabras están unidas si comparten una cubeta:
        * cubeta de comodín (pos, palabra sin la letra pos): todas las
          palabras que coinciden salvo en la posición pos (difieren en
          exactamente una letra);
        * cubeta de anagrama: palabras con las mismas letras ordenadas.
      Cada cubeta es una CLIQUE; una cubeta de anagramas puede tener miles
      de palabras (≈ 10^8 aristas), por eso no se expanden.
    - Observación clave: en una clique las distancias BFS difieren a lo más
      en 1. Así que la primera vez que el BFS toca una cubeta (desde la capa
      d) sus miembros están en la capa d o d+1 (o sin visitar → pasan a
      d+1). Se procesa esa cubeta UNA sola vez:
          mejor = máximo puntaje entre sus miembros de la capa d
          cada miembro v de la capa d+1 (o nuevo): punt[v] = max(punt[v],
                                                   mejor + valor[v])
      Ninguna visita posterior a la cubeta puede mejorar nada (los de la
      capa d+1 ya recibieron lo mejor de la capa d, y una capa mayor no da
      caminos más cortos).
    - punt[v] = máximo de la suma de valores de las palabras de un camino
      más corto w1 → v, contando v pero no w1. La respuesta es
      punt[w2] − valor[w2].
    - Las cubetas de un solo elemento no aportan aristas y se descartan
      (acelera mucho con palabras largas).
    - Dos atajos para no repetir BFS caros:
        * Componentes conexas (union-find sobre las cubetas): si w1 y w2
          están en componentes distintas la respuesta es IMPOSSIBLE sin BFS
          (sin esto, cada IMPOSSIBLE recorría toda la componente de w1).
        * La respuesta es SIMÉTRICA (grafo no dirigido, extremos excluidos):
          un BFS desde una palabra responde todas las consultas donde ésta
          aparece como origen o destino; se eligen raíces vorazmente (la
          palabra que cubre más consultas pendientes) y cada BFS se detiene
          al completar la capa en que aparecen todos sus objetivos.
    - El BFS sólo da por resuelto un objetivo cuando termina su capa
      completa: otra cubeta de la misma capa podría mejorar su puntaje.

MACROALGORITMO
    1. Leer el diccionario; calcular el valor de Scrabble de cada palabra.
    2. Construir las cubetas (comodín por posición y anagrama), quedarse con
       las de tamaño ≥ 2 y guardar para cada palabra sus cubetas.
    3. Union-find sobre las cubetas → componente de cada palabra.
    4. Consultas triviales: w1 = w2 → «0 0»; distinta componente →
       IMPOSSIBLE.
    5. Para las demás: escoger como raíz la palabra que más consultas
       pendientes cubre y hacer BFS por capas desde ella: cada cubeta nueva
       tocada desde la capa d se procesa una vez (máximo de la capa d y
       propagación a la capa d+1).
    6. Para cada consulta cubierta, con «o» = el otro extremo: imprimir
       dist[o] y punt[o] − valor[o]. Repetir 5–6 hasta cubrir todas.

COMPLEJIDAD
    Construcción O(N·L^2) (L ≤ 20). Cada BFS recorre cada cubeta a lo sumo
    una vez: O(N·L), total O(Q·N·L) en el peor caso. Medido (Python):
      - 9 999 palabras de 20 letras (hipercubo {a,b}^13 + sufijo, cubetas de
        anagrama de ~1 700 palabras) y 199 consultas con extremos TODOS
        distintos y lejanos: ~8.9 s (el peor caso que encontramos; antes de
        los atajos de componentes/simetría, casos así tardaban ~40 s);
      - el mismo diccionario con consultas IMPOSSIBLE o con extremos
        repetidos: < 0.5 s;
      - 9 999 palabras de 4 letras sobre 10 letras, 199 consultas: ~1.5 s.
    Con un juez estricto y casos adversarios, Python podría quedar justo.

EJEMPLO A MANO
    iron→icon→coin→corn→cord→lord→load→lead: 7 pasos, valores intermedios
    6+6+6+7+5+5 = 35 (iron y lead no cuentan).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/C")
    - Fuerza bruta: OK en 500 casos aleatorios (diccionarios de ≤ 9 palabras
      de 1–3 letras sobre alfabetos pequeños, hasta 6 consultas con extremos
      repetidos, iguales o en otra componente) contra la enumeración por DFS
      de TODOS los caminos simples con aristas comprobadas par a par.
"""
import sys

VALOR_LETRA = {}
for letras, puntos in (("eaionrtlsu", 1), ("dg", 2), ("bcmp", 3), ("fhvwy", 4),
                       ("k", 5), ("jx", 8), ("qz", 10)):
    for ch in letras:
        VALOR_LETRA[ch] = puntos


def construir_cubetas(palabras):
    """Devuelve (miembros[b], cubetas_de[w]) sólo con cubetas de tamaño ≥ 2."""
    indice = {}
    miembros = []
    for w_id, w in enumerate(palabras):
        claves = [(p, w[:p] + w[p + 1:]) for p in range(len(w))]
        claves.append(("anagrama", "".join(sorted(w))))
        for clave in claves:
            b = indice.get(clave)
            if b is None:
                b = indice[clave] = len(miembros)
                miembros.append([])
            miembros[b].append(w_id)
    miembros = [m for m in miembros if len(m) >= 2]
    cubetas_de = [[] for _ in palabras]
    for b, m in enumerate(miembros):
        for w_id in m:
            cubetas_de[w_id].append(b)
    return miembros, cubetas_de


def componentes(n, miembros):
    """Union-find: comp[w] = representante de la componente conexa de w."""
    padre = list(range(n))

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for grupo in miembros:
        r0 = raiz(grupo[0])
        for x in grupo[1:]:
            rx = raiz(x)
            if rx != r0:
                padre[rx] = r0
    return [raiz(x) for x in range(n)]


def bfs_puntaje(raiz, objetivos, n, valor, miembros, cubetas_de, marca, sello):
    """BFS por capas desde `raiz` con DP de máximo; se detiene al terminar la
    capa en la que ya se alcanzaron todos los `objetivos` (o si se agota la
    componente). Devuelve (dist, punt)."""
    dist = [-1] * n
    punt = [0] * n
    dist[raiz] = 0
    faltan = set(objetivos)
    faltan.discard(raiz)
    capa = [raiz]
    d = 0
    while capa and faltan:
        nueva = []
        d1 = d + 1
        for u in capa:
            for b in cubetas_de[u]:
                if marca[b] == sello:
                    continue          # la cubeta ya se procesó en este BFS
                marca[b] = sello
                grupo = miembros[b]
                # Mejor puntaje entre los miembros de la capa actual d.
                mejor = max([punt[x] for x in grupo if dist[x] == d])
                for v in grupo:
                    dv = dist[v]
                    if dv == -1:            # nuevo: entra a la capa d+1
                        dist[v] = d1
                        punt[v] = mejor + valor[v]
                        nueva.append(v)
                    elif dv == d1:          # ya en la capa d+1: ¿mejora?
                        cand = mejor + valor[v]
                        if cand > punt[v]:
                            punt[v] = cand
        # La capa d+1 quedó COMPLETA: ya se pueden dar por resueltos sus
        # objetivos (antes de terminarla, otra cubeta podría mejorarlos).
        for v in nueva:
            faltan.discard(v)
        capa = nueva
        d = d1
    return dist, punt


def main():
    datos = sys.stdin.read().split()
    n = int(datos[0])
    palabras = datos[1:1 + n]
    q = int(datos[1 + n])
    consultas = [(datos[2 + n + 3 * i], datos[4 + n + 3 * i]) for i in range(q)]

    id_de = {w: i for i, w in enumerate(palabras)}
    valor = [sum(VALOR_LETRA[c] for c in w) for w in palabras]
    miembros, cubetas_de = construir_cubetas(palabras)
    comp = componentes(n, miembros)
    marca = [0] * len(miembros)   # «sello» del BFS que ya usó la cubeta

    respuesta = [None] * q
    pendientes = []               # índices de consultas que requieren BFS
    for i, (w1, w2) in enumerate(consultas):
        s, t = id_de[w1], id_de[w2]
        if s == t:
            respuesta[i] = "%s TO %s 0 0" % (w1, w2)
        elif comp[s] != comp[t]:
            # Distinta componente conexa: no hay camino (sin hacer BFS).
            respuesta[i] = "%s TO %s IMPOSSIBLE" % (w1, w2)
        else:
            pendientes.append(i)

    # La respuesta es SIMÉTRICA (el grafo es no dirigido y no se cuentan los
    # extremos), así que un BFS desde una palabra resuelve todas las
    # consultas en las que aparece como origen O como destino. Elegimos
    # vorazmente la palabra que más consultas pendientes cubre.
    sello = 0
    while pendientes:
        cuenta = {}
        for i in pendientes:
            for w in consultas[i]:
                cuenta[w] = cuenta.get(w, 0) + 1
        raiz_txt = max(cuenta, key=cuenta.get)
        raiz = id_de[raiz_txt]
        cubiertas = [i for i in pendientes if raiz_txt in consultas[i]]
        otros = {}
        for i in cubiertas:
            w1, w2 = consultas[i]
            otros[i] = id_de[w2] if w1 == raiz_txt else id_de[w1]
        sello += 1
        dist, punt = bfs_puntaje(raiz, set(otros.values()), n, valor,
                                 miembros, cubetas_de, marca, sello)
        for i in cubiertas:
            w1, w2 = consultas[i]
            o = otros[i]
            # punt[o] cuenta o pero no la raíz → se resta valor[o].
            respuesta[i] = "%s TO %s %d %d" % (w1, w2, dist[o], punt[o] - valor[o])
        cubiertas_set = set(cubiertas)
        pendientes = [i for i in pendientes if i not in cubiertas_set]

    sys.stdout.write("\n".join(respuesta) + ("\n" if respuesta else ""))


if __name__ == "__main__":
    main()
