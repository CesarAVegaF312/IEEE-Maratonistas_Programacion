"""
ACM ICPC Guangzhou Summer Series 2017 — A: Alice's Travels II («Los viajes de Alice II»)
Ejecutar: python alicetravels.py < alicetravels.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    El mundo es un árbol de N ciudades. En cada ciudad i hay gemas
    ilimitadas, todas con costo T_i y brillo S_i. Alice viaja de U a V por
    el único camino y puede comprar en cualquier ciudad del camino. Con K
    dólares, f(K) es el brillo total máximo que puede conseguir.

QUÉ HAY QUE HACER
    Entrada: hasta 20 casos hasta fin de archivo. Cada caso: N K; N−1
    aristas; los N costos T_i; los N brillos S_i; Q; Q líneas "U V" (el
    enunciado dice "tres enteros" pero son DOS: U y V).
    Salida:  por consulta, "g h" con g = f(1)+…+f(K) y h = f(1)^…^f(K) (XOR).
    Restricciones clave: N, Q ≤ 40000, 1 ≤ T_i ≤ K ≤ 61, S_i ≤ 10^6.
    Errata del ejemplo: dice Q = 5 pero solo trae 2 consultas (y la salida
    tiene 2 líneas); el programa responde las consultas que realmente hay
    si la entrada se acaba antes.

IDEA Y ALGORITMO
    1) Mochila ilimitada (unbounded knapsack). Las gemas de una ciudad son
       infinitas, así que f es la mochila ilimitada con los objetos
       (T_i, S_i) de las ciudades del camino y capacidad "a lo sumo k".
       Observación clave: de todas las ciudades del camino con el MISMO
       costo c solo importa la de mayor brillo (cualquier compra de las otras
       se cambia por esa sin perder). Como c ≤ 61, el camino se resume en un
       vector mejor[1..K] = máximo brillo con costo c en el camino (0 si no
       hay). Con ese vector:
           f(k) = max_{c=1..k} f(k − c) + mejor[c],   f(0) = 0,
       y como mejor[c] ≥ 0, el término c = 1 ya incluye "no gastar" un dólar
       (f(k) ≥ f(k−1)), que es lo que pide "empezó con K dólares".
    2) Máximo por costo en un camino del árbol — offline con un DFS:
       el camino U–V es la unión de los segmentos verticales U→LCA y
       V→LCA (LCA por binary lifting). Para un segmento vertical v→ancestro
       a se usa, para cada costo c, una PILA MONÓTONA de los nodos de costo
       c en el camino raíz→v: de arriba (raíz) hacia abajo el brillo es
       estrictamente decreciente (un nodo más profundo con brillo ≥ tapa a
       los anteriores más profundos que él… es decir, borra los de arriba de
       la pila con brillo ≤). Entonces el máximo de costo c en el segmento
       de profundidad ≥ prof(a) es la PRIMERA entrada de la pila con
       profundidad ≥ prof(a) (las más superficiales tienen más brillo pero
       están fuera; las eliminadas fueron tapadas por otra más profunda, que
       también está dentro). Se encuentra con búsqueda binaria.
       Al bajar por el DFS se "inserta" en O(log) reemplazando una posición y
       guardando lo que había, y al subir se restaura (pila con rollback),
       así cada consulta vertical se responde cuando el DFS está en v.
    3) Con el vector mejor de cada consulta se corre la mochila, con PODA DE
       DOMINADOS: el objeto de costo c solo se usa si su brillo supera lo
       que ya se logra con objetos de costo < c y presupuesto c (si no,
       cualquier copia suya se reemplaza por esa combinación). En datos
       típicos quedan pocos objetos útiles. Los vectores repetidos se
       responden desde una caché.

MACROALGORITMO
    1. Leer el caso; armar el árbol; DFS iterativo desde 1: padre,
       profundidad y orden.
    2. Tabla de binary lifting; para cada consulta calcular el LCA y anotar
       dos segmentos verticales (U, prof(LCA)) y (V, prof(LCA)).
    3. DFS iterativo con las K pilas monótonas (con rollback). Al entrar a
       v: insertar v en la pila de su costo; responder los segmentos que
       empiezan en v (una búsqueda binaria por costo) y combinarlos con
       máximo en el vector de la consulta. Al salir: restaurar.
    4. Para cada consulta: mochila ilimitada sobre el vector (podando los
       objetos dominados) → f(1..K).
    5. Imprimir Σ f y XOR de f.

COMPLEJIDAD
    Árbol y LCA: O((N + Q) log N). Segmentos: O(Q · C · log N), C = número
    de costos distintos (≤ 61). Mochila: O(Q · K · útiles), con útiles ≤ K
    (peor caso ≈ 1900 sumas por consulta). Medido con N = Q = 40000, K = 61:
    árbol aleatorio o en línea con datos al azar ~2.5 s por caso; caso
    adversario (línea con brillos superaditivos, todos los costos útiles)
    ~4.9 s por caso. Con 20 casos grandes en un mismo archivo el total
    (50–100 s) pasa del límite de 5 s del juez en Python.

EJEMPLO A MANO
    Consulta 5→4: camino 5–1–2–4 con gemas (5,50), (1,10), (2,15), (4,45).
    f(1..10) = 10, 20, 30, 45, 55, 65, 75, 90, 100, 110 → suma 600; el XOR
    da 64. ✔

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/A")
    - Fuerza bruta: OK en 400 casos aleatorios (N ≤ 30, K ≤ 12, árboles
      aleatorios y en línea, muchos costos repetidos) contra una versión que
      recorre el camino nodo a nodo (padres + profundidades) y hace la
      mochila ilimitada clásica con todos los objetos del camino.
"""
import sys
from bisect import bisect_left


def leer_casos(datos):
    """Generador de casos: (N, K, aristas, T, S, consultas)."""
    pos = 0
    total = len(datos)
    while pos + 1 < total:
        n, k = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        aristas = datos[pos:pos + 2 * (n - 1)]
        pos += 2 * (n - 1)
        costos = [0] + [int(x) for x in datos[pos:pos + n]]
        pos += n
        brillos = [0] + [int(x) for x in datos[pos:pos + n]]
        pos += n
        q = int(datos[pos])
        pos += 1
        # El ejemplo oficial dice Q = 5 pero trae solo 2 consultas: si el
        # archivo se acaba antes, se responden las consultas que haya.
        q = min(q, (total - pos) // 2)
        consultas = datos[pos:pos + 2 * q]
        pos += 2 * q
        yield n, k, aristas, costos, brillos, q, consultas


def resolver_caso(n, K, aristas, costos, brillos, q, consultas_raw):
    # --- Árbol: listas de adyacencia y DFS iterativo desde la raíz 1 -----
    ady = [[] for _ in range(n + 1)]
    for i in range(0, len(aristas), 2):
        x, y = int(aristas[i]), int(aristas[i + 1])
        ady[x].append(y)
        ady[y].append(x)
    padre = [0] * (n + 1)
    prof = [0] * (n + 1)
    orden = []
    visto = [False] * (n + 1)
    visto[1] = True
    pila = [1]
    while pila:
        v = pila.pop()
        orden.append(v)
        for w in ady[v]:
            if not visto[w]:
                visto[w] = True
                padre[w] = v
                prof[w] = prof[v] + 1
                pila.append(w)
    padre[1] = 1  # la raíz apunta a sí misma (cómodo para binary lifting)

    # --- Binary lifting para LCA -----------------------------------------
    saltos = [padre]
    while (1 << len(saltos)) <= n:
        ant = saltos[-1]
        saltos.append([ant[ant[v]] for v in range(n + 1)])

    def lca(u, v):
        if prof[u] < prof[v]:
            u, v = v, u
        dif = prof[u] - prof[v]
        b = 0
        while dif:
            if dif & 1:
                u = saltos[b][u]
            dif >>= 1
            b += 1
        if u == v:
            return u
        for tabla in reversed(saltos):
            if tabla[u] != tabla[v]:
                u, v = tabla[u], tabla[v]
        return padre[u]

    # Cada consulta → dos segmentos verticales (nodo inferior, prof. del LCA).
    segmentos = [[] for _ in range(n + 1)]
    for qi in range(q):
        u, v = int(consultas_raw[2 * qi]), int(consultas_raw[2 * qi + 1])
        dl = prof[lca(u, v)]
        segmentos[u].append((qi, dl))
        segmentos[v].append((qi, dl))

    # --- DFS con pilas monótonas por costo (con rollback) -----------------
    # Para el costo c: prof_c[c][0:largo[c]] crece (raíz→abajo) y
    # negb_c[c][0:largo[c]] = −brillo también crece (brillo decreciente).
    costos_usados = sorted(set(costos[1:]))
    prof_c = [[] for _ in range(K + 1)]
    negb_c = [[] for _ in range(K + 1)]
    largo = [0] * (K + 1)
    mejor = [None] * q          # vector mejor[1..K] de cada consulta

    pila = [(1, False)]
    deshacer = [None] * (n + 1)
    # Se recorre con una pila explícita: (v, salida?)
    while pila:
        v, salida = pila.pop()
        c = costos[v]
        if salida:
            # Restaurar la pila del costo c a como estaba antes de v.
            p, viejo_prof, viejo_negb, viejo_largo = deshacer[v]
            if viejo_prof is None:
                prof_c[c].pop()
                negb_c[c].pop()
            else:
                prof_c[c][p] = viejo_prof
                negb_c[c][p] = viejo_negb
            largo[c] = viejo_largo
            continue
        # Insertar v: se conservan las entradas con brillo > S_v.
        lc = largo[c]
        nb = negb_c[c]
        pc = prof_c[c]
        p = bisect_left(nb, -brillos[v], 0, lc)
        if p == len(nb):
            pc.append(prof[v])
            nb.append(-brillos[v])
            deshacer[v] = (p, None, None, lc)
        else:
            deshacer[v] = (p, pc[p], nb[p], lc)
            pc[p] = prof[v]
            nb[p] = -brillos[v]
        largo[c] = p + 1

        # Responder los segmentos verticales que bajan hasta v.
        for qi, dl in segmentos[v]:
            vec = mejor[qi]
            if vec is None:
                vec = mejor[qi] = [0] * (K + 1)
            for cc in costos_usados:
                lcc = largo[cc]
                if lcc:
                    i = bisect_left(prof_c[cc], dl, 0, lcc)
                    if i < lcc:
                        b = -negb_c[cc][i]
                        if b > vec[cc]:
                            vec[cc] = b

        pila.append((v, True))
        for w in ady[v]:
            if prof[w] > prof[v]:       # hijos (el vecino restante es el padre)
                pila.append((w, False))

    # --- Mochila ilimitada por consulta -----------------------------------
    cache = {}
    salida = []
    for qi in range(q):
        clave = tuple(mejor[qi])
        res = cache.get(clave)
        if res is None:
            res = cache[clave] = mochila(mejor[qi], K)
        salida.append(res)
    return salida


def mochila(vec, K):
    """f(k) = max(f(k−1), max_c f(k−c) + vec[c]); devuelve "Σf XORf".

    Poda de objetos dominados: al llegar a k, el mejor valor usando solo
    costos < k ya está calculado (sin_k). Si vec[k] ≤ sin_k, el objeto de
    costo k nunca sirve (cualquier copia suya se cambia por esa combinación
    más barata o igual, sin perder brillo), así que no se agrega a la lista
    de útiles. En datos típicos quedan pocos útiles y la mochila es casi
    O(K); en el peor caso (brillos superaditivos) todos son útiles y es
    O(K²/2)."""
    f = [0] * (K + 1)
    utiles = []                 # pares (costo, brillo) no dominados
    suma = 0
    xor = 0
    for k in range(1, K + 1):
        sin_k = f[k - 1]        # gastar a lo sumo k: nunca peor que k − 1
        if utiles:
            mejor_util = max([f[k - c] + b for c, b in utiles])
            if mejor_util > sin_k:
                sin_k = mejor_util
        if vec[k] > sin_k:      # el objeto de costo k aporta algo nuevo
            utiles.append((k, vec[k]))
            sin_k = vec[k]
        f[k] = sin_k
        suma += sin_k
        xor ^= sin_k
    return "%d %d" % (suma, xor)


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for caso in leer_casos(datos):
        salida.extend(resolver_caso(*caso))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
