"""
Colombia 2017 — A: A Contest to Meet («Un concurso para encontrarse»)
Ejecutar: python acm.py < acm.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un reality ubica a tres concursantes en intersecciones aleatorias de una
    ciudad y deben reunirse en alguna intersección. Cada uno camina a una
    velocidad conocida. La TV quiere saber cuánto debe durar la transmisión
    para cubrir el recorrido sin importar dónde empiecen ni dónde se reúnan.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta EOF. Cada caso: N S, luego S calles "i j d"
             (bidireccionales, longitud d metros) y una línea "sA sB sC" con
             las velocidades (metros/minuto).
    Salida:  por caso, un entero: minutos en el PEOR escenario, redondeados
             hacia arriba (techo; 2.9 -> 3, 3.2 -> 4, 8.0 -> 8).
    Restricciones clave: N <= 100, S <= 9000, d <= 200, 50 <= s <= 100.

IDEA Y ALGORITMO
    "Peor escenario" se toma sobre TODO lo desconocido: las tres posiciones
    iniciales Y la intersección de encuentro (así lo confirma el ejemplo 3:
    con un nodo central a 200 m de todos, si se pudiera elegir el punto de
    encuentro la respuesta sería 4, pero la esperada es 8 = 400/50).
    Cada concursante camina por el camino más corto, así que el tiempo total
    es max_i dist(inicio_i, encuentro)/s_i. Maximizar eso sobre todas las
    elecciones es simplemente:
        max_{u,v} dist(u, v) / min(sA, sB, sC)
    porque basta poner al más lento en u y el encuentro en v (los otros dos
    tardan menos o igual). Es decir: DIÁMETRO del grafo / velocidad mínima.
    Distancias entre todos los pares: Floyd–Warshall (N <= 100).
    El redondeo hacia arriba se hace con enteros: ceil(D/s) = (D + s - 1)//s,
    sin errores de punto flotante.

MACROALGORITMO
    1. Leer todos los tokens; procesar casos mientras queden datos.
    2. Armar la matriz de distancias (INF fuera de las calles, 0 diagonal).
    3. Floyd–Warshall para las distancias mínimas entre todo par.
    4. D = máxima distancia entre dos intersecciones (diámetro).
    5. s = min(sA, sB, sC); imprimir ceil(D / s).

COMPLEJIDAD
    Tiempo O(N^3) por caso (10^6 operaciones con N = 100; con el truco de
    recorrer filas como listas: 5 casos con N = 100 y 4950 calles en 0.42 s).
    Memoria O(N^2).

EJEMPLO A MANO
    Caso 2: 0-1 (100), 1-2 (80). Diámetro = dist(0,2) = 180, velocidad
    mínima 50 -> 3.6 -> 4. Correcto.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/A")
    - Fuerza bruta: OK en 500 casos aleatorios (N <= 6): Bellman-Ford +
      máximo literal sobre las 4-tuplas (a, b, c, encuentro) con Fracciones.
"""
import sys


def floyd_warshall(n, dist):
    """Distancias mínimas entre todo par (modifica 'dist' en sitio)."""
    for k in range(n):
        fila_k = dist[k]
        for i in range(n):
            fila_i = dist[i]
            dik = fila_i[k]
            # Relajar i -> k -> j para todo j usando la fila k completa.
            for j in range(n):
                nd = dik + fila_k[j]
                if nd < fila_i[j]:
                    fila_i[j] = nd
    return dist


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    INF = float("inf")
    while pos + 1 < len(datos):
        n, s = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for _ in range(s):
            i, j, d = int(datos[pos]), int(datos[pos + 1]), int(datos[pos + 2])
            pos += 3
            # Calles bidireccionales; por si acaso nos quedamos con la menor.
            if d < dist[i][j]:
                dist[i][j] = dist[j][i] = d
        velocidades = [int(datos[pos]), int(datos[pos + 1]), int(datos[pos + 2])]
        pos += 3

        floyd_warshall(n, dist)
        # Diámetro: la peor pareja (inicio del más lento, punto de encuentro).
        diametro = max(max(fila) for fila in dist)
        v_min = min(velocidades)
        # Techo entero de diametro / v_min (sin flotantes).
        salida.append(str((diametro + v_min - 1) // v_min))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
