"""
Colombia 2018 — I: Impossible Communication («Comunicación imposible»)
Ejecutar: python impossible.py < impossible.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Una universidad tiene N grupos de investigación y M procedimientos para
    pasar información: unos dirigidos (de I a J) y otros «complejos» que
    permiten compartir en ambos sentidos entre k grupos. El rector quiere
    saber si cualquier grupo puede hacer llegar información a cualquier otro.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta fin de archivo. Cada caso: «N M» y M líneas.
             «1 I J» = arista dirigida I→J; «k I1 ... Ik» (k ≥ 2) = todos los
             pares de esos k grupos se comunican en ambos sentidos.
    Salida:  «YES» si el grafo es fuertemente conexo, «NO» si no.
    Restricciones clave: N ≤ 50 000, M ≤ 1 000, k ≤ 1 000 (hasta ~10^6
             apariciones de grupos por caso).

IDEA Y ALGORITMO
    Conectividad fuerte con dos BFS (idea de Kosaraju simplificada):
    un grafo dirigido es fuertemente conexo  ⇔  desde un vértice cualquiera
    (el 1) se alcanzan todos los vértices en el grafo original Y también en
    el grafo transpuesto (aristas invertidas). (Si todo v es alcanzable desde
    1 y 1 es alcanzable desde todo v, entonces u → 1 → v para todo par.)

    El problema: un procedimiento complejo con k grupos equivale a una
    clique bidireccional de k·(k-1) aristas → hasta ~10^9 aristas. Se
    reemplaza por un NODO VIRTUAL («estrella»): por cada procedimiento
    complejo se crea un vértice extra h con aristas Ii→h y h→Ii para cada
    miembro. Así Ii llega a Ij pasando por h, y el nodo virtual no crea
    caminos nuevos entre grupos que no estuvieran en la clique. Las
    alcanzabilidades entre vértices reales quedan idénticas, con sólo 2k
    aristas por procedimiento. Los nodos virtuales no hace falta exigirlos
    en la verificación (sólo importan los grupos reales).

MACROALGORITMO
    1. Leer todos los tokens; por cada caso leer N, M.
    2. Para cada procedimiento: si empieza en 1 → arista I→J; si empieza en
       k ≥ 2 → crear nodo virtual h y aristas Ii↔h.
    3. Construir listas de adyacencia del grafo y de su transpuesto.
    4. BFS desde el grupo 1 en el grafo: ¿alcanza a los N grupos?
    5. BFS desde el grupo 1 en el transpuesto: ¿alcanza a los N grupos?
    6. Imprimir YES si ambas respuestas son sí, NO en otro caso.

COMPLEJIDAD
    Tiempo O(N + M + Σk) por caso, memoria igual. Caso grande
    (N = 50 000, M = 1 000, k = 1 000 en cada procedimiento, más otro caso
    con 1 000 aristas simples): ~0.9 s en Python.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/I")
    - Fuerza bruta: OK en 500 casos aleatorios pequeños contra una cerradura
      transitiva (Floyd–Warshall) con las cliques expandidas explícitamente.
"""
import sys


def fuertemente_conexo(n_total, n_reales, ady, ady_t):
    """¿Desde el vértice 1 se alcanzan todos los grupos 1..n_reales en el
    grafo y en su transpuesto?"""
    for grafo in (ady, ady_t):
        visto = bytearray(n_total + 1)
        visto[1] = 1
        pila = [1]
        alcanzados_reales = 1
        while pila:
            u = pila.pop()
            for v in grafo[u]:
                if not visto[v]:
                    visto[v] = 1
                    if v <= n_reales:
                        alcanzados_reales += 1
                    pila.append(v)
        if alcanzados_reales < n_reales:
            return False
    return True


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        n = int(datos[pos]); m = int(datos[pos + 1]); pos += 2
        # Primero leemos los procedimientos para saber cuántos nodos
        # virtuales hacen falta (uno por procedimiento complejo).
        simples = []    # pares (I, J)
        complejos = []  # listas de miembros
        for _ in range(m):
            k = int(datos[pos]); pos += 1
            if k == 1:
                simples.append((int(datos[pos]), int(datos[pos + 1])))
                pos += 2
            else:
                complejos.append([int(x) for x in datos[pos:pos + k]])
                pos += k
        n_total = n + len(complejos)
        ady = [[] for _ in range(n_total + 1)]
        ady_t = [[] for _ in range(n_total + 1)]
        for i, j in simples:
            ady[i].append(j)
            ady_t[j].append(i)
        # Nodo virtual h = n+1, n+2, ...: estrella bidireccional.
        for idx, miembros in enumerate(complejos):
            h = n + 1 + idx
            ady[h].extend(miembros)
            ady_t[h].extend(miembros)
            for x in miembros:
                ady[x].append(h)
                ady_t[x].append(h)
        salida.append("YES" if fuertemente_conexo(n_total, n, ady, ady_t) else "NO")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
