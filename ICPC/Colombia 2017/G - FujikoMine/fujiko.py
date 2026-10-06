"""
Colombia 2017 — G: FujikoMine («FujikoMine»)
Ejecutar: python fujiko.py < fujiko.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Lupin quiere robar criptomonedas con el ransomware FujikoMine. La red es
    un árbol con raíz (cada nodo tiene <= 3 hijos) con nodos de TRANSMISIÓN y
    nodos PUENTE; cada arista padre-hijo vale w criptomonedas. Los puentes se
    infectan libremente; de transmisión se infectan exactamente x.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta EOF. Cada uno: "n m q"; n-1 líneas "u v w"
             (u es PADRE de v); m etiquetas de nodos de transmisión; q
             consultas x_j.
    Salida:  por consulta, una línea con el máximo botín infectando
             exactamente x_j nodos de transmisión.
    Restricciones clave: n <= 500, <= 3 hijos por nodo, w <= 500, q <= 100.

IDEA Y ALGORITMO
    Interpretación (deducida del ejemplo del enunciado):
      * Un ataque va de un nodo de transmisión infectado u a otro v que sea
        DESCENDIENTE de u (los caminos son hacia abajo: el enunciado dice que
        g y h, primos en el árbol, "no tienen camino" entre sí) y vale sólo si
        todos los nodos intermedios están infectados, o sea, si no pasa por
        un nodo de transmisión NO elegido (a,d da 0 porque b no está).
      * El botín es el peso de la UNIÓN de esos caminos (a,b,d vale 90, no
        20+70+90), y esa unión "debe formar un subárbol".
    Entonces una elección válida con x >= 2 es un subárbol conexo T cuya
    cima r es un nodo de transmisión, cuyas hojas son nodos de transmisión y
    que contiene exactamente x nodos de transmisión (todos elegidos). El
    botín es la suma de las aristas de T. Con x <= 1 el botín es 0.
    Si no existe ninguna elección válida (p. ej. x > m) se imprime 0, como en
    el ejemplo (x = 16 > 9 -> 0).

    DP EN ÁRBOL tipo MOCHILA sobre los hijos:
      F[v][k] = mejor peso de una estructura que baja desde v (v incluido),
                con k nodos de transmisión (contando a v si lo es), y cuyas
                hojas (distintas de v) son todas de transmisión.
      Combinación de hijos (a lo sumo 3): G[a] = mejor peso usando a nodos de
      transmisión entre las ramas escogidas; para cada hijo c con arista w,
      o se ignora la rama o se toma con b >= 1 nodos: G'[a+b] = G[a]+w+F[c][b].
      Si v es de transmisión: F[v][1+a] = G[a] (v cuenta y puede ser hoja).
      Si v es puente: F[v][a] = G[a] sólo para a >= 1 (un puente no puede
      ser hoja: esa arista no estaría en ningún camino de ataque).
      Respuesta(x) = max sobre nodos de transmisión r de F[r][x] (r es la
      cima del subárbol).
    La mochila sobre hijos cuesta O(tam(A)*tam(B)) por fusión; la suma total
    es O(n^2) (argumento clásico de "fusionar subárboles").

MACROALGORITMO
    1. Leer el árbol (padre -> hijos con peso) y marcar transmisores.
    2. Raíz = el nodo que no es hijo de nadie; orden BFS y recorrerlo al revés
       (post-orden sin recursión).
    3. Para cada nodo v: G = [0]; fusionar cada hijo como mochila.
    4. F[v] = G desplazado en 1 si v es transmisor; si es puente, G con
       G[0] = -inf.
    5. mejor[k] = max(F[v][k]) sobre transmisores v.
    6. Para cada consulta x: mejor[x] si existe y es finito (x >= 1), si no 0.

COMPLEJIDAD
    Tiempo O(n^2) por caso (~2.5*10^5 operaciones), memoria O(n^2) en el
    peor caso (listas F por nodo). Medido: 10 casos con n = 500
    (cadenas, árboles ternarios completos y aleatorios) en 0.32 s.

EJEMPLO A MANO
    x = 3 en el ejemplo: cima a, ramas a->b (20) y a->9->12->g (80): 100.
    x = 4: agregar b->10->d (40+30): 170. Coincide con la salida.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/G")
    - Fuerza bruta: OK en 1500 árboles aleatorios (n <= 10, m <= 8): se
      enumeran todos los subconjuntos de transmisores, se calcula la unión de
      los caminos de ataque válidos (ancestro -> descendiente, sin
      transmisores no elegidos en medio) y se exige que la unión sea conexa y
      toque a todos los elegidos.
    - AMBIGÜEDAD: el ejemplo no distingue esta lectura ("la unión debe ser UN
      subárbol conexo") de otra donde se permitieran varias componentes
      disjuntas sumadas. Se eligió la lectura literal del enunciado ("must
      form a subtree"); con la otra, algunos casos darían valores mayores.
"""
import sys
from collections import deque

NEG = float("-inf")


def resolver(n, hijos, es_transmisor, raiz):
    # Orden BFS desde la raíz; recorrerlo al revés procesa hijos antes que padres.
    orden = []
    cola = deque([raiz])
    while cola:
        v = cola.popleft()
        orden.append(v)
        for c, _ in hijos[v]:
            cola.append(c)

    F = [None] * n
    mejor = [NEG] * (n + 2)
    for v in reversed(orden):
        G = [0]                      # G[a]: mejor peso con a transmisores
        for c, w in hijos[v]:
            Fc = F[c]
            nuevo = G + [NEG] * (len(Fc) - 1)    # opción: ignorar la rama c
            for a, ga in enumerate(G):
                if ga == NEG:
                    continue
                base = ga + w
                for b in range(1, len(Fc)):
                    fb = Fc[b]
                    if fb != NEG and base + fb > nuevo[a + b]:
                        nuevo[a + b] = base + fb
            G = nuevo
            F[c] = None              # liberar memoria del hijo ya usado
        if es_transmisor[v]:
            Fv = [NEG] + G           # v cuenta como transmisor elegido
            for k in range(1, len(Fv)):
                if Fv[k] > mejor[k]:
                    mejor[k] = Fv[k]
        else:
            Fv = G
            Fv[0] = NEG              # un puente no puede terminar la estructura
        F[v] = Fv
    return mejor


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 2 < len(datos):
        n, m, q = int(datos[pos]), int(datos[pos + 1]), int(datos[pos + 2])
        pos += 3
        hijos = [[] for _ in range(n)]
        tiene_padre = [False] * n
        for _ in range(n - 1):
            u, v, w = int(datos[pos]), int(datos[pos + 1]), int(datos[pos + 2])
            pos += 3
            hijos[u].append((v, w))
            tiene_padre[v] = True
        es_transmisor = [False] * n
        for _ in range(m):
            es_transmisor[int(datos[pos])] = True
            pos += 1
        consultas = [int(x) for x in datos[pos:pos + q]]
        pos += q

        raiz = tiene_padre.index(False)
        mejor = resolver(n, hijos, es_transmisor, raiz)
        for x in consultas:
            valor = mejor[x] if 1 <= x <= n else NEG
            salida.append(str(valor if valor != NEG else 0))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
