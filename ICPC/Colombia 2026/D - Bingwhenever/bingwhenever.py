"""
Colombia 2026 — D: Bingwhenever («Bingwhenever (bingo a cualquier hora)»)
Ejecutar: python bingwhenever.py < bingwhenever.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    N amigos juegan un bingo "asíncrono": cada uno tiene un cartón con K
    números distintos y REDIS publica la secuencia de B bolas. Gana (o ganan)
    quien complete su cartón en el primer paso en que alguien lo completa.

QUÉ HAY QUE HACER
    Entrada: varios casos; "N K B", N líneas "nombre n1 … nK" y una línea con
             las B bolas en orden. Termina con "0 0 0".
    Salida:  por caso, los nombres de los ganadores en orden lexicográfico,
             separados por un espacio.
    Restricciones clave: N, K <= 10^3 (hasta 10^6 números en cartones),
             B <= 10^6, números <= 10^9. Todo número de un cartón sale en
             alguna bola.

IDEA Y ALGORITMO
    No hace falta simular bola por bola. Si turno(x) es la posición en que
    sale la bola x, un jugador completa su cartón exactamente en el turno
        fin(jugador) = max{ turno(x) : x en su cartón }
    (es el momento en que sale el ÚLTIMO de sus números). Los ganadores son
    los jugadores con fin mínimo.
    → Tabla hash (dict) valor → turno, y un máximo por cartón.

    Simular marcando cartones bola por bola costaría O(B + N·K) igual, pero
    con mucho más trabajo en Python; el dict hace todo con funciones en C
    (dict(zip(...)), map, max), lo que importa con 10^6 números.

    Memoria: los cartones se guardan como la línea cruda (bytes) y se
    procesan cuando llegan las bolas: guardar 10^6 enteros sueltos ocuparía
    mucho más. Se lee un caso a la vez (no toda la entrada) por la misma
    razón: el archivo de prueba grande tiene ~20 MB.

MACROALGORITMO
    1. Leer "N K B" (fin si son 0 0 0).
    2. Leer las N líneas de jugadores (si una línea trae menos de K+1
       tokens, se le pegan las siguientes) y guardarlas crudas.
    3. Leer las B bolas (pueden venir en varias líneas) y construir
       turno = {valor: posición}.
    4. Para cada jugador: fin = max(turno[x] para x en su cartón).
    5. mejor = min(fin); ganadores = nombres con fin == mejor, ordenados.
    6. Imprimir los ganadores separados por un espacio.

COMPLEJIDAD
    O(N·K + B) por caso (más O(N log N) del ordenamiento de nombres).
    Memoria O(B + N·K). Archivo del usuario bingwhenever.in (19.8 MB,
    69 casos, incluido uno con N = K = 1000 y B = 10^6): ≈ 1.3 s.

EJEMPLO A MANO
    Bolas 4 5 7 3 2 10 11 15 → turnos 4:0, 5:1, 7:2, 3:3, 2:4, 10:5, 11:6,
    15:7. alice {3,7,10,15} → max(3,2,5,7) = 7; charles {2,7,11,15} → 7;
    bob {3,4,7,10} → max(3,0,2,5) = 5. Mínimo 5 → gana "bob".

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/D")
    - Fuerza bruta (simulación literal: se sacan las bolas una a una, se
      marcan los cartones y se para en el primer paso con algún cartón
      completo): idéntica en 2000 casos aleatorios pequeños.
    - Archivo grande del usuario (bingwhenever.in / .ans): idéntico.
"""
import sys
from itertools import repeat


def main():
    leer = sys.stdin.buffer.readline
    salida = []
    while True:
        linea = leer()
        if not linea:                       # EOF sin "0 0 0"
            break
        partes = linea.split()
        if not partes:                      # línea en blanco entre casos
            continue
        n, k, b = int(partes[0]), int(partes[1]), int(partes[2])
        if n == 0 and k == 0 and b == 0:    # fin de la entrada
            break

        # Jugadores: se guarda la línea cruda "nombre n1 … nK" (bytes).
        jugadores = []
        for _ in range(n):
            linea = leer()
            # Si el cartón viene partido en varias líneas, se juntan.
            while len(linea.split()) < k + 1:
                extra = leer()
                if not extra:
                    break
                linea += b" " + extra
            jugadores.append(linea)

        # Bolas en orden (pueden venir repartidas en varias líneas).
        bolas = leer().split()
        while len(bolas) < b:
            extra = leer()
            if not extra:
                break
            bolas += extra.split()

        # turno[valor] = posición (0, 1, 2, …) en que sale esa bola. Se
        # convierten a int para que "07" y "7" sean el mismo número. Se
        # recorre al revés para que, si una bola se repitiera (el enunciado
        # dice que no), quede su PRIMERA aparición.
        valores = list(map(int, bolas))
        del bolas
        turno = dict(zip(reversed(valores), range(len(valores) - 1, -1, -1)))
        del valores

        # fin = turno en que el jugador completa su cartón (el máximo turno
        # de sus números). El enunciado garantiza que todos salen; por
        # seguridad, un número ausente cuenta como "nunca" (turno b).
        obtener = turno.get
        fines = []
        for linea in jugadores:
            tokens = linea.split()
            # map en C: obtener(int(x), b) para cada número del cartón.
            fin = max(map(obtener, map(int, tokens[1:]), repeat(b)))
            fines.append((fin, tokens[0].decode()))

        mejor = min(f for f, _ in fines)
        ganadores = sorted(nombre for f, nombre in fines if f == mejor)
        salida.append(" ".join(ganadores))
        del jugadores, turno               # liberar memoria antes del siguiente caso

    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
