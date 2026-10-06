"""
Colombia 2026 — C: Into the Onion («Dentro de la cebolla»)
Ejecutar: python onion.py < onion.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Unos biólogos cortan una cebolla y ven N células en el plano, cada una con
    un valor w. Las células se agrupan en CAPAS: L1 = células sobre el borde
    del casco convexo (vértices y puntos sobre los lados); se quitan y L2 es
    el borde del casco de las restantes; etc. La última capa es el corazón.
    Un marcador entra por una célula de L1 y salta capa a capa hacia adentro.

QUÉ HAY QUE HACER
    Entrada: varios casos; N y luego N líneas "x y w". Termina con N = 0.
    Salida:  por caso, la máxima suma de valores w de un recorrido
             L1 → L2 → … → LK (una célula por capa) o -1 si ninguno llega al
             corazón.
    Regla de salto: de u ∈ Li a v ∈ Li+1 si dist(u, v) <= (3/2)·d(Li, Li+1),
             donde d(Li, Li+1) es la MÍNIMA distancia entre una célula de Li
             y una de Li+1 (todas las células, no solo las alcanzables).
    Restricciones clave: N <= 3000, |x|, |y| <= 10^8, 1 <= w <= 10^6.

IDEA Y ALGORITMO
    1) "Pelado de cebolla" (onion peeling / convex layers) con la cadena
       monótona de Andrew, SIN descartar los puntos colineales: en cada
       cadena (inferior y superior) solo se saca un punto cuando hay un giro
       estrictamente a la derecha (producto cruz < 0); con cruz = 0 el punto
       está sobre un lado del casco y debe pertenecer a la capa.
       Si todos los puntos restantes son colineales, el "polígono" es un
       segmento y todos quedan en el borde (la cadena los conserva todos).
       Se ordena una sola vez por (x, y) y en cada capa se filtran los
       puntos ya usados, así el orden se mantiene sin reordenar.
    2) Distancias sin raíces ni flotantes: dist(u,v) <= 3/2·d  ⇔
       4·dist²(u,v) <= 9·d²  (todo entero, exacto).
    3) Programación dinámica por capas (es un DAG por niveles):
           mejor[v] = w_v + max{ mejor[u] : u ∈ Li alcanzable, u → v }
       con mejor[u] = w_u para u ∈ L1. La respuesta es max(mejor) en el
       corazón, o -1 si ninguna célula del corazón es alcanzable (en cuanto
       una capa queda sin células alcanzables ya se puede responder -1).
       Como w >= 1, cualquier camino válido tiene valor > 0.

MACROALGORITMO
    1. Leer las N células.
    2. Ordenar por (x, y); repetir: calcular el borde del casco (con
       colineales), guardarlo como capa, quitar esos puntos. Hasta vaciar.
    3. mejor = {u: w_u} para las células de L1.
    4. Para cada par de capas consecutivas (Li, Li+1):
         a. d² = mínima distancia² entre TODAS las células de Li y Li+1.
         b. para cada v ∈ Li+1: buscar el mayor mejor[u] (u alcanzable en Li)
            con 4·dist²(u,v) <= 9·d²; si existe, mejor'[v] = ese + w_v.
         c. si nadie de Li+1 es alcanzable → -1.
    5. Imprimir max(mejor) sobre el corazón.

COMPLEJIDAD
    Pelado: O(N·K) (K = número de capas <= N/3), DP: O(Σ |Li|·|Li+1|)
    <= O(N²/4). Memoria O(N).
    Medido: N = 3000 en 1000 triángulos anidados (peor caso del pelado)
    ≈ 1.4 s; N = 3000 en dos capas de 1500 (peor caso de la DP) ≈ 0.6 s;
    N = 3000 aleatorio ≈ 0.2 s. Con muchos casos máximos Python sería lento.

EJEMPLO A MANO (el de la figura del enunciado, 7 células)
    L1 = {c1, c2, c3, c4}, L2 = {c5, c6, c7}; d(L1, L2) = dist(c3, c7) =
    sqrt(2), radio = 1.5·sqrt(2) ≈ 2.12. c1 → c5 (dist sqrt(4) = 2) y
    c3 → c7. Mejor: w3 + w7 = 1 + 8 = 9.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/C")
    - Fuerza bruta: capas con el criterio "p está en el borde si existe otro
      punto q tal que todos los puntos quedan del mismo lado (cerrado) de la
      recta pq" en O(n³), y DFS que enumera TODOS los caminos con distancias
      en punto flotante: idéntica en 1500 casos aleatorios (N <= 14,
      coordenadas pequeñas para forzar colineales, capas degeneradas en
      segmento y respuestas -1).
"""
import sys


def borde_casco(pts):
    """pts: lista de (x, y, idx) ORDENADA por (x, y). Devuelve los idx de los
    puntos sobre el borde del casco convexo, incluyendo los colineales."""
    if len(pts) <= 2:
        return [p[2] for p in pts]

    def cadena(secuencia):
        pila = []
        for p in secuencia:
            px, py, _ = p
            # Se saca el tope solo con giro ESTRICTO a la derecha (cruz < 0);
            # si cruz == 0 el tope está sobre el lado y se conserva.
            while len(pila) >= 2:
                (ox, oy, _), (ax, ay, _) = pila[-2], pila[-1]
                if (ax - ox) * (py - oy) - (ay - oy) * (px - ox) < 0:
                    pila.pop()
                else:
                    break
            pila.append(p)
        return pila

    inferior = cadena(pts)
    superior = cadena(reversed(pts))
    # Los extremos (y, si todo es colineal, todos) aparecen en ambas cadenas.
    return list({p[2] for p in inferior} | {p[2] for p in superior})


def pelar_capas(celdas):
    """Lista de capas (listas de índices), de la más externa al corazón."""
    restantes = sorted((x, y, i) for i, (x, y, _) in enumerate(celdas))
    capas = []
    while restantes:
        capa = borde_casco(restantes)
        capas.append(capa)
        usados = set(capa)
        # Filtrar conserva el orden por (x, y): no hace falta reordenar.
        restantes = [p for p in restantes if p[2] not in usados]
    return capas


def resolver(celdas):
    capas = pelar_capas(celdas)

    # mejor[i] = máximo valor acumulado al llegar a la célula i (solo
    # células alcanzables de la capa actual).
    mejor = {i: celdas[i][2] for i in capas[0]}

    for t in range(len(capas) - 1):
        capa_i, capa_sig = capas[t], capas[t + 1]
        xs = [celdas[u][0] for u in capa_i]
        ys = [celdas[u][1] for u in capa_i]

        # (a) d² = distancia mínima² entre TODAS las células de Li y Li+1.
        d2 = min(
            min([(xu - xv) * (xu - xv) + (yu - yv) * (yu - yv) for xu, yu in zip(xs, ys)])
            for xv, yv, _ in (celdas[v] for v in capa_sig)
        )
        limite = 9 * d2                    # 4·dist² <= 9·d²  ⇔  dist <= 1.5·d

        # (b) Células alcanzables de Li ordenadas de mayor a menor valor: para
        # cada v basta encontrar la PRIMERA que lo alcance (es la mejor).
        alcanzables = sorted(((mejor[u], celdas[u][0], celdas[u][1]) for u in mejor),
                             reverse=True)
        nuevo = {}
        for v in capa_sig:
            xv, yv, wv = celdas[v]
            for val, xu, yu in alcanzables:
                dx, dy = xu - xv, yu - yv
                if 4 * (dx * dx + dy * dy) <= limite:
                    nuevo[v] = val + wv
                    break
        if not nuevo:                      # (c) el marcador no puede seguir
            return -1
        mejor = nuevo

    return max(mejor.values())


def main():
    datos = sys.stdin.buffer.read().split()
    idx, salida = 0, []
    while idx < len(datos):
        n = int(datos[idx])
        idx += 1
        if n == 0:                         # fin de la entrada
            break
        vals = list(map(int, datos[idx: idx + 3 * n]))
        idx += 3 * n
        celdas = [(vals[3 * j], vals[3 * j + 1], vals[3 * j + 2]) for j in range(n)]
        salida.append(resolver(celdas))
    sys.stdout.write("\n".join(map(str, salida)) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
