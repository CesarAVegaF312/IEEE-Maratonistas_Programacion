"""
Colombia 2026 — M: Byte Flu («Gripe de bytes»)
Ejecutar: python flu.py < flu.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un virus salta entre dispositivos de una red cuando sus identificadores
    (cadenas) están a distancia de edición <= K. Algunos dispositivos están
    infectados al inicio y otros son críticos; los administradores pueden
    desconectar dispositivos (ni críticos ni infectados) pagando su costo.
    Quieren el costo mínimo para que el virus no llegue a ningún crítico.

QUÉ HAY QUE HACER
    Entrada: varios casos: "N K I C", N líneas "identificador costo", una
             línea con los I infectados y otra con los C críticos (índices
             1..N). Termina con "0 0 0 0".
    Salida:  por caso, el costo mínimo; 0 si no hace falta desconectar
             nada; -1 si es imposible.
    Restricciones clave: N <= 1000 (hasta ~5·10^5 pares), K <= 20,
             |identificador| <= 20, costos <= 10^6.

IDEA Y ALGORITMO
    Dos partes: (1) construir el grafo con distancia de Levenshtein y
    (2) corte mínimo de VÉRTICES = flujo máximo (teorema max-flow min-cut).

    1) Grafo. Hay arista u—v si lev(s_u, s_v) <= K. Se calcula con el
       algoritmo bit-paralelo de Myers (1999): la columna de la tabla de
       programación dinámica se guarda como bits de "+1/-1" verticales en
       dos enteros, y cada letra de la otra cadena se procesa con ~15
       operaciones de bits (O(|t|) por par en vez de O(|s|·|t|)). Filtros
       baratos antes de Myers: si || s_u | - | s_v || > K no hay arista; si
       K >= max(|s_u|, |s_v|) siempre hay arista (caso particular de la
       cota siguiente). Aceptación
       rápida: lev <= (#posiciones distintas en el prefijo común) +
       diferencia de largos (se calcula con map en C). Además Myers
       corta temprano: si a la distancia actual de la última fila le quitamos
       las letras que faltan y aún supera K, ya no puede bajar a K.

    2) ¿Cuándo es imposible? Solo se pueden quitar dispositivos "libres".
       Si un infectado es VECINO DIRECTO de un crítico no hay nada que
       cortar: -1. Si no, cualquier camino infectado -> crítico pasa por al
       menos un dispositivo libre, así que quitar todos los libres siempre
       funciona: la respuesta es finita. Por eso se revisan primero los pares
       (infectado, crítico) y, si alguno está conectado, se responde -1 sin
       construir todo el grafo ni correr el flujo.

    3) Corte mínimo de vértices como flujo. Cada dispositivo libre v se
       parte en entrada(v) -> salida(v) con capacidad c_v (cortar el arco =
       desconectar v). Cada arista u—v entre libres da salida(u) -> entrada(v)
       y salida(v) -> entrada(u) con capacidad "infinita". Todos los
       infectados se FUSIONAN en la fuente S (arco S -> entrada(v) si v es
       vecino de un infectado) y todos los críticos en el sumidero T
       (salida(v) -> T). Las aristas infectado—infectado y crítico—crítico
       no importan. Un corte S-T finito solo puede usar arcos entrada->salida,
       es decir, conjuntos de dispositivos libres que separan; por max-flow
       min-cut su costo mínimo es el flujo máximo, que se calcula con Dinic
       (BFS por niveles + DFS de caminos de aumento con punteros).
       "Infinito" = 1 + suma de todos los costos (entero; nunca se alcanza).

    Por qué no lo ingenuo: probar todos los subconjuntos de dispositivos es
    2^N; y la distancia de edición clásica por par O(20·20) sobre 5·10^5
    pares sería ~2·10^8 operaciones en Python.

MACROALGORITMO
    1. Leer el caso; marcar infectados y críticos.
    2. Si algún par (infectado, crítico) está a distancia <= K: imprimir -1.
    3. Para cada par de dispositivos con al menos uno libre: filtro por
       longitudes, aceptación rápida y, si hace falta, Myers con corte
       temprano; si están conectados, agregar los arcos de flujo que
       correspondan (libre-libre, infectado-libre o libre-crítico).
    4. Arcos entrada(v) -> salida(v) con capacidad c_v para cada libre.
    5. Dinic de S a T; imprimir el flujo máximo.

COMPLEJIDAD
    Grafo: O(N^2 · L) operaciones de bits con L <= 20.
    Flujo: Dinic O(V^2 · E) en teoría, mucho menos en la práctica.
    Casos grandes medidos (N = 1000, un caso; la máquina estaba compartida,
    los tiempos variaron ±50 % entre corridas):
      K=10, 20 letras sobre {a,b} (≈4.8·10^5 aristas, respuesta finita):
          ~4.5–5.5 s (≈3 s construir el grafo, ≈1 s el flujo)
      K=19, alfabeto de 10 letras (casi completo):          ~1.6 s
      K=3 sobre {a,b}, longitudes 1..20:                    ~1.3 s
      K=2, 26 letras (casi sin aristas):                    ~1.5 s
      K=5 con respuesta -1:                                 ~0.06 s
      10 casos como el de K=3 seguidos:                     ~14 s
    Versión del usuario en los mismos: 10–34 s, 2.7–6 s, 1.3–1.8 s,
    1.3–1.7 s, 3–18 s y ~29 s.
    El enunciado no acota la cantidad de casos: cada caso con N = 1000
    cuesta ≥ ~1.3 s solo por los 5·10^5 pares, así que con muchos casos
    grandes Python puede pasarse del límite del juez.

EJEMPLO A MANO
    Caso 1 (K=1): aaa infectado, bba crítico. aaa—baa, aaa—aba, baa—bba,
    aba—bba; aaa y bba no son vecinos (distancia 2). Caminos S->baa->T y
    S->aba->T, de capacidades 4 y 7: flujo 11 = cortar baa y aba.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/M")
    - Fuerza bruta: OK en 4000 casos aleatorios (N <= 10, cadenas de largo
      1..5 sobre alfabetos de 2–4 letras, K de 0 a 5; una tanda de 2000 con
      ~65 % de respuestas -1 y otra de 2000 con ~22 %) contra Levenshtein por
      DP clásica + prueba de TODOS los subconjuntos de dispositivos libres
      con BFS.
    - Coincide con flu.py del usuario en todos los casos grandes.
"""
import sys
from collections import deque
from operator import ne


# ----------------------------------------------------------------------------
# Distancia de edición (Myers bit-paralelo)
# ----------------------------------------------------------------------------
def mascaras_por_letra(s):
    """peq[c] = bits de las posiciones de s donde aparece la letra de código
    c (s es bytes; una lista indexada por código es más rápida que un dict)."""
    peq = [0] * 128
    for i, ch in enumerate(s):
        peq[ch] |= 1 << i
    return peq


def a_lo_sumo_k(peq, m, t, k):
    """True si lev(s, t) <= k, donde s (longitud m >= 1) viene dada por sus
    máscaras peq. Invariante: pv/mv son los bits de diferencias verticales
    +1/-1 de la columna actual y 'dist' es el valor de la última fila."""
    mascara = (1 << m) - 1
    alto = 1 << (m - 1)
    pv, mv, dist = mascara, 0, m
    restantes = len(t)
    for ch in t:
        restantes -= 1
        eq = peq[ch]
        xv = eq | mv
        xh = ((((eq & pv) + pv) & mascara) ^ pv) | eq
        ph = mv | (~(xh | pv) & mascara)
        mh = pv & xh
        if ph & alto:
            dist += 1
        elif mh & alto:
            dist -= 1
        ph = ((ph << 1) | 1) & mascara
        mh = (mh << 1) & mascara
        pv = mh | (~(xv | ph) & mascara)
        mv = ph & xv
        # Cada letra restante puede bajar la distancia en 1 como máximo.
        if dist - restantes > k:
            return False
    return dist <= k


# ----------------------------------------------------------------------------
# Flujo máximo (Dinic sobre arreglos planos)
# ----------------------------------------------------------------------------
class Dinic:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]   # índices de arcos que salen de cada nodo
        self.dest = []                      # dest[e]: nodo destino del arco e
        self.cap = []                       # cap[e]: capacidad residual
        # El arco e y su reverso son e y e ^ 1 (se agregan en pareja).

    def arco(self, u, v, c):
        self.adj[u].append(len(self.dest))
        self.dest.append(v)
        self.cap.append(c)
        self.adj[v].append(len(self.dest))
        self.dest.append(u)
        self.cap.append(0)

    def flujo_maximo(self, s, t):
        adj, dest, cap, n = self.adj, self.dest, self.cap, self.n
        total = 0
        while True:
            # BFS: nivel[v] = distancia desde s en el grafo residual.
            nivel = [-1] * n
            nivel[s] = 0
            cola = deque([s])
            while cola:
                u = cola.popleft()
                siguiente = nivel[u] + 1
                for e in adj[u]:
                    if cap[e] and nivel[dest[e]] < 0:
                        nivel[dest[e]] = siguiente
                        cola.append(dest[e])
            if nivel[t] < 0:
                return total
            # DFS iterativo con punteros: busca caminos s -> t que suban de
            # nivel de a uno; los callejones sin salida se descartan.
            ptr = [0] * n
            camino = []                     # arcos del camino actual
            u = s
            while True:
                if u == t:
                    # Aumentar por el cuello de botella y retroceder hasta
                    # el primer arco saturado.
                    f = min(cap[e] for e in camino)
                    total += f
                    corte = len(camino)
                    for i, e in enumerate(camino):
                        cap[e] -= f
                        cap[e ^ 1] += f
                        if cap[e] == 0 and i < corte:
                            corte = i
                    del camino[corte:]
                    u = dest[camino[-1]] if camino else s
                    continue
                lista = adj[u]
                avanzo = False
                while ptr[u] < len(lista):
                    e = lista[ptr[u]]
                    v = dest[e]
                    if cap[e] and nivel[v] == nivel[u] + 1:
                        camino.append(e)
                        u = v
                        avanzo = True
                        break
                    ptr[u] += 1
                if not avanzo:
                    if u == s:
                        break                # no hay más caminos en esta fase
                    nivel[u] = -1            # callejón: no volver a entrar
                    e = camino.pop()
                    u = dest[e ^ 1]          # nodo anterior
                    ptr[u] += 1


# ----------------------------------------------------------------------------
# Resolución de un caso
# ----------------------------------------------------------------------------
LIBRE, INFECTADO, CRITICO = 0, 1, 2


def conectados(i, j, ids, largos, peqs, k):
    """True si el virus salta directamente entre los dispositivos i y j."""
    li, lj = largos[i], largos[j]
    dif = li - lj if li > lj else lj - li
    if dif > k:
        return False                 # cota inferior: lev >= diferencia de largos
    # Cota superior barata (aceptación rápida): reemplazar letra a letra el
    # prefijo común en largo y borrar/insertar lo que sobra:
    # lev <= #posiciones distintas en el prefijo + diferencia de largos.
    if sum(map(ne, ids[i], ids[j])) + dif <= k:
        return True
    return a_lo_sumo_k(peqs[i], li, ids[j], k)


def resolver(n, k, ids, costos, infectados, criticos):
    tipo = [LIBRE] * n
    for i in infectados:
        tipo[i] = INFECTADO
    for i in criticos:
        tipo[i] = CRITICO
    largos = [len(s) for s in ids]
    peqs = [mascaras_por_letra(s) for s in ids]

    # Paso 2: imposible <=> algún infectado es vecino directo de un crítico.
    for i in infectados:
        for j in criticos:
            if conectados(i, j, ids, largos, peqs, k):
                return -1

    # Red de flujo: entrada(v) = v, salida(v) = n + v, S = 2n, T = 2n + 1.
    infinito = sum(costos) + 1
    S, T = 2 * n, 2 * n + 1
    red = Dinic(2 * n + 2)
    for v in range(n):
        if tipo[v] == LIBRE:
            red.arco(v, n + v, costos[v])           # desconectar v cuesta c_v

    # Paso 3: aristas por distancia de edición.
    for i in range(n):
        ti = tipo[i]
        for j in range(i + 1, n):
            tj = tipo[j]
            if ti != LIBRE and tj != LIBRE:
                continue          # I-I y C-C no importan; I-C ya se revisó
            if not conectados(i, j, ids, largos, peqs, k):
                continue
            if ti == LIBRE and tj == LIBRE:
                red.arco(n + i, j, infinito)
                red.arco(n + j, i, infinito)
            else:
                libre, otro = (i, tj) if ti == LIBRE else (j, ti)
                if otro == INFECTADO:
                    red.arco(S, libre, infinito)     # el virus entra a 'libre'
                else:
                    red.arco(n + libre, T, infinito)  # 'libre' toca un crítico
    return red.flujo_maximo(S, T)


def main():
    datos = sys.stdin.buffer.read().split()
    idx, salida = 0, []
    while idx + 3 < len(datos):
        n, k, ni, nc = (int(x) for x in datos[idx: idx + 4])
        idx += 4
        if n == 0 and k == 0 and ni == 0 and nc == 0:   # fin de la entrada
            break
        ids, costos = [], []
        for _ in range(n):
            ids.append(datos[idx])          # bytes: iterar da códigos de letra
            costos.append(int(datos[idx + 1]))
            idx += 2
        infectados = [int(x) - 1 for x in datos[idx: idx + ni]]
        idx += ni
        criticos = [int(x) - 1 for x in datos[idx: idx + nc]]
        idx += nc
        salida.append(resolver(n, k, ids, costos, infectados, criticos))
    sys.stdout.write("\n".join(map(str, salida)) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
