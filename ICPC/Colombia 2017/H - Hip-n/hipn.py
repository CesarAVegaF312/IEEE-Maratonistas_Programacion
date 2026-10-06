"""
Colombia 2017 — H: Hip-n («Hip-n»)
Ejecutar: python hipn.py < hipn.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Dos jugadores ponen fichas por turnos en un tablero n x n. Pierde el
    primero que tenga cuatro fichas PROPIAS en los vértices de un cuadrado
    (de cualquier tamaño y en cualquier inclinación). Si se llena el tablero
    sin que nadie pierda, es empate.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta EOF; cada uno: n y luego n^2 parejas "r c"
             (jugadas alternadas, empieza el jugador 1).
    Salida:  por caso, 0 si hay empate, 1 si pierde el jugador 1, 2 si
             pierde el jugador 2.
    Restricciones clave: n <= 200, es decir, hasta 40000 jugadas.

IDEA Y ALGORITMO
    Basta revisar, en cada jugada, los cuadrados que tienen como vértice la
    ficha recién puesta p (los demás ya se habrían detectado antes).
    Representación: un cuadrado con vértice p se describe con el vector v
    hacia uno de sus vecinos: vértices p, q = p+v, p+rot(v), q+rot(v), donde
    rot gira 90°. Todo cuadrado con vértice p tiene dos vecinos de p, q1 y q2,
    con q2 - p = rot(q1 - p) o q1 - p = rot(q2 - p); por eso basta con UNA
    orientación de rot si probamos q = cada ficha propia (q1 y q2 son
    propias, así que alguna de las dos lo detecta).
    Por lo tanto: para cada ficha propia q ya puesta, se calculan los otros
    dos vértices y se miran en el tablero: O(fichas propias) por jugada.
    Truco de implementación: tablero aplanado (bytearray) con un BORDE de n
    casillas vacías por cada lado, así p+rot(v) y q+rot(v) siempre caen
    dentro del arreglo sin comprobar límites, y rot(v) es un simple
    desplazamiento de índice:  v = (a, b)  ->  rot(v) = (-b, a)  ->
    delta = a - b*ANCHO.
    ¿Por qué no es O(n^4)? Un jugador con muchas fichas forma cuadrados muy
    rápido: con densidad rho hay ~rho^4 * n^4/12 cuadrados propios esperados,
    así que en partidas "normales" alguien pierde tras ~2n fichas por
    jugador. Sólo partidas construidas para evitar cuadrados duran mucho.

MACROALGORITMO
    1. Leer n y las n^2 jugadas.
    2. Tablero (3n x 3n) con 0 = libre, 1/2 = dueño; listas de fichas por
       jugador (índice y coordenadas).
    3. Para cada jugada p del jugador j: para cada ficha propia q,
       a = fila(q)-fila(p), b = col(q)-col(p), delta = a - b*ANCHO;
       si tablero[p+delta] == j y tablero[q+delta] == j -> j pierde.
    4. Si no perdió, marcar p y agregarla a la lista de j.
    5. Si nadie pierde, imprimir 0.

COMPLEJIDAD
    Tiempo O(sum de fichas propias) = O(T^2) con T = jugadas hasta que
    alguien pierde; memoria O(n^2).
    Medido (n = 200): 3 partidas aleatorias -> 0.21 s en total (terminan en
    pocas centenas de jugadas). Partidas adversarias generadas con un voraz
    que elige casillas que NO forman cuadrado: 3935 jugadas sin cuadrado ->
    1.2 s; 5887 jugadas sin cuadrado -> 2.1 s. Si un juez tuviera partidas
    con decenas de miles de jugadas sin cuadrado (cuadrático), Python sería
    lento; no parece posible llegar tan lejos en un tablero de 200 x 200.

EJEMPLO A MANO
    Caso 2: el jugador 1 pone (1,0), (2,1), (0,1) y luego (1,2): esos cuatro
    son un cuadrado inclinado 45° -> pierde el jugador 1.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/H")
    - Fuerza bruta: OK en 600 partidas aleatorias (n <= 6, a veces con
      jugadas elegidas para evitar cuadrados y llegar a empates): tras cada
      jugada se revisan TODAS las 4-tuplas de fichas del jugador con una
      prueba geométrica de cuadrado (4 lados iguales + 2 diagonales iguales).
"""
import sys


def perdedor(n, jugadas):
    """jugadas: lista plana [r0, c0, r1, c1, ...]. Devuelve 0, 1 o 2."""
    ancho = 3 * n
    tablero = bytearray(ancho * ancho)
    # Por jugador: listas paralelas (índice aplanado, fila, columna).
    idx = [None, [], []]
    fil = [None, [], []]
    col = [None, [], []]
    jugador = 1
    for k in range(0, 2 * n * n, 2):
        r, c = jugadas[k], jugadas[k + 1]
        ip = (r + n) * ancho + (c + n)
        lista_i, lista_r, lista_c = idx[jugador], fil[jugador], col[jugador]
        for t in range(len(lista_i)):
            a = lista_r[t] - r
            b = lista_c[t] - c
            delta = a - b * ancho        # desplazamiento de rot(q - p)
            if tablero[ip + delta] == jugador and tablero[lista_i[t] + delta] == jugador:
                return jugador           # formó un cuadrado con sus fichas
        tablero[ip] = jugador
        lista_i.append(ip)
        lista_r.append(r)
        lista_c.append(c)
        jugador = 3 - jugador
    return 0


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos])
        pos += 1
        jugadas = list(map(int, datos[pos:pos + 2 * n * n]))
        pos += 2 * n * n
        salida.append(str(perdedor(n, jugadas)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
