"""
Colombia 2025 — C: Celestial Veins («Venas celestiales»)
Ejecutar: python celestial.py < celestial.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Los Luminari, astrónomos antiguos, dibujaban las estrellas en un plano.
    Dos estrellas forman un "vínculo" si cada una está entre las K vecinas
    más cercanas de la otra (vecinos mutuos). Las componentes conexas de ese
    grafo de vínculos son "constelaciones" y se clasifican por su forma.

QUÉ HAY QUE HACER
    Entrada: varios mapas; cada uno empieza con "N K" y siguen N líneas "X Y".
             Termina con "0 0".
    Salida:  por mapa, cinco enteros: cantidad de Camino del Viajero,
             Ouroboros Cósmico, Cúmulo Estelar, Garra del Dragón y Nebulosa
             Amorfa (en ese orden).
    Restricciones clave: N ≤ 1 500, K ≤ 5, |X|,|Y| ≤ 10^9.
    Empates de distancia: gana la estrella de menor índice (orden de entrada).

IDEA Y ALGORITMO
    1) K vecinos más cercanos por fuerza bruta: para cada estrella i se
       calculan las distancias AL CUADRADO (enteras: no hay errores de punto
       flotante y el orden es el mismo que con la distancia real) a todas las
       demás y se toman las K menores con la clave (distancia², índice), que
       implementa exactamente el desempate por índice de crónica.
       N² = 2.25·10^6 distancias por mapa: aceptable. (Un k-d tree no hace
       falta con N ≤ 1500.)
    2) Grafo de vínculos: arista i–j si j ∈ vecinos(i) e i ∈ vecinos(j).
       Cada vértice tiene grado ≤ K ≤ 5.
    3) Componentes conexas con BFS; para cada una se cuentan s = #estrellas,
       e = #vínculos y los grados. Clasificación en el ORDEN DE PRIORIDAD
       del enunciado:
         - s == 1                      → Nebulosa (estrella aislada).
         - e == s(s−1)/2               → Cúmulo (grafo completo; incluye el
                                          par suelto s=2 y el triángulo).
         - e == s y todos grado 2      → Ouroboros (conexo + 2-regular = ciclo).
         - e == s−1 y algún grado s−1  → Garra (estrella: un centro unido a
                                          todos; con e = s−1 las hojas no
                                          pueden tener aristas entre sí).
         - e == s−1 y grado máximo ≤ 2 → Camino (árbol sin ramificaciones).
         - en otro caso                → Nebulosa.
       Por qué basta mirar e y los grados: una componente CONEXA con e = s−1
       es un árbol; un árbol con grados ≤ 2 es un camino; una conexa con
       todos los grados 2 es un ciclo. El camino de 3 estrellas es también
       una garra; gana la garra por prioridad (se evalúa antes).

MACROALGORITMO
    1. Leer N, K; si ambos son 0, terminar. Leer las N coordenadas.
    2. Para cada estrella, calcular sus K vecinas más cercanas (distancia²,
       índice) y guardarlas en un conjunto.
    3. Construir la lista de adyacencia con los vínculos mutuos.
    4. Recorrer componentes con BFS contando estrellas, aristas y grados.
    5. Clasificar cada componente según la tabla de prioridades.
    6. Imprimir los cinco contadores en el orden pedido.

COMPLEJIDAD
    Tiempo O(N² + N·log K) por mapa (dominado por las distancias),
    memoria O(N). En Python ≈ 0.5 s por mapa con N = 1500; si el juez trae
    muchos mapas grandes podría ser lento.

EJEMPLO A MANO
    Segundo mapa (K = 2): (0,0),(1,0),(0,1) son vecinos mutuos dos a dos →
    Cúmulo. En (100,0)…(103,0): 100↔101, 101↔102, 102↔103 son mutuos
    (101 elige a 100 y 102; 102 elige a 101 y 103), pero 100–102 no lo es →
    camino de 4 → "1 0 1 0 0".

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/C")
    - Fuerza bruta (ordenar todas las distancias + clasificar comprobando las
      definiciones directamente: todos los pares unidos, recorrido del ciclo,
      búsqueda de un centro, etc.): OK en 1500 mapas aleatorios pequeños con
      coordenadas en rangos chicos (muchos empates y puntos repetidos).
    - Caso grande (N = 1500, K = 5, coordenadas hasta 10^9): ~0.5 s por mapa.
"""
import sys
import heapq
from collections import deque


def vecinos_cercanos(xs, ys, k):
    """Para cada estrella, conjunto de sus k vecinas más cercanas.

    Desempate por índice: heapq.nsmallest es estable (equivale a sorted(...)[:k])
    y recorre range(n) en orden creciente, así que a igual distancia gana el
    índice menor.
    """
    n = len(xs)
    indices = range(n)
    resultado = []
    for i in range(n):
        xi, yi = xs[i], ys[i]
        dist = [(xi - x) * (xi - x) + (yi - y) * (yi - y) for x, y in zip(xs, ys)]
        dist[i] = -1  # la propia estrella queda primera y se descarta
        mejores = heapq.nsmallest(k + 1, indices, key=dist.__getitem__)
        resultado.append(set(mejores[1:]))
    return resultado


def clasificar(s, e, grados):
    """Devuelve el índice de categoría en el orden de SALIDA:
    0 Camino, 1 Ouroboros, 2 Cúmulo, 3 Garra, 4 Nebulosa."""
    if s == 1:
        return 4  # estrella aislada
    if e == s * (s - 1) // 2:
        return 2  # cúmulo: todos con todos
    if e == s and all(g == 2 for g in grados):
        return 1  # ciclo
    if e == s - 1:  # árbol (la componente es conexa)
        if max(grados) == s - 1:
            return 3  # estrella con centro
        if max(grados) <= 2:
            return 0  # camino
    return 4


def resolver(xs, ys, k):
    n = len(xs)
    cerca = vecinos_cercanos(xs, ys, k)
    # Vínculo solo si la relación es mutua.
    ady = [[j for j in cerca[i] if i in cerca[j]] for i in range(n)]

    conteo = [0] * 5
    visitado = [False] * n
    for inicio in range(n):
        if visitado[inicio]:
            continue
        # BFS de la componente: se guardan los grados de sus estrellas.
        visitado[inicio] = True
        cola = deque([inicio])
        grados = []
        while cola:
            u = cola.popleft()
            grados.append(len(ady[u]))
            for v in ady[u]:
                if not visitado[v]:
                    visitado[v] = True
                    cola.append(v)
        s = len(grados)
        e = sum(grados) // 2  # cada vínculo se cuenta desde sus dos extremos
        conteo[clasificar(s, e, grados)] += 1
    return conteo


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        n, k = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        if n == 0 and k == 0:  # caso de fin
            break
        coords = list(map(int, datos[pos:pos + 2 * n]))
        pos += 2 * n
        xs, ys = coords[0::2], coords[1::2]
        salida.append(" ".join(map(str, resolver(xs, ys, k))))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
