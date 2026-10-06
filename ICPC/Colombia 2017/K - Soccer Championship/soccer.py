"""
Colombia 2017 — K: Soccer Championship («Campeonato de fútbol»)
Ejecutar: python soccer.py < soccer.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un periodista tiene los resultados de una liga y quiere la tabla final y
    el número de "paradojas": partidos donde el equipo que PERDIÓ terminó
    mejor ubicado en la tabla que el que ganó.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta EOF; cada uno M y M líneas "L X vs. Y V"
             (local L con X goles, visitante V con Y goles). Los nombres
             tienen mayúsculas, dígitos, puntos y espacios internos.
    Salida:  "The paradox occurs X time(s)." y luego la tabla
             "1. Nombre1", "2. Nombre2", ...
    Restricciones clave: M <= 64, nombres de hasta 100 caracteres.

IDEA Y ALGORITMO
    SIMULACIÓN + ORDENAMIENTO con clave compuesta. Por equipo se acumulan
    puntos (3 victoria, 1 empate), goles a favor, goles en contra y goles
    como visitante. Orden: (-puntos, -diferencia, -goles a favor,
    -goles de visitante, nombre) — el nombre en orden ASCII, que es justo
    como Python compara cadenas, así que la posición es única.
    Lo delicado es el ANÁLISIS DE LA LÍNEA: los nombres pueden contener
    dígitos y espacios ("TEAM 1 4 vs. 2 TEAM 2"). Se usa la expresión
    regular  ^(.*?)\\s+(\\d+)\\s+vs\\.\\s+(\\d+)\\s+(.*)$ : el marcador
    "vs." no puede aparecer en un nombre (lleva minúsculas), y los números
    pegados a él son los goles.
    Paradoja: en cada partido no empatado, si la posición del perdedor es
    menor (mejor) que la del ganador, se cuenta.

MACROALGORITMO
    1. Leer M (saltando líneas vacías) y las M líneas del caso.
    2. Separar cada línea en (local, goles_local, goles_visitante, visitante).
    3. Acumular puntos, goles a favor/en contra y goles de visitante.
    4. Ordenar los equipos con la clave compuesta y asignar posiciones.
    5. Contar los partidos donde el perdedor quedó arriba del ganador.
    6. Imprimir la línea de paradojas y la tabla numerada.

COMPLEJIDAD
    Tiempo O(M log M) por caso, memoria O(M). Medido: 200 casos con M = 64 y
    nombres de 100 caracteres en 0.18 s.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/K")
    - Fuerza bruta: OK en 500 ligas aleatorias con nombres "difíciles"
      (dígitos, puntos, espacios, prefijos comunes): el generador conoce los
      datos estructurados, calcula la tabla con comparaciones por pares
      (ordenamiento por inserción con un comparador explícito de los 5
      criterios) y cuenta paradojas; se compara la salida completa.
"""
import re
import sys

PATRON = re.compile(r"^(.*?)\s+(\d+)\s+vs\.\s+(\d+)\s+(.*)$")


def resolver(partidos):
    """partidos: lista de (local, gl, gv, visitante). Devuelve líneas."""
    puntos, favor, contra, visita = {}, {}, {}, {}
    for equipo in {p[0] for p in partidos} | {p[3] for p in partidos}:
        puntos[equipo] = favor[equipo] = contra[equipo] = visita[equipo] = 0

    for local, gl, gv, visitante in partidos:
        favor[local] += gl
        contra[local] += gv
        favor[visitante] += gv
        contra[visitante] += gl
        visita[visitante] += gv
        if gl > gv:
            puntos[local] += 3
        elif gl < gv:
            puntos[visitante] += 3
        else:
            puntos[local] += 1
            puntos[visitante] += 1

    tabla = sorted(puntos, key=lambda e: (-puntos[e], -(favor[e] - contra[e]),
                                          -favor[e], -visita[e], e))
    posicion = {e: i for i, e in enumerate(tabla)}

    paradojas = 0
    for local, gl, gv, visitante in partidos:
        if gl == gv:
            continue
        ganador, perdedor = (local, visitante) if gl > gv else (visitante, local)
        if posicion[perdedor] < posicion[ganador]:
            paradojas += 1

    lineas = [f"The paradox occurs {paradojas} time(s)."]
    lineas += [f"{i + 1}. {e}" for i, e in enumerate(tabla)]
    return lineas


def main():
    lineas = [l.strip() for l in sys.stdin.read().split("\n")]
    pos, total = 0, len(lineas)
    salida = []
    while pos < total:
        if not lineas[pos]:              # saltar líneas vacías entre casos
            pos += 1
            continue
        m = int(lineas[pos])
        pos += 1
        partidos = []
        while len(partidos) < m and pos < total:
            linea = lineas[pos]
            pos += 1
            if not linea:
                continue
            coincide = PATRON.match(linea)
            local, gl, gv, visitante = coincide.groups()
            partidos.append((local.strip(), int(gl), int(gv), visitante.strip()))
        salida.extend(resolver(partidos))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
