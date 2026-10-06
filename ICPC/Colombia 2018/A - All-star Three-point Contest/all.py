"""
Colombia 2018 — A: All-star Three-point Contest («Concurso de triples del Juego de las Estrellas»)
Ejecutar: python all.py < all.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En el concurso de triples de un All-Star cada jugador lanza 25 balones
    desde 5 posiciones (5 por posición). Cada enceste vale 1 punto, salvo el
    último balón de cada posición, que vale 2. Hay que publicar la tabla final.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta fin de archivo. Cada caso: una línea con P
             (0 < P < 101) y P líneas «Nombre;# # # # #;...;# # # # #»
             (5 bloques de 5 ceros/unos). El nombre puede tener espacios.
    Salida:  «Case N:» y luego P líneas «Nombre puntos», ordenadas por puntos
             descendente y, en empate, por nombre en orden lexicográfico
             ascendente SIN distinguir mayúsculas/minúsculas.
    Restricciones clave: P ≤ 100, así que cualquier ordenamiento sirve.

IDEA Y ALGORITMO
    Simulación + ordenamiento con clave compuesta.
    - Puntaje de un bloque «b1 b2 b3 b4 b5» = b1+b2+b3+b4 + 2·b5.
    - Se ordena con la clave (-puntos, nombre.lower()). Usar -puntos hace que
      el orden ascendente de Python sea descendente en puntos; nombre.lower()
      implementa la comparación «case-insensitive». Se añade el nombre
      original como tercer criterio sólo para que el orden sea determinista
      si dos nombres difieren únicamente en mayúsculas (el enunciado no lo
      especifica; no ocurre en el ejemplo).
    - Hay que leer por LÍNEAS (no por tokens) porque el nombre tiene espacios
      y el separador real es ';'.

MACROALGORITMO
    1. Leer todas las líneas no vacías.
    2. Mientras queden líneas: leer P.
    3. Para cada una de las P líneas, separar por ';' → nombre y 5 bloques.
    4. Sumar cada bloque con el último lanzamiento valiendo doble.
    5. Ordenar por (-puntos, nombre en minúsculas, nombre).
    6. Imprimir «Case k:» y las líneas «nombre puntos».

COMPLEJIDAD
    Tiempo O(P log P) por caso; memoria O(P). Instantáneo.

EJEMPLO A MANO
    «Michael Jordan;0 1 1 0 1;0 1 1 0 1;0 1 1 0 1;0 0 0 0 1;0 0 0 0 1»
    → bloques 4,4,4,2,2 = 16.  Caso 3: «charl es» < «charle s» < «charles»
    porque el espacio (ASCII 32) es menor que cualquier letra.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/A")
    - Fuerza bruta: no aplica (es una simulación directa; el único punto
      delicado, el desempate case-insensitive con espacios, está cubierto por
      el caso 3 del ejemplo).
"""
import sys


def puntaje_bloque(bloque):
    """Puntos de una posición: los 4 primeros valen 1, el último vale 2."""
    tiros = [int(t) for t in bloque.split()]
    return sum(tiros[:4]) + 2 * tiros[4]


def main():
    # Leemos por líneas: el nombre del jugador contiene espacios.
    lineas = [l.rstrip("\r\n") for l in sys.stdin.read().split("\n")]
    lineas = [l for l in lineas if l.strip() != ""]
    salida = []
    i = 0
    caso = 0
    while i < len(lineas):
        p = int(lineas[i])
        i += 1
        caso += 1
        jugadores = []
        for _ in range(p):
            partes = lineas[i].split(";")
            i += 1
            nombre = partes[0].strip()
            puntos = sum(puntaje_bloque(b) for b in partes[1:6])
            jugadores.append((puntos, nombre))
        # Orden: más puntos primero; empate → nombre sin distinguir mayúsculas.
        jugadores.sort(key=lambda j: (-j[0], j[1].lower(), j[1]))
        salida.append("Case %d:" % caso)
        for puntos, nombre in jugadores:
            salida.append("%s %d" % (nombre, puntos))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
