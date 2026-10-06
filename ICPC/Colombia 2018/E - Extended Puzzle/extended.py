"""
Colombia 2018 — E: Extended Puzzle («Rompecabezas extendido»)
Ejecutar: python extended.py < extended.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    El clásico «15-puzzle» generalizado a un marco de m filas × n columnas:
    fichas 1..mn−1 y un hueco (la ficha mn). Una jugada desliza una ficha
    vecina al hueco. ¿Se puede llegar a 1, 2, …, mn (hueco al final)?

QUÉ HAY QUE HACER
    Entrada: varios casos hasta fin de archivo: «m n» y m filas de n números
             (una permutación de 1..mn; el valor mn es el hueco).
    Salida:  «Y» si la configuración tiene solución, «N» si no.
    Restricciones clave: 1 < m·n ≤ 100 000 → hace falta O(mn) por caso;
             buscar en el espacio de estados es imposible.

IDEA Y ALGORITMO
    Invariante de paridad (el propio enunciado lo explica):
      paridad(permutación de las mn casillas, contando el hueco como mn)
      + paridad(distancia Manhattan del hueco a la esquina inferior derecha)
    es par en la configuración resuelta y no cambia con ninguna jugada
    (una jugada es una transposición —cambia la paridad de la
    permutación— y mueve el hueco una casilla —cambia la paridad de la
    distancia—). Para m, n ≥ 2 vale también el recíproco (teorema de Wilson
    sobre puzzles en grafos: en una cuadrícula 2-conexa bipartita se
    alcanzan exactamente las configuraciones pares; el caso 2×2 es un ciclo,
    pero ahí las rotaciones de 3 fichas son justo las permutaciones pares),
    así que «tiene solución ⇔ esa suma es par».
    - La paridad de una permutación de tamaño N se obtiene en O(N) sin
      contar inversiones: paridad = (N − número de ciclos) mód 2, porque un
      ciclo de longitud ℓ se escribe con ℓ−1 transposiciones.

    CASO ESPECIAL m = 1 o n = 1 (permitido porque sólo se pide m·n > 1):
    el marco es una línea; las fichas sólo pueden correrse y NUNCA cambian
    su orden relativo. Entonces hay solución ⇔ las fichas (sin el hueco)
    ya están en orden creciente. Aquí el criterio de paridad del enunciado
    falla (p. ej. 1×5 «2 1 4 3 5» tiene suma par pero no tiene solución),
    así que el enunciado exagera al afirmar el recíproco «para m × n» en
    general. Usamos la respuesta físicamente correcta; si el juez hubiera
    usado ciegamente la fórmula en marcos 1×n, las salidas diferirían en
    esos casos (no hay casos 1×n en el ejemplo).

MACROALGORITMO
    1. Leer m, n y los mn números (fila por fila = arreglo lineal).
    2. Si m = 1 o n = 1: quitar el hueco y verificar que la lista quede
       ordenada → Y/N.
    3. Si no: contar los ciclos de la permutación (arreglo de visitados).
    4. paridad_perm = (mn − ciclos) mód 2.
    5. Ubicar el hueco (valor mn) en (f, c); dist = (m−1−f) + (n−1−c).
    6. Imprimir Y si paridad_perm + dist es par, N si no.

COMPLEJIDAD
    Tiempo O(mn) por caso, memoria O(mn). Casos 316×316 y 1×100 000:
    ~0.15 s en total.

EJEMPLO A MANO
    2×3 «4 1 3 / 6 2 5»: inversiones 4>1, 4>3, 4>2, 3>2, 6>2, 6>5 = 6 (par);
    el hueco 6 está en (1,0), distancia 2 (par) → par → Y.
    2×3 «4 1 3 / 6 5 2»: 7 inversiones (impar) + 2 → impar → N.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/E")
    - Fuerza bruta: OK de forma EXHAUSTIVA (todas las configuraciones) para
      los marcos 1×2..1×7, 2×1..7×1, 2×2, 2×3, 3×2, 2×4, 4×2, comparando con
      un BFS sobre el espacio de estados desde la configuración resuelta.
"""
import sys


def paridad_permutacion(perm):
    """perm: lista con los valores 1..N. Devuelve (N − #ciclos) mód 2."""
    N = len(perm)
    visto = bytearray(N + 1)
    ciclos = 0
    for inicio in range(1, N + 1):
        if not visto[inicio]:
            ciclos += 1
            x = inicio
            # Seguimos el ciclo: posición x (1-indexada) contiene perm[x-1].
            while not visto[x]:
                visto[x] = 1
                x = perm[x - 1]
    return (N - ciclos) & 1


def resolver(m, n, valores):
    total = m * n
    if m == 1 or n == 1:
        # Marco lineal: las fichas no pueden adelantarse unas a otras.
        fichas = [v for v in valores if v != total]
        return all(fichas[i] < fichas[i + 1] for i in range(len(fichas) - 1))
    pos_hueco = valores.index(total)
    fila, col = divmod(pos_hueco, n)
    distancia = (m - 1 - fila) + (n - 1 - col)
    return (paridad_permutacion(valores) + distancia) % 2 == 0


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        m, n = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        valores = list(map(int, datos[pos:pos + m * n]))
        pos += m * n
        salida.append("Y" if resolver(m, n, valores) else "N")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
