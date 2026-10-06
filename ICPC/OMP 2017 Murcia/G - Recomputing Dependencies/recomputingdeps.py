"""
OMP 2017 Murcia — G: Recomputing Dependencies («Recalculando dependencias»)
Ejecutar: python recomputingdeps.py < recomputingdeps.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Grupos de carros viajan a la costa; algunos carros siguen a otro carro
    que va p posiciones más adelante. Durante el viaje se meten carros nuevos
    en medio, así que hay que recalcular a cuántas posiciones queda ahora el
    carro al que cada uno sigue.

QUÉ HAY QUE HACER
    Entrada: varias líneas, terminadas por una línea "0". Cada línea es una
    fila de fichas separadas por espacios:
        '-'  carro original sin dependencia,
        p    carro original que sigue al carro original p posiciones adelante
             (contando SOLO carros originales), 0 < p < 1000,
        '#'  carro nuevo que se metió en esa posición.
    Salida:  la misma fila, con cada número p sustituido por la distancia
    real (contando también los '#') hasta el carro que sigue.
    Restricciones clave: no se dan límites de longitud; la solución es
    lineal en el número de fichas.

IDEA Y ALGORITMO
    Reindexación con un arreglo de posiciones (simulación directa).
    "Más adelante" = más a la izquierda en la línea (en el ejemplo, el carro
    5 sigue al carro 2 con p = 3). Si numeramos los carros ORIGINALES
    0, 1, 2, … (saltando los '#') y guardamos en pos[k] la posición final
    (índice de ficha, contando '#') del carro original k, entonces el carro
    original k con dependencia p sigue al carro original k - p y su nueva
    distancia es pos[k] - pos[k - p]. Los '#' no cambian el orden relativo
    de los originales, solo los separan: por eso basta esta resta.
    Caso no especificado: si k - p < 0 (el carro seguido no está en la
    línea) se deja el número original tal cual.

MACROALGORITMO
    1. Leer líneas hasta encontrar "0" (o el fin de la entrada).
    2. Partir la línea en fichas.
    3. Recorrer las fichas: cada ficha que no sea '#' es un carro original;
       guardar su índice de ficha en pos.
    4. Recorrer de nuevo: para cada número p del carro original k,
       sustituirlo por pos[k] - pos[k - p].
    5. Imprimir las fichas separadas por un espacio.

COMPLEJIDAD
    Tiempo O(L) por línea (L = número de fichas), memoria O(L).
    Caso grande (20 líneas de 100 000 fichas): ~0.65 s.

EJEMPLO A MANO
    "- - # # - # - 3 2 -": originales en las posiciones de ficha
    pos = [0, 1, 4, 6, 7, 8, 9]. El carro original 4 (ficha 7, p = 3) sigue
    al original 1 (ficha 1): 7 - 1 = 6. El original 5 (ficha 8, p = 2) sigue
    al original 3 (ficha 6): 8 - 6 = 2. Salida "- - # # - # - 6 2 -".

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "OMP 2017/G")
    - Fuerza bruta: OK en 500 líneas aleatorias contra una simulación con
      identificadores de carro (se asigna un id a cada carro original, se
      busca con list.index la posición del carro seguido, O(L²)).
"""
import sys


def recalcular(fichas):
    """Devuelve la lista de fichas con las distancias recalculadas."""
    # pos[k] = índice (en la línea final) del k-ésimo carro original.
    pos = [i for i, f in enumerate(fichas) if f != "#"]
    resultado = list(fichas)
    k = -1                        # índice del carro original actual
    for i, f in enumerate(fichas):
        if f == "#":
            continue              # carro nuevo: no tiene dependencias
        k += 1
        if f == "-":
            continue              # carro original sin dependencia
        p = int(f)
        objetivo = k - p          # carro original al que sigue
        if 0 <= objetivo:
            resultado[i] = str(pos[k] - pos[objetivo])
        # si objetivo < 0 (no especificado) se deja el número como venía
    return resultado


def main():
    salida = []
    for linea in sys.stdin.read().split("\n"):
        fichas = linea.split()
        if not fichas:
            continue              # líneas vacías: se ignoran
        if fichas == ["0"]:
            break                 # fin de la entrada
        salida.append(" ".join(recalcular(fichas)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
